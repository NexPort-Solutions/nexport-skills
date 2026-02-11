---
name: nexport-test-logging-diagnostics
description: "NexPort skill: nexport-test-logging-diagnostics."
---

# Skill: nexport-test-logging-diagnostics

## When to use
- Tests are flaky, timing out, or failing with unclear output.

## Checklist
- Validate test structure against `.codex/skills/nexport-nhibernate-aaaa-session-pattern/SKILL.md` before deep log analysis.
- Enable test log capture per patterns/test-logging.md.
- Keep logs minimal and focused on the failing subsystem.
- Avoid logging secrets or credentials.
- When TRX output is large, use the TRX parsing skill for fast failure extraction.
- Timeout triage: if logs show `Execution Timeout Expired` during `UpdatingLeftright`, split Arrange into separate sessions/transactions and avoid nested Unit of Work.
- Redirect mismatch triage (`ShowFinal` vs `Redeem` or similar): verify session key contract is fully primed for the current action step.
- Auth-flow triage: if failures started after sign-in refactors, verify only one authoritative sign-in/commit path is active.

## References
- .codex/skills/nexport-nhibernate-aaaa-session-pattern/SKILL.md
- patterns/test-logging.md
- .codex/skills/nexport-trx-parsing/SKILL.md
