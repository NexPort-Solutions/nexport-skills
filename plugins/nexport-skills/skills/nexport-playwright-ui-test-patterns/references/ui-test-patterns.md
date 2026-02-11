# UI Test Patterns (NexPort.UiTests + Playwright, C#)

Fast-start checklist for writing resilient UI tests in `NexPort.UiTests` (Playwright + NUnit).

## Environment & Config
- Tests target an already-running NexPort site. Set `UiTests:BaseUrl` (and optional `BrowserName`) in `appsettings.uitests.json` or `appsettings.tests.json`.
- Credentials:
  - **Preferred (UiTests personas):** use loopback-only UiTests helper endpoints to create deterministic personas and mint single-use login URLs. This avoids hardcoded passwords and reduces drift across environments.
    - Example flow: `Ensure*Personas` → `LoginAs*Persona` → navigate to returned `signOnUrl`.
  - Alternative: store accounts in gitignored `tests.credentials.toml` (copy from `tests.credentials.example.toml`).
    - Reference them via `CredentialKey` in config; `TestCredentialProvider` resolves them.
    - Inline `Username`/`Password` also works but avoid committing real secrets.
- Local deterministic helpers (UiTests environment only):
  - When `UiTests:BaseUrl` points at `localhost`/`127.0.0.1` and the server runs with `ASPNETCORE_ENVIRONMENT=UiTests`, tests may call loopback-only helper endpoints to avoid hardcoded passwords or manual data seeding.
  - Manage Campus IdP tests use:
    - `POST /Nexport/UiTests/SeedIdentityProviders?organizationId=<guid>`
    - `POST /Nexport/UiTests/EnsureIdentityProviderPersonas?organizationId=<guid>`
    - `POST /Nexport/UiTests/LoginAsIdentityProviderPersona?persona=viewer|manager&organizationId=<guid>`
  - Question Analytics + Observability tests can use:
    - `POST /Nexport/UiTests/EnsureQuestionAnalyticsPersonas?organizationId=<guid>` or `?organizationShortName=<shortName>`
    - `POST /Nexport/UiTests/LoginAsQuestionAnalyticsPersona?persona=viewer|sysops&organizationId=<guid>` or `?organizationShortName=<shortName>`
    - `POST /Nexport/UiTests/EnsureOrganization?shortName=<shortName>&name=<displayName>` (optional helper to seed an org for UiTests)
    - The Question Analytics persona endpoint also ensures active subscriptions so org pickers can list the seeded org.
  - Mock OAuth endpoints for IdP automation flows (UiTests-only + loopback):
    - `GET /UiTests/OAuthMock/authorize`
    - `POST /UiTests/OAuthMock/token`
    - `POST /UiTests/OAuthMock/register`
  - These endpoints are only enabled in the UiTests environment and should not be used outside local runs.
- Org inputs:
  - `ManageCampus` routes need org GUIDs (`PrimaryOrganizationId`, optional `ViewerOrganizationId`).
  - Question Analytics tests need an org short name (`QuestionAnalyticsOrgShortName`).
- Browser binaries: run Playwright install once (`pwsh ./NexPort.UiTests/bin/Debug/net8.0-windows/playwright.ps1 install --with-deps`).

## UiTests Controller Pattern (Server-Side Helpers)
- Use `UiTestsController` as the pattern for new test-only endpoints.
- Guardrails are mandatory:
  - Require `ASPNETCORE_ENVIRONMENT=UiTests`.
  - Require loopback requests only (localhost/127.0.0.1).
  - Return `NotFound` or `Forbid` outside those constraints.
- Keep endpoints deterministic and idempotent:
  - Seed data by stable prefixes (e.g., `UiTests:`) so tests can safely re-run.
  - Prefer personas over raw credentials; use `Nickname` to find/create users.
  - Use org short names or explicit org IDs; validate inputs and return clear errors.
- Avoid using ViewData in UI tests:
  - Inject services directly in views/tests when needed (matches current UI patterns and reduces fragility).

## Base Fixtures & Utilities
- Derive tests from `UiTestBase` (inherits `PageTest`):
  - Provides `BaseAddress`, sets `ContextOptions` with `BaseURL` and `IgnoreHTTPSErrors = true`.
  - Honors global `BrowserName` from settings.
- Global setup (`UiTestGlobalSetup`):
  - Reads config, verifies server reachability, ensures Playwright browsers installed.
  - Exposes `CredentialProvider`, `AdminAccount`, `ViewerAccount`, org IDs/short names.
- ILogger capture (`TestLogSink`/`TestLoggerProvider`) applies to `NexPort.Tests` fixtures, not UiTests. See `patterns/test-logging.md` for server-side test logging.
- Logging in: use `AuthenticationHelper.LoginAsync(page, account, CredentialProvider)`; it clears cookies, navigates to `/Home/Login`, fills username/password, waits for redirect.
- UiTests persona sign-on URLs are **single-use**. Treat the returned `signOnUrl` as a one-time navigation token:
  - Always fetch a fresh URL immediately before navigation.
  - Never reuse the same `signOnUrl` (including `Back`/`Forward` or retry navigations).
  - If a navigation fails, request a new token instead of reusing the old one.
- Routes: use `UiTestUrlResolver.Resolve(UiTestRoute, arg)` for consistent paths (e.g., Question Analytics short-name, Manage Campus org id).
- Assertions: use `AssertionExtensions.Eventually` to poll for UI state (default 15s / 250ms) instead of brittle sleeps.

## Writing Tests
- Keep tests focused and non-parallel when they mutate shared UI state (`[NonParallelizable]` for modal-heavy flows).
- Preferred persona login flow:
  - Call `Ensure*Personas` for the org you plan to test.
  - Call `LoginAs*Persona` immediately before navigation to get a fresh `signOnUrl`.
  - Navigate to the `signOnUrl` once; request a new token if navigation fails.
- Favor ARIA-role selectors or stable data hooks/classes used by the components (e.g., `.org-selector-modal`, `.qb-modal`, `.q-modal`).
- When checking selections:
  - Verify both URL query (for applied filters) and visible pills/badges.
  - Reopen modals to confirm rehydration (`IsChecked`/`InnerText` assertions).
- Always wait for elements before interacting (`locator.WaitForAsync()` or `Eventually`).
- Avoid raw `Thread.Sleep`; rely on Playwright waits and `Eventually`.
- For multi-step flows: login → navigate (UrlResolver) → open modal → search/select → apply → assert.

## Test Data & Creds
- Store personal creds only in `tests.credentials.toml`; never commit. Gitignore already covers it.
- If tests need deterministic data, seed it ahead of time (see Question Analytics seeder notes) or restrict to known fixtures (e.g., AST Employee Campus / Test bank in current UI tests).
- Prefer loopback-only UiTests helpers (when available) to create deterministic personas or seed IdP connectors/providers instead of relying on manual SQL or shared accounts.

## Running
```bash
dotnet test NexPort.UiTests/NexPort.UiTests.csproj
```
Optional filters: `--filter FullyQualifiedName~QuestionAnalytics` etc.

## Examples
- `NexPort.UiTests/QuestionAnalytics/QuestionAnalyticsFilterTests.cs` — org→bank→question modal flow, URL + pill assertions, rehydration check.
- `Infrastructure/*.cs` — base classes and helpers (Auth, CredentialProvider, Eventually, UrlResolver).

## Stability Tips
- Keep selectors scoped to modal containers to avoid collisions when multiple dialogs share roles.
- Prefer `.First` only after narrowing scope; otherwise assert counts to catch duplicate matches.
- Use `IgnoreHTTPSErrors = true` via `UiTestBase.ContextOptions` to avoid TLS noise on local certs.
- Keep credentials/org ids in config, not in test code; pull them from `UiTestGlobalSetup`.
