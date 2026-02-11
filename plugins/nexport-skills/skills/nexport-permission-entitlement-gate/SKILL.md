---
name: nexport-permission-entitlement-gate
description: "NexPort skill: nexport-permission-entitlement-gate."
---

# Skill: nexport-permission-entitlement-gate

## When to use
- Any new UI/API/job that must be gated by permissions or feature entitlements.

## Checklist
- Enforce permission checks (e.g., CanViewQuestionAnalytics) at controller entry points.
- Use PermissionScopeResolver or IOrgSelectorService.ValidateAsync for org-scoped validation.
- Use IFeatureCatalog / entitlement resolver as the source of truth for feature access.
- For non-entitled orgs: block config and jobs; show friendly messaging in UI.
- Prefer injecting services into views when entitlement metadata is needed; avoid fragile ViewData wiring.

## Common pitfalls
- Relying only on UI gating without enforcing in services/jobs.
- Failing to validate selected org within user scope.

## References
- AGENTS.md: permissions and entitlement guidance.
