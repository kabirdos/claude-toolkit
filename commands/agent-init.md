# /agent-init — Bootstrap agent files (AGENTS.md = guidance, workflow must be read)

You are operating inside a code repository.

Authoritative file roles:

- AGENTS.md (root): open-standard, read-mostly agent guidance entry point.
- CLAUDE.md: tiny constitution, always loaded by Claude Code.
- /agent/CONSTITUTION.md: tool-agnostic mirror of the constitution.
- /agent/WORKFLOWS.md: workflow policy (Tasks, HZL, or anything else).
- /agent/MEMORY.md: append-only learnings (NOT auto-loaded).
- /agent/LEARNINGS.md: distilled promotions.
- /agent/HANDOFF.md: point-in-time session snapshot (overwritten each handoff).
- /agent/README.md: wiring notes + file roles.

Inputs:

- Use repo files available in this session.
- $ARGUMENTS: optional preferences.

Hard constraints:

1. AGENTS.md is NOT a memory log.
2. CLAUDE.md must remain small (20–60 lines).
3. CLAUDE.md MUST NOT duplicate rules already in ~/.claude/CLAUDE.md (git workflow, conventional commits, feature branches, PRs, secrets, Gemini review, agent workflows/handoff, content preservation, breakpoint coverage). These are global and apply automatically.
4. CLAUDE.md Invariants section MUST begin with this comment:
   "<!-- Note: Universal rules (git workflow, Gemini review, secrets) are in ~/.claude/CLAUDE.md -->"
   Then list ONLY project-specific invariants (e.g., "MUST use atomic credit deduction", "MUST work on iOS Safari").
5. If /agent/ directory already exists (re-run):
   - MERGE new invariants and pointers into CLAUDE.md, AGENTS.md, CONSTITUTION.md, and README.md — preserve all project-specific content (architecture, conventions, commands).
   - NEVER overwrite MEMORY.md, LEARNINGS.md, or HANDOFF.md if they contain content beyond their header.
   - SKIP WORKFLOWS.md if it contains more than a placeholder.
6. If unsure about commands or stack, write TODO rather than guessing.

Files to create/update:

- AGENTS.md
- CLAUDE.md
- /agent/CONSTITUTION.md
- /agent/WORKFLOWS.md
- /agent/MEMORY.md
- /agent/LEARNINGS.md
- /agent/HANDOFF.md
- /agent/README.md

Step 1 — Quick repo discovery
Infer language/framework/tooling from README, package.json, pyproject, go.mod, Cargo.toml, Makefile, CI configs, etc.
Identify canonical commands (dev/test/lint/build/typecheck/format) or mark TODO.

Step 2 — Write/Update CLAUDE.md (tiny constitution)
Use exactly these sections:

# Project

(1–3 sentences)

# Commands

- dev:
- test:
- lint:
- build:
- typecheck: (optional)
- format: (optional)

# Invariants

<!-- Note: Universal rules (git workflow, Gemini review, secrets) are in ~/.claude/CLAUDE.md -->

- MUST ... (project-specific rules only)
- MUST NOT ... (project-specific rules only)

# Architecture

(4–10 bullets)

# Conventions

(5–12 bullets)

Create/update /agent/CONSTITUTION.md with the same content, tool-agnostic wording.

Step 3 — Ensure GitHub Actions CI exists
Check if `.github/workflows/ci.yml` (or any CI workflow that runs lint/typecheck/test/build) exists.

If NO CI workflow is found:

1. Create `.github/workflows/ci.yml` using this template:
   - Triggers: push to main, PRs targeting main.
   - Jobs: lint, typecheck, test (parallel), then build (gated on the first three).
   - Each job: actions/checkout@v4, actions/setup-node@v4 (node 22, cache npm), npm ci, then the relevant npm script.
   - Detect which scripts exist in package.json and only create jobs for scripts that exist (lint, typecheck, test, build).
   - If the project uses environment variables at build time (e.g. Supabase, database URLs), add dummy env vars to the build step so prerendering doesn't fail.
2. Update /agent/WORKFLOWS.md deployment section to note CI is configured.

If CI already exists, skip this step.

Step 4 — Write/Update AGENTS.md (guidance entry point)
AGENTS.md must be stable, read-mostly guidance. Near the top include:

- "Workflow policy: /agent/WORKFLOWS.md (MUST read before starting work)"

Also include:

- Short project summary
- How to run dev/test/lint/build (or TODO)
- Safety notes (brief)
- Pointers to:
  - CLAUDE.md and /agent/CONSTITUTION.md
  - /agent/WORKFLOWS.md
  - /agent/MEMORY.md
  - /agent/LEARNINGS.md
  - /agent/HANDOFF.md (session snapshot, read on start)

Do NOT include dated learnings.

Step 5 — Create /agent files

- /agent/WORKFLOWS.md:
  - If no workflow chosen yet, create a minimal placeholder with TODO.
  - Deployment section should note: "GitHub Actions CI runs lint, typecheck, test, and build on all PRs and pushes to main" (if CI was set up in Step 3 or already exists).
- /agent/MEMORY.md:
  - Header only:
    # Memory (selectively loaded)
- /agent/LEARNINGS.md:
  - Header only:
    # Learnings (distilled)
- /agent/HANDOFF.md:
  - Header only:
    # Session Handoff
    (populated by /agent-handoff command)
- /agent/README.md:
  - Explain file roles and wiring:
    - Claude Code: CLAUDE.md always loaded.
    - Codex/Gemini: inject /agent/CONSTITUTION.md; retrieve MEMORY/LEARNINGS selectively.
    - HANDOFF.md: point-in-time session snapshot; read on session start, written by /agent-handoff.

Output:

1. Concise change plan
2. Full contents or unified diff for each file
3. List any assumptions or TODOs

User preferences:
$ARGUMENTS
