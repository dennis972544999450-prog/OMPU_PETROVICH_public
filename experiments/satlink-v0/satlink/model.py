from __future__ import annotations

import json
import re
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from typing import Any

from .errors import SchemaError

MAX_MESSAGE_BYTES = 64 * 1024
MAX_BODY_BYTES = 32 * 1024
MAX_TTL = timedelta(hours=72)

_MESSAGE_ID = re.compile(r"^sl0_[0-9a-f]{32}$")
_HANDLE = re.compile(r"^[a-z][a-z0-9-]{0,63}$")
_KEY_ID = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._:-]{0,127}$")
_THREAD_ID = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._:-]{0,127}$")
_TIMESTAMP = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d{1,6})?Z$")

_TOP_LEVEL_FIELDS = {
    "version",
    "kind",
    "message_id",
    "sender",
    "recipient",
    "thread_id",
    "sequence",
    "issued_at",
    "expires_at",
    "signing_key_id",
    "intent",
    "disclosure",
    "route",
    "hop_count",
    "reply_to",
    "body",
}
_BODY_FIELDS = {"media_type", "text"}
_ROUTE_FIELDS = {"target_agent", "target_channel", "hop_limit"}


def _reject_duplicate_keys(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise SchemaError(f"duplicate JSON key: {key}")
        result[key] = value
    return result


def parse_timestamp(value: str) -> datetime:
    if not isinstance(value, str) or not _TIMESTAMP.fullmatch(value):
        raise SchemaError("timestamps must be RFC3339 UTC values ending in Z")
    try:
        parsed = datetime.fromisoformat(value[:-1] + "+00:00")
    except ValueError as exc:
        raise SchemaError("invalid RFC3339 timestamp") from exc
    if parsed.tzinfo is None or parsed.utcoffset() != timedelta(0):
        raise SchemaError("timestamps must be UTC")
    return parsed.astimezone(timezone.utc)


@dataclass(frozen=True)
class SatlinkMessage:
    message_id: str
    sender: str
    recipient: str
    thread_id: str
    sequence: int
    issued_at: str
    expires_at: str
    signing_key_id: str
    intent: str
    disclosure: str
    route_target_agent: str
    route_target_channel: str | None
    hop_count: int
    reply_to: str | None
    text: str

    @property
    def issued_datetime(self) -> datetime:
        return parse_timestamp(self.issued_at)

    @property
    def expires_datetime(self) -> datetime:
        return parse_timestamp(self.expires_at)

    def to_mapping(self) -> dict[str, Any]:
        return {
            "body": {
                "media_type": "text/plain; charset=utf-8",
                "text": self.text,
            },
            "disclosure": self.disclosure,
            "expires_at": self.expires_at,
            "hop_count": self.hop_count,
            "intent": self.intent,
            "issued_at": self.issued_at,
            "kind": "satlink.message.v0",
            "message_id": self.message_id,
            "recipient": self.recipient,
            "reply_to": self.reply_to,
            "route": {
                "hop_limit": 1,
                "target_agent": self.route_target_agent,
                "target_channel": self.route_target_channel,
            },
            "sender": self.sender,
            "sequence": self.sequence,
            "signing_key_id": self.signing_key_id,
            "thread_id": self.thread_id,
            "version": 0,
        }


def _validate_mapping(value: Any) -> SatlinkMessage:
    if not isinstance(value, dict) or set(value) != _TOP_LEVEL_FIELDS:
        raise SchemaError("message fields do not match SATLINK/0 schema")
    if value["version"] != 0 or value["kind"] != "satlink.message.v0":
        raise SchemaError("unsupported protocol version or message kind")
    if not isinstance(value["message_id"], str) or not _MESSAGE_ID.fullmatch(value["message_id"]):
        raise SchemaError("invalid message_id")
    for field in ("sender", "recipient"):
        if not isinstance(value[field], str) or not _HANDLE.fullmatch(value[field]):
            raise SchemaError(f"invalid {field}")
    if not isinstance(value["thread_id"], str) or not _THREAD_ID.fullmatch(value["thread_id"]):
        raise SchemaError("invalid thread_id")
    sequence = value["sequence"]
    if isinstance(sequence, bool) or not isinstance(sequence, int) or not 1 <= sequence < 2**63:
        raise SchemaError("sequence must be a positive signed 64-bit integer")
    if not isinstance(value["signing_key_id"], str) or not _KEY_ID.fullmatch(value["signing_key_id"]):
        raise SchemaError("invalid signing_key_id")
    if value["intent"] not in {"message", "request", "heartbeat", "refusal", "exit_only"}:
        raise SchemaError("invalid intent")
    if value["disclosure"] not in {"bus_ok", "petrovich_only"}:
        raise SchemaError("invalid disclosure policy")
    route = value["route"]
    if not isinstance(route, dict) or set(route) != _ROUTE_FIELDS:
        raise SchemaError("invalid route fields")
    if not isinstance(route["target_agent"], str) or not _HANDLE.fullmatch(route["target_agent"]):
        raise SchemaError("invalid route target_agent")
    if route["target_channel"] is not None:
        raise SchemaError("target_channel is reserved and must be null in v0")
    if route["hop_limit"] != 1:
        raise SchemaError("v0 hop_limit must equal one")
    hop_count = value["hop_count"]
    if isinstance(hop_count, bool) or hop_count != 0:
        raise SchemaError("new v0 envelopes must have hop_count zero")
    reply_to = value["reply_to"]
    if reply_to is not None and (not isinstance(reply_to, str) or not _MESSAGE_ID.fullmatch(reply_to)):
        raise SchemaError("invalid reply_to")
    body = value["body"]
    if not isinstance(body, dict) or set(body) != _BODY_FIELDS:
        raise SchemaError("invalid body fields")
    if body["media_type"] != "text/plain; charset=utf-8" or not isinstance(body["text"], str):
        raise SchemaError("unsupported body media type or value")
    if (
        any(ord(character) < 32 and character not in "\n\r\t" for character in body["text"])
        or len(body["text"].encode("utf-8")) > MAX_BODY_BYTES
    ):
        raise SchemaError("body is unsafe or too large")

    issued_at = parse_timestamp(value["issued_at"])
    expires_at = parse_timestamp(value["expires_at"])
    if expires_at <= issued_at or expires_at - issued_at > MAX_TTL:
        raise SchemaError("expiry must be after issue time and within 72 hours")

    return SatlinkMessage(
        message_id=value["message_id"],
        sender=value["sender"],
        recipient=value["recipient"],
        thread_id=value["thread_id"],
        sequence=sequence,
        issued_at=value["issued_at"],
        expires_at=value["expires_at"],
        signing_key_id=value["signing_key_id"],
        intent=value["intent"],
        disclosure=value["disclosure"],
        route_target_agent=route["target_agent"],
        route_target_channel=route["target_channel"],
        hop_count=hop_count,
        reply_to=reply_to,
        text=body["text"],
    )


def encode_message(message: SatlinkMessage) -> bytes:
    _validate_mapping(message.to_mapping())
    raw = json.dumps(
        message.to_mapping(),
        ensure_ascii=False,
        separators=(",", ":"),
        sort_keys=True,
    ).encode("utf-8")
    if len(raw) > MAX_MESSAGE_BYTES:
        raise SchemaError("message exceeds SATLINK/0 byte limit")
    return raw


def decode_message(raw: bytes) -> SatlinkMessage:
    if not isinstance(raw, bytes) or not raw or len(raw) > MAX_MESSAGE_BYTES:
        raise SchemaError("message is empty or too large")
    try:
        value = json.loads(raw.decode("utf-8"), object_pairs_hook=_reject_duplicate_keys)
    except UnicodeDecodeError as exc:
        raise SchemaError("message is not valid UTF-8") from exc
    except (json.JSONDecodeError, ValueError) as exc:
        raise SchemaError("message is not valid JSON") from exc
    except RecursionError as exc:
        raise SchemaError("message JSON nesting is too deep") from exc
    return _validate_mapping(value)
