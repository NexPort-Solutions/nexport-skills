# AGENTS.md

## Purpose
This repository publishes NexPort skills in two forms:
- Packaged bundles in `packages/*.skill`.
- Claude marketplace plugin content in `plugins/nexport-skills/skills/*`.

Keep both forms in sync.

## Repository Layout
- `packages/`: distributable `.skill` archives.
- `plugins/nexport-skills/skills/`: unpacked skills for Claude plugin indexing.
- `.claude-plugin/marketplace.json`: canonical marketplace metadata.
- `marketplace.json`: root mirror of the same marketplace metadata.
- `plugins/nexport-skills/.claude-plugin/plugin.json`: plugin metadata.
- `SKILLS.md`: catalog shown to users.

## Adding a New Skill
1. Create/package the new skill as `packages/<skill-name>.skill`.
2. Archive format requirement: the bundle must contain a top-level `<skill-name>/` folder with `SKILL.md` inside it.
3. Update `SKILLS.md` with the new skill, purpose, and package path.
4. Re-sync unpacked plugin skills (extract all `.skill` bundles):

```powershell
tar -xf packages/<skill-name>.skill -C plugins/nexport-skills/skills
```

For a full refresh, clear and re-extract all skills:

```powershell
Remove-Item -Recurse -Force plugins/nexport-skills/skills/*
Get-ChildItem packages -Filter *.skill | ForEach-Object { tar -xf $_.FullName -C plugins/nexport-skills/skills }
```

5. Validate structure:
- each directory under `plugins/nexport-skills/skills/` should contain `SKILL.md`.
- no stray root file at `plugins/nexport-skills/skills/SKILL.md`.

## Maintaining Marketplace Metadata
- Update `.claude-plugin/marketplace.json` when plugin metadata changes.
- Keep `marketplace.json` byte-for-byte identical to `.claude-plugin/marketplace.json`.
- Keep `plugins/nexport-skills/.claude-plugin/plugin.json` version and description aligned with marketplace entries.

Hash check:

```powershell
(Get-FileHash .claude-plugin/marketplace.json -Algorithm SHA256).Hash
(Get-FileHash marketplace.json -Algorithm SHA256).Hash
```

## Validation Checklist Before Commit
- `SKILLS.md` reflects current packages.
- package count equals extracted skill count.
- marketplace canonical/mirror files match.
- `git status --short` shows only intended changes.

## Publishing
1. Commit all related catalog/package/plugin updates together.
2. Push branch to `origin`.
3. Optional local check if Claude CLI is installed:

```bash
claude plugin validate .
```
