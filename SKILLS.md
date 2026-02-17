# NexPort Skills Catalog

This repo stores packaged Codex skills for NexPort workflows. Packages live under packages/.

## Available Skills

| Skill | Purpose | Package |
| --- | --- | --- |
| es-file-lookup | Use when the user asks to find or locate files by name or path on Windows (e.g., "find file X", "where is Y", "search for *.csproj"). Always use the Everything CLI (es.exe) instead of Get-ChildItem/dir/PowerShell recursion unless es.exe is missing or errors. | packages/es-file-lookup.skill |
| fast-file-io-selection | Select the fastest file-reading method in PowerShell/.NET based on intent (raw bytes, full text, or streaming text). Use when performance matters, when comparing Get-Content vs .NET APIs, or when choosing file IO for large or medium files. | packages/fast-file-io-selection.skill |
| fortigate-change-window-runbook | Execute FortiGate change windows with safe sequencing, explicit validation checkpoints, rollback triggers, and evidence logging for audit-ready operations. | packages/fortigate-change-window-runbook.skill |
| fortigate-log-evidence-normalizer | Parse and normalize FortiGate/FortiCloud/FortiAnalyzer VPN log exports into evidence-ready summaries, including event distributions, success/failure patterns, and schema-gap checks required for control validation. | packages/fortigate-log-evidence-normalizer.skill |
| fortigate-plink-key-bootstrap | Add or update FortiGate admin SSH public keys for PuTTY/plink, enable SSH on the correct FortiGate interface, and verify non-interactive key login with pinned host key fingerprints. | packages/fortigate-plink-key-bootstrap.skill |
| fortigate-vpn-hardening-execution | Execute a phased FortiGate VPN hardening plan with feasibility gates, low-risk sequencing, validation checkpoints, rollback notes, and evidence collection for CMMC/SOC-aligned operations. | packages/fortigate-vpn-hardening-execution.skill |
| nexport-ajaxq-request-guarding | NexPort skill: when and how to use ajaxq + beforeSend guards to prevent duplicate AJAX requests. | packages/nexport-ajaxq-request-guarding.skill |
| nexport-appsec-pre-commit-gate | Run a multi-stack application security review on staged changes before commit (.NET, Python, PHP, Node.js), including dependency vulnerabilities, code scanning, and secrets checks. | packages/nexport-appsec-pre-commit-gate.skill |
| nexport-azure-pipeline-status | Retrieve Azure DevOps pipeline status and troubleshoot failed runs using az devops CLI. Use when asked about pipeline status, failed builds, stage failures, or to inspect recent runs for the current repo’s project. | packages/nexport-azure-pipeline-status.skill |
| nexport-ci-pipeline-hygiene | NexPort skill: nexport-ci-pipeline-hygiene. | packages/nexport-ci-pipeline-hygiene.skill |
| nexport-cold-start | NexPort skill: cold start workflow (Quick Memory + epic discovery + docs anchoring). | packages/nexport-cold-start.skill |
| nexport-controller-test-patterns | NexPort skill: nexport-controller-test-patterns. | packages/nexport-controller-test-patterns.skill |
| nexport-epic-shaping-decomposition | NexPort skill: epic shaping and decomposition with roadmap composition + optional FogBugz epic and child cases. | packages/nexport-epic-shaping-decomposition.skill |
| nexport-fogbugz-ops | NexPort skill: nexport-fogbugz-ops. | packages/nexport-fogbugz-ops.skill |
| nexport-kendo-grid-edit-patterns | NexPort skill: nexport-kendo-grid-edit-patterns. | packages/nexport-kendo-grid-edit-patterns.skill |
| nexport-kendo-upgrade-runbook | Runbook for upgrading Kendo UI/Telerik ASP.NET Core components in NexPort Campus (server-side NuGet + client-side JS/themes via zip assets), including version alignment, zip-first client assets, and required UiSmoke validation before commit. | packages/nexport-kendo-upgrade-runbook.skill |
| nexport-localization-resources | NexPort skill: nexport-localization-resources. | packages/nexport-localization-resources.skill |
| nexport-logging-telemetry-audit | Logging, telemetry, and auditing guidance for NexPort. Use when discussing logging config, Serilog/log4net usage, audit logs, app logs, telemetry events, observability dashboards, or deciding where to record a system/user event. | packages/nexport-logging-telemetry-audit.skill |
| nexport-memory-hygiene | NexPort skill: nexport-memory-hygiene. | packages/nexport-memory-hygiene.skill |
| nexport-nhibernate-aaaa-session-pattern | Apply the NexPort NHibernate AAAA session pattern for controller and service tests: fresh session/transaction per phase, explicit initial asserts, and deterministic multi-step flow setup. | packages/nexport-nhibernate-aaaa-session-pattern.skill |
| nexport-nhibernate-session-guard | NexPort skill: nexport-nhibernate-session-guard. | packages/nexport-nhibernate-session-guard.skill |
| nexport-permission-entitlement-gate | NexPort skill: nexport-permission-entitlement-gate. | packages/nexport-permission-entitlement-gate.skill |
| nexport-playwright-ui-test-patterns | NexPort skill: Playwright UI test patterns, including UiTests personas and helper endpoints. | packages/nexport-playwright-ui-test-patterns.skill |
| nexport-proctoring-host-patterns | NexPort skill: nexport-proctoring-host-patterns. | packages/nexport-proctoring-host-patterns.skill |
| nexport-question-analytics-flow | NexPort skill: nexport-question-analytics-flow. | packages/nexport-question-analytics-flow.skill |
| nexport-release-announcement | Create NexPort Campus release announcements in https://github.com/NexPort-Solutions/NexPort-Campus-Documentation, including drafting the release note, adding the file under getting-started/whats-new, and linking it in SUMMARY.md and getting-started/whats-new/README.md. Use for new releases based on FogBugz cases and deployment date. | packages/nexport-release-announcement.skill |
| nexport-scheduler-job-lifecycle | NexPort skill: nexport-scheduler-job-lifecycle. | packages/nexport-scheduler-job-lifecycle.skill |
| nexport-smoke-test-runner | Run NexPort smoke tests with a consistent prompt that always asks whether UI or unit smoke tests are desired; prefers Roslyn MCP StartTest/TestSolution when available and falls back to Windows dotnet.exe or CLI commands. Use when asked to run smoke tests, tag smoke tests, or validate a quick sanity pass. | packages/nexport-smoke-test-runner.skill |
| nexport-solr-aks-replication | Replicate NexPort Solr deployment on AKS using automation-first az/kubectl workflows. AKS-only; no Tomcat path. | packages/nexport-solr-aks-replication.skill |
| nexport-test-logging-diagnostics | NexPort skill: nexport-test-logging-diagnostics. | packages/nexport-test-logging-diagnostics.skill |
| nexport-tree-permission-queries | NexPort skill: nexport-tree-permission-queries. | packages/nexport-tree-permission-queries.skill |
| nexport-trx-parsing | Parse and summarize TRX test results, extract failures fast, and benchmark TRX parsers (pygixml/ElementTree/xunitparserx/rg). Use when asked to analyze large TRX outputs or compare parsing speed/correctness. | packages/nexport-trx-parsing.skill |
| nexport-ui-fixtures-my-courses | UiTests fixtures for My Courses/My Training coverage (seeding data, login-as, selectors, and common pitfalls). | packages/nexport-ui-fixtures-my-courses.skill |
| nexport-ui-tests-runner | Run NexPort Playwright UI tests end-to-end (start/stop site, build, run tests, check logs). Use when asked to run UiTests/Playwright tests, start a UiTests site for tests, or troubleshoot UI test timeouts (always review logs first). Prefer roslyn_code_navigator build/start/test; fall back to Windows dotnet.exe when needed. | packages/nexport-ui-tests-runner.skill |
| nexport-ui-tests-startup-troubleshooting | Start/stop and troubleshoot NexPort Playwright UI tests in UiTests env. Use when the app or UiTests endpoints return 404/503, when persona login fails, or when dashboard tools never load during UI tests. | packages/nexport-ui-tests-startup-troubleshooting.skill |
| nexport-ui-ux-checklist-enforcer | NexPort skill: review a change set against docs/ui-ux/checklist.md and produce a concrete pass/fail report with file-specific fixes. | packages/nexport-ui-ux-checklist-enforcer.skill |
| nexport-ui-visual-walkthrough | Run a manual UI visual walkthrough/check. Build first with roslyn_code_navigator, start the site with roslyn_code_navigator StartAspNet, then validate pages/interactions with Playwright MCP when available. | packages/nexport-ui-visual-walkthrough.skill |
| nexport-user-docs | Update NexPort Campus end user documentation in https://github.com/NexPort-Solutions/NexPort-Campus-Documentation, including release announcements, SUMMARY.md, and What's New. Use when asked to add/modify user docs or align docs with a NexPort Campus release branch; handles branch selection rules, scratch checkout, and optional branch mapping updates. | packages/nexport-user-docs.skill |
| nexport-vocabulary-glossary-enforcement | NexPort skill: detect user-facing terminology drift and engineer-centric jargon; propose fixes and glossary updates aligned to docs/ui-ux/glossary.md. | packages/nexport-vocabulary-glossary-enforcement.skill |
| php-lint-checks | PHP syntax linting helpers (php -l) and workflows for validating changed files or selected paths. Use when asked to verify PHP syntax, lint modified files, or add quick PHP lint scripts. | packages/php-lint-checks.skill |
| qa-ready-to-testing | Use when a FogBugz case is ready for QA validation. Trigger on requests like "ready for QA", "send to QA", "move to testing", or "resolve this case". The required action is to set the case status to Resolved (To Testing), not Beta or Production. | packages/qa-ready-to-testing.skill |
| research-orchestration | Research workflow for when a question requires investigation or validation. Use to coordinate local repo context + Quick Memory, Microsoft Learn docs MCP (for Microsoft/Azure topics), Context7 MCP (for programming libraries), and web searches for up-to-date or niche info. | packages/research-orchestration.skill |
| sensitive-artifact-scan | Scan project artifacts for sensitive material (for example keys, PSKs, tokens, secrets) and produce remediation actions such as redaction, rotation, and storage-control follow-ups. | packages/sensitive-artifact-scan.skill |
| sysops-project-kickoff | End-to-end workflow for SysOps projects/cases (kickoff, planning, execution, validation, progress updates). Use for starting or maintaining SysOps projects, updating plans/phases, tracking progress, or organizing case work across the full lifecycle. | packages/sysops-project-kickoff.skill |
| test-creation-lessons | Repo-specific guidance for creating or updating tests in fogbugz-mcp. Use when the user asks to add tests, expand test coverage, or create new test cases; covers node:test setup, AAAA structure, and payload-focused tests that avoid starting the MCP server or calling FogBugz. | packages/test-creation-lessons.skill |
| windows-network-admin-preflight | Validate and prepare a Windows admin workstation network path before infrastructure changes, including adapter selection, static IP/DNS setup, route/metric checks, and rollback-to-DHCP steps. | packages/windows-network-admin-preflight.skill |

## Notes
- Packages are generated from source skill directories and copied into packages/.
- Keep this list updated when adding or removing skills.
