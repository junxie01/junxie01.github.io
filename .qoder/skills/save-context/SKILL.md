---
name: save-context
description: Update PROJECT_SUMMARY.md with the latest project state to preserve context across sessions. Use when the user wants to save progress, checkpoint the session, or before closing a long conversation. Triggered by "/save-context" or when the user mentions saving context, updating summary, or ending the session.
---

# Save Context

Scan the SEISAMUSE project, update `PROJECT_SUMMARY.md` with the current state, and remind the user to start a new conversation.

## Workflow

### Step 1: Read current state

1. Read `PROJECT_SUMMARY.md` to understand existing documented state
2. Read `build.py` to check for new build features or configuration changes
3. List `content/links/` for any new link sub-pages
4. List `content/posts/` and count total posts
5. List `templates/` for any new or changed templates
6. List `.qoder/skills/` for any new skills
7. Check `content/scripts/` for new scripts
8. Check recent git changes if available: `git log --oneline -20` and `git diff --stat HEAD~5`

### Step 2: Detect changes

Compare what you found against what `PROJECT_SUMMARY.md` currently documents. Identify:
- New features not yet listed
- New files or directories not yet listed
- Changed file counts (e.g., post count increased)
- New skills added
- New link sub-pages added
- Any architectural changes (new templates, new build steps)

### Step 3: Update PROJECT_SUMMARY.md

Rewrite `PROJECT_SUMMARY.md` preserving the existing structure but updating all sections:

```markdown
# SEISAMUSE Project Summary

## Quick Reference for New Sessions

### What This Is
[Keep existing description]

### Key Files
[Update table with any new important files]

### Features Implemented
[Update checklist — mark new features with [x], keep all existing ones]

### Skills Available
[List all skills in .qoder/skills/]

### Common Tasks
[Keep existing, add any new common tasks discovered]

### URLs (after build)
[Update with any new URL patterns]

### Deployment
[Keep existing]

---
Last updated: [TODAY'S DATE in YYYY-MM-DD format]
```

**Important rules for the update:**
- NEVER remove existing entries — only add or update
- Keep the format clean and scannable
- Use exact file paths relative to project root
- Update the "Last updated" date to today
- Keep it under 100 lines — be concise

### Step 4: Notify the user

After updating, display a brief summary of what changed, then show this message:

```
✅ PROJECT_SUMMARY.md has been updated.

📋 Changes captured:
[list what was added/updated]

💡 Recommendation: Close this conversation and start a new one.
   The new session will read PROJECT_SUMMARY.md to pick up where you left off.
```
