---
name: nexport-ui-tests-runner
description: "Run NexPort Playwright UI tests end-to-end (start/stop site, build, run tests, check logs). Use when asked to run UiTests/Playwright tests, start a UiTests site for tests, or troubleshoot UI test timeouts (always review logs first). Prefer roslyn_code_navigator build/start/test; fall back to Windows dotnet.exe when needed."
---

# NexPort UI Tests Runner

## Workflow
- Identify any running site sessions before starting a new one.
  - Prefer `roslyn_code_navigator.ListAspNetSessions`.
  - If a session exists, read logs first (`GetAspNetOutput`) before assuming a timeout.
  - Stop stale/conflicting sessions with `StopAspNet` (use the token).
- Build the solution before starting the site.
  - Prefer `roslyn_code_navigator.BuildSolution` on `/mnt/e/Sandbox/nexport-core-git-2/NexportVirtualCampus.sln`.
  - Use `additionalArguments`: `-clp:ErrorsOnly` and `/p:SkipWebContentCopy=true`.
- Start the UiTests site with the launch profile.
  - `StartAspNet` project: `/mnt/e/Sandbox/nexport-core-git-2/NexPortVirtualCampus/NexPortVirtualCampus.csproj`
  - `launchProfile`: `NexportVirtualCampusUiTests`
  - `logToFile: true`
- Always inspect logs before concluding the app timed out or failed to bind.
- Do not assume `StartAspNet.urls` is the real listener.
  - Check logs for `Overriding address(es)... Binding to endpoints defined via IConfiguration and/or UseKestrel()`.
  - If present, treat configured Kestrel/appsettings endpoints as authoritative.
  - Verify actual listeners by checking the child app process socket bindings (the Roslyn session PID may be the parent `dotnet` process).
- Preflight before running tests:
  - build succeeds
  - site starts and responds on the actual bound endpoint
  - target route renders expected shell content
- Confirm startup completion by polling the root URL **before** running tests:
  - Hit `http://localhost:5068/` and look for startup markers:
    - If the response contains `id="startup-splash"`, wait and retry.
    - If the response contains `id="startup-failed-splash"`, stop and report failure.
  - Only run tests after the splash screen is gone.
- Require a known org to keep tests deterministic.
  - Default known org: short name `AEC`, orgId `b68aef6b-32ba-4822-bec7-9636b4dc594f`.
  - If the environment differs, swap to a pre-seeded org and document the values before running tests.
- Preflight org routing before running tests.
  - Navigate to `http://localhost:5068/AEC/` (or the known org short name) and verify it loads without the org picker.
- Treat UiTests helper endpoints as POST-only.
  - Use POST for `/UiTests/*` calls; GETs can 404/405 even when the site is healthy.
- Sign-on URLs are single-use and short-lived.
  - Always fetch a fresh sign-on URL immediately before navigation and avoid reusing tokens.
  - Follow the server redirect after sign-on so the auth cookie is set.
- Run UI tests.
  - Prefer `roslyn_code_navigator.StartTest` or `TestSolution` on `/mnt/e/Sandbox/nexport-core-git-2/NexPort.UiTests/NexPort.UiTests.csproj`.
  - Use filters when possible (do not run full suite).
  - If a timeout occurs, read test status/logs first (`GetTestStatus`, `GetTestTrx`) before retrying.
  - For large TRX outputs, use the TRX parsing skill/scripts to extract failures quickly.
  - If startup tasks appear stuck and the splash never clears, consider restarting the local SQL Server instance before retrying.
  - If Roslyn StartAspNet/Test session disappears unexpectedly, check `ListAspNetSessions`, restart once, then retry.
  - If manual route probes fail but startup logs show normal app execution, proceed with targeted `Category=UiSmoke` and use test outcomes as pass/fail authority.
  - Capture at least one screenshot plus selector-level computed-style evidence for CSS regression failures.

## Fallbacks (when Roslyn MCP is unavailable)
- Build with Windows dotnet:
  - `"$NEXPORT_WINDOTNETdotnet.exe" build E:\\Sandbox\\nexport-core-git-2\\NexportVirtualCampus.sln -c Debug /p:SkipWebContentCopy=true -clp:ErrorsOnly`
- Start the site with Windows dotnet (UiTests profile):
  - `cmd.exe /C "set ASPNETCORE_ENVIRONMENT=UiTests&& C:\\Program Files\\dotnet\\dotnet.exe run --project E:\\Sandbox\\nexport-core-git-2\\NexPortVirtualCampus\\NexPortVirtualCampus.csproj --launch-profile NexportVirtualCampusUiTests"`
- Run UI tests with Windows dotnet (ensure BaseUrl is set for the Windows process):
  - `cmd.exe /C "set UiTests__BaseUrl=http://localhost:5068/Nexport&& set ASPNETCORE_ENVIRONMENT=UiTests&& C:\\Program Files\\dotnet\\dotnet.exe test E:\\Sandbox\\nexport-core-git-2\\NexPort.UiTests\\NexPort.UiTests.csproj -c Debug --filter FullyQualifiedName~<TestName>"`
- If MSB3027/MSB3021 (locked outputs), kill stale `testhost.exe` and retry:
  - `taskkill /IM testhost.exe /F`

## Log-first rules (do not skip)
- Always check site logs via `GetAspNetOutput` (or the log file path from `StartAspNet`) before calling a startup a “timeout.”
- Always check test logs (`GetTestStatus`/`GetTestTrx`) before assuming the suite hung.
- If Playwright waits for a selector that never appears, check the app log for 500s in partials (e.g., MyCourses/Enrollments).
- If `StopAspNet` reports `No process is associated with this object`, confirm with `ListAspNetSessions`; this is often normal when the host already exited.

## References
- `NexPort.UiTests/README.md` for configuration and local seeding notes.
- `.codex/skills/nexport-ui-tests-startup-troubleshooting/SKILL.md`
- `.codex/skills/nexport-playwright-ui-test-patterns/SKILL.md`
- `.codex/skills/nexport-trx-parsing/SKILL.md`
- `references/ui-tests-runner.md` (command crib sheet)
