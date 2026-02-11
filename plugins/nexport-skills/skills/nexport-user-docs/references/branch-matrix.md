# Docs Branch Mapping Matrix

Purpose: record non-obvious mappings between NexPort Campus branches and NexPort Campus Documentation branches.

## Rules (Current)

- Campus `6.x.x` -> Docs `gitbook`.
- If exact docs branch exists, use it.
- Else use nearest lower minor in same major (e.g., campus `7.1.x` -> docs `7.0.0`).
- If no lower minor exists or ambiguity remains, ask for confirmation.

## Explicit Mappings

| Campus branch | Docs branch | Notes | Date |
| --- | --- | --- | --- |
| 6.x.x | gitbook | Default for 6.x releases | 2026-01-16 |
