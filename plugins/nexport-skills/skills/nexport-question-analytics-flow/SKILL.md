---
name: nexport-question-analytics-flow
description: "NexPort skill: nexport-question-analytics-flow."
---

# Skill: nexport-question-analytics-flow

## When to use
- Question Analytics UI/API/config changes or seeder updates.

## Checklist
- Keep Apply flow client-driven; use selectors for org/bank/question and post filter.
- Ensure SelectedQuestionIds are echoed in responses for rehydration.
- Validate org scope using IOrgSelectorService.ValidateAsync with CanViewQuestionAnalytics.
- Apply entitlement exclusions (feature catalog) to queries and jobs.
- Surface friendly entitlement messages in UI.
- Org-scoped refresh status drill-ins should be viewable by users with CanViewQuestionAnalytics (not SysOps-only).

## References
- docs/question-ranking/roadmap.md
- QuestionAnalyticsController / QuestionDifficultyStatsService
