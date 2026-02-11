---
name: qa-ready-to-testing
description: Use when a FogBugz case is ready for QA validation. Trigger on requests like "ready for QA", "send to QA", "move to testing", or "resolve this case". The required action is to set the case status to Resolved (To Testing), not Beta or Production.
---

# Skill: qa-ready-to-testing

## When to use

- User says a case is ready for QA, testing, or handoff.
- User asks to "resolve" an implementation case (Enhancement, Bug, New Feature) after dev is complete.
- User asks what status should be used for QA handoff.

## Required action

- Move the case to `Resolved (To Testing)`.
- Do not skip directly to `Resolved to Beta` or `Resolved to Production`.

## Workflow

1. Confirm target case ID(s).
2. Verify case category is implementation work (`Enhancement`, `Bug`, `New Feature`) unless user explicitly says otherwise.
3. Resolve the case to testing using FogBugz tools.
4. Add a concise progress comment with:
- What changed
- Validation performed
- Known risks or follow-up items
5. Keep assignment/ownership consistent with team conventions unless user requests reassignment.

## Guardrails

- Never include credentials, tokens, connection strings, or customer data in comments.
- If work is incomplete or blocked, do not resolve; keep Active and add blocker notes.
- If multiple cases are requested, resolve each explicitly and report each case ID and final status.

## Expected output to user

- List of case IDs updated.
- Final status for each case (`Resolved (To Testing)`).
- Any cases not updated and why.
