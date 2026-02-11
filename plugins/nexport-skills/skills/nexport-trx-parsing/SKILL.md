---
name: nexport-trx-parsing
description: "Parse and summarize TRX test results, extract failures fast, and benchmark TRX parsers (pygixml/ElementTree/xunitparserx/rg). Use when asked to analyze large TRX outputs or compare parsing speed/correctness."
---

# NexPort TRX Parsing

## When to use
- Large TRX files need fast failure extraction.
- Comparing parser speed/correctness for TRX analysis.
- Summarizing failed tests for quick diagnosis.

## Quick start
- Failure summary (preferred):
  - `python .codex/skills/nexport-trx-parsing/scripts/trx_failures.py --dir <trx-dir> --top 3`
- Benchmark parsers:
  - `python .codex/skills/nexport-trx-parsing/scripts/trx_benchmark.py --dir <trx-dir> --top 3`

## Rules
- Prefer using the TRX path(s) produced by the current test run (e.g., Roslyn MCP `trxPath`).
- It is OK to parse a single known TRX file when the tool returned its path.
- If multiple runs exist, prefer the TRX directory containing the latest run.
- Prefer `pygixml` for speed; fall back to `ElementTree.iterparse` if unavailable.
- Failure detail may live under `<StdOut>` (common) or `<Message>`; check both.
- Default output is agent-friendly markdown; use `--format json` when structured output is required.
- Timeout hints: search for `Execution Timeout Expired` and `UpdatingLeftright` to spot group tree updates; recommend splitting Arrange into separate sessions/transactions.

## Scripts
- `scripts/trx_failures.py` – fast failure extraction with optional JSON output.
- `scripts/trx_benchmark.py` – compares `rg`, `ElementTree`, `xunitparserx`, `pygixml`.
