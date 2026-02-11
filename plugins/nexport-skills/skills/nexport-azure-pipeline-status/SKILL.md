---
name: nexport-azure-pipeline-status
description: "Retrieve Azure DevOps pipeline status and troubleshoot failed runs using az devops CLI. Use when asked about pipeline status, failed builds, stage failures, or to inspect recent runs for the current repo’s project."
---

# NexPort Azure Pipeline Status & Failure Triage

## Workflow
- Infer org/project if not provided:
  - Parse `git remote -v` for an Azure DevOps URL (`https://dev.azure.com/{org}/{project}/_git/{repo}` or `{org}@dev.azure.com/{org}/{project}/_git/{repo}`).
  - If missing, scan `AGENTS.md` for org/project hints.
  - If still unknown, ask the user.
- Ask for pipeline ID or pipeline name if not specified.
- Resolve pipeline name → ID with `az pipelines list` when needed.
- Fetch the latest run and **summarize stage results first** (if stages exist), then ask which stage(s) to troubleshoot.
- For the selected stage(s), use timeline → logs to surface the failing task and error.
- If a timeline JSON was already downloaded, prefer the stage summary script to keep output concise.

## Commands (core)
- Configure defaults:
  - `az devops configure --defaults organization="<org-url>" project="<project>"`
- Find pipeline by name:
  - `az pipelines list --query "[?name=='<name>'].{id:id,name:name}" -o json`
- Latest run (by pipeline id):
  - `az pipelines runs list --pipeline-ids <id> --top 1 --query "[0].{id:id,status:status,result:result,finishTime:finishTime,sourceBranch:sourceBranch,requestedFor:requestedFor.displayName,commit:sourceVersion}" -o json`
- Timeline (stage/task statuses):
  - `az devops invoke --area build --resource timeline --route-parameters project=\"<project>\" buildId=<runId> --api-version 7.1 -o json`
- Task log (use logId from timeline):
  - `az devops invoke --area build --resource logs --route-parameters project=\"<project>\" buildId=<runId> logId=<logId> --api-version 7.1 --out-file <tmp-file>`

## Scripts
- `scripts/ado_stage_summary.py <timeline.json>`: summarize failed stages/jobs/tasks from a timeline JSON and include log IDs and issue hints.

## Triage Heuristics
- **Stages first**: group timeline records by `type=Stage` and report `name + result`. Ask which stage(s) to investigate before drilling down.
- **Failed tasks**: scan timeline records where `result=failed` and extract `log.id`.
- **Log parsing**: logs are JSON with `value: [lines...]`. Search for `##[error]`, error codes, and task-specific hints.
- **Deploy failures**: for `AzureRmWebAppDeployment@4`, common causes are file locks (`ERROR_INSUFFICIENT_ACCESS_TO_SITE_FOLDER`) and missing “Take app offline” setting.

## Notes
- If CLI commands fail or aren’t logged in, prompt to `az devops login`.
- If REST endpoints return HTML, the request is unauthenticated; use `az devops invoke` instead of `az rest`.
- Summarize failures by stage → job/task → error, then propose targeted fixes.
