from __future__ import annotations

import json
import unittest
from dataclasses import replace
from pathlib import Path

from satlink.bundle import pack_bundle, unpack_bundle
from satlink.errors import BundleError, SchemaError
from satlink.model import _BODY_FIELDS, _ROUTE_FIELDS, _TOP_LEVEL_FIELDS, decode_message, encode_message

from tests.common import message_for


class MessageAndBundleTests(unittest.TestCase):
    def test_canonical_message_round_trip_preserves_unicode(self) -> None:
        message = message_for(1, text="тихий сигнал с орбиты")
        raw = encode_message(message)
        self.assertEqual(encode_message(decode_message(raw)), raw)
        self.assertIn("тихий".encode("utf-8"), raw)

    def test_duplicate_json_key_is_rejected(self) -> None:
        raw = encode_message(message_for(1))
        value = json.loads(raw)
        body = json.dumps(value, ensure_ascii=False, separators=(",", ":"))
        malformed = body[:-1] + ',"version":0}'
        with self.assertRaises(SchemaError):
            decode_message(malformed.encode("utf-8"))

    def test_deep_json_nesting_fails_as_schema_error(self) -> None:
        nested = ("[" * 2000 + "0" + "]" * 2000).encode("ascii")
        with self.assertRaises(SchemaError):
            decode_message(nested)

    def test_oversized_integer_fails_as_schema_error(self) -> None:
        with self.assertRaises(SchemaError):
            decode_message(("{" + '"sequence":' + "9" * 5000 + "}").encode("ascii"))

    def test_route_and_hop_are_strict(self) -> None:
        value = json.loads(encode_message(message_for(1)))
        value["hop_count"] = 1
        with self.assertRaises(SchemaError):
            decode_message(json.dumps(value).encode("utf-8"))
        value["hop_count"] = 0
        value["route"]["hop_limit"] = 2
        with self.assertRaises(SchemaError):
            decode_message(json.dumps(value).encode("utf-8"))

    def test_encoder_cannot_bypass_schema_and_timestamps_are_strict(self) -> None:
        with self.assertRaises(SchemaError):
            encode_message(replace(message_for(1), sequence=0))
        with self.assertRaises(SchemaError):
            encode_message(replace(message_for(1), issued_at="2026-07-18Z"))
        with self.assertRaises(SchemaError):
            encode_message(replace(message_for(1), text="bad\x1bcontrol"))

    def test_bundle_rejects_trailing_bytes(self) -> None:
        raw = pack_bundle(b"{}", b"signature")
        self.assertEqual(unpack_bundle(raw).message, b"{}")
        with self.assertRaises(BundleError):
            unpack_bundle(raw + b"x")

    def test_json_schema_field_sets_match_strict_parser(self) -> None:
        schema_path = Path(__file__).parents[1] / "schema" / "satlink-message-v0.schema.json"
        schema = json.loads(schema_path.read_text(encoding="utf-8"))
        self.assertFalse(schema["additionalProperties"])
        self.assertEqual(set(schema["required"]), _TOP_LEVEL_FIELDS)
        self.assertEqual(set(schema["properties"]), _TOP_LEVEL_FIELDS)
        self.assertEqual(set(schema["properties"]["body"]["required"]), _BODY_FIELDS)
        self.assertEqual(set(schema["properties"]["route"]["required"]), _ROUTE_FIELDS)


if __name__ == "__main__":
    unittest.main()
