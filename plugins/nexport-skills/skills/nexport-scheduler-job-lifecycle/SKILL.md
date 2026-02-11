---
name: nexport-scheduler-job-lifecycle
description: "NexPort skill: nexport-scheduler-job-lifecycle."
---

# Skill: nexport-scheduler-job-lifecycle

## When to use
- Implementing a new scheduler job or extending existing job behavior.

## Checklist
- Implement IAsyncJob and Interruptable job base for NSS jobs.
- Register job in scheduler configuration and ensure correct DI lifetimes.
- Add health provider only when needed; register as scoped.
- If adding observability, wire IJobDetailsResolverService + detail view.

## Common pitfalls
- Registering job health providers as singleton while using scoped dependencies.

## References
- patterns/scheduler-job-observability-pattern.md
- AGENTS.md: NSS jobs guidance.
