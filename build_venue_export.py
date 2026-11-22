#!/usr/bin/env python3
"""Build a standardised per-venue export from the crawled sources.

One venue in, one folder out:

    exports/<Region>/<Venue>/venue.json   canonical, machine-readable record
    exports/<Region>/<Venue>/venue.md     readable view derived from the JSON

The JSON is the source of truth. It merges the three things we hold for a
venue, which until now lived in separate places:

* the printed menus, as PDF-derived Markdown (prices, sections, wording)
* the Kafoodie outlet JSON (allergens, nutrition, dietary tags, dish photos)
* the website crawl (venue profile, serving times, offers, FAQs, media)

Nothing venue-specific lives in this file. Venues are discovered from the
crawl folders, and tunable data is read from ./config:

    config/rules.json     stopwords, spelling variants, drink/promo rules,
                          dietary codes, menu kinds, website page markers
    config/aliases.json   printed-name -> Kafoodie-recipe renames
    config/venues.json    optional per-venue overrides (region, name, slug...)

    python3 build_venue_export.py --list
    python3 build_venue_export.py --venue "The Kingslodge Inn"
    python3 build_venue_export.py --venue kingslodge --check
    python3 build_venue_export.py --all
    python3 build_venue_export.py --venue Offshore --suggest-aliases
"""

from __future__ import annotations

import argparse
import csv
import difflib
import json
import re
import subprocess
import sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent
CRAWL = ROOT / "inncollectiongroup.com_root"
KAFFODIE = CRAWL / "kafoodie"
MENUS_MD = CRAWL / "menus_md"
PDFS = CRAWL / "documents" / "extracted-to-md"
PAGES_TEXT = CRAWL / "pages_text"
MEDIA_CSV = CRAWL / "discovered_media.csv"
EXPORTS = ROOT / "exports"
CONFIG_DIR = ROOT / "config"

SCHEMA_VERSION = "1.0.0"


# --------------------------------------------------------------------------
# configuration
# --------------------------------------------------------------------------
def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def load_config(name: str, required: bool = True) -> dict:
    path = CONFIG_DIR / name
    if not path.is_file():
        if required:
            raise SystemExit(f"Missing config file: {path}")
        return {}
    return {k: v for k, v in load_json(path).items() if not k.startswith("_")}


RULES = load_config("rules.json")
ALIAS_CONFIG = load_config("aliases.json")
VENUE_OVERRIDES = load_config("venues.json", required=False)

STOPWORDS = set(RULES["stopwords"])
SPELLING_VARIANTS = RULES["spelling_variants"]
DIETARY_CODES = RULES["dietary_codes"]
DRINK_SECTIONS = tuple(RULES["drink_sections"])
PROMO_PATTERNS = tuple(RULES["promo_patterns"])
KIDS_SECTION_WORDS = tuple(RULES["kids_section_words"])
KIDS_SUFFIX = RULES["kids_recipe_suffix"]
KIDS_MARKER = RULES["kids_recipe_marker"]
MENU_KINDS = RULES["menu_kinds"]
MENU_KIND_DEFAULT = RULES["menu_kind_default"]
MENU_KIND_ORDER = RULES["menu_kind_order"]
GENERIC_WORDS = set(RULES["generic_name_words"])
MARKERS = RULES["page_markers"]


def alias_tables(venue_id: str) -> tuple[dict[str, str], dict[str, str]]:
    """Global alias tables with any venue-specific entries layered on top."""
    venue = (ALIAS_CONFIG.get("venues") or {}).get(venue_id, {})
    items = {**(ALIAS_CONFIG.get("items") or {}), **(venue.get("items") or {})}
    kids = {**(ALIAS_CONFIG.get("kids") or {}), **(venue.get("kids") or {})}
    return (
        {k.casefold(): v for k, v in items.items()},
        {k.casefold(): v for k, v in kids.items()},
    )


# --------------------------------------------------------------------------
# helpers
# --------------------------------------------------------------------------
def slugify(value: str) -> str:
    value = value.lower().replace("&", " and ")
    value = re.sub(r"[^a-z0-9]+", "-", value)
    return value.strip("-")


def clean_name(value: str) -> str:
    """Undo Markdown escaping and drop Kafoodie's ordering/qualifier noise."""
    value = value.replace("\\*", "*").replace("\\_", "_")
    value = re.sub(r"^\d+\.\s*", "", value)
    value = re.sub(r"^ADD\s+", "", value, flags=re.IGNORECASE)
    value = re.sub(r"\s*\((?:Childrens|Children's|side)\)\s*$", "", value, flags=re.IGNORECASE)
    # Strip dietary codes like (V, GFA), (VG), etc.
    value = re.sub(r"\s*\([A-Z][A-Za-z, ]*\)\s*$", "", value)
    return re.sub(r"\s+", " ", value).strip()


def tokens(value: str) -> set[str]:
    value = clean_name(value).lower().replace("&", " and ")
    value = re.sub(r"[^a-z0-9 ]+", " ", value)
    out = set()
    for word in value.split():
        word = SPELLING_VARIANTS.get(word, word)
        if word in STOPWORDS or len(word) < 2:
            continue
        if word.endswith("ies") and len(word) > 4:
            word = word[:-3] + "y"
        elif word.endswith("s") and not word.endswith("ss") and len(word) > 3:
            word = word[:-1]
        out.add(word)
    return out


def pdf_info(path: Path) -> dict:
    info: dict[str, object] = {}
    try:
        text = subprocess.run(
            ["pdfinfo", str(path)], capture_output=True, text=True, check=True
        ).stdout
    except (OSError, subprocess.CalledProcessError):
        return info
    for line in text.splitlines():
        if ":" not in line:
            continue
        key, _, value = line.partition(":")
        key, value = key.strip().lower(), value.strip()
        if key == "pages":
            info["pages"] = int(value) if value.isdigit() else None
        elif key == "creationdate":
            info["created"] = value
        elif key == "producer":
            info["producer"] = value
    return info


def money(raw: str) -> float | None:
    cleaned = raw.replace("£", "").replace(",", "").strip()
    try:
        return float(cleaned)
    except ValueError:
        return None


# --------------------------------------------------------------------------
# Venue discovery
# --------------------------------------------------------------------------
def key_tokens(name: str) -> list[str]:
    """The distinctive words of a venue name ('The Kingslodge Inn' -> kingslodge)."""
    words = slugify(name).split("-")
    return [w for w in words if w not in GENERIC_WORDS] or words


def folder_to_name(folder: str) -> str:
    folder = re.sub(r"_full_menu$", "", folder)
    return folder.replace("_", " ").strip()


def find_outlet_json(folder: str) -> Path | None:
    candidates = sorted((KAFFODIE / folder).glob("*_all_menus.json"))
    candidates = [path for path in candidates if not path.name.endswith("_previous.json")]
    return candidates[0] if candidates else None


def latest_versions(files: list[Path]) -> list[Path]:
    """Keep only the highest '-vN' of a menu that has been re-issued."""
    best: dict[str, tuple[int, Path]] = {}
    for path in files:
        match = re.match(r"^(.*?)(?:-v(\d+))?$", path.stem)
        base, version = match.group(1), int(match.group(2) or 0)
        if base not in best or version > best[base][0]:
            best[base] = (version, path)
    return [path for _, path in best.values()]


def menu_kind(filename: str) -> str:
    name = filename.lower()
    for kind, keywords in MENU_KINDS:
        if any(word in name for word in keywords):
            return kind
    return MENU_KIND_DEFAULT


def menu_sort_key(filename: str) -> tuple[int, str]:
    kind = menu_kind(filename)
    order = MENU_KIND_ORDER.index(kind) if kind in MENU_KIND_ORDER else len(MENU_KIND_ORDER)
    return order, filename


def discover_slug(tokens_: list[str]) -> str | None:
    """Find the website page for a venue by matching page filenames to its name."""
    if not PAGES_TEXT.is_dir():
        return None
    for path in sorted(PAGES_TEXT.glob("*.txt")):
        base = path.stem.removesuffix("_restaurant")
        if "_" in base:
            continue
        words = [w for w in base.split("-") if w not in GENERIC_WORDS]
        if words == tokens_:
            return base
    return None


def discover_region(names: list[str]) -> str | None:
    """Region from an existing export folder, else the accommodation page that lists the venue."""
    if EXPORTS.is_dir():
        for region_dir in sorted(p for p in EXPORTS.iterdir() if p.is_dir()):
            if any((region_dir / name).is_dir() for name in names):
                return region_dir.name
    pattern = re.compile(RULES["region_page_pattern"])
    found = set()
    if PAGES_TEXT.is_dir():
        for path in sorted(PAGES_TEXT.glob("accommodation_*.txt")):
            match = pattern.match(path.name)
            if not match:
                continue
            text = path.read_text(encoding="utf-8", errors="replace")
            if any(name in text for name in names):
                found.add(match.group(1))
    if len(found) == 1:
        return re.sub(r"\bAnd\b", "and", next(iter(found)).replace("-", " ").title())
    return None


def discover_venues() -> dict[str, dict]:
    """Build the venue registry from the crawl folders plus config/venues.json."""
    if not KAFFODIE.is_dir():
        return {}

    venues: dict[str, dict] = {}
    for folder in sorted(p for p in KAFFODIE.iterdir() if p.is_dir()):
        if find_outlet_json(folder.name) is None:
            continue
        discovered = folder_to_name(folder.name)
        venue_id = slugify(discovered)
        override = VENUE_OVERRIDES.get(venue_id, {})
        name = override.get("name", discovered)
        venue_tokens = override.get("menu_tokens") or key_tokens(discovered)
        slug = override.get("slug") or discover_slug(key_tokens(discovered))
        venues[name] = {
            "id": venue_id,
            "discoveredName": discovered,
            "region": override.get("region"),
            "slug": slug,
            "patterns": tuple(
                override.get("patterns")
                or [r"[-_ ]?".join(re.escape(t) for t in venue_tokens)]
            ),
            "kafoodie": folder.name,
            "tokens": venue_tokens,
            "menu_files": tuple(override.get("menu_files") or ()),
        }

    # Assign each menu file to the venue whose name tokens it contains. When
    # several venues match ("swan" vs "black swan"), the most specific wins.
    claimed: dict[str, list[Path]] = {name: [] for name in venues}
    explicit = {name for name, cfg in venues.items() if cfg["menu_files"]}
    for path in sorted(MENUS_MD.glob("*.md")) if MENUS_MD.is_dir() else []:
        words = set(slugify(path.stem).split("-"))
        matches = [
            (len(cfg["tokens"]), name)
            for name, cfg in venues.items()
            if name not in explicit and set(cfg["tokens"]) <= words
        ]
        if not matches:
            continue
        best = max(size for size, _ in matches)
        for size, name in matches:
            if size == best:
                claimed[name].append(path)

    for name, cfg in venues.items():
        if not cfg["menu_files"]:
            cfg["menu_files"] = tuple(
                sorted((p.name for p in latest_versions(claimed[name])), key=menu_sort_key)
            )
        if not cfg["region"]:
            cfg["region"] = (
                discover_region([name, cfg["discoveredName"]]) or RULES["region_unknown"]
            )
    return venues


VENUES = discover_venues()


def resolve_venue(query: str) -> str:
    """Accept a venue's exact name, its id, or any unambiguous fragment."""
    needle = slugify(query)
    exact = [n for n, c in VENUES.items() if n.casefold() == query.casefold() or c["id"] == needle]
    if exact:
        return exact[0]
    partial = [n for n, c in VENUES.items() if needle in slugify(n) or needle in c["id"]]
    if len(partial) == 1:
        return partial[0]
    if not partial:
        raise SystemExit(f"Unknown venue '{query}'. Use --list to see discovered venues.")
    raise SystemExit(f"'{query}' is ambiguous: " + ", ".join(sorted(partial)))


# --------------------------------------------------------------------------
# Markdown menu parsing
# --------------------------------------------------------------------------
ITEM_RE = re.compile(r"^- \*\*(?P<name>.+?)\*\*(?P<rest>.*)$")
DESC_RE = re.compile(r"^  - (?P<text>.+)$")
NOTE_RE = re.compile(r"^\*(?P<text>.+)\*$")
HEADING_RE = re.compile(r"^(?P<hashes>#{2,4}) (?P<text>.+)$")
DIRECTIVE_RE = re.compile(r"^<!--\s*(?P<key>[a-z]+):\s*(?P<value>.*?)\s*-->$")
DIETARY_RE = re.compile(r"\((?P<codes>[A-Z][A-Za-z, ]*)\)")
PRICE_SPLIT = " · "


def parse_item(line: str, page: int | None, columns: list[str] | None) -> dict:
    match = ITEM_RE.match(line)
    assert match
    name = match.group("name").strip().rstrip("\\").strip()
    rest = match.group("rest").strip().lstrip("*").strip()

    dietary: list[str] = []
    recommended = "♛" in rest
    rest = rest.replace("♛", "").strip()

    dietary_match = DIETARY_RE.search(rest)
    if dietary_match:
        dietary = [code.strip() for code in dietary_match.group("codes").split(",") if code.strip()]
        rest = (rest[: dietary_match.start()] + rest[dietary_match.end() :]).strip()

    prices: list[dict] = []
    # Two price formats:
    # 1. Dotted style: " · 8.50" or " · 20 · 7 · 5.5"
    # 2. Trailing style: "With crusty sourdough and butter 4.95"
    if rest.startswith("·"):
        raw_prices = [part.strip() for part in rest[1:].split("·")]
        for index, raw in enumerate(raw_prices):
            label = None
            if columns and index < len(columns):
                label = columns[index]
            prices.append({"raw": raw, "amount": money(raw), "label": label})
    else:
        price_matches = list(re.finditer(r"\s+(\d+(?:\.\d{2})?)\s*$", rest))
        if price_matches:
            last_match = price_matches[-1]
            raw_price = last_match.group(1)
            prices.append({"raw": raw_price, "amount": money(raw_price), "label": columns[0] if columns else None})
            rest = rest[: last_match.start()].strip()
        elif rest:
            # Trailing text that is not a price list (e.g. "with any kids' mains").
            name = f"{name} {rest}".strip()

    return {
        "name": name,
        "dietary": dietary,
        "recommended": recommended,
        "prices": prices,
        "priceInName": bool(re.search(r"£\s?\d", name)),
        "description": None,
        "notes": [],
        "page": page,
    }


def parse_menu_markdown(path: Path) -> dict:
    lines = path.read_text(encoding="utf-8").splitlines()
    menu: dict = {
        "id": slugify(path.stem),
        "name": None,
        "kind": None,
        "source": {"markdown": str(path.relative_to(ROOT))},
        "sections": [],
    }
    page: int | None = None
    # A cols directive labels the heading it sits under and every sub-heading
    # below it, until the next heading of the same or a higher level.
    columns_by_level: dict[int, list[str]] = {}
    section: dict | None = None
    item: dict | None = None

    def active_columns() -> list[str] | None:
        if not columns_by_level:
            return None
        return columns_by_level[max(columns_by_level)]

    def ensure_section() -> dict:
        nonlocal section
        if section is None:
            section = {
                "name": None,
                "level": 0,
                "page": page,
                "notes": [],
                "columns": active_columns(),
                "items": [],
            }
            menu["sections"].append(section)
        return section

    for raw in lines:
        line = raw.rstrip()
        if not line.strip():
            item = None
            continue

        directive = DIRECTIVE_RE.match(line.strip())
        if directive:
            key, value = directive.group("key"), directive.group("value")
            if key == "page":
                page = int(value) if value.isdigit() else page
                if section is not None and section["items"]:
                    section = None
            elif key == "cols":
                columns = [part.strip() for part in value.split("|")]
                level = section["level"] if section else 2
                columns_by_level[level] = columns
                ensure_section()["columns"] = columns
            elif key == "source":
                menu["source"]["pdf"] = value
            continue

        if line.startswith("# ") and menu["name"] is None:
            menu["name"] = line[2:].strip()
            continue

        heading = HEADING_RE.match(line)
        if heading:
            level = len(heading.group("hashes"))
            for stale in [depth for depth in columns_by_level if depth >= level]:
                del columns_by_level[stale]
            section = {
                "name": heading.group("text").strip(),
                "level": level,
                "page": page,
                "notes": [],
                "columns": active_columns(),
                "items": [],
            }
            menu["sections"].append(section)
            item = None
            continue

        if ITEM_RE.match(line):
            target = ensure_section()
            item = parse_item(line, page, target["columns"])
            target["items"].append(item)
            continue

        desc = DESC_RE.match(line)
        if desc and item is not None:
            text = desc.group("text").strip()
            # Also extract price from description line if item has no price yet
            if not item["prices"]:
                price_matches = list(re.finditer(r"\s+(\d+(?:\.\d{2})?)\s*$", text))
                if price_matches:
                    last_match = price_matches[-1]
                    raw_price = last_match.group(1)
                    item["prices"].append({"raw": raw_price, "amount": money(raw_price), "label": None})
                    text = text[: last_match.start()].strip()
            if item["description"] is None:
                item["description"] = text
            else:
                item["notes"].append(text)
            continue

        note = NOTE_RE.match(line.strip())
        if note:
            target = ensure_section()
            target["notes"].append(
                {"text": note.group("text").strip(), "afterItem": len(target["items"]) - 1 if target["items"] else None}
            )
            item = None
            continue

    menu["kind"] = menu_kind(path.name)
    if menu["name"] is None:
        menu["name"] = path.stem
    return menu


def menu_stats(menu: dict) -> dict:
    items = [item for section in menu["sections"] for item in section["items"]]
    return {
        "sections": len([s for s in menu["sections"] if s["name"]]),
        "items": len(items),
        "itemsWithPrice": sum(1 for item in items if item["prices"]),
        "itemsWithDescription": sum(1 for item in items if item["description"]),
        "itemsRecommended": sum(1 for item in items if item["recommended"]),
        "itemsDietaryTagged": sum(1 for item in items if item["dietary"]),
    }


# --------------------------------------------------------------------------
# Kafoodie products
# --------------------------------------------------------------------------
def allergen_split(recipe: dict) -> tuple[list[dict], list[dict]]:
    contains, may_contain = [], []
    for entry in recipe.get("allergens") or []:
        record = {
            "id": entry.get("id"),
            "name": entry.get("name"),
            "label": entry.get("label"),
            "abbr": entry.get("abbr"),
            "primaryId": entry.get("primary_id"),
        }
        (may_contain if entry.get("is_may_contain") else contains).append(record)
    return contains, may_contain


def nutrition_block(recipe: dict) -> dict | None:
    for key in ("nutrition_per_serving", "nutrition"):
        values = recipe.get(key)
        if not values:
            continue
        nutrients = {}
        for nutrient, entry in values.items():
            if not isinstance(entry, dict):
                continue
            nutrients[nutrient] = {
                "quantity": entry.get("quantity"),
                "unit": entry.get("unit"),
                "reference": entry.get("est"),
                "percentReference": entry.get("actual_ratio"),
                "level": entry.get("doze"),
            }
        return {"basis": "per serving" if key.endswith("per_serving") else "per 100g", "nutrients": nutrients}
    return None


def build_products(outlet: dict) -> list[dict]:
    products: dict[int, dict] = {}
    for group_id, group in outlet["menu_groups_data"].items():
        for payload in group.get("api_payloads", []):
            data = payload.get("data")
            if not isinstance(data, dict) or "menus" not in data:
                continue
            for menu in data["menus"]:
                for recipe in menu.get("recipes", []):
                    recipe_id = recipe.get("id")
                    if recipe_id in products:
                        continue
                    contains, may_contain = allergen_split(recipe)
                    products[recipe_id] = {
                        "id": recipe_id,
                        "name": recipe.get("name"),
                        "menuGroup": group.get("name"),
                        "menuGroupId": int(group_id),
                        "menu": menu.get("name"),
                        "menuId": menu.get("id"),
                        "description": recipe.get("description"),
                        "photo": recipe.get("photo"),
                        "prices": recipe.get("prices") or [],
                        "dietaryTags": [tag.get("name") for tag in recipe.get("tags") or []],
                        "allergens": contains,
                        "mayContain": may_contain,
                        "nutrition": nutrition_block(recipe),
                        "ingredients": recipe.get("ingredients_simple"),
                        "deliveryMethods": recipe.get("delivery_methods") or [],
                        "isPublic": recipe.get("isPublic"),
                        "allergenDataMissing": bool(recipe.get("is_pw_allergen_not_set")),
                    }
    return sorted(products.values(), key=lambda p: (p["menuGroupId"], p["id"]))


def allergen_definitions(outlet: dict) -> list[dict]:
    definitions = []
    for entry in outlet["outlet_metadata"].get("allergens", []):
        definitions.append(
            {
                "id": entry.get("id"),
                "name": entry.get("name"),
                "label": entry.get("label"),
                "abbr": entry.get("abbr"),
                "mayContain": bool(entry.get("is_may_contain")),
                "primaryId": entry.get("primary_id"),
                "sortOrder": entry.get("sortorder"),
                "description": entry.get("description") or None,
            }
        )
    return sorted(definitions, key=lambda d: (d["sortOrder"] or 0, d["id"]))


# --------------------------------------------------------------------------
# Matching printed items to Kafoodie products
# --------------------------------------------------------------------------
def classify_item(item: dict, section_name: str, kind: str) -> str:
    """Say what a printed line is, so unmatched lines can be triaged."""
    name = clean_name(item["name"]).lower()
    section = (section_name or "").lower()
    if kind == "Drinks" or any(word in section for word in DRINK_SECTIONS):
        return "drink"
    if any(re.search(pattern, name) for pattern in PROMO_PATTERNS):
        return "promo"
    if not item["prices"] and not item["description"]:
        return "heading"
    # A described line with no price is a base or a choice list ("Rainbow Bowls",
    # "Breakfast Sandwiches"), not a dish you can order on its own.
    if not item["prices"]:
        return "grouping"
    return "dish"


def suggest_products(item_name: str, products: list[dict], limit: int = 3) -> list[dict]:
    """Closest Kafoodie names by string similarity, to help write new aliases."""
    target = clean_name(item_name).casefold()
    scored = sorted(
        (
            (difflib.SequenceMatcher(None, target, clean_name(p["name"] or "").casefold()).ratio(), p["name"])
            for p in products
        ),
        reverse=True,
    )[:limit]
    return [{"product": name, "score": round(score, 2)} for score, name in scored if score >= 0.4]


def match_products(
    menus: list[dict],
    products: list[dict],
    item_aliases: dict[str, str],
    kids_aliases: dict[str, str],
) -> dict:
    """Link each printed dish to its Kafoodie recipe.

    Confidence is recorded per link so a reviewer can see which allergen and
    nutrition records were attached by name and which by a listed rename.
    """
    index = [(product, tokens(product["name"] or "")) for product in products]
    by_name = {(product["name"] or "").casefold(): product for product in products}
    token_owners: dict[str, int] = {}
    for _, product_tokens in index:
        for token in product_tokens:
            token_owners[token] = token_owners.get(token, 0) + 1

    report = {
        "matched": 0,
        "matchedExact": 0,
        "matchedAlias": 0,
        "matchedTokens": 0,
        "unmatched": 0,
        "ambiguous": 0,
        "skipped": 0,
        "unmatchedItems": [],
        "ambiguousItems": [],
        "unmatchedDishes": [],
        "staleAliases": [],
    }

    def link(item: dict, product: dict, score: float, via: str, ambiguous: bool = False) -> None:
        item["product"] = {
            "id": product["id"],
            "name": product["name"],
            "matchScore": round(score, 3),
            "ambiguous": ambiguous,
            "via": via,
        }
        report["matched"] += 1
        report[f"matched{via.capitalize()}"] += 1

    for menu in menus:
        for section in menu["sections"]:
            section_name = (section["name"] or "").lower()
            kids_section = any(word in section_name for word in KIDS_SECTION_WORDS)
            for item in section["items"]:
                item["product"] = None
                item["kind"] = classify_item(item, section["name"], menu["kind"])
                # Headings, promos and drinks are not dishes; matching them would
                # attach allergen data to something that is not a plated item.
                if item["kind"] != "dish":
                    report["skipped"] += 1
                    continue

                item_tokens = tokens(item["name"])
                if not item_tokens:
                    report["skipped"] += 1
                    continue

                key = clean_name(item["name"]).casefold()

                # 1. A listed rename. Kids sections use their own table first,
                #    because the same printed line is a different recipe there.
                alias = (kids_aliases.get(key) if kids_section else None) or item_aliases.get(key)
                if alias:
                    target = by_name.get(alias.casefold())
                    if target is not None:
                        link(item, target, 1.0, "alias")
                        continue
                    report["staleAliases"].append(
                        {"menu": menu["name"], "item": item["name"], "alias": alias}
                    )

                # 2. The printed name exactly as Kafoodie spells it. In a kids
                #    section the children's recipe wins over the adult one.
                exact = None
                if kids_section:
                    exact = by_name.get(f"{clean_name(item['name'])}{KIDS_SUFFIX}".casefold())
                if exact is None:
                    exact = by_name.get(key)
                if exact is not None:
                    link(item, exact, 1.0, "exact")
                    continue

                # 3. Token overlap, used only when it is unambiguous.
                scored = []
                for product, product_tokens in index:
                    shared = item_tokens & product_tokens
                    if not shared:
                        continue
                    coverage_item = len(shared) / len(item_tokens)
                    coverage_product = len(shared) / len(product_tokens)
                    score = max(coverage_item, (coverage_item + coverage_product) / 2)
                    # A single shared token is only enough when it is distinctive
                    # and belongs to exactly one product ("lasagne").
                    if len(shared) == 1:
                        token = next(iter(shared))
                        if len(token) < 5 or token_owners.get(token, 0) != 1:
                            continue
                        score = max(score, 0.5)
                    elif score < 0.55:
                        continue
                    product_is_kids = KIDS_MARKER in (product["name"] or "").lower()
                    if product_is_kids == kids_section:
                        score += 0.1
                    scored.append((score, product))
                scored.sort(key=lambda pair: pair[0], reverse=True)

                if not scored:
                    report["unmatched"] += 1
                    entry = {
                        "menu": menu["name"],
                        "item": item["name"],
                        "suggestions": suggest_products(item["name"], products),
                    }
                    report["unmatchedItems"].append(entry)
                    report["unmatchedDishes"].append(entry)
                    continue

                best_score, best = scored[0]
                runner_up = scored[1][0] if len(scored) > 1 else 0.0
                ambiguous = runner_up >= best_score - 0.05
                link(item, best, best_score, "tokens", ambiguous)
                if ambiguous:
                    report["ambiguous"] += 1
                    report["ambiguousItems"].append(
                        {
                            "menu": menu["name"],
                            "item": item["name"],
                            "candidates": [product["name"] for _, product in scored[:3]],
                        }
                    )
    return report


# --------------------------------------------------------------------------
# Website profile
# --------------------------------------------------------------------------
def read_page(slug: str | None, suffix: str = "") -> list[str] | None:
    if not slug:
        return None
    path = PAGES_TEXT / f"{slug}{suffix}.txt"
    if not path.is_file():
        return None
    return path.read_text(encoding="utf-8").splitlines()


def slice_between(lines: list[str], start: str, end: str | None) -> list[str]:
    try:
        first = lines.index(start) + 1
    except ValueError:
        return []
    if end is None:
        return lines[first:]
    for index in range(first, len(lines)):
        if lines[index] == end:
            return lines[first:index]
    return lines[first:]


def first_marker(lines: list[str], markers: list[str]) -> str | None:
    for marker in markers:
        if marker in lines:
            return marker
    return None


def build_profile(name: str, config: dict) -> dict:
    slug = config["slug"]
    main = read_page(slug) or []
    restaurant = read_page(slug, "_restaurant") or []
    # The page may use the venue's discovered name rather than a display override.
    names = list(dict.fromkeys([name, config["discoveredName"]]))

    profile: dict = {"website": f"https://www.inncollectiongroup.com/{slug}/" if slug else None}

    def starts_with_name(line: str) -> bool:
        return any(line.startswith(n + ",") for n in names)

    # Address: first line that starts with the venue name followed by comma
    address_line = next((line for line in main if starts_with_name(line)), None)
    if address_line:
        parts = [part.strip() for part in address_line.split(",")]
        profile["address"] = {
            "raw": address_line,
            "street": parts[1] if len(parts) > 1 else None,
            "locality": parts[2] if len(parts) > 2 else None,
            "city": parts[3] if len(parts) > 3 else None,
            "postcode": parts[4] if len(parts) > 4 else None,
        }

    # Phone: UK number pattern
    phone = next((line for line in main if re.fullmatch(r"0[\d ]{9,13}", line.strip())), None)
    if phone:
        digits = re.sub(r"\D", "", phone)
        profile["phone"] = f"{digits[:4]} {digits[4:7]} {digits[7:]}" if len(digits) == 11 else digits

    amenities = slice_between(main, MARKERS["amenities_start"], MARKERS["amenities_end"])
    profile["amenities"] = [line.strip() for line in amenities if line.strip()]

    # Description: first substantial paragraphs after the address
    description = []
    found_address = False
    skip_prefixes = tuple(MARKERS["description_skip_prefixes"])
    for line in main:
        if starts_with_name(line):
            found_address = True
            continue
        if found_address and line.strip() and not line.startswith(skip_prefixes):
            description.append(line.strip())
            if len(description) >= MARKERS["description_lines"]:
                break
    profile["description"] = description

    # Serving times: between the serving marker and the address line on the restaurant page
    restaurant_address_idx = None
    for i, line in enumerate(restaurant):
        if any(n in line for n in names) and any(c.isdigit() for c in line):
            restaurant_address_idx = i
            break
    if restaurant_address_idx is None:
        for i, line in enumerate(restaurant):
            if line.strip() == MARKERS["features_start"]:
                restaurant_address_idx = i
                break
    serving_end = restaurant_address_idx if restaurant_address_idx is not None else len(restaurant)
    serving = slice_between(
        restaurant,
        MARKERS["serving_start"],
        restaurant[serving_end] if serving_end < len(restaurant) else None,
    )
    times = []
    for index in range(0, len(serving) - 1, 2):
        label, hours = serving[index].strip(), serving[index + 1].strip()
        if label and hours:
            times.append({"name": label, "hours": hours})
    profile["servingTimes"] = times

    features = slice_between(restaurant, MARKERS["features_start"], MARKERS["features_end"])
    profile["diningFeatures"] = [line.strip() for line in features if line.strip()]

    offers = []
    offer_lines = slice_between(main, MARKERS["offers_start"], MARKERS["offers_end"])
    for index, line in enumerate(offer_lines):
        if line.strip() == MARKERS["offer_button"] and index >= 2:
            offers.append({"name": offer_lines[index - 2].strip(), "description": offer_lines[index - 1].strip()})
    profile["offers"] = offers

    faq_end = first_marker(main, MARKERS["faq_end_markers"])
    faq_lines = slice_between(main, MARKERS["faq_start"], faq_end)
    faqs = []
    question = None
    answer: list[str] = []
    question_starts = tuple(MARKERS["faq_question_starts"])
    for line in faq_lines:
        stripped = line.strip()
        if stripped == MARKERS["faq_close"]:
            if question:
                faqs.append({"question": question, "answer": " ".join(answer).strip()})
            question, answer = None, []
            continue
        if question is None:
            if stripped.endswith("?") or stripped.startswith(question_starts):
                question = stripped
            continue
        answer.append(stripped)
    profile["faqs"] = faqs

    nearby_end = first_marker(main, MARKERS["nearby_end_markers"])
    nearby_lines = slice_between(main, MARKERS["nearby_start"], nearby_end)
    nearby = []
    for index, line in enumerate(nearby_lines):
        if line.strip() == MARKERS["nearby_button"] and index >= 2:
            nearby.append({"name": nearby_lines[index - 2].strip(), "location": nearby_lines[index - 1].strip()})
    profile["nearbyInns"] = nearby

    attraction_lines = slice_between(main, MARKERS["attractions_start"], MARKERS["attractions_end"])
    attractions = []
    for index, line in enumerate(attraction_lines):
        if re.fullmatch(r"\d+ (Minutes?|Hours?)", line.strip()) and index >= 1:
            attractions.append({"name": attraction_lines[index - 1].strip(), "travel": line.strip()})
    profile["attractions"] = attractions

    return profile


# --------------------------------------------------------------------------
# Media inventory
# --------------------------------------------------------------------------
def build_media(config: dict) -> dict:
    patterns = [re.compile(pattern, re.IGNORECASE) for pattern in config["patterns"]]
    images, documents = [], []
    if MEDIA_CSV.is_file():
        with MEDIA_CSV.open(newline="", encoding="utf-8") as handle:
            for row in csv.DictReader(handle):
                path = row.get("path") or ""
                if not any(pattern.search(path) for pattern in patterns):
                    continue
                record = {"url": row["url"], "path": path, "type": row.get("type")}
                (documents if row.get("type") == "document" else images).append(record)

    def dedupe(records: list[dict]) -> list[dict]:
        seen, out = set(), []
        for record in records:
            if record["path"] in seen:
                continue
            seen.add(record["path"])
            out.append(record)
        return sorted(out, key=lambda r: r["path"])

    return {"images": dedupe(images), "documents": dedupe(documents)}


def local_assets(venue_dir: Path) -> dict:
    assets: dict[str, list[str]] = {}
    if not venue_dir.is_dir():
        return assets
    for path in sorted(venue_dir.rglob("*")):
        if not path.is_file() or path.name in {"venue.json", "venue.md"}:
            continue
        category = path.relative_to(venue_dir).parts[0]
        assets.setdefault(category, []).append(str(path.relative_to(ROOT)))
    return assets


# --------------------------------------------------------------------------
# Assemble
# --------------------------------------------------------------------------
def build_venue(name: str) -> dict:
    config = VENUES[name]
    outlet_path = find_outlet_json(config["kafoodie"])
    if outlet_path is None:
        raise SystemExit(f"No Kafoodie all-menus JSON in {KAFFODIE / config['kafoodie']}")

    outlet = load_json(outlet_path)
    products = build_products(outlet)

    menus = []
    for filename in config["menu_files"]:
        path = MENUS_MD / filename
        if not path.is_file():
            raise SystemExit(f"Missing menu Markdown: {path}")
        menu = parse_menu_markdown(path)
        pdf_name = menu["source"].get("pdf")
        if pdf_name:
            pdf_path = PDFS / pdf_name
            menu["source"]["pdfPath"] = str(pdf_path.relative_to(ROOT)) if pdf_path.is_file() else None
            menu["source"]["pdfInfo"] = pdf_info(pdf_path) if pdf_path.is_file() else {}
        menu["stats"] = menu_stats(menu)
        menus.append(menu)

    item_aliases, kids_aliases = alias_tables(config["id"])
    match_report = match_products(menus, products, item_aliases, kids_aliases)

    venue_dir = EXPORTS / config["region"] / name
    media = build_media(config)
    media["localAssets"] = local_assets(venue_dir)

    outlet_meta = outlet["outlet_metadata"]["outlet"]
    profile = build_profile(name, config)

    items = [item for menu in menus for section in menu["sections"] for item in section["items"]]
    dishes = [item for item in items if item["kind"] == "dish"]
    matched_ids = {item["product"]["id"] for item in dishes if item["product"]}
    products_with_allergens = sum(1 for p in products if p["allergens"] or p["mayContain"])
    products_with_nutrition = sum(1 for p in products if p["nutrition"])
    products_with_photo = sum(1 for p in products if p["photo"])
    duplicate_names = sorted(
        pname for pname, count in Counter(p["name"] for p in products).items() if count > 1
    )

    coverage = {
        "menus": len(menus),
        "menuLines": len(items),
        "dishes": len(dishes),
        "dishesWithPrice": sum(1 for item in dishes if item["prices"]),
        "dishesWithDescription": sum(1 for item in dishes if item["description"]),
        "dishesMatchedToProduct": match_report["matched"],
        "dishesUnmatched": match_report["unmatched"],
        "dishesAmbiguous": match_report["ambiguous"],
        "nonDishLines": len(items) - len(dishes),
        "products": len(products),
        "productsWithAllergens": products_with_allergens,
        "productsWithNutrition": products_with_nutrition,
        "productsWithPhoto": products_with_photo,
        "productsLinkedFromMenus": len(matched_ids),
        "pdfMenus": sum(1 for menu in menus if menu["source"].get("pdfPath")),
        "mediaImages": len(media["images"]),
        "mediaDocuments": len(media["documents"]),
    }

    gaps = []
    if not menus:
        gaps.append("No printed menus were found for this venue; add them to menus_md or set `menu_files` in config/venues.json.")
    if not config["slug"]:
        gaps.append("No website page was found for this venue; set `slug` in config/venues.json.")
    if config["region"] == RULES["region_unknown"]:
        gaps.append("Region could not be determined; set `region` in config/venues.json.")
    if coverage["dishesWithPrice"] < coverage["dishes"]:
        gaps.append(
            f"{coverage['dishes'] - coverage['dishesWithPrice']} dishes carry no printed price."
        )
    if match_report["unmatched"]:
        gaps.append(
            f"{match_report['unmatched']} dishes have no Kafoodie product match, so they have no "
            "allergen or nutrition record from that source."
        )
    if match_report["staleAliases"]:
        gaps.append(
            f"{len(match_report['staleAliases'])} aliases point at a Kafoodie recipe that no longer exists; "
            "update config/aliases.json."
        )
    if not any(product["prices"] for product in products):
        gaps.append("Kafoodie returns no prices for this outlet; prices come from the printed menus only.")
    if any(menu["kind"] == "Drinks" for menu in menus):
        gaps.append("Drinks menus have no Kafoodie outlet data, so they carry no allergen or nutrition records.")
    if match_report["ambiguous"]:
        gaps.append(f"{match_report['ambiguous']} dish matches were ambiguous and need a human check.")
    if duplicate_names:
        gaps.append(
            "Kafoodie holds more than one recipe under the same name ("
            + ", ".join(duplicate_names)
            + "); the first is linked and the rest are kept in `products`."
        )
    if coverage["productsWithAllergens"] < coverage["products"]:
        missing = [p["name"] for p in products if not (p["allergens"] or p["mayContain"])]
        gaps.append(
            f"{len(missing)} products have no allergen data in Kafoodie: " + ", ".join(missing) + "."
        )

    return {
        "schemaVersion": SCHEMA_VERSION,
        "generated": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "venue": {
            "id": slugify(name),
            "name": name,
            "region": config["region"],
            "outletId": outlet.get("outlet_id"),
            "kafoodieBaseUrl": outlet.get("base_url"),
            "kafoodieSource": str(outlet_path.relative_to(ROOT)),
            **profile,
            "outletFlags": {
                key: outlet_meta.get(key)
                for key in (
                    "is_allergens_enabled",
                    "is_nutritions_enabled",
                    "is_tags_enabled",
                    "is_ingredients_enabled",
                    "is_micronutrients_enabled",
                )
            },
        },
        "menus": menus,
        "products": products,
        "allergens": allergen_definitions(outlet),
        "dietaryTags": outlet["outlet_metadata"].get("tags", []),
        "dietaryCodes": DIETARY_CODES,
        "media": media,
        "coverage": coverage,
        "gaps": gaps,
        "matchReport": match_report,
    }


# --------------------------------------------------------------------------
# Markdown rendering
# --------------------------------------------------------------------------
COVERAGE_LABELS = {
    "menus": "Menus",
    "menuLines": "Printed lines",
    "dishes": "Dishes",
    "dishesWithPrice": "Dishes with a price",
    "dishesWithDescription": "Dishes with a description",
    "dishesMatchedToProduct": "Dishes linked to a product",
    "dishesUnmatched": "Dishes without a product",
    "dishesAmbiguous": "Dishes with an ambiguous link",
    "nonDishLines": "Non-dish lines (drinks, promos, headings)",
    "products": "Products",
    "productsWithAllergens": "Products with allergen data",
    "productsWithNutrition": "Products with nutrition",
    "productsWithPhoto": "Products with a photo",
    "productsLinkedFromMenus": "Products linked from a menu",
    "pdfMenus": "Menus with a PDF",
    "mediaImages": "Images discovered",
    "mediaDocuments": "Documents discovered",
}


def primary_allergens(entries: list[dict]) -> list[str]:
    """Collapse sub-allergens (Wheat, Barley…) into their parent (Gluten)."""
    names = []
    for entry in entries:
        if entry.get("primaryId"):
            continue
        if entry["name"] not in names:
            names.append(entry["name"])
    return names


def product_line(link: dict, products_by_id: dict[int, dict]) -> str:
    """One italic line summarising the linked product's allergen and nutrition data."""
    product = products_by_id.get(link["id"])
    if product is None:
        return f"*product: {link['name']} #{link['id']} (not in this outlet's data)*"

    parts = [f"#{product['id']} {product['name']}"]
    if link.get("via") != "exact":
        parts.append(f"via {link['via']}")
    if link.get("ambiguous"):
        parts.append("ambiguous")

    contains = ", ".join(primary_allergens(product["allergens"])) or "none declared"
    parts.append(f"contains {contains}")
    may = primary_allergens(product["mayContain"])
    if may:
        parts.append("may contain " + ", ".join(may))
    if product["dietaryTags"]:
        parts.append(", ".join(product["dietaryTags"]))
    if product["nutrition"]:
        energy = product["nutrition"]["nutrients"].get("energy")
        if energy and energy["quantity"] is not None:
            parts.append(f"{energy['quantity']:g} {energy['unit']}")
    if product["photo"]:
        parts.append("photo")
    return "*" + " · ".join(parts) + "*"


def render_markdown(data: dict) -> str:
    venue = data["venue"]
    coverage = data["coverage"]
    products_by_id = {product["id"]: product for product in data["products"]}
    lines = [
        f"# {venue['name']}",
        "",
        f"*{venue['region']} · generated {data['generated'][:10]} from `venue.json` (schema {data['schemaVersion']})*",
        "",
    ]

    address = venue.get("address") or {}
    if address.get("raw"):
        lines.append(f"**Address:** {address['raw']}  ")
    if venue.get("phone"):
        lines.append(f"**Phone:** {venue['phone']}  ")
    if venue.get("website"):
        lines.append(f"**Website:** {venue['website']}  ")
    lines.append(f"**Kafoodie outlet:** {venue['outletId']} · {venue['kafoodieBaseUrl']}")
    lines.append("")

    if venue.get("description"):
        lines += ["## About", ""]
        lines += [f"{paragraph}" for paragraph in venue["description"]]
        lines.append("")

    if venue.get("amenities"):
        lines += ["## Amenities", "", ", ".join(venue["amenities"]), ""]

    if venue.get("servingTimes"):
        lines += ["## Serving times", "", "| Service | Hours |", "| --- | --- |"]
        lines += [f"| {row['name']} | {row['hours']} |" for row in venue["servingTimes"]]
        lines.append("")

    lines += ["## Coverage", "", "| Measure | Count |", "| --- | ---: |"]
    for key, value in coverage.items():
        lines.append(f"| {COVERAGE_LABELS.get(key, key)} | {value} |")
    lines.append("")

    if data["gaps"]:
        lines += ["## Gaps", ""]
        lines += [f"- {gap}" for gap in data["gaps"]]
        lines.append("")

    lines += ["## Menus", ""]
    for menu in data["menus"]:
        source = menu["source"]
        lines += [f"### {menu['name']}", ""]
        meta = [f"kind: {menu['kind']}"]
        if source.get("pdf"):
            pages = (source.get("pdfInfo") or {}).get("pages")
            meta.append(f"PDF: `{source['pdf']}`" + (f" ({pages} pages)" if pages else ""))
        meta.append(f"Markdown: `{source['markdown']}`")
        stats = menu["stats"]
        meta.append(f"{stats['items']} items, {stats['itemsWithPrice']} priced")
        lines += ["*" + " · ".join(meta) + "*", ""]

        for section in menu["sections"]:
            if section["name"]:
                # Menu is ###, so a printed ## section becomes #### and a
                # printed #### sub-heading becomes ######.
                depth = min(6, 2 + (section["level"] or 2))
                lines.append(f"{'#' * depth} {section['name']}")
                lines.append("")
            if section.get("columns"):
                lines.append(f"*Columns: {' | '.join(section['columns'])}*")
                lines.append("")
            for note in section["notes"]:
                lines.append(f"*{note['text']}*")
            if section["notes"]:
                lines.append("")
            for item in section["items"]:
                tags = f" ({', '.join(item['dietary'])})" if item["dietary"] else ""
                crown = " ♛" if item["recommended"] else ""
                prices = ""
                if item["prices"]:
                    prices = " · " + " · ".join(price["raw"] for price in item["prices"])
                lines.append(f"- **{item['name']}**{tags}{crown}{prices}")
                if item["description"]:
                    lines.append(f"  - {item['description']}")
                for note in item["notes"]:
                    lines.append(f"  - {note}")
                product = item.get("product")
                if product:
                    lines.append(f"  - {product_line(product, products_by_id)}")
            lines.append("")

    lines += ["## Products (Kafoodie)", ""]
    lines.append("| Product | Group | Allergens | May contain | Energy | Photo |")
    lines.append("| --- | --- | --- | --- | ---: | --- |")
    for product in data["products"]:
        allergens = ", ".join(primary_allergens(product["allergens"])) or "—"
        may = ", ".join(primary_allergens(product["mayContain"])) or "—"
        energy = "—"
        if product["nutrition"]:
            value = product["nutrition"]["nutrients"].get("energy")
            if value and value["quantity"] is not None:
                energy = f"{value['quantity']:g} {value['unit']}"
        photo = "yes" if product["photo"] else "—"
        lines.append(
            f"| {product['name']} | {product['menuGroup']} | {allergens} | {may} | {energy} | {photo} |"
        )
    lines.append("")

    media = data["media"]
    lines += ["## Media", ""]
    lines.append(f"- Images discovered: **{len(media['images'])}**")
    lines.append(f"- Documents discovered: **{len(media['documents'])}**")
    for category, files in media.get("localAssets", {}).items():
        lines.append(f"- Local `{category}`: **{len(files)}** files")
    lines.append("")

    if venue.get("offers"):
        lines += ["## Offers", ""]
        lines += [f"- **{offer['name']}** — {offer['description']}" for offer in venue["offers"]]
        lines.append("")

    if venue.get("faqs"):
        lines += ["## FAQs", ""]
        for faq in venue["faqs"]:
            lines += [f"**{faq['question']}**", "", faq["answer"], ""]

    return "\n".join(lines).rstrip() + "\n"


def write_venue(name: str, data: dict) -> Path:
    venue_dir = EXPORTS / data["venue"]["region"] / name
    venue_dir.mkdir(parents=True, exist_ok=True)
    json_path = venue_dir / "venue.json"
    md_path = venue_dir / "venue.md"
    json_path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    md_path.write_text(render_markdown(data), encoding="utf-8")
    return venue_dir


# --------------------------------------------------------------------------
# CLI
# --------------------------------------------------------------------------
def check_venue(name: str) -> bool:
    data = build_venue(name)
    venue_dir = EXPORTS / data["venue"]["region"] / name
    json_path, md_path = venue_dir / "venue.json", venue_dir / "venue.md"
    stale = []
    if not json_path.is_file():
        stale.append(json_path.name)
    else:
        current = load_json(json_path)
        if {k: v for k, v in current.items() if k != "generated"} != {
            k: v for k, v in data.items() if k != "generated"
        }:
            stale.append(json_path.name)
    if not md_path.is_file() or md_path.read_text(encoding="utf-8") != render_markdown(data):
        stale.append(md_path.name)
    if stale:
        print(f"{name}: out of date: " + ", ".join(stale), file=sys.stderr)
        return False
    print(f"{name}: export is current.")
    return True


def export_venue(name: str, suggest: bool) -> None:
    data = build_venue(name)
    venue_dir = EXPORTS / data["venue"]["region"] / name
    write_venue(name, data)
    coverage = data["coverage"]
    print(f"Wrote {(venue_dir / 'venue.json').relative_to(ROOT)} and {(venue_dir / 'venue.md').relative_to(ROOT)}")
    print(
        f"  menus {coverage['menus']} · lines {coverage['menuLines']} · dishes {coverage['dishes']} "
        f"(priced {coverage['dishesWithPrice']}, matched {coverage['dishesMatchedToProduct']}) "
        f"· products {coverage['products']} "
        f"(allergens {coverage['productsWithAllergens']}, nutrition {coverage['productsWithNutrition']})"
    )
    if suggest:
        stub = {
            clean_name(entry["item"]).casefold(): entry["suggestions"][0]["product"]
            for entry in data["matchReport"]["unmatchedItems"]
            if entry["suggestions"]
        }
        print(f"\nCandidate aliases for {name} (review, then merge into config/aliases.json):")
        print(json.dumps(stub, ensure_ascii=False, indent=2))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    target = parser.add_mutually_exclusive_group(required=True)
    target.add_argument("--venue", help="venue name, id or unambiguous fragment")
    target.add_argument("--all", action="store_true", help="export every discovered venue")
    target.add_argument("--list", action="store_true", help="list discovered venues and exit")
    parser.add_argument("--check", action="store_true", help="fail if the export is out of date")
    parser.add_argument("--suggest-aliases", action="store_true", help="print candidate aliases for unmatched dishes")
    args = parser.parse_args()

    if args.list:
        for name, cfg in sorted(VENUES.items()):
            print(
                f"{name:<32} region={cfg['region']:<16} slug={cfg['slug'] or '-':<24} "
                f"menus={len(cfg['menu_files'])}"
            )
        return 0

    names = sorted(VENUES) if args.all else [resolve_venue(args.venue)]
    if args.check:
        results = [check_venue(name) for name in names]
        return 0 if all(results) else 1
    for name in names:
        export_venue(name, args.suggest_aliases)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())