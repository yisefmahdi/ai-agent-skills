---
name: project-onboarding
description: Use at the start of any project — the very first message, or whenever project-structure.md does not yet exist in the workspace. Also use whenever a task references "the project", asks to build/add/fix/refactor something, mentions routes/controllers/models/database/schema/folder structure, or whenever you are about to guess a file path, naming convention, tech stack detail, database column, route, or workflow preference instead of checking the record or the actual files. This covers detecting a brand-new empty project vs an existing codebase, an adaptive interview whose questions depend on project type (web, mobile, API/backend, CLI/script, data-ML, other), building and maintaining a single project-structure.md file as the project's permanent, deep architectural memory (full folder tree, routes tables, controllers/models list, database schema with columns and relationships, data-flow diagrams, and multi-step build/migration plans — not just a shallow summary — while never splitting into separate module files; everything stays as sections within the one file), token-efficient reading rules (search vs full-read, reading only the relevant section by heading instead of the whole file), detecting drift between the documented context and the real codebase, and periodic cleanup so the file doesn't grow stale or bloated. Trigger this even if the user never says "skill" or "onboarding" — any first interaction with an undocumented project, or any moment of uncertainty about project facts, should trigger it.
---

# Project Onboarding & Structural Memory Skill

The goal of this skill: every project — empty or with existing code — gets a **deep, comprehensive architectural document** at `project-structure.md` in the project root, not just a shallow summary. The point is that any developer (or the agent itself, in a brand-new session) can read this one file and fully understand the project: the complete folder structure, routes, controllers and models, the full database schema with columns and relationships, data flow between parts, and even in-progress multi-step build plans. Every later interaction relies on this memory instead of re-asking the same questions or guessing facts about the project.

**Hard constraint: the only persistent file this skill produces is `project-structure.md`.** Do not create separate module files, config files, JSON, or scripts — everything related to project memory is written inside this single file, organized into clear sections and sub-headings, no matter how large or detailed the project gets.

---

## Step Zero: always check state first

Before responding to or executing any task in the project, follow this order:

```
1) Does project-structure.md exist in the project root?
   ├─ Yes → jump to "Efficient Reading" and start work directly (skip onboarding entirely)
   └─ No  → continue to step 2

2) Is the folder actually empty, or does it just contain placeholder files (empty README, etc.)?
   ├─ Empty        → "New Project Path" (below)
   └─ Has real code → "Existing Project Path" (below)
```

Never assume either case — actually inspect the project root before deciding.

---

## Path A: New Project (empty)

### Step 1 — Classification question

Ask one question first: **"What type of project is this?"** with options: Web / Mobile / API-backend / CLI or automation script / Data-ML / Other.

### Step 2 — Branching interview by type

Ask in small batches (2-3 questions at a time), never all at once. Use the appropriate track below:

**Web App:**
- Batch 1 (architecture): Frontend framework? Backend language/framework? Database?
- Batch 2 (deployment): Where will it be deployed? Multiple environments (dev/staging/prod)?
- Batch 3 (workflow): Plan before execution, or direct implementation? Fixed code style?

**Mobile App:**
- Batch 1: Native or cross-platform? Target platform (iOS/Android/both)?
- Batch 2: Separate backend? State management library?
- Batch 3: Plan before execution? Platform-specific constraints?

**API / Backend:**
- Batch 1: Language and framework? REST or GraphQL?
- Batch 2: Database and ORM? Expected auth system?
- Batch 3: Preferred folder structure (MVC, feature-based)? Security/performance constraints?

**CLI / automation script:**
- Batch 1: Language? Exact automation goal?
- Batch 2: Target OS? Distribution method (script, package, binary)?
- Batch 3: Desired level of implementation detail?

**Data / ML:**
- Batch 1: Data source? Approximate data size?
- Batch 2: Goal (analysis, visualization, model training)? Expected libraries?
- Batch 3: Output format? Data-quality/privacy constraints?

**Other / custom:**
Ask manually: What is the project and its goal? What tools are used? Preferred workflow and any constraints?

### Step 3 — Never assume

Never assume an answer to any question. If the user answers vaguely, ask a short, specific follow-up.

### Step 4 — Build the file

Actually create `project-structure.md` in the project root, based on the "File Template" below. Show a short summary and ask "Is this correct and complete?" before any real implementation begins.

---

## Path B: Existing Project (has code already, but no project-structure.md)

The key difference here: **scan the project itself first**, because the code is a more accurate source of truth than guessing.

### Detection files table — check for these first

| File present | Indicates | Extract from it |
|---|---|---|
| `package.json` | JS/TS project | Name, dependencies, scripts, framework |
| `requirements.txt` / `pyproject.toml` | Python project | Libraries, Python version |
| `Cargo.toml` | Rust project | Name, dependencies |
| `composer.json` | PHP project | Framework (Laravel...), dependencies |
| `*.csproj` / `*.sln` | C#/.NET project | Target framework |
| `pom.xml` / `build.gradle` | Java/Kotlin project | Dependencies, build tool |
| `Gemfile` | Ruby project | Framework (Rails...) |
| `docker-compose.yml` / `Dockerfile` | Defined runtime environment | Linked services (database, cache) |
| `.env.example` | Expected environment variables | Variable names only (no sensitive values) |
| `.git` + recent commits | Project activity | Whether active, what was last touched |

### Scanning steps

1. List the project root and note which detection files are present.
2. Open each detection file found and extract the essential info only (don't read individual code files at this stage).
3. Inspect the general folder structure (one or two levels, not every file).
4. Summarize for the user in a short paragraph: "Here's what I understood from scanning the project: [...]. Correct? Anything missing or wrong?"
5. Never assume everything in the code is "intentional" or "current" — automated detection is a starting point for confirmation, not final truth.

### When to stop auto-extracting and ask directly

- Workflow preferences (plan before execution, explanation level) — code never states this
- Intentional architectural decisions not obvious from the files alone
- Constraints or "don't do this" rules that aren't written anywhere
- Conflicts in auto-detection (e.g. both React and Vue present — ask why)

### Building the file

Build `project-structure.md` from a mix of: (auto-detected facts confirmed by the user) + (direct answers for what the code can't answer).

---

## File Template (project-structure.md)

This template is **deep and detailed**, not a shallow summary. The goal is for the file to function as a complete architectural document — a new developer reading it should understand the project without opening a single code file. Don't settle for vague sentences ("there's a user system") — write the actual details (column names, route names, controller names) as soon as you know them, whether from auto-detection or from the user.

Not every section needs to be filled in on the first onboarding. Build the full skeleton from the start, fill in the sections you have information for, and leave the rest as "not built yet" until the project grows. Update sections progressively as features actually get added.

```markdown
# [Project Name]

## 1. Overview
- Description: ...
- Project type: (Web / Mobile / API / CLI / Data-ML / Other)
- Goal / end user: ...
- Tagline / brief identity (if any): ...

## 2. Tech Stack
- Backend: language/framework/version
- Frontend: framework or approach (Blade, React, Vue...)
- Database: type
- Key tools and libraries: ...
- Deployment environment (if known): ...

## 3. Full Folder Structure
> Write the actual full folder tree (like the VEXA example), not a general description. Update it whenever an important new folder or file is added.

```
project/
├── ...
```

## 4. Visual Identity / Design System (if applicable)
- Primary colors (hex codes)
- Fonts
- Design style (dark mode, minimal, etc.)
- Main CSS/theme files and their location

## 5. Preferred Workflow
- Plan before execution, or direct implementation? ...
- Required explanation level: ...
- Naming conventions / code style: ...
- Versioning and git workflow (branches, commit convention)

## 6. Rules & Gotchas
- Never: ...
- Always: ...
- Mistakes that happened before and were avoided: ...
- Files not to touch (if any sensitive or external parts must stay as-is)

## 7. Sections & Pages / Main Features
> A table for every actual section of the project (page, feature, screen) with its details. Update this table as soon as a new feature is added.

| # | Section | Path/Page | Description & Details |
|---|---------|-----------|------------------------|
| 1 | ... | `/...` | Responsible Controller@method + precise explanation of what actually happens |

## 8. Complete Routes
> A table for every actual route in the project. Update it immediately whenever a new route is added.

| Method | URI | Name/Handler | Middleware/Auth |
|--------|-----|--------------|------------------|
| ... | ... | ... | ... |

## 9. Database Schema
> For each table: columns, types, description. This is one of the most important sections — it must be 100% accurate since it underlies any future data change.

### Table: `...`
| Column | Type | Description |
|--------|------|--------------|
| ... | ... | ... |

## 10. Models/Entities & Relationships
```
Model (1) ──→ Model (1:N)
```
| Model | Table | Relationships |
|-------|-------|----------------|
| ... | ... | ... |

## 11. Controllers / Core Business Logic
| Controller/Module | Main Methods | Purpose |
|---------------------|---------------|---------|
| ... | ... | ... |

## 12. Data Flow
> A simple text diagram showing how data moves between the main parts (e.g. Frontend → API → DB → display result). Update it whenever an important flow changes.

```
[Source] → [Processing] → [Storage] → [Display]
```

## 13. Active Build Plans
> Any in-progress, multi-step implementation plan (e.g. integrating an external API, a feature under construction). Once a plan is fully implemented, move it to "Changelog" below and remove it from here.

### Plan: [Plan Name]
- **Goal:** ...
- **Steps:**
  1. ...
  2. ...
- **Expected new files:** ...
- **Expected modified files:** ...
- **Current status:** (Not started / In progress on step X / Done)

## 14. Changelog
- [Date] — [What changed and why]
```

---

## Efficient Reading (reducing token usage)

Since project-structure.md is now a deep, detailed document (14 sections), reading only the relevant sections is what actually makes this skill save tokens instead of wasting them:

- **Don't read the whole file** except the first time in a new conversation (to build a general picture), or when the task is genuinely comprehensive (a full review, a large refactor).
- For a specific task, read only the related section: editing a route → read section "8. Routes"; changing the database → section "9. Database Schema"; a question about workflow style → section "5", etc. Use a specific line range or search (grep) for the section number/name instead of opening the whole file.
- For actual code files (not project-structure.md): if the task is searching for a specific function/symbol → use grep/search instead of opening and reading every file in full. Only read a file in full if you're actually going to edit it or need to fully understand its logic.

---

## Updating During Active Work (the most important section in this skill)

This is what separates a file that "gets written once and goes stale" from one that's "actually alive and trustworthy." The rule:

**Before any real implementation (writing code, adding a feature, changing structure):**
1. Read the relevant sections of project-structure.md (Routes, Database Schema, Controllers as needed)
2. If the task is large or multi-step (e.g. integrating an external API, adding a full system), write its plan first in section "13. Active Build Plans" **before starting implementation** — exactly like the VEXA example (the problem, the steps, expected new/modified files)
3. Show the plan to the user for confirmation if it's large or involves architectural decisions

**During and after implementation:**
4. Any new route → add it immediately to table "8. Complete Routes"
5. Any new column or table in the database → add it immediately to section "9. Database Schema"
6. Any new Controller or method → add it to table "11. Controllers"
7. Any new folder or important file in the structure → update "3. Full Folder Structure"
8. Any new decision or constraint discovered during work → add it to "6. Rules & Gotchas"
9. Once a large plan (section 13) is fully implemented → move a one-line summary to "14. Changelog" and remove it from section 13

**Don't delay the update until the end of the conversation or wait for the user to ask** — update the file as soon as the change actually happens in the code, in the same response that contains the implementation. This way, any new conversation — or even the same conversation later — finds the file reflecting the real current state, not a stale snapshot.

---

## The "If You Don't Know — Check, Don't Guess" Rule

The single most important rule in this entire skill. Any decision (naming, structure, where new code goes, a design preference) not explicitly documented in project-structure.md:

1. Search the actual project (grep/search) — the answer might exist as a repeated pattern in the code.
2. If no clear answer is found, **ask the user** — a short, specific question, not a general one.
3. Whatever answer you arrive at (from the code or from the user), **update it immediately** in the relevant section of project-structure.md, so the same question doesn't get asked again in a future conversation.

Never assume a "logical" answer and proceed with implementation if the decision affects structure, naming, or architecture.

---

## Drift Detection

Every time you read project-structure.md in full (e.g. at the start of a new conversation), quickly compare what's documented (stack, folder structure) against what's actually observed in the current project (an unexpected new file, a new library in the dependency file).

If you notice a clear conflict:
- Don't silently fix it or ignore it
- Tell the user in one short sentence: "I noticed [X] has changed from what's documented in the file — should I update it?"
- After confirmation, update project-structure.md directly

---

## Expanding Sections (when a specific part of the project grows)

The template above has 14 fixed sections. If a particular part grows a lot (e.g. 15+ routes or 10+ database tables), **don't create a separate file** — just organize within the same section using smaller sub-headings (### by feature or module name) to make partial reading via search (grep) easier later.

Example: if "9. Database Schema" grows to twenty tables, keep it in the same section but order the tables logically (users → subscriptions → transactions → settings) so searching for a specific table stays fast.

---

## Periodic Maintenance (preventing bloat and staleness)

Whenever you have a reason to read project-structure.md in full:

- If you find outdated or duplicated information in more than one place → merge it or remove the duplication
- If section "6. Rules & Gotchas" or any sub-section has grown long without adding value → summarize and trim it, without losing important information, and keep it inside the same file
- Since the file is now a deep architectural document (like the VEXA example, which can run to hundreds of lines), large size is normal and expected — the problem isn't length, it's duplication or stale information. Watch for that instead of just watching the line count.
- Section "13. Active Build Plans" specifically must stay clean — any plan that's fully implemented gets moved as a one-line summary to "14. Changelog" and removed from section 13, so no forgotten stale plans linger.

---

## Closing Note

The "Updating During Active Work" section above is the primary reference for all update rules. The core idea repeated throughout this skill: **project-structure.md is the permanent memory, not the conversation** — any information worth remembering must reach the file immediately when discovered, not just get mentioned in the current response and lost.
