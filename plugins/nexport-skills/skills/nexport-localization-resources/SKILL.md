---
name: nexport-localization-resources
description: "NexPort skill: nexport-localization-resources."
---

# Skill: nexport-localization-resources

## When to use
- Any user-facing text, DisplayAttributes, enum display names, or DTO/ViewModel labels.

## Checklist
- Use DisplayAttribute with localized Name + Description for enums and view models.
- Follow display-resource segmentation rules; avoid DescriptionAttribute for data annotations.
- Prefer dedicated resx files for new view models.
- Keep localization changes out of generated ResourceGenTemplate files.

## References
- patterns/display-resource-segmentation.md
- AGENTS.md: Localization rules.
