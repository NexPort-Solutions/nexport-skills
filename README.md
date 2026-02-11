# nexport-skills

Repository for NexPort Codex skills, including packaged `.skill` bundles and a Claude Code marketplace layout.

## Contents
- `.claude-plugin/marketplace.json` defines the canonical marketplace metadata for repo-based discovery.
- `marketplace.json` mirrors the same metadata at repo root for file-path based marketplace add flows.
- `plugins/nexport-skills/.claude-plugin/plugin.json` defines the installable plugin.
- `plugins/nexport-skills/skills/` contains unpacked skill directories (`<skill>/SKILL.md`) for Claude marketplace indexing.
- `packages/` contains the distributable `.skill` bundles.
- `SKILLS.md` lists the available skills and their purposes.

## Example Prompts
Use these prompts with Codex to discover and install skills:

- "list installable skills"
- "list installable skills and descriptions at https://github.com/NexPort-Solutions/nexport-skills/tree/main/packages"
- "install the nexport-playwright-ui-test-patterns skill"
- "install the nexport-trx-parsing skill"
- "install skills from https://github.com/NexPort-Solutions/nexport-skills/tree/main/packages"

## Claude Code Marketplace
Validate from repo root:

```bash
claude plugin validate .
```

Add marketplace and install plugin:

```bash
/plugin marketplace add NexPort-Solutions/nexport-skills
/plugin install nexport-skills@nexport-skills-marketplace
```

## Updating Skills
1. Package skills from their source directories.
2. Copy the resulting `.skill` files into `packages/`.
3. Rebuild `plugins/nexport-skills/skills/` from `packages/*.skill` so marketplace content stays in sync.
4. Update `SKILLS.md` to keep the catalog current.

## Notes
- Keep this repo focused on NexPort skills and marketplace/plugin metadata.
- Prefer small, purpose-built skills that align with NexPort workflows.
