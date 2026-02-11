---
name: nexport-user-docs
description: Update NexPort Campus end user documentation in https://github.com/NexPort-Solutions/NexPort-Campus-Documentation, including release announcements, SUMMARY.md, and What's New. Use when asked to add/modify user docs or align docs with a NexPort Campus release branch; handles branch selection rules, scratch checkout, and optional branch mapping updates.
---

# NexPort User Docs Workflow

## Defaults

- Prefer checkout in the workspace `.scratch/` directory (safe, non-committed).
- Use Windows git binary for any `/mnt/**` path: `"/mnt/c/Program Files/Git/bin/git.exe"`.
- Determine the docs default branch by reading `origin/HEAD` (do not assume `main`).

## Branch Selection Rules

1. If campus branch is `6.x.x`, use docs branch `gitbook`.
2. If a docs branch matches the campus branch exactly, use it.
3. If no exact match:
   - Use the **nearest lower minor** in the same major (e.g., campus `7.1.x` -> docs `7.0.0`).
   - If no lower minor exists, ask for confirmation before proceeding.
4. For non-6.x branches with no match and no clear lower minor, ask first.

Keep the mapping matrix in `references/branch-matrix.md` updated when a new decision is made.
If the project’s `AGENTS.md` has a branch mapping section, update it to match the matrix.

## Minimal Procedure

1. Resolve campus branch (ask if not provided).
2. Fetch docs repo branches and default branch:
   - `git ls-remote --heads <docs-repo-url>`
   - `git symbolic-ref refs/remotes/origin/HEAD` (after clone/fetch)
3. Choose docs branch per rules above.
4. Clone into `.scratch/` (or reuse existing checkout). Example:
   - `.scratch/nexport-user-docs` or `.scratch/nexport-6-user-docs`
5. Make sure you have the latest from the origin
6. Read the agents.md in the docs folder
7. Make doc changes.
8. Update `SUMMARY.md` and `getting-started/whats-new/README.md` if a new release entry is added.
9. Show `git status --short`, commit, and push.

## Branch Mapping Matrix

Update `references/branch-matrix.md` when new mappings are chosen or when rules change.
