---
name: nexport-nhibernate-session-guard
description: "NexPort skill: nexport-nhibernate-session-guard."
---

# Skill: nexport-nhibernate-session-guard

## When to use
- NHibernate session/transaction failures ("session closed", timeouts, deadlocks).
- Changes to services that open/replace sessions or manage transactions.

## Checklist
- Verify controller transaction pattern uses CurrentNhibernateSessionAccessor.NhSession = NhSession and explicit BeginTransaction/Commit/Rollback.
- Audit any service that sets CurrentNhibernateSessionAccessor.NhSession; restore previous session when done.
- Avoid nested session/transaction creation in helper/service methods.
- If using a temporary session, scope it and restore the prior session after use.
- For timeouts, look for nested transactions or long-running tree queries holding locks.
- In tests, split Arrange into multiple sessions (org/group creation in its own commit) to avoid `UpdatingLeftright` timeouts.

## Common fixes
- Wrap temporary session usage in a scope that restores the prior accessor session.
- Remove redundant BeginTransaction around helpers that already open transactions.
- Ensure async flows do not outlive the session scope.

## References
- AGENTS.md: NHibernate transactions and timeout diagnostics guidance.
