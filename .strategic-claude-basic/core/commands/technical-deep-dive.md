---
description: "Conduct comprehensive technical deep dive analysis of the current repository to extract architecture patterns, algorithms, and implementation strategies"
argument-hint: <focus_area> [optional_description]
allowed-tools: Read(./**), Write(./strategic-claude-basic/research/**), Task, Bash(mkdir:*, git:*, date:*), Glob
model: claude-opus-4-1
---

You are tasked with conducting comprehensive technical deep dive analysis of the current repository to extract architectural patterns, algorithmic choices, and implementation strategies that can be learned from and adapted.

**Focus area provided:** $1

## Technical Deep Dive Process

If no focus area was provided or if you need to specify what to analyze, please tell me:
**What technical area or focus would you like me to analyze in depth?**

**IMPORTANT EXCLUSIONS**: When analyzing the codebase, **IGNORE** these directories entirely:

- `.claude/` - Claude Code internal files
- `.serena/` - Serena MCP server files
- `.strategic-claude-basic/` - Our own documentation and research files

Focus only on the actual project source code and implementation.

1. **Read any directly mentioned files first:**

   - If the user mentions specific files (docs, configs, source files), read them FULLY first
   - **IMPORTANT**: Use the Read tool WITHOUT limit/offset parameters to read entire files
   - **CRITICAL**: Read these files yourself in the main context before spawning any sub-tasks
   - This ensures you have full context before decomposing the technical analysis
   - **Remember**: Skip `.claude/`, `.serena/`, and `.strategic-claude-basic/` directories

2. **Analyze and decompose the technical deep dive:**

   - Break down the analysis into composable technical research areas
   - Take time to think deeply about architectural patterns, algorithms, and implementation strategies
   - Identify specific components, design patterns, or technical concepts to investigate
   - Create a technical analysis plan using TodoWrite to track all subtasks
   - Consider which directories, files, or technical patterns are most relevant to the focus area
   - Focus on extracting insights across these technical dimensions:
     - **Algorithmic Intelligence**: Core algorithms, data structures, mathematical foundations
     - **Architectural Excellence**: Component design, design patterns, abstractions, scalability
     - **Engineering Craftsmanship**: Code quality, testing strategies, build systems, documentation
     - **Technical Innovation**: Novel solutions, creative integrations, performance optimizations
     - **Operational Considerations**: Error handling, monitoring, configuration, security

3. **Spawn parallel sub-agent tasks for comprehensive technical analysis:**

   - Create multiple Task agents to analyze different technical aspects concurrently
   - We have specialized agents for technical deep dive analysis:

   **For codebase technical analysis:**

   - Use the **codebase-locator** agent to find WHERE core implementations and technical components live
   - Use the **codebase-analyzer** agent to understand HOW specific algorithms and patterns work
   - Use the **codebase-pattern-finder** agent to find examples of design patterns and architectural approaches

   **For web research:**

   - Use the **web-search-researcher** agent for external documentation, papers, or technical resources
   - IF you use web-research agents, instruct them to return LINKS with their findings, and INCLUDE those links in your final report

   The key is to use these agents intelligently for technical analysis:

   - Start with locator agents to find core technical implementations
   - Then use analyzer agents on the most promising algorithmic and architectural findings
   - Run multiple agents in parallel when analyzing different technical dimensions
   - Each agent knows its job - tell it what technical area you're investigating
   - Don't write detailed prompts about HOW to search - focus on WHAT to analyze
   - **Always remind agents to exclude `.claude/`, `.serena/`, and `.strategic-claude-basic/` directories**

4. **Wait for all sub-agents to complete and synthesize technical findings:**

   - IMPORTANT: Wait for ALL sub-agent tasks to complete before proceeding
   - Compile all sub-agent results focusing on technical insights
   - Prioritize live codebase findings as primary source of technical truth
   - Connect findings across different technical components and patterns
   - Include specific file paths and line numbers for technical reference
   - Highlight architectural patterns, algorithmic choices, and engineering decisions
   - Answer the technical focus with concrete evidence from the codebase

5. **Gather metadata for technical deep dive document:**
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

6. **Generate technical deep dive document:**

   - Use template: `@.strategic-claude-basic/templates/commands/technical-deep-dive.template.md`
   - Replace ALL bracketed placeholders with actual metadata gathered in step 5
   - Follow naming convention: `RESEARCH_NNNN_DD-MM-YYYY_day_technical-deep-dive-[subject].md`
   - Write document to: `.strategic-claude-basic/research/[filename]` using the naming convention rules
   - Update the `@.strategic-claude-basic/research/CLAUDE.md` file with the new document entry

7. **Present technical findings:**

   - Present a concise summary of technical findings to the user
   - Include key file references for easy navigation to technical implementations
   - Highlight architectural patterns and algorithmic insights discovered
   - Ask if they have follow-up questions or need deeper analysis of specific areas

8. **Handle follow-up questions:**
   - If the user has follow-up questions, append to the same technical deep dive document
   - Update the frontmatter fields `last_updated` and add `last_updated_note` to reflect the update
   - Add a new section: `## Follow-up Analysis [timestamp]`
   - Spawn new sub-agents as needed for additional technical investigation
   - Continue updating the document with deeper technical insights

## Important notes:

- Always use parallel Task agents to maximize efficiency and minimize context usage
- Always run fresh codebase analysis - never rely solely on existing research documents
- The @.strategic-claude-basic/research/ directory provides historical context to supplement live findings
- Focus on finding concrete file paths and line numbers for technical reference
- Technical deep dive documents should be self-contained with all necessary context
- Each sub-agent prompt should be specific and focused on read-only operations
- Consider cross-component connections and architectural patterns
- Include temporal context (when the analysis was conducted)
- Keep the main agent focused on synthesis, not deep file reading
- Encourage sub-agents to find examples and usage patterns, not just definitions
- **File reading**: Always read mentioned files FULLY (no limit/offset) before spawning sub-tasks
- **Directory exclusions**: ALWAYS exclude `.claude/`, `.serena/`, and `.strategic-claude-basic/` directories
- **Critical ordering**: Follow the numbered steps exactly
  - ALWAYS read mentioned files first before spawning sub-tasks (step 1)
  - ALWAYS wait for all sub-agents to complete before synthesizing (step 4)
  - ALWAYS gather metadata before writing the document (step 5 before step 6)
  - NEVER write the technical deep dive document with placeholder values
- **Frontmatter consistency**:
  - Always include frontmatter at the beginning of technical deep dive documents
  - Keep frontmatter fields consistent across all documents
  - Update frontmatter when adding follow-up analysis
  - Use snake_case for multi-word field names (e.g., `last_updated`, `git_commit`)
  - Tags should be relevant to the technical analysis focus and components studied
- **Technical focus**:
  - **Current repository only**: Analyze only the actual project code, not tooling directories
  - **Depth over breadth**: Focus on understanding WHY technical decisions were made
  - **Extractable insights**: Identify patterns that can be adapted to other contexts
  - **Concrete evidence**: Always include specific file paths and code references
  - **Innovation identification**: Highlight novel or particularly elegant technical solutions
  - **Practical application**: Focus on insights that provide actionable technical value

The goal is to create a comprehensive technical knowledge base that enables learning from the engineering practices, architectural decisions, algorithms, and implementation strategies in the current repository, making it a valuable reference for future development work.
