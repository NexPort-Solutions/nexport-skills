---
name: nexport-playwright-ui-test-patterns
description: "NexPort skill: Playwright UI test patterns, including UiTests personas and helper endpoints."
---

# Skill: nexport-playwright-ui-test-patterns

## When to use
- Adding or updating Playwright UI tests.

## Checklist
- Prefer UiTests personas over appsettings credentials.
  - Call `Ensure*Personas` for the target org.
  - Call `LoginAs*Persona` immediately before navigation to get a fresh one-time `signOnUrl`.
  - Navigate to the `signOnUrl` once; reissue a token on retries.
- Use UiTests helper endpoints when available (UiTests env + loopback only).
  - IdP personas: `EnsureIdentityProviderPersonas`, `LoginAsIdentityProviderPersona`.
  - Question Analytics personas: `EnsureQuestionAnalyticsPersonas`, `LoginAsQuestionAnalyticsPersona`.
  - Optional org seed: `EnsureOrganization`.
  - OAuth mock (IdP automation): `GET /UiTests/OAuthMock/authorize`, `POST /UiTests/OAuthMock/token`, `POST /UiTests/OAuthMock/register`.
- Use org short-name routes to preserve org context.
- Avoid back/forward; navigate directly to target URLs.
- Wait for app startup; retry navigation after warm-up timeouts.
- If first navigation times out, retry once after a short wait before treating it as a failure.
- Call UiTests endpoints from an active page context on the same origin
  (e.g., `page.evaluate(fetch('/UiTests/...'))`) to avoid loopback/CORS failures.
- There is no `/UiTests/Health` endpoint; use `/` or `/Home/Login` for a liveness check.
- Treat `/Home/Login` redirects on protected routes as auth/setup preconditions, not styling failures.
- On org dashboard tools, wait for the “Loading the tool...” alert to disappear before asserting.
- Use `UiTestUrlResolver` + `AssertionExtensions.Eventually`; avoid `Thread.Sleep`.
- Keep selectors scoped to modal containers; avoid global `First()` until scoped.
- For style regressions, collect both screenshot and computed-style assertions for impacted selectors.
- If `roslyn_code_navigator` StartAspNet/StartTest returns "Transport closed", fall back to Windows `dotnet.exe` for the run.
- When starting the UiTests site with Windows `dotnet.exe`, prefer Windows paths (`E:\...`) and set `ASPNETCORE_ENVIRONMENT=UiTests`.
- If the site won't start, check for a port collision on `:5068` (`netstat -ano | findstr 5068`) and kill the owning PID.
- Confirm the site is actually listening before running tests; a build can succeed while the host fails to bind.
- Do not assume Roslyn `StartAspNet` URLs are authoritative.
  - If app config/Kestrel overrides `--urls`, resolve the real endpoint from logs and listener sockets.
- If Playwright navigation fails but startup logs and smoke tests are healthy, treat it as endpoint-resolution/tooling context and re-target navigation before changing test logic.

## References
- `references/ui-test-patterns.md` (primary).
- `AGENTS.md` (Playwright MCP guidance + UI testing notes).
