---
name: nexport-controller-test-patterns
description: "NexPort skill: nexport-controller-test-patterns."
---

# Skill: nexport-controller-test-patterns

## When to use
- Adding or updating controller tests.

## Checklist
- Use `.codex/skills/nexport-nhibernate-aaaa-session-pattern/SKILL.md` first as the base pattern.
- Follow AAAA pattern (Arrange → Initial Assert → Act → Assert).
- Keep fixture setup explicit; avoid hidden magic in SetUp.
- Validate ModelState with ErrorCount (not IsValid).
- Include logging capture when diagnosing flakiness.
- For DB-heavy Arrange, split org/group creation into its own session/transaction to avoid `UpdatingLeftright` timeouts.
- In multi-step controller flows, re-prime required session keys before each Act step.
- Add explicit initial asserts for required session keys and expected preconditions.
- Rehydrate controller context between steps when test flow changes host/controller instances.

## References
- .codex/skills/nexport-nhibernate-aaaa-session-pattern/SKILL.md
- patterns/controller-test-patterns.md
- patterns/test-logging.md
