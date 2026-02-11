---
name: nexport-kendo-upgrade-runbook
description: Runbook for upgrading Kendo UI/Telerik ASP.NET Core components in NexPort Campus (server-side NuGet + client-side JS/themes via zip assets), including version alignment, zip-first client assets, and required UiSmoke validation before commit.
---

# Nexport Kendo Upgrade Runbook

## Overview
Use this workflow when updating Kendo UI/Telerik ASP.NET Core components in this repo. It enforces server/client alignment, uses zip assets for all JS/CSS, and requires UiSmoke validation before any commit.

## Workflow

### 1) Preflight
- Identify the target Kendo version and confirm server/client components will match.
- Locate the Telerik ASP.NET Core client zip (usually in `.scratch`).
- Verify the zip contains `js` and `styles` directories (themes live in `styles`).
- Use the JS libraries (not ES modules).
- Do not rely on the Kendo/Telerik MCP for upgrade guidance.

### 2) Review changes with the user
- Summarize the exact files and versions you plan to update.
- Offer an aggregate impact matrix (components/pages + likely risk areas) before applying changes.
- Confirm the zip-first approach for this upgrade.
- Wait for explicit approval before modifying files.

### 3) Update server-side NuGet
- Upgrade the Telerik ASP.NET Core NuGet packages to the target version together.
- Keep server-side package versions aligned to avoid runtime mismatches.
- Use the Telerik NuGet installation/upgrade guide for exact steps.

### 4) Update client-side JS
- Use the files from the downloaded zip:
  - Replace `wwwroot/lib/kendo-ui/<version>/js` with the JS directory from the zip.
  - Update `bundles.config` and any script tags that still point to the old version.

### 5) Update client-side themes
- Use the theme files from the downloaded zip (from the `styles` directory).
- Update bundling to point at the new theme CSS files.

### 6) Validate before commit
- All UiSmoke tests must pass before committing any changes.
- Start the site and run the UiSmoke category tests (see the UiTests runner skill for the preferred workflow).
- Do not commit if any UiSmoke tests fail.

## Notes
- Server-side and client-side updates must happen together.
- Use JS libraries, not ES modules.
- The zip file contains all required files for client JS and themes.
- Do not rely on the Kendo/Telerik MCP to drive upgrade decisions.

## Reference docs
Store these links as references (use in a browser when needed):
```
NuGet install/upgrade: https://www.telerik.com/aspnet-core-ui/documentation/installation/installation-options/nuget-install
Client resources/libman: https://www.telerik.com/aspnet-core-ui/documentation/installation/adding-client-side-resources/using-libman
```

## Related local docs
- `E:/Sandbox/nexport-dev-docs/nexport-dev-guide/nexport-devops/dev-ops-home/server-dependencies-by-product/telerik-kendo-ui.md`
- `E:/Sandbox/nexport-dev-docs/nexport-dev-guide/nexport-devops/codex-telerik-mcp-setup.md`
