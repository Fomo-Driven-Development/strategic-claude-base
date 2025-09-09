# strategic-claude-basic

A structured template system for Claude AI development workflows with specialized commands, agents, and documentation conventions.

## Claude Code Router Branch

**Branch**: `ccr-template`

This branch contains enhancements specifically designed for Claude Code Router (CCR) compatibility, including:

- **Web Search MCP Integration**: The `web-search-researcher` subagent has been updated to use MCP (Model Context Protocol) web search tools instead of the built-in WebSearch tool for improved search capabilities
- **Enhanced Web Research**: More powerful and flexible web search options with support for comprehensive searches, quick summaries, and direct URL content extraction

### MCP Web Search Tools

The following MCP tools are now available through the web-search-researcher agent:
- `mcp__web-search__full-web-search` - Comprehensive research with full page content
- `mcp__web-search__get-web-search-summaries` - Quick overview of search results  
- `mcp__web-search__get-single-web-page-content` - Extract content from specific URLs

## Key Commands

### Research & Analysis
- `/research <topic>` - Comprehensive research with parallel sub-agents
- `/codebase_analyzer <component>` - Analyze code implementations 
- `/codebase_locator <feature>` - Find files and components
- `/codebase_pattern_finder <pattern>` - Find similar implementations

**Note**: The `web-search-researcher` subagent now uses MCP web search tools for enhanced web research capabilities with better search results and content extraction.

### Planning & Implementation
- `/plan <research_file>` - Create implementation plans
- `/plan_phase <plan_file>` - Execute plan phases
- `/read_and_execute_plan <plan_file>` - Execute plans with validation

### Documentation & Tracking
- `/summarize [plan_reference]` - Problem-focused work summaries
- `/validate_summary <summary_file>` - Validate and archive summaries
- `/create_issue <subject_or_file>` - Create issue documentation

### Product Management
- `/create_product_roadmap <research_or_plan>` - Generate roadmaps
- `/archive_docs_update_roadmap` - Archive docs and update roadmap

## Structure

```
.strategic-claude-basic/
├── core/                # Commands and agent definitions
├── templates/           # Document templates
├── research/            # Research documentation
├── plan/                # Implementation plans
├── summary/             # Work summaries
├── issues/              # Issue tracking
└── product/             # Product documentation
```

## Document Naming

**CRITICAL**: Follow strict patterns:
- Research: `RESEARCH_NNNN_DD-MM-YYYY_day_subject.md`
- Plans: `PLAN_NNNN_DD-MM-YYYY_day_subject.md`
- Summaries: `SUMMARY_NNNN_DD-MM-YYYY_day_subject.md`

Get current date: `date '+%d-%m-%Y-%a' | tr '[:upper:]' '[:lower:]'`

## Usage

1. Start with `/research` for exploration (now enhanced with MCP web search tools)
2. Use `/plan` to create implementation strategies
3. Use `/summarize` to document problems and progress
4. Always check directory CLAUDE.md files for specific conventions

## Claude Code Router Compatibility

This branch is specifically configured for use with Claude Code Router (CCR) and includes:
- MCP web search server configuration in `.mcp.json`
- Enhanced web research capabilities through the `web-search-researcher` subagent
- Backward compatibility with existing workflows

To use the web search functionality, ensure the MCP web search server is properly configured and running.

This framework emphasizes structured documentation over traditional development workflows.