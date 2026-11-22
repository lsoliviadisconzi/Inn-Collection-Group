#!/usr/bin/env python3
"""Netlify Serverless Function implementing all API endpoints for Inn Collection Group.

Compatible with Python 3.8+ on AWS Lambda / Netlify Functions.
Endpoints handled:
  - GET  /api/menus
  - GET  /api/menu?name=...
  - GET  /api/pdf?name=...
  - GET  /api/issues?name=...
  - POST /api/issues
  - POST /api/issues/fix-duplicates
  - POST /api/export
"""

from __future__ import annotations

import base64
from collections import Counter
from contextlib import closing
import hashlib
import io
import json
import os
from pathlib import Path
import re
import shutil
import sqlite3
import urllib.error
import urllib.parse
import urllib.request
import zipfile
from datetime import datetime, timezone

# Base directories
FUNC_DIR = Path(__file__).resolve().parent
ROOT_DIR = FUNC_DIR.parent.parent

# Locate menus and documents
MENUS_CANDIDATES = [
    Path("/tmp/menus_md"),
    FUNC_DIR / "data" / "menus_md",
    ROOT_DIR / "pages" / "menus_md",
    ROOT_DIR / "inncollectiongroup.com_root" / "menus_md",
]

DOCS_CANDIDATES = [
    ROOT_DIR / "pages" / "documents" / "extracted-to-md",
    ROOT_DIR / "inncollectiongroup.com_root" / "documents" / "extracted-to-md",
]

TMP_DIR = Path("/tmp")
DB_PATH = TMP_DIR / "menu_review_state.sqlite3"
SEED_DB = ROOT_DIR / "menu_review_state.sqlite3"
SEED_JSON = FUNC_DIR / "data" / "seed_reviews.json"

ASSET_HOST = "www.inncollectiongroup.com"
ISSUE_IDS = {"headings", "list_entries", "pdf_missing", "repeated_lines", "unusual_chars"}
MAX_EXPORT_ITEMS = 20_000


def get_menus_dir() -> Path:
    for candidate in MENUS_CANDIDATES[1:]:
        if candidate.is_dir():
            return candidate
    return ROOT_DIR / "pages" / "menus_md"


def get_docs_dir() -> Path:
    for candidate in DOCS_CANDIDATES:
        if candidate.is_dir():
            return candidate
    return ROOT_DIR / "pages" / "documents" / "extracted-to-md"


def ensure_db() -> sqlite3.Connection:
    TMP_DIR.mkdir(parents=True, exist_ok=True)
    if not DB_PATH.exists():
        if SEED_DB.exists():
            try:
                shutil.copy2(SEED_DB, DB_PATH)
            except OSError:
                pass
    conn = sqlite3.connect(DB_PATH)
    conn.execute(
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
    if SEED_JSON.exists():
        try:
            with SEED_JSON.open("r", encoding="utf-8") as f:
                rows = json.load(f)
            for r in rows:
                conn.execute(
                    """INSERT OR IGNORE INTO issue_reviews
                       (menu_name, source_hash, issue_id, status, note, updated_at)
                       VALUES (?, ?, ?, ?, ?, ?)""",
                    (
                        r.get("menu_name"),
                        r.get("source_hash"),
                        r.get("issue_id"),
                        r.get("status"),
                        r.get("note", ""),
                        r.get("updated_at"),
                    ),
                )
            conn.commit()
        except Exception:
            pass
    return conn


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


def read_menu_bytes(name: str) -> tuple[bytes, str]:
    tmp_path = Path("/tmp/menus_md") / name
    if tmp_path.is_file():
        content = tmp_path.read_bytes()
        return content, hashlib.sha256(content).hexdigest()
    menus_dir = get_menus_dir()
    path = menus_dir / name
    if not path.is_file():
        raise FileNotFoundError(f"Menu '{name}' not found")
    content = path.read_bytes()
    return content, hashlib.sha256(content).hexdigest()


def safe_folder_name(value: str) -> str:
    value = re.sub(r"\s*/\s*", " - ", value.strip())
    value = re.sub(r"[^A-Za-z0-9 .,'&()_-]+", "_", value).strip(" ._-")
    if not value or value in {".", ".."}:
        raise ValueError("Invalid name")
    return value[:120]


def export_filename(url: str, used: set[str]) -> str:
    base = urllib.parse.unquote(Path(urllib.parse.urlsplit(url).path).name)
    base = re.sub(r"[^\w.-]+", "_", base, flags=re.UNICODE).strip(" ._")[:160] or "file"
    name = base
    index = 2
    while name.casefold() in used:
        stem, suffix = (base.rsplit(".", 1) if "." in base else (base, ""))
        name = f"{stem}-{index}{'.' + suffix if suffix else ''}"
        index += 1
    used.add(name.casefold())
    return name


def json_response(data: object, status: int = 200, headers: dict[str, str] | None = None) -> dict:
    h = {
        "Content-Type": "application/json; charset=utf-8",
        "Cache-Control": "no-store",
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Headers": "Content-Type, X-Source-Hash",
        "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
    }
    if headers:
        h.update(headers)
    return {
        "statusCode": status,
        "headers": h,
        "body": json.dumps(data, ensure_ascii=False),
    }


def text_response(text: str, status: int = 200, headers: dict[str, str] | None = None) -> dict:
    h = {
        "Content-Type": "text/markdown; charset=utf-8",
        "Cache-Control": "no-store",
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Headers": "Content-Type, X-Source-Hash",
        "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
    }
    if headers:
        h.update(headers)
    return {
        "statusCode": status,
        "headers": h,
        "body": text,
    }


def get_pdf_path(name: str, docs_dir: Path) -> tuple[Path | None, str | None]:
    stem = Path(name).stem
    pdf = docs_dir / f"{stem}.pdf"
    if pdf.is_file():
        return pdf, stem
    alt_stem = re.sub(r"-v\d+$", "", stem)
    alt_pdf = docs_dir / f"{alt_stem}.pdf"
    if alt_pdf.is_file():
        return alt_pdf, alt_stem
    return None, None


def handle_menus_list() -> dict:
    menus_dir = get_menus_dir()
    docs_dir = get_docs_dir()
    entries = []
    seen = set()

    tmp_menus_dir = Path("/tmp/menus_md")
    if tmp_menus_dir.is_dir():
        for path in tmp_menus_dir.glob("*.md"):
            seen.add(path.name)
            pdf, _ = get_pdf_path(path.name, docs_dir)
            entries.append(
                {
                    "name": path.name,
                    "kind": menu_kind(path.name),
                    "hasPdf": pdf is not None,
                    "bytes": path.stat().st_size,
                }
            )

    if menus_dir.is_dir():
        for path in menus_dir.glob("*.md"):
            if path.name in seen:
                continue
            seen.add(path.name)
            pdf, _ = get_pdf_path(path.name, docs_dir)
            entries.append(
                {
                    "name": path.name,
                    "kind": menu_kind(path.name),
                    "hasPdf": pdf is not None,
                    "bytes": path.stat().st_size,
                }
            )

    entries.sort(key=lambda item: item["name"].casefold())
    return json_response(entries)


def handle_get_menu(name: str | None) -> dict:
    if not name or not name.endswith(".md") or "/" in name or "\\" in name:
        return json_response({"error": "Menu not found"}, status=404)
    try:
        content, source_hash = read_menu_bytes(name)
        text = content.decode("utf-8")
        return text_response(text, headers={"X-Source-Hash": source_hash})
    except (FileNotFoundError, UnicodeDecodeError) as e:
        return json_response({"error": str(e)}, status=404)


def handle_get_pdf(name: str | None) -> dict:
    if not name or not name.endswith(".md") or "/" in name or "\\" in name:
        return json_response({"error": "PDF not found"}, status=404)
    docs_dir = get_docs_dir()
    pdf_path, stem = get_pdf_path(name, docs_dir)
    if not pdf_path or not pdf_path.is_file():
        return json_response({"error": "PDF not found"}, status=404)
    target_url = f"/documents/extracted-to-md/{urllib.parse.quote(stem)}.pdf"
    return {
        "statusCode": 302,
        "headers": {
            "Location": target_url,
            "Cache-Control": "public, max-age=3600",
        },
        "body": "",
    }


def handle_get_issues(name: str | None) -> dict:
    if not name or not name.endswith(".md") or "/" in name or "\\" in name:
        return json_response({"error": "Menu not found"}, status=404)
    try:
        _, source_hash = read_menu_bytes(name)
        with closing(ensure_db()) as conn:
            rows = conn.execute(
                "SELECT issue_id, status, note FROM issue_reviews WHERE menu_name = ? AND source_hash = ?",
                (name, source_hash),
            ).fetchall()
        decisions = {
            issue_id: {"status": status, "note": note}
            for issue_id, status, note in rows
        }
        return json_response({"name": name, "sourceHash": source_hash, "decisions": decisions})
    except FileNotFoundError:
        return json_response({"error": "Menu not found"}, status=404)
    except Exception as e:
        return json_response({"error": f"Database error: {e}"}, status=500)


def handle_post_issues(payload: dict) -> dict:
    name = payload.get("name")
    issue_id = payload.get("issueId")
    status = payload.get("status")
    note = payload.get("note", "")
    source_hash = payload.get("sourceHash")

    if not isinstance(name, str) or not name.endswith(".md"):
        return json_response({"error": "Menu not found"}, status=404)
    if (
        not isinstance(issue_id, str)
        or issue_id not in ISSUE_IDS
        or not isinstance(status, str)
        or status not in {"open", "fixed", "intentional"}
    ):
        return json_response({"error": "Invalid issue or review status"}, status=400)
    if not isinstance(note, str) or len(note) > 4000:
        return json_response({"error": "Review note must be 4000 characters or fewer"}, status=400)

    try:
        _, current_hash = read_menu_bytes(name)
    except FileNotFoundError:
        return json_response({"error": "Menu not found"}, status=404)

    if source_hash != current_hash:
        return json_response({"error": "Menu changed since this review was opened; reload and try again"}, status=409)

    try:
        with closing(ensure_db()) as conn, conn:
            conn.execute(
                """INSERT INTO issue_reviews
                   (menu_name, source_hash, issue_id, status, note, updated_at)
                   VALUES (?, ?, ?, ?, ?, ?)
                   ON CONFLICT(menu_name, source_hash, issue_id) DO UPDATE SET
                   status = excluded.status, note = excluded.note, updated_at = excluded.updated_at""",
                (name, current_hash, issue_id, status, note, datetime.now(timezone.utc).isoformat()),
            )
        return json_response({"name": name, "issueId": issue_id, "status": status, "sourceHash": current_hash})
    except Exception as e:
        return json_response({"error": f"Could not save issue review: {e}"}, status=500)


def handle_fix_duplicates(payload: dict) -> dict:
    name = payload.get("name")
    source_hash = payload.get("sourceHash")
    line_numbers = payload.get("lineNumbers")
    note = payload.get("note", "")

    if not isinstance(name, str) or not name.endswith(".md"):
        return json_response({"error": "Menu not found"}, status=404)
    if (
        not isinstance(line_numbers, list)
        or not line_numbers
        or len(line_numbers) > 10_000
        or not all(isinstance(n, int) and n > 0 for n in line_numbers)
    ):
        return json_response({"error": "Select one or more valid duplicate line numbers"}, status=400)
    if len(set(line_numbers)) != len(line_numbers):
        return json_response({"error": "Duplicate line numbers were provided"}, status=400)
    if not isinstance(note, str) or len(note) > 4000:
        return json_response({"error": "Review note must be 4000 characters or fewer"}, status=400)

    try:
        content, current_hash = read_menu_bytes(name)
        text = content.decode("utf-8")
    except FileNotFoundError:
        return json_response({"error": "Menu not found"}, status=404)
    except UnicodeDecodeError:
        return json_response({"error": "Menu is not valid UTF-8 and cannot be edited safely"}, status=500)

    if source_hash != current_hash:
        return json_response({"error": "Menu changed since this review was opened; reload and try again"}, status=409)

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
        return json_response(
            {"error": "One or more selected lines are no longer repeated; reload the menu"},
            status=409,
        )

    updated_text = "".join(line for number, line in enumerate(lines, start=1) if number not in line_numbers)
    new_hash = hashlib.sha256(updated_text.encode("utf-8")).hexdigest()

    # Save to /tmp/menus_md
    tmp_menus = Path("/tmp/menus_md")
    tmp_menus.mkdir(parents=True, exist_ok=True)
    (tmp_menus / name).write_text(updated_text, encoding="utf-8")

    remaining = sum(
        count - 1
        for count in Counter(
            line.strip().lower() for line in updated_text.splitlines() if len(line.strip()) > 12
        ).values()
        if count > 1
    )
    status = "fixed" if remaining == 0 else "open"

    try:
        with closing(ensure_db()) as conn, conn:
            conn.execute(
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
    except Exception as e:
        return json_response({"error": f"Menu updated but review status could not be saved: {e}"}, status=500)

    return json_response(
        {
            "name": name,
            "sourceHash": new_hash,
            "removedLines": sorted(line_numbers),
            "remainingRepeatedLines": remaining,
            "status": status,
        }
    )


def handle_export(payload: dict) -> dict:
    items = payload.get("items") if isinstance(payload, dict) else None
    if not isinstance(items, list) or not items:
        return json_response({"error": "Select at least one asset to export"}, status=400)
    if len(items) > MAX_EXPORT_ITEMS:
        return json_response({"error": f"An export can contain at most {MAX_EXPORT_ITEMS} assets"}, status=413)

    zip_buffer = io.BytesIO()
    used_names: dict[tuple[str, str, str], set[str]] = {}
    downloaded_count = 0
    failures = []

    with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zf:
        for item in items:
            if not isinstance(item, dict):
                continue
            url = item.get("url")
            alt_urls = item.get("urls", [])
            region = item.get("region", "Uncategorized")
            venue = item.get("venue", "General")
            category = item.get("category", "Media")
            if not isinstance(url, str):
                continue

            candidates = list(dict.fromkeys([url, *alt_urls]))
            valid_candidates = []
            for cand in candidates:
                try:
                    parsed = urllib.parse.urlsplit(cand)
                    if parsed.scheme == "https" and parsed.hostname == ASSET_HOST and parsed.path:
                        valid_candidates.append(cand)
                except ValueError:
                    pass

            if not valid_candidates:
                failures.append({"name": Path(urllib.parse.urlsplit(url).path).name or "file", "error": "Invalid URL"})
                continue

            try:
                c_region = safe_folder_name(region)
                c_venue = safe_folder_name(venue)
                c_cat = safe_folder_name(category)
            except ValueError:
                c_region, c_venue, c_cat = "General", "General", "General"

            group = (c_region, c_venue, c_cat)
            if group not in used_names:
                used_names[group] = set()

            filename = export_filename(url, used_names[group])
            rel_path = f"{c_region}/{c_venue}/{c_cat}/{filename}"

            success = False
            for target_url in valid_candidates:
                try:
                    req = urllib.request.Request(
                        target_url,
                        headers={"User-Agent": "InnCollectionGroup-NetlifyExporter/1.0"},
                    )
                    with urllib.request.urlopen(req, timeout=15) as resp:
                        data = resp.read()
                        zf.writestr(rel_path, data)
                        success = True
                        downloaded_count += 1
                        break
                except Exception as e:
                    pass

            if not success:
                failures.append({"name": filename, "error": "Failed to download from remote server"})

    zip_bytes = zip_buffer.getvalue()
    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/zip",
            "Content-Disposition": 'attachment; filename="icg-media-export.zip"',
            "Access-Control-Allow-Origin": "*",
        },
        "body": base64.b64encode(zip_bytes).decode("ascii"),
        "isBase64Encoded": True,
    }


def handler(event: dict, context: object) -> dict:
    http_method = event.get("httpMethod", "GET").upper()
    if http_method == "OPTIONS":
        return {
            "statusCode": 200,
            "headers": {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Headers": "Content-Type, X-Source-Hash",
                "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
            },
            "body": "",
        }

    raw_path = event.get("path", "")
    if "/api/" in raw_path:
        path = "/api/" + raw_path.split("/api/", 1)[1]
    elif raw_path.startswith("/.netlify/functions/api"):
        sub = raw_path[len("/.netlify/functions/api"):]
        path = "/api" + sub if sub else "/api"
    else:
        path = raw_path

    query = event.get("queryStringParameters") or {}

    if http_method == "GET":
        if path == "/api/menus":
            return handle_menus_list()
        if path == "/api/menu":
            return handle_get_menu(query.get("name"))
        if path == "/api/pdf":
            return handle_get_pdf(query.get("name"))
        if path == "/api/issues":
            return handle_get_issues(query.get("name"))
        return json_response({"error": "Not found"}, status=404)

    if http_method == "POST":
        body_raw = event.get("body", "")
        if event.get("isBase64Encoded") and body_raw:
            try:
                body_raw = base64.b64decode(body_raw).decode("utf-8")
            except Exception:
                return json_response({"error": "Invalid base64 payload"}, status=400)
        try:
            payload = json.loads(body_raw) if body_raw else {}
        except json.JSONDecodeError:
            return json_response({"error": "Request body must be valid JSON"}, status=400)

        if path == "/api/issues":
            return handle_post_issues(payload)
        if path == "/api/issues/fix-duplicates":
            return handle_fix_duplicates(payload)
        if path == "/api/export":
            return handle_export(payload)
        return json_response({"error": "Not found"}, status=404)

    return json_response({"error": "Method not allowed"}, status=405)


if __name__ == "__main__":
    # Local verification test
    print("Testing GET /api/menus...")
    res = handler({"httpMethod": "GET", "path": "/api/menus"}, None)
    print("Status:", res["statusCode"])
    data = json.loads(res["body"])
    print(f"Found {len(data)} menus.")
    if data:
        first = data[0]["name"]
        print(f"Testing GET /api/menu?name={first}...")
        res_m = handler({"httpMethod": "GET", "path": "/api/menu", "queryStringParameters": {"name": first}}, None)
        print("Status:", res_m["statusCode"], "X-Source-Hash:", res_m["headers"].get("X-Source-Hash"))
        print(f"Testing GET /api/issues?name={first}...")
        res_i = handler({"httpMethod": "GET", "path": "/api/issues", "queryStringParameters": {"name": first}}, None)
        print("Status:", res_i["statusCode"], "Body:", res_i["body"])
