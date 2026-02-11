---
name: nexport-fogbugz-ops
description: "NexPort skill: nexport-fogbugz-ops."
---

# Skill: nexport-fogbugz-ops

## When to use

- Creating/updating FogBugz cases, progress reports, or child tasks.

## Checklist

- Use correct project/milestone (Nexport Campus 6: 7.0.0 vs 7.1.0).
- Main Case Details go in the User Story Field
- Prefer `textType: "markdown"` for `edit_case`, `add_comment`, `add_comment_with_attachment`, `resolve_case`, and `reactivate_case` so updates render as rich text.
- Case categories are not always specified but if the user asks for:
  - Enhancement Case -> Category is Enhancement
  - Feature Case -> New Feature Category
  - Bug case -> Bug Category
  - Engineering Task -> Engineer Task Category
  - etc etc etc 
- Areas: use colon-delimited names to emulate hierarchy (e.g., `Assignments:Student Verification Assignment:Editor`) because FogBugz supports only a single area per case.
- Areas: call `list_areas` before creating to avoid duplicates and to capture the `ixArea` for later case assignments.
- Areas: create with `create_area` (requires `ixProject` + `sArea`) and store the returned `ixArea` for follow-on edits.
- Areas: when moving a case, use `edit_case` with `fields.ixArea = <ixArea>` and include a short event note.
- Include Progress, Decisions, Validation, Files, Next steps in stakeholder updates.
- Avoid secrets in case notes.
- For commits, include case number and detailed message; ask for the case number if unknown.

## References

- AGENTS.md: commit and case guidelines.
