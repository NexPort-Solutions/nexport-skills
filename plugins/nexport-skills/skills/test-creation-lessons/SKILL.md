---
name: test-creation-lessons
description: Repo-specific guidance for creating or updating tests in fogbugz-mcp. Use when the user asks to add tests, expand test coverage, or create new test cases; covers node:test setup, AAAA structure, and payload-focused tests that avoid starting the MCP server or calling FogBugz.
---

# Test Creation Lessons

## Overview
Add pragmatic, low-friction tests that exercise payload shaping and textType behavior without hitting the network. Prefer `node:test`, keep tests deterministic, and avoid starting the MCP server during imports.

## Workflow
1. Check `package.json` for an existing test harness; if none, add a minimal `node --test` script.
2. Keep tests under `test/` using ESM imports.
3. Use AAAA comments (`// Arrange`, `// Assert (initial)`, `// Act`, `// Assert`) to keep intent clear.
4. Prefer testing pure helpers (payload builders / text conversion) instead of handlers that call FogBugz.
5. If a handler is the only seam, refactor to expose a pure helper and export it; add a main-entry guard so imports do not start the MCP server.
6. For markdown conversion, assert for key HTML fragments (`<strong>`, `<em>`, `<h2>`) rather than full HTML to reduce brittleness.
7. Run `npm test` and keep tests fast, side-effect free, and offline.

## Notes
- Do not call FogBugz or require `FOGBUGZ_TOKEN` in tests.
- Keep assertions specific to behavior and avoid normalizing outputs in tests to mask bugs.
- For NexPort NHibernate-backed controller/service tests, use the repo skill `.codex/skills/nexport-nhibernate-aaaa-session-pattern/SKILL.md` to enforce AAAA session boundaries and explicit session precondition asserts.
