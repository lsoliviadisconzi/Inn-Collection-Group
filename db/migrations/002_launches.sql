-- Migration 002: Launch campaigns, tasks, and venue readiness
CREATE TABLE IF NOT EXISTS launch_campaigns (
    id          TEXT PRIMARY KEY,
    name        TEXT NOT NULL,
    launch_date TEXT NOT NULL,
    as_of_date  TEXT NOT NULL,
    created_at  TEXT NOT NULL,
    updated_at  TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS launch_milestones (
    campaign_id TEXT NOT NULL REFERENCES launch_campaigns(id) ON DELETE CASCADE,
    name        TEXT NOT NULL,
    target_date TEXT NOT NULL,
    sort_order  INTEGER NOT NULL DEFAULT 0,
    PRIMARY KEY (campaign_id, name)
);

CREATE TABLE IF NOT EXISTS launch_workstreams (
    campaign_id   TEXT NOT NULL REFERENCES launch_campaigns(id) ON DELETE CASCADE,
    workstream_id TEXT NOT NULL,
    name          TEXT NOT NULL,
    owner         TEXT NOT NULL,
    due_date      TEXT NOT NULL,
    gate          TEXT NOT NULL,
    sort_order    INTEGER NOT NULL DEFAULT 0,
    PRIMARY KEY (campaign_id, workstream_id)
);

CREATE TABLE IF NOT EXISTS launch_tasks (
    campaign_id   TEXT NOT NULL,
    workstream_id TEXT NOT NULL,
    task_id       TEXT NOT NULL,
    title         TEXT NOT NULL,
    status        TEXT NOT NULL DEFAULT 'todo',
    owner         TEXT NOT NULL,
    note          TEXT NOT NULL DEFAULT '',
    updated_at    TEXT NOT NULL,
    updated_by    TEXT NOT NULL DEFAULT '',
    PRIMARY KEY (campaign_id, workstream_id, task_id)
);

CREATE TABLE IF NOT EXISTS launch_venue_status (
    campaign_id   TEXT NOT NULL,
    venue_name    TEXT NOT NULL,
    region        TEXT NOT NULL,
    workstream_id TEXT NOT NULL,
    status        TEXT NOT NULL DEFAULT 'todo',
    updated_at    TEXT NOT NULL,
    updated_by    TEXT NOT NULL DEFAULT '',
    PRIMARY KEY (campaign_id, venue_name, workstream_id)
);

-- Seed baseline Spring 2027 campaign
INSERT OR IGNORE INTO launch_campaigns (id, name, launch_date, as_of_date, created_at, updated_at)
VALUES ('spring-2027', 'Spring menu 2027', '2027-03-01', '2027-02-08', datetime('now'), datetime('now'));

INSERT OR IGNORE INTO launch_milestones (campaign_id, name, target_date, sort_order) VALUES
('spring-2027', 'Products locked', '2027-01-22', 1),
('spring-2027', 'EPOS configured', '2027-02-15', 2),
('spring-2027', 'Spec books to sites', '2027-02-22', 3),
('spring-2027', 'Launch', '2027-03-01', 4);

INSERT OR IGNORE INTO launch_workstreams (campaign_id, workstream_id, name, owner, due_date, gate, sort_order) VALUES
('spring-2027', 'MEN', 'Menus', 'F&B team', '2027-01-29', 'Every dish has a description, section and allergens, and F&B has approved the menu.', 1),
('spring-2027', 'REC', 'Recipes', 'F&B team', '2027-02-05', 'Every dish has a recipe card with yield, portion weight and costed ingredients.', 2),
('spring-2027', 'PRI', 'Pricing', 'Finance', '2027-02-10', 'Sell price, VAT and GP are set for each product, and Finance has signed off.', 3),
('spring-2027', 'SYS', 'Systems', 'Coordinator', '2027-02-15', 'Every product has a code, a record and mapped supplier items in the food data platform.', 4),
('spring-2027', 'POS', 'POS setup', 'Coordinator', '2027-02-19', 'Menu structure, prices and promotions are built, tested and released to sites.', 5),
('spring-2027', 'INF', 'Product information', 'Coordinator', '2027-02-17', 'Each product has allergen and nutrition sheets and a spec-book page.', 6),
('spring-2027', 'TRN', 'Training materials', 'Operations', '2027-02-24', 'Site teams have briefing, tasting notes and a short check before launch.', 7),
('spring-2027', 'COM', 'Launch communications', 'Coordinator', '2027-02-22', 'Every site has the launch brief, spec book, timings and field-team contact.', 8);

-- Seed tasks for Menus workstream
INSERT OR IGNORE INTO launch_tasks (campaign_id, workstream_id, task_id, title, status, owner, note, updated_at, updated_by) VALUES
('spring-2027', 'MEN', '0', 'Dish list locked', 'done', 'F&B', '', datetime('now'), 'system'),
('spring-2027', 'MEN', '1', 'Descriptions approved', 'done', 'F&B', '', datetime('now'), 'system'),
('spring-2027', 'MEN', '2', 'Drinks list locked', 'track', 'F&B', '', datetime('now'), 'system'),
('spring-2027', 'MEN', '3', 'Allergen matrix signed off', 'risk', 'F&B', 'Two dishes have no allergen entry', datetime('now'), 'system'),
('spring-2027', 'MEN', '4', 'Menu artwork proofed', 'todo', 'Marketing', '', datetime('now'), 'system');

-- Seed tasks for Recipes workstream
INSERT OR IGNORE INTO launch_tasks (campaign_id, workstream_id, task_id, title, status, owner, note, updated_at, updated_by) VALUES
('spring-2027', 'REC', '0', 'Recipe cards written', 'track', 'F&B', '', datetime('now'), 'system'),
('spring-2027', 'REC', '1', 'Yields and portion weights confirmed', 'track', 'F&B', '', datetime('now'), 'system'),
('spring-2027', 'REC', '2', 'Ingredient costs from Procurement', 'risk', 'Procurement', 'Four items still unpriced', datetime('now'), 'system'),
('spring-2027', 'REC', '3', 'Nutrition calculated', 'todo', 'F&B', '', datetime('now'), 'system'),
('spring-2027', 'REC', '4', 'Prep standards photographed', 'todo', 'Operations', '', datetime('now'), 'system');

-- Seed tasks for Pricing workstream
INSERT OR IGNORE INTO launch_tasks (campaign_id, workstream_id, task_id, title, status, owner, note, updated_at, updated_by) VALUES
('spring-2027', 'PRI', '0', 'Target GP agreed', 'done', 'Finance', '', datetime('now'), 'system'),
('spring-2027', 'PRI', '1', 'VAT rates checked', 'done', 'Finance', '', datetime('now'), 'system'),
('spring-2027', 'PRI', '2', 'Sell prices set', 'track', 'Commercial', '', datetime('now'), 'system'),
('spring-2027', 'PRI', '3', 'Site price variants', 'todo', 'Commercial', '', datetime('now'), 'system'),
('spring-2027', 'PRI', '4', 'Finance sign-off', 'todo', 'Finance', '', datetime('now'), 'system');

-- Seed tasks for Systems workstream
INSERT OR IGNORE INTO launch_tasks (campaign_id, workstream_id, task_id, title, status, owner, note, updated_at, updated_by) VALUES
('spring-2027', 'SYS', '0', 'Product codes assigned', 'done', 'Coordinator', '', datetime('now'), 'system'),
('spring-2027', 'SYS', '1', 'Product records created', 'track', 'Coordinator', '', datetime('now'), 'system'),
('spring-2027', 'SYS', '2', 'Supplier items mapped', 'block', 'Procurement', 'Waiting on supplier item codes', datetime('now'), 'system'),
('spring-2027', 'SYS', '3', 'Food data platform updated', 'todo', 'Coordinator', '', datetime('now'), 'system');

-- Seed tasks for POS setup workstream
INSERT OR IGNORE INTO launch_tasks (campaign_id, workstream_id, task_id, title, status, owner, note, updated_at, updated_by) VALUES
('spring-2027', 'POS', '0', 'Menu structure built', 'track', 'Coordinator', '', datetime('now'), 'system'),
('spring-2027', 'POS', '1', 'Modifiers and promotions configured', 'todo', 'Coordinator', '', datetime('now'), 'system'),
('spring-2027', 'POS', '2', 'Test transactions run', 'todo', 'Coordinator', '', datetime('now'), 'system'),
('spring-2027', 'POS', '3', 'Pre-release QA passed', 'todo', 'Coordinator', '', datetime('now'), 'system'),
('spring-2027', 'POS', '4', 'Released to sites', 'todo', 'EPOS provider', '', datetime('now'), 'system');

-- Seed tasks for Product information workstream
INSERT OR IGNORE INTO launch_tasks (campaign_id, workstream_id, task_id, title, status, owner, note, updated_at, updated_by) VALUES
('spring-2027', 'INF', '0', 'Guest descriptions written', 'done', 'Marketing', '', datetime('now'), 'system'),
('spring-2027', 'INF', '1', 'Allergen and nutrition sheets', 'risk', 'F&B', 'Waiting on nutrition figures', datetime('now'), 'system'),
('spring-2027', 'INF', '2', 'Spec books drafted', 'track', 'Coordinator', '', datetime('now'), 'system'),
('spring-2027', 'INF', '3', 'Product knowledge cards', 'todo', 'F&B', '', datetime('now'), 'system');

-- Seed tasks for Training materials workstream
INSERT OR IGNORE INTO launch_tasks (campaign_id, workstream_id, task_id, title, status, owner, note, updated_at, updated_by) VALUES
('spring-2027', 'TRN', '0', 'Tasting notes', 'todo', 'F&B', '', datetime('now'), 'system'),
('spring-2027', 'TRN', '1', 'Prep steps and video', 'todo', 'Operations', '', datetime('now'), 'system'),
('spring-2027', 'TRN', '2', 'Server briefing', 'todo', 'Operations', '', datetime('now'), 'system'),
('spring-2027', 'TRN', '3', 'Team quiz', 'todo', 'Operations', '', datetime('now'), 'system');

-- Seed tasks for Launch communications workstream
INSERT OR IGNORE INTO launch_tasks (campaign_id, workstream_id, task_id, title, status, owner, note, updated_at, updated_by) VALUES
('spring-2027', 'COM', '0', 'Launch brief to sites', 'done', 'Coordinator', '', datetime('now'), 'system'),
('spring-2027', 'COM', '1', 'Field team call scheduled', 'done', 'Operations', '', datetime('now'), 'system'),
('spring-2027', 'COM', '2', 'Timings and checklist', 'track', 'Coordinator', '', datetime('now'), 'system'),
('spring-2027', 'COM', '3', 'Marketing assets aligned', 'track', 'Marketing', '', datetime('now'), 'system'),
('spring-2027', 'COM', '4', 'Spec books sent to sites', 'todo', 'Coordinator', '', datetime('now'), 'system');
