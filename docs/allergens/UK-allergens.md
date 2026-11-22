# UK Statutory Allergens & Compliance Specification

> **Authority**: Retained Regulation (EU) No 1169/2011 (Food Information to Consumers / FIC), Food Information Regulations 2014 (FIR), and Food Information (Wales/Scotland/Northern Ireland) Regulations.  
> **Jurisdictions**: England (Food Standards Agency - FSA) and Scotland (Food Standards Scotland - FSS).  
> **System Master**: Kafoodie (Recipe, BOM & Allergen Master per Decision D7).  
> **Last Verified**: November 2026.

---

## 1. The 14 Statutory Allergens (FIC Annex II)

UK food law mandates the explicit identification and communication of **14 specific allergens** whenever used as an ingredient or processing aid that remains in the finished product.

| # | Allergen | Scope & Definition | Common Sources & Culinary Context | Statutory Sub-Types Required | Kafoodie ID / Abbr |
|:---:|:---|:---|:---|:---|:---:|
| **1** | **Celery** | Stalks, leaves, seeds, celeriac root | Stocks, soups, celery salt, spice mixes, bouillons, salads | — | `2048` (`cel`) |
| **2** | **Cereals containing gluten** | Wheat, rye, barley, oats, spelt, Khorasan (Kamut) | Batter, breading, roux, pastry, pasta, sauces, soy sauce, beer | **Specific cereal must be named** (Wheat, Rye, Barley, Oats, Spelt, Kamut) | `1` (`glu`) |
| **3** | **Crustaceans** | Crabs, lobsters, prawns, scampi, crayfish, langoustines | Shellfish stock, bisque, shrimp paste, curry pastes | — | `2` (`shl`) |
| **4** | **Eggs** | Bird eggs of all species (hen, duck, quail) | Mayonnaise, pasta, pastry glazes, meringues, dressings | — | `4` (`egg`) |
| **5** | **Fish** | All finned fish species, fish roe, fish oil | Fish sauce, Worcestershire sauce, Caesar dressing, stocks | — | `8` (`fsh`) |
| **6** | **Lupin** | Lupin seeds, lupin flour, lupin meal | Specialty flours, artisan breads, pastry, pizzas | — | `8192` (`lup`) |
| **7** | **Milk** | Mammalian milk (cow, goat, sheep), lactose | Butter, cream, cheese, milk powder, ghee, whey, glazes | — | `64` (`mlk`) |
| **8** | **Molluscs** | Snails, bivalves (mussels, oysters, clams), cephalopods (squid, octopus) | Paella, oyster sauce, fish stews, tempura squid | — | `1024` (`mol`) |
| **9** | **Mustard** | Liquid mustard, mustard powder, seeds, sprouted leaves | Dressings, marinades, curries, rubs, sausages | — | `4096` (`mus`) |
| **10** | **Peanuts** | Groundnuts (legumes grown underground) | Satay, peanut butter, arachis oil, snacks, Asian cuisine | Declare as **Peanut** (never just "groundnut") | `16` (`pnt`) |
| **11** | **Sesame seeds** | Whole seeds, sesame paste (tahini), oil | Burger buns, hummus, gomashio, crackers, dressings | — | `256` (`ses`) |
| **12** | **Soybeans (Soya)** | Soya beans, edamame, tofu, miso, tempeh, texturised protein | Soy sauce, vegetarian meat substitutes, margarines, lecithin (E322) | Declare with clear **Soya** identifier | `32` (`soy`) |
| **13** | **Sulphur dioxide / Sulphites** | Preservatives exceeding $10\text{ mg/kg}$ or $10\text{ mg/L}$ expressed as $\text{SO}_2$ | Wine, beer, cider, dried fruits, sausages, soft drinks | Exemption below $10\text{ mg/kg}$ or $10\text{ mg/L}$ | `512` (`so2`) |
| **14** | **Tree nuts** | 8 statutory species only: Almond, Hazelnut, Walnut, Cashew, Pecan, Brazil, Pistachio, Macadamia (Queensland) | Pesto, marzipan, satay substitutes, desserts, nut oils | **Specific nut must be named** (Chestnuts, pine nuts, coconuts are not tree nuts) | `128` (`tnt`) |

---

## 2. Technical Data Representation (Kafoodie & `venue.json`)

Kafoodie structures allergen declarations using a **bitmask architecture** combined with relational sub-type expansion.

### A. Bitmask Structure
In Kafoodie outlet data:
- Primary allergens utilize bit flags: $1, 2, 4, 8, 16, 32, 64, 128, 256, 512, 1024, 2048, 4096, 8192$.
- Sub-types roll up under their parent category via `primary_id`:
  - **Gluten (`1`)**: Wheat (`65536`), Rye (`131072`), Barley (`262144`), Oats (`524288`), Spelt, Kamut.
  - **Tree Nuts (`128`)**: Almond, Hazelnut, Walnut, Cashew, Pecan, Brazil nut, Pistachio, Macadamia.
- Precautionary Allergen Labelling (PAL / "May Contain") uses duplicate keys prefixed with `may-` (e.g., `may-1` for Gluten, `may-128` for Tree Nuts).

### B. Product Schema Attributes in `venue.json`
Every product exported by `build_venue_export.py` contains:
```json
{
  "id": "14920",
  "name": "Fish & Chips",
  "allergens": [
    {"id": "1", "name": "Gluten", "label": "Gluten", "abbr": "glu"},
    {"id": "65536", "name": "Wheat", "label": "Wheat", "abbr": "glu", "primaryId": "1"},
    {"id": "8", "name": "Fish", "label": "Fish", "abbr": "fsh"}
  ],
  "mayContain": [],
  "dietaryTags": ["V", "GF"],
  "allergenDataMissing": false
}
```

---

## 3. Statutory Presentation Rules by Food Service Type

### A. Non-Prepacked (Restaurant, Pub & Loose Service)
- **Requirement**: Accurate allergen information for every dish served must be available to customers **before purchase**.
- **Delivery**: Written format (printed menu, allergen matrix, digital tablet) or verbal.
- **Signposting Rule**: If information is provided verbally, a conspicuous notice (FSA "Food Allergy or Intolerance?" sign) must be prominently displayed instructing guests to speak with staff.
- **Whole Dish Principle**: Allergens must be assessed for the complete dish as presented (including dressings, sauces, batters, and garnishes).

### B. Prepacked for Direct Sale (PPDS — Natasha's Law)
- **Scope**: Food packaged on-site before a customer selects or orders it (e.g., grab-and-go packaged sandwiches, boxed salads, pre-wrapped bakery items).
- **Mandatory Label**:
  1. Name of the food.
  2. Full ingredient list in descending order of weight.
  3. All 14 allergens **emphasised** each time they appear (e.g. bold, underline, contrasting colour).
  4. Minimum font size ($x\text{-height} \ge 1.2\text{ mm}$).

### C. Distance Selling (Takeaway, Online, Phone Delivery)
- **Two-stage requirement**:
  1. **Before purchase**: Allergen information must be made available without extra charge (e.g. on the online ordering site or stated over the phone).
  2. **At delivery**: Written allergen information must accompany the delivered order (e.g. meal container stickers, delivery slip, or printed menu).

---

## 4. Gluten & Precautionary Labelling Standards

### A. Gluten Thresholds
Statutory definitions under retained Regulation (EU) No 828/2014:
- **“Gluten-free”**: Strict threshold of $\le 20\text{ mg/kg}$ ($\le 20\text{ ppm}$) gluten in the food as sold.
- **“Very low gluten”**: Specifically processed ingredients containing $> 20\text{ mg/kg}$ but $\le 100\text{ mg/kg}$.
- **Banned Claims**: Terms such as "low gluten", "gluten-reduced", or "gluten-friendly" are legally prohibited.
- **NGCI (“Non-Gluten Containing Ingredients”)**: FSA/FSS best practice strongly discourages NGCI for loose food. If used, it **must** include an explicit warning that it is not prepared in a gluten-free environment and is not suitable for coeliac disease sufferers.

### B. Precautionary Allergen Labelling (PAL / "May Contain")
- Voluntary statement; must **only** be applied after a documented HACCP cross-contamination risk assessment demonstrates a genuine, uncontrollable cross-contact risk.
- Must name the specific allergen (e.g. `"May contain peanuts"`, never generic `"May contain nuts"`).
- Prohibited from being combined with an absolute "Free From" claim for that same allergen.

---

## 5. England (FSA) vs Scotland (FSS) Differences

| Operational Aspect | England (FSA / FIR 2014) | Scotland (FSS / Food (Scotland) Act 2015) |
|:---|:---|:---|
| **Primary Regulatory Body** | Food Standards Agency (FSA) | Food Standards Scotland (FSS) |
| **Breach Reporting Duty** | Voluntary / local authority liaison | **Mandatory statutory duty** to report food information breaches to FSS |
| **Enforcement Powers** | Improvement notices, unlimited fines upon criminal conviction | Detention & seizure powers for suspected mislabelled food; Sheriff orders |
| **Digital Tooling** | FSA Allergen Checklist & Matrix | **MenuCal** (recipe calculation, PPDS label generator, supplier sheets) |
| **Food Hygiene Scheme** | Food Hygiene Rating Scheme (0 to 5) | Food Hygiene Information Scheme (Pass / Improvement Required) |
| **HACCP Framework** | Standard HACCP / Safer Food Better Business | **CookSafe** Allergen Management system |

---

## 6. Integration with ICG Architecture & Review Tooling

1. **System Boundary (Decision D7)**:
   - Kafoodie is the authoritative master.
   - The Inn Collection Group backend **never overrides** Kafoodie recipe declarations locally.
2. **Compliance & Gap Detection (`GET /api/allergens/gaps`)**:
   - The platform continuously audits `venue.json` against statutory compliance criteria:
     - `is_pw_allergen_not_set = true`: Triggers `allergenDataMissing` flag and action requirement.
     - Unmatched printed menu items: Flagged as compliance warnings (unmatched items lack Kafoodie allergen backing).
     - Drinks menus: Identified as lacking Kafoodie outlet linkage, requiring cellar and brand-level supplier review.
