# Menu markdown format (reference: the three Kingslodge Inn files)

Goal: one clean, predictable shape so the review page can show prices/tags and highlight the exact spot in the PDF.

## Structure
- `# Title` — venue + menu name. One per file.
- `## SECTION` — printed section headings (LIGHT BITES, KIDS MENU…). Use `###`/`####` for sub-headings (Smooth & Fruity, Kids puddings). Order = reading order of the PDF, page by page.
- *Italic line* — notes, service times, taglines, legends. Never a list item.
- Items — **one line per item, no hard wraps**:

      - **Dish name** (V, GFA) ♛ · 12.50
        - Description exactly as printed.
        - Extra note line (e.g. Add bread and butter +1.00 each)

  - Name in bold. Dietary tags in brackets straight after it, as printed. `♛` = chef’s/bartender’s recommendation (crown icon in the PDF).
  - Price(s) after ` · `, exactly as printed (`4.95`, `10`, `£25`). Several prices: `20 · 7 · 5.5`, with a `cols` directive (below).
  - Description is a nested `  - ` line (2-space indent). No price inside the description.
  - Promos with no price (Coffee & Cake for £5) are items too; keep the price in the name.

## Page and column directives (HTML comments, invisible elsewhere)
- `<!-- page: 2 -->` — PDF page for everything below, until the next one. Makes matching faster and avoids duplicate-dish mix-ups.
- `<!-- cols: Bottle | 250ml | 175ml -->` — labels for multi-price items; goes straight after the heading it applies to and resets at the next heading.
- `<!-- source: file.pdf -->` — optional, for traceability.

## Rules
1. Faithful to the PDF: keep wording, spelling and prices as printed, even typos (report them in review notes, don’t silently fix).
2. Nothing belongs in a section it isn’t under in the PDF. Don’t split a price from its item.
3. No decorative text (Rooms sign, logos, illustrations). Taglines go in italics.
4. Escape literal asterisks: `\*`.
