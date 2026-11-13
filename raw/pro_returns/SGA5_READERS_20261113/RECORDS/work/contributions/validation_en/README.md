# Independent English master audit

The final audit passes. It checks the complete English authorial text from the
first verified Exposé I anchor through the final index against both frozen flat
sources. It uses its own balanced TeX argument parser, comment lexer, character
provenance map, edit-component construction, and branch replay; it imports no
preparation or wrapping helper.

## Exact body coverage

| Check | Corrected | Diplomatic |
|---|---:|---:|
| Authorial source characters before comment removal | 802,890 | 806,156 |
| Original comment characters removed | 188 | 188 |
| Retained source characters | 802,702 | 805,968 |
| Inserted folio-marker characters | 40,134 | 40,134 |
| Final prepared body characters | 842,836 | 846,102 |
| Verified folio markers | 793 | 793 |
| Distinct supplied folios | 479 | 479 |

Both prepared bodies equal the independently constructed frozen-source
projections byte-for-byte. Expanding each annotated-master choice produces
those same prepared bodies byte-for-byte. No whitespace-equivalence fallback
is used. Every retained character has its exact original flat-source offset.
Every discarded authorial-body character belongs to an explicitly identified
TeX comment. The first verified authorial anchor is at character 12,309 in each
flat source. The earlier 1,521-character editorial front, after the document
opening, is accounted for separately by length and SHA-256; the preamble is
hashed separately as well.

The full comment accounting distinguishes six original comment lines from the
792 later generated separator comments. The first generated separator is
removed when the body starts at its first folio marker. All 793 retained folio
comments match the alignment register in order, with their exact branch
positions and scan-index relation preserved.

## Variants and source provenance

All 875 original source variants and all 879 balanced master calls are
preserved. The two complete edit paths are divided into 843 exact components.
For every component, the original input edits and the master edits separately
reconstruct the same complete printed/corrected text pair. Every common gap
between components is also checked byte-for-byte. This accommodates exact
alternative placements of a deletion among repeated parentheses, and larger
balanced TeX spans that contain several original edits, without guessing a
source from similar words on a nearby page.

The final source resolver supplies precise original IDs for every master call.
The final audit finds zero generic source fallbacks, zero unknown IDs, zero
nearby-but-mismatched input citations, and zero folio labels outside the
recorded source component. Three grouped entries retain explicit multiple
folios: EN-0442 has 247 and 248; EN-0637 and EN-0638 have 384 and 385. Their
metadata and source text preserve those recorded ranges.

All 32 R98 entries retain separate calls and separate scan source IDs. Each
call preserves the exact original printed and corrected glyph strings and
adds the identical following script suffix to both choices. No following
superscript, subscript, or prime remains outside a variant call.

## TeX argument boundaries

Every master call and every folio-marker boundary is checked for an unbraced
preceding script, an unabsorbed following script, and a directly preceding
argument-taking macro. There are zero unsafe cases. One call, EN-0814, is the
single token argument of `\mod`. The installed `amsmath` definition reinserts
that argument once as its final token; the exact expansion therefore leaves
`\SGAvar` immediately followed by its three original groups. The definition
and token-level explanation are retained in the boundary audit.

## Reproduction and files

Run `audit_english_master.py` for a read-only audit. The optional arguments
`--english`, `--prepared`, and `--output` select the frozen source directory,
prepared-body directory, and audit destination. `apply_resolved_sources.py`
requires a fresh successful body/variation audit, verifies the audited hashes,
and changes only source/folio metadata in `EN_variants.json`; it preserves call
IDs and all before/after readings. The preparation script runs audit, resolution,
and audit in that order, then requires the final audit to pass.

The main result is `INDEPENDENT_EN_MASTER_AUDIT.json`. Its evidence files give
both directions of the input/master mapping, the exact edit components, the
resolved source table, every folio marker, argument-boundary checks, and all
32 scan-variant comparisons. Offsets are zero-based Unicode character offsets
with exclusive ends. SHA-256 values use the UTF-8 bytes of the exact text.

## Separate inherited-note relocation

The frozen prepared source retains the inherited English editorial footnote at
folio 43, so its characters remain included in the frozen-source totals above.
The reader wrapper separately extracts this one footnote and preserves its
entire payload in the corrected-only unresolved appendix. The decision is
EN-INHERITED-0046-P43. Its exact removal and reinsertion are independently
verified from the extraction ledger; all 879 calls and 793 markers are
unchanged. The glossary/note audit verifies the full payload against the
archived SGA5-READER-PROSE-002 record and checks the resulting 31 English notes
and 30 French notes.

This audit covers source preservation, annotation choices, provenance, and
TeX token boundaries. The build owner's separate reader-wrapper and PDF
checks cover the rendered apparatus, contents, and final pagination.
