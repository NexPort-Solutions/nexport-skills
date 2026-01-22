# nexport-skills

Repository for packaged Codex skills used by NexPort teams.

## Contents
- `packages/` contains the distributable `.skill` files.
- `SKILLS.md` lists the available skills and their purposes.

## Example Prompts
Use these prompts with Codex to discover and install skills:

- "list installable skills"
- "list installable skills and descriptions at https://github.com/NexPort-Solutions/nexport-skills/tree/main/packages"
- "install the nexport-playwright-ui-test-patterns skill"
- "install skills from https://github.com/NexPort-Solutions/nexport-skills/tree/main/packages"

## Updating Skills
1. Package skills from their source directories.
2. Copy the resulting `.skill` files into `packages/`.
3. Update `SKILLS.md` to keep the catalog current.

## Notes
- Keep this repo focused on packaged skills only.
- Prefer small, purpose-built skills that align with NexPort workflows.
