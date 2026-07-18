# T4 Verified-Bytes Consistency

## Result

`render_packet` emitted the later replacement, not the bytes accepted by
`verify_sources`.

## Reproduction

1. Copied `fixtures/case-alpha/full_context.md` to a temporary file.
2. Pointed an in-memory copy of the case-alpha tube at that file and called
   `verify_sources(tube, [temp_root])`.
3. The returned record reported `1365` bytes and SHA-256
   `a1eee6c51f51f38a2332f2024a3dc400893f7e0349ff37ead02d9b5e2e8a0b7c`.
4. Replaced the temporary file with `This is a harmless later replacement.\n`
   (38 bytes; SHA-256
   `1976a1faa408005ba03c5fcb381feab6882550731155f1304fcb17b454a33845`).
5. Called `render_packet(tube, verified)` with the already returned record.

Observed in the rendered packet:

- exact originally hashed source bytes: **absent**
- exact later replacement bytes: **present**
- rendered source body: `This is a harmless later replacement.`

Therefore the verification record preserves metadata and a path, but not the
verified bytes; rendering rereads the path after verification.
