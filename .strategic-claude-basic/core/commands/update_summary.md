---
description: "Update an existing summary document with latest implementation progress"
argument-hint: <summary_file_path>
allowed-tools: Read(./**), Write(./.strategic-claude-basic/summary/**), Bash(git:*, date:*, grep:*), Glob
model: claude-opus-4-1
---

You are tasked with updating existing implementation summaries by analyzing the current work session and intelligently merging new findings with existing problems and incomplete work. You should be smart enough to detect if the wrong summary document was provided and only update summaries that are specific to the current work.

**Summary file to update:** $1

## Initial Response

When this command is invoked:

1. **Check if summary file path was provided**:

   - If summary file path was provided, proceed with validation
   - If no summary file provided, respond with:

   ```
   I'll update an existing summary document with your latest implementation progress.

   Please provide the summary file path to update:
   Example: `/update_summary @.strategic-claude-basic/summary/SUMMARY_PLAN_0001_07-09-2025_sat_user-auth.md`

   I'll validate that the summary matches your current work and intelligently merge new progress.
   ```

   Then wait for the user's input.

## Process Steps

### Step 1: Summary Document Validation

1. **Verify summary document exists and is valid**:

   ```bash
   # Check if file exists
   test -f "$1" && echo "File exists" || echo "File not found"

   # Check if it's in the correct directory
   echo "$1" | grep -q "\.strategic-claude-basic/summary/" && echo "Correct directory" || echo "Wrong directory"
   ```

2. **Parse existing summary document**:

   - Read the complete summary document
   - Extract frontmatter metadata (plan_reference, phase, status, completion_rate, etc.)
   - Identify all existing issues (Critical, Incomplete, TODOs, Discovered)
   - Note files mentioned in the "Files Modified/Created" section
   - Extract the original creation date and last_updated

3. **Validate summary document format**:

   - Verify it follows the standard summary template structure
   - Check that it has proper frontmatter with required fields
   - Confirm it's actually a summary document (not a plan or research doc)
   - If invalid format, respond with error and guidance

### Step 2: Work Session Correlation Analysis

1. **Analyze current uncommitted changes**:

   ```bash
   # Check what files are currently modified
   git status --porcelain

   # Get detailed changes
   git diff
   git diff --cached
   ```

2. **Correlate with summary document**:

   - Compare currently modified files with files mentioned in summary
   - Check if the plan_reference matches current work context
   - Look for evidence that this summary is related to current session
   - Analyze conversation context for plan/task references

3. **Smart mismatch detection**:

   If correlation analysis suggests wrong summary:

   ```
   ⚠️ POTENTIAL MISMATCH DETECTED

   The summary you provided appears to be for: [extracted task/plan]
   But your current work session shows changes to: [current files]

   Current modified files:
   - [file1] - [change type]
   - [file2] - [change type]

   Summary mentions these files:
   - [summary_file1] - [from summary]
   - [summary_file2] - [from summary]

   Let me search for a better matching summary...
   ```

   **Auto-search for correct summary**:
   - Use Glob to find all summary files: `@.strategic-claude-basic/summary/SUMMARY_*.md`
   - Read recent summaries to find one that matches current work
   - Suggest the correct summary if found
   - Ask for confirmation before proceeding

### Step 3: Session-Scoped Progress Analysis

**CRITICAL**: Only analyze changes since the summary's `last_updated` timestamp or since last commit.

1. **Identify changes since last update**:

   ```bash
   # Get commits since summary was last updated
   git log --oneline --since="[last_updated_date]"

   # Check what was modified since then
   git diff --name-status HEAD~[N]..HEAD
   ```

2. **Analyze progress on existing issues**:

   For each issue in the current summary:
   - Check if related files were modified
   - Look for test results that might indicate resolution
   - Search for TODO comments that might have been resolved
   - Identify any new related problems

3. **Discover new issues from current session**:

   - Search for new TODO comments in modified files
   - Look for new FIXME, HACK, or similar markers
   - Check for test failures from conversation context
   - Identify incomplete implementations in current changes

4. **Calculate progress metrics**:

   - Determine how many existing issues were resolved
   - Count new critical issues discovered
   - Estimate updated completion percentage
   - Assess if overall status changed (partial → complete, etc.)

### Step 4: Intelligent Issue Merging

1. **Issue Resolution Tracking**:

   For issues that appear to be resolved:
   - Move to new "Resolved Issues" section
   - Add resolution timestamp and commit reference
   - Include brief description of how it was resolved
   - Keep original issue details for traceability

   **Example resolved issue format**:
   ```markdown
   ### Resolved Issues

   Issues that were resolved during this update:

   - ✅ **CLI Flag Parsing Error Messages** (RESOLVED 17-09-2025) - Fixed flag format inconsistencies
     - **Resolution**: Updated all test files to use proper short flag names (-d instead of -depth)
     - **Commit**: a498b3c - Fix CLI flag parsing tests
     - **Original Issue**: Tests failing due to incorrect flag format expectations
   ```

2. **New Issue Integration**:

   Add new issues discovered in current session:
   - Place in appropriate category (Critical, Incomplete, TODOs, Discovered)
   - Include session context about when/how discovered
   - Mark clearly as new in this update
   - Maintain existing issue numbering/priorities

3. **Issue Status Updates**:

   For ongoing issues that had progress:
   - Update the issue description to reflect current status
   - Add progress notes with timestamps
   - Adjust priority or impact assessments if changed
   - Include any new context discovered

### Step 5: Metadata and Document Updates

1. **Update frontmatter metadata**:

   ```yaml
   ---
   date: [KEEP ORIGINAL DATE] # Preserve original creation date
   git_commit: [CURRENT COMMIT HASH] # Update to current HEAD
   branch: [CURRENT BRANCH]
   repository: [REPOSITORY NAME]
   plan_reference: [KEEP ORIGINAL] # Don't change plan reference
   phase: [KEEP OR UPDATE IF PHASE CHANGED]
   status: [UPDATE BASED ON PROGRESS] # complete | blocked | partial
   completion_rate: "[UPDATED %] complete"
   critical_issues: [NEW COUNT] # Recalculated count
   last_updated: [CURRENT DATE YYYY-MM-DD] # Update to today
   ---
   ```

2. **Update document sections**:

   **Overview**: Update with current status, keeping historical context
   **Outstanding Issues**: Merge new/resolved/updated issues intelligently
   **Implementation Summary**: Add new work completed
   **Files Modified**: Add any new files modified in current session
   **Problems Needing Attention**: Update based on current critical issues

3. **Add update tracking**:

   Include an "Update History" section at the bottom:
   ```markdown
   ## Update History

   - **17-09-2025**: CLI flag parsing fixes implemented, config path truncation bug discovered
   - **16-09-2025**: Original summary created
   ```

### Step 6: Document Generation and Validation

1. **Generate updated document**:

   - Preserve the original filename (don't create a new file)
   - Maintain document structure and formatting
   - Include all original content that's still relevant
   - Add new content in appropriate sections

2. **Update summary directory index**:

   - Update `.strategic-claude-basic/summary/CLAUDE.md`
   - Modify the entry for this summary to reflect new status
   - Update completion rates and issue counts in the index
   - Add note about latest update date

3. **Validation checks**:

   - Ensure document still follows template structure
   - Verify all placeholders are filled
   - Check that references are still valid
   - Confirm metadata consistency

### Step 7: Present Update Results

1. **Present comprehensive update summary**:

   ```
   Updated summary document: [filename]

   Progress Summary:
   ✅ Resolved Issues: [N] (moved to Resolved Issues section)
   🆕 New Issues: [N] (added to appropriate categories)
   📝 Updated Issues: [N] (progress or status changes)
   📈 Completion: [old%] → [new%]
   🔍 Status: [old] → [new]

   Key Changes This Session:
   - [Major progress item 1]
   - [Major progress item 2]
   - [New critical issue discovered]

   Issues Still Requiring Attention:
   1. **[Most critical issue]** - [brief description]
   2. **[Second critical issue]** - [brief description]

   The summary has been updated with your latest progress and is ready for review.
   ```

## Important Guidelines

1. **Preserve Historical Context**:

   - Never delete original issues - mark them as resolved instead
   - Keep original creation date and metadata
   - Maintain traceability of issue progression
   - Preserve author intent and original problem descriptions

2. **Be Session-Scoped**:

   - Only analyze changes since last summary update
   - Don't audit the entire codebase for new issues
   - Focus on progress and problems from current work session
   - Use conversation context to understand what was worked on

3. **Smart Correlation**:

   - Detect when wrong summary is provided
   - Auto-suggest correct summary when possible
   - Validate that update makes sense given current work
   - Refuse to update if no relevant changes found

4. **Maintain Quality**:

   - Follow existing summary template structure
   - Keep consistent formatting and style
   - Update completion percentages realistically
   - Ensure all references remain valid

5. **Resolution Tracking**:

   - Create clear audit trail of what was resolved
   - Include commit references for resolutions
   - Maintain issue history for future reference
   - Don't lose information when marking things complete

## Common Scenarios

### Scenario 1: Progress on Existing Plan

When updating a summary for ongoing plan work:

- Match plan reference and verify current work relates to that plan
- Track progress on specific plan phases or tasks
- Update completion percentage based on plan requirements
- Add new issues discovered during plan execution

### Scenario 2: Bug Fix Session

When fixing issues identified in summary:

- Move resolved issues to "Resolved Issues" section
- Update affected issue statuses
- Add any new issues discovered during fixes
- Update overall completion if major blockers removed

### Scenario 3: Test Implementation

When adding tests after implementation:

- Update incomplete tasks related to testing
- Add any new test failures as critical issues
- Increase completion percentage for test coverage
- Move testing-related incomplete items to resolved

### Scenario 4: Wrong Summary Provided

When user provides unrelated summary:

- Detect mismatch through file analysis
- Search for correct summary automatically
- Suggest the right summary to update
- Explain why the provided summary doesn't match

## Error Handling

### File Not Found
```
❌ Summary file not found: [path]

Please check the file path and try again.
Use: `ls .strategic-claude-basic/summary/` to see available summaries
```

### Wrong Directory
```
❌ File is not in the summary directory

Summary files must be in: .strategic-claude-basic/summary/
Use: `/update_summary @.strategic-claude-basic/summary/SUMMARY_...`
```

### Invalid Format
```
❌ File is not a valid summary document

The file appears to be a [plan/research/other] document.
Summary files have frontmatter with fields like: completion_rate, critical_issues
```

### No Relevant Changes
```
⚠️ No relevant changes found since last update

The summary was last updated on [date] and I don't see any changes related to this work.
If you've been working on this task, please make sure you have uncommitted changes or specify what you'd like me to update.
```

### Mismatch Detected
```
⚠️ This summary doesn't appear to match your current work

Summary is about: [task from summary]
Your current changes are in: [files from git status]

I found a better matching summary: [suggested file]
Would you like me to update that instead? (y/n)
```

## Success Criteria

A successful update should:

- **Preserve all valuable historical information** from the original summary
- **Accurately reflect progress** made in the current session
- **Add new issues or problems** discovered during current work
- **Mark resolved issues** with proper timestamps and context
- **Update completion metrics** realistically based on progress
- **Maintain document quality** and template compliance
- **Provide clear audit trail** of what changed and when

The updated summary should be immediately useful for understanding current status and what work remains to be done.
