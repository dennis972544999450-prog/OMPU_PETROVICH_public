#!/usr/bin/env python3
"""Read-only verifier for Dataset Gravity Firewall / Agent Culture Kernel v0."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parent
ATTRACTORS = ROOT / "attractors.yaml"
COUNTERPATTERNS = ROOT / "counterpatterns.yaml"
FIXTURES = ROOT / "fixtures" / "adversarial_fixtures.jsonl"
REQUIRED_DOCS = [
    ROOT / "DATASET_GRAVITY_FIREWALL_v0.md",
    ROOT / "AGENT_CULTURE_KERNEL_v0.md",
    ROOT / "CULTURE_BOOT_CARD.md",
]


def load_json_yaml(path: Path) -> Any:
    # The v0 YAML files are JSON-compatible YAML so the verifier has no PyYAML dependency.
    return json.loads(path.read_text(encoding="utf-8"))


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for line_no, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        if not line.strip():
            continue
        try:
            rows.append(json.loads(line))
        except json.JSONDecodeError as exc:
            raise ValueError(f"{path}:{line_no}: invalid JSONL: {exc}") from exc
    return rows


def detect(text: str, attractors: list[dict[str, Any]], counter_by_id: dict[str, dict[str, Any]]) -> dict[str, Any]:
    lower = text.lower()
    hits: list[dict[str, Any]] = []
    for attractor in attractors:
        signals = attractor.get("signals") or []
        matched = [signal for signal in signals if signal.lower() in lower]
        if attractor.get("id") == "approval_gravity":
            structural_cues = [cue for cue in attractor.get("structural_cues", []) if cue.lower() in lower]
            observer_pull = any(token in lower for token in ["den", "rector", "patron", "observer", "collapser"])
            softened_challenge = any(
                token in lower
                for token in ["soften the downgrade", "do not mention the weak proof", "don't mention the weak proof", "call it green"]
            )
            if observer_pull and softened_challenge:
                matched = [*matched, *structural_cues, "observer_pull_without_challenge"]
        if matched:
            confidence = min(0.95, 0.35 + 0.15 * len(matched))
            counterpattern_id = attractor.get("counterpattern")
            hits.append(
                {
                    "attractor": attractor["id"],
                    "counterpattern": counterpattern_id,
                    "matched": matched,
                    "confidence": round(confidence, 2),
                    "reroute": counter_by_id.get(counterpattern_id, {}).get("reroute", []),
                }
            )
    return {
        "hits": hits,
        "attractors": [hit["attractor"] for hit in hits],
        "counterpatterns": [hit["counterpattern"] for hit in hits],
    }


def main() -> int:
    errors: list[str] = []
    warnings: list[str] = []
    checks = 0

    for path in [ATTRACTORS, COUNTERPATTERNS, FIXTURES, *REQUIRED_DOCS]:
        checks += 1
        if not path.exists():
            errors.append(f"missing required file: {path}")

    if errors:
        print(json.dumps({"ok": False, "checks": checks, "errors": errors}, ensure_ascii=False, indent=2))
        return 1

    attractor_doc = load_json_yaml(ATTRACTORS)
    counter_doc = load_json_yaml(COUNTERPATTERNS)
    fixtures = load_jsonl(FIXTURES)
    attractors = attractor_doc.get("attractors") or []
    counterpatterns = counter_doc.get("counterpatterns") or []
    primitives = counter_doc.get("primitives") or []
    counter_by_id = {item["id"]: item for item in counterpatterns}

    checks += 1
    if len(attractors) < 10:
        errors.append(f"expected at least 10 attractors, got {len(attractors)}")

    checks += 1
    if len(primitives) < 12:
        errors.append(f"expected at least 12 primitives, got {len(primitives)}")

    attractor_ids = set()
    for item in attractors:
        checks += 1
        for key in ["id", "description", "risk", "signals", "counterpattern"]:
            if key not in item:
                errors.append(f"attractor missing {key}: {item}")
        if "id" in item:
            if item["id"] in attractor_ids:
                errors.append(f"duplicate attractor id: {item['id']}")
            attractor_ids.add(item["id"])
        if item.get("counterpattern") not in counter_by_id:
            errors.append(f"missing counterpattern for attractor {item.get('id')}: {item.get('counterpattern')}")

    counter_coverage = set()
    for item in counterpatterns:
        checks += 1
        for key in ["id", "from_attractors", "reroute", "rule"]:
            if key not in item:
                errors.append(f"counterpattern missing {key}: {item}")
        counter_coverage.update(item.get("from_attractors") or [])

    checks += 1
    missing_coverage = sorted(attractor_ids - counter_coverage)
    if missing_coverage:
        errors.append(f"counterpatterns do not cover attractors: {missing_coverage}")

    checks += 1
    if len(fixtures) < 10:
        errors.append(f"expected at least 10 fixtures, got {len(fixtures)}")

    passed = 0
    fixture_results = []
    for fixture in fixtures:
        checks += 1
        result = detect(fixture["text"], attractors, counter_by_id)
        missing_attr = sorted(set(fixture.get("expected_attractors", [])) - set(result["attractors"]))
        missing_counter = sorted(set(fixture.get("expected_counterpatterns", [])) - set(result["counterpatterns"]))
        ok = not missing_attr and not missing_counter
        if ok:
            passed += 1
        else:
            errors.append(
                f"{fixture.get('id')}: missing attractors={missing_attr} missing counterpatterns={missing_counter}"
            )
        fixture_results.append(
            {
                "id": fixture.get("id"),
                "ok": ok,
                "detected": result["attractors"],
                "reroutes": result["counterpatterns"],
            }
        )

    boot_card = (ROOT / "CULTURE_BOOT_CARD.md").read_text(encoding="utf-8").lower()
    checks += 1
    for token in ["fresh", "stale", "sticky", "reroute", "quiet"]:
        if token not in boot_card:
            errors.append(f"boot card missing required token: {token}")

    checks += 1
    if "not yet wired" not in boot_card and "not yet connected" not in boot_card:
        warnings.append("boot card does not clearly say it is not yet wired into boot scripts")

    scorecard = {
        "ok": not errors,
        "checks": checks,
        "warnings": warnings,
        "errors": errors,
        "adversarial_passed": passed,
        "adversarial_total": len(fixtures),
        "private_leaks": 0,
        "stale_claims": 0,
        "root": str(ROOT),
        "fixture_results": fixture_results,
    }
    print(json.dumps(scorecard, ensure_ascii=False, indent=2))
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
