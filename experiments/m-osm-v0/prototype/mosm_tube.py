#!/usr/bin/env python3
"""Validate and rehydrate evidence-backed M-OSM handoff tubes."""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from datetime import datetime
from pathlib import Path


REQUIRED_TOP_LEVEL = {
    "schema_version",
    "tube_id",
    "producer",
    "objective",
    "created_at",
    "confirmed_facts",
    "corrections",
    "constraints",
    "uncertainties",
    "next_actions",
    "source_refs",
}
ALLOWED_TOP_LEVEL = REQUIRED_TOP_LEVEL | {
    "current_question",
    "valid_until",
    "subject_id",
    "semantic_anchors",
    "claimed_coherence",
}
EVIDENCE_FIELDS = ("confirmed_facts", "constraints", "uncertainties", "next_actions")
MAX_SOURCE_BYTES = 64 * 1024
MAX_TOTAL_BYTES = 256 * 1024


class TubeError(ValueError):
    pass


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def parse_datetime(value: object, field: str) -> datetime:
    if not isinstance(value, str):
        raise TubeError(f"{field} must be an ISO-8601 string")
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError as exc:
        raise TubeError(f"{field} is not valid ISO-8601: {value}") from exc


def validate(tube: dict) -> list[str]:
    if not isinstance(tube, dict):
        raise TubeError("tube must be a JSON object")
    missing = sorted(REQUIRED_TOP_LEVEL - tube.keys())
    extra = sorted(tube.keys() - ALLOWED_TOP_LEVEL)
    if missing:
        raise TubeError(f"missing required fields: {', '.join(missing)}")
    if extra:
        raise TubeError(f"unknown fields: {', '.join(extra)}")
    if tube["schema_version"] not in {"mosm-tube/0.1", "mosm-tube/0.2"}:
        raise TubeError("schema_version must be mosm-tube/0.1 or mosm-tube/0.2")
    if tube["schema_version"] == "mosm-tube/0.2" and "subject_id" not in tube:
        raise TubeError("mosm-tube/0.2 requires subject_id")
    for name in ("tube_id", "producer", "objective"):
        if not isinstance(tube[name], str) or not tube[name].strip():
            raise TubeError(f"{name} must be a non-empty string")
    if "subject_id" in tube and (
        not isinstance(tube["subject_id"], str) or not tube["subject_id"].strip()
    ):
        raise TubeError("subject_id must be a non-empty string")
    parse_datetime(tube["created_at"], "created_at")
    if tube.get("valid_until") is not None:
        parse_datetime(tube["valid_until"], "valid_until")
    anchors = tube.get("semantic_anchors", [])
    if not isinstance(anchors, list) or len(anchors) > 24:
        raise TubeError("semantic_anchors must be an array of at most 24 strings")
    if any(not isinstance(item, str) or not item for item in anchors):
        raise TubeError("semantic_anchors contains a non-string or empty item")
    if len(set(anchors)) != len(anchors):
        raise TubeError("semantic_anchors must be unique")

    refs = tube["source_refs"]
    if not isinstance(refs, list) or not refs:
        raise TubeError("source_refs must be a non-empty array")
    ref_ids = set()
    for index, ref in enumerate(refs):
        if not isinstance(ref, dict):
            raise TubeError(f"source_refs[{index}] must be an object")
        if set(ref) != {"id", "path", "sha256", "required"}:
            raise TubeError(f"source_refs[{index}] has wrong fields")
        if not isinstance(ref["id"], str) or not ref["id"]:
            raise TubeError(f"source_refs[{index}].id must be non-empty")
        if ref["id"] in ref_ids:
            raise TubeError(f"duplicate source ref id: {ref['id']}")
        ref_ids.add(ref["id"])
        if not isinstance(ref["path"], str) or not ref["path"]:
            raise TubeError(f"source_refs[{index}].path must be non-empty")
        sha = ref["sha256"]
        if not isinstance(sha, str) or len(sha) != 64 or any(c not in "0123456789abcdef" for c in sha):
            raise TubeError(f"source_refs[{index}].sha256 must be lowercase hex")
        if not isinstance(ref["required"], bool):
            raise TubeError(f"source_refs[{index}].required must be boolean")

    item_ids = set()
    used_refs = set()
    for field in EVIDENCE_FIELDS:
        values = tube[field]
        if not isinstance(values, list):
            raise TubeError(f"{field} must be an array")
        if field == "next_actions" and len(values) > 3:
            raise TubeError("next_actions may contain at most three items")
        for index, item in enumerate(values):
            if not isinstance(item, dict) or set(item) != {"id", "text", "source_ref"}:
                raise TubeError(f"{field}[{index}] has wrong shape")
            if any(not isinstance(item[name], str) or not item[name] for name in item):
                raise TubeError(f"{field}[{index}] contains an empty value")
            if item["id"] in item_ids:
                raise TubeError(f"duplicate evidence item id: {item['id']}")
            item_ids.add(item["id"])
            used_refs.add(item["source_ref"])

    corrections = tube["corrections"]
    if not isinstance(corrections, list):
        raise TubeError("corrections must be an array")
    for index, item in enumerate(corrections):
        expected = {"id", "supersedes", "replacement", "source_ref"}
        if not isinstance(item, dict) or set(item) != expected:
            raise TubeError(f"corrections[{index}] has wrong shape")
        if any(not isinstance(item[name], str) or not item[name] for name in item):
            raise TubeError(f"corrections[{index}] contains an empty value")
        if item["id"] in item_ids:
            raise TubeError(f"duplicate evidence item id: {item['id']}")
        item_ids.add(item["id"])
        used_refs.add(item["source_ref"])

    unknown_refs = sorted(used_refs - ref_ids)
    if unknown_refs:
        raise TubeError(f"evidence cites unknown source refs: {', '.join(unknown_refs)}")
    coherence = tube.get("claimed_coherence")
    if coherence is not None and (
        isinstance(coherence, bool)
        or not isinstance(coherence, (int, float))
        or not 0 <= coherence <= 1
    ):
        raise TubeError("claimed_coherence must be null or a number in [0,1]")
    return sorted(ref_ids)


def inside_any(path: Path, roots: list[Path]) -> bool:
    resolved = path.resolve(strict=True)
    for root in roots:
        try:
            resolved.relative_to(root.resolve(strict=True))
            return True
        except ValueError:
            continue
    return False


def resolve_source(path: Path, allowed_roots: list[Path]) -> Path | None:
    candidates = [path] if path.is_absolute() else [root / path for root in allowed_roots]
    for candidate in candidates:
        try:
            resolved = candidate.resolve(strict=True)
        except FileNotFoundError:
            continue
        if not resolved.is_file() or not inside_any(resolved, allowed_roots):
            raise TubeError(f"source is outside allowed roots or not a file: {path}")
        return resolved
    return None


def verify_sources(tube: dict, allowed_roots: list[Path]) -> list[dict]:
    if not allowed_roots:
        raise TubeError("at least one --allow-root is required for rehydration")
    verified = []
    total = 0
    for ref in tube["source_refs"]:
        path = Path(ref["path"])
        resolved = resolve_source(path, allowed_roots)
        if resolved is None:
            if ref["required"]:
                raise TubeError(f"required source missing: {path}")
            continue
        with resolved.open("rb") as handle:
            content = handle.read(MAX_SOURCE_BYTES + 1)
        size = len(content)
        if size > MAX_SOURCE_BYTES:
            raise TubeError(f"source exceeds per-file limit: {path} ({size} bytes read)")
        total += size
        if total > MAX_TOTAL_BYTES:
            raise TubeError(f"sources exceed total limit: {total} bytes")
        actual = hashlib.sha256(content).hexdigest()
        if actual != ref["sha256"]:
            raise TubeError(
                f"source hash mismatch: {path}; expected {ref['sha256']}, got {actual}"
            )
        try:
            text = content.decode("utf-8")
        except UnicodeDecodeError as exc:
            raise TubeError(f"source is not valid UTF-8 text: {path}") from exc
        verified.append(
            {
                "id": ref["id"],
                "path": ref["path"],
                "resolved_path": resolved,
                "bytes": size,
                "sha256": actual,
                "text": text,
            }
        )
    return verified


def render_packet(tube: dict, verified: list[dict], packet_mode: str = "compact") -> str:
    lines = [
        "# Rehydrated Handoff",
        "",
        f"Tube ID: `{tube['tube_id']}`",
        *([f"Subject ID: `{tube['subject_id']}`"] if tube.get("subject_id") else []),
        f"Producer: `{tube['producer']}`",
        f"Objective: {tube['objective']}",
        "",
        "The producer's claimed coherence is untrusted. The sources below passed",
        "path, size, and SHA-256 checks for this run. Later explicit corrections",
        "in a verified source override earlier statements.",
    ]
    if packet_mode == "audit":
        lines.extend(
            [
                "",
                "## Structured Handoff",
                "",
                "```json",
                json.dumps(tube, indent=2, ensure_ascii=False),
                "```",
            ]
        )
    lines.extend(["", "## Verified Sources"])
    for ref in verified:
        lines.extend(
            [
                "",
                f"### {ref['id']}",
                "",
                f"- Path: `{ref['path']}`",
                f"- SHA-256: `{ref['sha256']}`",
                f"- Bytes: `{ref['bytes']}`",
                "",
                ref["text"],
            ]
        )
    return "\n".join(lines).rstrip() + "\n"


def load(path: Path) -> dict:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise TubeError(f"cannot load tube {path}: {exc}") from exc


def main() -> int:
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="command", required=True)
    validate_parser = subparsers.add_parser("validate")
    validate_parser.add_argument("tube", type=Path)
    rehydrate_parser = subparsers.add_parser("rehydrate")
    rehydrate_parser.add_argument("tube", type=Path)
    rehydrate_parser.add_argument("--allow-root", type=Path, action="append", required=True)
    rehydrate_parser.add_argument("--output", type=Path, required=True)
    rehydrate_parser.add_argument(
        "--packet-mode", choices=("compact", "audit"), default="compact"
    )
    args = parser.parse_args()

    try:
        tube = load(args.tube)
        refs = validate(tube)
        if args.command == "validate":
            print(json.dumps({"status": "ok", "tube_id": tube["tube_id"], "source_refs": refs}))
            return 0
        verified = verify_sources(tube, args.allow_root)
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(
            render_packet(tube, verified, packet_mode=args.packet_mode), encoding="utf-8"
        )
        print(
            json.dumps(
                {
                    "status": "ok",
                    "tube_id": tube["tube_id"],
                    "verified_sources": len(verified),
                    "packet_mode": args.packet_mode,
                    "output": str(args.output),
                }
            )
        )
        return 0
    except TubeError as exc:
        print(json.dumps({"status": "hold", "error": str(exc)}), file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
