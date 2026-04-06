# Claude Toolkit

Reusable skills, agents, commands, hooks, and settings for Claude Code.

## Quick Install

```bash
# Clone the repo
git clone https://github.com/craigdossantos/claude-toolkit.git
cd claude-toolkit

# Interactive install
./install.sh

# Or install everything to current project
./install.sh --all

# Or install globally (available in all projects)
./install.sh --global --all
```

## Available Components

### Skills

| Skill             | Description                                                                                                                                                          |
| ----------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `harness-profile` | Generate a visual report of your Claude Code setup — skills, hooks, CLI tools, agent patterns, and more. Like `/insights` but focused on your harness configuration. |
| `init`            | Bootstrap new projects with frontend design and skill creation capabilities                                                                                          |
| `testing-webapps` | Test web apps with Claude for Chrome (visual/interactive) or Playwright (automated/CI)                                                                               |
| `frontend-design` | Create distinctive, production-grade frontend interfaces that avoid generic AI aesthetics                                                                            |

### Quick Install: Harness Profile

Generate a visual report of how you use Claude Code — no project content exposed, just harness metadata:

```bash
mkdir -p ~/.claude/skills/harness-profile/scripts && \
curl -sL https://raw.githubusercontent.com/craigdossantos/claude-toolkit/main/skills/harness-profile/SKILL.md \
  -o ~/.claude/skills/harness-profile/SKILL.md && \
curl -sL https://raw.githubusercontent.com/craigdossantos/claude-toolkit/main/skills/harness-profile/scripts/extract.py \
  -o ~/.claude/skills/harness-profile/scripts/extract.py && \
open "$(python3 ~/.claude/skills/harness-profile/scripts/extract.py)"
```

This installs the skill and immediately generates your report. The report saves to `~/.claude/usage-data/harness-profile.html` (alongside the `/insights` report). After installing, you can also run it anytime in Claude Code with `/harness-profile`.

### Agents

_Coming soon_

### Commands

_Coming soon_

### Hooks

_Coming soon_

## Usage

### Install Specific Components

```bash
# Install specific skills
./install.sh --skills testing-webapps frontend-design

# Install all skills
./install.sh --skills

# Install to global ~/.claude
./install.sh --global --skills testing-webapps
```

### List Available Components

```bash
./install.sh --list
```

### Full Options

```
./install.sh                    Interactive menu
./install.sh --list             List available components
./install.sh --all              Install everything
./install.sh --global           Install to ~/.claude (global)
./install.sh --skills           Install all skills
./install.sh --skills NAME...   Install specific skills
./install.sh --agents           Install all agents
./install.sh --commands         Install all commands
./install.sh --hooks            Install all hooks
```

## Directory Structure

```
claude-toolkit/
├── install.sh          # Installer script
├── README.md
├── skills/             # Claude Code skills
│   ├── init/
│   │   └── SKILL.md
│   ├── testing-webapps/
│   │   ├── SKILL.md
│   │   ├── playwright-patterns.md
│   │   ├── ci-cd-integration.md
│   │   ├── test_template.py
│   │   └── with_server.py
│   └── frontend-design/
│       └── SKILL.md
├── agents/             # Subagent definitions
├── commands/           # Slash commands
├── hooks/              # Pre/post tool hooks
├── settings/           # Settings presets
└── plugins/            # Full plugin bundles
```

## Adding Your Own Components

### Skills

Create a directory in `skills/` with a `SKILL.md`:

```markdown
---
name: my-skill-name
description: "What it does. When to use it."
---

# My Skill

Instructions for Claude...
```

### Commands

Create a `.md` file in `commands/`:

```markdown
# /my-command

Instructions for what this command does...
```

### Hooks

Add Python or shell scripts to `hooks/`:

```python
#!/usr/bin/env python3
# hooks/my_hook.py
# Pre-tool hook that validates something
```

## Contributing

1. Add your component to the appropriate directory
2. Test with `./install.sh --list` to verify it's detected
3. Install and test in a project
4. Submit a PR

## License

MIT
