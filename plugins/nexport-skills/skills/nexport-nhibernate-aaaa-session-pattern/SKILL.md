---
name: nexport-nhibernate-aaaa-session-pattern
description: "Apply the NexPort NHibernate AAAA session pattern for controller and service tests: fresh session/transaction per phase, explicit initial asserts, and deterministic multi-step flow setup."
---

# Skill: nexport-nhibernate-aaaa-session-pattern

## When to use
- Adding or updating tests that touch NHibernate-backed behavior.
- Writing multi-step MVC/controller tests that depend on session state.
- Debugging flaky tests likely caused by stale identity-map/session state.

## Core pattern (AAAA with session boundaries)
- `Arrange`: seed only required test data in a dedicated session + transaction.
- `Initial Assert`: prove preconditions in a fresh read session.
- `Act`: execute one behavior under test in a fresh session/host.
- `Assert`: verify final state in a fresh read session.
- Optional `Cleanup`: only when fixture isolation cannot rely on normal tear-down.

Each phase owns its own session scope. Never reuse the same NHibernate session across phases.

## Session and transaction discipline
- Open sessions with `SessionProvider.OpenSession("<context>")` inside `using` blocks.
- Wrap writes with `using var transaction = session.BeginTransaction(IsolationLevel.ReadCommitted);`.
- Commit explicitly at phase end (`transaction.Commit();`).
- Use rollback only for intentional temporary setup.
- Do not nest helper sessions/transactions under an existing unit of work unless explicitly designed.

## Controller test adaptation
- Rebuild/rehydrate controller host context between multi-step actions when needed.
- Treat Http session keys as explicit test inputs, not incidental leftovers.
- Before each `Act` in a session-backed flow, prime full key contract (example ticket flow):
  - `Ticket`
  - `Requested_Username`
  - `Requested_Password`
- Add explicit precondition asserts for required session values before invoking the action.

## Failure signatures and likely causes
- Redirect mismatch (`ShowFinal` vs `Redeem`) in multi-step flows:
  - Usually missing or stale session contract before `Act`.
- Intermittent auth/DB failures after sign-in flow changes:
  - Often duplicate sign-in/commit paths or overlapping DB work on same flow.
- SQL timeout around tree updates / `UpdatingLeftright`:
  - Arrange too broad or nested transactions; split setup into smaller committed units.

## Test filter reliability
- If a fully qualified filter returns 0 tests, retry with a stable class/name filter.
- Treat `No test matches the given testcase filter` as a failed verification of the intended run.

## Regions convention
Wrap longer tests with:
- `#region Arrange`
- `#region Initial Assert`
- `#region Act`
- `#region Assert`
- `#region Cleanup` (optional)

## Reference source
- `docs/development/unit-test-session-pattern.md`
