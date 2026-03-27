---
name: init
description: "Bootstrap new projects with frontend design capabilities and skill creation tools. Use when starting a new project or setting up a development environment."
---

# Project Initialization

Set up AI-powered development tools for your project with frontend design capabilities and skill creation.

## What This Does

When you run `/init`, Claude will:

1. **Enable Frontend Design**: Activate the `frontend-design` skill for creating distinctive, production-grade interfaces
2. **Enable Skill Creation**: Set up access to skill creation and management tools
3. **Optional Setup**: Guide you through additional project-specific configurations

## Initialization Steps

### 1. Frontend Design Skill

The frontend-design skill helps you create:

- Distinctive, production-grade frontend interfaces
- Bold aesthetic choices that avoid generic AI patterns
- Working code with exceptional attention to visual details
- Cohesive designs with clear aesthetic point-of-view

**Usage after init:**

- Simply ask Claude to design or build frontend components
- The skill automatically guides the design process

### 2. Skill Creator

For creating custom skills specific to your project:

**Option A: Use the compound-engineering plugin skill**

```bash
# If you have compound-engineering plugin installed:
# Run: /create-agent-skill
# This provides expert guidance on creating skills
```

**Option B: Manual skill creation**

Create skills in `.claude/skills/` with this structure:

```markdown
---
name: your-skill-name
description: "What it does. When to use it."
---

# Your Skill

Instructions for Claude...
```

### 3. Project-Specific Setup

After enabling the core skills, I can help you:

- **Install additional toolkit skills**: Testing, git workflows, etc.
- **Create project-specific skills**: Custom workflows for your codebase
- **Configure hooks**: Pre/post tool execution automation
- **Set up commands**: Project-specific slash commands

## Quick Start

Just run `/init` and I'll guide you through the setup process, asking questions about:

1. What type of project are you working on?
2. Do you need frontend design capabilities? (Recommended: Yes)
3. Do you need to create custom skills? (Recommended: Yes if setting up a new codebase)
4. Any additional toolkit components you want to install?

## After Initialization

Once initialized, you can:

- **Build interfaces**: "Create a landing page for my SaaS product"
- **Create custom skills**: "Help me create a skill for my Python testing workflow"
- **Install more tools**: Run the installer again to add specific components

## Available Toolkit Skills

After init, you can install additional skills from the toolkit:

| Skill             | Description                                                  |
| ----------------- | ------------------------------------------------------------ |
| `frontend-design` | Create distinctive, production-grade frontend interfaces     |
| `testing-webapps` | Test web apps with Chrome (visual) or Playwright (automated) |

## Installation Commands

```bash
# Install from toolkit to current project
cd /path/to/claude-toolkit
./install.sh --skills frontend-design

# Install globally (available in all projects)
./install.sh --global --skills frontend-design testing-webapps
```

## Workflow

1. Run `/init` to start the setup
2. Answer a few questions about your project
3. I'll enable the relevant skills and guide you through setup
4. Start building with AI-powered tools immediately

## Notes

- The init skill configures your project's `.claude/` directory
- Skills can be project-local or global (installed in `~/.claude`)
- You can re-run `/init` to add more capabilities later
- Custom skills you create are automatically available in your project
