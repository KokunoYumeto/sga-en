# Exact English packet routing: independent audit

**Passed. All 2,952 original English packet manifest/member files fit with the final English readers in the English ZIP. No packet projection, omission, redaction or collector change is needed.**

| Archive | Exact in-memory bytes | Headroom below 105,000,000 bytes |
|---|---:|---:|
| SGA6_READERS_FR.zip | 14,287,234 | 90,712,766 |
| SGA6_READERS_EN.zip | 76,818,374 | 28,181,626 |
| SGA6_READERS_RECORDS.zip | 79,926,749 | 25,073,251 |

The sizes cover the implemented plan captured at audit start. This audit's newly written reports add a small amount; their total uncompressed upper bound is recorded in the routing seal. The final packager retains its own exact size gate.

## Verified coverage

- All eight final reader/master PDFs remain in their language archives.
- All ten original catalog manifests and every one of their 2,952 manifest/member paths are present in EN with the exact original SHA-256 values. The unchanged collector verifies all ten packets.
- All 27 exact glossary input captures are in RECORDS, including the eight formerly excluded build-subpath captures.
- The archive payload union has no duplicate path across the three ZIPs. README.md and each archive's own MANIFEST.tsv remain common top-level metadata.
- Every manifest row in each in-memory ZIP was read back and its length/SHA-256 verified. CRC tests passed all three ZIPs.

## Privacy and historical diagnostics

All 2,858 text members of the packet/glossary closure passed the packaging privacy detector. An additional absolute-path scan produced exactly two explicitly inspected attribution tokens: `/root/review_late`, in the frozen XIII amendment records for source notes 616 and 631. The field identifies the canonical collaborating review agent; the corresponding image references use archive-relative paths. The audit records both source IDs and evidence paths.

The 16 probe logs total 15,744 bytes. Each already begins with its diagnostic-only sanitization notice and retains only run/exit status, diagnostics and relative output names. Their historical failed runs remain historical probe evidence; their files and original hashes are preserved. No private path or email was found.

The 10 probe PDFs and 111 PNGs remain included as binary packet members. The implemented packager handles them without attempting UTF-8 decoding.

## Fixed inputs and records

- Packager SHA-256: `3a69b30704b36e4906f5b7d8cd9beeb8103c1cbda6efcb9cb7f709d23aed375a`
- Required packet inventory SHA-256: `a1162edb7985a6890b53c9b69e3d0069b7987ec1b4d8f4e96bc2357782737bef`
- Catalog SHA-256: `15bd3c902f2e02f45b57fb0d5663d7b80743622d285297ee5f32560ed0411abd`
- `ROUTING_INPUTS.json` records every critical input hash and confirms stability through the run.
- `ROUTING_FILE_UNION.json` records every selected payload path, archive, size, hash and successful ZIP readback.
- `ROUTING_PACKET_VERIFICATION.json` records every required packet path and every exact glossary capture.
- `ROUTING_PRIVACY_AUDIT.json` records the text-file checks, all 16 log checks and the two agent-identifier dispositions.
- `ROUTING_IMPLEMENTATION_AUDIT.json` records the size and reconstruction conclusion.

Only this independent audit's records were written. No final ZIP, sealed packet, reader source or source decision was modified.
