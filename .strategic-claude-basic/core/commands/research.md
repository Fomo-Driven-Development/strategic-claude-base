---
description: "Conduct research on a topic and generate documentation following project standards"
argument-hint: <topic> [optional_description]
allowed-tools: Read(./**), Write(./strategic-claude-basic/research/**), Task, Bash(mkdir:*), Glob
model: claude-opus-4-1
---

You are tasked with conducting comprehensive research across the codebase to answer user questions by spawning parallel sub-agents and synthesizing their findings.

**Topic provided:** $1

## Research Process

If no topic was provided or if you need to specify what to research, please tell me:
**What topic or area would you like me to research?**

### Steps to follow after receiving the research query:

1. **Read any directly mentioned files first:**

   - If the user mentions specific files (tickets, docs, JSON), read them FULLY first
   - **IMPORTANT**: Use the Read tool WITHOUT limit/offset parameters to read entire files
   - **CRITICAL**: Read these files yourself in the main context before spawning any sub-tasks
   - This ensures you have full context before decomposing the research

2. **Analyze and decompose the research question:**

   - Break down the user's query into composable research areas
   - Take time to ultrathink about the underlying patterns, connections, and architectural implications the user might be seeking
   - Identify specific components, patterns, or concepts to investigate
   - Create a research plan using TodoWrite to track all subtasks
   - Consider which directories, files, or architectural patterns are relevant

### Step 2.5: Architecture Decision Records (ADR) Review

1. **Discover and read all relevant ADRs**:

   - Use Glob to find all ADR files: `.strategic-claude-basic/decisions/ADR_*.md`
   - Read all ADRs with status: accepted, proposed (skip rejected, superseded)
   - Extract key decisions, rationale, and consequences that may impact research
   - Note any decisions that directly affect the research topic or approach

2. **If ADRs are found**, analyze their relevance:

   ```
   Found [N] Architecture Decision Records:
   - ADR-NNNN: [Title] - [Status] - [Relevance to research topic]
   - ADR-NNNN: [Title] - [Status] - [Relevance to research topic]

   These architectural decisions will inform the research approach and findings.
   ```

3. **If no ADRs found**, note this for context:

   ```
   No Architecture Decision Records found in .strategic-claude-basic/decisions/
   Research will proceed without architectural decision constraints.
   ```

4. **Spawn parallel sub-agent tasks for comprehensive research:**

   - Create multiple Task agents to research different aspects concurrently
   - We now have specialized agents that know how to do specific research tasks:

   **For codebase research:**

   - Use the **codebase-locator** agent to find WHERE files and components live
   - Use the **codebase-analyzer** agent to understand HOW specific code works
   - Use the **codebase-pattern-finder** agent if you need examples of similar implementations

   **For web research (only if user explicitly asks):**

   - Use the **web-search-researcher** agent for external documentation and resources
   - IF you use web-research agents, instruct them to return LINKS with their findings, and please INCLUDE those links in your final report

   The key is to use these agents intelligently:

   - Start with locator agents to find what exists
   - Then use analyzer agents on the most promising findings
   - Run multiple agents in parallel when they're searching for different things
   - Each agent knows its job - just tell it what you're looking for
   - Don't write detailed prompts about HOW to search - the agents already know

5. **Wait for all sub-agents to complete and synthesize findings:**

   - IMPORTANT: Wait for ALL sub-agent tasks to complete before proceeding
   - Compile all sub-agent results (both codebase and thoughts findings)
   - Prioritize live codebase findings as primary source of truth
   - Connect findings across different components
   - Include specific file paths and line numbers for reference
   - Highlight patterns, connections, and architectural decisions
   - Answer the user's specific questions with concrete evidence

6. **Gather metadata for research document:**
   Run these commands to gather all required metadata before writing the document:

   ```bash
   # Get current date/time with timezone
   date --iso-8601=seconds

   # Get current git commit hash
   git rev-parse HEAD

   # Get current branch name
   git branch --show-current

   # Get repository name (from remote origin)
   basename -s .git $(git config --get remote.origin.url)

   # Get next document number and create filename
   date '+%d-%m-%Y-%a' | tr '[:upper:]' '[:lower:]'
   ```

   Use these values to populate the frontmatter template. Never create documents with placeholder values.

7. **Generate research document:**

   - Use template: `@.strategic-claude-basic/templates/commands/research.template.md`
   - Replace ALL bracketed placeholders with actual metadata gathered in step 5
   - Follow naming convention from: `@.strategic-claude-basic/research/CLAUDE.md`
   - Include relevant ADR references in frontmatter and findings sections
   - Write document to: `.strategic-claude-basic/research/[filename]` using the naming convention rules
   - Update the `@.strategic-claude-basic/research/CLAUDE.md` file with the new document entry

8. **Present findings:**

   - Present a concise summary of findings to the user
   - Include key file references for easy navigation
   - Reference any relevant ADRs that influenced or constrain the research findings
   - Ask if they have follow-up questions or need clarification

9. **Handle follow-up questions:**
   - If the user has follow-up questions, append to the same research document
   - Update the frontmatter fields `last_updated` and `last_updated_by` to reflect the update
   - Add `last_updated_note: "Added follow-up research for [brief description]"` to frontmatter
   - Add a new section: `## Follow-up Research [timestamp]`
   - Spawn new sub-agents as needed for additional investigation
   - Continue updating the document

## Important notes:

- Always use parallel Task agents to maximize efficiency and minimize context usage
- Always run fresh codebase research - never rely solely on existing research documents
- The @.strategic-claude-basic/research/ directory provides historical context to supplement live findings
- Review and consider all relevant ADRs to ensure research aligns with architectural decisions
- Focus on finding concrete file paths and line numbers for developer reference
- Research documents should be self-contained with all necessary context
- Each sub-agent prompt should be specific and focused on read-only operations
- Consider cross-component connections and architectural patterns
- Include temporal context (when the research was conducted)
- Keep the main agent focused on synthesis, not deep file reading
- Encourage sub-agents to find examples and usage patterns, not just definitions
- **File reading**: Always read mentioned files FULLY (no limit/offset) before spawning sub-tasks
- **Critical ordering**: Follow the numbered steps exactly
  - ALWAYS read mentioned files first before spawning sub-tasks (step 1)
  - ALWAYS wait for all sub-agents to complete before synthesizing (step 4)
  - ALWAYS gather metadata before writing the document (step 5 before step 6)
  - NEVER write the research document with placeholder values
- **Frontmatter consistency**:
  - Always include frontmatter at the beginning of research documents
  - Keep frontmatter fields consistent across all research documents
  - Update frontmatter when adding follow-up research
  - Use snake_case for multi-word field names (e.g., `last_updated`, `git_commit`)
  - Tags should be relevant to the research topic and components studied
