# Complete English change logs

The release comparison retains every byte difference between the authenticated released English source and the frozen corrected English. The second comparison retains every difference between the exact raw body beginning at the first verified Exposé I anchor and the prepared reader body. Both written TSVs and both unified patches reconstruct their target bytes exactly.

| Comparison | Rows | Source SHA-256 | Target SHA-256 |
|---|---:|---|---|
| `release` | 2,055 | `64025cdf8285d54f894112b9179195dbb113b245674b4e0580f6af3756d187b1` | `3e662aeb9a77da7ac51427064cab5ef9648e9aeff63278c4bee9147a5cec5eec` |
| `representation:corrected-body` | 798 | `c1a7d520cdebce0a7f069a406b103e79449d4f75496181ab29a1dea418e20fe0` | `43f67ead9781a5563ab5b253e34c18a824ff52591258cf5277a95717faa01977` |

## Complete differences and line endings

`CHANGES_EN.tsv` and `CHANGES_EN_REPRESENTATION.tsv` have exactly `page`, `place`, `before`, `after`, and `source`. Before/after fields contain complete original line hunks, with all tabs, quotes, and line endings preserved. The `place` field supplies zero-based, half-open original byte ranges, so repeated strings and empty insertions replay unambiguously.

The released file has 15,829 CRLF line endings; the corrected file uses LF. Alignment alone uses the explicit key obtained by removing exactly one terminal CRLF, LF, or CR from a physical line. Every unequal ending is still retained in a `line-ending` row; every other non-equal line span is also retained. No ending, source comment, preamble change, formula, or textual correction is silently discarded.

To read or append these TSVs, use a CSV/TSV parser with `newline=''`. Default universal-newline reading would alter the CRLF bytes inside quoted cells. No cells are truncated.

## Source proof and attribution

The script verifies both attached English source files and the port log against their manifest. Starting with the ported source, it applies the explicitly recorded CRLF-to-LF input mapping, then replays all **398 common correction operations** at their recorded counts (**515 occurrences**). Scoped internal-Hom replacements use their recorded source scope or original occurrence positions. It then applies the **95 corrected-text changes** from the variant catalogue. The result equals the frozen corrected English byte for byte.

For port provenance, all **1,856** original one-based row numbers and their source IDs are retained. The script additionally rechecks both ends of **803** port-to-final intervals supplied by the port audit: the quoted source reading matches the ported source at its offset, and its terminal reading matches final English at its offset. Records with other audit dispositions keep those dispositions; no interval is fabricated.

Every change row has its own reasoned decision in `EN_DIFF_DECISIONS.tsv` and exact source/target paths. Located port intervals and traced common/projection intervals add the relevant one-based record references, open-item IDs, French-source references, and scan decisions. Intersecting later edits are retained in an explicitly defined provenance interval envelope. A linked record supplies located evidence within the full hunk; it is not represented as accounting for every hunk byte by itself.

`EN_COMMON_CHANGE_LINKS.tsv` has one row for each of the 398 common operations. `EN_PORT_CHANGE_LINKS.tsv` has one row for each of the 1,856 port records. `EN_PROJECTION_CHANGE_LINKS.tsv` has one row per input variant. A correction can have no non-line-ending release hunk when the released source already has its resulting reading; such an empty link list is retained without inventing a new release change. The exact source reconstruction proves the operation was applied to the ported source.

## Folio attribution

The 793 entries of `english/EN_ALIGNMENT.json` are the sole basis for folio labels. Their positions and folios are ordered, and their exact source hashes are recorded. Each change hunk is labelled by the nearest validated anchors that bound its final span. Equal bounding folios are labelled as bounded by validated anchors; differing folios are shown as a range. Material before the first anchor is labelled preamble/original front matter; material after the last is labelled from the last validated anchor onward. No interpolated exact folio is assigned to intervening English text.

The representation table uses the same anchors after their exact transport to the inserted marker positions. The reconstruction JSON records both bounding anchor IDs and positions for every hunk, so the basis of each label is inspectable.

## Body representation and scope

The independently replayed body mapping inserts all **793** validated marker events, retains their exact ordered folio sequence (**479 distinct folios**), extracts from the first verified Exposé I anchor through the final body end, and processes source comments with the recorded percent/line-ending rule. It reproduces `prepared/EN_corrected_body.tex` exactly. `EN_REPRESENTATION_RULES.json` gives the full mapping and offsets. No additional visual-equivalence claim is made here.

New reader front matter, the generated contents, apparatus wrappers, and final marker display are handled by the main reader build. This source/body log does not pretend to include those later wrapper operations.

## Privacy and reproduction

The shared script applies exactly the declared email and absolute-machine-path substitutions before comparison. These inputs required zero substitutions, so their sanitized bytes equal their original bytes. The detector patterns and event lists are recorded; generated outputs contain archive-relative source paths and relative build-artifact labels.

Place `build_changes_en.py` beside `build_changes_fr.py` in `scripts/`. From the records root, with the attached English ZIP extracted under `sources/SGA5_EN` and the recorded intermediate artifacts under `english/` and `prepared/`, run:

```sh
python scripts/build_changes_en.py --en sources/SGA5_EN --english english --prepared prepared --output changes_en
```

All four paths are configurable relative paths. The workspace command is:

```sh
python work/contributions/changes_en/build_changes_en.py --en work/sources/SGA5_EN --english work/contributions/english --prepared work/build/prepared --output work/contributions/changes_en
```

The script reloads written TSVs, applies every row at its original byte range, and independently applies both exported patches with GNU patch. Identity, count, interval, or reconstruction failures stop the build.
