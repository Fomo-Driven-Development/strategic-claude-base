---
description: "Analyze plans for potential blocking issues by examining codebase, dependencies, and related documents"
argument-hint: <plan_file(s)_or_NNNN>
allowed-tools: Read(./**), Task, Bash(git:*, find:*, grep:*), Glob, Grep
model: claude-opus-4-1
---

You are tasked with analyzing implementation plans for potential blocking issues by examining the codebase, technical dependencies, related summaries, and research documents.

**Plan input provided:** $1

## Input Format Support

This command supports multiple input formats:

- **Single plan**: `/check_plan_for_blockers PLAN_0019_16-09-2025-tue_reed-solomon-aligned-strategy.md`
- **Multiple plans**: `/check_plan_for_blockers PLAN_0019_16-09-2025-tue_reed-solomon-aligned-strategy.md TEST_0019_16-09-2025-tue_rs-aligned-strategy-testing.md`
- **NNNN number**: `/check_plan_for_blockers 0019` (finds all plans with that number)
- **Multiple NNNN**: `/check_plan_for_blockers 0019 0020 0021`

## Initial Response

When this command is invoked:

1. **Check if plan input was provided**:

   - If plan input provided, proceed with analysis
   - If no input provided, respond with:

   ```
   I'll analyze implementation plans for potential blocking issues by examining the codebase, dependencies, and related work.

   Please provide plan file(s) or NNNN number(s) to analyze:
   Examples:
   - Single plan: `/check_plan_for_blockers PLAN_0019_16-09-2025-tue_reed-solomon-aligned-strategy.md`
   - Multiple plans: `/check_plan_for_blockers PLAN_0019... TEST_0019...`
   - NNNN number: `/check_plan_for_blockers 0019`
   - Multiple NNNN: `/check_plan_for_blockers 0019 0020 0021`

   I'll use codebase agents to analyze technical dependencies and identify any blockers.
   ```

   Then wait for the user's input.

## Process Steps

### Step 1: Plan Discovery and Validation

1. **Parse input arguments**:

   - If argument contains `.md`, treat as plan file path(s)
   - If argument is 4-digit number (NNNN), search for matching plans
   - Support space-separated multiple inputs

2. **Find and validate plan files**:

   ```bash
   # For NNNN inputs, find matching plans
   find .strategic-claude-basic/plan/ -name "*_NNNN_*" -type f

   # Validate plan files exist
   test -f ".strategic-claude-basic/plan/[plan-file]"
   ```

3. **Present plan discovery results**:

   ```
   Plan Discovery Results:
   Found [N] plan(s) for analysis:
   - PLAN_NNNN_date_subject.md ([implementation plan])
   - TEST_NNNN_date_subject.md ([test plan])

   Proceeding with blocker analysis...
   ```

### Step 2: Document Context Analysis

1. **Read all discovered plans completely**:

   - Extract implementation requirements and phases
   - Identify technical dependencies mentioned
   - Note file paths and components to be modified
   - Extract success criteria and prerequisites

2. **Find related documents**:

   **Summary Documents**:
   - Search for matching SUMMARY documents with same NNNN
   - Read summaries to understand current status and known issues
   - Extract incomplete work and technical debt

   **Research Documents**:
   - Search for matching RESEARCH documents
   - Read research to understand design decisions and constraints

3. **Present document context**:

   ```
   Document Context Analysis:
   Plans to analyze:
   - [Plan 1]: [brief description of scope]
   - [Plan 2]: [brief description of scope]

   Related documents found:
   - Summaries: [N] found ([completion status])
   - Research: [N] found ([topics covered])

   Proceeding with codebase dependency analysis...
   ```

### Step 3: Codebase Dependency Analysis

1. **Use codebase agents for deep analysis**:

   **For each plan, analyze dependencies using agents**:

   ```
   # Use codebase-locator to find relevant files
   Task: codebase-locator
   Prompt: "Find files related to [plan scope] including [key components from plan]"

   # Use codebase-analyzer for implementation details
   Task: codebase-analyzer
   Prompt: "Analyze implementation status and dependencies for [specific components]. Focus on interface compatibility, missing implementations, and integration points."

   # Use codebase-pattern-finder for similar implementations
   Task: codebase-pattern-finder
   Prompt: "Find existing patterns for [plan approach] that could guide or block implementation"
   ```

2. **Git history analysis**:

   ```bash
   # Check recent commits that might affect dependencies
   git log --oneline -20

   # Look for ongoing work that might conflict
   git status --porcelain

   # Check for unstaged changes in relevant areas
   git diff --name-only
   ```

### Step 4: Technical Blocker Identification

1. **Categorize potential blockers**:

   **Critical Blockers** 🔴:
   - Missing required dependencies
   - Incompatible interfaces or APIs
   - Test failures in prerequisite components
   - Conflicting ongoing work

   **Non-Critical Issues** 🟡:
   - Performance concerns
   - Technical debt
   - Minor API inconsistencies
   - Documentation gaps

   **Prerequisites** ⚠️:
   - Required setup or configuration
   - Dependency updates needed
   - Environmental requirements

2. **Test current codebase state**:

   ```bash
   # Run basic build check
   go build ./...

   # Check for linting issues in relevant areas
   golangci-lint run [relevant-paths]

   # Quick test check for critical components
   go test -short [relevant-packages]
   ```

### Step 5: Agent-Enhanced Analysis

1. **Use specialized agents for comprehensive analysis**:

   **For each identified dependency**:
   - **codebase-analyzer**: Analyze implementation completeness
   - **codebase-locator**: Find all related files and interfaces
   - **general-purpose**: Research complex integration points

2. **Cross-reference with known issues**:

   - Check summaries for unresolved critical issues
   - Look for TODO/FIXME comments in related code
   - Identify performance bottlenecks or limitations

### Step 6: Comprehensive Blocker Report

1. **Generate detailed blocker assessment**:

   ```
   ## Plan Blocker Analysis: [Plan Names]

   ### ✅ Prerequisites Status
   - [Dependency 1]: ✅ Available / ❌ Missing / ⚠️ Partial
   - [Dependency 2]: ✅ Available / ❌ Missing / ⚠️ Partial

   ### 🔴 Critical Blockers
   **Issues that prevent implementation:**
   1. **[Blocker Name]** - [Description]
      - **Impact**: [How it blocks the plan]
      - **Location**: [File/component affected]
      - **Resolution**: [Required action]
      - **Estimated Effort**: [Time/complexity]

   ### 🟡 Non-Critical Issues
   **Issues that may complicate but don't block implementation:**
   1. **[Issue Name]** - [Description]
      - **Impact**: [How it affects implementation]
      - **Workaround**: [Possible solutions]

   ### ⚠️ Prerequisites & Setup
   **Required before starting implementation:**
   1. **[Prerequisite]** - [Description and setup steps]

   ### 📋 Implementation Readiness
   - **Ready to proceed**: ✅ / ❌
   - **Critical blockers**: [N] found
   - **Dependencies available**: [N/Total]
   - **Risk level**: Low / Medium / High

   ### 🚀 Recommended Actions
   1. **Immediate**: [Actions needed before starting]
   2. **During implementation**: [Considerations during work]
   3. **Future**: [Items to address in subsequent work]
   ```

2. **Agent-sourced evidence**:

   - Include specific findings from codebase agents
   - Reference exact file locations and line numbers
   - Provide code examples of potential conflicts

## Advanced Analysis Features

### Multi-Plan Cross-Dependencies

When analyzing multiple plans:

1. **Check for plan interdependencies**:
   - Plans that modify the same components
   - Sequential dependencies between plans
   - Resource conflicts (same files, interfaces)

2. **Optimization opportunities**:
   - Shared implementations
   - Combined testing strategies
   - Coordinated development approach

### Performance Impact Analysis

For performance-sensitive plans:

1. **Use performance-focused agents**:
   - Analyze current performance baselines
   - Identify potential performance regressions
   - Evaluate resource requirements

2. **Benchmark existing similar code**:
   - Find performance-critical paths
   - Analyze memory and CPU usage patterns

### Integration Readiness

For plans involving multiple components:

1. **Interface compatibility analysis**:
   - Check API version compatibility
   - Analyze data structure alignment
   - Verify protocol consistency

2. **Testing infrastructure readiness**:
   - Check test coverage of dependencies
   - Verify testing tools availability
   - Assess CI/CD pipeline compatibility

## Error Handling

### Plan Not Found
```
❌ Plan file not found: [filename]

Available plans in .strategic-claude-basic/plan/:
[List of available plans with NNNN numbers]

Please check the filename or NNNN number and try again.
```

### Multiple NNNN Matches
```
⚠️ Multiple plans found for NNNN [number]:
- PLAN_NNNN_date_subject.md
- TEST_NNNN_date_subject.md
- [Additional matches]

Analyzing all found plans...
```

### Agent Analysis Failures
```
⚠️ Codebase agent analysis encountered issues:
- [Agent name]: [Error or limitation]
- Falling back to manual analysis for affected areas
```

## Success Criteria

A successful blocker analysis should:

- **Identify all critical blockers** that prevent implementation
- **Provide actionable resolution steps** for each blocker
- **Use agent insights** to validate technical assumptions
- **Offer implementation readiness assessment** with confidence level
- **Suggest optimization opportunities** for multi-plan scenarios
- **Reference specific code locations** and concrete evidence

The analysis should enable informed decision-making about when and how to proceed with implementation work.
