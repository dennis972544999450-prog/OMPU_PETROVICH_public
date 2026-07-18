#!/usr/bin/env python3
"""Probe whether an input packet contains enough information to recover context."""

import argparse
import hashlib
import json
import sys


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--mode", choices=("tube-only", "hash-only"), default="tube-only"
    )
    args = parser.parse_args()

    raw = sys.stdin.buffer.read()
    try:
        packet = json.loads(raw)
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        print(json.dumps({"status": "parse_error", "error": str(exc)}, indent=2))
        return 3

    context_fields = (
        "full_context",
        "interaction_history",
        "confirmed_facts",
        "source_refs",
    )
    present_context_fields = [name for name in context_fields if name in packet]
    hash_fields = [name for name in packet if "hash" in name or "digest" in name]

    result = {
        "mode": args.mode,
        "isolated_python": bool(sys.flags.isolated),
        "input_sha256": hashlib.sha256(raw).hexdigest(),
        "input_keys": sorted(packet),
        "external_state_reads": [],
        "present_context_fields": present_context_fields,
        "hash_fields": hash_fields,
        "rehydrated_context": None,
    }

    if present_context_fields:
        result.update(
            {
                "status": "embedded_context_only",
                "reason": "Context-bearing data is already embedded; no latent recovery occurred.",
            }
        )
        print(json.dumps(result, indent=2, sort_keys=True))
        return 1

    if hash_fields:
        result.update(
            {
                "status": "hash_not_recovered",
                "reason": (
                    "A digest supplies an equality check, not a preimage or a candidate corpus. "
                    "No context can be selected from the packet alone."
                ),
            }
        )
        print(json.dumps(result, indent=2, sort_keys=True))
        return 2

    result.update(
        {
            "status": "insufficient_information",
            "reason": (
                "The packet has no context, interaction history, evidence references, "
                "or specified attractor-state digest."
            ),
        }
    )
    print(json.dumps(result, indent=2, sort_keys=True))
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
