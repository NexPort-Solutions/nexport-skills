---
name: nexport-tree-permission-queries
description: "NexPort skill: nexport-tree-permission-queries."
---

# Skill: nexport-tree-permission-queries

## When to use
- Any query that must be scoped to a user's permitted org/group tree.
- Building read-only grid models that need TreeLeft/TreeRight for server filtering.

## Checklist
- Start from user's granted root groups and build tree ranges.
- Use tree ranges to constrain descendant queries (avoid listing IDs).
- For grids, prefer a read-only mapped view/subselect with TreeLeft/TreeRight (no proxies).
- Avoid LinqKit when building NHibernate LINQ queries.

## References
- patterns/treedata-proxies.md
- AGENTS.md: Permission-scoped queries guidance.
