---
name: nexport-kendo-grid-edit-patterns
description: "NexPort skill: nexport-kendo-grid-edit-patterns."
---

# Skill: nexport-kendo-grid-edit-patterns

## When to use
- Kendo grid/list surfaces or grid-to-form migrations.

## Checklist
- Use DataSourceRequest for paging/sorting; server filtering for remote search endpoints only.
- Use Razor partials for row templates (ClientRowTemplate/ClientAltRowTemplate).
- For complex edits, migrate to a dedicated form view with shared partial.
- Ensure permissions and localization are enforced in both grid and form.

## References
- patterns/kendo-grid-to-form-pattern.md
- AGENTS.md: Kendo/UI rules.
