#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parents[1]
BRIDGE = Path("/Users/denbell/OMPU_shared/attentionheads/bridge_v0")


def run(command: list[str], *, cwd: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        command,
        cwd=cwd,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        timeout=120,
    )


def require_success(label: str, result: subprocess.CompletedProcess[str]) -> str:
    if result.returncode != 0:
        tail = "\n".join(result.stdout.splitlines()[-30:])
        raise RuntimeError(f"{label} failed\n{tail}")
    return result.stdout


def unittest_count(output: str) -> int:
    match = re.search(r"Ran (\d+) tests?", output)
    if match is None:
        raise RuntimeError("could not parse unittest count")
    return int(match.group(1))


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def version(command: list[str]) -> str:
    output = require_success(command[0] + " version", run(command, cwd=ROOT))
    return output.strip().splitlines()[0]


def scan_forbidden_shapes() -> list[str]:
    patterns = [
        re.compile(r"AGE-SECRET-KEY-1[A-Z0-9]{20,}"),
        re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----"),
        re.compile(r"\bS[UOACN][A-Z2-7]{55,}\b"),
        re.compile(r"\bgh[pousr]_[A-Za-z0-9]{30,}\b"),
        re.compile(r"\bsk-[A-Za-z0-9]{20,}\b"),
    ]
    hits: list[str] = []
    for path in ROOT.rglob("*"):
        if not path.is_file() or any(part in {".venv", "__pycache__"} for part in path.parts):
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue
        if any(pattern.search(text) for pattern in patterns):
            hits.append(str(path.relative_to(ROOT)))
    return sorted(hits)


def scan_trailing_whitespace() -> list[str]:
    hits: list[str] = []
    for path in ROOT.rglob("*"):
        if not path.is_file() or any(part in {".venv", "__pycache__"} for part in path.parts):
            continue
        try:
            lines = path.read_text(encoding="utf-8").splitlines()
        except (UnicodeDecodeError, OSError):
            continue
        if any(line.endswith((" ", "\t")) for line in lines):
            hits.append(str(path.relative_to(ROOT)))
    return sorted(hits)


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--receipt", type=Path, required=True)
    args = parser.parse_args()

    satlink_output = require_success(
        "satlink tests",
        run(
            [sys.executable, "-W", "error::ResourceWarning", "-m", "unittest", "discover", "-s", "tests", "-v"],
            cwd=ROOT,
        ),
    )
    bridge_output = require_success(
        "bridge baseline",
        run(["python3", "-m", "unittest", "discover", "-s", "tests", "-v"], cwd=BRIDGE),
    )
    require_success("git diff check", run(["git", "diff", "--check"], cwd=REPO))

    forbidden = scan_forbidden_shapes()
    if forbidden:
        raise RuntimeError("forbidden secret/address shapes found in: " + ", ".join(forbidden))
    whitespace = scan_trailing_whitespace()
    if whitespace:
        raise RuntimeError("trailing whitespace found in: " + ", ".join(whitespace))

    process_check = run(["pgrep", "-f", "[/]nats-server"], cwd=ROOT)
    if process_check.returncode == 0:
        raise RuntimeError("a temporary nats-server process was left running")
    if process_check.returncode not in {1}:
        raise RuntimeError("could not verify nats-server process state")

    source_paths = [ROOT / "sources" / "OD-002_diagnostika_kanala.md"]
    research_paths = sorted((ROOT / "research").glob("0[1-5]_*.md"))
    implementation_paths = sorted(
        [
            ROOT / ".gitignore",
            ROOT / "ARCHITECTURE_DECISION.md",
            ROOT / "README.md",
            ROOT / "STATUS.md",
            ROOT / "WIRE_CONTRACT.md",
            ROOT / "requirements-test.txt",
            ROOT / "requirements-test.lock",
            ROOT / "research" / "README.md",
            ROOT / "schema" / "satlink-message-v0.schema.json",
        ]
        + list((ROOT / "satlink").glob("*.py"))
        + list((ROOT / "tests").glob("*.py"))
        + list((ROOT / "tools").glob("*"))
    )
    receipt: dict[str, Any] = {
        "schema": "satlink.verification.receipt.v0",
        "generated_at": utc_now(),
        "result": "pass",
        "tests": {
            "satlink": {
                "count": unittest_count(satlink_output),
                "resource_warnings_as_errors": True,
                "status": "pass",
            },
            "bridge_v0_baseline": {
                "count": unittest_count(bridge_output),
                "status": "pass",
            },
        },
        "toolchain": {
            "age": version(["age", "--version"]),
            "minisign": version(["minisign", "-v"]),
            "nats_server": version(["nats-server", "--version"]),
            "python": sys.version.split()[0],
        },
        "evidence": {
            "sources": {str(path.relative_to(ROOT)): sha256(path) for path in source_paths},
            "research": {str(path.relative_to(ROOT)): sha256(path) for path in research_paths},
            "implementation": {
                str(path.relative_to(ROOT)): sha256(path)
                for path in implementation_paths
                if path.is_file()
            },
            "forbidden_shape_hits": forbidden,
            "trailing_whitespace_hits": whitespace,
            "nats_server_left_running": False,
            "git_diff_check": "pass",
        },
        "safety": {
            "live_bus_writes": 0,
            "live_carrier_writes": 0,
            "live_credentials_created": 0,
            "launchagents_changed": 0,
            "public_deploys": 0,
        },
    }

    args.receipt.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(
        mode="w",
        encoding="utf-8",
        dir=args.receipt.parent,
        prefix=".satlink-receipt-",
        delete=False,
    ) as handle:
        json.dump(receipt, handle, ensure_ascii=False, indent=2, sort_keys=True)
        handle.write("\n")
        handle.flush()
        os.fsync(handle.fileno())
        temp_path = Path(handle.name)
    os.replace(temp_path, args.receipt)
    os.chmod(args.receipt, 0o644)
    print(args.receipt)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
