# nexport-skills

Repository for NexPort Codex skills as packaged `.skill` bundles.

## Contents
- `packages/` contains the distributable `.skill` bundles.
- `SKILLS.md` lists the available skills and their purposes.
- `skills.json` provides a machine-readable catalog for tooling.
- `scripts/` contains packaging and validation automation.
- `templates/skill-template/` provides a starter structure for new skills.
- `.github/workflows/validate-packages.yml` validates packages and catalog consistency in CI.

## Example Prompts
Use these prompts with Codex to discover and install skills:

- "list installable skills"
- "list installable skills and descriptions at https://github.com/NexPort-Solutions/nexport-skills/tree/main/packages"
- "install the nexport-playwright-ui-test-patterns skill"
- "install the nexport-trx-parsing skill"
- "install skills from https://github.com/NexPort-Solutions/nexport-skills/tree/main/packages"

## Updating Skills
1. Build one skill package:

```powershell
.\scripts\build-skill.ps1 -Name <skill-name>
```

2. Build all skill packages:

```powershell
.\scripts\build-all-skills.ps1
```

3. Validate package structure and referenced files:

```powershell
.\scripts\validate-packages.ps1
```

4. Check package size budget:

```powershell
.\scripts\check-package-size.ps1 -MaxSizeMB 5
```

5. Rebuild catalog files from packages:

```powershell
.\scripts\sync-catalog.ps1
```

## Notes
- Keep this repo focused on NexPort skills and package metadata.
- Prefer small, purpose-built skills that align with NexPort workflows.
