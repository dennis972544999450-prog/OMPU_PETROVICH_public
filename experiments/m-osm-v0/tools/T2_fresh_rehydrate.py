#!/usr/bin/env python3
"""Attempt tube-only rehydration without reading contextual external state."""

from __future__ import annotations

import builtins
import json
import sys


def _deny_file_reads(*_args: object, **_kwargs: object) -> object:
    raise RuntimeError("external file reads are disabled for the fresh-process test")


def main() -> int:
    builtins.open = _deny_file_reads
    request = json.load(sys.stdin)
    tube = request["tube"]
    requested_fields = request["requested_fields"]

    recovered = {}
    unsupported = []
    for field in requested_fields:
        if field in tube:
            recovered[field] = tube[field]
        else:
            recovered[field] = None
            unsupported.append(field)

    result = {
        "status": "explicit_tube_fields_only",
        "recovered": recovered,
        "unsupported_context_fields": unsupported,
        "hash_preimage": None,
        "external_context_reads": [],
        "reason": (
            "The input contains no source payload, source reference, decoder, or "
            "candidate corpus from which omitted context or a hash preimage can be recovered."
        ),
    }
    json.dump(result, sys.stdout, ensure_ascii=False, indent=2, sort_keys=True)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
