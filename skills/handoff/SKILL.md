---
name: handoff
description: "Use at the end of any working session or when pausing work. Captures durable learnings in /agent/MEMORY.md and writes a session snapshot to /agent/HANDOFF.md. Always runs in a background sub-agent so it doesn't block the main conversation."
user-invocable: true
argument-hint: '/handoff' or '/handoff "key learning from this session"'
allowed-tools: Agent, Bash, Read, Write, Glob, Grep
---

# Handoff

End-of-session skill that captures learnings and writes a handoff snapshot. **Always runs in a background sub-agent** so it doesn't block or pollute the main conversation context.

## When This Runs

- User types `/handoff`
- End of a significant work session
- Before switching to a different project
- When pausing work that will be resumed later

## How It Works

Launch a **single background sub-agent** that performs both steps sequentially. The main agent does NOT do this work itself.

### Step 1: Launch Background Agent

Spawn one Agent with `run_in_background: true` using the prompt template below. The agent handles both the note and the handoff in sequence.

**Agent prompt:**

```
You are a session handoff agent. Your job is to capture learnings and write a handoff snapshot for the next session. Do this work silently and efficiently.

CONTEXT FROM USER (if any): {any arguments the user passed}

## Part 1: Agent Note — Append learnings to /agent/MEMORY.md

Rules:
- Append-only — never rewrite past entries
- Use today's date as section header (YYYY-MM-DD)
- Never modify AGENTS.md, CLAUDE.md, or any constitution files
- Keep entries short, actionable bullets

Process:
1. Ensure /agent/ directory exists (create if missing)
2. Ensure /agent/MEMORY.md exists (create with "# Memory (selectively loaded)" header if missing)
3. Gather learnings from this session. If the user provided specific learnings in the arguments, use those. Otherwise, infer from:
   - `git log --oneline -10` — what was committed
   - `git diff --stat` — what's uncommitted
   - Any patterns, gotchas, or decisions worth remembering
4. Append under today's date:
   ## YYYY-MM-DD
   - <learning 1>
   - <learning 2>
   ...

Only add learnings that are genuinely useful for future sessions. Skip if nothing non-obvious was learned.

## Part 2: Agent Handoff — Write /agent/HANDOFF.md

This is a point-in-time snapshot (overwrite each time, NOT append-only).

Process:
1. Run `git branch --show-current`
2. Run `git status --short`
3. Run `git log --oneline -10`
4. If /agent/WORKFLOWS.md exists, read it for context
5. If /agent/MEMORY.md exists, read it for context

Write /agent/HANDOFF.md using this template:

# Session Handoff

## Date
YYYY-MM-DD (today)

## Branch
(current branch name, or "not in a git repo" if applicable)

## Git Status
(output of git status --short, or "Clean" if nothing to report, or "N/A" if not a git repo)

## Summary
(1–3 sentence overview of what this session was about)

## What Was Done
- (bullet list of completed work)

## What Remains
- (bullet list of unfinished tasks, next steps)

## Known Issues
- (any bugs, blockers, or concerns — or "None")

## Key Decisions
- (important choices made this session that affect future work — or "None")

## Relevant Files
- (files that were created or heavily modified this session)

## Context for Next Session
(free-form paragraph: anything the next agent/session needs to know to pick up smoothly)
```

### Step 2: Confirm to User

After launching the background agent, immediately tell the user:

```
Handoff agent launched in background. It will:
1. Append learnings to /agent/MEMORY.md
2. Write session snapshot to /agent/HANDOFF.md

You can continue working or end the session.
```

When the background agent completes, report:

```
Handoff complete.
  - Learnings saved to /agent/MEMORY.md
  - Snapshot saved to /agent/HANDOFF.md
```

## Key Design Decisions

- **Always background**: The handoff agent runs via `run_in_background: true` so it never blocks the user. Session-end should be fast.
- **Single agent, two steps**: One sub-agent does both note + handoff sequentially (not two separate agents) to avoid race conditions on /agent/MEMORY.md.
- **Note before handoff**: Learnings are captured first so the handoff snapshot can reference them if needed.
- **Works outside git repos**: If not in a git repo, the agent skips git commands and writes what it can (session summary, files modified, decisions made).
- **Idempotent**: Running `/handoff` twice overwrites HANDOFF.md (by design) and appends to MEMORY.md (only if new learnings exist).
