---
name: harness-profile
description: Generate a visual profile of your Claude Code harness setup — skills used, hooks configured, workflow patterns, tool usage, and plugin inventory across the last 30 days. Like /insights but focused on your harness configuration, not project content. Use when asked about "harness profile", "my setup", "what skills do I use", "show my harness", or "harness report".
user-invocable: true
argument-hint: "harness-profile"
allowed-tools: Bash, Read
---

# Harness Profile

Generate a comprehensive visual report of the user's Claude Code harness configuration and usage patterns over the last 30 days.

## What This Does

Runs a Python extraction script that reads harness metadata from:

- `~/.claude/settings.json` (hooks, plugins, permissions)
- `~/.claude/plugins/installed_plugins.json` (plugin inventory)
- `~/.claude/skills/` (skill frontmatter — names and allowed-tools only)
- `~/.claude/usage-data/session-meta/` (pre-computed session stats)
- `~/.claude/projects/*/*.jsonl` (field-whitelisted: tool names, skill names, hook events only)
- `~/.claude/projects/*/settings.local.json` (approved permissions)

**Privacy guarantee:** The script uses a strict field whitelist. It NEVER reads tool arguments, message text, tool results, file paths, or any project-specific content. Real credentials exist in JSONL files — the script never touches those fields.

## How to Run

Run the extraction script and open the result:

```bash
python3 ~/.claude/skills/harness-profile/scripts/extract.py
```

The script outputs the HTML file path to stdout. Open it in the browser:

```bash
open "$(python3 ~/.claude/skills/harness-profile/scripts/extract.py)"
```

After running, tell the user:

1. Where the report was saved
2. That it's been opened in their browser
3. A brief summary of the top-level stats (sessions, skills used, hooks active)
