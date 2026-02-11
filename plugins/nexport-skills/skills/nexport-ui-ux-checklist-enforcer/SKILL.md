---
name: nexport-ui-ux-checklist-enforcer
description: "NexPort skill: review a change set against docs/ui-ux/checklist.md and produce a concrete pass/fail report with file-specific fixes."
metadata:
  short-description: "Enforce NexPort 7.0 UI/UX checklist on a diff"
---

# Skill: nexport-ui-ux-checklist-enforcer

## When to use
- Any UI/UX change (new view, modernization, form, blade, modal, grid, JS behavior change).
- Code review requests where UI/UX regressions are likely.
- Before resolving a UI-facing case to Testing.

## Inputs
- Preferred: a case number and the list of files/PR/diff.
- If not provided: infer the change set from git status/diff.

## Primary references
- Checklist: `docs/ui-ux/checklist.md`
- Guide entrypoint: `docs/ui-ux/README.md`
- Vocabulary: `docs/ui-ux/glossary.md`
- Roles/personas: `docs/roles-and-personas.md`
- Double-submit guarding patterns: `.codex/skills/nexport-ajaxq-request-guarding/SKILL.md`

## Procedure
1) Identify the change set.
   - If working under `/mnt/**`, use Windows git:
     - `"/mnt/c/Program Files/Git/bin/git.exe" status -sb`
     - `"/mnt/c/Program Files/Git/bin/git.exe" diff --name-only HEAD`
2) Categorize touched surfaces (helps apply the checklist efficiently):
   - Views: `**/*.cshtml`
   - Client JS/TS: `**/*.js`, `**/*.ts`
   - Controllers/viewmodels: `**/*Controller.cs`, `**/*ViewModel*.cs`
   - Styles: `**/*.scss`, `**/*.css`
3) Run fast heuristics to find common UX regressions (adjust globs as needed):
   - Inline styles / fixed widths:
     - `rg -n \"\\bstyle=\\\"|width:\\s*\\d|height:\\s*\\d\" NexPortVirtualCampus -g'*.cshtml'`
   - Modal-heavy patterns / hidden complexity:
     - `rg -n \"modal|dialog|kendoWindow\" NexPortVirtualCampus -g'*.cshtml' -g'*.js'`
   - Kendo Form usage (guide prefers normal forms):
     - `rg -n \"kendo(Form|FormBuilder)|Form\\(\\)\" NexPortVirtualCampus -g'*.cshtml' -g'*.js' -g'*.cs'`
   - Multiple submit / long-running actions:
     - `rg -n \"type=\\\"submit\\\"|\\.submit\\(|\\$\\.post\\(|\\$\\.ajax\\(\" NexPortVirtualCampus -g'*.cshtml' -g'*.js'`
   - Shared class collision risks for embedded tools (Swagger/Kendo/third-party widgets):
     - `rg -n \"\\.tab\\b|\\.arrow\\b|\\.link\\b\" NexPortVirtualCampus/wwwroot -g'*.css' -g'*.scss'`
     - `rg -n \"swagger-ui|#swagger-ui\" NexPortVirtualCampus -g'*.cshtml' -g'*.css' -g'*.scss'`
4) Review the change set against each checklist section and record a report.

## Output format (required)
Produce a review report with:
- **Pass/fail per checklist section** (Language, Layout/CRAP, Responsive, No Dead Ends, Forms/Validation, Media, A11y, Performance, Double-submit guards).
- **Findings ordered by severity** with file references.
- **Concrete fix suggestions** tied to NexPort patterns (not generic advice).
- **Validation plan**: which golden flows to manually check or which tests to run.
- **Collision-proofing evidence**: include selector-level computed-style proof for any third-party embed styling fixes.

## Notes / common pitfalls
- Do not “fix” validation by weakening assertions or hiding issues in toasts. Prefer field-level messaging for field-level problems.
- If a blade or modal is introduced, verify focus handling and unsaved-changes behavior; ensure phone behavior is full-screen.
- If a change touches labels/copy, cross-check `docs/ui-ux/glossary.md` and localization patterns.
- For embedded tools (for example Swagger UI), ensure global app classes do not leak visual styles into vendor class names.
