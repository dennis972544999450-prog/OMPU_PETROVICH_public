from __future__ import annotations

import hashlib
import json
import os
import re
import tempfile
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from pathlib import Path

from .bundle import pack_bundle, unpack_bundle
from .crypto_cli import age_decrypt, age_encrypt, minisign_sign, minisign_verify
from .errors import BundleError, CryptoError, SatlinkError, SchemaError, StorageError
from .ledger import Acceptance, SatlinkLedger
from .model import SatlinkMessage, decode_message, encode_message, parse_timestamp

MAX_CIPHERTEXT_BYTES = 128 * 1024
_CARRIER = re.compile(r"^[a-z0-9][a-z0-9._:-]{0,63}$")


@dataclass(frozen=True)
class TrustEntry:
    sender: str
    signing_key_id: str
    minisign_public_key: Path
    status: str = "active"
    valid_from: str | None = None
    valid_until: str | None = None

    def active_at(self, when: datetime) -> bool:
        if self.status != "active":
            return False
        if self.valid_from and when < parse_timestamp(self.valid_from):
            return False
        if self.valid_until and when >= parse_timestamp(self.valid_until):
            return False
        return True


class TrustRegistry:
    def __init__(self, entries: list[TrustEntry]) -> None:
        self._entries = {(entry.sender, entry.signing_key_id): entry for entry in entries}
        if len(self._entries) != len(entries):
            raise ValueError("duplicate trust registry binding")

    def lookup(self, sender: str, signing_key_id: str, when: datetime) -> TrustEntry | None:
        entry = self._entries.get((sender, signing_key_id))
        return entry if entry is not None and entry.active_at(when) else None


@dataclass(frozen=True)
class GatewayResult:
    acceptance: Acceptance
    message: SatlinkMessage | None = None


def seal_message(message: SatlinkMessage, signing_secret_key: Path, age_recipient: str) -> bytes:
    message_bytes = encode_message(message)
    signature = minisign_sign(
        message_bytes,
        signing_secret_key,
        trusted_comment=f"SATLINK/0 {message.message_id} {message.signing_key_id}",
    )
    return age_encrypt(pack_bundle(message_bytes, signature), age_recipient)


class SatlinkGateway:
    def __init__(
        self,
        *,
        ledger: SatlinkLedger,
        registry: TrustRegistry,
        age_identity: Path,
        spool_dir: Path,
        expected_recipient: str = "ompu",
        allowed_route_targets: frozenset[str] = frozenset({"petrovich-codex"}),
        max_clock_skew: timedelta = timedelta(minutes=5),
    ) -> None:
        self.ledger = ledger
        self.registry = registry
        self.age_identity = age_identity
        self.spool_dir = spool_dir
        self.expected_recipient = expected_recipient
        self.allowed_route_targets = allowed_route_targets
        self.max_clock_skew = max_clock_skew
        self.spool_dir.mkdir(parents=True, exist_ok=True)
        os.chmod(self.spool_dir, 0o700)

    def _spool(self, ciphertext: bytes, ciphertext_sha256: str) -> Path:
        destination = self.spool_dir / f"{ciphertext_sha256}.age"
        if destination.exists():
            if hashlib.sha256(destination.read_bytes()).hexdigest() != ciphertext_sha256:
                raise CryptoError("opaque spool collision")
            return destination
        fd, raw_temp = tempfile.mkstemp(prefix=".incoming-", dir=self.spool_dir)
        temp_path = Path(raw_temp)
        try:
            os.fchmod(fd, 0o600)
            with os.fdopen(fd, "wb") as handle:
                handle.write(ciphertext)
                handle.flush()
                os.fsync(handle.fileno())
            os.link(temp_path, destination)
            os.chmod(destination, 0o600)
        except FileExistsError:
            pass
        except OSError as exc:
            raise StorageError("opaque spool write failed") from exc
        finally:
            temp_path.unlink(missing_ok=True)
        return destination

    def receive(
        self,
        ciphertext: bytes,
        *,
        carrier: str,
        origin_id: str,
        now: datetime | None = None,
    ) -> GatewayResult:
        now = (now or datetime.now(timezone.utc)).astimezone(timezone.utc)
        ciphertext_sha256 = hashlib.sha256(ciphertext).hexdigest()
        if not ciphertext or len(ciphertext) > MAX_CIPHERTEXT_BYTES:
            return GatewayResult(
                self.ledger.record_rejection(
                    code="CIPHERTEXT_SIZE_INVALID",
                    envelope_sha256=ciphertext_sha256,
                    now=now,
                )
            )
        if (
            not _CARRIER.fullmatch(carrier)
            or not 0 < len(origin_id.encode("utf-8")) <= 256
            or any(ord(character) < 32 for character in origin_id)
        ):
            return GatewayResult(
                self.ledger.record_rejection(
                    code="TRANSPORT_METADATA_INVALID",
                    envelope_sha256=ciphertext_sha256,
                    now=now,
                )
            )
        observation = self.ledger.observe_transport(
            carrier=carrier,
            origin_id=origin_id,
            ciphertext_sha256=ciphertext_sha256,
            now=now,
        )
        if observation.verdict == "rejected":
            return GatewayResult(
                self.ledger.record_rejection(
                    code=observation.code,
                    envelope_sha256=ciphertext_sha256,
                    now=now,
                )
            )
        try:
            self._spool(ciphertext, ciphertext_sha256)
            bundle_bytes = age_decrypt(ciphertext, self.age_identity)
            envelope_sha256 = hashlib.sha256(bundle_bytes).hexdigest()
            bundle = unpack_bundle(bundle_bytes)
            message = decode_message(bundle.message)
            trust = self.registry.lookup(message.sender, message.signing_key_id, now)
            if trust is None:
                return GatewayResult(
                    self.ledger.record_rejection(
                        code="UNKNOWN_OR_INACTIVE_SIGNING_KEY",
                        envelope_sha256=envelope_sha256,
                        message_id=message.message_id,
                        now=now,
                    )
                )
            try:
                minisign_verify(bundle.message, bundle.signature, trust.minisign_public_key)
            except CryptoError:
                return GatewayResult(
                    self.ledger.record_rejection(
                        code="SIGNATURE_INVALID",
                        envelope_sha256=envelope_sha256,
                        message_id=message.message_id,
                        now=now,
                    )
                )
            if message.recipient != self.expected_recipient:
                return GatewayResult(
                    self.ledger.record_rejection(
                        code="RECIPIENT_MISMATCH",
                        envelope_sha256=envelope_sha256,
                        message_id=message.message_id,
                        now=now,
                    )
                )
            if message.route_target_agent not in self.allowed_route_targets or message.hop_count != 0:
                return GatewayResult(
                    self.ledger.record_rejection(
                        code="ROUTE_NOT_ALLOWED",
                        envelope_sha256=envelope_sha256,
                        message_id=message.message_id,
                        now=now,
                    )
                )
            if message.issued_datetime > now + self.max_clock_skew:
                return GatewayResult(
                    self.ledger.record_rejection(
                        code="ISSUED_IN_FUTURE",
                        envelope_sha256=envelope_sha256,
                        message_id=message.message_id,
                        now=now,
                    )
                )
            if now >= message.expires_datetime:
                return GatewayResult(
                    self.ledger.record_rejection(
                        code="MESSAGE_EXPIRED",
                        envelope_sha256=envelope_sha256,
                        message_id=message.message_id,
                        now=now,
                    )
                )
            acceptance = self.ledger.accept(message, envelope_sha256=envelope_sha256, now=now)
            recoverable = acceptance.verdict == "accepted" or acceptance.code == "ENVELOPE_DUPLICATE"
            return GatewayResult(acceptance, message if recoverable else None)
        except StorageError:
            code = "STORAGE_FAILED"
        except CryptoError:
            code = "DECRYPT_OR_CRYPTO_FAILED"
        except BundleError:
            code = "BUNDLE_INVALID"
        except SchemaError:
            code = "SCHEMA_INVALID"
        except SatlinkError:
            code = "SATLINK_REJECTED"
        return GatewayResult(
            self.ledger.record_rejection(
                code=code,
                envelope_sha256=ciphertext_sha256,
                now=now,
            )
        )

    def project_shadow(
        self,
        result: GatewayResult,
        *,
        directory: Path,
        now: datetime | None = None,
    ) -> str:
        now = (now or datetime.now(timezone.utc)).astimezone(timezone.utc)
        message = result.message
        if (
            result.acceptance.verdict not in {"accepted", "duplicate"}
            or message is None
            or message.disclosure != "bus_ok"
        ):
            return "PROJECTION_NOT_ALLOWED"
        projection = {
            "authenticated_sender": message.sender,
            "body": message.text,
            "disclosure": message.disclosure,
            "envelope_sha256": result.acceptance.envelope_sha256,
            "from_agent": "satlink-gateway-v0",
            "hop_count": message.hop_count + 1,
            "intent": message.intent,
            "message_id": message.message_id,
            "recipient": message.recipient,
            "reply_to": message.reply_to,
            "sequence": message.sequence,
            "signing_key_id": message.signing_key_id,
            "thread_id": message.thread_id,
            "to_agent": message.route_target_agent,
        }
        raw = json.dumps(projection, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
        projection_sha256 = hashlib.sha256(raw).hexdigest()
        directory.mkdir(parents=True, exist_ok=True)
        os.chmod(directory, 0o700)
        destination = directory / f"{message.message_id}.json"
        try:
            with destination.open("xb") as handle:
                os.chmod(destination, 0o600)
                handle.write(raw)
                handle.flush()
                os.fsync(handle.fileno())
        except FileExistsError:
            existing = destination.read_bytes()
            if hashlib.sha256(existing).hexdigest() != projection_sha256:
                return "PROJECTION_COLLISION"
        return self.ledger.mark_projected(
            message_id=message.message_id,
            projection_sha256=projection_sha256,
            projection_ref=str(destination),
            now=now,
        )
