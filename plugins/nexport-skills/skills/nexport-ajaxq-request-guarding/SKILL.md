---
name: nexport-ajaxq-request-guarding
description: "NexPort skill: when and how to use ajaxq + beforeSend guards to prevent duplicate AJAX requests."
---

# Skill: nexport-ajaxq-request-guarding

## When to use
- UI actions trigger rapid, duplicate AJAX calls (tree selection, filters, typeahead, toggles).
- Requests must be serialized (new call should wait for the previous one).
- There is a client-side “already set” check but the request still fires.
- Server logs show redundant operations or user clicks cause request storms.

## Checklist
- Add a `beforeSend` guard to skip the request when the target state is already current.
- Route the call through `ajaxq` with a stable, feature-specific queue name (e.g., `orgManagement.setGroup`).
- Keep endpoints idempotent or dedupe with a last-request signature.
- Validate behavior in the browser console and confirm fewer server hits.

## References
- `patterns/ajaxq-request-guarding.md` (primary).
