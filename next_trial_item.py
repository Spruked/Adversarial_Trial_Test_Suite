#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser(description="Print next pending adversarial trial item")
    parser.add_argument("--run-id", required=True)
    parser.add_argument("--suite-path", default="Adversarial_Trial_Test_Suite")
    args = parser.parse_args()

    run_root = Path(args.suite_path).resolve() / "runs" / args.run_id
    log_path = run_root / "execution_log.csv"
    manifest_path = run_root / "manifest.json"
    if not log_path.exists():
        raise SystemExit(f"missing log: {log_path}")
    if not manifest_path.exists():
        raise SystemExit(f"missing manifest: {manifest_path}")

    with log_path.open("r", encoding="utf-8", newline="") as f:
        rows = list(csv.DictReader(f))
    with manifest_path.open("r", encoding="utf-8") as f:
        manifest = json.load(f)

    judge_order = {name: idx for idx, name in enumerate(manifest.get("judges", []))}
    rows.sort(key=lambda r: (judge_order.get(r["judge"], 999), int(r["phase"])))
    for row in rows:
        if row["status"] == "PENDING":
            print(json.dumps(row, indent=2))
            return 0

    print(json.dumps({"status": "COMPLETE", "message": "no pending tests"}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
