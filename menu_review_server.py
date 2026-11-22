#!/usr/bin/env python3
"""Serve the local menu/media review UIs and their API endpoints."""

from __future__ import annotations

import argparse
from collections import Counter
from contextlib import closing
import hashlib
import json
import os
import re
import sqlite3
import tempfile
import urllib.error
import urllib.request
from datetime import datetime, timezone
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, unquote, urlsplit


ROOT = Path(__file__).resolve().parent
PAGES = ROOT / "pages"
EXPLORER_PAGE = "Menu explorer — Inn Collection Group.html"
MENUS = ROOT / "inncollectiongroup.com_root" / "menus_md"
PDFS = ROOT / "inncollectiongroup.com_root" / "documents" / "extracted-to-md"
EXPORTS = ROOT / "exports"
REVIEW_DB = ROOT / "menu_review_state.sqlite3"
MAX_EXPORT_REQUEST_BYTES = 32 * 1024 * 1024
MAX_EXPORT_ITEMS = 20_000
ASSET_HOST = "www.inncollectiongroup.com"
ISSUE_IDS = {"headings", "list_entries", "pdf_missing", "repeated_lines", "unusual_chars"}
JSON_BODY_ERROR = object()


class SameHostRedirectHandler(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, request, response, code, message, headers, new_url):
        try:
            target = urlsplit(new_url)
            port = target.port
        except ValueError:
            return None
        if (
            target.scheme != "https"
            or target.hostname != ASSET_HOST
            or port not in (None, 443)
            or target.username is not None
            or target.password is not None
        ):
            return None
        return super().redirect_request(request, response, code, message, headers, new_url)


def safe_folder_name(value: str) -> str:
    value = re.sub(r"\s*/\s*", " - ", value.strip())
    value = re.sub(r"[^A-Za-z0-9 .,'&()_-]+", "_", value).strip(" ._-")
    if not value or value in {".", ".."}:
        raise ValueError("Region and venue names must contain valid characters")
    return value[:120]


def export_filename(url: str, used: set[str]) -> str:
    base = unquote(Path(urlsplit(url).path).name)
    base = re.sub(r"[^\w.-]+", "_", base, flags=re.UNICODE).strip(" ._")[:160] or "file"
    name = base
    index = 2
    while name.casefold() in used:
        stem, suffix = (base.rsplit(".", 1) if "." in base else (base, ""))
        name = f"{stem}-{index}{'.' + suffix if suffix else ''}"
        index += 1
    used.add(name.casefold())
    return name


def download_asset(urls: list[str], destination: Path, opener) -> str:
    errors = []
    temporary = destination.with_name(destination.name + ".part")
    for url in urls:
        try:
            request = urllib.request.Request(
                url, headers={"User-Agent": "InnCollectionGroup-MediaExporter/1.0"}
            )
            with opener.open(request, timeout=30) as response, temporary.open("xb") as output:
                while chunk := response.read(64 * 1024):
                    output.write(chunk)
            temporary.replace(destination)
            return url
        except (urllib.error.URLError, TimeoutError, OSError) as error:
            temporary.unlink(missing_ok=True)
            errors.append(str(error))
    raise urllib.error.URLError("All candidate URLs failed: " + "; ".join(errors))


def menu_kind(filename: str) -> str:
    name = filename.lower()
    if "drink" in name or "wine-list" in name:
        return "Drinks"
    if "sunday" in name:
        return "Sunday"
    if "menu" in name:
        return "Food"
    if "christmas" in name or "party" in name:
        return "Events"
    return "Other"


class MenuReviewHandler(BaseHTTPRequestHandler):
    server_version = "MenuReview/1.0"

    def do_POST(self) -> None:
        path = urlsplit(self.path).path
        if path not in ("/api/export", "/api/issues", "/api/issues/fix-duplicates"):
            self.send_error(404, "Not found")
            return
        payload = self._read_json_body()
        if payload is JSON_BODY_ERROR:
            return
        if path == "/api/issues":
            self._save_issue_review(payload)
            return
        if path == "/api/issues/fix-duplicates":
            self._remove_duplicate_lines(payload)
            return

        items = payload.get("items") if isinstance(payload, dict) else None
        if not isinstance(items, list) or not items:
            self._send_json({"error": "Select at least one asset to export"}, status=400)
            return
        if len(items) > MAX_EXPORT_ITEMS:
            self._send_json(
                {"error": f"An export can contain at most {MAX_EXPORT_ITEMS} assets"},
                status=413,
            )
            return

        try:
            validated = [self._validate_export_item(item) for item in items]
        except ValueError as error:
            self._send_json({"error": str(error)}, status=400)
            return

        try:
            result = self._export_items(validated)
        except OSError as error:
            self._send_json({"error": f"Could not create export files: {error}"}, status=500)
            return
        self._send_json(result, status=207 if result["failed"] else 200)

    def do_GET(self) -> None:
        request = urlsplit(self.path)
        if request.path == "/":
            self.send_response(302)
            self.send_header("Location", "/pages/menu-review.html")
            self.end_headers()
            return
        if request.path in (
            "/pages/menu-review.html",
            "/pages/discovered-media.html",
            "/pages/fnb-crosscheck.html",
            "/pages/launch-readiness.html",
            "/pages/product-data.html",
        ):
            self._send_file(PAGES / request.path.rsplit("/", 1)[-1], "text/html; charset=utf-8")
            return
        if request.path == "/pages/menu-explorer.html":
            self._send_file(PAGES / EXPLORER_PAGE, "text/html; charset=utf-8")
            return
        if request.path == "/pages/menu-explorer-data.js":
            self._send_file(PAGES / "menu-explorer-data.js", "text/javascript; charset=utf-8")
            return
        if request.path == "/inncollectiongroup.com_root/discovered_media.csv":
            self._send_file(
                ROOT / "inncollectiongroup.com_root" / "discovered_media.csv",
                "text/csv; charset=utf-8",
            )
            return
        if request.path == "/api/menus":
            self._send_json(self._menu_index())
            return
        if request.path == "/api/issues":
            name = self._query_name(request.query)
            if name is None or not self._known_menu(name):
                self._send_json({"error": "Menu not found"}, status=404)
                return
            self._get_issue_reviews(name)
            return
        if request.path == "/api/menu":
            name = self._query_name(request.query)
            if name is None or not self._known_menu(name):
                self.send_error(404, "Menu not found")
                return
            try:
                _, content, source_hash = self._issue_source(name)
            except OSError as error:
                self.send_error(500, f"Could not read requested menu: {error}")
                return
            self._send_bytes(
                content,
                "text/markdown; charset=utf-8",
                headers={"X-Source-Hash": source_hash},
            )
            return
        if request.path == "/api/pdf":
            name = self._query_name(request.query)
            if name is None or not self._known_menu(name):
                self.send_error(404, "PDF not found")
                return
            pdf = PDFS / f"{Path(name).stem}.pdf"
            if not pdf.is_file():
                self.send_error(404, "PDF not found")
                return
            self._send_file(pdf, "application/pdf", disposition="inline")
            return
        self.send_error(404, "Not found")

    @staticmethod
    def _query_name(query: str) -> str | None:
        values = parse_qs(query).get("name", [])
        return values[0] if len(values) == 1 else None

    @staticmethod
    def _known_menu(name: str) -> bool:
        return Path(name).name == name and name.endswith(".md") and (MENUS / name).is_file()

    @staticmethod
    def _menu_index() -> list[dict[str, object]]:
        entries = []
        for path in sorted(MENUS.glob("*.md"), key=lambda item: item.name.casefold()):
            pdf = PDFS / f"{path.stem}.pdf"
            entries.append(
                {
                    "name": path.name,
                    "kind": menu_kind(path.name),
                    "hasPdf": pdf.is_file(),
                    "bytes": path.stat().st_size,
                }
            )
        return entries

    def _send_json(self, value: object, status: int = 200) -> None:
        data = json.dumps(value, ensure_ascii=False).encode("utf-8")
        self._send_bytes(data, "application/json; charset=utf-8", status=status)

    def _read_json_body(self) -> object:
        if self.headers.get_content_type() != "application/json":
            self._send_json({"error": "Content-Type must be application/json"}, status=415)
            return JSON_BODY_ERROR
        try:
            content_length = int(self.headers.get("Content-Length", ""))
        except ValueError:
            self._send_json({"error": "A valid Content-Length header is required"}, status=400)
            return JSON_BODY_ERROR
        if content_length < 0 or content_length > MAX_EXPORT_REQUEST_BYTES:
            self._send_json({"error": "Request body is too large"}, status=413)
            return JSON_BODY_ERROR
        try:
            return json.loads(self.rfile.read(content_length))
        except (json.JSONDecodeError, UnicodeDecodeError):
            self._send_json({"error": "Request body must be valid JSON"}, status=400)
            return JSON_BODY_ERROR

    @staticmethod
    def _issue_source(name: str) -> tuple[Path, bytes, str]:
        path = MENUS / name
        content = path.read_bytes()
        return path, content, hashlib.sha256(content).hexdigest()

    @staticmethod
    def _review_connection() -> sqlite3.Connection:
        connection = sqlite3.connect(REVIEW_DB)
        connection.execute(
            """CREATE TABLE IF NOT EXISTS issue_reviews (
                menu_name TEXT NOT NULL,
                source_hash TEXT NOT NULL,
                issue_id TEXT NOT NULL,
                status TEXT NOT NULL,
                note TEXT NOT NULL DEFAULT '',
                updated_at TEXT NOT NULL,
                PRIMARY KEY (menu_name, source_hash, issue_id)
            )"""
        )
        return connection

    def _get_issue_reviews(self, name: str) -> None:
        try:
            _, _, source_hash = self._issue_source(name)
            with closing(self._review_connection()) as connection, connection:
                rows = connection.execute(
                    "SELECT issue_id, status, note FROM issue_reviews "
                    "WHERE menu_name = ? AND source_hash = ?",
                    (name, source_hash),
                ).fetchall()
        except (OSError, sqlite3.Error) as error:
            self._send_json({"error": f"Could not load issue review: {error}"}, status=500)
            return
        self._send_json(
            {
                "name": name,
                "sourceHash": source_hash,
                "decisions": {
                    issue_id: {"status": status, "note": note}
                    for issue_id, status, note in rows
                },
            }
        )

    def _save_issue_review(self, payload: object) -> None:
        if not isinstance(payload, dict):
            self._send_json({"error": "Request body must be an object"}, status=400)
            return
        name, issue_id = payload.get("name"), payload.get("issueId")
        status, note, source_hash = payload.get("status"), payload.get("note", ""), payload.get("sourceHash")
        if not isinstance(name, str) or not self._known_menu(name):
            self._send_json({"error": "Menu not found"}, status=404)
            return
        if (
            not isinstance(issue_id, str)
            or issue_id not in ISSUE_IDS
            or not isinstance(status, str)
            or status not in {"open", "fixed", "intentional"}
        ):
            self._send_json({"error": "Invalid issue or review status"}, status=400)
            return
        if not isinstance(note, str) or len(note) > 4000:
            self._send_json({"error": "Review note must be 4000 characters or fewer"}, status=400)
            return
        try:
            _, _, current_hash = self._issue_source(name)
        except OSError as error:
            self._send_json({"error": f"Could not read menu: {error}"}, status=500)
            return
        if source_hash != current_hash:
            self._send_json({"error": "Menu changed since this review was opened; reload and try again"}, status=409)
            return
        try:
            with closing(self._review_connection()) as connection, connection:
                connection.execute(
                    """INSERT INTO issue_reviews
                       (menu_name, source_hash, issue_id, status, note, updated_at)
                       VALUES (?, ?, ?, ?, ?, ?)
                       ON CONFLICT(menu_name, source_hash, issue_id) DO UPDATE SET
                       status = excluded.status, note = excluded.note, updated_at = excluded.updated_at""",
                    (name, current_hash, issue_id, status, note, datetime.now(timezone.utc).isoformat()),
                )
        except sqlite3.Error as error:
            self._send_json({"error": f"Could not save issue review: {error}"}, status=500)
            return
        self._send_json({"name": name, "issueId": issue_id, "status": status, "sourceHash": current_hash})

    def _remove_duplicate_lines(self, payload: object) -> None:
        if not isinstance(payload, dict):
            self._send_json({"error": "Request body must be an object"}, status=400)
            return
        name, source_hash, line_numbers, note = (
            payload.get("name"),
            payload.get("sourceHash"),
            payload.get("lineNumbers"),
            payload.get("note", ""),
        )
        if not isinstance(name, str) or not self._known_menu(name):
            self._send_json({"error": "Menu not found"}, status=404)
            return
        if (
            not isinstance(line_numbers, list)
            or not line_numbers
            or len(line_numbers) > 10_000
            or not all(type(number) is int and number > 0 for number in line_numbers)
        ):
            self._send_json({"error": "Select one or more valid duplicate line numbers"}, status=400)
            return
        if len(set(line_numbers)) != len(line_numbers):
            self._send_json({"error": "Duplicate line numbers were provided"}, status=400)
            return
        if not isinstance(note, str) or len(note) > 4000:
            self._send_json({"error": "Review note must be 4000 characters or fewer"}, status=400)
            return
        try:
            path, content, current_hash = self._issue_source(name)
        except OSError as error:
            self._send_json({"error": f"Could not read menu: {error}"}, status=500)
            return
        if source_hash != current_hash:
            self._send_json({"error": "Menu changed since this review was opened; reload and try again"}, status=409)
            return
        try:
            text = content.decode("utf-8")
        except UnicodeDecodeError:
            self._send_json({"error": "Menu is not valid UTF-8 and cannot be edited safely"}, status=500)
            return

        lines = text.splitlines(keepends=True)
        seen: set[str] = set()
        removable = set()
        for number, line in enumerate(lines, start=1):
            normalized = line.strip().lower()
            if len(normalized) > 12:
                if normalized in seen:
                    removable.add(number)
                else:
                    seen.add(normalized)
        if not set(line_numbers).issubset(removable):
            self._send_json(
                {"error": "One or more selected lines are no longer repeated; reload the menu"},
                status=409,
            )
            return

        updated_text = "".join(line for number, line in enumerate(lines, start=1) if number not in line_numbers)
        temporary_path = None
        try:
            with tempfile.NamedTemporaryFile(
                mode="wb", dir=path.parent, prefix=f".{path.name}.", suffix=".tmp", delete=False
            ) as temporary:
                temporary_path = Path(temporary.name)
                temporary.write(updated_text.encode("utf-8"))
                temporary.flush()
                os.fsync(temporary.fileno())
            temporary_path.chmod(path.stat().st_mode)
            temporary_path.replace(path)
        except OSError as error:
            if temporary_path:
                temporary_path.unlink(missing_ok=True)
            self._send_json({"error": f"Could not update menu: {error}"}, status=500)
            return

        new_hash = hashlib.sha256(updated_text.encode("utf-8")).hexdigest()
        remaining = sum(
            count - 1
            for count in Counter(
                line.strip().lower() for line in updated_text.splitlines() if len(line.strip()) > 12
            ).values()
            if count > 1
        )
        status = "fixed" if remaining == 0 else "open"
        try:
            with closing(self._review_connection()) as connection, connection:
                connection.execute(
                    """INSERT INTO issue_reviews
                       (menu_name, source_hash, issue_id, status, note, updated_at)
                       VALUES (?, ?, 'repeated_lines', ?, ?, ?)
                       ON CONFLICT(menu_name, source_hash, issue_id) DO UPDATE SET
                       status = excluded.status, note = excluded.note, updated_at = excluded.updated_at""",
                    (
                        name,
                        new_hash,
                        status,
                        note or f"Removed duplicate Markdown lines: {', '.join(map(str, sorted(line_numbers)))}",
                        datetime.now(timezone.utc).isoformat(),
                    ),
                )
        except sqlite3.Error as error:
            self._send_json({"error": f"Menu was updated but review status could not be saved: {error}"}, status=500)
            return
        self._send_json(
            {
                "name": name,
                "sourceHash": new_hash,
                "removedLines": sorted(line_numbers),
                "remainingRepeatedLines": remaining,
                "status": status,
            }
        )

    @staticmethod
    def _validate_export_item(item: object) -> dict[str, str]:
        if not isinstance(item, dict):
            raise ValueError("Each export item must be an object")
        url = item.get("url")
        alternate_urls = item.get("urls", [])
        region = item.get("region")
        venue = item.get("venue")
        category = item.get("category")
        if not isinstance(url, str) or len(url) > 4096:
            raise ValueError("Each asset must have a valid URL")
        if not isinstance(alternate_urls, list) or len(alternate_urls) > 100:
            raise ValueError("Each asset can include at most 100 alternate URLs")
        if not all(isinstance(candidate, str) and len(candidate) <= 4096 for candidate in alternate_urls):
            raise ValueError("Each alternate asset URL must be valid")
        if not all(isinstance(value, str) for value in (region, venue, category)):
            raise ValueError("Each asset must include its region, venue, and category")
        candidates = list(dict.fromkeys([url, *alternate_urls]))
        for candidate in candidates:
            try:
                parsed = urlsplit(candidate)
                port = parsed.port
            except ValueError as error:
                raise ValueError("Each asset must have a valid URL") from error
            if (
                parsed.scheme != "https"
                or parsed.hostname != ASSET_HOST
                or parsed.username is not None
                or parsed.password is not None
                or port not in (None, 443)
            ):
                raise ValueError(f"Only HTTPS assets from {ASSET_HOST} can be exported")
            if not parsed.path or parsed.path == "/":
                raise ValueError("Each asset URL must include a file path")
        try:
            clean_region = safe_folder_name(region)
            clean_venue = safe_folder_name(venue)
            clean_category = safe_folder_name(category)
        except ValueError as error:
            raise ValueError("Each asset must include valid region, venue, and category names") from error
        return {
            "url": url,
            "urls": candidates,
            "region": clean_region,
            "venue": clean_venue,
            "category": clean_category,
        }

    @staticmethod
    def _export_items(items: list[dict[str, str]]) -> dict[str, object]:
        stamp = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")
        folders: dict[tuple[str, str, str], Path] = {}
        used_names: dict[tuple[str, str, str], set[str]] = {}
        files = []
        failures = []
        opener = urllib.request.build_opener(SameHostRedirectHandler())

        for item in items:
            group = (item["region"], item["venue"], item["category"])
            if group not in folders:
                parent = EXPORTS / group[0] / group[1] / group[2]
                parent.mkdir(parents=True, exist_ok=True)
                export_dir = parent / stamp
                suffix = 2
                while True:
                    try:
                        export_dir.mkdir()
                        break
                    except FileExistsError:
                        export_dir = parent / f"{stamp}-{suffix}"
                        suffix += 1
                folders[group] = export_dir
                used_names[group] = set()

            filename = export_filename(item["url"], used_names[group])
            destination = folders[group] / filename
            try:
                source_url = download_asset(item["urls"], destination, opener)
                files.append(
                    {
                        "name": filename,
                        "category": item["category"],
                        "directory": str(folders[group].relative_to(ROOT)),
                        "sourceUrl": source_url,
                    }
                )
            except (urllib.error.URLError, TimeoutError, OSError) as error:
                failures.append({"name": filename, "error": str(error)})

        directories = sorted(str(path.relative_to(ROOT)) for path in folders.values())
        return {
            "requested": len(items),
            "downloaded": len(files),
            "failed": failures,
            "directories": directories,
        }

    def _send_file(
        self, path: Path, content_type: str, disposition: str | None = None
    ) -> None:
        try:
            data = path.read_bytes()
        except OSError as error:
            self.send_error(500, f"Could not read requested file: {error}")
            return
        self._send_bytes(data, content_type, disposition)

    def _send_bytes(
        self,
        data: bytes,
        content_type: str,
        disposition: str | None = None,
        status: int = 200,
        headers: dict[str, str] | None = None,
    ) -> None:
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(data)))
        self.send_header("Cache-Control", "no-store")
        self.send_header("X-Content-Type-Options", "nosniff")
        if disposition:
            self.send_header("Content-Disposition", disposition)
        for name, value in (headers or {}).items():
            self.send_header(name, value)
        self.end_headers()
        self.wfile.write(data)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--host", default="127.0.0.1", help="interface to bind (default: localhost)")
    parser.add_argument("--port", type=int, default=8000, help="port to bind (default: 8000)")
    args = parser.parse_args()

    if not MENUS.is_dir() or not PDFS.is_dir() or not PAGES.is_dir():
        parser.error("Expected pages/, inncollectiongroup.com_root/menus_md/, and documents/extracted-to-md/")
    if not re.fullmatch(r"[A-Za-z0-9_.-]+", args.host):
        parser.error("--host must be a hostname or IP address")

    server = ThreadingHTTPServer((args.host, args.port), MenuReviewHandler)
    print(f"Menu review available at http://{args.host}:{args.port}/")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nStopping menu review server.")
    finally:
        server.server_close()


if __name__ == "__main__":
    main()