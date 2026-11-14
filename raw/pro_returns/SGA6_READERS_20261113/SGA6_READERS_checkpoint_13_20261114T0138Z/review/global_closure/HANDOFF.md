# Historical closure handoff

The live stream `review/global_closure/decisions.jsonl` contains **108 attributed dispositions**: all **99** pending FIXLOG rows and **8** page-less rejected Codex rows from checkpoint11, plus the separately requested apparatus attribution amendment for **MISPRINT665**.

No source-body patch or new full-page certification is added. The complete French reviews, English seals and checkpoint inputs remain unchanged. Each closure points to exact existing source-decision records and page certifications; their literal JSON and hashes are retained in `evidence/attributed_records.json`. Forty group packets preserve every original historical payload and explain the disposition of each alias. Every pending canonical ID occurs exactly once in this stream.

## Material outcomes

- Codex241 and245 are closed by the already accepted VI411 total-cohomology and VI415 factor-count corrections, including their complete explicit proofs.
- Codex173 keeps the precise I89 local site-rule correction while rejecting blanket calligraphic normalization. Codex228 accepts the four scan-resolved A-prime transcription repairs and keeps the exact site/object glyph distinctions.
- Codex264 retains the unlabelled first assertion. Codex275 and282 use the already established local paired delimiter repairs. Codex278 retains the balanced label-plus-outer-parenthesis construction, newly re-viewed in both261 images.
- Global macros and scoped glyph records defer to the completed occurrence-specific decisions, including Cart's single rule, plain parf exceptions, Ab fil local expansions, the G/C definitions and the plain geometric Proj occurrence. Historical replacement counts are not presented as newly counted scan occurrences.
- The nineteen identical elision events in each old log have no individual offsets. Their operation is resolved, and all fifteen recoverable present occurrences in each layer are inventoried; a one-to-one reconstruction of the old events remains unavailable and is explicitly not asserted.
- MISPRINT665's copied MAt./Mat. explanation is replaced by its correct Sborik/Sbornik missing-n explanation, with checker686–690#47 and FIXLOG2656 as exact aliases. This intentionally supersedes `review/late/decisions.jsonl#746`; MISPRINT664 is unchanged. The source bodies already contain the proper paired readings.

`validation.json` records exact coverage and hashes. `write_closure.py` regenerates this evidence-only stream from the immutable source records and attached TeX, without editing either.
