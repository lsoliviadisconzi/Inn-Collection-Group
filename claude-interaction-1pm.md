
07_ARCHITECTURE_VERIFICATION_AND_NETLIFY_REMOVAL.md
07_ARCHITECTURE_VERIFICATION_AND_NETLIF
Y_REMOVAL
.md
MD
08_TECHNICAL_BASELINE_CLOSURE_AND_EVIDENCE_AUDIT.md
08_TECHNICAL_BASELINE_CLOSURE_AND_EVIDE
NCE_AUDIT
.md
MD
09_OPERATIONAL_REQUIREMENTS_AND_CAPABILITY_MAPPING.md
09_OPERATIONAL_REQUIREMENTS_AND_CAPABILIT
Y_MAPPING
.md
MD
10_TARGET_DATA_ARCHITECTURE_AND_ENTITY_MODEL.md
10_TARGET_DATA_ARCHITECTURE_AND_ENTITY_MODEL.md
MD
11_TARGET_APPLICATION_AND_INTEGRATION_ARCHITECTURE.md
11_TARGET_APPLICATION_AND_INTEGRATION_ARC
HITECTURE
.md
MD
12_END_TO_END_OPERATIONAL_WORKFLOW_DESIGN.md
12_END_TO_END_OPERATIONAL_WORKFLOW_DESIGN.md
MD
menu_review_server.py
menu_review_server.py
PY
menu_review_state.sqlite3
menu_review_state.sqlite3
SQLITE3
root.tree.md
root.tree.md
MD
01_SYSTEM_ARCHITECTURE_OVERVIEW.md
01_SYSTEM_ARCHITECTURE_OVERVIEW.md
158 lines
MD
02_DATA_MODEL_AND_ENTITY_RELATIONSHIPS.md
02_DATA_MODEL_AND_ENTITY_RELA
TIONSHIPS
.md
177 lines
MD
03_COMPONENT_AND_CAPABILITY_REGISTER.md
03_COMPONENT_AND_CAPABILITY
_REGISTER
.md
137 lines
MD
04_OPERATIONAL_WORKFLOW_MAP.md
04_OPERATIONAL_WORKFLOW_MAP.md
145 lines
MD
05_INTEGRATION_AND_DEPENDENCY_REGISTER.md
05_INTEGRATION_AND_DEPENDENCY
_REGISTER
.md
125 lines
MD
06_CAPABILITY_GAPS_AND_DEVELOPMENT_PRIORITIES.md
06_CAPABILITY_GAPS_AND_DEVELOPMENT_P
RIORITIES
.md
130 lines
MD
13_CURRENT_TO_TARGET_ARCHITECTURE_TRANSITION_MAP.md
13_CURRENT_TO_TARGET_ARCHITECTURE_TRANS
ITION_MAP
.md
101 lines
MD
14_IMPLEMENTATION_ROADMAP_AND_PRIORITISATION.md
14_IMPLEMENTATION_ROADMAP_AND_PRIOR
ITISATION
.md
127 lines
MD
15_ARCHITECTURE_BLUEPRINT_EXECUTIVE_SUMMARY.md
15_ARCHITECTURE_BLUEPRINT_EXECUTIV
E_SUMMARY
.md
139 lines
MD
Right, so, I will share with you, um, the root three directory, so you can understand the full project directory, and I will also, um, provide to you, um, Documentation, revision that we have been making, on our project, um, and I would like you to review it, and then, do not change anything yet, but help to properly, professionally, efficiently, cohesively, define the next steps, ancient, reorganising or organising the architecture, documenting the proper architecture, without fluffing, without, you know, like ChatGPT does, that goes round and round, and pay attention to, you know, will this, uh, will this service needed to be used in more than one computer?

Jesus, that's not a problem.

And you know what I mean?

So, please review it.

And then propose the architecture, that we can then start working on it afterwards.

But please review everything, correct anything if there is a need.

And what I would expect from the outcome, it is a clear documentation of the architecture and what's next.

Okay?

Thank you.

God bless you.  ***observation, there are still important files to provide you

Ran 4 commands, read memory
Reviewing the uploaded documentation before proposing an architecture.

Checking which files are actually present.

- working on menu-review.html (Inn Collection Group menu review UI, served locally by menu_review_server.py at 127.0.0.1:8000, sibling page discovered-media.html)
bash

cd /mnt/user-data/uploads; ls -la; wc -l root_tree.md menu_review_server.py 0*.md 1*.md; echo ----; cat root_tree.md | head -250
Output

total 368
drwxr-xr-x 1 claude ubuntu     0 Nov 22 15:57 .
drwxr-xr-x 5 root   root    4096 Nov 22 15:57 ..
-rw-r--r-- 1 claude ubuntu 11316 Nov 22 15:57 01_SYSTEM_ARCHITECTURE_OVERVIEW.md
-rw-r--r-- 1 claude ubuntu 11615 Nov 22 15:56 02_DATA_MODEL_AND_ENTITY_RELATIONSHIPS.md
-rw-r--r-- 1 claude ubuntu 10388 Nov 22 15:56 03_COMPONENT_AND_CAPABILITY_REGISTER.md
-rw-r--r-- 1 claude ubuntu  8420 Nov 22 15:56 04_OPERATIONAL_WORKFLOW_MAP.md
-rw-r--r-- 1 claude ubuntu  8367 Nov 22 15:56 05_INTEGRATION_AND_DEPENDENCY_REGISTER.md
-rw-r--r-- 1 claude ubuntu  9404 Nov 22 15:56 06_CAPABILITY_GAPS_AND_DEVELOPMENT_PRIORITIES.md
-rw-r--r-- 1 claude ubuntu 15723 Nov 22 15:56 07_ARCHITECTURE_VERIFICATION_AND_NETLIFY_REMOVAL.md
-rw-r--r-- 1 claude ubuntu 27251 Nov 22 15:56 08_TECHNICAL_BASELINE_CLOSURE_AND_EVIDENCE_AUDIT.md
-rw-r--r-- 1 claude ubuntu 28253 Nov 22 15:56 09_OPERATIONAL_REQUIREMENTS_AND_CAPABILITY_MAPPING.md
-rw-r--r-- 1 claude ubuntu 24772 Nov 22 15:56 10_TARGET_DATA_ARCHITECTURE_AND_ENTITY_MODEL.md
-rw-r--r-- 1 claude ubuntu 18040 Nov 22 15:56 11_TARGET_APPLICATION_AND_INTEGRATION_ARCHITECTURE.md
-rw-r--r-- 1 claude ubuntu 17292 Nov 22 15:56 12_END_TO_END_OPERATIONAL_WORKFLOW_DESIGN.md
-rw-r--r-- 1 claude ubuntu 11982 Nov 22 15:56 13_CURRENT_TO_TARGET_ARCHITECTURE_TRANSITION_MAP.md
-rw-r--r-- 1 claude ubuntu 12208 Nov 22 15:56 14_IMPLEMENTATION_ROADMAP_AND_PRIORITISATION.md
-rw-r--r-- 1 claude ubuntu 11117 Nov 22 15:56 15_ARCHITECTURE_BLUEPRINT_EXECUTIVE_SUMMARY.md
-rw-r--r-- 1 claude ubuntu 25367 Nov 22 15:56 menu_review_server.py
-rw-r--r-- 1 claude ubuntu 12288 Nov 22 15:56 menu_review_state.sqlite3
-rw-r--r-- 1 claude ubuntu 74120 Nov 22 15:56 root_tree.md
  1110 root_tree.md
   614 menu_review_server.py
   158 01_SYSTEM_ARCHITECTURE_OVERVIEW.md
   177 02_DATA_MODEL_AND_ENTITY_RELATIONSHIPS.md
   137 03_COMPONENT_AND_CAPABILITY_REGISTER.md
   145 04_OPERATIONAL_WORKFLOW_MAP.md
   125 05_INTEGRATION_AND_DEPENDENCY_REGISTER.md
   130 06_CAPABILITY_GAPS_AND_DEVELOPMENT_PRIORITIES.md
   212 07_ARCHITECTURE_VERIFICATION_AND_NETLIFY_REMOVAL.md
   196 08_TECHNICAL_BASELINE_CLOSURE_AND_EVIDENCE_AUDIT.md
   168 09_OPERATIONAL_REQUIREMENTS_AND_CAPABILITY_MAPPING.md
   304 10_TARGET_DATA_ARCHITECTURE_AND_ENTITY_MODEL.md
   191 11_TARGET_APPLICATION_AND_INTEGRATION_ARCHITECTURE.md
   289 12_END_TO_END_OPERATIONAL_WORKFLOW_DESIGN.md
   101 13_CURRENT_TO_TARGET_ARCHITECTURE_TRANSITION_MAP.md
   127 14_IMPLEMENTATION_ROADMAP_AND_PRIORITISATION.md
   139 15_ARCHITECTURE_BLUEPRINT_EXECUTIVE_SUMMARY.md
  4323 total
----
.
├── PROJECT-REVIEW
│   ├── 01 - Agent_Mandate_Architecture_Discovery_Workflow_Mapping_&_Product_Consolidation.md
│   ├── 02 - Agent Instructions: Next Documentation Phase.md
│   ├── 03.1 - Architecture Verification Evidence Reconciliation and Netlify Removal.md
│   ├── 03.md
│   ├── 04.1 - Document 08 — Technical Baseline Closure and Evidence Audit.md
│   ├── 04.md
│   ├── 05.1 - PHASE 2 — HOSPITALITY TECHNOLOGY REQUIREMENTS, TARGET ARCHITECTURE & IMPLEMENTATION BLUEPRINT.md
│   ├── 05.md
│   └── reviews
│       ├── Hospitality Technology Capability Assessment Chicken Liver Parfait Product Page.md
│       ├── Hospitality Technology Capability Assessment Discovered Media.md
│       ├── Hospitality Technology Capability Assessment F&B Role Cross-check.md
│       ├── Hospitality Technology Capability Assessment Launch Readiness.md
│       ├── Hospitality Technology Capability Assessment Menu Explorer.md
│       ├── Hospitality Technology Capability Assessment Menu Review.md
│       ├── Hospitality Technology Capability Assessment Product Data.md
│       └── Hospitality Technology Capability Assessment.md
├── __pycache__
│   ├── build_menu_explorer.cpython-315.pyc
│   ├── build_venue_export.cpython-315.pyc
│   └── menu_review_server.cpython-315.pyc
├── _dev
│   ├── Chicken Liver Parfait Carousel-png
│   │   ├── Chicken Liver Parfait.png
│   │   ├── Cost drift, stock and demand.png
│   │   ├── Detail is what makes it pass on.png
│   │   ├── From a 10 kg case to 45 grams.png
│   │   ├── How it lands on the table.png
│   │   ├── Make it the same, every time.png
│   │   ├── What goes on one plate.png
│   │   ├── What’s in it, and what can come off.png
│   │   ├── Where the drops go.png
│   │   ├── Who delivers, and when.png
│   │   └── £8.95 on the menu, £5.36 in the bank.png
│   ├── Chicken Liver Parfait Carousel.html
│   ├── Chicken Liver Parfait · The Lindisfarne Inn-v2.html
│   ├── Chicken Liver Parfait · The Lindisfarne Inn.html
│   └── Chicken Liver Parfait_ Reel Storyboard.html
├── build_menu_explorer.py
├── build_venue_export.py
├── config
│   ├── aliases.json
│   ├── rules.json
│   └── venues.json
├── docs
│   ├── MENU-MD-SPEC.md
│   ├── VENUE-EXPORT-SPEC.md
│   ├── architecture
│   │   ├── 01_PROJECT_OVERVIEW.md
│   │   ├── 02_EXISTING_SYSTEM_INVENTORY.md
│   │   ├── 03_INFORMATION_ARCHITECTURE.md
│   │   ├── 04_WORKFLOW_MAP.md
│   │   ├── 05_COMPONENT_RELATIONSHIPS.md
│   │   ├── 06_WORKSPACE_PROPOSAL.md
│   │   ├── 07_ARCHITECTURAL_GAPS.md
│   │   ├── 08_AI_AUTOMATION_OPPORTUNITIES.md
│   │   ├── 09_IMPLEMENTATION_STATUS.md
│   │   └── 10_NEXT_STAGE_RECOMMENDATIONS.md
│   └── capability-assessment
│       ├── 01_SYSTEM_ARCHITECTURE_OVERVIEW.md
│       ├── 02_DATA_MODEL_AND_ENTITY_RELATIONSHIPS.md
│       ├── 03_COMPONENT_AND_CAPABILITY_REGISTER.md
│       ├── 04_OPERATIONAL_WORKFLOW_MAP.md
│       ├── 05_INTEGRATION_AND_DEPENDENCY_REGISTER.md
│       ├── 06_CAPABILITY_GAPS_AND_DEVELOPMENT_PRIORITIES.md
│       ├── 07_ARCHITECTURE_VERIFICATION_AND_NETLIFY_REMOVAL.md
│       ├── 08_TECHNICAL_BASELINE_CLOSURE_AND_EVIDENCE_AUDIT.md
│       └── phase-2
│           ├── 09_OPERATIONAL_REQUIREMENTS_AND_CAPABILITY_MAPPING.md
│           ├── 10_TARGET_DATA_ARCHITECTURE_AND_ENTITY_MODEL.md
│           ├── 11_TARGET_APPLICATION_AND_INTEGRATION_ARCHITECTURE.md
│           ├── 12_END_TO_END_OPERATIONAL_WORKFLOW_DESIGN.md
│           ├── 13_CURRENT_TO_TARGET_ARCHITECTURE_TRANSITION_MAP.md
│           ├── 14_IMPLEMENTATION_ROADMAP_AND_PRIORITISATION.md
│           └── 15_ARCHITECTURE_BLUEPRINT_EXECUTIVE_SUMMARY.md
├── exports
│   ├── Lake District
│   │   └── The Ullswater Inn
│   │       ├── MD Menus
│   │       │   └── 20261121-142137
│   │       │       ├── Crown-Menu-The-Ullswater-Inn-DIGITAL-WEB.md
│   │       │       ├── Sunday-Menu-The-Ullswater-Inn-DIGITAL.md
│   │       │       └── The-Ullswater-Inn-Drinks-Autumnx3aWinter-2026-DIGITAL.md
│   │       ├── Other
│   │       │   └── 20261121-142137
│   │       │       ├── Bluebird-K7-at-Ullswater-in-1955-credit-Leo-Villa.jpg
│   │       │       ├── Bluebird-K7-at-Ullswater-in-1955-credit-Leo-Villa.webp
│   │       │       ├── ULLSWATER_STEAMERS_2021_049-720x720.jpg
│   │       │       ├── ULLSWATER_STEAMERS_2021_049-720x720.jpg.webp
│   │       │       ├── ULLSWATER_STEAMERS_2021_049-scaled.jpg
│   │       │       ├── ULLSWATER_STEAMERS_2021_049-scaled.webp
│   │       │       └── couple-ullswater-scaled-1.jpg
│   │       ├── PDF Menus
│   │       │   └── 20261121-142137
│   │       │       ├── Crown-Menu-The-Ullswater-Inn-DIGITAL-WEB.pdf
│   │       │       ├── Sunday-Menu-The-Ullswater-Inn-DIGITAL.pdf
│   │       │       └── The-Ullswater-Inn-Drinks-Autumnx3aWinter-2026-DIGITAL.pdf
│   │       ├── The_Ullswater_Inn_all_menus.json
│   │       ├── Venues & property
│   │       │   └── 20261121-142137
│   │       │       ├── The-Ullswater-Inn-Logo-1-720x720.jpg
│   │       │       ├── The-Ullswater-Inn-Logo-1-scaled.jpg
│   │       │       ├── The-Ullswater-Inn-Logo-1-scaled.webp
│   │       │       ├── The-Ullswater-Inn-Logo-Reverse-2.png
│   │       │       ├── The-Ullswater-Inn-Logo-Reverse-2.webp
│   │       │       ├── The-Ullswater-Inn-Logo-Reverse.png
│   │       │       ├── The-Ullswater-Inn-Logo-Reverse.webp
│   │       │       ├── The-Ullswater-Inn-exterior-412x275.jpg.webp
│   │       │       ├── The-Ullswater-Inn-exterior.jpg
│   │       │       ├── The-Ullswater-Inn-exterior.webp
│   │       │       ├── Ullswater-Inn-Bedroom-scaled.jpg
│   │       │       ├── Ullswater-Inn-Bedroom-scaled.jpg.webp
│   │       │       ├── Ullswater-Inn-Bedroom-scaled.webp
│   │       │       ├── Ullswater-Inn-Exterior.jpg
│   │       │       └── Ullswater-Inn-Exterior.webp
│   │       ├── venue.json
│   │       └── venue.md
│   ├── Lancashire
│   │   ├── Offshore
│   │   │   ├── venue.json
│   │   │   └── venue.md
│   │   └── The Midland
│   │       ├── venue.json
│   │       └── venue.md
│   └── TestRegion
│       └── TestVenue
│           └── Property
│               └── 20261122-143635
├── inncollectiongroup.com_root
│   ├── crawl_state.json
│   ├── discovered_media.csv
│   ├── discovered_video_embeds.csv
│   ├── documents
│   │   ├── Offshore-Food-Spring-2024-Web.pdf
│   │   ├── The-Commissioners-Quay-Inn-Drinks-Summer-2024-Web.pdf
│   │   ├── The-Coniston-Inn-Food-Spring-2025-WEB.pdf
│   │   └── extracted-to-md
│   │       ├── 2026-Christmas-Day-Lunch.pdf
│   │       ├── Crown-Menu-Offshore-DIGITAL-WEB.pdf
│   │       ├── Crown-Menu-The-Ambleside-Inn-DIGITAL-WEB.pdf
│   │       ├── Crown-Menu-The-Angel-Inn-DIGITAL-WEB.pdf
│   │       ├── Crown-Menu-The-Bamburgh-Castle-Inn-DIGITAL-WEB.pdf
│   │       ├── Crown-Menu-The-Bulls-Head-Inn-DIGITAL-WEB.pdf
│   │       ├── Crown-Menu-The-Coniston-Inn-DIGITAL-WEB.pdf
│   │       ├── Crown-Menu-The-Hogs-Head-Inn-DIGITAL-WEB.pdf
│   │       ├── Crown-Menu-The-Knaresborough-Inn-DIGITAL-WEB.pdf
│   │       ├── Crown-Menu-The-Pheasant-Inn-DIGITAL-WEB.pdf
│   │       ├── Crown-Menu-The-Ripon-Inn-DIGITAL-WEB.pdf
│   │       ├── Crown-Menu-The-Stables-DIGITAL-WEB.pdf
│   │       ├── Crown-Menu-The-Swallow-Falls-Inn-DIGITAL-WEB.pdf
│   │       ├── Crown-Menu-The-Swan-DIGITAL-WEB.pdf
│   │       ├── Crown-Menu-The-Tynemouth-Castle-Inn-DIGITAL-WEB.pdf
│   │       ├── Crown-Menu-The-Ullswater-Inn-DIGITAL-WEB.pdf
│   │       ├── Crown-Menu-The-Wateredge-Inn-DIGITAL-WEB.pdf
│   │       ├── Dean-Court-Drinks-Summer-2026-Web.pdf
│   │       ├── E-Bike-and-Scooter-Policy.pdf
│   │       ├── Heritage-Menu-The-Amble-Inn-DIGITAL-WEB.pdf
│   │       ├── Heritage-Menu-The-Commissioners-Quay-Inn-DIGITAL-WEB.pdf
│   │       ├── Heritage-Menu-The-Kings-Head-Inn-DIGITAL-WEB.pdf
│   │       ├── Heritage-Menu-The-Kingslodge-Inn-DIGITAL-WEB.pdf
│   │       ├── Heritage-Menu-The-Lindisfarne-Inn-DIGITAL-WEB.pdf
│   │       ├── Heritage-Menu-The-Northallerton-Inn-DIGITAL-WEB.pdf
│   │       ├── Heritage-Menu-The-Seaburn-Inn-DIGITAL-WEB.pdf
│   │       ├── Heritage-Menu-The-Seaton-Lane-Inn-DIGITAL-WEB.pdf
│   │       ├── Midland-Drinks-Summer-2026-Web.pdf
│   │       ├── Offshore-Drinks-Autumnx3aWinter-2026-DIGITAL.pdf
│   │       ├── Oswins.pdf
│   │       ├── Party-Night-Menu-2026.pdf
│   │       ├── Signature-All-Day-Menu-Black-Swan-DIGITAL-WEB.pdf
│   │       ├── Signature-All-Day-Menu-Dean-Court-DIGITAL-WEB.pdf
│   │       ├── Signature-All-Day-Menu-The-Harrogate-Inn-DIGITAL-WEB.pdf
│   │       ├── Signature-All-Day-Menu-The-Midland-Hotel-DIGITAL-WEB.pdf
│   │       ├── Signature-All-Day-Menu-The-Waterhead-Hotel-DIGITAL-WEB.pdf
│   │       ├── Signature-All-Day-Menu-The-Wordsworth-DIGITAL-WEB.pdf
│   │       ├── Signature-Dining-Menu-Black-Swan-DIGITAL.pdf
│   │       ├── Signature-Dining-Menu-Dean-Court-DIGITAL.pdf
│   │       ├── Signature-Dining-Menu-The-Harrogate-Inn-DIGITAL.pdf
│   │       ├── Signature-Dining-Menu-The-Midland-Hotel-DIGITAL.pdf
│   │       ├── Signature-Dining-Menu-The-Waterhead-Hotel-DIGITAL.pdf
│   │       ├── Signature-Dining-Menu-The-Wordsworth-DIGITAL.pdf
│   │       ├── Sunday-Menu-Black-Swan-DIGITAL.pdf
│   │       ├── Sunday-Menu-Dean-Court-WEB.pdf
│   │       ├── Sunday-Menu-Offshore-WEB.pdf
│   │       ├── Sunday-Menu-The-Amble-Inn-DIGITAL.pdf
│   │       ├── Sunday-Menu-The-Ambleside-WEB.pdf
│   │       ├── Sunday-Menu-The-Angel-Inn-DIGITAL.pdf
│   │       ├── Sunday-Menu-The-Bamburgh-Castle-Inn.pdf
│   │       ├── Sunday-Menu-The-Bulls-Head-Inn-DIGITAL.pdf
│   │       ├── Sunday-Menu-The-Commissioners-Quay-Inn-DIGITAL.pdf
│   │       ├── Sunday-Menu-The-Coniston-Inn-DIGITAL.pdf
│   │       ├── Sunday-Menu-The-Harrogate-Inn-DIGITAL.pdf
│   │       ├── Sunday-Menu-The-Hogs-Head-Inn-DIGITAL.pdf
│   │       ├── Sunday-Menu-The-Kings-Head-Inn-DIGITAL.pdf
│   │       ├── Sunday-Menu-The-Kingslodge-Inn-DIGITAL.pdf
│   │       ├── Sunday-Menu-The-Knaresborough-Inn-DIGITAL.pdf
│   │       ├── Sunday-Menu-The-Lindisfarne-Inn-DIGITAL.pdf
│   │       ├── Sunday-Menu-The-Midland-DIGITAL.pdf
│   │       ├── Sunday-Menu-The-Northallerton-Inn-DIGITAL.pdf
│   │       ├── Sunday-Menu-The-Pheasant-Inn-DIGITAL.pdf
│   │       ├── Sunday-Menu-The-Ripon-Inn-DIGITAL.pdf
│   │       ├── Sunday-Menu-The-Seaburn-Inn-DIGITAL.pdf
│   │       ├── Sunday-Menu-The-Seaton-Lane-Inn-DIGITAL.pdf
│   │       ├── Sunday-Menu-The-Stables-DIGITAL.pdf
│   │       ├── Sunday-Menu-The-Swallow-Falls-Inn-DIGITAL.pdf
│   │       ├── Sunday-Menu-The-Swan-DIGITAL.pdf
│   │       ├── Sunday-Menu-The-Tynemouth-Castle-Inn-DIGITAL.pdf
│   │       ├── Sunday-Menu-The-Ullswater-Inn-DIGITAL.pdf
│   │       ├── Sunday-Menu-The-Wateredge-WEB.pdf
│   │       ├── Sunday-Menu-The-Waterhead-Hotel-DIGITAL.pdf
│   │       ├── Sunday-Menu-The-Wordsworth-NEW-DIGITAL.pdf
│   │       ├── TTI-The-Temperance-Inn-Autumn-2026-WEB.pdf
│   │       ├── TTI-The-Temperance-Inn-Drinks-Spring-2026-WEB.pdf
│   │       ├── The-Amble-Inn-Drinks-Autumnx3aWinter-2026-DIGITAL.pdf
│   │       ├── The-Ambleside-Inn-Drinks-Autumnx3aWinter-2026-DIGITAL.pdf
│   │       ├── The-Angel-Inn-Drinks-Autumnx3aWinter-2026-DIGITAL.pdf
│   │       ├── The-Bamburgh-Castle-Inn-Drinks-Autumnx3aWinter-2026-DIGITAL.pdf
│   │       ├── The-Black-Swan-Drinks-Summer-2026-Web.pdf
│   │       ├── The-Bulls-Head-Inn-Drinks-Autumnx3aWinter-2026-DIGITAL.pdf
│   │       ├── The-Commissioners-Quay-Inn-Drinks-Autumnx3aWinter-2026-DIGITAL.pdf
│   │       ├── The-Coniston-Inn-Drinks-Autumnx3aWinter-2026-DIGITAL.pdf
│   │       ├── The-Harrogate-Inn-Drinks-Summer-2026-Web.pdf
│   │       ├── The-Hogs-Head-Inn-Drinks-Autumnx3aWinter-2026-DIGITAL.pdf
│   │       ├── The-Kings-Head-Inn-Drinks-Autumnx3aWinter-2026-DIGITAL.pdf
│   │       ├── The-Kingslodge-Inn-Drinks-Autumnx3aWinter-2026-DIGITAL.pdf
│   │       ├── The-Knaresborough-Inn-Drinks-Autumnx3aWinter-2026-DIGITAL.pdf
│   │       ├── The-Lindisfarne-Inn-Drinks-Autumnx3aWinter-2026-DIGITAL.pdf
│   │       ├── The-Northallerton-Inn-Drinks-Autumnx3aWinter-2026-DIGITAL.pdf
│   │       ├── The-Pheasant-Inn-Drinks-Autumnx3aWinter-2026-DIGITAL.pdf
│   │       ├── The-Ripon-Inn-Drinks-Autumnx3aWinter-2026-DIGITAL.pdf
│   │       ├── The-Seaburn-Inn-Drinks-Autumnx3aWinter-2026-DIGITAL.pdf
│   │       ├── The-Seaton-Lane-Inn-Drinks-Autumnx3aWinter-2026-DIGITAL.pdf
│   │       ├── The-Stables-Drinks-Autumnx3aWinter-2026-DIGITAL.pdf
│   │       ├── The-Swallow-Falls-Inn-Drinks-Autumnx3aWinter-2026-DIGITAL.pdf
│   │       ├── The-Swan-Drinks-Autumnx3aWinter-2026-DIGITAL.pdf
│   │       ├── The-Tynemouth-Castle-Inn-Drinks-Autumnx3aWinter-2026-DIGITAL.pdf
│   │       ├── The-Ullswater-Inn-Drinks-Autumnx3aWinter-2026-DIGITAL.pdf
│   │       ├── The-Wateredge-Inn-Drinks-Autumnx3aWinter-2026-DIGITAL.pdf
│   │       ├── Waterhead-Drinks-Summer-2026-WEB.pdf
│   │       └── Wine-List-The-Waterhead-Inn.pdf
│   ├── download-2026-11-20T14-31-42.sh
│   ├── images
│   ├── kafoodie
│   │   ├── ALL_MENUS_CHECKLIST.md
│   │   ├── Northallerton_Inn
│   │   │   └── Northallerton_Inn_all_menus.json
│   │   ├── Offshore
│   │   │   └── Offshore_all_menus.json
│   │   ├── The_Amble_Inn_full_menu
bash

cd /mnt/user-data/uploads; sed -n 250,1110p root_tree.md | grep -v -E '\.(pdf|jpg|jpeg|png|webp|md|json)$' | head -150; echo ======; grep -n -E "^(├|└)── [^ ]+$" root_tree.md | sed -n 1,80p
Output

│   │   ├── The_Amble_Inn_full_menu
│   │   ├── The_Ambleside_Inn_full_menu
│   │   ├── The_Angel_Inn_full_menu
│   │   ├── The_Bamburgh_Castle_Inn_full_menu
│   │   ├── The_Black_Swan_Inn_full_menu
│   │   ├── The_Commissioners_Quay_Inn_full_menu
│   │   ├── The_Coniston_Inn_full_menu
│   │   ├── The_Harrogate_Inn
│   │   ├── The_Hogs_Head_Inn_full_menu
│   │   ├── The_Kings_Head_Inn_full_menu
│   │   ├── The_Kingslodge_Inn_full_menu
│   │   ├── The_Knaresborough_Inn
│   │   ├── The_Lindisfarne_Inn_full_menu
│   │   ├── The_Midland_Hotel
│   │   ├── The_Pheasant_full_menu
│   │   ├── The_Ripon_Inn
│   │   ├── The_Seaburn_Inn_full_menu
│   │   ├── The_Seaton_Lane_Inn_full_menu
│   │   ├── The_Stables_At_Cross_Butts_full_menu
│   │   ├── The_Swallow_Falls_Inn
│   │   ├── The_Swan_full_menu
│   │   ├── The_Temperance_Inn_full_menu
│   │   ├── The_Ullswater_Inn
│   │   ├── The_Wateredge_Inn_full_menu
│   │   ├── The_Waterhead_Inn
│   │   ├── The_Wordsworth
│   │   ├── Tynemouth_Castle_Inn
│   ├── menus_md
│   ├── pages_text
│   │   ├── about-us.txt
│   │   ├── accommodation.txt
│   │   ├── accommodation_durham_dog-friendly.txt
│   │   ├── accommodation_lake-district.txt
│   │   ├── accommodation_lake-district_dog-friendly.txt
│   │   ├── accommodation_lancashire.txt
│   │   ├── accommodation_lytham-st-annes_dog-friendly.txt
│   │   ├── accommodation_north-wales.txt
│   │   ├── accommodation_north-wales_dog-friendly.txt
│   │   ├── accommodation_northumberland.txt
│   │   ├── accommodation_northumberland_dog-friendly.txt
│   │   ├── accommodation_sunderland.txt
│   │   ├── accommodation_tyne-and-wear.txt
│   │   ├── accommodation_yorkshire.txt
│   │   ├── accommodation_yorkshire_dog-friendly.txt
│   │   ├── amble-inn_restaurant.txt
│   │   ├── ambleside-inn.txt
│   │   ├── ambleside-inn_restaurant.txt
│   │   ├── angel-inn_restaurant.txt
│   │   ├── bamburgh-castle-inn.txt
│   │   ├── book-a-table.txt
│   │   ├── book-direct.txt
│   │   ├── bulls-head-inn.txt
│   │   ├── bulls-head-inn_gift-vouchers.txt
│   │   ├── bulls-head-inn_restaurant.txt
│   │   ├── businessbooker.txt
│   │   ├── careers-lh.txt
│   │   ├── christmas.txt
│   │   ├── christmas_breakfast-with-santa.txt
│   │   ├── christmas_christmas-day-lunch.txt
│   │   ├── christmas_festive-fayre.txt
│   │   ├── christmas_party-nights.txt
│   │   ├── commissioners-quay-inn.txt
│   │   ├── cones.txt
│   │   ├── coniston-inn.txt
│   │   ├── coniston-inn_restaurant.txt
│   │   ├── contact-us-2.txt
│   │   ├── contact-us-lh.txt
│   │   ├── contact-us.txt
│   │   ├── cookies-list.txt
│   │   ├── dean-court.txt
│   │   ├── dean-court_restaurant.txt
│   │   ├── dog-fest-sign-up.txt
│   │   ├── dog-friendly.txt
│   │   ├── dog-friendly_durham-walks.txt
│   │   ├── dog-friendly_lake-district-walks.txt
│   │   ├── dog-friendly_lancashire-walks.txt
│   │   ├── dog-friendly_north-wales-walks.txt
│   │   ├── dog-friendly_tyne-and-wear-walks.txt
│   │   ├── dog-friendly_yorkshire-walks.txt
│   │   ├── dogfest-ticket-giveaway.txt
│   │   ├── fathers-day.txt
│   │   ├── food-and-drink_breakfast.txt
│   │   ├── food-and-drink_lake-district.txt
│   │   ├── food-and-drink_sunday-carvery.txt
│   │   ├── gift-vouchers.txt
│   │   ├── groups.txt
│   │   ├── guides_things-to-do-in-york.txt
│   │   ├── harrogate-inn.txt
│   │   ├── harrogate-inn_restaurant.txt
│   │   ├── hogs-head-inn.txt
│   │   ├── hogs-head-inn_restaurant.txt
│   │   ├── hogs-travelzoo.txt
│   │   ├── index.txt
│   │   ├── inn-the-know.txt
│   │   ├── inntheknow-thankyou.txt
│   │   ├── join-the-inn-crowd.txt
│   │   ├── kings-head-inn.txt
│   │   ├── kings-head-inn_family-friendly.txt
│   │   ├── kings-head-inn_restaurant.txt
│   │   ├── kingslodge-inn.txt
│   │   ├── kingslodge-inn_restaurant.txt
│   │   ├── knaresborough-inn.txt
│   │   ├── knaresborough-inn_restaurant.txt
│   │   ├── legals.txt
│   │   ├── legals_code-of-conduct.txt
│   │   ├── legals_cookie-policy.txt
│   │   ├── legals_gift-voucher-terms-and-conditions.txt
│   │   ├── legals_privacy-policy.txt
│   │   ├── legals_terms-conditions.txt
│   │   ├── lindisfarne-inn.txt
│   │   ├── lindisfarne-inn_restaurant.txt
│   │   ├── lms-moderation-charter.txt
│   │   ├── news_5-reasons-to-book-a-uk-holiday.txt
│   │   ├── news_5-reasons-to-visit-the-lake-district.txt
│   │   ├── news_8-inns-shortlisted-pub-bar-awards.txt
│   │   ├── news___thekingsheadinn.txt
│   │   ├── news_adorable-arlo-the-lindisfarne-inn.txt
│   │   ├── news_alnwick-markets.txt
│   │   ├── news_amble-inn-rock-with-colony-fest-support.txt
│   │   ├── news_ambleside-christmas-lights-support.txt
│   │   ├── news_angel-reopens.txt
│   │   ├── news_applications-open-swallow-falls-roles.txt
│   │   ├── news_art-deco-icons-at-inn-collection-group.txt
│   │   ├── news_bamburgh-castle-inn-unique-renovation.txt
│   │   ├── news_bamburgh-castle-inn-welcomes-tourism-students.txt
│   │   ├── news_bernhoeft-joins-as-cfo.txt
│   │   ├── news_best-place-to-work-recognition.txt
│   │   ├── news_best-pub-employer-for-second-year-running.txt
│   │   ├── news_black-swan-deliver-helmsley-post-office.txt
│   │   ├── news_blooming-result-the-amble-inn-receives-community-garden-award.txt
│   │   ├── news_bluebird-k7s-return-to-ullswater.txt
│   │   ├── news_bomb-back-blast-tynemouth-castle-inn.txt
│   │   ├── news_bookings-open-wordsworth.txt
│   │   ├── news_businesses-raise-over-70k-for-ne-youth-at-charity-event.txt
│   │   ├── news_celebrations-at-record-breaking-tourism-awards.txt
│   │   ├── news_central-reservations-investment-for-group.txt
│   │   ├── news_charity-walk-inn-breaks-launch.txt
│   │   ├── news_clay-shooting-at-bywell-shooting-grounds.txt
│   │   ├── news_coastal-inns-shining-times-guardian.txt
│   │   ├── news_cocktail-contest-nominees-chosen.txt
│   │   ├── news_coniston-christmas-lights.txt
│   │   ├── news_construction-tynemouth-castle-inn.txt
│   │   ├── news_contributions-boost-cash-for-kids.txt
│   │   ├── news_cook-off-ekes-young-chef-title-for-sam.txt
│   │   ├── news_creative-sound-off-tynemouth-castle-inn.txt
│   │   ├── news_culinary-careers-beckon-chef-academy.txt
│   │   ├── news_dawdon-community-centre-give-inn-back.txt
│   │   ├── news_dean-court-trinity-hay-awards-finalists.txt
│   │   ├── news_dean-court-triumph-at-hay-annual-awards.txt
│   │   ├── news_deliver-good-cheer-mission-christmas.txt
======
2:├── PROJECT-REVIEW
20:├── __pycache__
24:├── _dev
41:├── build_menu_explorer.py
42:├── build_venue_export.py
43:├── config
47:├── docs
78:├── exports
131:├── inncollectiongroup.com_root
877:├── menu_review_server.py
878:├── menu_review_state.sqlite3
879:├── pages
1107:├── requirements.txt
1108:└── root.tree.md
bash

cd /mnt/user-data/uploads; sed -n 879,1110p root_tree.md | grep -v -E '\.(jpg|jpeg|png|webp|svg)$' | head -120; echo ====; sed -n 1,212p 07_ARCHITECTURE_VERIFICATION_AND_NETLIFY_REMOVAL.md | head -120
Output

├── pages
│   ├── Menu explorer — Inn Collection Group.html
│   ├── discovered-media.html
│   ├── discovered_media.csv
│   ├── documents
│   │   └── extracted-to-md
│   │       ├── 2026-Christmas-Day-Lunch.pdf
│   │       ├── Crown-Menu-Offshore-DIGITAL-WEB.pdf
│   │       ├── Crown-Menu-The-Ambleside-Inn-DIGITAL-WEB.pdf
│   │       ├── Crown-Menu-The-Angel-Inn-DIGITAL-WEB.pdf
│   │       ├── Crown-Menu-The-Bamburgh-Castle-Inn-DIGITAL-WEB.pdf
│   │       ├── Crown-Menu-The-Bulls-Head-Inn-DIGITAL-WEB.pdf
│   │       ├── Crown-Menu-The-Coniston-Inn-DIGITAL-WEB.pdf
│   │       ├── Crown-Menu-The-Hogs-Head-Inn-DIGITAL-WEB.pdf
│   │       ├── Crown-Menu-The-Knaresborough-Inn-DIGITAL-WEB.pdf
│   │       ├── Crown-Menu-The-Pheasant-Inn-DIGITAL-WEB.pdf
│   │       ├── Crown-Menu-The-Ripon-Inn-DIGITAL-WEB.pdf
│   │       ├── Crown-Menu-The-Stables-DIGITAL-WEB.pdf
│   │       ├── Crown-Menu-The-Swallow-Falls-Inn-DIGITAL-WEB.pdf
│   │       ├── Crown-Menu-The-Swan-DIGITAL-WEB.pdf
│   │       ├── Crown-Menu-The-Tynemouth-Castle-Inn-DIGITAL-WEB.pdf
│   │       ├── Crown-Menu-The-Ullswater-Inn-DIGITAL-WEB.pdf
│   │       ├── Crown-Menu-The-Wateredge-Inn-DIGITAL-WEB.pdf
│   │       ├── Dean-Court-Drinks-Summer-2026-Web.pdf
│   │       ├── E-Bike-and-Scooter-Policy.pdf
│   │       ├── Heritage-Menu-The-Amble-Inn-DIGITAL-WEB.pdf
│   │       ├── Heritage-Menu-The-Commissioners-Quay-Inn-DIGITAL-WEB.pdf
│   │       ├── Heritage-Menu-The-Kings-Head-Inn-DIGITAL-WEB.pdf
│   │       ├── Heritage-Menu-The-Kingslodge-Inn-DIGITAL-WEB.pdf
│   │       ├── Heritage-Menu-The-Lindisfarne-Inn-DIGITAL-WEB.pdf
│   │       ├── Heritage-Menu-The-Northallerton-Inn-DIGITAL-WEB.pdf
│   │       ├── Heritage-Menu-The-Seaburn-Inn-DIGITAL-WEB.pdf
│   │       ├── Heritage-Menu-The-Seaton-Lane-Inn-DIGITAL-WEB.pdf
│   │       ├── Midland-Drinks-Summer-2026-Web.pdf
│   │       ├── Offshore-Drinks-Autumnx3aWinter-2026-DIGITAL.pdf
│   │       ├── Oswins.pdf
│   │       ├── Party-Night-Menu-2026.pdf
│   │       ├── Signature-All-Day-Menu-Black-Swan-DIGITAL-WEB.pdf
│   │       ├── Signature-All-Day-Menu-Dean-Court-DIGITAL-WEB.pdf
│   │       ├── Signature-All-Day-Menu-The-Harrogate-Inn-DIGITAL-WEB.pdf
│   │       ├── Signature-All-Day-Menu-The-Midland-Hotel-DIGITAL-WEB.pdf
│   │       ├── Signature-All-Day-Menu-The-Waterhead-Hotel-DIGITAL-WEB.pdf
│   │       ├── Signature-All-Day-Menu-The-Wordsworth-DIGITAL-WEB.pdf
│   │       ├── Signature-Dining-Menu-Black-Swan-DIGITAL.pdf
│   │       ├── Signature-Dining-Menu-Dean-Court-DIGITAL.pdf
│   │       ├── Signature-Dining-Menu-The-Harrogate-Inn-DIGITAL.pdf
│   │       ├── Signature-Dining-Menu-The-Midland-Hotel-DIGITAL.pdf
│   │       ├── Signature-Dining-Menu-The-Waterhead-Hotel-DIGITAL.pdf
│   │       ├── Signature-Dining-Menu-The-Wordsworth-DIGITAL.pdf
│   │       ├── Sunday-Menu-Black-Swan-DIGITAL.pdf
│   │       ├── Sunday-Menu-Dean-Court-WEB.pdf
│   │       ├── Sunday-Menu-Offshore-WEB.pdf
│   │       ├── Sunday-Menu-The-Amble-Inn-DIGITAL.pdf
│   │       ├── Sunday-Menu-The-Ambleside-WEB.pdf
│   │       ├── Sunday-Menu-The-Angel-Inn-DIGITAL.pdf
│   │       ├── Sunday-Menu-The-Bamburgh-Castle-Inn.pdf
│   │       ├── Sunday-Menu-The-Bulls-Head-Inn-DIGITAL.pdf
│   │       ├── Sunday-Menu-The-Commissioners-Quay-Inn-DIGITAL.pdf
│   │       ├── Sunday-Menu-The-Coniston-Inn-DIGITAL.pdf
│   │       ├── Sunday-Menu-The-Harrogate-Inn-DIGITAL.pdf
│   │       ├── Sunday-Menu-The-Hogs-Head-Inn-DIGITAL.pdf
│   │       ├── Sunday-Menu-The-Kings-Head-Inn-DIGITAL.pdf
│   │       ├── Sunday-Menu-The-Kingslodge-Inn-DIGITAL.pdf
│   │       ├── Sunday-Menu-The-Knaresborough-Inn-DIGITAL.pdf
│   │       ├── Sunday-Menu-The-Lindisfarne-Inn-DIGITAL.pdf
│   │       ├── Sunday-Menu-The-Midland-DIGITAL.pdf
│   │       ├── Sunday-Menu-The-Northallerton-Inn-DIGITAL.pdf
│   │       ├── Sunday-Menu-The-Pheasant-Inn-DIGITAL.pdf
│   │       ├── Sunday-Menu-The-Ripon-Inn-DIGITAL.pdf
│   │       ├── Sunday-Menu-The-Seaburn-Inn-DIGITAL.pdf
│   │       ├── Sunday-Menu-The-Seaton-Lane-Inn-DIGITAL.pdf
│   │       ├── Sunday-Menu-The-Stables-DIGITAL.pdf
│   │       ├── Sunday-Menu-The-Swallow-Falls-Inn-DIGITAL.pdf
│   │       ├── Sunday-Menu-The-Swan-DIGITAL.pdf
│   │       ├── Sunday-Menu-The-Tynemouth-Castle-Inn-DIGITAL.pdf
│   │       ├── Sunday-Menu-The-Ullswater-Inn-DIGITAL.pdf
│   │       ├── Sunday-Menu-The-Wateredge-WEB.pdf
│   │       ├── Sunday-Menu-The-Waterhead-Hotel-DIGITAL.pdf
│   │       ├── Sunday-Menu-The-Wordsworth-NEW-DIGITAL.pdf
│   │       ├── TTI-The-Temperance-Inn-Autumn-2026-WEB.pdf
│   │       ├── TTI-The-Temperance-Inn-Drinks-Spring-2026-WEB.pdf
│   │       ├── The-Amble-Inn-Drinks-Autumnx3aWinter-2026-DIGITAL.pdf
│   │       ├── The-Ambleside-Inn-Drinks-Autumnx3aWinter-2026-DIGITAL.pdf
│   │       ├── The-Angel-Inn-Drinks-Autumnx3aWinter-2026-DIGITAL.pdf
│   │       ├── The-Bamburgh-Castle-Inn-Drinks-Autumnx3aWinter-2026-DIGITAL.pdf
│   │       ├── The-Black-Swan-Drinks-Summer-2026-Web.pdf
│   │       ├── The-Bulls-Head-Inn-Drinks-Autumnx3aWinter-2026-DIGITAL.pdf
│   │       ├── The-Commissioners-Quay-Inn-Drinks-Autumnx3aWinter-2026-DIGITAL.pdf
│   │       ├── The-Coniston-Inn-Drinks-Autumnx3aWinter-2026-DIGITAL.pdf
│   │       ├── The-Harrogate-Inn-Drinks-Summer-2026-Web.pdf
│   │       ├── The-Hogs-Head-Inn-Drinks-Autumnx3aWinter-2026-DIGITAL.pdf
│   │       ├── The-Kings-Head-Inn-Drinks-Autumnx3aWinter-2026-DIGITAL.pdf
│   │       ├── The-Kingslodge-Inn-Drinks-Autumnx3aWinter-2026-DIGITAL.pdf
│   │       ├── The-Knaresborough-Inn-Drinks-Autumnx3aWinter-2026-DIGITAL.pdf
│   │       ├── The-Lindisfarne-Inn-Drinks-Autumnx3aWinter-2026-DIGITAL.pdf
│   │       ├── The-Northallerton-Inn-Drinks-Autumnx3aWinter-2026-DIGITAL.pdf
│   │       ├── The-Pheasant-Inn-Drinks-Autumnx3aWinter-2026-DIGITAL.pdf
│   │       ├── The-Ripon-Inn-Drinks-Autumnx3aWinter-2026-DIGITAL.pdf
│   │       ├── The-Seaburn-Inn-Drinks-Autumnx3aWinter-2026-DIGITAL.pdf
│   │       ├── The-Seaton-Lane-Inn-Drinks-Autumnx3aWinter-2026-DIGITAL.pdf
│   │       ├── The-Stables-Drinks-Autumnx3aWinter-2026-DIGITAL.pdf
│   │       ├── The-Swallow-Falls-Inn-Drinks-Autumnx3aWinter-2026-DIGITAL.pdf
│   │       ├── The-Swan-Drinks-Autumnx3aWinter-2026-DIGITAL.pdf
│   │       ├── The-Tynemouth-Castle-Inn-Drinks-Autumnx3aWinter-2026-DIGITAL.pdf
│   │       ├── The-Ullswater-Inn-Drinks-Autumnx3aWinter-2026-DIGITAL.pdf
│   │       ├── The-Wateredge-Inn-Drinks-Autumnx3aWinter-2026-DIGITAL.pdf
│   │       ├── Waterhead-Drinks-Summer-2026-WEB.pdf
│   │       └── Wine-List-The-Waterhead-Inn.pdf
│   ├── fnb-crosscheck.html
│   ├── index.html
│   ├── launch-readiness.html
│   ├── menu-explorer-data.js
│   ├── menu-explorer.html
│   ├── menu-review.html
│   ├── menus.json
│   ├── menus_md
│   │   ├── 2026-Christmas-Day-Lunch.md
│   │   ├── Crown-Menu-Offshore-DIGITAL-WEB.md
│   │   ├── Crown-Menu-The-Ambleside-Inn-DIGITAL-WEB.md
│   │   ├── Crown-Menu-The-Angel-Inn-DIGITAL-WEB.md
====
# Document 07 — Architecture Verification, Evidence Reconciliation & Netlify Removal Report

> **Hospitality Technology Capability Assessment — The Inn Collection Group**  
> **Phase**: Architecture Verification, Evidence Reconciliation & Netlify Decommissioning  
> **Standard Key**: `[Observed]` · `[Code-verified]` · `[Database-verified]` · `[Tested]` · `[Inferred]` · `[Proposed]` · `[Unknown]`

---

## 1. Executive Summary

This report concludes the architecture verification and evidence reconciliation phase for The Inn Collection Group (ICG) hospitality technology workspace, executing the instructions set forth in `PROJECT-REVIEW/03.1 - Architecture Verification Evidence Reconciliation and Netlify Removal.md` and addressing the technical review in `PROJECT-REVIEW/03.md`.

### Core Outcomes:
1. **Complete Netlify Decommissioning**: All Netlify configuration files, serverless function implementations, local CLI metadata, and redundant file bundles have been completely excised from the repository. Zero Netlify dependencies remain.
2. **File-Path & Redundancy Reconciliation**: The relationship between `inncollectiongroup.com_root/menus_md/` and `pages/menus_md/` has been verified via byte-for-byte checksums and code tracing. The actual local runtime reads and modifies exclusively `inncollectiongroup.com_root/menus_md/`.
3. **Database Reality Clarification**: The SQL database is confirmed as SQLite (`menu_review_state.sqlite3`) with exactly one table (`issue_reviews`) holding review-state metadata. No domain models or business records are stored in SQL.
4. **Build Pipeline Reconciliation**: The number of build pipelines is formally reconciled to **exactly two**: `build_menu_explorer.py` and `build_venue_export.py`.
5. **Data Authority Boundaries**: `venue.json` is formally classified as a **canonical generated data artifact**, not a global source of truth.
6. **Regulatory Deferral**: Compliance rules (such as un-set allergen blocking policies) have been separated from technical architecture and designated for future policy review.

---

## 2. Deliverable A: Netlify Removal Manifest

Every file and directory touched during the Netlify decommissioning is cataloged below:

| Path | Classification | Action | Reason | Application Impact |
| :--- | :--- | :--- | :--- | :--- |
| `netlify.toml` | Netlify-only | **Removed** | Development deployment configuration (redirects, functions path, headers). Obsolete for local runtime. | **None** (`[Tested]`). Local server handles its own routing. |
| `netlify/functions/api.py` | Netlify-only | **Removed** | Ephemeral serverless duplicate of `menu_review_server.py`. | **None** (`[Tested]`). `menu_review_server.py` is the actual local API service. |
| `netlify/functions/__pycache__/` | Netlify-only | **Removed** | Compiled Python bytecode for serverless function. | **None**. |
| `netlify/functions/data/seed_reviews.json` | Netlify-only | **Removed** | Cold-start seed database for serverless function. Original master copy preserved at `pages/seed_reviews.json`. | **None**. Master copy preserved. |
| `netlify/functions/data/menus_md/` (103 files) | Netlify-only | **Removed** | Third duplicate copy of menu markdown packaged for AWS Lambda execution. | **None**. Master menus preserved in `inncollectiongroup.com_root/menus_md/`. |
| `netlify/` | Netlify-only | **Removed** | Directory tree hosting former serverless infrastructure. | **None**. |
| `.netlify/state.json` | Netlify-only | **Removed** | Local Netlify CLI state and site ID cache. | **None**. |
| `.netlify/` | Netlify-only | **Removed** | Netlify CLI cache directory. | **None**. |
| `.gitignore` | Shared | **Edited** | Removed lines referencing `.netlify/`. | **None** (`[Code-verified]`). |
| `requirements.txt` | Mixed | **Edited** | Replaced Netlify Python runtime detection notice with clean standard-library statement. | **None** (`[Code-verified]`). Application uses stdlib only. |
| `05_COMPONENT_RELATIONSHIPS.md` (root) | Obsolete Draft | **Removed** | Legacy root-level markdown file containing un-reconciled Netlify serverless claims. | **None**. Replaced by reconciled `docs/capability-assessment/` suite. |

---

## 3. Deliverable B: Architecture Verification Report

### 3.1 Actual Application Architecture & Runtime
* `[Code-verified]`: The application is a self-contained local web environment running on Python 3.8+ standard library.
* `[Code-verified]`: Application server is `menu_review_server.py`, an instance of `ThreadingHTTPServer` binding to `http://127.0.0.1:8000/`.
* `[Code-verified]`: Zero third-party web frameworks (no Flask, Django, FastAPI) and zero package dependencies.

### 3.2 File-Path Verification: The Markdown Directories
Investigation into the relationship between `inncollectiongroup.com_root/menus_md/` and `pages/menus_md/`:
1. **Content Comparison**:
   * `[Code-verified]`: Both directories contain exactly 103 Markdown files.
   * `[Code-verified]`: A deep binary comparison (`filecmp.cmp()`) across all 103 files confirms they are **100% byte-for-byte identical**. Zero content drift currently exists.
2. **Code Consumption Analysis**:
   * `[Code-verified]`: In `menu_review_server.py:26`, `MENUS = ROOT / "inncollectiongroup.com_root" / "menus_md"`.
   * `[Code-verified]`: `GET /api/menus` reads exclusively from `inncollectiongroup.com_root/menus_md/`.
   * `[Code-verified]`: `GET /api/menu` reads exclusively from `inncollectiongroup.com_root/menus_md/`.
   * `[Code-verified]`: `POST /api/issues/fix-duplicates` rewrites files exclusively in `inncollectiongroup.com_root/menus_md/`.
   * `[Code-verified]`: In `build_venue_export.py:47`, `MENUS_MD = CRAWL / "menus_md" = inncollectiongroup.com_root/menus_md`.
   * `[Code-verified]`: **`pages/menus_md/` is never read or written by any local server or build script**.
3. **Origin & Next Steps**:
   * `[Inferred]`: `pages/menus_md/` was created solely because Netlify was configured with `publish = "pages"`, requiring static files to reside under that web root.
   * `[Proposed]`: In accordance with Section 2.2 of the mandate, `pages/menus_md/` has been left intact for now. However, because Netlify is now removed, `pages/menus_md/` is completely redundant and can be safely deleted in a future cleanup phase once confirmed.

### 3.3 Database Implementation Verification
* `[Database-verified]`: Engine is **SQLite 3**, located at `/Users/leandrodisconzi/repos/Inn-Collection-Group/menu_review_state.sqlite3`.
* `[Database-verified]`: Schema consists of exactly one table:
  ```sql
  CREATE TABLE issue_reviews (
      menu_name TEXT NOT NULL,
      source_hash TEXT NOT NULL,
      issue_id TEXT NOT NULL,
      status TEXT NOT NULL,
      note TEXT NOT NULL DEFAULT '',
      updated_at TEXT NOT NULL,
      PRIMARY KEY (menu_name, source_hash, issue_id)
  );
  ```
* `[Database-verified]`: Constraints: Composite Primary Key on `(menu_name, source_hash, issue_id)`.
* `[Database-verified]`: Records: Exactly 1 row recording duplicate line fixes on `Crown-Menu-The-Tynemouth-Castle-Inn-DIGITAL-WEB-v2.md`.
* `[Database-verified]`: Consumers: Only `menu_review_server.py` reads and writes to this database. No other script or interface connects to SQLite.
* `[Database-verified]`: Persistence: Changes persist across process restarts because the database is written directly to the filesystem disk file.

### 3.4 Build Pipelines Reconciliation
* `[Code-verified]`: Reconciled the count discrepancy: **There are exactly two build pipelines**:
  1. **`build_menu_explorer.py` (411 lines)**:
     * *Inputs*: `inncollectiongroup.com_root/kafoodie/*_all_menus.json`, `config/venues.json`, `config/rules.json`.
     * *Outputs*: `pages/menu-explorer-data.js` (exported as `window.MENU_DATA`) and `ALL_MENUS_CHECKLIST.md`.
     * *Consumers*: `pages/menu-explorer.html` consumes `menu-explorer-data.js`.
  2. **`build_venue_export.py` (1,376 lines)**:
     * *Inputs*: `inncollectiongroup.com_root/menus_md/*.md`, `inncollectiongroup.com_root/kafoodie/`, `pages_text/*.txt`, `discovered_media.csv`, `config/*.json`.
     * *Outputs*: `exports/<Region>/<Venue>/venue.json` and `exports/<Region>/<Venue>/venue.md`.
     * *Consumers*: Currently an offline compilation output; **no interface currently consumes `venue.json`**.
* `[Code-verified]`: Neither pipeline depends on the other; both read raw crawl files independently. Neither pipeline contained any Netlify-specific logic.

### 3.5 Generated Data: `venue.json` Classification
* `[Code-verified]`: `venue.json` is a **canonical generated data artifact**, derived by merging four separate upstream sources via heuristic matching rules.
* **Source of Authority per Field**:
  * *Recipe identifiers, allergen declarations, nutritional values*: Sourced from Kafoodie crawl (`inncollectiongroup.com_root/kafoodie/`).
  * *Printed dish titles, printed descriptions, section placement, retail prices*: Sourced from extracted Markdown (`menus_md/`).
  * *Venue identity, phone, address, amenities*: Sourced from website text (`pages_text/`) and `config/venues.json`.
  * *Dish-to-recipe links*: Sourced from `config/aliases.json` and algorithmic token scoring.
* `[Code-verified]`: It is **not** an authoritative database; it is a compiled snapshot that must be regenerated whenever upstream files or alias rules change.

---

## 4. Deliverable C: Final Netlify Reference Audit

* **Files & Directories Removed**:
  * 1 configuration file (`netlify.toml`)
  * 2 directory trees (`netlify/` and `.netlify/`) containing 107 total files (including bytecode, seeds, and duplicated markdown files)
  * 1 legacy root draft (`05_COMPONENT_RELATIONSHIPS.md`)
* **Shared Files Edited**:
  * `.gitignore`: Removed `.netlify/` rule.
  * `requirements.txt`: Cleaned of Netlify runtime detection wording.
* **Remaining Netlify References**:
  * **Zero runtime or configuration references** remain in application source files (`*.py`, `*.html`, `*.js`, `*.json`, `*.csv`).
  * The only occurrences of the word "Netlify" in the entire repository exist in historical review and audit documents (`PROJECT-REVIEW/` and `docs/capability-assessment/`) explicitly documenting its decommissioning.
* **Local Dependency Check**:
Skimming the later project documents and key server code.
bash

cd /mnt/user-data/uploads; grep -n -i -E "multi-user|concurrent|0\.0\.0\.0|127\.0\.0\.1|LAN|network|more than one|several computers|hosting|deploy|WAL|postgres|auth|NFS|shared drive" 08*.md 09*.md 10*.md 11*.md 12*.md | cut -c1-260 | head -70; echo ====; sed -n 1,80p 11_TARGET_APPLICATION_AND_INTEGRATION_ARCHITECTURE.md | cut -c1-300
Output

08_TECHNICAL_BASELINE_CLOSURE_AND_EVIDENCE_AUDIT.md:16:* **Corrected**: Reconciled all documentation contradictions across Documents 02, 04, 05, 06, and 07. Specifically: corrected `venue.json` terminology to reflect its status as a generated data artifact rat
08_TECHNICAL_BASELINE_CLOSURE_AND_EVIDENCE_AUDIT.md:30:| **F-01** | **`venue.json` Terminology Contradiction** (Doc 02 stated `venue.json` was the "true canonical data model", contradicting Doc 07). | Inspected `build_venue_export.py` lines 1280–1335 and `ex
08_TECHNICAL_BASELINE_CLOSURE_AND_EVIDENCE_AUDIT.md:31:| **F-02** | **Overstated Real-Time Cross-Venue Auditing** (Doc 04 described cross-venue variance auditing as "real-time" and isolating "unapproved regional modifications"). | Inspected `pages/menu-explore
08_TECHNICAL_BASELINE_CLOSURE_AND_EVIDENCE_AUDIT.md:32:| **F-03** | **Speculative External Integrations** (Doc 05 named Zonal, Micros, Tevalis, FnB, Access, Birchman, Okta, Azure AD without proof of use by ICG). | Inspected full codebase, git history, configur
08_TECHNICAL_BASELINE_CLOSURE_AND_EVIDENCE_AUDIT.md:34:| **F-05** | **Overstated Scope of Application Testing** (Doc 07 claimed "all core application services verified", but listed only smoke tests). | Reviewed tests executed in Doc 07 vs total codebase capabi
08_TECHNICAL_BASELINE_CLOSURE_AND_EVIDENCE_AUDIT.md:36:| **F-07** | **Operational Authority Boundary Prematurely Hardcoded** (Doc 06 presented Kafoodie vs `venue.json` split as an agreed operational rule). | Reviewed culinary data governance and hospitality sy
08_TECHNICAL_BASELINE_CLOSURE_AND_EVIDENCE_AUDIT.md:95:1. **Source Data (Authoritative Crawl Inputs)**:
08_TECHNICAL_BASELINE_CLOSURE_AND_EVIDENCE_AUDIT.md:167:   * With Netlify decommissioned, `pages/menus_md/` is completely orphaned. Deletion has been held in abeyance in compliance with mandate preservation rules, pending final operational authorization.
08_TECHNICAL_BASELINE_CLOSURE_AND_EVIDENCE_AUDIT.md:169:   * Actual operational platforms used by The Inn Collection Group for Point-of-Sale (EPOS), Enterprise Resource Planning (ERP), stock control, and corporate Single Sign-On (SSO) remain unverified. Vendor
09_OPERATIONAL_REQUIREMENTS_AND_CAPABILITY_MAPPING.md:27:| **A1** | **Browser `localStorage` Role** | Inspected `pages/menu-review.html` lines 437–438 (`localStorage.getItem("icg_review_" + current + "_" + issueHash)`) and line 524. Code reveals `localStorag
09_OPERATIONAL_REQUIREMENTS_AND_CAPABILITY_MAPPING.md:98:* **Key Activities**: Accommodating regional menu variations (e.g. North Wales vs Lake District vs Northumberland specialties); tracking localized pricing tiers; ensuring brand standards across all prope
09_OPERATIONAL_REQUIREMENTS_AND_CAPABILITY_MAPPING.md:114:| **REQ-01** | Menu Admin | Maintain master menu definitions | F&B Coordinator | Menu metadata, validFrom, validTo, menu kind, brand | Create, version, and archive menu shells across seasons | None (rea
09_OPERATIONAL_REQUIREMENTS_AND_CAPABILITY_MAPPING.md:116:| **REQ-03** | Menu Admin | Author guest-facing dish descriptions | F&B Coordinator | Dish title, marketing copy, dietary tags | Rich text editing, dietary badge assignment | `menus_md/*.md` | `[Code-ve
09_OPERATIONAL_REQUIREMENTS_AND_CAPABILITY_MAPPING.md:151:| **REQ-38** | Governance | Role-based access control (RBAC) | Systems Administrator | User, role (Chef, Coordinator, Commercial) | Restrict editing of prices, recipes, and approvals | None | `[Code-ver
09_OPERATIONAL_REQUIREMENTS_AND_CAPABILITY_MAPPING.md:166:* **Priority 1 (P1 — Core Master Data & Reconciliation)**: 14 requirements establishing the essential data loop: Product Master, Recipe-to-Menu Item association, Allergen provenance tracking, Menu aut
10_TARGET_DATA_ARCHITECTURE_AND_ENTITY_MODEL.md:41:A major finding of the technical assessment is that **no single system is or should be authoritative across all hospitality data domains**. Declaring Kafoodie or printed menu cards universally authoritative cr
10_TARGET_DATA_ARCHITECTURE_AND_ENTITY_MODEL.md:43:The target architecture establishes an explicit, domain-specific authority matrix:
10_TARGET_DATA_ARCHITECTURE_AND_ENTITY_MODEL.md:45:| Information Domain | Authoritative Master Source | Secondary / Derived Consumers | Ingestion & Synchronization Mechanism | Authority Status |
10_TARGET_DATA_ARCHITECTURE_AND_ENTITY_MODEL.md:51:| **Guest Menu Copy & Sections** | **Marketing & F&B Menu Team** | Printed PDF menus, digital web menus, venue displays | Central Menu Authoring Module | `[Proposed]` |
10_TARGET_DATA_ARCHITECTURE_AND_ENTITY_MODEL.md:126:* **Classification**: Master Data. Persisted in SQL. Authority: Corporate Legal.
10_TARGET_DATA_ARCHITECTURE_AND_ENTITY_MODEL.md:132:* **Classification**: Reference Data. Persisted in SQL. Authority: Operations Director.
10_TARGET_DATA_ARCHITECTURE_AND_ENTITY_MODEL.md:138:* **Classification**: Master Data. Persisted in SQL. Authority: Operations Director.
10_TARGET_DATA_ARCHITECTURE_AND_ENTITY_MODEL.md:144:* **Classification**: Master Data. Persisted in SQL. Authority: Head of Procurement.
10_TARGET_DATA_ARCHITECTURE_AND_ENTITY_MODEL.md:150:* **Classification**: Master Data. Persisted in SQL. Authority: Procurement.
10_TARGET_DATA_ARCHITECTURE_AND_ENTITY_MODEL.md:156:* **Classification**: Master Data. Persisted in SQL. Authority: Development Chef / Procurement.
10_TARGET_DATA_ARCHITECTURE_AND_ENTITY_MODEL.md:162:* **Classification**: Master Data. Persisted in SQL. Authority: Group Executive Chef.
10_TARGET_DATA_ARCHITECTURE_AND_ENTITY_MODEL.md:168:* **Classification**: Audit History. Persisted in SQL. Authority: Executive Chef.
10_TARGET_DATA_ARCHITECTURE_AND_ENTITY_MODEL.md:174:* **Classification**: Master Data. Persisted in SQL. Authority: Development Chef.
10_TARGET_DATA_ARCHITECTURE_AND_ENTITY_MODEL.md:180:* **Classification**: Master Data. Persisted in SQL. Authority: Commercial Manager & F&B Coordinator.
10_TARGET_DATA_ARCHITECTURE_AND_ENTITY_MODEL.md:186:* **Classification**: Master Data. Persisted in SQL. Authority: F&B Coordinator.
10_TARGET_DATA_ARCHITECTURE_AND_ENTITY_MODEL.md:192:* **Classification**: Master Data. Persisted in SQL. Authority: F&B Coordinator.
10_TARGET_DATA_ARCHITECTURE_AND_ENTITY_MODEL.md:198:* **Classification**: Master Data. Persisted in SQL. Authority: F&B Coordinator.
10_TARGET_DATA_ARCHITECTURE_AND_ENTITY_MODEL.md:204:* **Classification**: Master Data (Binding Entity). Persisted in SQL. Authority: F&B Coordinator & General Manager.
10_TARGET_DATA_ARCHITECTURE_AND_ENTITY_MODEL.md:210:* **Classification**: Master Data. Persisted in SQL. Authority: Commercial Manager.
10_TARGET_DATA_ARCHITECTURE_AND_ENTITY_MODEL.md:216:* **Classification**: Master Data. Persisted in SQL. Authority: Systems Administrator.
10_TARGET_DATA_ARCHITECTURE_AND_ENTITY_MODEL.md:222:* **Classification**: Master Data. Persisted in SQL. Authority: Food Safety Compliance Officer.
10_TARGET_DATA_ARCHITECTURE_AND_ENTITY_MODEL.md:228:* **Classification**: Master Data. Persisted in SQL. Authority: Kafoodie Engine / Technical Chef.
10_TARGET_DATA_ARCHITECTURE_AND_ENTITY_MODEL.md:234:* **Classification**: Reference Data. Persisted on disk + SQL metadata. Authority: F&B Coordinator.
10_TARGET_DATA_ARCHITECTURE_AND_ENTITY_MODEL.md:240:* **Classification**: Audit History. Persisted in SQL. Authority: Compliance Officer.
10_TARGET_DATA_ARCHITECTURE_AND_ENTITY_MODEL.md:246:* **Classification**: Workflow State. Persisted in SQL. Authority: F&B Coordinator.
10_TARGET_DATA_ARCHITECTURE_AND_ENTITY_MODEL.md:252:* **Classification**: Workflow State. Persisted in SQL. Authority: F&B Coordinator.
10_TARGET_DATA_ARCHITECTURE_AND_ENTITY_MODEL.md:258:* **Classification**: Workflow State. Persisted in SQL. Authority: Area Operations Manager.
10_TARGET_DATA_ARCHITECTURE_AND_ENTITY_MODEL.md:264:* **Classification**: Master Data. Persisted in SQL. Authority: Systems Admin.
10_TARGET_DATA_ARCHITECTURE_AND_ENTITY_MODEL.md:270:* **Classification**: Master Data. Persisted in SQL. Authority: Systems Admin.
10_TARGET_DATA_ARCHITECTURE_AND_ENTITY_MODEL.md:276:* **Classification**: Audit History (Immutable). Persisted in SQL. Authority: Compliance.
10_TARGET_DATA_ARCHITECTURE_AND_ENTITY_MODEL.md:289:│ Engine: SQLite 3 (WAL Mode)       │ Storage: File System Versioned     │
10_TARGET_DATA_ARCHITECTURE_AND_ENTITY_MODEL.md:303:* **SQLite in WAL (Write-Ahead Logging) Mode**: Provides zero-maintenance, zero-configuration local ACID persistence. Ideal for local multi-threaded Python server access. Capable of supporting millions of row
10_TARGET_DATA_ARCHITECTURE_AND_ENTITY_MODEL.md:304:* **Migration Boundary**: SQLite serves as the target operational database for Phases 1–3. A transition to PostgreSQL is recommended only when multi-user concurrent remote editing, enterprise SSO integratio
11_TARGET_APPLICATION_AND_INTEGRATION_ARCHITECTURE.md:34:│ • Menu Authoring API   │ • Master SKU Catalog   │ • 14 FIR Allergen Engine       │
11_TARGET_APPLICATION_AND_INTEGRATION_ARCHITECTURE.md:51:│                  OPERATIONAL DATA LAYER (SQLite WAL / ACID)                      │
11_TARGET_APPLICATION_AND_INTEGRATION_ARCHITECTURE.md:75:| **Operational Complexity** | High. Multiple services, RPC protocols, network latency, distributed transactions. | Low. Single unified Python application running locally or on a standard internal VM. | 
11_TARGET_APPLICATION_AND_INTEGRATION_ARCHITECTURE.md:76:| **Data Consistency** | Eventual consistency; complex saga patterns across menu, recipe, and price services. | Strong ACID consistency via SQLite WAL mode. | Culinary recipes, allergens, and menu prices
11_TARGET_APPLICATION_AND_INTEGRATION_ARCHITECTURE.md:77:| **Deployment Footprint** | Docker, Kubernetes, API Gateways, service meshes, distributed monitoring. | Zero-dependency or single virtualenv standard Python deployment. | Matches existing repository rea
11_TARGET_APPLICATION_AND_INTEGRATION_ARCHITECTURE.md:78:| **Development Velocity** | Significant cross-service boilerplate, contract testing, and network mocking. | Direct Python module imports and shared data models. | Allows rapid implementation of end-to-e
11_TARGET_APPLICATION_AND_INTEGRATION_ARCHITECTURE.md:137:The integration landscape strictly separates verified internal systems from hypothetical external platforms:
11_TARGET_APPLICATION_AND_INTEGRATION_ARCHITECTURE.md:169:1. **Authentication & Session Security**:
11_TARGET_APPLICATION_AND_INTEGRATION_ARCHITECTURE.md:170:   * *Phase 1–3*: Lightweight session token authentication built on standard secure HTTP-only cookies.
11_TARGET_APPLICATION_AND_INTEGRATION_ARCHITECTURE.md:174:   * **Development / Executive Chef**: Authoring rights for recipes, ingredients, and prep SOPs; read-only for commercial margins.
11_TARGET_APPLICATION_AND_INTEGRATION_ARCHITECTURE.md:175:   * **Food Safety Compliance Officer**: Exclusive certification authority for allergen declarations and supplier spec sheet sign-offs.
11_TARGET_APPLICATION_AND_INTEGRATION_ARCHITECTURE.md:176:   * **Commercial Manager**: Exclusive approval authority for retail selling prices and target margin thresholds.
11_TARGET_APPLICATION_AND_INTEGRATION_ARCHITECTURE.md:189:| **Operational Database** | SQLite 3 (single table `issue_reviews`) | 1. **SQLite (WAL Mode)**<br/>2. PostgreSQL<br/>3. MongoDB | **SQLite 3 in WAL Mode** | SQLite is already embedded in Python, requir
12_END_TO_END_OPERATIONAL_WORKFLOW_DESIGN.md:85:* **Trigger**: Periodic menu refresh, dish replacement, or planned seasonal menu adjustment.
12_END_TO_END_OPERATIONAL_WORKFLOW_DESIGN.md:114:  1. Coordinator reviews section balance, pricing flow, and layout constraints.
12_END_TO_END_OPERATIONAL_WORKFLOW_DESIGN.md:222:  1. Chef determines whether the difference represents an unauthorized kitchen shortcut, supplier substitution, or clerical data-entry error.
12_END_TO_END_OPERATIONAL_WORKFLOW_DESIGN.md:223:  2. Compliance Officer authorizes the required operational remediation.
12_END_TO_END_OPERATIONAL_WORKFLOW_DESIGN.md:254:  1. Compliance Officer certifies the authenticity and regulatory validity of the change.
12_END_TO_END_OPERATIONAL_WORKFLOW_DESIGN.md:273:    E7_6 -->|Discrepancy Detected| E7_7["Block Till Deployment & Generate Exception Report"]
12_END_TO_END_OPERATIONAL_WORKFLOW_DESIGN.md:274:    E7_6 -->|100% Match| E7_8["Authorize Till Master Package for Site Download"]
12_END_TO_END_OPERATIONAL_WORKFLOW_DESIGN.md:288:  1. Systems Admin authorizes release of till package following 100% validation pass.
====
# Document 11 — Target Application and Integration Architecture

> **Knowledge Base** · Inn Collection Group (ICG) Hospitality Technology Workspace  
> **Document** 11 of 15 · Published: 2026-11-22  
> **Phase**: Phase 2 — Hospitality Technology Requirements, Target Architecture & Implementation Blueprint  
> **Evidence Standards**: `[Code-verified]` · `[Database-verified]` · `[Proposed]` · `[Requires-confirmation]`

---

## 1. Executive Summary & Architecture Strategy

This document establishes the application, API, integration, security, and technology architecture for the target Inn Collection Group (ICG) hospitality technology platform.

A foundational architectural principle governs this design:
> **Proportionate Engineering**: Avoid premature microservices, distributed complexity, and excessive infrastructure. Build a clean, maintainable **modular application** centered around operational workflows rather than theoretical software patterns.

The current system is an effective local data-processing environment comprising a single-threaded/multi-threaded Python standard library server (`menu_review_server.py`), two batch build scripts, and seven isolated HTML interfaces. 

The target application architecture unifies these capabilities into a **cohesive modular architecture** powered by an extended local Python backend, structured REST APIs, an integrated SQLite operational database, and unified web workspaces.

---

## 2. Target Application Component Decomposition

The application layer is structured into ten cohesive functional modules:

```
┌──────────────────────────────────────────────────────────────────────────────────┐
│                   TARGET APPLICATION ARCHITECTURE (MODULAR BACKEND)             │
├──────────────────────────────────────────────────────────────────────────────────┤
│                                 REST ROUTING & DISPATCH                          │
├────────────────────────┬────────────────────────┬────────────────────────────────┤
│ 1. MENU MANAGEMENT     │ 2. PRODUCT & RECIPE    │ 3. FOOD SAFETY & ALLERGENS     │
│ • Menu Authoring API   │ • Master SKU Catalog   │ • 14 FIR Allergen Engine       │
│ • Section Ordering     │ • Recipe Formulation   │ • Un-set Allergen Gate         │
│ • Item Pricing Sync    │ • Ingredient BOM Cost  │ • Supplier Spec Sheets         │
├────────────────────────┼────────────────────────┼────────────────────────────────┤
│ 4. COMMERCIAL ENGINE   │ 5. SUPPLIER & PURCHASE │ 6. EPOS ADAPTER & MAPPING      │
│ • Margin & GP% Calc    │ • Purveyor Registry    │ • PLU Code Assignment          │
│ • Price Tier Hierarchy │ • Pack-to-Kitchen Unit │ • Till Category Formatting     │
│ • Cost Shift Modeling  │ • Price Change History │ • Pre-launch Till QA           │
├────────────────────────┼────────────────────────┼────────────────────────────────┤
│ 7. LAUNCH ORCHESTRATOR │ 8. MULTI-SITE RECON    │ 9. MEDIA & DOCUMENT QC         │
│ • Campaign Milestones  │ • 29-Inn Directory     │ • Menu Review & Triage         │
│ • Spec Book Generator  │ • Cross-Site Variance  │ • Duplicate Line Remediation   │
│ • Venue Readiness RAG  │ • Heuristic Matcher    │ • Batch Media Exporter         │
├────────────────────────┴────────────────────────┴────────────────────────────────┤
│ 10. GOVERNANCE, RBAC & AUDIT LOGGING                                             │
│ • User Roles & Permissions • Tamper-evident Audit Trail • Provenance Tracking    │
├──────────────────────────────────────────────────────────────────────────────────┤
│                  OPERATIONAL DATA LAYER (SQLite WAL / ACID)                      │
└──────────────────────────────────────────────────────────────────────────────────┘
```

### Module Responsibilities:
1. **Menu Management Module**: Provides CRUD operations for master menus, sections, and menu items. Manages menu lifecycle states (`Draft`, `Review`, `Approved`, `Published`, `Archived`). Replaces raw manual markdown editing with structured endpoints.
2. **Product & Recipe Module**: Manages commercial product records (SKUs), culinary recipes, ingredient lists (Bills of Materials), yields, portion sizes, and prep instructions. Bridges central kitchen formulations to sellable menu items.
3. **Food Safety & Allergen Module**: Manages the 14 statutory allergens per UK Food Information Regulations (FIR). Provides automated bitmask calculation, tracks containment types (`Contains`, `May Contain`), and enforces compliance gates for un-set flags (`is_pw_allergen_not_set`).
4. **Commercial Engine Module**: Computes dish Cost of Goods Sold (COGS), net selling prices excluding 20% VAT, and gross profit percentages ($\text{GP\%} = \frac{\text{Net Price} - \text{COGS}}{\text{Net Price}}$). Models price-tier variations and cost-inflation impact across recipes.
5. **Supplier & Purchasing Module**: Catalogs approved suppliers, purchasing pack sizes, order units, and net case costs. Handles unit conversions (e.g. converting a 6x1kg case into recipe gram portions).
6. **EPOS Adapter & Mapping Module**: Assigns Price Look-Up (PLU) numbers, button labels, and kitchen printer routes. Prepares importable till configuration files and conducts pre-release price-verification audits.
7. **Launch Orchestrator Module**: Manages seasonal menu campaigns, cross-functional milestone checklists (Marketing, Operations, F&B, Finance), compiles kitchen "Spec Books" (PDF recipe/plating cards), and tracks venue-by-venue sign-offs.
8. **Multi-Site Reconciliation Module**: Houses the 29-inn estate directory across 7 operating regions. Executes heuristic token reconciliation between printed menu titles and Kafoodie recipes (`build_venue_export.py`).
9. **Media & Document QC Module**: Retains and extends the verified capabilities of `menu_review_server.py`: side-by-side PDF/Markdown inspection, atomic duplicate line fixes, and batch media downloading.
10. **Governance & Audit Module**: Manages user identities, role-based access control (RBAC), and writes append-only event logs capturing all menu, recipe, allergen, and price modifications.

---

## 3. Justification for a Modular Monolith (Vs. Microservices)

A deliberate architectural decision has been made: **Do NOT adopt a microservices architecture**.

| Architectural Dimension | Microservices Approach | Proposed Modular Monolith | Rationale & Justification |
| :--- | :--- | :--- | :--- |
| **Operational Complexity** | High. Multiple services, RPC protocols, network latency, distributed transactions. | Low. Single unified Python application running locally or on a standard internal VM. | The ICG estate comprises 29–31 properties managed by a lean head-office F&B team. Distributed i
| **Data Consistency** | Eventual consistency; complex saga patterns across menu, recipe, and price services. | Strong ACID consistency via SQLite WAL mode. | Culinary recipes, allergens, and menu prices require strict transactional consistency; food safety compliance cannot tolerate eventual-consis
| **Deployment Footprint** | Docker, Kubernetes, API Gateways, service meshes, distributed monitoring. | Zero-dependency or single virtualenv standard Python deployment. | Matches existing repository reality; can be run on a local workstation or deployed on an internal server in minutes without DevO
| **Development Velocity** | Significant cross-service boilerplate, contract testing, and network mocking. | Direct Python module imports and shared data models. | Allows rapid implementation of end-to-end operational workflows (e.g. Product -> Recipe -> Allergen -> Menu Item -> Price). |

---
Checking the server file and the documentation claims.
Still reviewing: I’ve read the tree and docs, and now I’m checking the server code and sqlite against what the docs claim, especially for multi-computer use.

Ran 4 commands, updated memory
bash

cd /mnt/user-data/uploads; grep -n -E "HOST|PORT|127\.0\.0\.1|ThreadingHTTPServer|ROOT =|DB_PATH|sqlite3.connect|journal|WAL|def do_|Access-Control|path_traversal|resolve\(\)|ASSET_HOST|subprocess" menu_review_server.py | head -50; echo ====; sqlite3 menu_review_state.sqlite3 ".tables" "PRAGMA journal_mode;" "select count(*) from issue_reviews;" 2>&1; echo ====; grep -c "venue.json" root_tree.md; grep -n -E "requirements|root.tree" root_tree.md | tail -3; grep -n -i -E "29|31" 15_ARCHITECTURE_BLUEPRINT_EXECUTIVE_SUMMARY.md | head -5; grep -n -E "Level [123]|40 operational|100\+" 03*.md 09*.md 13*.md | cut -c1-160 | head
Output

18:from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
23:ROOT = Path(__file__).resolve().parent
28:EXPORTS = ROOT / "exports"
30:MAX_EXPORT_REQUEST_BYTES = 32 * 1024 * 1024
31:MAX_EXPORT_ITEMS = 20_000
32:ASSET_HOST = "www.inncollectiongroup.com"
46:            or target.hostname != ASSET_HOST
111:    def do_POST(self) -> None:
130:        if len(items) > MAX_EXPORT_ITEMS:
132:                {"error": f"An export can contain at most {MAX_EXPORT_ITEMS} assets"},
150:    def do_GET(self) -> None:
254:        if content_length < 0 or content_length > MAX_EXPORT_REQUEST_BYTES:
271:        connection = sqlite3.connect(REVIEW_DB)
491:                or parsed.hostname != ASSET_HOST
496:                raise ValueError(f"Only HTTPS assets from {ASSET_HOST} can be exported")
525:                parent = EXPORTS / group[0] / group[1] / group[2]
595:    parser.add_argument("--host", default="127.0.0.1", help="interface to bind (default: localhost)")
604:    server = ThreadingHTTPServer((args.host, args.port), MenuReviewHandler)
====
/bin/sh: 1: sqlite3: not found
====
3
1107:├── requirements.txt
1108:└── root.tree.md
41:* **Target State**: A unified, modular hospitality management platform where commercial products, culinary recipes, ingredient costs, statutory allergens, printed menu cards, and till configurations are transactionally linked across all 29 estate inns.
47:1. **Rejects Premature Microservices**: The system serves 29–31 properties managed by a lean head-office culinary and operations team. A microservices architecture would introduce distributed network failures, eventual consistency lag in food safety data, and unnecessary DevOps complexity. The **modular monolith** approach provides strong ACID guarantees, sub-millisecond query execution, and rapid development velocity within a single Python runtime.
66:| **Multi-Site Coordination**| 29-inn estate directory, regional menus, variance comparison | Multi-Site Module (`build_venue_export.py`, Explorer) | Phase 1 & 3 |
03_COMPONENT_AND_CAPABILITY_REGISTER.md:104:  * `[Code-verified]`: Client-side filtering of 100+ operational requirements across hospitality personas.
09_OPERATIONAL_REQUIREMENTS_AND_CAPABILITY_MAPPING.md:110:The following matrix formally catalogs 40 operational requirements derived from the F&B Coordinator ma
13_CURRENT_TO_TARGET_ARCHITECTURE_TRANSITION_MAP.md:34:| **Menu Review UI** | `pages/menu-review.html` | Level 1: Operational document review tool (vanilla SPA)
13_CURRENT_TO_TARGET_ARCHITECTURE_TRANSITION_MAP.md:35:| **Discovered Media UI** | `pages/discovered-media.html` | Level 1: Operational media discovery and batc
13_CURRENT_TO_TARGET_ARCHITECTURE_TRANSITION_MAP.md:36:| **Menu Explorer UI** | `pages/menu-explorer.html` | Level 1: Operational multi-outlet explorer and cros
13_CURRENT_TO_TARGET_ARCHITECTURE_TRANSITION_MAP.md:37:| **Product Data UI** | `pages/product-data.html` | Level 3: Static prototype mockup. Hardcoded HTML tabl
13_CURRENT_TO_TARGET_ARCHITECTURE_TRANSITION_MAP.md:38:| **Launch Readiness UI** | `pages/launch-readiness.html` | Level 3: Client-side prototype simulation. In
13_CURRENT_TO_TARGET_ARCHITECTURE_TRANSITION_MAP.md:39:| **F&B Role Cross-check** | `pages/fnb-crosscheck.html` | Level 3: Internal role-coverage analysis SPA. 
13_CURRENT_TO_TARGET_ARCHITECTURE_TRANSITION_MAP.md:40:| **Chicken Liver Parfait** | `pages/recipes/chicken-liver-parfait...html` | Level 3: Static, rich dish s
13_CURRENT_TO_TARGET_ARCHITECTURE_TRANSITION_MAP.md:41:| **Local Application Server** | `menu_review_server.py` | Level 1: Python stdlib HTTP server (615 lines)
bash

cd /mnt/user-data/uploads; python3 - <<'E'
import sqlite3
c=sqlite3.connect('menu_review_state.sqlite3')
print(c.execute("select name from sqlite_master").fetchall())
print(c.execute("pragma journal_mode").fetchall())
print(c.execute("select count(*) from issue_reviews").fetchall())
E
sed -n 260,290p menu_review_server.py; grep -n "recipes/\|/pages\|SimpleHTTP\|directory=" menu_review_server.py | head; ls /mnt/user-data/uploads | grep -i -E "VENUE-EXPORT|requirements"; grep -n -i "fnb-crosscheck\|40 \|100+" 08*.md | cut -c1-200 | head -5
Output

[('issue_reviews',), ('sqlite_autoindex_issue_reviews_1',)]
[('delete',)]
[(1,)]
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
154:            self.send_header("Location", "/pages/menu-review.html")
158:            "/pages/menu-review.html",
159:            "/pages/discovered-media.html",
160:            "/pages/fnb-crosscheck.html",
161:            "/pages/launch-readiness.html",
162:            "/pages/product-data.html",
166:        if request.path == "/pages/menu-explorer.html":
169:        if request.path == "/pages/menu-explorer-data.js":
09_OPERATIONAL_REQUIREMENTS_AND_CAPABILITY_MAPPING.md
74:│ • F&B Role Cross-check (pages/fnb-crosscheck.html: static matrix)      │
Checking the proposed database settings against the docs.

Comparing the file layout against the documentation.

bash

cd /mnt/user-data/uploads; grep -c "Persisted in SQL" 10*.md; grep -n -E "^#### |^### " 10*.md | sed -n 1,45p | cut -c1-120; grep -n -i "tamper\|unified icg_hospitality\|icg_hospitality" 1*.md | cut -c1-150 | head -5; sed -n 295,304p 10*.md | cut -c1-400
Output

The command ran, but its output was not valid UTF-8 text, so nothing was returned: no stdout, no stderr and no exit code. One cause is UTF-8 text cut in the middle of a character: `head -c`, `tail -c` and `cut -c` count bytes, and a `grep -o` pattern can match part of a character. For such text, use `head -n` if its lines are short; otherwise slice or match it in Python. If the output was binary, redirect both stdout and stderr to a file. To look at an image, call the view tool on its path. To inspect any other binary file, read it with a Python library or convert it to text first; for a quick look at its raw bytes, run `od -c FILE | head`. For text in another encoding, decode it in Python with that encoding or convert it with iconv.
bash

cd /mnt/user-data/uploads; python3 - <<'E'
import re
t=open('10_TARGET_DATA_ARCHITECTURE_AND_ENTITY_MODEL.md',encoding='utf8').read()
print(t.count('Persisted in SQL'))
print(re.findall(r'^#{3,4} (.+)$',t,re.M)[:40])
print(t[-1500:])
E
Output

25
['4.1 Target Entity Relationship Diagram (Mermaid)', '4.2 Comprehensive Entity Dictionary (26 Core Entities)', '1. Organisation', '2. Region', '3. Venue (Site / Inn)', '4. Supplier', '5. Supplier Product', '6. Ingredient', '7. Recipe', '8. Recipe Version', '9. Recipe Ingredient (Bill of Materials)', '10. Commercial Product', '11. Menu', '12. Menu Section', '13. Menu Item', '14. Venue Offering', '15. Price', '16. Product Code / EPOS Mapping', '17. Allergen Declaration', '18. Nutrition Profile', '19. Source Document', '20. Verification Record', '21. Launch Campaign', '22. Launch Task', '23. Launch Venue Status', '24. User', '25. User Role (RBAC)', '26. Audit Event']
ATIONAL SQL DATABASE  │ TIER 2: REPOSITORY FLAT-FILE STORES│
│ Engine: SQLite 3 (WAL Mode)       │ Storage: File System Versioned     │
│ Database: icg_hospitality.sqlite3 │ • Markdown Menus (menus_md/*.md)   │
│ Tables:                           │ • Raw Crawls (kafoodie/*.json)     │
│ • venues, regions                 │ • Discovered Media CSV             │
│ • products, recipes, ingredients  │ • Rule Configs (config/*.json)     │
│ • menus, menu_sections, menu_items│ • Generated venue.json models      │
│ • venue_offerings, prices, epos   │ • Generated menu-explorer-data.js  │
│ • allergens, nutrition            │ • Original PDF Documents           │
│ • launches, launch_tasks          │                                    │
│ • issue_reviews (from prototype)  │                                    │
│ • audit_events (append-only)      │                                    │
└───────────────────────────────────┴────────────────────────────────────┘
```

* **SQLite in WAL (Write-Ahead Logging) Mode**: Provides zero-maintenance, zero-configuration local ACID persistence. Ideal for local multi-threaded Python server access. Capable of supporting millions of rows with sub-millisecond query execution.
* **Migration Boundary**: SQLite serves as the target operational database for Phases 1–3. A transition to PostgreSQL is recommended only when multi-user concurrent remote editing, enterprise SSO integration, or multi-region database clustering becomes an active requirement (Phase 4).

- working on menu-review.html (Inn Collection Group menu review UI, served locally by menu_review_server.py at 127.0.0.1:8000, sibling page discovered-media.html)
The documents are mostly sound, but the multi-computer question is the biggest hole: none of the docs decide it, and the plan quietly assumes both answers. I changed nothing.

I read all 15 docs, the tree, menu_review_server.py and the SQLite file. I have not seen the build scripts, the pages/*.html files, config/*.json, or the two specs, so any “code-verified” claim about those is taken from your docs, not re-checked by me.

What I verified myself
The server binds to 127.0.0.1 by default, but it has a --host flag and no authentication. Anyone who starts it with --host 0.0.0.0 exposes the endpoint that rewrites menu files.
The database has one table and one row, as documented.
Correction: its journal mode is delete, not WAL. WAL is only a proposal in docs 10 and 15.
The server uses tuple[Path, ...] annotations, so it needs Python 3.9 or later, not the 3.8+ the docs state.
Problems in the docs
Deployment is undecided and the docs contradict themselves.
Doc 06 calls access control “unnecessary during local single-user”.
Doc 11 plans cookie sessions and roles for six or more people (chef, compliance officer, commercial manager).
Doc 10 defers Postgres to “multi-user remote editing”, which is exactly what that role list implies.
Venue and requirement counts disagree.
Venues: doc 15 says 29 and also “29–31”; docs 01 and 04 say 31.
Requirements: doc 03 says the cross-check holds “100+” requirements, while docs 09 and 13 say 40.
Doc 15 claims “14 core tables”, but doc 10 defines 26 entities.
Docs 13–15 use evidence tags outside the standard key (Runtime-tested, File-verified, Data-verified).
Several claims are untested. These are “sub-50ms”, “sub-millisecond”, and the week-by-week timelines in doc 14.
Doc 14 adds WeasyPrint while the architecture is described as zero-dependency. That is acceptable, but it should be stated.
The orphan list is incomplete. The tree shows more duplication in pages/: pages/documents/extracted-to-md/ (about 100 PDFs), pages/discovered_media.csv, menus.json, a stray Menu explorer — Inn Collection Group.html, and index.html. Docs 01 and 03 also say “seven interfaces”, which is out of date.
Other repository clutter. exports/TestRegion/ is leftover test data. There are two overlapping doc sets (docs/architecture/01–10 and docs/capability-assessment/). There is also root.tree.md alongside root_tree.md.
The most important issue is scope. Doc 10 makes this platform the master for recipes, ingredient BOMs, allergen declarations and COGS. Kafoodie already holds recipes and allergens. Building a second allergen master next to it is a food-safety liability, and the docs never ask whether to do it. Docs 06 and 08 rightly defer allergen policy to the business, but docs 14 and 15 then plan the engine anyway.
The multi-computer question
SQLite is fine for several computers if exactly one server process owns the file and everyone else uses a browser. It breaks if computers open the .sqlite3 file from a shared drive (SMB or NFS), because locking and WAL are unreliable there. Syncing separate copies by folder sync or git also fails, because the database and .md files diverge.

So there are three options:

A. Single user, local. This is what you have now, with no changes.
B. One shared internal host. A small VM or always-on machine runs the server, and everyone else uses a browser over the LAN or VPN. This is what I recommend.
C. A copy on each computer. I reject this one.
I would move to Postgres only if you need more than one server process, or hosting outside your network. The docs’ Phase 4 trigger is right, but it should be worded that way.

Proposed architecture (option B)
One modular monolith, one process. Keep the standard-library Python server, but split it into modules: routing, services, db, and jobs.
Four data zones, with code kept separate from data.
Source: PDFs, crawls, CSV. Never edited.
Working: the .md menus and config.
Generated: venue.json, explorer data and exports. Rebuildable, so kept out of git.
State: SQLite.
All of it lives under one configurable data/ root.
SQLite in WAL mode on a local disk, with a busy timeout, schema migrations and a nightly .backup.
A rebuild job with a lock. Menu Review triggers build_venue_export.py through this job, so two people can’t rebuild at once. The job reports its status through an endpoint.
UIs read from the API, not from hardcoded data or static bundles.
Minimal authentication before the server is bound to the LAN. Use per-user logins, record the user on every write, and add roles later.
Explicit scope boundary. This platform owns menu QC, dish-to-recipe reconciliation, gap registers, launch tracking, media, and later the EPOS mapping. Recipe BOM, the allergen master and COGS stay out until you decide Kafoodie’s role. At most the platform would hold a read-only mirror of Kafoodie’s allergen data, flagged as unverified when unset.
Core entities now: Region, Venue, Menu, Section, Item, Venue Offering, Price, Source Document, Review, Launch Campaign/Task/Venue Status, User, Audit Event. Supplier, Ingredient, Recipe, BOM, Allergen and Nutrition entities wait for the Kafoodie decision.
What’s next
Decide five things: the deployment option, the Kafoodie boundary, how Kafoodie data arrives (crawl, export or API), the EPOS vendor, and the deletions (pages/menus_md/, the duplicated PDFs and CSV, the test folder).
Fix the docs: correct the items above, then merge everything into three living documents (ARCHITECTURE.md, DECISIONS.md as a decision log, and ROADMAP.md). Archive docs 07 and 08 as audit history.
Build order after sign-off:
Repository and data-root cleanup, then database migrations, WAL and backup.
Rebuild job with the lock (closes the review-to-export loop).
API endpoints for products and venues, then rewire product-data.html.
Launch-task persistence, then authentication.
Everything else is gated on the Kafoodie decision.
Files I’d like before writing this up
build_venue_export.py and build_menu_explorer.py
pages/menu-review.html, product-data.html and launch-readiness.html
config/*.json and requirements.txt
docs/MENU-MD-SPEC.md and VENUE-EXPORT-SPEC.md
PROJECT-REVIEW/05.1 (the Phase 2 mandate)
Question for you: how many people, on how many computers, will use this, and is there an office machine or server that could stay on and host it?

build_menu_explorer.py
build_menu_explorer.py
PY
build_venue_export.py
build_venue_export.py
PY
discovered-media.html
discovered-media.html
HTML
fnb-crosscheck.html
fnb-crosscheck.html
HTML
index.html
index.html
HTML
launch-readiness.html
launch-readiness.html
HTML
menu-explorer-data.js
menu-explorer-data.js
JS
menu-explorer.html
menu-explorer.html
HTML
menu-review.html
menu-review.html
HTML
product-data.html
product-data.html
HTML
01_PROJECT_OVERVIEW.md
01_PROJECT_OVERVIEW.md
122 lines
MD
02_EXISTING_SYSTEM_INVENTORY.md
02_EXISTING_SYSTEM_INVENTORY.md
182 lines
MD
03_INFORMATION_ARCHITECTURE.md
03_INFORMATION_ARCHITECTURE.md
132 lines
MD
04_WORKFLOW_MAP.md
04_WORKFLOW_MAP.md
162 lines
MD
05_COMPONENT_RELATIONSHIPS.md
05_COMPONENT_RELATIONSHIPS.md
115 lines
MD
06_WORKSPACE_PROPOSAL.md
06_WORKSPACE_PROPOSAL.md
133 lines
MD
07_ARCHITECTURAL_GAPS.md
07_ARCHITECTURAL_GAPS.md
76 lines
MD
08_AI_AUTOMATION_OPPORTUNITIES.md
08_AI_AUTOMATION_OPPORTUNITIES.md
78 lines
MD
09_IMPLEMENTATION_STATUS.md
09_IMPLEMENTATION_STATUS.md
62 lines
MD
10_NEXT_STAGE_RECOMMENDATIONS.md
10_NEXT_STAGE_RECOMMENDATIONS.md
129 lines
MD
Right. I'm not sure if you're taking the mic out of me because that question was exactly what annoyed me from ChatGPT. How many computers? Probably just one, maybe more than one. Server? Yes, anything is possible. Right, can you review the remaining? And then let's decide what we need to do.

Checking the build scripts, page code and data file
Thought for 2s

Dropping the question and picking a default for any number of machines.

Checking the build scripts, page code and data file.

Understood, no more questions on that. I’ll design it to work for one computer now and more later. Reviewing the remaining files now.

Ran 4 commands
I’ve finished reviewing the rest. The architecture is decided below with defaults that work for one computer or several, so I won’t ask about computers again. Nothing has been changed.

Corrections from the code
Requirement count: fnb-crosscheck.html holds about 40 requirements, not “100+”. Docs 03 and 09, and the old doc 02, repeat the wrong number.
Explorer data size: menu-explorer-data.js is 9.0 MB, not about 3 MB. It does hold 29 venues.
Duplicate page: index.html is byte-identical to menu-explorer.html. The docs say it redirects, so it is another copy that can drift.
HTML line counts are wrong across the docs. For example, launch-readiness.html is 134 lines against the 710 claimed, and product-data.html is 160 against 820. File sizes are fine, so drop line counts from the docs and keep file sizes.
Review state lives in two places. menu-review.html also saves it in the browser’s localStorage (“Saved in this browser”), as well as in SQLite. With a second computer the two copies diverge silently. This is the real multi-computer bug, and doc 09 only half-noted it.
Good news for multiple computers: both build scripts find their files relative to their own location (ROOT = Path(__file__).parent), and venue.json stores relative paths. Nothing is tied to your machine, so the code is already portable.
The review-to-export loop is cheap to close. build_venue_export.py --venue <name> already exists, so a rebuild hook is a short subprocess call with no refactor.
The old docs (docs/architecture/01–10) are superseded. They still describe Netlify, say 104 menu files (it is 103), and call venue.json the “single source of truth”, which doc 08 later withdrew. They also give a 4-week roadmap that conflicts with doc 14’s 12+ weeks. Archive them. The only parts worth keeping are the 5-domain navigation idea (old 06), the AI-advisory principle (old 08), and the staging logic of old 10.
Decisions, with my recommended defaults
#	Decision	Recommendation
D1	Topology	One server process owns all data. Everyone else uses a browser. The same code runs on localhost today and on a shared machine later, switched by --host. Never sync copies between computers.
D2	Database	Stay on SQLite, switched to WAL mode and kept on the host’s local disk. Move to Postgres only if you ever need several server processes or off-site hosting.
D3	Browser storage	Use localStorage only for UI preferences. Review state is stored on the server only.
D4	Data layout	Keep the current layout for now, but add one configurable data root. Four zones: source, working, generated (rebuildable, not in git) and state.
D5	Rebuilds	A server job runs build_venue_export.py --venue after a menu is fixed. It uses a lock and reports its status. It writes venue.json atomically.
D6	Security	Before the server listens on anything beyond localhost, add a simple login and record the user on every write. Full roles come later.
D7	Scope	Kafoodie stays the master for recipes and allergens. We do not build a recipe BOM, allergen engine or COGS now. This platform owns menu QC, reconciliation, gap registers, launch tracking, media, and later EPOS mapping.
D8	Netlify	Gone for good. No public hosting.
D9	Backups	Nightly SQLite .backup, with the menus and config in git.
D10	AI	Advisory only, always staged for human approval, and later in the plan.
What’s next
Documentation (first, before code). Merge everything into three living files:
ARCHITECTURE.md covers current state, target state, and the topology above.
DECISIONS.md is a decision log. D1–D10 go in as proposed, and the allergen-publication rule and the two missing Kafoodie venues stay open.
ROADMAP.md is a single roadmap replacing the two conflicting ones.
Docs 07 and 08 and the old set move to an archive/ folder. I’ll also fix the corrections above in the files that stay.
Build order.
Step 1: repository hygiene (delete the orphaned copies once you confirm), the data root setting, and moving review state off the browser.
Step 2: WAL mode, a migration mechanism, and the backup.
Step 3: the rebuild job, which closes the review-to-export loop.
Step 4: API endpoints that read venue.json, with product-data.html rewired to them.
Step 5: launch tracking saved in SQLite, then the simple login.
After that: the recipe, allergen and costing work, gated on D7.
Still outstanding on your side:
Confirm the deletions: pages/menus_md/, pages/documents/, the duplicate CSV and index.html, and exports/TestRegion/.
Get outlet IDs for Dean Court and The Bull’s Head Inn.
These don’t block step 1.
Reply “approved” to take D1–D10 as written, or name the ones you want changed, and I’ll write the three documents.


You are out of free messages until 1:50 PM


Claude is AI and can make mistakes. Please double-check responses.
Claude finished the response
