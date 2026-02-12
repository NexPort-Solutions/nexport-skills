---
name: nexport-solr-aks-replication
description: "Replicate NexPort Solr deployment on AKS using automation-first az/kubectl workflows. AKS-only; no Tomcat path."
---

# Skill: nexport-solr-aks-replication

## When to use
- User asks to install, deploy, replicate, or troubleshoot Solr in NexPort-style environments on AKS.
- User wants to automate Solr provisioning as much as possible through Azure CLI tooling.
- User needs a repeatable runbook for Solr provisioning plus post-deploy indexing verification.

## Scope guardrails
- AKS-only workflow. Do not propose Tomcat-based deployment steps.
- Prefer execution via `az` and `kubectl` by default.
- Use `Nexport.SolrDeployer` and `Nexport.Solr.Core` as the installer/orchestrator path.
- Never print or persist clear-text secrets in logs or docs.

## Source anchors (read before acting)
- `Nexport.SolrDeployer/Program.cs`
- `Nexport.Solr.Core/AzureSolrInfo.cs`
- `Nexport.Solr.Core/AzureSolrCoreInfo.cs`
- `Nexport.Solr.Core/DeploymentHelper.cs`
- `NexPort.Models/Solr/SolrHelper.cs`
- `NexPort.Models/Solr/Entities/SolrSettings.cs`
- `E:/Sandbox/nexport-dev-docs/nexport-dev-guide/readme/how-to-install-solr.md`
- `E:/Sandbox/nexport-dev-docs/nexport-dev-guide/developer-handbook-home/nexport-solr-index-architecture.md`

## Required inputs
- `subscription_id`
- `resource_group`
- `aks_cluster_name`
- `solr_instance_name`
- `storage_account_name`
- `file_share_name`
- `solr_username`
- `solr_password`

Optional:
- `namespace` (default: `default`)
- `use_ssl` (default: `false`)
- `azure_keyvault_uri`
- `ssl_certificate_name`
- `reset_strategy` (`none`, `regenerate-schema`, `delete-and-reindex`, `full-reset`)

## Workflow

1) Detect and validate repo capabilities
- Confirm `Nexport.SolrDeployer` and `Nexport.Solr.Core` projects exist.
- Confirm runtime settings model exists (`SolrSettings`) and indexing jobs exist.
- Confirm core generation support via `SolrHelper.GenerateCoreData`.

2) Azure and AKS preflight (execute by default)
- Set subscription:
  - `az account set --subscription <subscription_id>`
- Validate RG and AKS:
  - `az group show -n <resource_group>`
  - `az aks show -g <resource_group> -n <aks_cluster_name>`
- Pull kube context:
  - `az aks get-credentials -g <resource_group> -n <aks_cluster_name> --overwrite-existing`
- Validate cluster access:
  - `kubectl cluster-info`
  - `kubectl get ns`
  - `kubectl get ns <namespace>`
- Validate storage account:
  - `az storage account show -g <resource_group> -n <storage_account_name>`

3) Build installer payloads
- Create `solr-info.json` using `AzureSolrInfo` fields:
  - `AzureSubscriptionId`, `AzureResourceGroupName`, `AksClusterName`, `AzureStorageAccountName`, `AzureFileShareName`, `SolrInstanceName`, `SolrUsername`, `SolrPassword`, `UseSsl`, `AzureKeyVaultUri`, `SslCertificateName`.
- Create `solr-cores.json` using `AzureSolrCoreInfo[]` entries:
  - `CoreName`, `CoreConfigFilePath`, `ResetData`.
- Prefer generating core configs from project metadata (`SolrHelper` patterns) rather than hand-authoring schema files.
- Starter templates are provided at:
  - `.codex/skills/nexport-solr-aks-replication/references/solr-info.json.template`
  - `.codex/skills/nexport-solr-aks-replication/references/solr-cores.json.template`

4) Deploy Solr through installer
- Execute:
  - `dotnet run --project <repo>/Nexport.SolrDeployer --type DeploySolr --config-file-path <solr-info.json> --core-file-path <solr-cores.json> --result-file-path <solr-deploy-result.json>`
- If deployment fails, capture and report:
  - Installer diagnostics from result JSON
  - Pod, PVC, PV, and service details:
    - `kubectl get pods -n <namespace> -o wide`
    - `kubectl get pvc -n <namespace>`
    - `kubectl describe pvc <name> -n <namespace>`
    - `kubectl get pv`
    - `kubectl get svc -n <namespace>`

5) Verify runtime and indexing
- Verify Solr reachability:
  - `http(s)://<solr-address>:8983/solr/#/`
- Verify runtime settings are persisted (`SolrSettings` semantics):
  - `SolrAddress`, `UrlScheme`, `SolrPort`, `SolrStatus`.
- Validate index pipeline behavior:
  - `SolrInitialIndexingJob` bootstrap behavior
  - `SolrIndexProcessingJob` queue drain behavior
  - Search smoke checks for user/invite flows

6) Reset and recovery paths
- `regenerate-schema`:
  - Update Solr credentials/settings first, then queue regenerate schema through app path.
- `delete-and-reindex`:
  - Queue delete/reindex via app path and validate queue completion.
- `full-reset`:
  - Destructive. Require explicit confirmation before running.
- Credential recovery:
  - Update credentials in settings, then run regenerate schema or reindex workflow.

## Environment behavior and identity rules
- For development installs, default away from managed identity if local identity artifacts fail.
- Use `NEXPORT_SOLR_USE_MANAGED_IDENTITY=true` only when explicitly requested and supported.
- Always record resolved credential strategy in the run summary.

## Required output in responses
- Preflight summary (pass/fail by step)
- Exact commands run
- Deployment result summary (success, Solr address, namespace, core list)
- Verification summary (endpoint, runtime settings, indexing checks)
- If failed: concise root cause + immediate next command to run

## Safety checks
- Never commit generated JSON files containing credentials.
- Redact passwords in all echoed command output.
- In non-dev environments, require explicit user confirmation before destructive reset operations.

## Done criteria
- Solr pod and service healthy in target namespace.
- Solr endpoint responds.
- Runtime settings updated and consistent.
- Initial indexing/reindex path validated.
- Run summary includes troubleshooting breadcrumbs for handoff.
