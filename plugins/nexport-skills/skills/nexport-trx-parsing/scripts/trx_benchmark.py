#!/usr/bin/env python
"""Benchmark TRX parsing speed and correctness.

Compares rg (names), ElementTree iterparse, xunitparserx (if available), and pygixml (if available).
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import time
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import xml.etree.ElementTree as ET

try:
    import pygixml  # type: ignore
except Exception:
    pygixml = None

try:
    import xunitparserx as xpx  # type: ignore
except Exception:
    xpx = None


RG_NAME_PAT = r"UnitTestResult(?=[^>]*outcome=\"Failed\")[^>]*testName=\"[^\"]+\""
NAME_EXTRACT = re.compile(r'testName="([^"]+)"')


def _iter_trx_files(dir_path: Path, top: int) -> List[Path]:
    files = sorted(dir_path.glob("*.trx"), key=lambda p: p.stat().st_size, reverse=True)
    if top > 0:
        return files[:top]
    return files


def _iterparse_failures(path: Path) -> Tuple[List[str], Dict[str, Optional[str]]]:
    names: List[str] = []
    detail: Dict[str, Optional[str]] = {}
    for _, elem in ET.iterparse(path, events=("end",)):
        if elem.tag.endswith("UnitTestResult") and elem.attrib.get("outcome") == "Failed":
            name = elem.attrib.get("testName", "")
            names.append(name)
            detail_text: Optional[str] = None
            stdout = elem.find(".//{*}StdOut")
            if stdout is not None and stdout.text and stdout.text.strip():
                detail_text = stdout.text.strip()
            if detail_text is None:
                msg = elem.find(".//{*}Message")
                if msg is not None and msg.text and msg.text.strip():
                    detail_text = msg.text.strip()
            detail[name] = detail_text
            elem.clear()
    return names, detail


def _rg_names(path: Path) -> List[str]:
    rg = subprocess.run(["rg", "-oP", RG_NAME_PAT, str(path)], capture_output=True, text=True)
    return [NAME_EXTRACT.search(line).group(1) for line in rg.stdout.splitlines() if NAME_EXTRACT.search(line)]


def _xunitparserx_names(path: Path) -> Tuple[List[str], Dict[str, Optional[str]], Optional[str]]:
    if xpx is None:
        return [], {}, "xunitparserx not installed"
    try:
        _, result = xpx.parse_trx(str(path))
    except FileNotFoundError as exc:
        return [], {}, f"xunitparserx missing dependency: {exc}"
    names: List[str] = []
    detail: Dict[str, Optional[str]] = {}
    for test_case, trace in result.failures:
        name = getattr(test_case, "methodname", None) or getattr(test_case, "name", None) or str(test_case)
        names.append(name)
        detail[name] = trace.strip() if isinstance(trace, str) else None
    return names, detail, None


def _pygixml_names(path: Path) -> Tuple[List[str], Dict[str, Optional[str]], Optional[str]]:
    if pygixml is None:
        return [], {}, "pygixml not installed"
    doc = pygixml.parse_file(str(path))
    root = doc.first_child()
    failed_nodes = root.select_nodes("//*[local-name()='UnitTestResult'][@outcome='Failed']")
    names: List[str] = []
    detail: Dict[str, Optional[str]] = {}
    for wrap in failed_nodes:
        node = wrap.node
        name_attr = node.attribute("testName")
        name = name_attr.value if name_attr else ""
        names.append(name)
        detail_text: Optional[str] = None
        stdout_nodes = node.select_nodes(".//*[local-name()='StdOut']")
        if stdout_nodes:
            text = stdout_nodes[0].node.text()
            if text and text.strip():
                detail_text = text.strip()
        if detail_text is None:
            msg_nodes = node.select_nodes(".//*[local-name()='Message']")
            if msg_nodes:
                text = msg_nodes[0].node.text()
                if text and text.strip():
                    detail_text = text.strip()
        detail[name] = detail_text
    return names, detail, None


def _detail_presence(detail_map: Dict[str, Optional[str]]) -> int:
    return len([k for k, v in detail_map.items() if v])


def main() -> int:
    parser = argparse.ArgumentParser(description="Benchmark TRX parsers.")
    parser.add_argument("--dir", required=True, help="Directory containing TRX files")
    parser.add_argument("--top", type=int, default=3, help="Number of largest TRX files to benchmark")
    parser.add_argument("--format", choices=("md", "json"), default="md", help="Output format")
    args = parser.parse_args()

    dir_path = Path(args.dir)
    files = _iter_trx_files(dir_path, args.top)
    if not files:
        print("No TRX files found.")
        return 1

    rows = []
    for path in files:
        # iterparse baseline
        t0 = time.perf_counter()
        iter_names, iter_detail = _iterparse_failures(path)
        iter_time = time.perf_counter() - t0

        # rg
        t0 = time.perf_counter()
        rg_names = _rg_names(path)
        rg_time = time.perf_counter() - t0

        # xunitparserx
        t0 = time.perf_counter()
        xpx_names, xpx_detail, xpx_note = _xunitparserx_names(path)
        xpx_time = time.perf_counter() - t0

        # pygixml
        t0 = time.perf_counter()
        pg_names, pg_detail, pg_note = _pygixml_names(path)
        pg_time = time.perf_counter() - t0

        iter_set = set(iter_names)
        rows.append({
            "file": str(path),
            "size_mb": round(path.stat().st_size / 1024 / 1024, 1),
            "iterparse_time_s": round(iter_time, 2),
            "rg_time_s": round(rg_time, 2),
            "xunitparserx_time_s": round(xpx_time, 2) if xpx_note is None else None,
            "pygixml_time_s": round(pg_time, 2) if pg_note is None else None,
            "rg_missing": len(iter_set - set(rg_names)),
            "rg_extra": len(set(rg_names) - iter_set),
            "xunitparserx_missing": len(iter_set - set(xpx_names)),
            "xunitparserx_extra": len(set(xpx_names) - iter_set),
            "pygixml_missing": len(iter_set - set(pg_names)),
            "pygixml_extra": len(set(pg_names) - iter_set),
            "iterparse_detail": _detail_presence(iter_detail),
            "xunitparserx_detail": _detail_presence(xpx_detail),
            "pygixml_detail": _detail_presence(pg_detail),
            "xunitparserx_note": xpx_note,
            "pygixml_note": pg_note,
        })

    if args.format == "json":
        print(json.dumps({"files": rows}, indent=2))
        return 0

    print("# TRX Parser Benchmark")
    print(f"Source: {dir_path}")
    print("")
    print("| file | size MB | rg s | iterparse s | xunitparserx s | pygixml s | rg miss/extra | xunit miss/extra | pygixml miss/extra | detail (iter/xunit/pygi) |")
    print("| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |")
    for r in rows:
        print("| {file} | {size_mb} | {rg} | {iter} | {xunit} | {pygi} | {rg_me} | {xunit_me} | {pygi_me} | {detail} |".format(
            file=Path(r["file"]).name,
            size_mb=r["size_mb"],
            rg=r["rg_time_s"],
            iter=r["iterparse_time_s"],
            xunit=r["xunitparserx_time_s"] if r["xunitparserx_time_s"] is not None else "n/a",
            pygi=r["pygixml_time_s"] if r["pygixml_time_s"] is not None else "n/a",
            rg_me=f"{r['rg_missing']}/{r['rg_extra']}",
            xunit_me=f"{r['xunitparserx_missing']}/{r['xunitparserx_extra']}",
            pygi_me=f"{r['pygixml_missing']}/{r['pygixml_extra']}",
            detail=f"{r['iterparse_detail']}/{r['xunitparserx_detail']}/{r['pygixml_detail']}",
        ))

    notes = [r for r in rows if r.get("xunitparserx_note") or r.get("pygixml_note")]
    if notes:
        print("")
        print("Notes:")
        for r in notes:
            if r.get("xunitparserx_note"):
                print(f"- {Path(r['file']).name}: xunitparserx: {r['xunitparserx_note']}")
            if r.get("pygixml_note"):
                print(f"- {Path(r['file']).name}: pygixml: {r['pygixml_note']}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
