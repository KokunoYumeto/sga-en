# Complete French change logs

Every comparison is a complete sequence of full-line UTF-8 hunks. Applying the TSV rows at their recorded original byte ranges reproduces the target bytes exactly. The exported unified patches independently reproduce the same targets with GNU patch. No before/after cell is shortened.

## Comparisons

| Comparison | Complete change rows | Source SHA-256 | Target SHA-256 | TSV replay | Patch replay |
|---|---:|---|---|---|---|
| `baseline:o` | 6,069 | `f995450460a3a828233dee9098d5f4085eb544437cf9c972763df720d8b904cd` | `de944d630421fda55862f8f9079d87ddb92f86ae9e02bbdc67f7db9970f06e3e` | exact | exact |
| `baseline:c5` | 5,980 | `90aa8b45d0d012f0fb6733445ccf0a5ce719dea67c8e56b7fec8b0551ef1c523` | `de944d630421fda55862f8f9079d87ddb92f86ae9e02bbdc67f7db9970f06e3e` | exact | exact |
| `baseline:c4` | 5,956 | `e288737bd49bffecaf438ed653e18dbad7b043985cbdfc5e14006a5082bd23b3` | `de944d630421fda55862f8f9079d87ddb92f86ae9e02bbdc67f7db9970f06e3e` | exact | exact |
| `current` | 18 | `e789ad80e0862d61ab2d5a9503874883283b03d3fe3526ee74a816cd25b08800` | `de944d630421fda55862f8f9079d87ddb92f86ae9e02bbdc67f7db9970f06e3e` | exact | exact |
| `representation:current-body` | 1,163 | `31f41b039101c5eb94540263b0219b67ce7bd185d60b304dd2d216033b82dcf8` | `bef0b79566cc5911519b39a99bb134b8375ff1710b6ee8d15c33c5992b1ff786` | exact | exact |

`CHANGES_FR.tsv` contains the four source comparisons, with exactly the columns `page`, `place`, `before`, `after`, and `source`. The first text in `place` identifies `baseline:o`, `baseline:c5`, `baseline:c4`, or `current`. `CHANGES_FR_REPRESENTATION.tsv` contains the separate body-preparation comparison. Reader front matter, contents, apparatus wrappers, and final page-marker display are handled by the main reader build and are outside these source/body comparisons.

## Scope and source attribution

All source differences are included: body text and formulas, punctuation, source comments, folio-marker additions, macro/environment definitions, preamble, document delimiters, layout commands, and whitespace. A hunk can carry several categories because a changed full line can contain both text and a comment, or because a replacement crosses a structural boundary. These labels describe source structure; they do not assign mathematical significance.

The August files contain mixed physical line endings, including 15,341 CRLF endings in `o`, 15,319 in `c5`, and 15,283 in `c4`; final current uses LF. For alignment only, each line is mapped to the string obtained by removing exactly one terminal CRLF, LF, or CR. The raw lines remain untouched. Paired equal-content lines with unequal ending bytes become separate, fully recorded `line-ending` rows, and all other non-equal alignment spans become complete source-change rows. This explicit mapping makes textual changes inspectable while retaining every line-ending change. No line ending is silently discarded.

Folios come from the final French marker sequence. A deletion with an empty target span is assigned the final folio at that insertion position. A hunk spanning markers lists every touched folio. The August files contain no folio markers, so this target alignment is explicit. `preamble` identifies material before the first folio.

Every row has its own stable diff decision in `FR_DIFF_DECISIONS.tsv`, the exact source and target artifact paths, and a reason to retain the authoritative final reading. Where an entire logged old string and new string are both literally present on the corresponding sides of a hunk, the related fix-log, hand-record, or misprint identifiers are added. These links are corroborating literal-pair evidence within a complete hunk; they are not represented as proof that one historical record accounts for every difference in that hunk. Rows without such a pair remain sourced by the exact authoritative files and their explicit diff decision. No historical attribution is fabricated.

The individually located new build decisions are linked by exact target-byte overlap with the full hunk: 32 R98 decisions, OPEN-H75, SOL-EN-084, and GLOBAL-98b. The current comparison therefore accounts for all 35 changes from the supplied current layer, even when several edits lie on one changed line. `FR_CHANGELOG_RECONSTRUCTION.json` records the complete edit-location mapping and every hunk range/hash.

## Exact privacy policy

Before diffing, the script applies only three declared substitutions: email addresses become `[email omitted]`; absolute paths under the explicitly enumerated Unix directories become `[local source path omitted]`; Windows drive paths under the explicitly enumerated user/system directories receive the same path placeholder. The regular expressions and stage-by-stage event counts are stored in `FR_CHANGELOG_RECONSTRUCTION.json`, and the implementation is in `build_changes_fr.py`. No whitespace, line endings, TeX notation, prose, or punctuation is otherwise rewritten for the comparisons.

The actual inputs produced **0 privacy substitutions**. Their sanitized bytes therefore coincide with their original bytes. All final TSV, JSON, Markdown, and patch outputs were checked with the same privacy detectors. Only archive-relative source paths and relative build-artifact labels are written.

## Body representation mapping

The raw body is extracted as the exact substring after `\begin{document}` and before `\end{document}`, without trimming. Evaluating the shipped `prepare_french.expand_document` function on the final current source reproduces `prepared/FR_corrected_body.tex` byte for byte. The report pins the SHA-256 of that implementation and its shared helper. The separate representation log records every literal difference caused by the mapping, including source-comment removal and joining, scoped macro expansion, protection of one-token arguments, and explicit braces around font arguments. Its rules, source/body offsets, macro names, and event counts are supplied in `FR_REPRESENTATION_RULES.json`.

The preparation mapping records 642 macro-expansion events covering 955 literal macro occurrences. This changelog establishes the exact transformation and byte reconstruction. Visual equivalence is assessed by the main reader build; no new visual verification is claimed here.

## Reproduction

From the build workspace:

```sh
python work/contributions/changes/build_changes_fr.py
```

The script accepts `--fr`, `--prepared`, `--source-edit-audit`, `--build-scripts`, and `--output`. It first verifies input manifests and the source-edit audit, then emits the logs, reloads the written TSVs, replays every comparison, and independently applies every unified patch. A failed identity, range check, or reconstruction stops the script.

In the records layout, place `build_changes_fr.py`, `prepare_french.py`, and `sga5_common.py` in `scripts/`, keep the prepared layers under `prepared/` and the inheritance edit table under `audit/`, and extract the attached French ZIP under `sources/SGA5_FR`. All inputs are configurable relative paths:

```sh
python scripts/build_changes_fr.py --fr sources/SGA5_FR --prepared prepared --source-edit-audit audit/SOURCE_TO_PREPARED_FR.tsv --build-scripts scripts --output changes
```

To replay one table directly, select rows whose `place` starts with the desired comparison label plus ` |`, encode their `before` and `after` cells as UTF-8, verify `before` at `old_bytes=start:end`, and replace the ranges in descending offset order. Byte ranges are zero-based and half-open. The script exposes this operation as `replay_tsv`. TSV quoting preserves embedded tabs, quotes, and newlines; read with a TSV/CSV parser, not by splitting physical lines.

Files: `CHANGES_FR.tsv`, `CHANGES_FR_REPRESENTATION.tsv`, `FR_DIFF_DECISIONS.tsv`, `FR_CHANGELOG_RECONSTRUCTION.json`, `FR_REPRESENTATION_RULES.json`, `FR_CHANGELOG_REPORT.md`, the five files in `patches/`, and `build_changes_fr.py`.
