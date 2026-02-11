---
name: research-orchestration
description: Research workflow for when a question requires investigation or validation. Use to coordinate local repo context + Quick Memory, Microsoft Learn docs MCP (for Microsoft/Azure topics), Context7 MCP (for programming libraries), and web searches for up-to-date or niche info.
---

# Research Orchestration

Use this skill to structure investigations when you need to research a subject before responding.

## Workflow

1) **Check local context first**
   - Scan relevant `docs/` and repo files before external research.

2) **Query organizational memory**
   - Use `mcp__quick-memory__searchEntries` to find prior decisions, notes, or related work.
   - Use `mcp__quick-memory__listRecentEntries` if the topic is broad or you need a quick recap.

3) **Use the right first‑party source MCPs**
   - **Microsoft/Azure topics** → `mcp__microsoft_learn_docs__microsoft_docs_search` then `mcp__microsoft_learn_docs__microsoft_docs_fetch` for primary guidance and code.
   - **Programming libraries/frameworks** → `mcp__context7__resolve-library-id` then `mcp__context7__query-docs` for accurate, versioned docs.

4) **Web research (when needed)**
   - Use `web.run` for up‑to‑date, niche, or non‑Microsoft topics and to validate anything time‑sensitive.
   - Prefer authoritative sources and cite them in the response.

5) **Synthesize + record**
   - Summarize findings with sources and assumptions.
   - If this work updates ongoing decisions, log the result via Quick Memory (avoid secrets/PII).

## Notes
- Keep results scoped and actionable; avoid speculative guidance.
- Favor primary sources; document gaps if authoritative guidance is missing.
- For Azure Automation issues involving variables/secrets, check Automation variable docs (complex types and encrypted variables can return non-string objects from `Get-AutomationVariable`).
