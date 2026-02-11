---
name: php-lint-checks
description: PHP syntax linting helpers (php -l) and workflows for validating changed files or selected paths. Use when asked to verify PHP syntax, lint modified files, or add quick PHP lint scripts.
---

# PHP Lint Checks

Use this skill to standardize PHP syntax validation with `php -l`.

## Workflow

1) Decide scope
- **Changed files only** (preferred for quick checks)
- **Explicit file list** (user-provided)
- **Directory scan** (only when requested; can be slow)

2) Run lint
- Use `php -l` on each file; stop on first failure only if user requests.
- Scripts auto-select a PHP exe based on repo target (prefers 8.2 over 8.3 when noted in `composer.json` or `php-compatibility-matrix.md`).
- Keep output concise: file path + error line.
- Note: `php -l` validates syntax only; it does not catch inheritance/signature compatibility fatals.

3) Report
- Summarize which files were checked.
- If failures: show the first error and file.
- If lint passes but runtime still fails, call out likely compatibility/runtime categories and request runtime log check.

4) Compatibility gate (recommended for legacy apps)
- Add quick checks for known high-risk legacy dependencies after lint:
  - `vendor/nesbot/carbon`
  - old Symfony HttpFoundation classes
  - old Laravel exception/error handler signatures
- Pair lint with minimal runtime smoke check after deploy (`/health.php` and one app route).

## Bundled scripts

- `scripts/lint-changed.ps1` — lints PHP files changed in git working tree.
- `scripts/lint-paths.ps1` — lints specific files (supports globs).
- `scripts/resolve-php.ps1` — resolves php.exe (prefers repo target version).

### Examples

```powershell
# Lint changed PHP files in git
.\scripts\lint-changed.ps1

# Lint explicit files or patterns
.\scripts\lint-paths.ps1 -Paths "site\vendor\laravel\framework\src\Illuminate\Foundation\start.php","public\phoenix\system\functions.php"
```

## Practical warning

- For PHP 8.3 targets, signature mismatch failures (for example Carbon method signatures) can still return app-wide 500 with clean lint output. Treat lint as necessary but insufficient.
