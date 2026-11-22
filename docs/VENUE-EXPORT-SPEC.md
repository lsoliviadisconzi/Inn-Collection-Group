# Venue export format

One folder per venue, holding everything we know about it in one standard shape:

```
exports/<Region>/<Venue>/
  venue.json          canonical record — the source of truth
  venue.md            readable view, generated from venue.json
  PDF Menus/          downloaded menu PDFs (from the media exporter)
  Venues & property/  downloaded venue photography
  Other Documents/    anything else downloaded for the venue
```

`venue.md` is always derived from `venue.json`. Never edit it by hand — rerun
`build_venue_export.py` instead.

## Building

```bash
python3 build_venue_export.py --venue "The Kingslodge Inn"
python3 build_venue_export.py --venue "The Kingslodge Inn" --check   # CI / drift check
```

Venues are registered in `VENUES` at the top of `build_venue_export.py`: region,
website slug, Kafoodie folder and the menu Markdown files that belong to it.

## Where each field comes from

| Source | Path | Provides |
| --- | --- | --- |
| Printed menus | `inncollectiongroup.com_root/menus_md/*.md` | sections, dish names, prices, printed descriptions, dietary codes, chef's recommendations |
| Menu PDFs | `inncollectiongroup.com_root/documents/extracted-to-md/*.pdf` | page count and creation date, for traceability |
| Kafoodie outlet JSON | `inncollectiongroup.com_root/kafoodie/<folder>/*_all_menus.json` | products, allergens, may-contain, nutrition, dietary tags, dish photos |
| Website crawl | `inncollectiongroup.com_root/pages_text/*.txt` | address, phone, description, amenities, serving times, offers, FAQs, nearby inns |
| Media crawl | `inncollectiongroup.com_root/discovered_media.csv` | every image and document URL for the venue |

## `venue.json` shape

```jsonc
{
  "schemaVersion": "1.0.0",
  "generated": "2026-11-21T13:00:00+00:00",
  "venue": {
    "id": "the-kingslodge-inn",
    "name": "The Kingslodge Inn",
    "region": "County Durham",
    "outletId": 15900,                  // Kafoodie outlet — the reliable join key
    "kafoodieBaseUrl": "https://wba.kafoodle.com/15900/",
    "kafoodieSource": "inncollectiongroup.com_root/kafoodie/...",
    "website": "https://www.inncollectiongroup.com/kingslodge-inn/",
    "address": { "raw": "...", "street": "...", "locality": "...", "city": "...", "postcode": "..." },
    "phone": "0191 580 3610",
    "description": ["...", "..."],
    "amenities": ["Bar/Lounge", "..."],
    "servingTimes": [{ "name": "Breakfast", "hours": "7:30am - 11:00am" }],
    "diningFeatures": ["Real Ales", "..."],
    "offers": [{ "name": "Winter Breaks", "description": "..." }],
    "faqs": [{ "question": "...", "answer": "..." }],
    "nearbyInns": [{ "name": "...", "location": "..." }],
    "attractions": [{ "name": "...", "travel": "17 Minutes" }],
    "outletFlags": { "is_allergens_enabled": true, "is_nutritions_enabled": true }
  },
  "menus": [
    {
      "id": "heritage-menu-the-kingslodge-inn-digital-web",
      "name": "Heritage Menu — The Kingslodge Inn",
      "kind": "Food",                   // Food | Drinks | Sunday | Events | Breakfast | Other
      "source": { "markdown": "...", "pdf": "...", "pdfPath": "...", "pdfInfo": { "pages": 2 } },
      "stats": { "sections": 12, "items": 92, "itemsWithPrice": 84 },
      "sections": [
        {
          "name": "LIGHT BITES",
          "level": 2,                   // heading depth in the printed menu
          "page": 1,                    // PDF page
          "columns": ["Bottle", "250ml", "175ml"],   // price column labels, inherited by sub-headings
          "notes": [{ "text": "Served 11am - 5pm", "afterItem": null }],
          "items": [
            {
              "name": "Classic Prawn Sandwich",
              "kind": "dish",           // dish | drink | promo | heading | grouping
              "dietary": ["GFA"],       // codes as printed; see dietaryCodes
              "recommended": false,     // ♛ in the printed menu
              "prices": [{ "raw": "8.50", "amount": 8.5, "label": null }],
              "priceInName": false,     // e.g. "Coffee & Cake for £5"
              "description": "With Marie Rose sauce, ...",
              "notes": [],
              "page": 1,
              "product": {              // link to products[]; null when not a dish
                "id": 5323684,
                "name": "Prawn Marie Rose Sandwich",
                "matchScore": 1.0,
                "ambiguous": false,
                "via": "alias"          // exact | alias | tokens
              }
            }
          ]
        }
      ]
    }
  ],
  "products": [
    {
      "id": 2010587,
      "name": "Full Breakfast",
      "menuGroup": "Breakfast",
      "menuGroupId": 801,
      "menu": "SU26 Breakfast",
      "menuId": 186721,
      "description": null,
      "photo": "https://kitchen.kafoodle.com/...",
      "prices": [],                     // Kafoodie prices; empty for this group
      "dietaryTags": ["Low in sugar"],
      "allergens": [{ "id": "1", "name": "Gluten", "label": "Gluten", "abbr": "glu", "primaryId": null }],
      "mayContain": [{ "id": "may-2", "name": "Crustaceans", "primaryId": null }],
      "nutrition": {
        "basis": "per serving",
        "nutrients": {
          "energy": { "quantity": 1557.0, "unit": "kcal", "reference": 2000.0, "percentReference": 77.85, "level": null }
        }
      },
      "ingredients": null,
      "deliveryMethods": ["collection", "eat_in"],
      "isPublic": false,
      "allergenDataMissing": false
    }
  ],
  "allergens": [{ "id": "1", "name": "Gluten", "mayContain": false, "primaryId": null, "sortOrder": 1 }],
  "dietaryTags": [{ "id": 265, "name": "Low in sugar", "group": "Low in" }],
  "dietaryCodes": { "V": "Vegetarian", "VG": "Vegan", "GFA": "Gluten free option available" },
  "media": {
    "images": [{ "url": "...", "path": "/wp-content/uploads/...", "type": "image" }],
    "documents": [{ "url": "...", "path": "/wp-content/uploads/...pdf", "type": "document" }],
    "localAssets": { "PDF Menus": ["exports/.../PDF Menus/20261121-054647/x.pdf"] }
  },
  "coverage": { "menus": 3, "dishes": 130, "dishesMatchedToProduct": 130, "products": 165 },
  "gaps": ["..."],
  "matchReport": {
    "matched": 130, "matchedExact": 18, "matchedAlias": 104, "matchedTokens": 8,
    "unmatched": 0, "ambiguous": 0, "skipped": 82,
    "unmatchedItems": [], "ambiguousItems": [], "unmatchedDishes": []
  }
}
```

## Conventions

- **`kind` on a menu line.** Only `dish` lines are matched to products. `drink`,
  `promo`, `heading` and `grouping` lines are kept verbatim but never carry
  allergen data, because attaching it would be wrong.
- **Allergens.** `allergens` and `mayContain` keep Kafoodie's full list, including
  sub-allergens (`Gluten: Wheat`). Sub-allergens have a `primaryId`; collapse to
  entries with `primaryId: null` for a customer-facing list.
- **Nutrition.** `basis` is `per serving` when Kafoodie supplied
  `nutrition_per_serving`, otherwise `per 100g`. `level` is Kafoodie's
  low/medium/high banding for salt, fat, saturated fat and sugar.
- **Matching.** `via` records how a dish was linked: `exact` (same name),
  `alias` (a listed rename in `ITEM_ALIASES` / `KIDS_ALIASES`) or `tokens`
  (unambiguous word overlap). `ambiguous: true` means two products scored
  within 0.05 of each other and a human should confirm.
- **Prices.** `raw` is exactly as printed. `amount` is the parsed number, or
  `null` when the printed value is not a plain number. `label` comes from the
  section's `cols` directive.
- **`gaps`.** Plain-language list of what is missing for this venue. It is
  generated, so it stays honest as sources change.
