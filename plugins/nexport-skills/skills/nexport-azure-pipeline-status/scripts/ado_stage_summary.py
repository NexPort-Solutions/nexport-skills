#!/usr/bin/env python3
"""Summarize Azure DevOps build timeline JSON into stage/job/task failures."""

from __future__ import annotations

import json
import sys
from typing import Any, Iterable


def _load(path: str) -> dict[str, Any]:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def _records(data: dict[str, Any]) -> Iterable[dict[str, Any]]:
    return data.get("records", [])


def _format_record(r: dict[str, Any]) -> str:
    name = r.get("name", "?")
    rtype = r.get("type", "?")
    result = r.get("result", "?")
    log = r.get("log") or {}
    log_id = log.get("id")
    issue_msgs = []
    for issue in r.get("issues") or []:
        msg = issue.get("message")
        if msg:
            issue_msgs.append(msg)
    issue_text = "; ".join(issue_msgs)
    return f"{rtype}\t{name}\t{result}\tlog:{log_id}\t{issue_text}".rstrip()


def main() -> int:
    if len(sys.argv) != 2:
        print("Usage: ado_stage_summary.py <timeline.json>")
        return 2

    data = _load(sys.argv[1])
    records = list(_records(data))

    failed = [r for r in records if r.get("result") == "failed"]
    if not failed:
        print("No failed records found.")
        return 0

    # Stages first
    stages = [r for r in failed if r.get("type") == "Stage"]
    if stages:
        print("Failed stages:")
        for r in stages:
            print(_format_record(r))
        print()

    # Jobs then tasks
    jobs = [r for r in failed if r.get("type") == "Job"]
    tasks = [r for r in failed if r.get("type") == "Task"]

    if jobs:
        print("Failed jobs:")
        for r in jobs:
            print(_format_record(r))
        print()

    if tasks:
        print("Failed tasks:")
        for r in tasks:
            print(_format_record(r))
        print()

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
