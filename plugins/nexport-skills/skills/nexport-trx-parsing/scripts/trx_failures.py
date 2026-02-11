#!/usr/bin/env python
"""Summarize failed tests from TRX files.

Defaults to markdown output for Codex-friendly review. Use --format json for structured output.
"""
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
from typing import Dict, Iterable, List, Optional

try:
    import pygixml  # type: ignore
except Exception:  # pragma: no cover - optional
    pygixml = None

import xml.etree.ElementTree as ET


def _iter_trx_files(paths: List[str]) -> List[Path]:
    files: List[Path] = []
    for raw in paths:
        path = Path(raw)
        if path.is_dir():
            files.extend(sorted(path.glob("*.trx")))
        elif path.is_file() and path.suffix.lower() == ".trx":
            files.append(path)
    return files


def _first_detail_line(detail: Optional[str]) -> Optional[str]:
    if not detail:
        return None
    for line in detail.splitlines():
        if line.strip():
            return line.strip()
    return None


def _parse_pygixml(path: Path) -> List[Dict[str, Optional[str]]]:
    doc = pygixml.parse_file(str(path))
    root = doc.first_child()
    failed_nodes = root.select_nodes("//*[local-name()='UnitTestResult'][@outcome='Failed']")

    results: List[Dict[str, Optional[str]]] = []
    for wrap in failed_nodes:
        node = wrap.node
        name_attr = node.attribute("testName")
        duration_attr = node.attribute("duration")
        name = name_attr.value if name_attr else ""
        duration = duration_attr.value if duration_attr else None

        detail: Optional[str] = None
        stdout_nodes = node.select_nodes(".//*[local-name()='StdOut']")
        if stdout_nodes:
            text = stdout_nodes[0].node.text()
            if text and text.strip():
                detail = text.strip()
        if detail is None:
            msg_nodes = node.select_nodes(".//*[local-name()='Message']")
            if msg_nodes:
                text = msg_nodes[0].node.text()
                if text and text.strip():
                    detail = text.strip()

        results.append({
            "file": str(path),
            "testName": name,
            "duration": duration,
            "detail": detail,
            "detailLine": _first_detail_line(detail),
        })
    return results


def _parse_iterparse(path: Path) -> List[Dict[str, Optional[str]]]:
    results: List[Dict[str, Optional[str]]] = []
    for _, elem in ET.iterparse(path, events=("end",)):
        if elem.tag.endswith("UnitTestResult") and elem.attrib.get("outcome") == "Failed":
            name = elem.attrib.get("testName", "")
            duration = elem.attrib.get("duration")
            detail: Optional[str] = None
            stdout = elem.find(".//{*}StdOut")
            if stdout is not None and stdout.text and stdout.text.strip():
                detail = stdout.text.strip()
            if detail is None:
                msg = elem.find(".//{*}Message")
                if msg is not None and msg.text and msg.text.strip():
                    detail = msg.text.strip()
            results.append({
                "file": str(path),
                "testName": name,
                "duration": duration,
                "detail": detail,
                "detailLine": _first_detail_line(detail),
            })
            elem.clear()
    return results


def _summarize_markdown(failures: List[Dict[str, Optional[str]]], file_count: int, source: str) -> str:
    lines: List[str] = []
    lines.append("# TRX Failure Summary")
    lines.append(f"Source: {source}")
    lines.append(f"Files scanned: {file_count}")
    lines.append(f"Failures: {len(failures)}")
    lines.append("")

    if not failures:
        lines.append("No failures found.")
        return "\n".join(lines)

    lines.append("| test | duration | file | first detail line |")
    lines.append("| --- | --- | --- | --- |")
    for f in failures:
        lines.append("| {test} | {duration} | {file} | {detail} |".format(
            test=(f.get("testName") or ""),
            duration=(f.get("duration") or ""),
            file=os.path.basename(f.get("file") or ""),
            detail=(f.get("detailLine") or ""),
        ))
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="Summarize TRX failures.")
    parser.add_argument("paths", nargs="*", help="TRX files and/or directories containing TRX files")
    parser.add_argument("--dir", dest="dir", help="Directory containing TRX files")
    parser.add_argument("--top", type=int, default=0, help="Only analyze the N largest TRX files")
    parser.add_argument("--format", choices=("md", "json"), default="md", help="Output format")
    args = parser.parse_args()

    inputs: List[str] = []
    if args.dir:
        inputs.append(args.dir)
    inputs.extend(args.paths)

    if not inputs:
        print("No TRX paths provided. Use --dir or pass files/dirs.")
        return 2

    files = _iter_trx_files(inputs)
    if not files:
        print("No TRX files found.")
        return 1

    if args.top and args.top > 0:
        files = sorted(files, key=lambda p: p.stat().st_size, reverse=True)[: args.top]

    failures: List[Dict[str, Optional[str]]] = []
    for path in files:
        if pygixml is not None:
            failures.extend(_parse_pygixml(path))
        else:
            failures.extend(_parse_iterparse(path))

    if args.format == "json":
        payload = {
            "source": inputs,
            "files": [str(p) for p in files],
            "failures": failures,
        }
        print(json.dumps(payload, indent=2))
    else:
        source = ", ".join(inputs)
        print(_summarize_markdown(failures, len(files), source))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
