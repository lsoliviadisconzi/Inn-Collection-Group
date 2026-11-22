Agent Instructions: Next Documentation Phase

Hospitality Technology Capability Assessment — The Inn Collection Group

1. Objective

Continue developing the technical and operational documentation for the Hospitality Technology Capability Assessment.

The purpose of this phase is to move beyond individual interface reviews and progressively establish a coherent understanding of the underlying system:

* What components and capabilities exist?
* How are they implemented?
* What data do they use?
* How do the components relate to one another?
* Which workflows are implemented, and which are still conceptual?
* What architecture supports the intended operational model?
* What documentation is needed to guide the next development stage?

This is an investigative and documentation exercise. Do not prematurely redesign, refactor or expand the application.

The objective is to establish an accurate picture of the existing system before making architectural or product decisions.

⸻

2. Important Architectural Clarification: Netlify

Netlify must not be treated as part of the application’s underlying architecture.

The Netlify deployment is an independent development convenience. It was created to make individual pages accessible online so that agents could inspect, navigate and interact with the interfaces.

It is not:

* The production application.
* The authoritative data source.
* The application’s database.
* An integration layer.
* A required hosting dependency.
* Evidence of the application’s deployment architecture.

The actual application uses a SQL database.

Agents must therefore distinguish between:

Development access

* Netlify-hosted copies of interfaces.
* Temporary public access for agent inspection.
* Development and demonstration purposes.

Actual application architecture

* The application code and its real execution environment.
* The SQL database.
* Actual data models, relationships and persistence.
* Backend services, APIs and application logic.
* Existing integrations and dependencies, where verified.

Do not infer the SQL database engine, schema, hosting arrangements or connection architecture without inspecting the project.

If a Netlify page differs from the locally implemented application, the local application and its actual codebase should be treated as the primary source of truth.

Netlify can be removed without changing the intended application architecture.

⸻

3. Allergen, Food Safety and UK Regulatory Information

A substantial collection of official UK information concerning food allergens, food safety, health and safety and related regulatory requirements has already been gathered.

However, this information is not being finalised or consolidated during this documentation phase.

Do not:

* Attempt to produce a definitive allergen compliance framework.
* Rewrite or independently consolidate the regulatory research.
* Treat existing prototype allergen information as verified compliance data.
* Introduce new regulatory interpretations without being asked.
* Confuse interface fields with validated operational information.
* Allow regulatory research to distract from documenting the system’s architecture and capabilities.

For now, document where allergen, nutrition and food-safety information appears in the system, how the relevant information is represented, and what data relationships or validation mechanisms exist.

Where something remains unverified, explicitly record it as an open question.

The regulatory refinement will be a separate, controlled phase.

⸻

4. Evidence and Verification Standards

Every finding must be classified using the following distinctions:

Classification	Meaning
Observed	Directly observed through interaction with an interface.
Code-verified	Confirmed by inspecting the relevant implementation.
Database-verified	Confirmed through the actual SQL schema, records or queries.
Tested	A workflow or function was executed successfully.
Inferred	A reasonable interpretation, but not directly verified.
Proposed	A suggested capability or future design direction.
Unknown	Evidence is currently insufficient.

Do not confuse:

* A visible interface with an implemented feature.
* A documented workflow with an operational workflow.
* A field in a form with a persisted database record.
* A displayed status with an automated calculation.
* A product code with an EPOS integration.
* A menu document with an authoritative recipe specification.
* A SQL database existing with every interface being connected to it.

Where possible, verify functionality against the actual code and database rather than relying exclusively on browser-rendered content.

Do not invent data, integrations, operational outcomes or business processes.

⸻

5. Cumulative System Understanding

Use the existing assessments as the starting point. Do not restart the analysis or treat each interface as an isolated product.

The current capability map includes:

Component	Intended role	Current assessment
Discovered Media	Source-document discovery and intake	Interface and workflow described; execution requires further verification.
Menu Review	Document extraction review and quality control	Interface identified; persistence and downstream connections unverified.
Menu Explorer	Menu browsing, allergen views and venue comparison	Interface structure identified; data and functionality require verification.
Product Data	Structured product information	Explicitly labelled front-end mock-up with invented sample data.
Chicken Liver Parfait	Product-centred information and presentation	Demonstration of a connected product-information concept; underlying data connections unverified.
Launch Readiness	Multi-site launch coordination	Explicitly labelled front-end mock-up.
F&B Role Cross-check	Requirements-to-capability analysis	Static analysis tool; underlying assessment data and controls require further verification.

These components suggest a potential information lifecycle:

Discover → Review → Structure → Present → Compare → Coordinate

This is currently a conceptual relationship between components, not a verified end-to-end workflow.

The next phase must investigate whether these components actually share data, use common identifiers, depend on common services or operate independently.

Do not assume that the intended lifecycle has already been implemented.

⸻

6. Investigation Priorities

Prioritise the following areas.

A. Actual application architecture

* Identify the real application entry points.
* Identify frontend and backend technologies.
* Identify services, routes, APIs and execution dependencies.
* Identify the SQL database engine and inspect its actual schema.
* Map relevant tables, relationships, primary keys and foreign keys.
* Identify where application data is stored and how it is accessed.
* Distinguish implemented functionality from static demonstration interfaces.

B. Data architecture

Investigate the actual representation of:

* Regions and venues.
* Menus and menu documents.
* Menu sections and menu items.
* Products and recipes.
* Ingredients.
* Suppliers.
* Product identifiers and codes.
* Prices and costs, where present.
* Allergen and nutrition fields.
* Launches and readiness information.
* Review and verification statuses.

Do not assume all these entities already exist. Record what is actually present, what is partially represented and what is absent.

Pay particular attention to whether the system distinguishes:

1. A product.
2. A recipe.
3. An ingredient.
4. A menu item.
5. A venue-specific menu offering.

These are related concepts, but they are not necessarily interchangeable.

C. Component relationships

Investigate whether the components share:

* Database records.
* APIs.
* Identifiers.
* File references.
* Data models.
* Validation logic.
* Status information.

Establish which relationships are implemented, which are merely intended and which have not yet been investigated.

D. Operational workflows

Identify concrete workflows relevant to hospitality operations, including:

* Adding or updating menu information.
* Reviewing menu documents.
* Maintaining product specifications.
* Updating product prices or codes.
* Reviewing information across venues.
* Preparing a menu or product launch.
* Identifying missing information.
* Coordinating work between central teams and individual sites.

For each workflow, identify the user, inputs, actions, outputs, dependencies and current implementation status.

⸻

7. Hospitality Operational Context

Keep the assessment grounded in the actual responsibilities of an F&B Coordinator.

Relevant operational areas include:

* Menu and product administration.
* Seasonal menu changes.
* Product and recipe specifications.
* Supplier and product information.
* Pricing and product codes.
* EPOS setup and quality assurance.
* Launch preparation and coordination.
* Site communication.
* Product information and training materials.
* Food data management.
* Commercial calendars.
* Menu performance and menu engineering.

For each area, establish:

1. Whether the system currently supports it.
2. What information it would require.
3. Whether the relevant information exists in the database.
4. Whether the process is automated, assisted or manual.
5. What remains outside the system.

Do not claim that a capability exists simply because a corresponding interface or field has been designed.

⸻

8. AI and Automation

Identify opportunities only after understanding the existing data and workflows.

Potential areas for investigation include:

* Extracting structured information from menu documents.
* Detecting inconsistencies between menus and product records.
* Identifying missing or incomplete product information.
* Comparing products and menus across venues.
* Supporting launch preparation.
* Highlighting changes that affect multiple records.
* Making operational information accessible through natural-language queries.
* Reducing repetitive administrative work.

For each opportunity, explain:

* The operational problem.
* The information required.
* The proposed process.
* Where human verification remains necessary.
* Whether the current architecture could support it.
* What would need to be developed.

Do not introduce AI merely to make a process appear more advanced. Prioritise clear data, reliable workflows and useful outcomes.

⸻

9. Documentation Deliverables

Produce the next documentation set as a collection of focused, connected documents.

Document 01 — System Architecture Overview

A factual explanation of the actual application architecture, including frontend, backend, SQL database, services and dependencies.

Document 02 — Data Model and Entity Relationships

A map of the actual database entities, their relationships, identifiers and missing or ambiguous structures.

Document 03 — Component and Capability Register

A consolidated inventory of the existing interfaces and services, their intended purposes and their verified implementation status.

Document 04 — Operational Workflow Map

A practical map of the relevant hospitality workflows, identifying users, inputs, outputs, dependencies and manual interventions.

Document 05 — Integration and Dependency Register

A record of existing connections, proposed connections, missing integrations and unresolved dependencies.

Document 06 — Capability Gaps and Development Priorities

A prioritised assessment of what is missing, what needs verification, what should be improved and what should remain outside the immediate scope.

These documents must reference one another consistently. Avoid duplicating the same information in different formats.

⸻

10. Documentation Quality

The documentation must be:

* Technically accurate.
* Specific rather than generic.
* Grounded in the actual codebase and database.
* Understandable to both technical and operational stakeholders.
* Explicit about uncertainty.
* Structured around real hospitality workflows.
* Suitable for subsequent architectural and development decisions.

Use diagrams and tables where they genuinely improve understanding.

Where a diagram describes an intended architecture rather than an existing one, label it clearly as proposed.

Do not create polished diagrams that imply integrations or capabilities that have not been verified.

⸻

11. Working Method

Proceed incrementally.

1. Inspect the repository and identify the actual application structure.
2. Identify and inspect the SQL database and relevant schema.
3. Relate the previously reviewed interfaces to the actual implementation.
4. Verify the most important workflows.
5. Update the cumulative capability map.
6. Identify contradictions between documentation, interface design, code and database.
7. Produce the documentation deliverables.
8. Record unresolved questions and evidence needed to answer them.

Do not modify or delete existing functionality during this exercise.

Do not publish, deploy or submit anything.

Do not treat this documentation exercise as authorisation to redesign the application.

If a required piece of evidence is unavailable, record the limitation rather than filling the gap with assumptions.

Final Principle

The purpose is not to demonstrate how many features the system appears to have.

The purpose is to establish what the system actually knows, what it can actually do, how its components work together and how those capabilities can support people carrying out hospitality operations.

Map the reality first. Establish the structure. Then identify what should be improved or automated.