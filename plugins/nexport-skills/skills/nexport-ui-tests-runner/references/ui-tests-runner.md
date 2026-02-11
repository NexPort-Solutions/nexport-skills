# UI Tests Runner Reference

## Roslyn MCP commands (preferred)
- List ASP.NET sessions:
  - `roslyn_code_navigator.ListAspNetSessions`
- Read ASP.NET output:
  - `roslyn_code_navigator.GetAspNetOutput`
- Stop ASP.NET session:
  - `roslyn_code_navigator.StopAspNet`
- Build solution:
  - `roslyn_code_navigator.BuildSolution` on `/mnt/e/Sandbox/nexport-core-git-2/NexportVirtualCampus.sln`
  - `additionalArguments`: `-clp:ErrorsOnly`, `/p:SkipWebContentCopy=true`
- Start site:
  - `roslyn_code_navigator.StartAspNet` on `/mnt/e/Sandbox/nexport-core-git-2/NexPortVirtualCampus/NexPortVirtualCampus.csproj`
  - `launchProfile`: `NexportVirtualCampusUiTests`
  - `logToFile: true`
- Run tests:
  - `roslyn_code_navigator.StartTest` or `TestSolution` on `/mnt/e/Sandbox/nexport-core-git-2/NexPort.UiTests/NexPort.UiTests.csproj`
  - Pass `--filter` (never run full suite)

## Windows dotnet.exe fallbacks (WSL /mnt)
- Build:
  - `"$NEXPORT_WINDOTNETdotnet.exe" build E:\\Sandbox\\nexport-core-git-2\\NexportVirtualCampus.sln -c Debug /p:SkipWebContentCopy=true -clp:ErrorsOnly`
- Start site (UiTests profile):
  - `cmd.exe /C "set ASPNETCORE_ENVIRONMENT=UiTests&& C:\\Program Files\\dotnet\\dotnet.exe run --project E:\\Sandbox\\nexport-core-git-2\\NexPortVirtualCampus\\NexPortVirtualCampus.csproj --launch-profile NexportVirtualCampusUiTests"`
- Run UiTests (set BaseUrl for Windows process):
  - `cmd.exe /C "set UiTests__BaseUrl=http://localhost:5068/Nexport&& set ASPNETCORE_ENVIRONMENT=UiTests&& C:\\Program Files\\dotnet\\dotnet.exe test E:\\Sandbox\\nexport-core-git-2\\NexPort.UiTests\\NexPort.UiTests.csproj -c Debug --filter FullyQualifiedName~<TestName>"`

## Log-first checks
- Always read app logs before declaring a startup timeout.
- Always read test status/TRX before assuming a hung test.

## Troubleshooting pointers
- 404 from UiTests endpoints: ensure `ASPNETCORE_ENVIRONMENT=UiTests` and UiTests profile.
- Port 5068 collision: find the PID and stop it before restarting.
- Locked test outputs (`MSB3027/MSB3021`): `taskkill /IM testhost.exe /F`.
