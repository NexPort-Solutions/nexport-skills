---
name: nexport-ui-tests-startup-troubleshooting
description: "Start/stop and troubleshoot NexPort Playwright UI tests in UiTests env. Use when the app or UiTests endpoints return 404/503, when persona login fails, or when dashboard tools never load during UI tests."
---

# NexPort UI Tests Startup + Troubleshooting

## Startup checklist
- Build the solution (skip web content copy when possible).
- Start `NexportVirtualCampusUiTests` profile with `ASPNETCORE_ENVIRONMENT=UiTests`.
- Confirm liveness by loading `/` or `/Home/Login` (no `/UiTests/Health`).
- Use UiTests endpoints from a same-origin page context:
  - `POST /UiTests/EnsureOrganization?shortName=<ORG>`
  - `POST /UiTests/EnsureTenantPersonas?organizationShortName=<ORG>`
  - `POST /UiTests/LoginAsTenantPersona?persona=sysops&organizationShortName=<ORG>`
- Navigate with org short-name routes and wait for tool loaders to clear.
- Ensure NHibernate Profiler is running or disabled in appsettings; if enabled without the profiler running, the site can stall.
 - If TRX output is large, use the TRX parsing skill to extract failures quickly.

## Known failure modes
- **UiTests endpoints return 404**: confirm `ASPNETCORE_ENVIRONMENT=UiTests` and launch profile.
- **Fetch fails or CORS**: call endpoints via `page.evaluate(fetch('/UiTests/...'))` after `page.goto`.
- **Dashboard assertions fail**: wait for “Loading the tool...” alert to disappear.
- **Tenant profile mismatch**: ensure persona setup reassigns the org subtree to the persona tenant profile.
- **Site stalls on startup**: check NHibernate Profiler settings; disable or run the profiler.
- **Site starts then exits quickly**: check `GetAspNetOutput`, verify no active sessions with `ListAspNetSessions`, then restart once.
- **`ERR_CONNECTION_REFUSED`/localhost not reachable**:
  1. Read startup logs first (`GetAspNetOutput` and session `logFilePath`).
  2. Check for `Overriding address(es)` warnings; this means `--urls` was ignored.
  3. Inspect child app process listeners (Roslyn session PID can be parent `dotnet` only).
  4. Re-target checks/tests to the actual bound endpoint.
- **Playwright timeouts on missing selectors**: inspect server logs for partial-render 500s (ex: `/MyCourses/Enrollments` causing `#enrollment-filters` to never render).
- **Repeated 302 to login after sign-on**: sign-on tokens are single-use; always fetch a fresh URL and allow redirect to set auth cookies.
- **Developer portal route checks**: validate `/developer/api-reference#/` and `/developer/orgs` separately; `/developer/orgs` may redirect to login when unauthenticated.

## Stop / restart
- Prefer `StopAspNet` with the session token.
- If the token is missing, stop by process id (Windows Task Manager or `taskkill`).
- If `StopAspNet` returns `No process is associated with this object`, treat it as non-fatal and verify with `ListAspNetSessions`.
