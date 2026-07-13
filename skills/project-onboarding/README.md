# Project Onboarding & Structural Memory Skill

A single-file [Agent Skill](https://agentskills.io) that turns any AI coding agent into a project onboarding assistant. On the first message in a new or existing project, it interviews you (or scans your codebase) and builds **one deep, living architecture file** — `project-structure.md` — that the agent keeps reading from and updating for the rest of the project's life.

No more re-explaining your stack, folder structure, database schema, or conventions every time you open a new chat. No more the agent guessing a file path or inventing a naming convention. It checks the record, or it asks.

## Why this exists

If you've worked with AI coding agents for a while, you've probably done this by hand already: write a markdown file describing your project, paste it into every new chat, and hope the agent doesn't forget it mid-task or contradict it later. This skill automates that entire workflow and adds guardrails around it:

- **Onboarding is automatic.** First message in an empty project → the agent asks what kind of project it is, then asks the right follow-up questions for that type (a web app gets different questions than a CLI tool or an ML pipeline).
- **Existing codebases get scanned, not just asked about.** If you drop this into a project that already has code, the agent looks for `package.json`, `requirements.txt`, `composer.json`, `Cargo.toml`, and similar files first, and only asks you about things the code can't answer (workflow preferences, undocumented constraints, intentional architecture decisions).
- **The memory file is deep, not a shallow summary.** It includes the full folder tree, routes tables, database schema with actual columns, controllers/models, data flow, and even in-progress multi-step build plans — modeled after real production architecture docs, not a two-paragraph project description.
- **It updates itself during work, not just at setup.** Add a route, a database column, a controller — the agent updates the relevant section of `project-structure.md` in the same response, not "later" or "if you ask."
- **It's one file, on purpose.** No `modules/*.md` sprawl, no config files, no JSON. Everything lives in sections inside a single `project-structure.md`, which keeps it simple to review, diff, and commit to git.
- **It's built to save tokens, not spend them.** The skill explicitly instructs the agent to read only the relevant section (by heading) instead of re-reading the whole file for every small task, and to prefer searching code over reading it in full.
- **It catches drift.** If the documented stack or structure no longer matches what's actually in the repo, the agent flags it instead of silently going along with a stale file.

## What's in this repo

```
.
├── SKILL.md      # The skill itself — this is the only file that matters functionally
└── README.md     # This file
```

That's it. `SKILL.md` is fully self-contained: the branching interview logic, the file template, the reading/writing rules, and the maintenance rules all live in one file, in plain markdown with a YAML frontmatter header.

## Installation

This skill follows the open [Agent Skills specification](https://agentskills.io), so it works across every tool that supports the standard — Claude Code, Cursor, OpenAI Codex CLI, Windsurf, Gemini CLI, and others. Installation is just "put `SKILL.md` where that tool looks for skills."

### Claude Code

Personal (all your projects):
```bash
mkdir -p ~/.claude/skills/project-onboarding
cp SKILL.md ~/.claude/skills/project-onboarding/
```

Project-scoped (shared with your team via git):
```bash
mkdir -p .claude/skills/project-onboarding
cp SKILL.md .claude/skills/project-onboarding/
```
Commit `.claude/skills/` to your repo and everyone who clones it gets the skill automatically.

### Claude.ai (web / desktop / mobile) and Claude Projects

Zip the folder containing `SKILL.md` (the zip must contain the folder itself, not just the loose file) and upload it via **Settings → Customize → Skills → Upload**. Once enabled, add it to a Project so it applies to every chat inside that project.

### Cursor

```bash
mkdir -p .cursor/skills/project-onboarding
cp SKILL.md .cursor/skills/project-onboarding/
```
(Cursor currently reads skills via manual placement — check Cursor's docs for the latest expected path in your version.)

### OpenAI Codex CLI

```bash
mkdir -p ~/.codex/skills/project-onboarding
cp SKILL.md ~/.codex/skills/project-onboarding/
```
Codex CLI may require an `--enable skills` flag depending on your version.

### Windsurf / other Agent Skills-compatible tools

Same pattern: create a `project-onboarding/` folder containing `SKILL.md` inside whatever skills directory your tool reads from (check that tool's docs for the exact path — this varies by product and changes over time).

## Usage

1. Install the skill using one of the methods above.
2. Open a new or existing project with your agent.
3. Just start working — say what you want to build, or ask the agent to fix/add something.
4. If there's no `project-structure.md` yet, the agent will:
   - Ask what type of project this is (web, mobile, API, CLI, data/ML, other)
   - Ask a small, focused set of follow-up questions based on that type
   - **If the project already has code**, scan it first (package.json, requirements.txt, etc.) and only ask about what the code can't tell it
   - Build `project-structure.md` in your project root and show you a summary to confirm
5. From then on, every conversation starts by reading that file instead of asking you again. As you build features, the agent keeps the file updated — new routes, new database tables, new controllers, and any workflow preferences or constraints you mention along the way.

You can open `project-structure.md` yourself at any time — it's a plain markdown file meant to be human-readable, reviewable, and commit-friendly.

## Design decisions worth knowing about

- **Single file, on purpose.** It would be easy to split this into `modules/auth.md`, `modules/database.md`, etc. This skill deliberately doesn't, to keep the setup dead simple (one file to install, one file to read, one file to commit) at the cost of the file growing large on bigger projects. If you prefer a modular approach, that's a reasonable fork.
- **Depth over brevity in the template.** The file template asks for actual route tables, actual column names, actual folder trees — not "there's an auth system." This is intentional: a vague summary doesn't actually prevent the agent from guessing later.
- **Plans get written before, not after.** For any multi-step build (e.g. wiring up an external API), the skill tells the agent to write out the plan in the file before touching code, so you can review the plan and so the file stays accurate even if the conversation gets interrupted mid-task.

## Contributing

Issues and PRs welcome — especially real-world examples of where the skill under-triggers, over-asks, or produces a template section that doesn't fit a project type it hasn't seen yet (e.g. embedded/firmware, game dev, infra-as-code).

## License

MIT — use it, fork it, adapt it.
