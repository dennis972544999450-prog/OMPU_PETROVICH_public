#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<'EOF'
Usage: bootstrap_sputnik_application_keys.sh --output-dir DIR [--test-only]

Generate Sputnik's Satlink application keys in Sputnik's own environment.
The directory must not already exist. Normal mode asks minisign for a key
password. Test mode requires SATLINK_TEST_ONLY=1 and creates disposable,
unencrypted fixture keys.

This script does not create or issue a NATS credential.
EOF
}

output_dir=""
test_only=0
while (($#)); do
  case "$1" in
    --output-dir)
      shift
      output_dir="${1:-}"
      ;;
    --test-only)
      test_only=1
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      printf 'unknown argument: %s\n' "$1" >&2
      usage >&2
      exit 2
      ;;
  esac
  shift
done

if [[ -z "$output_dir" ]]; then
  usage >&2
  exit 2
fi
if [[ -e "$output_dir" ]]; then
  printf 'refusing existing output path: %s\n' "$output_dir" >&2
  exit 2
fi
if ((test_only)) && [[ "${SATLINK_TEST_ONLY:-}" != "1" ]]; then
  printf '%s\n' 'test mode requires SATLINK_TEST_ONLY=1' >&2
  exit 2
fi

for tool in age-keygen minisign python3; do
  command -v "$tool" >/dev/null || {
    printf 'missing required tool: %s\n' "$tool" >&2
    exit 3
  }
done

umask 077
mkdir -p "$output_dir/private" "$output_dir/public"
chmod 700 "$output_dir" "$output_dir/private" "$output_dir/public"

age_identity="$output_dir/private/sputnik-satlink.age.identity"
minisign_secret="$output_dir/private/sputnik-satlink.minisign.key"
minisign_public="$output_dir/public/sputnik-satlink.minisign.pub"
enrollment="$output_dir/public/PUBLIC_ENROLLMENT.json"

age-keygen -o "$age_identity" >/dev/null
if ((test_only)); then
  minisign -G -W -p "$minisign_public" -s "$minisign_secret" >/dev/null
else
  printf '%s\n' 'Minisign will now ask for a local key password.' >&2
  minisign -G -p "$minisign_public" -s "$minisign_secret"
fi
chmod 600 "$age_identity" "$minisign_secret"
chmod 644 "$minisign_public"

age_recipient="$(age-keygen -y "$age_identity")"
export SATLINK_AGE_RECIPIENT="$age_recipient"
export SATLINK_MINISIGN_PUBLIC="$minisign_public"
export SATLINK_ENROLLMENT="$enrollment"

python3 - <<'PY'
import hashlib
import json
import os
from datetime import datetime, timezone
from pathlib import Path

public_path = Path(os.environ["SATLINK_MINISIGN_PUBLIC"])
public_bytes = public_path.read_bytes()
fingerprint = hashlib.sha256(public_bytes).hexdigest()
record = {
    "created_at": datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z"),
    "encryption": {
        "algorithm": "age-x25519-v1",
        "recipient": os.environ["SATLINK_AGE_RECIPIENT"],
    },
    "protocol": "satlink.enrollment.v0",
    "sender_claim": "sputnik",
    "signing": {
        "algorithm": "minisign-ed25519",
        "key_id": "sputnik-ms-" + fingerprint[:16],
        "public_key_file_sha256": fingerprint,
        "public_key_text": public_bytes.decode("utf-8"),
    },
    "status": "unbound_public_claim",
}
Path(os.environ["SATLINK_ENROLLMENT"]).write_text(
    json.dumps(record, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
    encoding="utf-8",
)
PY
chmod 644 "$enrollment"

printf 'public enrollment ready: %s\n' "$enrollment"
printf '%s\n' 'private keys stayed under private/ and must never be sent'
printf '%s\n' 'next gate: independent identity binding plus proof-of-possession challenge'
