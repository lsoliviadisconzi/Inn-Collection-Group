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

from db.database import init_db, connect as db_connect
import db.auth as auth
from jobs.rebuild import get_status as get_rebuild_status, trigger_rebuild, venue_for_menu


ROOT = Path(__file__).resolve().parent
PAGES = ROOT / "pages"
MENUS = ROOT / "inncollectiongroup.com_root" / "menus_md"
PDFS = ROOT / "inncollectiongroup.com_root" / "documents" / "extracted-to-md"
EXPORTS = ROOT / "exports"
REVIEW_DB = ROOT / "menu_review_state.sqlite3"
DB_BACKUP_DIR = ROOT / "db" / "backups"
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
        is_launch_op = path.startswith("/api/launches/") and (path.endswith("/tasks") or path.endswith("/venues"))
        if not (
            path in ("/api/export", "/api/issues", "/api/issues/fix-duplicates", "/api/rebuild", "/api/login", "/api/logout", "/api/menu-reviews")
            or is_launch_op
        ):
            self.send_error(404, "Not found")
            return
        payload = self._read_json_body()
        if payload is JSON_BODY_ERROR:
            return
        if path == "/api/login":
            self._handle_login(payload)
            return
        if path == "/api/logout":
            self._handle_logout()
            return
        if path == "/api/menu-reviews":
            self._save_menu_review(payload)
            return
        if path == "/api/rebuild":
            venue = payload.get("venue") if isinstance(payload, dict) else None
            if not isinstance(venue, str) or not venue.strip():
                self._send_json({"error": "A venue name or 'all' is required"}, status=400)
                return
            status = trigger_rebuild(venue.strip())
            self._send_json(status)
            return
        if path == "/api/issues":
            self._save_issue_review(payload)
            return
        if path == "/api/issues/fix-duplicates":
            self._remove_duplicate_lines(payload)
            return
        if is_launch_op and path.endswith("/tasks"):
            campaign_id = path[len("/api/launches/"): -len("/tasks")].strip("/")
            self._update_launch_task(campaign_id, payload)
            return
        if is_launch_op and path.endswith("/venues"):
            campaign_id = path[len("/api/launches/"): -len("/venues")].strip("/")
            self._update_launch_venue(campaign_id, payload)
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
            self.send_header("Location", "/pages/index.html")
            self.end_headers()
            return
        if request.path in (
            "/pages/index.html",
            "/pages/menu-review.html",
            "/pages/discovered-media.html",
            "/pages/fnb-crosscheck.html",
            "/pages/launch-readiness.html",
            "/pages/product-data.html",
            "/pages/menu-explorer.html",
        ):
            self._send_file(PAGES / request.path.rsplit("/", 1)[-1], "text/html; charset=utf-8")
            return
        if request.path.startswith("/pages/recipes/"):
            filename = request.path.rsplit("/", 1)[-1]
            if filename:
                self._send_file(PAGES / "recipes" / filename, "text/html; charset=utf-8")
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
        if request.path == "/pages/pdf_map.json":
            self._send_file(PAGES / "pdf_map.json", "application/json; charset=utf-8")
            return
        if request.path == "/api/health":
            self._get_health()
            return
        if request.path == "/api/rebuild-status":
            self._send_json(get_rebuild_status())
            return
        if request.path == "/api/me":
            self._handle_me()
            return
        if request.path == "/api/menu-reviews":
            self._get_menu_reviews()
            return
        if request.path == "/api/allergens/gaps":
            self._get_allergen_gaps()
            return
        if request.path == "/api/launches":
            self._get_launch_campaigns()
            return
        if request.path.startswith("/api/launches/"):
            campaign_id = request.path[len("/api/launches/"):].strip("/")
            if campaign_id:
                self._get_launch_detail(campaign_id)
                return
        if request.path == "/api/venues":
            self._send_json(self._venue_index())
            return
        if request.path.startswith("/api/venues/"):
            identifier = request.path[len("/api/venues/"):].strip("/")
            if identifier:
                self._venue_detail(identifier)
                return
        if request.path == "/api/menus":
            self._send_json(self._menu_index())
            return
        if request.path.startswith("/api/menus/"):
            filename = unquote(request.path[len("/api/menus/"):].strip("/"))
            if filename:
                self._get_menu_detail(filename)
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
    def _venue_index() -> list[dict[str, object]]:
        import build_venue_export
        entries = []
        for name, cfg in sorted(build_venue_export.VENUES.items(), key=lambda x: x[0].casefold()):
            region = cfg.get("region") or "Unknown"
            venue_id = cfg.get("id") or name.lower().replace(" ", "-")
            export_file = EXPORTS / region / name / "venue.json"
            has_export = export_file.is_file()
            entries.append({
                "id": venue_id,
                "name": name,
                "region": region,
                "slug": cfg.get("slug") or venue_id,
                "menuCount": len(cfg.get("menu_files", ())),
                "hasExport": has_export,
                "exportSize": export_file.stat().st_size if has_export else 0,
            })
        return entries

    def _venue_detail(self, identifier: str) -> None:
        import build_venue_export
        clean_id = unquote(identifier).strip().casefold()
        matched_name = None
        matched_cfg = None
        for name, cfg in build_venue_export.VENUES.items():
            if (
                name.casefold() == clean_id
                or cfg.get("id", "").casefold() == clean_id
                or cfg.get("slug", "").casefold() == clean_id
            ):
                matched_name = name
                matched_cfg = cfg
                break

        if not matched_name:
            self._send_json({"error": f"Venue '{identifier}' not found"}, status=404)
            return

        region = matched_cfg.get("region") or "Unknown"
        export_file = EXPORTS / region / matched_name / "venue.json"
        if not export_file.is_file():
            self._send_json({
                "venue": {
                    "id": matched_cfg.get("id"),
                    "name": matched_name,
                    "region": region,
                    "slug": matched_cfg.get("slug"),
                    "menuFiles": list(matched_cfg.get("menu_files", ())),
                },
                "hasExport": False,
                "message": "Export not yet generated. Use POST /api/rebuild with this venue to generate it."
            }, status=200)
            return

        try:
            with open(export_file, "r", encoding="utf-8") as f:
                data = json.load(f)
            self._send_json(data)
        except Exception as error:
            self._send_json({"error": f"Could not read venue export: {error}"}, status=500)

    @staticmethod
    def _menu_index() -> list[dict[str, object]]:
        entries = []
        for path in sorted(MENUS.glob("*.md"), key=lambda item: item.name.casefold()):
            pdf = PDFS / f"{path.stem}.pdf"
            venue = venue_for_menu(path.name)
            entries.append(
                {
                    "name": path.name,
                    "kind": menu_kind(path.name),
                    "venue": venue,
                    "hasPdf": pdf.is_file(),
                    "bytes": path.stat().st_size,
                }
            )
        return entries

    def _get_menu_detail(self, name: str) -> None:
        if not self._known_menu(name):
            self._send_json({"error": "Menu not found"}, status=404)
            return
        try:
            path, content, source_hash = self._issue_source(name)
            with closing(self._review_connection()) as connection, connection:
                rows = connection.execute(
                    "SELECT issue_id, status, note, updated_at FROM issue_reviews "
                    "WHERE menu_name = ? AND source_hash = ?",
                    (name, source_hash),
                ).fetchall()

            venue = venue_for_menu(name)
            pdf = PDFS / f"{Path(name).stem}.pdf"
            self._send_json({
                "name": name,
                "kind": menu_kind(name),
                "venue": venue,
                "hasPdf": pdf.is_file(),
                "bytes": len(content),
                "sourceHash": source_hash,
                "content": content.decode("utf-8", errors="replace"),
                "decisions": {
                    row[0]: {"status": row[1], "note": row[2], "updated_at": row[3]}
                    for row in rows
                },
            })
        except Exception as error:
            self._send_json({"error": f"Could not read menu: {error}"}, status=500)

    def _get_session_user(self) -> dict | None:
        cookie_header = self.headers.get("Cookie", "")
        from http.cookies import SimpleCookie
        cookie = SimpleCookie()
        try:
            cookie.load(cookie_header)
        except Exception:
            return None
        sess_cookie = cookie.get("icg_session")
        if not sess_cookie:
            return None
        with closing(self._review_connection()) as conn:
            return auth.get_user_from_session(conn, sess_cookie.value)

    def _current_user_name(self) -> str:
        u = self._get_session_user()
        return u["username"] if u else "local"

    def _handle_login(self, payload: object) -> None:
        if not isinstance(payload, dict):
            self._send_json({"error": "Request body must be an object"}, status=400)
            return
        username = payload.get("username", "").strip()
        password = payload.get("password", "")
        if not username or not password:
            self._send_json({"error": "Username and password are required"}, status=400)
            return
        with closing(self._review_connection()) as conn:
            user = auth.authenticate_user(conn, username, password)
            if not user:
                self._send_json({"error": "Invalid username or password"}, status=401)
                return
            sess_id = auth.create_session(conn, username)
            auth.record_audit(conn, "user", username, "login", "Successful session login", username)
        cookie = f"icg_session={sess_id}; Path=/; HttpOnly; SameSite=Lax"
        data = json.dumps({"ok": True, "user": user}, ensure_ascii=False).encode("utf-8")
        self._send_bytes(data, "application/json; charset=utf-8", headers={"Set-Cookie": cookie})

    def _handle_logout(self) -> None:
        cookie_header = self.headers.get("Cookie", "")
        from http.cookies import SimpleCookie
        cookie = SimpleCookie()
        try:
            cookie.load(cookie_header)
        except Exception:
            pass
        sess = cookie.get("icg_session")
        if sess:
            with closing(self._review_connection()) as conn:
                auth.delete_session(conn, sess.value)
        clear_cookie = "icg_session=deleted; Path=/; Expires=Thu, 01 Jan 1970 00:00:00 GMT; HttpOnly; SameSite=Lax"
        data = json.dumps({"ok": True}, ensure_ascii=False).encode("utf-8")
        self._send_bytes(data, "application/json; charset=utf-8", headers={"Set-Cookie": clear_cookie})

    def _handle_me(self) -> None:
        user = self._get_session_user()
        if user:
            self._send_json({"authenticated": True, "user": user})
        else:
            self._send_json({"authenticated": False, "user": None})

    def _get_launch_campaigns(self) -> None:
        with closing(self._review_connection()) as conn:
            rows = conn.execute(
                "SELECT id, name, launch_date, as_of_date FROM launch_campaigns ORDER BY launch_date DESC"
            ).fetchall()
            self._send_json([
                {"id": r["id"], "name": r["name"], "launchDate": r["launch_date"], "asOfDate": r["as_of_date"]}
                for r in rows
            ])

    def _get_launch_detail(self, campaign_id: str) -> None:
        with closing(self._review_connection()) as conn:
            camp = conn.execute("SELECT * FROM launch_campaigns WHERE id = ?", (campaign_id,)).fetchone()
            if not camp:
                self._send_json({"error": "Launch campaign not found"}, status=404)
                return

            milestones = conn.execute(
                "SELECT name, target_date FROM launch_milestones WHERE campaign_id = ? ORDER BY sort_order, target_date",
                (campaign_id,)
            ).fetchall()

            ws_rows = conn.execute(
                "SELECT workstream_id, name, owner, due_date, gate FROM launch_workstreams WHERE campaign_id = ? ORDER BY sort_order",
                (campaign_id,)
            ).fetchall()

            task_rows = conn.execute(
                "SELECT workstream_id, task_id, title, status, owner, note, updated_at, updated_by FROM launch_tasks WHERE campaign_id = ?",
                (campaign_id,)
            ).fetchall()

            tasks_by_ws: dict[str, list] = {}
            for t in task_rows:
                tasks_by_ws.setdefault(t["workstream_id"], []).append({
                    "id": t["task_id"],
                    "t": t["title"],
                    "st": t["status"],
                    "o": t["owner"],
                    "note": t["note"],
                    "updatedAt": t["updated_at"],
                    "updatedBy": t["updated_by"],
                })

            workstreams = []
            for ws in ws_rows:
                ws_id = ws["workstream_id"]
                workstreams.append({
                    "id": ws_id,
                    "n": ws["name"],
                    "s": ws_id,
                    "o": ws["owner"],
                    "due": ws["due_date"],
                    "gate": ws["gate"],
                    "items": sorted(tasks_by_ws.get(ws_id, []), key=lambda x: str(x["id"])),
                })

            venue_rows = conn.execute(
                "SELECT venue_name, region, workstream_id, status FROM launch_venue_status WHERE campaign_id = ?",
                (campaign_id,)
            ).fetchall()
            venue_status: dict[str, dict[str, str]] = {}
            for vr in venue_rows:
                venue_status.setdefault(vr["venue_name"], {})[vr["workstream_id"]] = vr["status"]

            self._send_json({
                "campaign": {
                    "id": camp["id"],
                    "name": camp["name"],
                    "launchDate": camp["launch_date"],
                    "asOfDate": camp["as_of_date"],
                },
                "milestones": [[m["name"], m["target_date"]] for m in milestones],
                "workstreams": workstreams,
                "venueStatus": venue_status,
            })

    def _update_launch_task(self, campaign_id: str, payload: object) -> None:
        if not isinstance(payload, dict):
            self._send_json({"error": "Request body must be an object"}, status=400)
            return
        ws_id = payload.get("workstreamId")
        task_id = str(payload.get("taskId"))
        status = payload.get("status")
        note = payload.get("note")

        if not ws_id or task_id is None or not status:
            self._send_json({"error": "workstreamId, taskId, and status are required"}, status=400)
            return

        user = self._current_user_name()
        now = datetime.now(timezone.utc).isoformat()

        with closing(self._review_connection()) as conn:
            conn.execute(
                """UPDATE launch_tasks
                   SET status = ?, note = COALESCE(?, note), updated_at = ?, updated_by = ?
                   WHERE campaign_id = ? AND workstream_id = ? AND task_id = ?""",
                (status, note, now, user, campaign_id, ws_id, task_id),
            )
            conn.commit()
            auth.record_audit(
                conn, "launch_task", f"{campaign_id}:{ws_id}:{task_id}", "update",
                f"Status: {status}, note: {note or ''}", user
            )
        self._send_json({"ok": True, "status": status, "updatedAt": now, "updatedBy": user})

    def _update_launch_venue(self, campaign_id: str, payload: object) -> None:
        if not isinstance(payload, dict):
            self._send_json({"error": "Request body must be an object"}, status=400)
            return
        venue_name = payload.get("venueName")
        region = payload.get("region", "")
        ws_id = payload.get("workstreamId")
        status = payload.get("status")
        if not venue_name or not ws_id or not status:
            self._send_json({"error": "venueName, workstreamId, and status are required"}, status=400)
            return
        user = self._current_user_name()
        now = datetime.now(timezone.utc).isoformat()
        with closing(self._review_connection()) as conn:
            conn.execute(
                """INSERT INTO launch_venue_status (campaign_id, venue_name, region, workstream_id, status, updated_at, updated_by)
                   VALUES (?, ?, ?, ?, ?, ?, ?)
                   ON CONFLICT(campaign_id, venue_name, workstream_id) DO UPDATE SET
                   status = excluded.status, updated_at = excluded.updated_at, updated_by = excluded.updated_by""",
                (campaign_id, venue_name, region, ws_id, status, now, user),
            )
            conn.commit()
            auth.record_audit(
                conn, "launch_venue", f"{campaign_id}:{venue_name}:{ws_id}", "update",
                f"Status: {status}", user
            )
        self._send_json({"ok": True, "venueName": venue_name, "status": status, "updatedBy": user})

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
        return db_connect(REVIEW_DB)

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

    def _get_menu_reviews(self) -> None:
        try:
            with closing(self._review_connection()) as conn:
                rows = conn.execute(
                    "SELECT menu_name, status, note, updated_at, updated_by FROM menu_reviews"
                ).fetchall()
                reviews = {
                    r["menu_name"]: {
                        "status": r["status"],
                        "note": r["note"],
                        "updated_at": r["updated_at"],
                        "updated_by": r["updated_by"],
                    }
                    for r in rows
                }
            self._send_json({"reviews": reviews})
        except sqlite3.Error as error:
            self._send_json({"error": f"Could not load menu reviews: {error}"}, status=500)

    def _check_menu_allergen_block(self, name: str) -> list[str]:
        import build_venue_export
        venue = venue_for_menu(name)
        if not venue:
            return []
        cfg = build_venue_export.VENUES.get(venue, {})
        region = cfg.get("region") or "Unknown"
        export_file = EXPORTS / region / venue / "venue.json"
        if not export_file.is_file():
            return []
        try:
            with open(export_file, "r", encoding="utf-8") as f:
                data = json.load(f)
            missing = []
            stem = Path(name).stem.casefold()
            for menu in data.get("menus", []):
                src_md = Path(menu.get("source", {}).get("markdown") or "").name.casefold()
                src_file = (menu.get("source", {}).get("file") or "").casefold()
                m_name = (menu.get("name") or "").casefold()
                if src_md == name.casefold() or src_file == name.casefold() or m_name == stem or stem in m_name:
                    for sec in menu.get("sections", []):
                        for item in sec.get("items", []):
                            prod = item.get("product")
                            if prod:
                                if prod.get("allergenDataMissing") or not (prod.get("allergens") or prod.get("mayContain")):
                                    missing.append(prod.get("name") or item.get("name") or "Unknown dish")
            return list(dict.fromkeys(missing))
        except Exception:
            return []

    def _save_menu_review(self, payload: object) -> None:
        if not isinstance(payload, dict):
            self._send_json({"error": "Request body must be an object"}, status=400)
            return
        name = payload.get("name")
        status = payload.get("status")
        note = payload.get("note", "")
        if not isinstance(name, str) or not self._known_menu(name):
            self._send_json({"error": "Menu not found"}, status=404)
            return
        if not isinstance(status, str) or status not in {"pending", "reviewed", "flagged"}:
            self._send_json({"error": "Invalid menu review status (must be pending, reviewed, or flagged)"}, status=400)
            return
        if not isinstance(note, str) or len(note) > 4000:
            self._send_json({"error": "Review note must be 4000 characters or fewer"}, status=400)
            return
        now = datetime.now(timezone.utc).isoformat()
        user = self._current_user_name()
        if status == "reviewed":
            blocking_items = self._check_menu_allergen_block(name)
            if blocking_items:
                try:
                    with closing(self._review_connection()) as conn, conn:
                        auth.record_audit(
                            conn, "menu_status", name, "publication_blocked",
                            f"Blocked attempt to mark reviewed by {user}. Items missing statutory allergens: {', '.join(blocking_items)}",
                            user
                        )
                except sqlite3.Error:
                    pass
                self._send_json({
                    "error": f"Publication blocked (Decision D12): {len(blocking_items)} item(s) have unset statutory allergens in Kafoodie: {', '.join(blocking_items[:3])}{'...' if len(blocking_items) > 3 else ''}. Allergen data must be completed before release.",
                    "blocked": True,
                    "missingItems": blocking_items
                }, status=409)
                return
        try:
            with closing(self._review_connection()) as conn, conn:
                conn.execute(
                    """INSERT INTO menu_reviews (menu_name, status, note, updated_at, updated_by)
                       VALUES (?, ?, ?, ?, ?)
                       ON CONFLICT(menu_name) DO UPDATE SET
                       status = excluded.status, note = excluded.note, updated_at = excluded.updated_at, updated_by = excluded.updated_by""",
                    (name, status, note, now, user),
                )
                auth.record_audit(
                    conn, "menu_status", name, "update", f"Status: {status}, note: {note}", user
                )
        except sqlite3.Error as error:
            self._send_json({"error": f"Could not save menu review: {error}"}, status=500)
            return
        self._send_json({"ok": True, "name": name, "status": status, "note": note, "updatedAt": now, "updatedBy": user})

    def _get_allergen_gaps(self) -> None:
        self._send_json(self._allergen_gap_data())

    def _get_health(self) -> None:
        """Estate summary for the home dashboard. Read-only; every section degrades on its own."""
        gaps = self._allergen_gap_data()
        venues = self._venue_index()
        blockers: dict[str, set[str]] = {}
        for v in gaps["venues"]:
            for prod in v.get("missingProducts", []) or []:
                blockers.setdefault(prod.get("name") or "(unnamed)", set()).add(v["venue"])
        health: dict[str, object] = {
            "generatedAt": datetime.now(tz=timezone.utc).isoformat(),
            "venues": {"total": len(venues), "exported": sum(1 for v in venues if v["hasExport"])},
            "allergens": gaps["summary"],
            "recurringBlockers": [
                {"name": n, "venues": len(vs)}
                for n, vs in sorted(blockers.items(), key=lambda kv: (-len(kv[1]), kv[0]))[:6]
            ],
            "notExported": [v["name"] for v in venues if not v["hasExport"]],
            "menus": {"total": len(self._menu_index()), "reviewByStatus": {}},
            "openIssues": None,
            "campaign": None,
            "activity": [],
            "rebuild": get_rebuild_status(),
            "lastBackup": None,
        }
        try:
            with closing(self._review_connection()) as conn:
                row = conn.execute("SELECT COUNT(*) FROM issue_reviews WHERE status = 'open'").fetchone()
                health["openIssues"] = row[0] if row else 0
                try:
                    rows = conn.execute("SELECT status, COUNT(*) FROM menu_reviews GROUP BY status").fetchall()
                    health["menus"]["reviewByStatus"] = {r[0]: r[1] for r in rows}
                except sqlite3.Error:
                    pass
                try:
                    c = conn.execute(
                        "SELECT id, name, launch_date FROM launch_campaigns ORDER BY launch_date DESC LIMIT 1"
                    ).fetchone()
                    if c:
                        health["campaign"] = {"id": c["id"], "name": c["name"], "launchDate": c["launch_date"]}
                except sqlite3.Error:
                    pass
                try:
                    rows = conn.execute(
                        "SELECT entity, entity_id, action, detail, user, created_at "
                        "FROM audit_events ORDER BY created_at DESC LIMIT 12"
                    ).fetchall()
                    health["activity"] = [
                        {"entity": r["entity"], "entityId": r["entity_id"], "action": r["action"],
                         "detail": r["detail"], "user": r["user"], "at": r["created_at"]}
                        for r in rows
                    ]
                except sqlite3.Error:
                    pass
        except sqlite3.Error:
            pass
        try:
            backups = sorted(DB_BACKUP_DIR.glob("*.sqlite3"), key=lambda f: f.stat().st_mtime)
            if backups:
                health["lastBackup"] = datetime.fromtimestamp(backups[-1].stat().st_mtime, tz=timezone.utc).isoformat()
        except OSError:
            pass
        self._send_json(health)

    def _allergen_gap_data(self) -> dict:
        import build_venue_export
        results = []
        total_products = 0
        total_missing_allergens = 0
        total_unmatched_dishes = 0
        for name, cfg in sorted(build_venue_export.VENUES.items(), key=lambda x: x[0].casefold()):
            region = cfg.get("region") or "Unknown"
            export_file = EXPORTS / region / name / "venue.json"
            if not export_file.is_file():
                results.append({
                    "venue": name,
                    "region": region,
                    "hasExport": False,
                    "status": "not_exported",
                    "productsCount": 0,
                    "missingAllergensCount": 0,
                    "unmatchedDishesCount": 0,
                    "gaps": ["Venue export has not been built yet"],
                })
                continue
            try:
                with open(export_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                products = data.get("products", [])
                missing_products = [
                    {"id": p.get("id"), "name": p.get("name"), "menu": p.get("menu")}
                    for p in products
                    if p.get("allergenDataMissing") or not (p.get("allergens") or p.get("mayContain"))
                ]
                match_report = data.get("matchReport", {})
                unmatched = match_report.get("unmatched", 0)
                gaps = data.get("gaps", [])

                total_products += len(products)
                total_missing_allergens += len(missing_products)
                total_unmatched_dishes += unmatched

                status = "compliant"
                if missing_products or unmatched > 0:
                    status = "action_required" if missing_products else "warning"

                results.append({
                    "venue": name,
                    "region": region,
                    "hasExport": True,
                    "status": status,
                    "productsCount": len(products),
                    "missingAllergensCount": len(missing_products),
                    "missingProducts": missing_products,
                    "unmatchedDishesCount": unmatched,
                    "gaps": gaps,
                })
            except Exception as e:
                results.append({
                    "venue": name,
                    "region": region,
                    "hasExport": True,
                    "status": "error",
                    "error": str(e),
                })

        return {
            "summary": {
                "totalVenues": len(build_venue_export.VENUES),
                "exportedVenues": sum(1 for r in results if r.get("hasExport")),
                "totalProducts": total_products,
                "totalMissingAllergenProducts": total_missing_allergens,
                "totalUnmatchedDishes": total_unmatched_dishes,
            },
            "venues": results,
        }

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
            user = self._current_user_name()
            now = datetime.now(timezone.utc).isoformat()
            with closing(self._review_connection()) as connection, connection:
                connection.execute(
                    """INSERT INTO issue_reviews
                       (menu_name, source_hash, issue_id, status, note, updated_at)
                       VALUES (?, ?, ?, ?, ?, ?)
                       ON CONFLICT(menu_name, source_hash, issue_id) DO UPDATE SET
                       status = excluded.status, note = excluded.note, updated_at = excluded.updated_at""",
                    (name, current_hash, issue_id, status, note, now),
                )
                auth.record_audit(
                    connection, "issue_review", f"{name}:{issue_id}", "update",
                    f"Status: {status}, note: {note}", user
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
            user = self._current_user_name()
            now = datetime.now(timezone.utc).isoformat()
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
                        now,
                    ),
                )
                auth.record_audit(
                    connection, "menu_file", name, "fix_duplicates",
                    f"Removed lines: {', '.join(map(str, sorted(line_numbers)))}", user
                )
        except sqlite3.Error as error:
            self._send_json({"error": f"Menu was updated but review status could not be saved: {error}"}, status=500)
            return
        rebuild_info = None
        venue = venue_for_menu(name)
        if venue:
            rebuild_info = trigger_rebuild(venue)
        self._send_json(
            {
                "name": name,
                "sourceHash": new_hash,
                "removedLines": sorted(line_numbers),
                "remainingRepeatedLines": remaining,
                "status": status,
                "rebuild": rebuild_info,
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
    parser.add_argument("--add-user", metavar="USERNAME", help="create or update a user and exit")
    parser.add_argument("--role", default="coordinator", help="role for --add-user (default: coordinator)")
    args = parser.parse_args()

    import logging
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s %(message)s")
    init_db(REVIEW_DB, backup_dir=DB_BACKUP_DIR)

    if args.add_user:
        import getpass
        pw = getpass.getpass(f"Enter password for '{args.add_user}': ")
        if not pw.strip():
            print("Password cannot be empty.")
            return
        with closing(db_connect(REVIEW_DB)) as conn:
            auth.add_user(conn, args.add_user.strip(), pw.strip(), args.add_user.strip().capitalize(), args.role)
        print(f"User '{args.add_user}' registered successfully.")
        return

    if not MENUS.is_dir() or not PDFS.is_dir() or not PAGES.is_dir():
        parser.error("Expected pages/, inncollectiongroup.com_root/menus_md/, and documents/extracted-to-md/")
    if not re.fullmatch(r"[A-Za-z0-9_.-]+", args.host):
        parser.error("--host must be a hostname or IP address")

    if args.host not in ("127.0.0.1", "localhost"):
        with closing(db_connect(REVIEW_DB)) as conn:
            if auth.count_users(conn) == 0:
                parser.error("When binding to an external interface (--host != 127.0.0.1), at least one user must exist in the database.")

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