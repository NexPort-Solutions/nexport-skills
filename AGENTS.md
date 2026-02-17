# AGENTS.md

## Purpose
This repository publishes NexPort skills as packaged bundles in `packages/*.skill`.

## Repository Layout
- `packages/`: distributable `.skill` archives.
- `SKILLS.md`: catalog shown to users.
- `skills.json`: machine-readable catalog for tooling.
- `scripts/`: package build/validation/catalog scripts.
- `templates/skill-template/`: starter template for new skills.

## Adding a New Skill
1. Create/package the new skill as `packages/<skill-name>.skill` (prefer `.\scripts\build-skill.ps1`).
2. Archive format requirement: the bundle must contain a top-level `<skill-name>/` folder with `SKILL.md` inside it.
3. Package completeness requirement: include all files needed by the skill, including any referenced `scripts/`, `references/`, `assets/`, `templates/`, and other companion files.
4. Update `SKILLS.md` with the new skill, purpose, and package path.
5. Regenerate `skills.json` and `SKILLS.md` via `.\scripts\sync-catalog.ps1`.

## Package Completeness Validation
- Do not publish a package that includes only `SKILL.md` when the skill references additional files.
- Validate each packaged skill by extracting it and confirming referenced paths exist inside the package.
- When `SKILL.md` references a relative file path, that same relative path must exist under the packaged `<skill-name>/` directory.

## Validation Checklist Before Commit
- `SKILLS.md` reflects current packages.
- package filenames and catalog entries align.
- each package contains `SKILL.md` plus all referenced companion files.
- run `.\scripts\validate-packages.ps1` successfully.
- run `.\scripts\check-package-size.ps1 -MaxSizeMB 5` successfully.
- run `.\scripts\sync-catalog.ps1` and commit resulting catalog updates.
- `git status --short` shows only intended changes.

## Publishing
1. Commit all related catalog/package updates together.
2. Push branch to `origin`.
