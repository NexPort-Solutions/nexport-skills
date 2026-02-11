---
name: nexport-ci-pipeline-hygiene
description: "NexPort skill: nexport-ci-pipeline-hygiene."
---

# Skill: nexport-ci-pipeline-hygiene

## When to use
- Editing Azure Pipelines YAML or build/test scripts.

## Checklist
- Validate YAML after edits (e.g., yq '.' file.yml).
- Quote display names that include colons.
- Use $(Pipeline.Workspace) for temp/output; log disk usage early.
- Avoid shared obj output across projects; make paths per-project.
- Quote results directories with spaces; keep TRX naming consistent across shards.
- Quote dotnet/test MSBuild path arguments that may include spaces.

## References
- .azuredevops/ and pipeline docs
