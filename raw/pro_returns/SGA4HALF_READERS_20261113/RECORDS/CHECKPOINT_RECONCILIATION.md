# Checkpoint reconciliation

All 16 immutable checkpoint archives are accounted for in 5450 member rows. The table has 0 unresolved members.

| Disposition | Member rows |
|---|---:|
| excluded with reason | 242 |
| retained hash-identical | 4843 |
| superseded binary | 4 |
| superseded text | 361 |

The 290 distinct unified diffs in `work/checkpoint_diffs` cover changed text and complete textual exclusions. Each diff was independently applied to its old sanitized reading and reconstructed its new reading exactly. The table gives both raw SHA-256 hashes, sanitized-reading hashes, changed-line counts, and final archive destinations. Repeated versions share the same diff.

Checkpoints 07 and 08 are unpublished candidates rejected by privacy preflight. They remain represented by archive/member hashes and sanitized differences; their original bytes are not copied into the final package. Both the compile-log sanitizer and the final verifier’s privacy cleaner were applied before any old text was written to a diff.

Retained binary readers map to the final French or English PDF by exact hashes. Temporary layout trials are explicitly excluded in favor of the final readers and retained layout validation. Checkpoint-only progress metadata is replaced by the final index and README, while its complete sanitized wording remains in deletion diffs.

This record describes the stable current files selected by the packaging map. After packing, `python3 scripts/reconcile_checkpoints.py --check-packaged` verifies all named destinations and diff hashes inside the three final ZIPs without changing the package.
