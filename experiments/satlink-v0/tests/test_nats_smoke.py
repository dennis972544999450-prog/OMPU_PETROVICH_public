from __future__ import annotations

import asyncio
import os
import shutil
import socket
import subprocess
import tempfile
import time
import unittest
from pathlib import Path

try:
    import nats
    import nkeys
except ImportError:  # pragma: no cover - explicit optional dependency
    nats = None
    nkeys = None

from satlink.nats_transport import ensure_test_stream, publish_persisted


def _free_local_port() -> int:
    with socket.socket() as sock:
        sock.bind(("127.0.0.1", 0))
        return int(sock.getsockname()[1])


def _test_user_key():
    seed = nkeys.encode_seed(os.urandom(32), nkeys.PREFIX_BYTE_USER)
    return nkeys.from_seed(seed)


@unittest.skipUnless(
    nats is not None and nkeys is not None and shutil.which("nats-server"),
    "nats-py, nkeys, and nats-server required",
)
class JetStreamPersistenceSmokeTest(unittest.IsolatedAsyncioTestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.temp = tempfile.TemporaryDirectory(prefix="satlink-nats-test-")
        cls.port = _free_local_port()
        root = Path(cls.temp.name)
        cls.admin_key = _test_user_key()
        cls.sputnik_key = _test_user_key()
        cls.admin_seed = cls.admin_key.seed.decode("ascii")
        cls.sputnik_seed = cls.sputnik_key.seed.decode("ascii")
        admin_public = cls.admin_key.public_key.decode("ascii")
        sputnik_public = cls.sputnik_key.public_key.decode("ascii")
        config = root / "nats.conf"
        config.write_text(
            f"""
host: 127.0.0.1
port: {cls.port}
jetstream {{ store_dir: '{root / 'jetstream'}' }}
authorization {{
  users: [
    {{ nkey: {admin_public} }},
    {{
      nkey: {sputnik_public},
      permissions: {{
        publish: [satlink.v0.sputnik.out],
        subscribe: [_INBOX.>]
      }}
    }}
  ]
}}
""".strip()
            + "\n",
            encoding="utf-8",
        )
        cls.log_handle = (root / "nats-server.log").open("wb")
        cls.process = subprocess.Popen(
            [
                shutil.which("nats-server"),  # type: ignore[list-item]
                "-c",
                str(config),
            ],
            stdout=cls.log_handle,
            stderr=subprocess.STDOUT,
        )
        deadline = time.monotonic() + 8
        while time.monotonic() < deadline:
            try:
                with socket.create_connection(("127.0.0.1", cls.port), timeout=0.2):
                    return
            except OSError:
                time.sleep(0.05)
        raise RuntimeError("temporary nats-server did not start")

    @classmethod
    def tearDownClass(cls) -> None:
        cls.process.terminate()
        try:
            cls.process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            cls.process.kill()
            cls.process.wait(timeout=5)
        cls.log_handle.close()
        cls.temp.cleanup()

    async def asyncSetUp(self) -> None:
        self.nc = await nats.connect(
            f"nats://127.0.0.1:{self.port}",
            nkeys_seed_str=self.admin_seed,
        )
        self.js = self.nc.jetstream()

    async def asyncTearDown(self) -> None:
        await self.nc.drain()

    async def test_persisted_ack_and_server_side_deduplication(self) -> None:
        stream = "SATLINK_TEST"
        subject = "satlink.v0.sputnik.out"
        await ensure_test_stream(self.js, stream=stream, subject=subject)
        await self.nc.drain()
        permission_errors = []

        async def on_error(error):
            permission_errors.append(error)

        self.nc = await nats.connect(
            f"nats://127.0.0.1:{self.port}",
            nkeys_seed_str=self.sputnik_seed,
            error_cb=on_error,
        )
        self.js = self.nc.jetstream()
        first = await publish_persisted(
            self.js,
            stream=stream,
            subject=subject,
            payload=b"opaque-test-envelope",
            message_id="sl0_00000000000000000000000000000001",
        )
        second = await publish_persisted(
            self.js,
            stream=stream,
            subject=subject,
            payload=b"opaque-test-envelope",
            message_id="sl0_00000000000000000000000000000001",
        )
        self.assertEqual(first.stage, "transport_persisted")
        self.assertFalse(first.duplicate)
        self.assertTrue(second.duplicate)
        self.assertEqual(first.sequence, second.sequence)
        # The restricted Sputnik principal cannot call stream_info. Reconnect
        # with the test-only admin to inspect server state.
        await self.nc.drain()
        self.nc = await nats.connect(
            f"nats://127.0.0.1:{self.port}",
            nkeys_seed_str=self.admin_seed,
        )
        self.js = self.nc.jetstream()
        info = await self.js.stream_info(stream)
        self.assertEqual(info.state.messages, 1)
        self.assertEqual(info.config.max_msg_size, 128 * 1024)
        self.assertEqual(info.config.max_age, 72 * 60 * 60)

        # Verify the NKey is a capability, not account adjacency.
        await self.nc.drain()
        self.nc = await nats.connect(
            f"nats://127.0.0.1:{self.port}",
            nkeys_seed_str=self.sputnik_seed,
            error_cb=on_error,
        )
        await self.nc.publish("satlink.v0.someone-else.out", b"must be denied")
        await self.nc.flush()
        for _ in range(20):
            if permission_errors:
                break
            await asyncio.sleep(0.01)
        self.assertTrue(permission_errors)
        self.assertIn("permissions violation", str(permission_errors[-1]).lower())

    async def test_unregistered_nkey_cannot_connect(self) -> None:
        from nats.aio.client import Client

        rogue = _test_user_key()
        rogue_client = Client()
        expected_errors = []

        async def on_expected_error(error):
            expected_errors.append(error)

        try:
            with self.assertRaisesRegex(nats.errors.Error, "Authorization Violation"):
                await rogue_client.connect(
                    f"nats://127.0.0.1:{self.port}",
                    nkeys_seed_str=rogue.seed.decode("ascii"),
                    allow_reconnect=False,
                    max_reconnect_attempts=0,
                    connect_timeout=0.5,
                    error_cb=on_expected_error,
                )
        finally:
            await rogue_client.close()
        self.assertTrue(expected_errors)


if __name__ == "__main__":
    unittest.main()
