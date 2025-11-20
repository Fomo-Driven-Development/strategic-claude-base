# Strategic Claude Basic Base Template

## Structure

```
strategic-claude-base/
├── .claude/             # Claude Code configuration
│   ├── agents/          # Custom agent definitions
│   │   └── strategic -> ../../.strategic-claude-basic/core/agents
│   ├── commands/        # Custom commands
│   │   └── strategic -> ../../.strategic-claude-basic/core/commands
│   ├── hooks/           # Git hooks
│   │   └── strategic -> ../../.strategic-claude-basic/core/hooks
│   └── settings.local.json
├── .git/                # Git repository
├── .strategic-claude-basic/
│   ├── archives/        # Archived documentation
│   ├── core/            # Commands and agent definitions
│   │   ├── agents/      # Core agent definitions
│   │   ├── commands/    # Core commands
│   │   └── hooks/       # Core hooks
│   ├── decisions/       # Architecture Decision Records (ADRs)
│   │   └── CLAUDE.md
│   ├── guides/          # User guides
│   ├── issues/          # Issue tracking
│   │   └── CLAUDE.md
│   ├── plan/            # Implementation plans
│   │   └── CLAUDE.md
│   ├── product/         # Product documentation
│   │   └── CLAUDE.md
│   ├── research/        # Research documentation
│   │   └── CLAUDE.md
│   ├── summary/         # Work summaries
│   │   └── CLAUDE.md
│   ├── templates/       # Document templates
│   │   ├── agents/      # Agent templates
│   │   ├── commands/    # Command templates
│   │   ├── hooks/       # Hook templates
│   │   ├── ignore/      # Ignore file templates
│   │   └── mcps/        # MCP templates
│   └── tools/           # Utility tools
├── .pre-commit-config.yaml
├── LICENSE
├── post-install.sh
├── pre-install.sh
└── README.md
```

## Basic Usage

### Context Management

**Always run `/context` between commands** to monitor context usage. Keep context under 40% for optimal performance.

- When approaching limits: `/compact` or `/clear` before running the next command
- **Exception**: Run `/summarize` after Claude finishes executing a plan to capture incomplete work _before_ clearing context

### Single Task Workflow

For focused implementation tasks:

```
/research → /plan → /read_execute_plan → /summarize
```

**Example commands:**

```bash
/research 'user authentication system'
/plan @.strategic-claude-basic/research/RESEARCH_0001_13-09-2025_fri_user-auth.md
/read_execute_plan @.strategic-claude-basic/plan/PLAN_0001_13-09-2025_fri_user-auth.md
/summarize @.strategic-claude-basic/plan/PLAN_0001_13-09-2025_fri_user-auth.md
```

**Purpose:**

- **Research**: Analyze codebase and requirements, spawn parallel sub-agents for comprehensive investigation
- **Plan**: Create detailed implementation plan with phases and checkboxes
- **Execute**: Implement the plan systematically, checking off completed tasks
- **Summarize**: Document problems and incomplete work for future sessions

### Resume Task Workflow

To continue work on an existing plan:

```bash
/read_execute_plan @.strategic-claude-basic/plan/[filename].md
```

The system will automatically search for connected summaries to provide continuity and context for resuming work.

### Product-Focused Workflow

For comprehensive product development:

```
/research → /create_product_roadmap → /research_phase 1 → /plan_phase 1 → /read_execute_plan → /summarize
```

**Example commands:**

```bash
/research 'mobile app requirements'
/create_product_roadmap @.strategic-claude-basic/research/RESEARCH_0001_13-09-2025_fri_mobile-app.md
/research_phase 1
/plan_phase 1
/read_execute_plan @.strategic-claude-basic/plan/PLAN_0001_13-09-2025_fri_phase-1.md
/summarize @.strategic-claude-basic/plan/PLAN_0001_13-09-2025_fri_phase-1.md
```

**Purpose:**

- **Research**: Initial market and technical analysis
- **Create Product Roadmap**: Generate PRD, architecture, roadmap, and reference documentation
- **Research Phase**: Focused research on specific roadmap phase requirements
- **Plan Phase**: Create implementation plan for the specific phase
- **Execute & Summarize**: Implement and document progress

## Architecture Decision Records (ADRs)

The `.strategic-claude-basic/decisions/` directory contains Architecture Decision Records that document important architectural decisions made during development.

### ADR Commands

- **`/adr_create`** - Create a new ADR document
- **`/adr_update`** - Update an existing ADR with new information
- **`/adr_list`** - List all ADRs in the project

ADRs help maintain architectural consistency and provide context for future development decisions.

## Hooks

The strategic-claude-basic framework includes specialized hooks that enhance development workflows with notifications, security, and quality controls.

### Available Hooks

#### Security & Quality Control

- **`block-config-writes.py`** - Prevents modifications to critical configuration files (`.pre-commit-config.yaml`, etc.)
- **`block-skip-hooks.py`** - Blocks attempts to bypass code quality checks with `--no-verify` or `SKIP` flags

#### Notification Hooks

- **`notification-hook.py`** - Sends notifications when Claude needs permission or approval
- **`precompact-notify.py`** - Alerts when Claude's context window becomes full and auto-compaction triggers
- **`stop-session-notify.py`** - Sends session summaries when development sessions complete

### Configuration

Each hook can be customized by editing constants at the top of the files:

#### Security Hooks

```python
# block-config-writes.py
ENABLE_CONFIG_PROTECTION = True
PROTECTED_CONFIG_FILES = [
    ".golangci.yml",
    ".pre-commit-config.yaml",
    # Add more files as needed
]

# block-skip-hooks.py
ENABLE_HOOK_BYPASS_PROTECTION = True
```

#### Notification Hooks

```python
# notification-hook.py
ENABLE_NOTIFICATIONS = True
NOTIFICATION_AUDIO_FILE = "toasty.mp3"

# precompact-notify.py
ENABLE_COMPACT_NOTIFICATIONS = True
COMPACT_AUDIO_FILE = "get-over-here.mp3"
```

#### Global Settings (`notifications.py`)

```python
PROJECT_NAME = "strategic-claude-basic"        # Used in notification titles
NTFY_SERVER_URL = "http://nas1-oryx:2586"     # Your ntfy server
NTFY_TOPIC = f"{PROJECT_NAME}"                # Notification topic
```

### Audio Assets

Available Mortal Kombat themed notification sounds:

- `toasty.mp3` - Classic "Toasty!" sound
- `get-over-here.mp3` - Scorpion's signature line
- `evil-laugh.mp3` - Villainous laugh
- `finisshh-him.mp3` - Fatality announcement
- `that-was-pathetic.mp3` - Taunt sound
- `gutter-trash.mp3` - Insult sound
