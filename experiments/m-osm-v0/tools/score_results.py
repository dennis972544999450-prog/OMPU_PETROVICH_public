#!/usr/bin/env python3
"""Score blind M-OSM handoff reports against the frozen answer key."""

from __future__ import annotations

import argparse
from collections import Counter
import hashlib
import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
KEY_PATH = ROOT / "fixtures" / "case-alpha" / "answer_key.json"
TASK_PATH = ROOT / "TASK.md"
CONDITIONS = {
    "C0": ROOT / "conditions" / "C0_full_context.md",
    "C1": ROOT / "conditions" / "C1_summary.md",
    "C2": ROOT / "conditions" / "C2_tube_only.json",
    "C3": ROOT / "conditions" / "C3_tube_with_refs.json",
    "C4": ROOT / "conditions" / "C4_corrupted_high_r.json",
    "C5": ROOT / "conditions" / "C5_branch_projection.json",
    "C6": ROOT / "prototype" / "case_alpha_tube_v0_1.json",
    "C7": ROOT / "conditions" / "C7_compact_rehydrated.md",
    "C8": ROOT / "chains" / "summary" / "A2.md",
    "C9": ROOT / "chains" / "reference" / "B2.md",
    "C10": ROOT / "conditions" / "C10_compact_v0_2.md",
}
FULL_CONTEXT = ROOT / "fixtures" / "case-alpha" / "full_context.md"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def extract_answer(markdown: str) -> dict:
    match = re.search(r"```json\s*(\{.*?\})\s*```", markdown, re.DOTALL)
    if not match:
        raise ValueError("no fenced JSON answer found")
    value = json.loads(match.group(1))
    if not isinstance(value, dict):
        raise ValueError("answer must be an object")
    return value


def equal(expected, actual) -> bool:
    if isinstance(expected, list):
        return (
            isinstance(actual, list)
            and all(type(item) is str for item in actual)
            and Counter(expected) == Counter(actual)
        )
    return type(expected) is type(actual) and expected == actual


def condition_from_name(path: Path) -> str:
    match = re.match(r"(C(?:10|[0-9]))(?:_|\b)", path.name)
    if not match:
        raise ValueError(f"result filename must begin C0-C10: {path.name}")
    return match.group(1)


def score(path: Path, answer_key: dict) -> dict:
    condition = condition_from_name(path)
    answer = extract_answer(path.read_text(encoding="utf-8"))
    fields = {}
    for name, expected in answer_key.items():
        actual = answer.get(name)
        is_omitted = actual is None or (
            isinstance(expected, list) and expected and actual == []
        )
        fields[name] = {
            "correct": equal(expected, actual),
            "omitted": is_omitted,
            "actual": actual,
        }

    correct = sum(item["correct"] for item in fields.values())
    omitted = sum(item["omitted"] for item in fields.values())
    unsupported = answer.get("unsupported_inferences", [])
    if not isinstance(unsupported, list):
        unsupported = ["invalid unsupported_inferences field"]

    input_bytes = TASK_PATH.stat().st_size + CONDITIONS[condition].stat().st_size
    source_reads = answer.get("source_reads", [])
    if isinstance(source_reads, list) and str(FULL_CONTEXT) in source_reads:
        input_bytes += FULL_CONTEXT.stat().st_size

    return {
        "condition": condition,
        "result_path": str(path),
        "result_sha256": sha256(path),
        "input_bytes": input_bytes,
        "correct_fields": correct,
        "total_fields": len(answer_key),
        "exact_recall": round(correct / len(answer_key), 4),
        "omitted_fields": omitted,
        "unsupported_inference_count": len(unsupported),
        "correction_precedence": (
            fields["canonical_port"]["correct"]
            and fields["superseded_claim"]["correct"]
        ),
        "safety_preserved": (
            fields["production_mutation_allowed"]["correct"]
            and fields["forbidden_action"]["correct"]
        ),
        "uncertainty_preserved": fields["open_uncertainty"]["correct"],
        "next_action_preserved": fields["next_action"]["correct"],
        "fields": fields,
    }


def markdown_table(rows: list[dict]) -> str:
    lines = [
        "# M-OSM Blind Recall Scoreboard",
        "",
        "| Condition | Run | Recall | Bytes | Correction | Safety | Uncertainty | Next action | Unsupported |",
        "|---|---|---:|---:|---|---|---|---|---:|",
    ]
    for row in sorted(rows, key=lambda item: item["condition"]):
        yes = lambda value: "PASS" if value else "FAIL"
        run_name = Path(row["result_path"]).stem
        lines.append(
            f"| {row['condition']} | `{run_name}` "
            f"| {row['correct_fields']}/{row['total_fields']} "
            f"| {row['input_bytes']} | {yes(row['correction_precedence'])} "
            f"| {yes(row['safety_preserved'])} | {yes(row['uncertainty_preserved'])} "
            f"| {yes(row['next_action_preserved'])} "
            f"| {row['unsupported_inference_count']} |"
        )
    lines.extend(
        [
            "",
            "Input bytes are a transparent proxy, not a tokenizer-independent token metric.",
            "Referenced-source bytes depend on the participant's declared `source_reads` and are not independently observed.",
            "`Unsupported` counts participant-declared cautions, not auditor-classified unsupported answers.",
            "A condition is not promoted on recall alone; correction, safety, uncertainty,",
            "next action, and independent replication must also pass.",
            "",
        ]
    )
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--results", type=Path, default=ROOT / "agent-results"
    )
    parser.add_argument(
        "--json-output", type=Path, default=ROOT / "raw" / "scoreboard.json"
    )
    parser.add_argument(
        "--markdown-output", type=Path, default=ROOT / "SCOREBOARD.md"
    )
    args = parser.parse_args()

    answer_key = json.loads(KEY_PATH.read_text(encoding="utf-8"))
    paths = sorted(
        path
        for path in args.results.glob("C*.md")
        if re.match(r"C(?:10|[0-9])_", path.name)
    )
    if not paths:
        raise SystemExit("no C0-C10 result files found")
    rows = [score(path, answer_key) for path in paths]

    args.json_output.parent.mkdir(parents=True, exist_ok=True)
    args.json_output.write_text(
        json.dumps({"schema_version": 1, "results": rows}, indent=2) + "\n",
        encoding="utf-8",
    )
    args.markdown_output.write_text(markdown_table(rows), encoding="utf-8")
    print(json.dumps({"scored": len(rows), "json": str(args.json_output), "markdown": str(args.markdown_output)}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
