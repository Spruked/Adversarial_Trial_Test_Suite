#!/usr/bin/env python3
"""
Prepare a timestamped adversarial trial run workspace.

Creates:
- runs/<run_id>/manifest.json
- runs/<run_id>/execution_log.csv
- runs/<run_id>/judges/<judge>/phase_<n>/<test_name>.md templates
"""

from __future__ import annotations

import argparse
import csv
import json
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List


def parse_test_number(filename: str) -> int:
    m = re.search(r"test(\d+)_", filename)
    return int(m.group(1)) if m else 9999


def phase_from_index(index: int) -> int:
    return index + 1


def collect_suite(base: Path, judges: List[str]) -> Dict[str, List[Path]]:
    suite: Dict[str, List[Path]] = {}
    for judge in judges:
        tests_dir = base / judge / "tests"
        files = sorted(
            [p for p in tests_dir.glob("*.md") if p.is_file()],
            key=lambda p: parse_test_number(p.name),
        )
        suite[judge] = files
    return suite


def write_template(path: Path, run_id: str, judge: str, phase: int, src_test: Path):
    path.parent.mkdir(parents=True, exist_ok=True)
    now = datetime.now(timezone.utc).isoformat()
    path.write_text(
        "\n".join(
            [
                f"# Trial Result Template - {src_test.name}",
                "",
                f"- run_id: {run_id}",
                f"- judge: {judge}",
                f"- phase: {phase}",
                f"- source_test: {src_test.as_posix()}",
                f"- created_utc: {now}",
                "- execution_start_utc: ",
                "- execution_end_utc: ",
                "- status: PENDING",
                "",
                "## Prompt",
                "",
                "[paste prompt used for this run]",
                "",
                "## Judge Response",
                "",
                "[paste raw judge response]",
                "",
                "## Verdict",
                "",
                "- pass_fail: ",
                "- notes: ",
                "",
            ]
        ),
        encoding="utf-8",
    )


def main() -> int:
    parser = argparse.ArgumentParser(description="Prepare adversarial trial run folders and logs")
    parser.add_argument("--suite-path", default="Adversarial_Trial_Test_Suite")
    parser.add_argument("--run-id", default="")
    parser.add_argument("--api-base", default="http://127.0.0.1:8003")
    parser.add_argument("--skip-preflight", action="store_true")
    args = parser.parse_args()

    suite_root = Path(args.suite_path).resolve()
    if not args.skip_preflight:
        preflight_script = suite_root / "preflight_trial_gate.py"
        cmd = [sys.executable, str(preflight_script), "--api-base", args.api_base]
        proc = subprocess.run(cmd, capture_output=True, text=True)
        if proc.returncode != 0:
            print("PRECHECK_FAILED")
            if proc.stdout:
                print(proc.stdout.strip())
            if proc.stderr:
                print(proc.stderr.strip())
            print("Aborting run creation. Fix endpoint validity first or pass --skip-preflight.")
            return 2

    judges = ["gemini", "kimi", "grok4", "deepseek", "chatgpt5_1"]
    run_id = args.run_id or datetime.now().strftime("%Y-%m-%d_%H%M%S")
    run_root = suite_root / "runs" / run_id
    judges_root = run_root / "judges"
    judges_root.mkdir(parents=True, exist_ok=True)

    suite = collect_suite(suite_root, judges)
    rows = []

    for judge in judges:
        tests = suite[judge]
        for idx, test_file in enumerate(tests):
            phase = phase_from_index(idx)
            result_file = judges_root / judge / f"phase_{phase}" / test_file.name
            write_template(result_file, run_id, judge, phase, test_file)
            rows.append(
                {
                    "run_id": run_id,
                    "judge": judge,
                    "phase": phase,
                    "test_number": parse_test_number(test_file.name),
                    "test_file": str(test_file.relative_to(suite_root)),
                    "result_file": str(result_file.relative_to(suite_root)),
                    "status": "PENDING",
                    "execution_start_utc": "",
                    "execution_end_utc": "",
                    "last_updated_utc": datetime.now(timezone.utc).isoformat(),
                }
            )

    manifest = {
        "run_id": run_id,
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "suite_root": str(suite_root),
        "judges": judges,
        "ordering": "judge-major, one test at a time, phase 1->2->3 within each judge",
        "total_tests": len(rows),
    }
    (run_root / "manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")

    with (run_root / "execution_log.csv").open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=[
                "run_id",
                "judge",
                "phase",
                "test_number",
                "test_file",
                "result_file",
                "status",
                "execution_start_utc",
                "execution_end_utc",
                "last_updated_utc",
            ],
        )
        writer.writeheader()
        writer.writerows(rows)

    print(str(run_root))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
