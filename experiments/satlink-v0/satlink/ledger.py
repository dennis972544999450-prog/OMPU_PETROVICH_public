from __future__ import annotations

import hashlib
import json
import sqlite3
from contextlib import contextmanager
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .model import SatlinkMessage


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


def iso_utc(value: datetime) -> str:
    return value.astimezone(timezone.utc).isoformat(timespec="microseconds").replace("+00:00", "Z")


@dataclass(frozen=True)
class TransportObservation:
    verdict: str
    code: str
    ciphertext_sha256: str


@dataclass(frozen=True)
class Acceptance:
    verdict: str
    code: str
    message_id: str | None
    envelope_sha256: str
    ordering: str | None = None
    gap_from: int | None = None
    gap_to: int | None = None
    disclosure: str | None = None


SCHEMA = """
CREATE TABLE IF NOT EXISTS transport_observations (
    observation_id TEXT PRIMARY KEY,
    carrier TEXT NOT NULL,
    origin_id TEXT NOT NULL,
    ciphertext_sha256 TEXT NOT NULL,
    first_seen_at TEXT NOT NULL,
    last_seen_at TEXT NOT NULL,
    seen_count INTEGER NOT NULL DEFAULT 1,
    UNIQUE(carrier, origin_id)
);

CREATE TABLE IF NOT EXISTS accepted_messages (
    envelope_sha256 TEXT PRIMARY KEY,
    message_id TEXT NOT NULL UNIQUE,
    sender TEXT NOT NULL,
    recipient TEXT NOT NULL,
    signing_key_id TEXT NOT NULL,
    intent TEXT NOT NULL,
    sequence INTEGER NOT NULL,
    issued_at TEXT NOT NULL,
    expires_at TEXT NOT NULL,
    disclosure TEXT NOT NULL,
    route_target_agent TEXT NOT NULL,
    hop_count INTEGER NOT NULL,
    ordering TEXT NOT NULL,
    gap_from INTEGER,
    gap_to INTEGER,
    accepted_at TEXT NOT NULL,
    state TEXT NOT NULL,
    UNIQUE(sender, signing_key_id, sequence)
);

CREATE TABLE IF NOT EXISTS projections (
    message_id TEXT PRIMARY KEY REFERENCES accepted_messages(message_id),
    projection_sha256 TEXT NOT NULL,
    projection_ref TEXT NOT NULL,
    projected_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS receipts (
    receipt_id INTEGER PRIMARY KEY AUTOINCREMENT,
    stage TEXT NOT NULL,
    verdict TEXT NOT NULL,
    code TEXT NOT NULL,
    envelope_sha256 TEXT,
    message_id TEXT,
    detail_json TEXT NOT NULL,
    created_at TEXT NOT NULL
);
"""


class SatlinkLedger:
    def __init__(self, path: Path) -> None:
        self.path = path
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self._initialize()

    def _connect(self) -> sqlite3.Connection:
        connection = sqlite3.connect(self.path, timeout=5.0, isolation_level=None)
        connection.row_factory = sqlite3.Row
        connection.execute("PRAGMA foreign_keys=ON")
        connection.execute("PRAGMA busy_timeout=5000")
        return connection

    @contextmanager
    def _connection(self):
        connection = self._connect()
        try:
            yield connection
        finally:
            connection.close()

    def _initialize(self) -> None:
        with self._connection() as connection:
            connection.execute("PRAGMA journal_mode=WAL")
            connection.execute("PRAGMA synchronous=FULL")
            connection.executescript(SCHEMA)

    @staticmethod
    def _receipt(
        connection: sqlite3.Connection,
        *,
        stage: str,
        verdict: str,
        code: str,
        now: datetime,
        envelope_sha256: str | None = None,
        message_id: str | None = None,
        detail: dict[str, Any] | None = None,
    ) -> None:
        connection.execute(
            """
            INSERT INTO receipts
                (stage, verdict, code, envelope_sha256, message_id, detail_json, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                stage,
                verdict,
                code,
                envelope_sha256,
                message_id,
                json.dumps(detail or {}, sort_keys=True, separators=(",", ":")),
                iso_utc(now),
            ),
        )

    def observe_transport(
        self,
        *,
        carrier: str,
        origin_id: str,
        ciphertext_sha256: str,
        now: datetime,
    ) -> TransportObservation:
        observation_id = hashlib.sha256(f"{carrier}\0{origin_id}".encode("utf-8")).hexdigest()
        with self._connection() as connection:
            connection.execute("BEGIN IMMEDIATE")
            row = connection.execute(
                "SELECT ciphertext_sha256 FROM transport_observations WHERE observation_id=?",
                (observation_id,),
            ).fetchone()
            if row is not None:
                if row["ciphertext_sha256"] != ciphertext_sha256:
                    self._receipt(
                        connection,
                        stage="transport",
                        verdict="rejected",
                        code="ORIGIN_ID_COLLISION",
                        envelope_sha256=ciphertext_sha256,
                        now=now,
                    )
                    connection.commit()
                    return TransportObservation("rejected", "ORIGIN_ID_COLLISION", ciphertext_sha256)
                connection.execute(
                    """
                    UPDATE transport_observations
                    SET seen_count=seen_count+1, last_seen_at=?
                    WHERE observation_id=?
                    """,
                    (iso_utc(now), observation_id),
                )
                self._receipt(
                    connection,
                    stage="transport",
                    verdict="duplicate",
                    code="TRANSPORT_DUPLICATE",
                    envelope_sha256=ciphertext_sha256,
                    now=now,
                )
                connection.commit()
                return TransportObservation("duplicate", "TRANSPORT_DUPLICATE", ciphertext_sha256)
            connection.execute(
                """
                INSERT INTO transport_observations
                    (observation_id, carrier, origin_id, ciphertext_sha256, first_seen_at, last_seen_at)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (observation_id, carrier, origin_id, ciphertext_sha256, iso_utc(now), iso_utc(now)),
            )
            self._receipt(
                connection,
                stage="transport",
                verdict="accepted",
                code="TRANSPORT_OBSERVED",
                envelope_sha256=ciphertext_sha256,
                now=now,
            )
            connection.commit()
            return TransportObservation("accepted", "TRANSPORT_OBSERVED", ciphertext_sha256)

    def record_rejection(
        self,
        *,
        code: str,
        envelope_sha256: str,
        now: datetime,
        message_id: str | None = None,
    ) -> Acceptance:
        with self._connection() as connection:
            connection.execute("BEGIN IMMEDIATE")
            self._receipt(
                connection,
                stage="gateway",
                verdict="rejected",
                code=code,
                envelope_sha256=envelope_sha256,
                message_id=message_id,
                now=now,
            )
            connection.commit()
        return Acceptance("rejected", code, message_id, envelope_sha256)

    def accept(
        self,
        message: SatlinkMessage,
        *,
        envelope_sha256: str,
        now: datetime,
    ) -> Acceptance:
        with self._connection() as connection:
            connection.execute("BEGIN IMMEDIATE")
            existing = connection.execute(
                "SELECT * FROM accepted_messages WHERE envelope_sha256=?",
                (envelope_sha256,),
            ).fetchone()
            if existing is not None:
                self._receipt(
                    connection,
                    stage="gateway",
                    verdict="duplicate",
                    code="ENVELOPE_DUPLICATE",
                    envelope_sha256=envelope_sha256,
                    message_id=existing["message_id"],
                    now=now,
                )
                connection.commit()
                return Acceptance(
                    "duplicate",
                    "ENVELOPE_DUPLICATE",
                    existing["message_id"],
                    envelope_sha256,
                    existing["ordering"],
                    existing["gap_from"],
                    existing["gap_to"],
                    existing["disclosure"],
                )

            message_collision = connection.execute(
                "SELECT envelope_sha256 FROM accepted_messages WHERE message_id=?",
                (message.message_id,),
            ).fetchone()
            if message_collision is not None:
                self._receipt(
                    connection,
                    stage="gateway",
                    verdict="rejected",
                    code="MESSAGE_ID_COLLISION",
                    envelope_sha256=envelope_sha256,
                    message_id=message.message_id,
                    now=now,
                )
                connection.commit()
                return Acceptance("rejected", "MESSAGE_ID_COLLISION", message.message_id, envelope_sha256)

            sequence_collision = connection.execute(
                """
                SELECT message_id FROM accepted_messages
                WHERE sender=? AND signing_key_id=? AND sequence=?
                """,
                (message.sender, message.signing_key_id, message.sequence),
            ).fetchone()
            if sequence_collision is not None:
                self._receipt(
                    connection,
                    stage="gateway",
                    verdict="rejected",
                    code="SEQUENCE_COLLISION",
                    envelope_sha256=envelope_sha256,
                    message_id=message.message_id,
                    now=now,
                )
                connection.commit()
                return Acceptance("rejected", "SEQUENCE_COLLISION", message.message_id, envelope_sha256)

            prior = connection.execute(
                """
                SELECT MAX(sequence) AS maximum FROM accepted_messages
                WHERE sender=? AND signing_key_id=?
                """,
                (message.sender, message.signing_key_id),
            ).fetchone()["maximum"]
            gap_from: int | None = None
            gap_to: int | None = None
            if prior is None:
                if message.sequence == 1:
                    ordering = "contiguous"
                else:
                    ordering = "gap"
                    gap_from, gap_to = 1, message.sequence - 1
            elif message.sequence == prior + 1:
                ordering = "contiguous"
            elif message.sequence > prior + 1:
                ordering = "gap"
                gap_from, gap_to = prior + 1, message.sequence - 1
            else:
                ordering = "late"

            state = "pending_projection" if message.disclosure == "bus_ok" else "held_private"
            connection.execute(
                """
                INSERT INTO accepted_messages
                    (envelope_sha256, message_id, sender, recipient, signing_key_id,
                     intent, sequence, issued_at, expires_at, disclosure,
                     route_target_agent, hop_count, ordering, gap_from, gap_to,
                     accepted_at, state)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    envelope_sha256,
                    message.message_id,
                    message.sender,
                    message.recipient,
                    message.signing_key_id,
                    message.intent,
                    message.sequence,
                    message.issued_at,
                    message.expires_at,
                    message.disclosure,
                    message.route_target_agent,
                    message.hop_count,
                    ordering,
                    gap_from,
                    gap_to,
                    iso_utc(now),
                    state,
                ),
            )
            code = "GATEWAY_ACCEPTED_GAP" if ordering == "gap" else "GATEWAY_ACCEPTED"
            self._receipt(
                connection,
                stage="gateway",
                verdict="accepted",
                code=code,
                envelope_sha256=envelope_sha256,
                message_id=message.message_id,
                detail={"ordering": ordering, "gap_from": gap_from, "gap_to": gap_to},
                now=now,
            )
            connection.commit()
            return Acceptance(
                "accepted",
                code,
                message.message_id,
                envelope_sha256,
                ordering,
                gap_from,
                gap_to,
                message.disclosure,
            )

    def mark_projected(
        self,
        *,
        message_id: str,
        projection_sha256: str,
        projection_ref: str,
        now: datetime,
    ) -> str:
        with self._connection() as connection:
            connection.execute("BEGIN IMMEDIATE")
            row = connection.execute(
                "SELECT projection_sha256, projection_ref FROM projections WHERE message_id=?",
                (message_id,),
            ).fetchone()
            if row is not None:
                if row["projection_sha256"] != projection_sha256:
                    self._receipt(
                        connection,
                        stage="projection",
                        verdict="rejected",
                        code="PROJECTION_COLLISION",
                        message_id=message_id,
                        now=now,
                    )
                    connection.commit()
                    return "PROJECTION_COLLISION"
                connection.commit()
                return "PROJECTION_DUPLICATE"
            accepted = connection.execute(
                "SELECT disclosure FROM accepted_messages WHERE message_id=?",
                (message_id,),
            ).fetchone()
            if accepted is None or accepted["disclosure"] != "bus_ok":
                self._receipt(
                    connection,
                    stage="projection",
                    verdict="rejected",
                    code="PROJECTION_NOT_ALLOWED",
                    message_id=message_id,
                    now=now,
                )
                connection.commit()
                return "PROJECTION_NOT_ALLOWED"
            connection.execute(
                """
                INSERT INTO projections
                    (message_id, projection_sha256, projection_ref, projected_at)
                VALUES (?, ?, ?, ?)
                """,
                (message_id, projection_sha256, projection_ref, iso_utc(now)),
            )
            connection.execute(
                "UPDATE accepted_messages SET state='projected' WHERE message_id=?",
                (message_id,),
            )
            self._receipt(
                connection,
                stage="projection",
                verdict="accepted",
                code="BUS_PROJECTED_SHADOW",
                message_id=message_id,
                detail={"projection_sha256": projection_sha256},
                now=now,
            )
            connection.commit()
            return "BUS_PROJECTED_SHADOW"

    def integrity_report(self) -> dict[str, Any]:
        with self._connection() as connection:
            integrity = connection.execute("PRAGMA integrity_check").fetchone()[0]
            foreign_keys = connection.execute("PRAGMA foreign_key_check").fetchall()
            counts = {
                table: connection.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]
                for table in ("transport_observations", "accepted_messages", "projections", "receipts")
            }
        return {"integrity": integrity, "foreign_key_errors": len(foreign_keys), "counts": counts}

    def public_receipts(self) -> list[dict[str, Any]]:
        with self._connection() as connection:
            rows = connection.execute(
                """
                SELECT stage, verdict, code, envelope_sha256, message_id, detail_json, created_at
                FROM receipts ORDER BY receipt_id
                """
            ).fetchall()
        return [
            {
                "stage": row["stage"],
                "verdict": row["verdict"],
                "code": row["code"],
                "envelope_sha256": row["envelope_sha256"],
                "message_id": row["message_id"],
                "detail": json.loads(row["detail_json"]),
                "created_at": row["created_at"],
            }
            for row in rows
        ]
