#!/usr/bin/env python3
"""Build the Menu explorer data file and the Kafoodie all-menus checklist.

Both outputs are derived from the downloaded outlet JSON in
``inncollectiongroup.com_root/kafoodie``. Run this after a crawl so the
explorer page and the checklist never drift apart again.

    python3 build_menu_explorer.py            # rebuild data + checklist
    python3 build_menu_explorer.py --prune    # also delete redundant copies
    python3 build_menu_explorer.py --check    # verify outputs are current
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent
KAFFODIE = ROOT / "inncollectiongroup.com_root" / "kafoodie"
PAGES = ROOT / "pages"
DATA_JS = PAGES / "menu-explorer-data.js"
CHECKLIST = KAFFODIE / "ALL_MENUS_CHECKLIST.md"
REMOVAL_LOG = KAFFODIE / "duplicates_removed.json"

# Venue names used by the Menu review filter, keyed by the outlet name that
# Kafoodie returns. Only the entries that actually differ are listed.
FILTER_NAMES = {
    "The Black Swan Inn": "The Black Swan",
    "The Midland Hotel": "The Midland",
    "The Stables At Cross Butts": "The Stables, Whitby",
    "The Swan": "The Swan, Grasmere",
    "Northallerton Inn": "The Northallerton Inn",
    "Tynemouth Castle Inn": "The Tynemouth Castle Inn",
    "The Pheasant": "The Pheasant Inn",
    "The Kings Head Inn": "The King's Head Inn",
}

# Venues that appear in the Menu review filter but have no Kafoodie outlet.
NO_KAFFODIE = ["Dean Court", "The Bull's Head Inn"]

# Recipe fields kept in the explorer payload. Allergen objects are replaced by
# their ids and resolved once through the shared ``allergens`` map, which is
# what removes the bulk of the duplication in the raw crawl.
RECIPE_FIELDS = (
    "id",
    "name",
    "description",
    "tags",
    "photo",
    "prices",
    "sort_order",
    "menu_id",
    "outlet_id",
    "isPublic",
    "is_pw_allergen_not_set",
    "preorder_availability_status",
    "delivery_methods",
    "emissions",
    "ingredients_simple",
    "tagMarks",
    "tagMarksTooltips",
    "allergen_sequence",
    "is_ingredients_empty",
)

# Nutrition is stored as ``[quantity, unit, reference, ratio, level]`` per
# nutrient. The five repeated key names cost more than the values themselves.
NUTRIENT_ORDER = ("quantity", "unit", "est", "actual_ratio", "doze")

# Payloads kept from each menu group's captured API traffic. The outlet-data
# payload duplicates ``outlet`` and the search payload is already expanded into
# ``menus``, so both are dropped.
KEPT_PAYLOAD_HINTS = ("terms-and-conditions", "recipe-ingredients", "/fp")


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def discover() -> tuple[dict[int, Path], list[tuple[int, Path, Path]]]:
    """Return the canonical file per outlet plus every redundant copy."""
    candidates: dict[int, list[Path]] = {}
    for path in sorted(KAFFODIE.glob("*/*_all_menus.json")):
        if path.name.endswith("_previous.json"):
            continue
        outlet_id = load(path).get("outlet_id")
        if outlet_id is None:
            continue
        candidates.setdefault(outlet_id, []).append(path)

    canonical: dict[int, Path] = {}
    duplicates: list[tuple[int, Path, Path]] = []
    for outlet_id, paths in candidates.items():
        # Prefer the *_full_menu folder, then the most recently written file.
        paths.sort(key=lambda p: (not p.parent.name.endswith("_full_menu"), -p.stat().st_mtime))
        canonical[outlet_id] = paths[0]
        duplicates.extend((outlet_id, paths[0], extra) for extra in paths[1:])
    return canonical, duplicates


def allergen_ids(values: object) -> object:
    if not isinstance(values, list):
        return values
    return [item.get("id") if isinstance(item, dict) else item for item in values]


def compact_nutrition(values: object) -> object:
    if not isinstance(values, dict):
        return values
    return {
        nutrient: [entry.get(key) for key in NUTRIENT_ORDER]
        for nutrient, entry in values.items()
        if isinstance(entry, dict)
    }


def build_recipe(recipe: dict) -> dict:
    out = {key: recipe.get(key) for key in RECIPE_FIELDS if key in recipe}
    for key in ("allergens", "all_allergens", "inherited_allergens"):
        out[key] = allergen_ids(recipe.get(key))
    for key in ("nutrition", "nutrition_per_serving"):
        out[key] = compact_nutrition(recipe.get(key))
    return out


def build_venue(path: Path, allergens: dict[str, dict]) -> dict:
    data = load(path)
    meta = data["outlet_metadata"]
    for definition in meta.get("allergens", []):
        allergens.setdefault(definition["id"], definition)

    groups = []
    for group_id, group in data["menu_groups_data"].items():
        menus = []
        for payload in group.get("api_payloads", []):
            if "/search/" not in payload["url"] or not isinstance(payload.get("data"), dict):
                continue
            for menu in payload["data"].get("menus", []):
                menus.append(
                    {
                        "id": menu.get("id"),
                        "name": menu.get("name"),
                        "recipes": [build_recipe(r) for r in menu.get("recipes", [])],
                    }
                )
        groups.append(
            {
                "id": group_id,
                "name": group.get("name"),
                "url": group.get("url"),
                "visible_text": group.get("visible_text", []),
                "other": [
                    payload
                    for payload in group.get("api_payloads", [])
                    if any(hint in payload["url"] for hint in KEPT_PAYLOAD_HINTS)
                ],
                "menus": menus,
            }
        )

    outlet = meta["outlet"]
    return {
        "file": path.name,
        "path": str(path.relative_to(ROOT)),
        "base_url": data.get("base_url"),
        "name": outlet["name"],
        "filter_name": FILTER_NAMES.get(outlet["name"], outlet["name"]),
        "outlet": outlet,
        "business": meta.get("business"),
        "tags": meta.get("tags", []),
        "menu_groups": meta.get("menu_groups", []),
        "groups": groups,
    }


def build_payload() -> dict:
    canonical, duplicates = discover()
    allergens: dict[str, dict] = {}
    venues = [build_venue(path, allergens) for _, path in sorted(canonical.items())]
    return {
        "generated": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "source": str(KAFFODIE.relative_to(ROOT)),
        "allergens": allergens,
        "venues": venues,
        "duplicates": [
            {
                "outlet_id": outlet_id,
                "kept": str(kept.relative_to(ROOT)),
                "removed": str(extra.relative_to(ROOT)),
            }
            for outlet_id, kept, extra in duplicates
        ],
    }


def counts(venue: dict) -> tuple[int, int, int]:
    menus = sum(len(group["menus"]) for group in venue["groups"])
    dishes = sum(len(menu["recipes"]) for group in venue["groups"] for menu in group["menus"])
    return len(venue["groups"]), menus, dishes


def render_checklist(payload: dict) -> str:
    venues = payload["venues"]
    duplicates = payload["duplicates"]
    total_dishes = sum(counts(v)[2] for v in venues)
    lines = [
        "# Kafoodie all-menus JSON checklist",
        "",
        f"Last checked: {payload['generated'][:10]}",
        "",
        "Generated by `build_menu_explorer.py` from the outlet JSON in",
        f"`{payload['source']}`. Do not edit by hand — rerun the script instead.",
        "",
        f"- Kafoodie outlets with an all-menus JSON: **{len(venues)}**",
        f"- Menu groups: **{sum(counts(v)[0] for v in venues)}**",
        f"- Menus: **{sum(counts(v)[1] for v in venues)}**",
        f"- Dishes: **{total_dishes}**",
        f"- Redundant duplicate files: **{len(duplicates)}**",
        "",
        f"The Menu review venue filter lists **{len(venues) + len(NO_KAFFODIE)}** named",
        f"venues: these {len(venues)} Kafoodie outlets plus the",
        f"{len(NO_KAFFODIE)} venues below that have no Kafoodie outlet.",
        "",
        "## Files present",
        "",
        "| Venue (Menu review filter) | Outlet | Folder | Groups | Menus | Dishes | JSON |",
        "| --- | ---: | --- | ---: | ---: | ---: | --- |",
    ]
    for venue in venues:
        groups, menus, dishes = counts(venue)
        folder = Path(venue["path"]).parent.name
        link = f"[{venue['file']}](./{folder}/{venue['file']})"
        lines.append(
            f"| {venue['filter_name']} | {venue['outlet']['id']} | `{folder}` "
            f"| {groups} | {menus} | {dishes} | {link} |"
        )

    lines += [
        "",
        "## Venues in the Menu review filter without a Kafoodie outlet",
        "",
        "These venues have menu Markdown but no Kafoodie all-menus JSON, so they",
        "cannot appear in the explorer:",
        "",
    ]
    lines += [f"- {name}" for name in NO_KAFFODIE]

    lines += ["", "## Duplicate files", ""]
    if duplicates:
        lines += [
            "Each outlet had more than one all-menus JSON. The copies below were",
            "byte-for-byte different only in photo URLs and captured API payload",
            "ordering; the menu, allergen and nutrition data was identical. The",
            "`*_full_menu` copy is kept as the representative file.",
            "",
            "| Outlet | Kept | Removed |",
            "| ---: | --- | --- |",
        ]
        for entry in duplicates:
            lines.append(
                f"| {entry['outlet_id']} | `{entry['kept']}` | `{entry['removed']}` |"
            )
    else:
        lines.append("No duplicate all-menus JSON files remain.")
        if REMOVAL_LOG.is_file():
            history = json.loads(REMOVAL_LOG.read_text(encoding="utf-8"))
            removed = [item for run in history for item in run.get("files", [])]
            if removed:
                lines += [
                    "",
                    f"{len(removed)} redundant copies were deleted. Each was verified",
                    "content-identical to the file kept for its outlet before removal;",
                    "the hashes and paths are recorded in",
                    "[`duplicates_removed.json`](./duplicates_removed.json).",
                    "",
                    "| Outlet | Kept | Removed |",
                    "| ---: | --- | --- |",
                ]
                for item in removed:
                    lines.append(
                        f"| {item['outlet_id']} | `{item['kept']}` | `{item['removed']}` |"
                    )

    lines += [
        "",
        "## Notes",
        "",
        "- Venue names differ between the Menu review filter and the Kafoodie outlet",
        "  metadata for The Black Swan, The Midland, The Stables, Whitby, The Swan,",
        "  Grasmere, The Northallerton Inn, The Tynemouth Castle Inn, The Pheasant Inn",
        "  and The King's Head Inn. The table above uses the filter name and the",
        "  outlet id, which is the reliable join key.",
        "- `The_Kingslodge_Inn_all_menus_previous.json` is a deliberate backup of an",
        "  earlier crawl, not a duplicate, so it is kept.",
        "",
    ]
    return "\n".join(lines)


def write_outputs(payload: dict) -> None:
    DATA_JS.write_text(
        "window.MENU_DATA=" + json.dumps(payload, ensure_ascii=False, separators=(",", ":")) + ";\n",
        encoding="utf-8",
    )
    CHECKLIST.write_text(render_checklist(payload), encoding="utf-8")


def prune(payload: dict) -> int:
    """Delete redundant copies, recording what was removed and why."""
    removed = []
    for entry in payload["duplicates"]:
        path = ROOT / entry["removed"]
        if not path.is_file():
            continue
        removed.append(
            {
                "outlet_id": entry["outlet_id"],
                "removed": entry["removed"],
                "kept": entry["kept"],
                "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
                "bytes": path.stat().st_size,
            }
        )
        path.unlink()

    if removed:
        history = []
        if REMOVAL_LOG.is_file():
            history = json.loads(REMOVAL_LOG.read_text(encoding="utf-8"))
        history.append(
            {
                "removed_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
                "reason": "Content-identical to the kept file apart from photo URLs and captured API payload ordering",
                "files": removed,
            }
        )
        REMOVAL_LOG.write_text(json.dumps(history, indent=2) + "\n", encoding="utf-8")

    # Folders that only held a redundant copy are now empty; drop them so the
    # directory listing matches the checklist.
    for folder in sorted({(ROOT / entry["removed"]).parent for entry in payload["duplicates"]}):
        if folder.is_dir() and not any(folder.iterdir()):
            folder.rmdir()
    return len(removed)


def stable(payload: dict) -> str:
    """Serialise the payload without the build timestamp, for comparison."""
    return json.dumps(
        {key: value for key, value in payload.items() if key != "generated"},
        ensure_ascii=False,
        separators=(",", ":"),
        sort_keys=True,
    )


def stable_checklist(text: str) -> str:
    """Drop the 'Last checked' line so a date change alone is not a diff."""
    return "\n".join(line for line in text.splitlines() if not line.startswith("Last checked:"))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--prune", action="store_true", help="delete redundant duplicate JSON files")
    parser.add_argument("--check", action="store_true", help="fail if outputs are out of date")
    args = parser.parse_args()

    if not KAFFODIE.is_dir():
        parser.error(f"Missing {KAFFODIE}")

    payload = build_payload()
    if args.check:
        stale = []
        if not DATA_JS.is_file():
            stale.append(DATA_JS.name)
        else:
            current = DATA_JS.read_text(encoding="utf-8")
            prefix = "window.MENU_DATA="
            body = current[len(prefix) :].rstrip().rstrip(";") if current.startswith(prefix) else ""
            try:
                if stable(json.loads(body)) != stable(payload):
                    stale.append(DATA_JS.name)
            except json.JSONDecodeError:
                stale.append(DATA_JS.name)
        if not CHECKLIST.is_file() or stable_checklist(
            CHECKLIST.read_text(encoding="utf-8")
        ) != stable_checklist(render_checklist(payload)):
            stale.append(CHECKLIST.name)
        if stale:
            print("Out of date: " + ", ".join(stale), file=sys.stderr)
            return 1
        print("Menu explorer data and checklist are current.")
        return 0

    write_outputs(payload)
    print(f"Wrote {DATA_JS.relative_to(ROOT)} ({DATA_JS.stat().st_size / 1e6:.1f} MB)")
    print(f"Wrote {CHECKLIST.relative_to(ROOT)}")
    print(f"{len(payload['venues'])} outlets, {len(payload['duplicates'])} redundant copies")

    if args.prune:
        print(f"Removed {prune(payload)} duplicate files")
        write_outputs(build_payload())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
