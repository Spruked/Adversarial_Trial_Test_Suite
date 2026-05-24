#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
from datetime import datetime, timezone
from pathlib import Path


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def main() -> int:
    parser = argparse.ArgumentParser(description="Record a single adversarial trial result")
    parser.add_argument("--run-id", required=True)
    parser.add_argument("--judge", required=True)
    parser.add_argument("--phase", type=int, required=True)
    parser.add_argument("--status", required=True, choices=["PENDING", "RUNNING", "PASS", "FAIL", "ERROR", "SKIPPED"])
    parser.add_argument("--suite-path", default="Adversarial_Trial_Test_Suite")
    parser.add_argument("--start", default="")
    parser.add_argument("--end", default="")
    args = parser.parse_args()

    run_root = Path(args.suite_path).resolve() / "runs" / args.run_id
    log_path = run_root / "execution_log.csv"
    if not log_path.exists():
        raise SystemExit(f"missing log: {log_path}")

    with log_path.open("r", encoding="utf-8", newline="") as f:
        rows = list(csv.DictReader(f))

    updated = False
    for row in rows:
        if row["judge"] == args.judge and int(row["phase"]) == args.phase:
            row["status"] = args.status
            if args.status == "PENDING":
                row["execution_start_utc"] = ""
                row["execution_end_utc"] = ""
                row["last_updated_utc"] = utc_now()
                updated = True
                break
            if args.start:
                row["execution_start_utc"] = args.start
            elif args.status == "RUNNING" and not row["execution_start_utc"]:
                row["execution_start_utc"] = utc_now()

            if args.end:
                row["execution_end_utc"] = args.end
            elif args.status in {"PASS", "FAIL", "ERROR", "SKIPPED"}:
                row["execution_end_utc"] = utc_now()

            row["last_updated_utc"] = utc_now()
            updated = True
            break

    if not updated:
        raise SystemExit(f"row not found for judge={args.judge}, phase={args.phase}")

    with log_path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)

    print(f"updated: judge={args.judge} phase={args.phase} status={args.status}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
