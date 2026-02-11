---
name: nexport-release-announcement
description: Create NexPort Campus release announcements in https://github.com/NexPort-Solutions/NexPort-Campus-Documentation, including drafting the release note, adding the file under getting-started/whats-new, and linking it in SUMMARY.md and getting-started/whats-new/README.md. Use for new releases based on FogBugz cases and deployment date.
---

# NexPort Release Announcement Workflow

## Inputs to Gather

- Version (e.g., 6.7.10)
- Deployment date (date only)
- FogBugz case list (ID + title + short outcome)
- Campus repo branch (if relevant for docs branch selection)

## Branch Selection

Use the branch rules from the NexPort user docs skill or `references/branch-matrix.md` (if present in the workspace). If none is available, ask before choosing a non-6.x branch.

## Drafting Rules

- Always include a **Case Reference Index** at the end.
- Keep upgrade timeline phrasing simple; date only.
- If a behavior is conditional (e.g., auto-grading only, template-dependent variables), state the condition clearly.
- Follow the house style: short intro, Key Enhancements, Why This Release Matters, Upgrade Timeline, Learn More, Case Reference Index.

Use `references/release-template.md` as the base.

## File Placement and Linking

- Create the new file in `getting-started/whats-new/`.
- Add the entry to `SUMMARY.md` under “What’s New?” with newest at top.
- Add a content-ref entry to `getting-started/whats-new/README.md` at the top.

## Validation

- `git status --short`
- Confirm file name and links match the version.
