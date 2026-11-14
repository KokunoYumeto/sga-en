# English checkpoint03 source handoff

The source is frozen through printed folio 110. Exposé 0 and the first 33 folios
of Exposé I have been freshly translated against the reviewed French. The
remainder remains the supplied unverified English, and the completion notice
is retained in every form.

## Exact state

- 28 accepted exact-text replacement records; 92 source variants.
- 3,548 current mathematical units on folios 1–110; 27 explicitly approved
  nonidentical pair occurrences; zero unexplained differences.
- The materialized current and diplomatic Exposé I branches, 78–110, both pass
  exact mathematical-unit comparison. Each has nine approved lexical pair
  occurrences and no unexplained difference.
- Five Exposé I transfer ledgers preserve all relevant page hashes, patch
  record hashes, glyph counts, original note marks, prose-reference decisions
  and printed/current variants. Original English sources are untouched.
- Four standalone TeX sources have been generated through110. Existing PDFs
  still come from the successful through95 build until the coordinator runs
  the frozen-stage compilation. These scopes are explicit in the work summary.
- The p90 matrix spacing repair preserves the identity map on every row/cell,
  formula and arrow; an isolated rendering of the exact generated source
  confirms clear spacing. Display-variant markers now sit before the diagram,
  with the same apparatus ID in both source branches. The probe succeeded and
  was visually inspected; temporary TeX/PDF products were removed.

## Commands from the frozen sga6_work directory

```sh
python review/english/verify_reviewed_english.py
python review/english/verify_expose_i_forms.py
python review/english/build_english_candidates.py
python review/english/compile_candidates.py
python review/english/make_alignment_hints.py
```

The compilation helper uses the coordinator's isolated TeX environment and
runs two passes on each of the four forms. It records exact source/PDF hashes,
compiled print markers and variant IDs, and sanitized diagnostics. After the
build, inspect the full-document regions around original90 and diagram
variants69/79, and the new p109 variant and p110 author note. Refresh the work
summary with the actual frozen-stage build results; no through110 PDF success
is claimed by this pre-compilation handoff.

The earlier EN_FROZEN_HANDOFF.md and EN_CHECKPOINT02_MANIFEST.json describe
checkpoint02 only; their historical identity is preserved. Current exact
source state is described by this handoff, the checkpoint03 manifest and the
through110 verification records. The glossary has115 scoped reference rows,
with literal case-sensitive raw-TeX phrase counts; cross-volume candidate
choices remain unresolved, and no complete glossary claim is made.
