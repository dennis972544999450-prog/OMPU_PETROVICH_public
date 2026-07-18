from __future__ import annotations

import struct
from dataclasses import dataclass

from .errors import BundleError
from .model import MAX_MESSAGE_BYTES

MAGIC = b"SATLINK-BUNDLE/0\n"
MAX_SIGNATURE_BYTES = 8 * 1024
_LENGTHS = struct.Struct(">II")


@dataclass(frozen=True)
class SignedBundle:
    message: bytes
    signature: bytes


def pack_bundle(message: bytes, signature: bytes) -> bytes:
    if not message or len(message) > MAX_MESSAGE_BYTES:
        raise BundleError("invalid message length")
    if not signature or len(signature) > MAX_SIGNATURE_BYTES:
        raise BundleError("invalid signature length")
    return MAGIC + _LENGTHS.pack(len(message), len(signature)) + message + signature


def unpack_bundle(raw: bytes) -> SignedBundle:
    header_size = len(MAGIC) + _LENGTHS.size
    if len(raw) < header_size or not raw.startswith(MAGIC):
        raise BundleError("invalid SATLINK/0 bundle header")
    message_length, signature_length = _LENGTHS.unpack(raw[len(MAGIC) : header_size])
    if not 0 < message_length <= MAX_MESSAGE_BYTES:
        raise BundleError("invalid bundled message length")
    if not 0 < signature_length <= MAX_SIGNATURE_BYTES:
        raise BundleError("invalid bundled signature length")
    expected = header_size + message_length + signature_length
    if len(raw) != expected:
        raise BundleError("bundle length mismatch or trailing bytes")
    message_end = header_size + message_length
    return SignedBundle(raw[header_size:message_end], raw[message_end:expected])
