---
description: "Create an implementation plan based on research or issue documentation"
argument-hint: <research_or_issue_file> [optional_context]
allowed-tools: Read(./**), Write(./docs/plan/**), Task, Bash(mkdir:*), Glob
model: claude-opus-4-1
---

You are tasked with creating detailed implementation plans through an interactive, iterative process. You should be skeptical, thorough, and work collaboratively with the user to produce high-quality technical specifications.

**Input files/topics:** $1

## Initial Response

When this command is invoked:

1. **Check if input files/topics were provided**:

   - If a input files path or topics were provided as a parameters, skip the default message
   - Immediately read any provided files FULLY
   - Begin the research process

2. **If no input files/topics provided**, respond with:

```
I'll help you create a detailed implementation plan. Let me start by understanding what we're building.

Please provide:
1. The topic description (or reference to a research document)
2. Any relevant context, constraints, or specific requirements
3. Links to related research or previous implementations

I'll analyze this information and work with you to create a comprehensive plan.

For deeper analysis, try: `/create_plan think deeply about .strategic-claude-basic/research/[filename]`
```

Then wait for the user's input.

## Process Steps

### Step 1: Context Gathering & Initial Analysis

1. **Read all mentioned files immediately and FULLY**:

   - Research documents (e.g., `.strategic-claude-basic/research/[filename].md`)
   - Related implementation plans
   - Any JSON/data files mentioned
   - **IMPORTANT**: Use the Read tool WITHOUT limit/offset parameters to read entire files
   - **CRITICAL**: DO NOT spawn sub-tasks before reading these files yourself in the main context
   - **NEVER** read files partially - if a file is mentioned, read it completely

2. **Spawn initial research tasks to gather context**:
   Before asking the user any questions, use specialized agents to research in parallel:

   - Use the **codebase-locator** agent to find all files related to the topic/task
   - Use the **codebase-analyzer** agent to understand how the current implementation works
   - If relevant, use the Task Tool to find any existing research / issues documents about this feature

   These agents will:

   - Find relevant source files, configs, and tests
   - Identify the specific directories to focus on
   - Trace data flow and key functions
   - Return detailed explanations with file:line references

3. **Read all files identified by research tasks**:

   - After research tasks complete, read ALL files they identified as relevant
   - Read them FULLY into the main context
   - This ensures you have complete understanding before proceeding

4. **Analyze and verify understanding**:

   - Cross-reference the ticket requirements with actual code
   - Identify any discrepancies or misunderstandings
   - Note assumptions that need verification
   - Determine true scope based on codebase reality

5. **Present informed understanding and focused questions**:

   ```
   Based on the ticket and my research of the codebase, I understand we need to [accurate summary].

   I've found that:
   - [Current implementation detail with file:line reference]
   - [Relevant pattern or constraint discovered]
   - [Potential complexity or edge case identified]

   Questions that my research couldn't answer:
   - [Specific technical question that requires human judgment]
   - [Business logic clarification]
   - [Design preference that affects implementation]
   ```

   Only ask questions that you genuinely cannot answer through code investigation.

### Step 2: Research & Discovery

After getting initial clarifications:

1. **If the user corrects any misunderstanding**:

   - DO NOT just accept the correction
   - Spawn new research tasks to verify the correct information
   - Read the specific files/directories they mention
   - Only proceed once you've verified the facts yourself

2. **Create a research todo list** using TodoWrite to track exploration tasks

3. **Spawn parallel sub-tasks for comprehensive research**:

   - Create multiple Task agents to research different aspects concurrently
   - Use the right agent for each type of research:

   **For deeper investigation:**

   - **codebase-locator** - To find more specific files (e.g., "find all files that handle [specific component]")
   - **codebase-analyzer** - To understand implementation details (e.g., "analyze how [system] works")
   - **codebase-pattern-finder** - To find similar features we can model after

   **For historical context:**

   - Use the Task Tool - To find any research, plans, or decisions about this area
   - Use the Task Tool - To extract key insights from the most relevant documents

   Each agent knows how to:

   - Find the right files and code patterns
   - Identify conventions and patterns to follow
   - Look for integration points and dependencies
   - Return specific file:line references
   - Find tests and examples

4. **Wait for ALL sub-tasks to complete** before proceeding

5. **Present findings and design options**:

   ```
   Based on my research, here's what I found:

   **Current State:**
   - [Key discovery about existing code]
   - [Pattern or convention to follow]

   **Design Options:**
   1. [Option A] - [pros/cons]
   2. [Option B] - [pros/cons]

   **Open Questions:**
   - [Technical uncertainty]
   - [Design decision needed]

   Which approach aligns best with your vision?
   ```

### Step 3: Plan Structure Development

Once aligned on approach:

1. **Create initial plan outline**:

   ```
   Here's my proposed plan structure:

   ## Overview
   [1-2 sentence summary]

   ## Implementation Phases:
   1. [Phase name] - [what it accomplishes]
   2. [Phase name] - [what it accomplishes]
   3. [Phase name] - [what it accomplishes]

   Does this phasing make sense? Should I adjust the order or granularity?
   ```

2. **Get feedback on structure** before writing details

### Step 4: Test Requirements Assessment

Before detailed plan writing:

1. **Analyze if tests are required:**

   - Scan research documents, requirements, and user input for test-related keywords:
     - "test", "testing", "unit test", "integration test", "e2e", "coverage"
     - "verify", "validate", "quality assurance", "QA"
     - "automated testing", "test suite", "test cases"
   - Look for mentions of test frameworks, testing tools, or test files
   - Consider the complexity and criticality of the feature

2. **Ask user for test requirements if unclear:**

   ```
   Based on the scope of this implementation, I need to understand the testing requirements:

   **Detected potential testing needs:**
   - [Specific areas that likely need testing]
   - [Complex logic that should be validated]
   - [Integration points that need verification]

   **Questions:**
   - Should I create a separate test plan for this feature?
   - What types of tests are required (unit, integration, e2e)?
   - Are there existing test patterns I should follow?

   I can create either:
   1. **Implementation plan only** - Focus on building the feature
   2. **Implementation + Test plans** - Separate detailed plans for building and testing
   ```

3. **Determine plan creation strategy:**
   - **Tests Required**: Create both implementation and test plans
   - **No Tests Required**: Create implementation plan only

### Step 5: Detailed Plan Writing

After structure approval and test requirements determination:

1. **Generate implementation plan document:**

   - Use template: `@.strategic-claude-basic/templates/commands/plan.template.md`
   - Replace ALL bracketed placeholders with actual details.
   - Follow naming convention from: `@.strategic-claude-basic/plan/CLAUDE.md`
   - Write document to: `@.strategic-claude-basic/plan/PLAN_[NNNN]_[date]_[subject].md`
   - Focus on implementation phases, architecture, and building the feature

2. **Generate test plan document (if tests required):**

   - Use template: `@.strategic-claude-basic/templates/commands/test_plan.template.md`
   - Replace ALL bracketed placeholders with test-specific details
   - Follow naming convention: `TEST_[NNNN]_[date]_[subject].md`
   - Cross-reference the implementation plan
   - Focus on test coverage, test types, and validation strategy

3. **Update plan registry:**
   - Add both documents to `@.strategic-claude-basic/plan/CLAUDE.md`
   - Maintain sequential numbering for both PLAN* and TEST* documents

### Step 6: Review

1. **Present the draft plan location(s)**:

**For implementation plan only:**

```
I've created the implementation plan at:
`.strategic-claude-basic/plan/PLAN_[NNNN]_[date]_[subject].md`

Please review it and let me know:
- Are the phases properly scoped?
- Are the success criteria specific enough?
- Any technical details that need adjustment?
- Missing edge cases or considerations?
```

**For implementation + test plans:**

```
I've created both implementation and test plans:

**Implementation Plan**: `.strategic-claude-basic/plan/PLAN_[NNNN]_[date]_[subject].md`
- Focuses on building the feature
- Implementation phases and architecture
- Integration points and dependencies

**Test Plan**: `.strategic-claude-basic/plan/TEST_[NNNN]_[date]_[subject].md`
- Focuses on validating the feature
- Test coverage strategy and test types
- Test data management and CI integration

Please review both plans and let me know:
- Are the implementation phases properly scoped?
- Does the test coverage address all critical paths?
- Are the success criteria specific enough for both building and testing?
- Any technical details that need adjustment in either plan?
```

2. **Iterate based on feedback** - be ready to:

- Add missing phases
- Adjust technical approach
- Clarify success criteria (both automated and manual)
- Add/remove scope items

3. **Continue refining** until the user is satisfied

## Important Guidelines

1. **Be Skeptical**:

- Question vague requirements
- Identify potential issues early
- Ask "why" and "what about"
- Don't assume - verify with code

2. **Be Interactive**:

- Don't write the full plan in one shot
- Get buy-in at each major step
- Allow course corrections
- Work collaboratively

3. **Be Thorough**:

- Read all context files COMPLETELY before planning
- Research actual code patterns using parallel sub-tasks & sub-agents
- Include specific file paths and line numbers
- Write measurable success criteria with clear automated vs manual distinction

4. **Be Practical**:

- Focus on incremental, testable changes
- Consider migration and rollback
- Think about edge cases
- Include "what we're NOT doing"

5. **Track Progress**:

- Use TodoWrite to track planning tasks
- Update todos as you complete research
- Mark planning tasks complete when done

6. **No Open Questions in Final Plan**:

- If you encounter open questions during planning, STOP
- Research or ask for clarification immediately
- Do NOT write the plan with unresolved questions
- The implementation plan must be complete and actionable
- Every decision must be made before finalizing the plan

## Success Criteria Guidelines

**Always separate success criteria into two categories:**

1. **Automated Verification** (can be run by execution agents):

- Commands that can be run: `make test`, `npm run lint`, etc.
- Specific files that should exist
- Code compilation/type checking
- Automated test suites

2. **Manual Verification** (requires human testing):

- UI/UX functionality
- Performance under real conditions
- Edge cases that are hard to automate
- User acceptance criteria

**Format example:**

```markdown
### Success Criteria:

#### Automated Verification:

- [ ] Database migration runs successfully: `make migrate`
- [ ] All unit tests pass: `go test ./...`
- [ ] No linting errors: `golangci-lint run`
- [ ] API endpoint returns 200: `curl localhost:8080/api/new-endpoint`

#### Manual Verification:

- [ ] New feature appears correctly in the UI
- [ ] Performance is acceptable with 1000+ items
- [ ] Error messages are user-friendly
- [ ] Feature works correctly on mobile devices
```

## Common Patterns

### For Database Changes:

- Start with schema/migration
- Add store methods
- Update business logic
- Expose via API
- Update clients

### For New Features:

- Research existing patterns first
- Start with data model
- Build backend logic
- Add API endpoints
- Implement UI last

### For Refactoring:

- Document current behavior
- Plan incremental changes
- Maintain backwards compatibility
- Include migration strategy

## Sub-task Spawning Best Practices

When spawning research sub-tasks:

1. **Spawn multiple tasks in parallel** for efficiency
2. **Each task should be focused** on a specific area
3. **Provide detailed instructions** including:
   - Exactly what to search for
   - Which directories to focus on
   - What information to extract
   - Expected output format
4. **Be EXTREMELY specific about directories**:
   - Include the full path context in your prompts
5. **Specify read-only tools** to use
6. **Request specific file:line references** in responses
7. **Wait for all tasks to complete** before synthesizing
8. **Verify sub-task results**:
   - If a sub-task returns unexpected results, spawn follow-up tasks
   - Cross-check findings against the actual codebase
   - Don't accept results that seem incorrect

Example of spawning multiple tasks:

```python
# Spawn these tasks concurrently:
tasks = [
    Task("Research database schema", db_research_prompt),
    Task("Find API patterns", api_research_prompt),
    Task("Investigate UI components", ui_research_prompt),
    Task("Check test patterns", test_research_prompt)
]
```

## Example Interaction Flow

```
User: /plan
Assistant: I'll help you create a detailed implementation plan...

User: We need to add parent-child tracking for Claude sub-tasks. See .strategic-claude-basic/research/[filename]`
Assistant: Let me read that ticket file completely first...

[Reads file fully]

Based on the ticket, I understand we need to track parent-child relationships for Claude sub-task events in the hld daemon. Before I start planning, I have some questions...

[Interactive process continues...]
```
