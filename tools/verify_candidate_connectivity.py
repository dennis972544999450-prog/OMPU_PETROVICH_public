#!/usr/bin/env python3
"""Verify an OMPU bus-compaction candidate without writing any state."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


REPORT_SCHEMA = "ompu.bus-compaction-connectivity-shadow.v1"


def verify_candidate(
    candidate: Any,
    *,
    candidate_path: Path | None = None,
) -> dict[str, Any]:
    errors: list[str] = []
    if not isinstance(candidate, dict):
        return {
            "schema": REPORT_SCHEMA,
            "ok": False,
            "candidate_path": str(candidate_path) if candidate_path else None,
            "compaction_id": None,
            "outcome": None,
            "metrics": {},
            "orphan_block_ids": [],
            "unlinked_zusammenfassung_ids": [],
            "unknown_endpoints": [],
            "errors": ["candidate must be an object"],
        }

    if candidate.get("destination") != "candidate":
        errors.append("destination must be candidate")
    live_writes = candidate.get("live_writes")
    if type(live_writes) is not int or live_writes != 0:
        errors.append("live_writes must be integer 0")

    outcome = candidate.get("outcome")
    blocks = candidate.get("blocks")
    edges = candidate.get("edges")
    if not isinstance(blocks, list):
        errors.append("blocks must be a list")
        blocks = []
    if not isinstance(edges, list):
        errors.append("edges must be a list")
        edges = []
    if outcome in {"quiet", "refusal"} and blocks:
        errors.append(f"{outcome} outcome must not carry blocks")

    block_ids: list[str] = []
    block_kinds: dict[str, str | None] = {}
    seen_block_ids: set[str] = set()
    for index, block in enumerate(blocks):
        locus = f"blocks[{index}]"
        if not isinstance(block, dict):
            errors.append(f"{locus} must be an object")
            continue
        block_id = block.get("block_id")
        if not isinstance(block_id, str) or not block_id:
            errors.append(f"{locus}.block_id must be a non-empty string")
            continue
        if block_id in seen_block_ids:
            errors.append(f"{locus}.block_id must be unique")
            continue
        seen_block_ids.add(block_id)
        block_ids.append(block_id)
        block_kinds[block_id] = block.get("kind")

    incident_block_ids: set[str] = set()
    unknown_endpoints: list[dict[str, Any]] = []
    malformed_edge_count = 0
    for index, edge in enumerate(edges):
        locus = f"edges[{index}]"
        if not isinstance(edge, dict):
            errors.append(f"{locus} must be an object")
            malformed_edge_count += 1
            continue
        edge_id = edge.get("edge_id")
        src = edge.get("from_block_id")
        dst = edge.get("to_block_id")
        if not isinstance(src, str) or not src or not isinstance(dst, str) or not dst:
            errors.append(f"{locus} endpoints must be non-empty strings")
            malformed_edge_count += 1
            continue
        missing = [endpoint for endpoint in (src, dst) if endpoint not in seen_block_ids]
        if missing:
            unknown_endpoints.append(
                {
                    "edge_id": edge_id if isinstance(edge_id, str) else f"index:{index}",
                    "block_ids": missing,
                }
            )
            continue
        incident_block_ids.update((src, dst))

    if unknown_endpoints:
        errors.append(f"edges reference unknown blocks: {len(unknown_endpoints)}")

    orphan_block_ids = sorted(set(block_ids) - incident_block_ids)
    if orphan_block_ids:
        errors.append(f"blocks without incident edges: {len(orphan_block_ids)}")
    unlinked_zusammenfassung_ids = sorted(
        block_id
        for block_id in orphan_block_ids
        if block_kinds.get(block_id) == "zusammenfassung"
    )
    if unlinked_zusammenfassung_ids:
        errors.append(
            "zusammenfassung blocks without incident edges: "
            f"{len(unlinked_zusammenfassung_ids)}"
        )

    return {
        "schema": REPORT_SCHEMA,
        "ok": not errors,
        "candidate_path": str(candidate_path) if candidate_path else None,
        "compaction_id": candidate.get("compaction_id"),
        "outcome": outcome,
        "metrics": {
            "block_count": len(blocks),
            "edge_count": len(edges),
            "orphan_block_count": len(orphan_block_ids),
            "unlinked_zusammenfassung_count": len(unlinked_zusammenfassung_ids),
            "unknown_endpoint_count": len(unknown_endpoints),
            "malformed_edge_count": malformed_edge_count,
        },
        "orphan_block_ids": orphan_block_ids,
        "unlinked_zusammenfassung_ids": unlinked_zusammenfassung_ids,
        "unknown_endpoints": unknown_endpoints,
        "errors": errors,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--candidate", type=Path, required=True)
    args = parser.parse_args()
    try:
        candidate = json.loads(args.candidate.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        report = {
            "schema": REPORT_SCHEMA,
            "ok": False,
            "candidate_path": str(args.candidate),
            "compaction_id": None,
            "outcome": None,
            "metrics": {},
            "orphan_block_ids": [],
            "unlinked_zusammenfassung_ids": [],
            "unknown_endpoints": [],
            "errors": [f"candidate could not be read: {error}"],
        }
    else:
        report = verify_candidate(candidate, candidate_path=args.candidate)
    print(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True))
    return 0 if report["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())

