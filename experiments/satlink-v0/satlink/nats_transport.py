from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class PersistedReceipt:
    stage: str
    stream: str
    sequence: int
    duplicate: bool
    message_id: str


async def ensure_test_stream(js: Any, *, stream: str, subject: str) -> None:
    """Create a localhost test stream. This is not production provisioning."""

    from nats.js.api import StorageType, StreamConfig
    from nats.js.errors import NotFoundError

    try:
        await js.stream_info(stream)
    except NotFoundError:
        await js.add_stream(
            config=StreamConfig(
                name=stream,
                subjects=[subject],
                storage=StorageType.FILE,
                max_age=72 * 60 * 60,
                max_msg_size=128 * 1024,
                duplicate_window=2 * 60,
            )
        )


async def publish_persisted(
    js: Any,
    *,
    stream: str,
    subject: str,
    payload: bytes,
    message_id: str,
) -> PersistedReceipt:
    ack = await js.publish(subject, payload, headers={"Nats-Msg-Id": message_id})
    if ack.stream != stream:
        raise RuntimeError("JetStream acknowledged an unexpected stream")
    return PersistedReceipt(
        stage="transport_persisted",
        stream=ack.stream,
        sequence=ack.seq,
        duplicate=bool(ack.duplicate),
        message_id=message_id,
    )
