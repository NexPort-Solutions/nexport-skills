# NexPort Skills Catalog

This repo stores packaged Codex skills for NexPort workflows. Packages live under `packages/`.

## Available Skills

| Skill | Purpose | Package |
| --- | --- | --- |
| es-file-lookup | Use Everything CLI (es.exe) for file name/path lookups | packages/es-file-lookup.skill |
| nexport-ajaxq-request-guarding | Prevent duplicate AJAX requests using ajaxq + beforeSend guards | packages/nexport-ajaxq-request-guarding.skill |
| nexport-azure-pipeline-status | Azure DevOps pipeline status and run inspection | packages/nexport-azure-pipeline-status.skill |
| nexport-ci-pipeline-hygiene | CI pipeline update and validation hygiene | packages/nexport-ci-pipeline-hygiene.skill |
| nexport-cold-start | Cold start workflow (Quick Memory + epic discovery + docs anchoring) | packages/nexport-cold-start.skill |
| nexport-controller-test-patterns | Controller test patterns and checklist | packages/nexport-controller-test-patterns.skill |
| nexport-epic-shaping-decomposition | Epic shaping + roadmap decomposition workflow | packages/nexport-epic-shaping-decomposition.skill |
| nexport-fogbugz-ops | FogBugz case operations workflow | packages/nexport-fogbugz-ops.skill |
| fast-file-io-selection | Choose fast PowerShell/.NET file IO patterns by workload | packages/fast-file-io-selection.skill |
| nexport-kendo-grid-edit-patterns | Kendo grid edit patterns | packages/nexport-kendo-grid-edit-patterns.skill |
| nexport-kendo-upgrade-runbook | Kendo/Telerik upgrade runbook with validation steps | packages/nexport-kendo-upgrade-runbook.skill |
| nexport-localization-resources | Localization resource usage patterns | packages/nexport-localization-resources.skill |
| nexport-logging-telemetry-audit | Logging, telemetry, and auditing guidance for NexPort | packages/nexport-logging-telemetry-audit.skill |
| nexport-memory-hygiene | Quick Memory hygiene and update guidance | packages/nexport-memory-hygiene.skill |
| nexport-nhibernate-aaaa-session-pattern | NHibernate AAAA session-boundary pattern for deterministic controller/service tests | packages/nexport-nhibernate-aaaa-session-pattern.skill |
| nexport-nhibernate-session-guard | NHibernate session/transaction guard patterns | packages/nexport-nhibernate-session-guard.skill |
| nexport-permission-entitlement-gate | Tenant feature entitlement gating patterns | packages/nexport-permission-entitlement-gate.skill |
| nexport-playwright-ui-test-patterns | Playwright UI test patterns and personas | packages/nexport-playwright-ui-test-patterns.skill |
| nexport-proctoring-host-patterns | External proctoring host patterns | packages/nexport-proctoring-host-patterns.skill |
| nexport-smoke-test-runner | Smoke test runner workflow (UI/unit prompt + Roslyn-first execution) | packages/nexport-smoke-test-runner.skill |
| nexport-question-analytics-flow | Question analytics workflow guidance | packages/nexport-question-analytics-flow.skill |
| nexport-release-announcement | Release announcement authoring workflow | packages/nexport-release-announcement.skill |
| nexport-scheduler-job-lifecycle | Scheduler job lifecycle patterns | packages/nexport-scheduler-job-lifecycle.skill |
| nexport-solr-aks-replication | Replicate NexPort Solr deployment on AKS using automation-first az/kubectl workflows | packages/nexport-solr-aks-replication.skill |
| nexport-test-logging-diagnostics | Test logging diagnostics and guidance | packages/nexport-test-logging-diagnostics.skill |
| nexport-trx-parsing | TRX parsing, failure extraction, and parser benchmarking | packages/nexport-trx-parsing.skill |
| nexport-ui-tests-runner | Playwright UI test runner workflow (start/stop, logs, test runs) | packages/nexport-ui-tests-runner.skill |
| nexport-ui-fixtures-my-courses | UiTests fixture guidance for My Courses/My Training | packages/nexport-ui-fixtures-my-courses.skill |
| nexport-tree-permission-queries | Tree-based permission query patterns | packages/nexport-tree-permission-queries.skill |
| nexport-ui-tests-startup-troubleshooting | UI tests startup troubleshooting | packages/nexport-ui-tests-startup-troubleshooting.skill |
| nexport-ui-ux-checklist-enforcer | Enforce UI/UX checklist compliance with concrete file-level fixes | packages/nexport-ui-ux-checklist-enforcer.skill |
| nexport-ui-visual-walkthrough | Manual visual walkthrough using Roslyn start/build + Playwright checks | packages/nexport-ui-visual-walkthrough.skill |
| nexport-user-docs | End-user docs update workflow | packages/nexport-user-docs.skill |
| nexport-vocabulary-glossary-enforcement | Detect terminology drift and align wording to glossary | packages/nexport-vocabulary-glossary-enforcement.skill |
| php-lint-checks | PHP syntax linting workflow (`php -l`) for changed files or selected paths | packages/php-lint-checks.skill |
| qa-ready-to-testing | Move QA-ready FogBugz cases to Resolved (To Testing) with case notes | packages/qa-ready-to-testing.skill |
| research-orchestration | Research orchestration across local context, docs MCP, and web sources | packages/research-orchestration.skill |
| test-creation-lessons | Repo-specific test creation lessons and AAAA structure guidance | packages/test-creation-lessons.skill |

## Notes
- Packages are generated from their source skill directories and copied into `packages/`.
- Keep this list updated when adding or removing skills.
