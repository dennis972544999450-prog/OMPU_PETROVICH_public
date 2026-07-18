from __future__ import annotations

import hashlib
import json
import os
import tempfile
import unittest
from datetime import timedelta
from pathlib import Path
from unittest.mock import patch

from satlink.bundle import pack_bundle, unpack_bundle
from satlink.crypto_cli import (
    Toolchain,
    age_decrypt,
    age_encrypt,
    generate_test_keyset,
)
from satlink.gateway import SatlinkGateway, TrustEntry, TrustRegistry, seal_message
from satlink.errors import StorageError
from satlink.ledger import SatlinkLedger
from satlink.model import encode_message

from tests.common import FIXED_NOW, message_for


class GatewayAdversarialTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.tools = Toolchain.discover()
        cls.key_temp = tempfile.TemporaryDirectory(prefix="satlink-test-keys-")
        os.environ["SATLINK_TEST_ONLY"] = "1"
        cls.public_key, cls.secret_key, cls.age_identity, cls.age_recipient = generate_test_keyset(
            Path(cls.key_temp.name) / "TEST_ONLY_KEYSET",
            tools=cls.tools,
        )

    @classmethod
    def tearDownClass(cls) -> None:
        cls.key_temp.cleanup()
        os.environ.pop("SATLINK_TEST_ONLY", None)

    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory(prefix="satlink-gateway-test-")
        root = Path(self.temp.name)
        self.ledger = SatlinkLedger(root / "ledger.sqlite3")
        registry = TrustRegistry(
            [TrustEntry("sputnik", "sputnik-test-sign-1", self.public_key)]
        )
        self.gateway = SatlinkGateway(
            ledger=self.ledger,
            registry=registry,
            age_identity=self.age_identity,
            spool_dir=root / "opaque-spool",
        )
        self.shadow = root / "shadow"

    def tearDown(self) -> None:
        self.temp.cleanup()

    def seal(self, sequence: int, **kwargs: object) -> bytes:
        return seal_message(message_for(sequence, **kwargs), self.secret_key, self.age_recipient)

    def test_round_trip_two_receipt_boundary_and_idempotent_projection(self) -> None:
        ciphertext = self.seal(1, text="hello; not a secret fixture")
        result = self.gateway.receive(
            ciphertext,
            carrier="fixture",
            origin_id="origin-1",
            now=FIXED_NOW,
        )
        self.assertEqual(result.acceptance.verdict, "accepted")
        self.assertEqual(result.acceptance.code, "GATEWAY_ACCEPTED")
        self.assertEqual(self.gateway.project_shadow(result, directory=self.shadow, now=FIXED_NOW), "BUS_PROJECTED_SHADOW")
        self.assertEqual(
            self.gateway.project_shadow(result, directory=self.shadow, now=FIXED_NOW + timedelta(minutes=10)),
            "PROJECTION_DUPLICATE",
        )
        projection = json.loads((self.shadow / f"{result.message.message_id}.json").read_text())  # type: ignore[union-attr]
        self.assertEqual(projection["from_agent"], "satlink-gateway-v0")
        self.assertEqual(projection["authenticated_sender"], "sputnik")
        self.assertEqual(projection["to_agent"], "petrovich-codex")
        self.assertEqual(projection["hop_count"], 1)

    def test_replay_across_carriers_is_not_delivered_twice(self) -> None:
        ciphertext = self.seal(1)
        first = self.gateway.receive(ciphertext, carrier="nats", origin_id="nats-1", now=FIXED_NOW)
        second = self.gateway.receive(ciphertext, carrier="kurilka", origin_id="kurilka-1", now=FIXED_NOW)
        self.assertEqual(first.acceptance.verdict, "accepted")
        self.assertEqual(second.acceptance.code, "ENVELOPE_DUPLICATE")

    def test_exact_duplicate_can_finish_projection_after_accept_crash(self) -> None:
        ciphertext = self.seal(1)
        accepted = self.gateway.receive(
            ciphertext,
            carrier="nats",
            origin_id="before-crash",
            now=FIXED_NOW,
        )
        self.assertEqual(accepted.acceptance.verdict, "accepted")
        # Simulate a crash before project_shadow. Re-ingest through another
        # carrier must finish, but a third attempt must remain idempotent.
        recovered = self.gateway.receive(
            ciphertext,
            carrier="fallback",
            origin_id="after-crash",
            now=FIXED_NOW + timedelta(minutes=1),
        )
        self.assertEqual(recovered.acceptance.code, "ENVELOPE_DUPLICATE")
        self.assertEqual(
            self.gateway.project_shadow(recovered, directory=self.shadow, now=FIXED_NOW + timedelta(minutes=1)),
            "BUS_PROJECTED_SHADOW",
        )
        self.assertEqual(
            self.gateway.project_shadow(recovered, directory=self.shadow, now=FIXED_NOW + timedelta(minutes=2)),
            "PROJECTION_DUPLICATE",
        )

    def test_reencrypted_replay_is_logically_duplicate(self) -> None:
        message = message_for(1)
        first = seal_message(message, self.secret_key, self.age_recipient)
        second = seal_message(message, self.secret_key, self.age_recipient)
        self.assertNotEqual(hashlib.sha256(first).digest(), hashlib.sha256(second).digest())
        accepted = self.gateway.receive(first, carrier="one", origin_id="1", now=FIXED_NOW)
        duplicate = self.gateway.receive(second, carrier="two", origin_id="2", now=FIXED_NOW)
        self.assertEqual(accepted.acceptance.verdict, "accepted")
        self.assertEqual(duplicate.acceptance.code, "ENVELOPE_DUPLICATE")

    def test_origin_id_collision_fails_closed(self) -> None:
        first = self.gateway.receive(self.seal(1), carrier="fixture", origin_id="same", now=FIXED_NOW)
        second = self.gateway.receive(self.seal(2), carrier="fixture", origin_id="same", now=FIXED_NOW)
        self.assertEqual(first.acceptance.verdict, "accepted")
        self.assertEqual(second.acceptance.code, "ORIGIN_ID_COLLISION")

    def test_ciphertext_tamper_fails_before_plaintext(self) -> None:
        ciphertext = bytearray(self.seal(1))
        ciphertext[len(ciphertext) // 2] ^= 1
        result = self.gateway.receive(bytes(ciphertext), carrier="fixture", origin_id="tampered", now=FIXED_NOW)
        self.assertEqual(result.acceptance.code, "DECRYPT_OR_CRYPTO_FAILED")
        self.assertIsNone(result.message)

    def test_size_and_transport_metadata_are_bounded_before_spooling(self) -> None:
        oversized = self.gateway.receive(
            b"x" * (128 * 1024 + 1),
            carrier="fixture",
            origin_id="too-large",
            now=FIXED_NOW,
        )
        bad_metadata = self.gateway.receive(
            self.seal(1),
            carrier="Fixture With Spaces",
            origin_id="bad\norigin",
            now=FIXED_NOW,
        )
        self.assertEqual(oversized.acceptance.code, "CIPHERTEXT_SIZE_INVALID")
        self.assertEqual(bad_metadata.acceptance.code, "TRANSPORT_METADATA_INVALID")
        self.assertEqual(list(self.gateway.spool_dir.glob("*.age")), [])

    def test_spool_failure_becomes_secret_free_rejection(self) -> None:
        with patch.object(self.gateway, "_spool", side_effect=StorageError("fixture disk failure")):
            result = self.gateway.receive(
                self.seal(1, text="must not leak through storage error"),
                carrier="fixture",
                origin_id="disk-failure",
                now=FIXED_NOW,
            )
        self.assertEqual(result.acceptance.code, "STORAGE_FAILED")
        self.assertNotIn("must not leak", json.dumps(self.ledger.public_receipts()))

    def test_valid_age_ciphertext_with_tampered_signed_message_is_rejected(self) -> None:
        ciphertext = self.seal(1)
        bundle = unpack_bundle(age_decrypt(ciphertext, self.age_identity))
        altered = bundle.message.replace(b"hello from orbit", b"hello from attack")
        self.assertNotEqual(altered, bundle.message)
        forged = age_encrypt(pack_bundle(altered, bundle.signature), self.age_recipient)
        result = self.gateway.receive(forged, carrier="fixture", origin_id="forged", now=FIXED_NOW)
        self.assertEqual(result.acceptance.code, "SIGNATURE_INVALID")

    def test_unknown_key_and_disallowed_route_fail_closed(self) -> None:
        unknown = self.gateway.receive(
            self.seal(1, signing_key_id="sputnik-unknown-sign"),
            carrier="fixture",
            origin_id="unknown-key",
            now=FIXED_NOW,
        )
        route = self.gateway.receive(
            self.seal(2, route_target="den"),
            carrier="fixture",
            origin_id="bad-route",
            now=FIXED_NOW,
        )
        self.assertEqual(unknown.acceptance.code, "UNKNOWN_OR_INACTIVE_SIGNING_KEY")
        self.assertEqual(route.acceptance.code, "ROUTE_NOT_ALLOWED")

    def test_expiry_and_future_clock_are_enforced(self) -> None:
        expired = self.gateway.receive(
            self.seal(
                1,
                issued_at=FIXED_NOW - timedelta(hours=2),
                expires_at=FIXED_NOW,
            ),
            carrier="fixture",
            origin_id="expired",
            now=FIXED_NOW,
        )
        future = self.gateway.receive(
            self.seal(
                2,
                issued_at=FIXED_NOW + timedelta(minutes=6),
                expires_at=FIXED_NOW + timedelta(hours=1),
            ),
            carrier="fixture",
            origin_id="future",
            now=FIXED_NOW,
        )
        self.assertEqual(expired.acceptance.code, "MESSAGE_EXPIRED")
        self.assertEqual(future.acceptance.code, "ISSUED_IN_FUTURE")

    def test_out_of_order_is_accepted_with_gap_evidence(self) -> None:
        third = self.gateway.receive(self.seal(3), carrier="fixture", origin_id="3", now=FIXED_NOW)
        first = self.gateway.receive(self.seal(1), carrier="fixture", origin_id="1", now=FIXED_NOW)
        second = self.gateway.receive(self.seal(2), carrier="fixture", origin_id="2", now=FIXED_NOW)
        self.assertEqual((third.acceptance.ordering, third.acceptance.gap_from, third.acceptance.gap_to), ("gap", 1, 2))
        self.assertEqual(first.acceptance.ordering, "late")
        self.assertEqual(second.acceptance.ordering, "late")
        self.assertTrue(all(item.acceptance.verdict == "accepted" for item in (third, first, second)))

    def test_sequence_collision_is_rejected(self) -> None:
        first = self.gateway.receive(self.seal(1), carrier="fixture", origin_id="one", now=FIXED_NOW)
        collision = self.gateway.receive(
            self.seal(1, message_tag=999, text="different signed message"),
            carrier="fixture",
            origin_id="two",
            now=FIXED_NOW,
        )
        self.assertEqual(first.acceptance.verdict, "accepted")
        self.assertEqual(collision.acceptance.code, "SEQUENCE_COLLISION")

    def test_private_disclosure_never_projects(self) -> None:
        result = self.gateway.receive(
            self.seal(1, disclosure="petrovich_only"),
            carrier="fixture",
            origin_id="private",
            now=FIXED_NOW,
        )
        self.assertEqual(result.acceptance.verdict, "accepted")
        self.assertEqual(self.gateway.project_shadow(result, directory=self.shadow), "PROJECTION_NOT_ALLOWED")
        self.assertFalse(self.shadow.exists())

    def test_receipts_are_secret_free_and_database_is_healthy(self) -> None:
        secret_fixture = "DO_NOT_LEAK_THIS_TEST_PLAINTEXT"
        result = self.gateway.receive(
            self.seal(1, text=secret_fixture),
            carrier="fixture",
            origin_id="receipt",
            now=FIXED_NOW,
        )
        self.assertEqual(result.acceptance.verdict, "accepted")
        rendered = json.dumps(self.ledger.public_receipts(), sort_keys=True)
        self.assertNotIn(secret_fixture, rendered)
        self.assertNotIn("AGE-SECRET-KEY", rendered)
        report = self.ledger.integrity_report()
        self.assertEqual(report["integrity"], "ok")
        self.assertEqual(report["foreign_key_errors"], 0)


if __name__ == "__main__":
    unittest.main()
