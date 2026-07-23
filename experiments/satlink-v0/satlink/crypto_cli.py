from __future__ import annotations

import os
import shutil
import subprocess
import tempfile
from dataclasses import dataclass
from pathlib import Path

from .errors import CryptoError


@dataclass(frozen=True)
class Toolchain:
    age: str
    age_keygen: str
    minisign: str

    @classmethod
    def discover(cls) -> "Toolchain":
        paths = {name: shutil.which(name) for name in ("age", "age-keygen", "minisign")}
        missing = [name for name, path in paths.items() if path is None]
        if missing:
            raise CryptoError("missing required crypto tools: " + ", ".join(missing))
        return cls(paths["age"], paths["age-keygen"], paths["minisign"])  # type: ignore[arg-type]


def _run(args: list[str], *, operation: str) -> subprocess.CompletedProcess[bytes]:
    try:
        return subprocess.run(
            args,
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=30,
        )
    except (OSError, subprocess.SubprocessError) as exc:
        # Tool output can contain paths or key material. Keep the receipt stable
        # and secret-free; callers can reproduce locally when debugging.
        raise CryptoError(f"{operation} failed") from exc


def minisign_sign(
    message: bytes,
    secret_key: Path,
    *,
    trusted_comment: str,
    tools: Toolchain | None = None,
) -> bytes:
    if "\n" in trusted_comment or len(trusted_comment.encode("utf-8")) > 160:
        raise CryptoError("invalid trusted comment")
    tools = tools or Toolchain.discover()
    with tempfile.TemporaryDirectory(prefix="satlink-sign-") as raw_dir:
        directory = Path(raw_dir)
        os.chmod(directory, 0o700)
        message_path = directory / "message.bin"
        signature_path = directory / "message.minisig"
        message_path.write_bytes(message)
        os.chmod(message_path, 0o600)
        _run(
            [
                tools.minisign,
                "-S",
                "-s",
                str(secret_key),
                "-m",
                str(message_path),
                "-x",
                str(signature_path),
                "-t",
                trusted_comment,
            ],
            operation="minisign signing",
        )
        return signature_path.read_bytes()


def minisign_verify(
    message: bytes,
    signature: bytes,
    public_key: Path,
    *,
    tools: Toolchain | None = None,
) -> None:
    tools = tools or Toolchain.discover()
    with tempfile.TemporaryDirectory(prefix="satlink-verify-") as raw_dir:
        directory = Path(raw_dir)
        os.chmod(directory, 0o700)
        message_path = directory / "message.bin"
        signature_path = directory / "message.minisig"
        message_path.write_bytes(message)
        signature_path.write_bytes(signature)
        os.chmod(message_path, 0o600)
        os.chmod(signature_path, 0o600)
        _run(
            [
                tools.minisign,
                "-V",
                "-q",
                "-p",
                str(public_key),
                "-m",
                str(message_path),
                "-x",
                str(signature_path),
            ],
            operation="minisign verification",
        )


def age_encrypt(plaintext: bytes, recipient: str, *, tools: Toolchain | None = None) -> bytes:
    if not recipient.startswith("age1") or any(ch.isspace() for ch in recipient):
        raise CryptoError("invalid age recipient")
    tools = tools or Toolchain.discover()
    with tempfile.TemporaryDirectory(prefix="satlink-encrypt-") as raw_dir:
        directory = Path(raw_dir)
        os.chmod(directory, 0o700)
        plain_path = directory / "bundle.bin"
        encrypted_path = directory / "bundle.age"
        plain_path.write_bytes(plaintext)
        os.chmod(plain_path, 0o600)
        _run(
            [tools.age, "-r", recipient, "-o", str(encrypted_path), str(plain_path)],
            operation="age encryption",
        )
        return encrypted_path.read_bytes()


def age_decrypt(ciphertext: bytes, identity: Path, *, tools: Toolchain | None = None) -> bytes:
    tools = tools or Toolchain.discover()
    with tempfile.TemporaryDirectory(prefix="satlink-decrypt-") as raw_dir:
        directory = Path(raw_dir)
        os.chmod(directory, 0o700)
        encrypted_path = directory / "bundle.age"
        plain_path = directory / "bundle.bin"
        encrypted_path.write_bytes(ciphertext)
        os.chmod(encrypted_path, 0o600)
        _run(
            [
                tools.age,
                "-d",
                "-i",
                str(identity),
                "-o",
                str(plain_path),
                str(encrypted_path),
            ],
            operation="age decryption",
        )
        return plain_path.read_bytes()


def generate_test_keyset(directory: Path, *, tools: Toolchain | None = None) -> tuple[Path, Path, Path, str]:
    """Create obvious, temporary, unencrypted keys for an offline test only."""

    if os.environ.get("SATLINK_TEST_ONLY") != "1":
        raise CryptoError("test key generation requires SATLINK_TEST_ONLY=1")
    tools = tools or Toolchain.discover()
    directory.mkdir(parents=True, exist_ok=False)
    os.chmod(directory, 0o700)
    public_key = directory / "TEST_ONLY.minisign.pub"
    secret_key = directory / "TEST_ONLY.minisign.key"
    age_identity = directory / "TEST_ONLY.age.identity"
    _run(
        [
            tools.minisign,
            "-G",
            "-W",
            "-p",
            str(public_key),
            "-s",
            str(secret_key),
        ],
        operation="test minisign key generation",
    )
    _run(
        [tools.age_keygen, "-o", str(age_identity)],
        operation="test age key generation",
    )
    recipient = _run(
        [tools.age_keygen, "-y", str(age_identity)],
        operation="test age recipient derivation",
    ).stdout.decode("ascii").strip()
    for path in (secret_key, age_identity):
        os.chmod(path, 0o600)
    return public_key, secret_key, age_identity, recipient
