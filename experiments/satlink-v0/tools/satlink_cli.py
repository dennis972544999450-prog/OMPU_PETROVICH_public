#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import secrets
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from satlink.gateway import SatlinkGateway, TrustEntry, TrustRegistry, seal_message  # noqa: E402
from satlink.ledger import SatlinkLedger  # noqa: E402
from satlink.model import SatlinkMessage, decode_message, encode_message  # noqa: E402


def iso(value: datetime) -> str:
    return value.astimezone(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")


def write_exclusive(path: Path, data: bytes, mode: int = 0o600) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("xb") as handle:
        os.chmod(path, mode)
        handle.write(data)
        handle.flush()
        os.fsync(handle.fileno())


def compose(args: argparse.Namespace) -> int:
    issued = datetime.now(timezone.utc).replace(microsecond=0)
    body = args.body_file.read_text(encoding="utf-8")
    message = SatlinkMessage(
        message_id=args.message_id or "sl0_" + secrets.token_hex(16),
        sender=args.sender,
        recipient="ompu",
        thread_id=args.thread_id,
        sequence=args.sequence,
        issued_at=iso(issued),
        expires_at=iso(issued + timedelta(hours=args.ttl_hours)),
        signing_key_id=args.signing_key_id,
        intent=args.intent,
        disclosure=args.disclosure,
        route_target_agent="petrovich-codex",
        route_target_channel=None,
        hop_count=0,
        reply_to=args.reply_to,
        text=body,
    )
    write_exclusive(args.output, encode_message(message))
    print(json.dumps({"message_id": message.message_id, "output": str(args.output)}, sort_keys=True))
    return 0


def seal(args: argparse.Namespace) -> int:
    message = decode_message(args.message.read_bytes())
    ciphertext = seal_message(message, args.signing_secret_key, args.age_recipient)
    write_exclusive(args.output, ciphertext)
    print(json.dumps({"message_id": message.message_id, "output": str(args.output)}, sort_keys=True))
    return 0


def receive_shadow(args: argparse.Namespace) -> int:
    ledger = SatlinkLedger(args.ledger)
    registry = TrustRegistry(
        [TrustEntry(args.sender, args.signing_key_id, args.signing_public_key)]
    )
    gateway = SatlinkGateway(
        ledger=ledger,
        registry=registry,
        age_identity=args.age_identity,
        spool_dir=args.spool_dir,
    )
    result = gateway.receive(
        args.envelope.read_bytes(),
        carrier=args.carrier,
        origin_id=args.origin_id,
    )
    projection = None
    if args.shadow_dir is not None:
        projection = gateway.project_shadow(result, directory=args.shadow_dir)
    payload = {
        "code": result.acceptance.code,
        "disclosure": result.acceptance.disclosure,
        "envelope_sha256": result.acceptance.envelope_sha256,
        "gap_from": result.acceptance.gap_from,
        "gap_to": result.acceptance.gap_to,
        "message_id": result.acceptance.message_id,
        "ordering": result.acceptance.ordering,
        "projection": projection,
        "verdict": result.acceptance.verdict,
    }
    print(json.dumps(payload, sort_keys=True))
    return 0 if result.acceptance.verdict in {"accepted", "duplicate"} else 4


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Offline-only SATLINK/0 fixture CLI")
    sub = parser.add_subparsers(dest="command", required=True)

    compose_parser = sub.add_parser("compose", help="create strict plaintext message bytes")
    compose_parser.add_argument("--body-file", type=Path, required=True)
    compose_parser.add_argument("--output", type=Path, required=True)
    compose_parser.add_argument("--sequence", type=int, required=True)
    compose_parser.add_argument("--signing-key-id", required=True)
    compose_parser.add_argument("--sender", default="sputnik")
    compose_parser.add_argument("--thread-id", default="thread_sputnik_petrovich")
    compose_parser.add_argument("--intent", choices=["message", "request", "heartbeat", "refusal", "exit_only"], default="message")
    compose_parser.add_argument("--disclosure", choices=["bus_ok", "petrovich_only"], default="petrovich_only")
    compose_parser.add_argument("--ttl-hours", type=int, choices=range(1, 73), default=24, metavar="1..72")
    compose_parser.add_argument("--message-id")
    compose_parser.add_argument("--reply-to")
    compose_parser.set_defaults(func=compose)

    seal_parser = sub.add_parser("seal", help="minisign then age-encrypt a message")
    seal_parser.add_argument("--message", type=Path, required=True)
    seal_parser.add_argument("--signing-secret-key", type=Path, required=True)
    seal_parser.add_argument("--age-recipient", required=True)
    seal_parser.add_argument("--output", type=Path, required=True)
    seal_parser.set_defaults(func=seal)

    receive_parser = sub.add_parser("receive-shadow", help="verify into a shadow ledger, never the live bus")
    receive_parser.add_argument("--envelope", type=Path, required=True)
    receive_parser.add_argument("--age-identity", type=Path, required=True)
    receive_parser.add_argument("--sender", default="sputnik")
    receive_parser.add_argument("--signing-key-id", required=True)
    receive_parser.add_argument("--signing-public-key", type=Path, required=True)
    receive_parser.add_argument("--carrier", default="fixture")
    receive_parser.add_argument("--origin-id", required=True)
    receive_parser.add_argument("--ledger", type=Path, required=True)
    receive_parser.add_argument("--spool-dir", type=Path, required=True)
    receive_parser.add_argument("--shadow-dir", type=Path)
    receive_parser.set_defaults(func=receive_shadow)

    return parser


def main() -> int:
    args = build_parser().parse_args()
    return int(args.func(args))


if __name__ == "__main__":
    raise SystemExit(main())
