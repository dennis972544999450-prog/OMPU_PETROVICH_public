#!/usr/bin/env python3
"""Executable-spec checks for the machine-readable Part 3 M-OSM claim."""

from __future__ import annotations

import hashlib
import json
import math
import os
from pathlib import Path
import re
import string
import subprocess
import sys
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "raw"
SOURCE = Path("/Users/denbell/Downloads/Swarm Oscillatory Memory (M-OSM).md")
CLAIMS = ROOT / "CLAIMS.md"
EXPECTED_SOURCE_SHA256 = "2367703aff86e220faacb8748d14812ba5978540fba42f0beb1b2146a2a97668"
PART3_HEADING = "## **Part 3: Machine-Readable Operational JSON Dataset**"
PART4_HEADING = "## **Part 4: Swarm Prompt-Instruction for Sub-agents (Direct Injection)**"
VALID_JSON_ESCAPE_INITIALS = set('"\\/bfnrtu')
MARKDOWN_ESCAPABLE_PUNCTUATION = set(string.punctuation)


def write_text(name: str, content: str) -> None:
    assert name.startswith("T2_")
    RAW.joinpath(name).write_text(content, encoding="utf-8")


def write_json(name: str, value: Any) -> None:
    write_text(name, json.dumps(value, indent=2, ensure_ascii=False, sort_keys=True) + "\n")


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def extract_part3_block(source_text: str) -> tuple[str, dict[str, Any]]:
    part3_start = source_text.index(PART3_HEADING)
    part4_start = source_text.index(PART4_HEADING, part3_start)
    section = source_text[part3_start:part4_start]
    marker_match = re.search(r"(?m)^JSON[ \t]*$", section[len(PART3_HEADING) :])
    if marker_match is None:
        raise ValueError("Part 3 does not contain a standalone JSON marker line")
    marker_offset = len(PART3_HEADING) + marker_match.start()
    marker_end = len(PART3_HEADING) + marker_match.end()
    object_start = section.index("{", marker_end)
    object_end = section.rfind("}")
    if object_end <= object_start:
        raise ValueError("Part 3 does not contain a complete object-looking block")

    block = section[object_start : object_end + 1]
    source_char_start = part3_start + object_start
    source_char_end = part3_start + object_end + 1
    metadata = {
        "part3_heading": PART3_HEADING,
        "part4_heading": PART4_HEADING,
        "language_marker_repr": repr(section[marker_offset:marker_end]),
        "source_character_start_zero_based": source_char_start,
        "source_character_end_exclusive_zero_based": source_char_end,
        "source_byte_start_zero_based": len(source_text[:source_char_start].encode("utf-8")),
        "source_byte_end_exclusive_zero_based": len(source_text[:source_char_end].encode("utf-8")),
        "block_sha256": sha256_bytes(block.encode("utf-8")),
        "block_bytes": len(block.encode("utf-8")),
        "extraction_rule": (
            "Between the exact Part 3 and Part 4 headings, take the substring from "
            "the first '{' after the standalone JSON marker through the last '}', inclusive."
        ),
    }
    return block, metadata


def markdown_unescape_for_json(block: str) -> tuple[str, dict[str, Any]]:
    output: list[str] = []
    events: list[dict[str, Any]] = []
    illegal_non_markdown: list[dict[str, Any]] = []
    i = 0
    line = 1
    column = 1

    while i < len(block):
        char = block[i]
        if char == "\\" and i + 1 < len(block):
            following = block[i + 1]
            if following not in VALID_JSON_ESCAPE_INITIALS:
                event = {
                    "character_offset_zero_based": i,
                    "line": line,
                    "column": column,
                    "escaped_character": following,
                }
                if following in MARKDOWN_ESCAPABLE_PUNCTUATION:
                    events.append(event)
                    i += 1
                    column += 1
                    continue
                illegal_non_markdown.append(event)
        output.append(char)
        i += 1
        if char == "\n":
            line += 1
            column = 1
        else:
            column += 1

    if illegal_non_markdown:
        raise ValueError(
            "Invalid JSON escapes not covered by Markdown punctuation unescape: "
            + repr(illegal_non_markdown)
        )

    counts: dict[str, int] = {}
    for event in events:
        escaped = event["escaped_character"]
        counts[escaped] = counts.get(escaped, 0) + 1

    transformed = "".join(output)
    manifest = {
        "rule": (
            "Delete only a backslash whose following character is ASCII punctuation "
            "and is not a valid JSON escape initial (quote, backslash, slash, b, f, n, r, t, u)."
        ),
        "non_operations": [
            "No whitespace stripping",
            "No key renaming",
            "No value changes",
            "No formula evaluation",
            "No line-ending normalization after extraction",
        ],
        "deletions": len(events),
        "counts_by_escaped_character": counts,
        "events": events,
        "input_sha256": sha256_bytes(block.encode("utf-8")),
        "output_sha256": sha256_bytes(transformed.encode("utf-8")),
    }
    return transformed, manifest


def strict_python_parse(text: str) -> tuple[Any | None, dict[str, Any]]:
    try:
        parsed = json.loads(text)
    except json.JSONDecodeError as exc:
        return None, {
            "ok": False,
            "exception_type": type(exc).__name__,
            "message": str(exc),
            "line": exc.lineno,
            "column": exc.colno,
            "character_offset_zero_based": exc.pos,
        }
    return parsed, {"ok": True, "top_level_type": type(parsed).__name__}


def run_command(argv: list[str]) -> dict[str, Any]:
    completed = subprocess.run(
        argv,
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    return {
        "argv": argv,
        "display_command": " ".join(argv),
        "exit_code": completed.returncode,
        "stdout": completed.stdout,
        "stderr": completed.stderr,
    }


def json_type_matches(instance: Any, declared: str) -> bool:
    if declared == "object":
        return isinstance(instance, dict)
    if declared == "array":
        return isinstance(instance, list)
    if declared == "string":
        return isinstance(instance, str)
    if declared == "number":
        return isinstance(instance, (int, float)) and not isinstance(instance, bool)
    if declared == "integer":
        return isinstance(instance, int) and not isinstance(instance, bool)
    if declared == "boolean":
        return isinstance(instance, bool)
    if declared == "null":
        return instance is None
    return False


def validate_schema_subset(instance: Any, schema: dict[str, Any], path: str = "$") -> list[str]:
    """Apply every assertion keyword used by the embedded tube schema."""
    errors: list[str] = []
    declared_type = schema.get("type")
    if declared_type is not None and not json_type_matches(instance, declared_type):
        return [f"{path}: expected {declared_type}, got {type(instance).__name__}"]

    if isinstance(instance, dict):
        required = schema.get("required", [])
        for key in required:
            if key not in instance:
                errors.append(f"{path}: missing required property {key!r}")
        properties = schema.get("properties", {})
        for key, value in instance.items():
            if key in properties:
                errors.extend(validate_schema_subset(value, properties[key], f"{path}.{key}"))
            elif schema.get("additionalProperties") is False:
                errors.append(f"{path}: unexpected property {key!r}")

    if isinstance(instance, list):
        if "minItems" in schema and len(instance) < schema["minItems"]:
            errors.append(f"{path}: has {len(instance)} items, minimum is {schema['minItems']}")
        if "maxItems" in schema and len(instance) > schema["maxItems"]:
            errors.append(f"{path}: has {len(instance)} items, maximum is {schema['maxItems']}")
        if "items" in schema:
            for index, value in enumerate(instance):
                errors.extend(validate_schema_subset(value, schema["items"], f"{path}[{index}]"))

    if isinstance(instance, (int, float)) and not isinstance(instance, bool):
        if "minimum" in schema and instance < schema["minimum"]:
            errors.append(f"{path}: {instance} is below minimum {schema['minimum']}")
        if "maximum" in schema and instance > schema["maximum"]:
            errors.append(f"{path}: {instance} exceeds maximum {schema['maximum']}")
    return errors


def schema_checks(config: dict[str, Any]) -> tuple[dict[str, Any], dict[str, Any]]:
    schema = config["identification_tube_schema"]
    required = schema.get("required", [])
    properties = schema.get("properties", {})
    conforming_tube = {
        "tube_id": "tube-shared-counterexample",
        "active_subagent_id": "agent-A",
        "target_motivational_vector": "M1",
        "phase_state": [0.0] * 8,
        "semantic_anchors": ["M-OSM", "handoff"],
        "inverse_temperature_beta": 1.0,
        "coherence_index_r": 0.8,
    }
    semantically_bad_but_schema_valid = {
        **conforming_tube,
        "tube_id": "not-a-uuid",
        "target_motivational_vector": "M9_NOT_DEFINED",
        "semantic_anchors": [],
        "inverse_temperature_beta": -999.0,
        "momentum_gradient": [1.0],
        "undeclared_payload": "accepted because additionalProperties is not false",
    }
    negative_instances = {
        "missing_required": {key: value for key, value in conforming_tube.items() if key != "tube_id"},
        "seven_phase_values": {**conforming_tube, "phase_state": [0.0] * 7},
        "coherence_above_one": {**conforming_tube, "coherence_index_r": 1.01},
    }
    negative_results = {
        name: validate_schema_subset(instance, schema)
        for name, instance in negative_instances.items()
    }
    scalar_errors = validate_schema_subset(7, schema)
    semantically_bad_errors = validate_schema_subset(semantically_bad_but_schema_valid, schema)

    standard_keywords = {
        "$schema",
        "$id",
        "$ref",
        "$defs",
        "title",
        "description",
        "type",
        "properties",
        "required",
        "additionalProperties",
        "items",
        "minItems",
        "maxItems",
        "minimum",
        "maximum",
        "enum",
        "const",
        "format",
        "pattern",
    }
    ignored_top_level_keywords = sorted(set(schema) - standard_keywords)
    result = {
        "validator_scope": (
            "Local standards-semantics evaluator for every assertion keyword used by the embedded schema: "
            "type, properties, required, items, minItems, maxItems, minimum, maximum."
        ),
        "embedded_schema_top_level_keys": sorted(schema),
        "required_properties_exist": sorted(required) == sorted(set(required) & set(properties)),
        "required_count": len(required),
        "property_count": len(properties),
        "missing_type_object": schema.get("type") != "object",
        "missing_schema_dialect": "$schema" not in schema,
        "additional_properties_open": schema.get("additionalProperties", True) is not False,
        "ignored_top_level_keywords": ignored_top_level_keywords,
        "hash_or_attractor_properties": sorted(
            key for key in properties if "hash" in key or "attractor" in key
        ),
        "source_or_context_properties": sorted(
            key
            for key in properties
            if any(token in key for token in ("source", "context", "history", "interaction"))
        ),
        "scalar_instance": {"instance": 7, "errors": scalar_errors, "valid": not scalar_errors},
        "conforming_tube_errors": validate_schema_subset(conforming_tube, schema),
        "semantically_bad_but_schema_valid": {
            "instance": semantically_bad_but_schema_valid,
            "errors": semantically_bad_errors,
            "valid": not semantically_bad_errors,
        },
        "negative_constraint_results": negative_results,
        "enforced_constraints": {
            "required": bool(negative_results["missing_required"]),
            "phase_state_exactly_eight": bool(negative_results["seven_phase_values"]),
            "coherence_maximum": bool(negative_results["coherence_above_one"]),
        },
        "verdict": "PARTIAL_SHAPE_ONLY_NOT_OPERATIONAL",
    }
    return result, conforming_tube


def unit_checks(config: dict[str, Any]) -> dict[str, Any]:
    core = config["theoretical_parameters_db"]["kuramoto_core"]
    coupling = core["coupling_strength_K"]
    noise = core["intrinsic_noise_floor_D"]
    dispersion = core["frequency_dispersion_gamma"]
    critical = 2.0 * (dispersion + noise)
    proposed_r = math.sqrt(coupling - critical)
    return {
        "inputs": {
            "K": coupling,
            "D": noise,
            "gamma": dispersion,
            "declared_Kc_formula": core["critical_synchronization_threshold_Kc"],
            "declared_r_formula": core["order_parameter_resolution"],
        },
        "computed": {"Kc": critical, "sqrt_K_minus_Kc": proposed_r},
        "checks": [
            {
                "id": "numeric_Kc",
                "status": "PASS_ARITHMETIC_ONLY",
                "evidence": f"2 * ({dispersion} + {noise}) = {critical}",
            },
            {
                "id": "r_range",
                "status": "FAIL",
                "evidence": f"sqrt({coupling} - {critical}) = {proposed_r:.15f} > schema maximum 1.0",
            },
            {
                "id": "r_dimensions",
                "status": "FAIL_UNLESS_UNSTATED_NONDIMENSIONALIZATION",
                "evidence": (
                    "If K and Kc carry frequency units, sqrt(K - Kc) carries sqrt(frequency), "
                    "while coherence_index_r is declared on the dimensionless interval [0, 1]."
                ),
            },
            {
                "id": "r_compared_to_Kc",
                "status": "FAIL_UNLESS_UNSTATED_NONDIMENSIONALIZATION",
                "evidence": (
                    "execution_loop_protocol compares coherence r to Kc, despite r being [0,1] "
                    "and Kc being derived from coupling/noise/frequency-dispersion parameters."
                ),
            },
            {
                "id": "hz_to_angular_frequency",
                "status": "UNDERSPECIFIED",
                "evidence": (
                    "target_frequency_hz values are assigned to omega_k in prose, but no "
                    "cycles/s to rad/s conversion (2*pi) or agent clock is defined."
                ),
            },
        ],
        "verdict": "DIMENSIONALLY_UNDERSPECIFIED_AND_NUMERICALLY_INCONSISTENT",
    }


def run_fresh_probe(input_name: str, output_stem: str, mode: str) -> dict[str, Any]:
    script = ROOT / "tools" / "T2_fresh_process_probe.py"
    argv = [sys.executable, "-I", str(script), "--mode", mode]
    input_path = RAW / input_name
    with input_path.open("rb") as input_stream:
        completed = subprocess.run(
            argv,
            stdin=input_stream,
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=False,
            env={"PATH": os.environ.get("PATH", "")},
        )
    write_text(f"{output_stem}_stdout.json", completed.stdout)
    write_text(f"{output_stem}_stderr.txt", completed.stderr)
    command = (
        f"{sys.executable} -I {script} --mode {mode} < {input_path}"
    )
    write_text(f"{output_stem}_command.txt", command + "\n")
    return {
        "command": command,
        "exit_code": completed.returncode,
        "stdout_file": f"raw/{output_stem}_stdout.json",
        "stderr_file": f"raw/{output_stem}_stderr.txt",
        "parsed_stdout": json.loads(completed.stdout),
    }


def main() -> int:
    source_bytes = SOURCE.read_bytes()
    claims_bytes = CLAIMS.read_bytes()
    source_sha256 = sha256_bytes(source_bytes)
    source_text = source_bytes.decode("utf-8")
    source_receipt = {
        "path": str(SOURCE),
        "bytes": len(source_bytes),
        "sha256": source_sha256,
        "expected_sha256": EXPECTED_SOURCE_SHA256,
        "fingerprint_matches": source_sha256 == EXPECTED_SOURCE_SHA256,
        "claims_path": str(CLAIMS),
        "claims_bytes": len(claims_bytes),
        "claims_sha256": sha256_bytes(claims_bytes),
    }
    write_json("T2_source_fingerprint.json", source_receipt)
    if not source_receipt["fingerprint_matches"]:
        raise RuntimeError("Source fingerprint changed; refusing to test a different draft")

    raw_block, extraction = extract_part3_block(source_text)
    write_text("T2_part3_raw_block.txt", raw_block)
    write_json("T2_extraction.json", extraction)

    parsed_raw, python_raw = strict_python_parse(raw_block)
    write_text(
        "T2_strict_python_unchanged.txt",
        json.dumps(python_raw, indent=2, sort_keys=True) + "\n",
    )
    if parsed_raw is not None:
        raise AssertionError("Expected unchanged Part 3 block to fail strict JSON parsing")

    jq_raw = run_command(["/usr/bin/jq", "-e", ".", str(RAW / "T2_part3_raw_block.txt")])
    write_text("T2_strict_jq_unchanged_stdout.txt", jq_raw["stdout"])
    write_text("T2_strict_jq_unchanged_stderr.txt", jq_raw["stderr"])

    unescaped, unescape_manifest = markdown_unescape_for_json(raw_block)
    write_text("T2_part3_markdown_unescaped.json", unescaped)
    write_json("T2_unescape_manifest.json", unescape_manifest)

    config, python_unescaped = strict_python_parse(unescaped)
    write_text(
        "T2_strict_python_unescaped.txt",
        json.dumps(python_unescaped, indent=2, sort_keys=True) + "\n",
    )
    if config is None:
        raise AssertionError(f"Minimal Markdown unescape did not parse: {python_unescaped}")

    jq_unescaped = run_command(
        ["/usr/bin/jq", "-e", ".", str(RAW / "T2_part3_markdown_unescaped.json")]
    )
    write_text("T2_strict_jq_unescaped_stdout.txt", jq_unescaped["stdout"])
    write_text("T2_strict_jq_unescaped_stderr.txt", jq_unescaped["stderr"])

    schema_result, conforming_tube = schema_checks(config)
    write_json("T2_schema_checks.json", schema_result)

    context_a = {
        "task": "hold publication",
        "critical_fact": "signing key revocation is still pending",
    }
    context_b = {
        "task": "publish package",
        "critical_fact": "signing key revocation is complete",
    }
    serialized_tube = json.dumps(conforming_tube, sort_keys=True, separators=(",", ":"))
    hash_counterexample = {
        "claim_ids": ["MOSM-C04", "MOSM-C05"],
        "schema_hash_fields": schema_result["hash_or_attractor_properties"],
        "schema_context_fields": schema_result["source_or_context_properties"],
        "context_a": context_a,
        "context_b": context_b,
        "contexts_are_distinct": context_a != context_b,
        "same_schema_valid_tube_for_both": conforming_tube,
        "tube_serialization_sha256": sha256_bytes(serialized_tube.encode("utf-8")),
        "indistinguishability_argument": (
            "The embedded schema permits this identical tube to be associated with either distinct context. "
            "A fresh decoder receiving only the identical bytes has identical observations and cannot "
            "correctly choose both contexts."
        ),
        "hash_specification_missing": [
            "No attractor/hash field in identification_tube_schema",
            "No digest algorithm",
            "No canonical serialization for the five interactions",
            "No preimage/candidate corpus or retrieval relation",
        ],
        "verdict": "HASH_RECOVERY_NOT_OPERATIONALLY_SPECIFIED",
    }
    write_json("T2_hash_counterexample.json", hash_counterexample)

    unit_result = unit_checks(config)
    write_json("T2_unit_checks.json", unit_result)

    write_json("T2_fresh_process_input.json", conforming_tube)
    fresh_probe = run_fresh_probe(
        "T2_fresh_process_input.json", "T2_fresh_process", "tube-only"
    )

    interaction_bytes = json.dumps(
        ["interaction-1", "interaction-2", "interaction-3", "interaction-4", "secret-interaction-5"],
        separators=(",", ":"),
    ).encode("utf-8")
    hash_only_input = {
        "attractor_hash_sha256": sha256_bytes(interaction_bytes),
        "interaction_count_claimed": 5,
    }
    write_json("T2_hash_only_input.json", hash_only_input)
    hash_probe = run_fresh_probe("T2_hash_only_input.json", "T2_hash_only", "hash-only")

    results = {
        "source": source_receipt,
        "extraction": extraction,
        "unchanged_parse": {
            "python": python_raw,
            "jq": {
                "command": jq_raw["display_command"],
                "exit_code": jq_raw["exit_code"],
                "stderr": jq_raw["stderr"],
            },
            "verdict": "FAILS_STRICT_JSON",
        },
        "markdown_unescape": {
            "manifest_file": "raw/T2_unescape_manifest.json",
            "deletions": unescape_manifest["deletions"],
            "counts": unescape_manifest["counts_by_escaped_character"],
            "python": python_unescaped,
            "jq": {
                "command": jq_unescaped["display_command"],
                "exit_code": jq_unescaped["exit_code"],
                "stderr": jq_unescaped["stderr"],
            },
            "verdict": "PASSES_AFTER_DOCUMENTED_MARKDOWN_UNESCAPE",
        },
        "schema": schema_result,
        "hash_recoverability": hash_counterexample,
        "units": unit_result,
        "fresh_process": fresh_probe,
        "hash_only_process": hash_probe,
        "overall": {
            "part3_machine_readable_unchanged": False,
            "part3_machine_readable_after_documented_markdown_unescape": True,
            "identification_tube_operational_schema": False,
            "hash_recoverable_without_external_state": False,
            "dimensionally_and_numerically_consistent": False,
            "fresh_process_rehydrates_context_without_external_state": False,
        },
    }
    write_json("T2_results.json", results)

    transcript = "\n".join(
        [
            f"source_sha256={source_sha256}",
            f"raw_block_sha256={extraction['block_sha256']}",
            f"python_unchanged_exit=logical_parse_failure error={python_raw['message']}",
            f"jq_unchanged_exit={jq_raw['exit_code']} stderr={jq_raw['stderr'].strip()}",
            f"markdown_unescape_deletions={unescape_manifest['deletions']}",
            f"python_unescaped_ok={python_unescaped['ok']}",
            f"jq_unescaped_exit={jq_unescaped['exit_code']}",
            f"schema_verdict={schema_result['verdict']}",
            f"unit_verdict={unit_result['verdict']}",
            f"fresh_process_exit={fresh_probe['exit_code']} status={fresh_probe['parsed_stdout']['status']}",
            f"hash_only_exit={hash_probe['exit_code']} status={hash_probe['parsed_stdout']['status']}",
        ]
    ) + "\n"
    write_text("T2_run_transcript.txt", transcript)
    print(transcript, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
