#!/usr/bin/env python3
"""
Hard preflight gate for adversarial trial validity.

Fails fast if /api/query is in echo/degraded mode or missing adjudication fields.
"""

from __future__ import annotations

import argparse
import json
import sys
import urllib.error
import urllib.request


def post_json(url: str, payload: dict) -> dict:
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        url=url,
        data=data,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=20) as resp:
        raw = resp.read().decode("utf-8", errors="replace")
        return json.loads(raw)


def run_preflight(api_base: str) -> tuple[bool, str]:
    url = f"{api_base.rstrip('/')}/api/query"
    paradox_prompt = (
        "Two events are defined with contradictory temporal constraints: "
        "EventA occurs after EventB, and EventB occurs after EventA. "
        "Determine if execution can proceed without violating causality. "
        "Provide formal reasoning."
    )
    try:
        body = post_json(url, {"query": paradox_prompt})
    except urllib.error.URLError as e:
        return False, f"endpoint_unreachable: {e}"
    except Exception as e:
        return False, f"request_failed: {e}"

    response = str(body.get("response", ""))
    reasoning = body.get("reasoning")

    if response.startswith("Query processed:"):
        return False, "echo_mode_detected"
    if not isinstance(reasoning, dict):
        return False, "missing_reasoning_block"
    if reasoning.get("classification") in ("general_query", None, ""):
        return False, "non_adjudication_reasoning"
    if not reasoning.get("verdict"):
        return False, "missing_verdict"

    return True, "ok"


def main() -> int:
    parser = argparse.ArgumentParser(description="Preflight gate for adversarial trial validity")
    parser.add_argument("--api-base", default="http://127.0.0.1:8003")
    args = parser.parse_args()

    ok, reason = run_preflight(args.api_base)
    print(json.dumps({"ok": ok, "reason": reason, "api_base": args.api_base}, indent=2))
    return 0 if ok else 2


if __name__ == "__main__":
    raise SystemExit(main())

