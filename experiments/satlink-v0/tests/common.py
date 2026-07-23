from __future__ import annotations

from datetime import datetime, timedelta, timezone

from satlink.model import SatlinkMessage

FIXED_NOW = datetime(2026, 7, 18, 12, 30, tzinfo=timezone.utc)


def iso(value: datetime) -> str:
    return value.isoformat(timespec="seconds").replace("+00:00", "Z")


def message_for(
    sequence: int,
    *,
    message_tag: int | None = None,
    sender: str = "sputnik",
    recipient: str = "ompu",
    signing_key_id: str = "sputnik-test-sign-1",
    disclosure: str = "bus_ok",
    route_target: str = "petrovich-codex",
    intent: str = "message",
    issued_at: datetime | None = None,
    expires_at: datetime | None = None,
    text: str = "test payload: hello from orbit",
) -> SatlinkMessage:
    issued_at = issued_at or (FIXED_NOW - timedelta(minutes=30))
    expires_at = expires_at or (FIXED_NOW + timedelta(hours=1))
    tag = message_tag if message_tag is not None else sequence
    return SatlinkMessage(
        message_id=f"sl0_{tag:032x}",
        sender=sender,
        recipient=recipient,
        thread_id="thread_satlink_test",
        sequence=sequence,
        issued_at=iso(issued_at),
        expires_at=iso(expires_at),
        signing_key_id=signing_key_id,
        intent=intent,
        disclosure=disclosure,
        route_target_agent=route_target,
        route_target_channel=None,
        hop_count=0,
        reply_to=None,
        text=text,
    )
