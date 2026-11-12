# Human editorial preservation audit

**Result: PASS.** 169 of 169 source, argument, projection and visibility checks passed.

The exact source arguments, source lines, per-record correspondences, selected body arguments and hashes are in [HUMAN_EDITORIAL_PRESERVATION_AUDIT.json](HUMAN_EDITORIAL_PRESERVATION_AUDIT.json). The complete original evidence is also retained separately in [HUMAN_ORIGINAL_SOURCE_RECORDS.json](HUMAN_ORIGINAL_SOURCE_RECORDS.json).

## Paired human records

| Source scope | Records | Verified preservation route |
|---|---:|---|
| Original French A71766d9 active outer `sisi` calls | 1,261 | Every original call and both raw arguments are retained, with a verified route in both language dossiers. |
| Supplied D transmission | 1,258 | Every transmitted argument pair is reproduced exactly through the documented literal-TeX encoding in the French dossier. |
| Released English body records | 1,171 | Every released argument pair is reproduced through the explicit folio-marker and literal-TeX encoding. |
| Additional original-A records in the French supplement | 44 | Three calls flattened before D and 41 further pairs with changed transmitted argument bytes. |
| Additional original-A records in the English supplement | 315 | Every original pair without two byte-identical raw arguments in a corresponding released English pair. |
| Dedicated original proof rewrite | 1 per language | Complete commented printed proof and the Changement Yves replacement at Vbis, p. 138. |

The three original calls absent from the D paired-record inventory are `A-ORG-01-0016`, `A-ORG-17-0424` and `A-ORG-17-0496`. Their actual second arguments are the single TeX tokens `(`, `m` and `M`; the evidence preserves those exact tokens. The English crosswalk locates every original record in its native French-source line-range fragment. It records 946 pairs whose two original raw arguments occur in a corresponding released pair and 315 originals supplied separately. Twenty repeated configuration switches outside translated body fragments are explicitly excluded from the 1,171 body-record total.

## Editorial notes and visibility

| Language and form | Raw `nde` / `ndetext` / `acorriger` calls | Hidden generated archive notices | Inline human note | Visible human notes |
|---|---:|---:|---:|---:|
| French diplomatic | 121 | 0 | 0 | 121 |
| French corrected | 129 | 0 | 0 | 129 |
| English diplomatic | 122 | 2 | 1 | 121 |
| English corrected | 130 | 2 | 1 | 129 |
| Both reading forms | — | — | 0 | 0 |

The original French source contains 127 direct editorial-note arguments and two actual `acorriger` arguments. The source definition `\newcommand{\acorriger}[1]{\nde{#1}}` sends each of those two arguments unchanged to `nde`. Macro-definition templates are excluded from the invocation census. Both languages preserve all 129 original arguments in documentary dossiers visible in the diplomatic and corrected forms.

The English inline note is `A-NDE-04-010`, IV, p. 465: “This exercise does not seem to exist.” Its complete released marker and text remain byte-identical inside `SGAeditor`, which suppresses it in reading form. Five released English human-note arguments formerly inside `SGAArchiveOnly` are restored at X, pp. 46, 51, 52 and XVI, pp. 232, 246 without wording changes. Two VIII release-generated reference notices retain their always-hidden archive wrappers and are excluded from the visible human-note count.

### Eight notes absent from the diplomatic body

| Original note | Exposé / page | Source scope | Retention in diplomatic and corrected forms |
|---|---|---|---|
| `A-NDE-04-002` | IV / 314 | `A-ORG-04-0009` | Exact original argument in both language dossiers. |
| `A-NDE-05bis-016` | Vbis / 138 | `A-ORG-VBIS-REWRITE-138` | Exact original argument in both language dossiers. |
| `A-NDE-17-024` | XVII / 382 | `A-ORG-17-0367` | Exact original argument in both language dossiers. |
| `A-NDE-17-038` | XVII / 469 | `A-ORG-17-0586` | Exact original argument in both language dossiers. |
| `A-NDE-17-039` | XVII / 471 | `A-ORG-17-0606` | Exact original argument in both language dossiers. |
| `A-NDE-18-003` | XVIII / 488 | `A-ORG-18-0002` | Exact original argument in both language dossiers. |
| `A-NDE-18-008` | XVIII / 494 | `A-ORG-18-0009` | Exact original argument in both language dossiers. |
| `A-NDE-18-022` | XVIII / 516 | `A-ORG-18-0013` | Exact original argument in both language dossiers. |

Seven notes occur only in corrected arguments of original human pairs. The eighth accompanies the proof rewrite at Vbis, p. 138. The audit carries unique note identifiers through the actual source branch selection in memory; removing the audit markers recovers the exact unmarked source projection. This identifies each omitted note and each retained note independently of note-text equality.

## Supplied D/E note differences

Five note arguments already differ between the supplied D and E trees. The audit records their full before/after arguments, exact source lines, surrounding source context and hashes. The final diplomatic and corrected bodies preserve their respective supplied readings.

| Original note | Supplied D → supplied E difference |
|---|---|
| `A-NDE-14-003` | Reference `XIV.thm1.1` → `XIV.thm3.1`. |
| `A-NDE-18-009` | `identication` → `identification`. |
| `A-NDE-18-012` | `est tensorisant` → `en tensorisant`. |
| `A-NDE-18-024` | `rappport` → `rapport`. |
| `A-NDE-18-032` | Adds `que`; reference `1.5.10.2` → `1.5.10.4`. |

The corrected French body also omits the inactive source comment `%peu compréhensible` from `A-NDE-17-039`. Removing precisely that TeX comment and its terminating newline reproduces the final argument byte for byte; the complete original comment remains in the original-note dossier. Every other final French body note argument matches its selected supplied-source argument byte for byte. All 130 raw released-English note-call arguments match the corrected English body byte for byte.

## Bibliography and dossier guards

Eight human-added XVIII bibliography entries are retained in a separately attributed diplomatic appendix in each language. French entries keep their exact original A texts and editorial ordinals 1, 2, 3, 6, 8, 9, 11, 13; only citation keys are explicitly namespaced. English entries reproduce their exact released-English wording and source record IDs. The full dossier files match their master spans after one documented metadata operation: removing an `addcontentsline` whose title exactly repeats the immediately preceding `chapter*` title. No argument bytes participate in that metadata operation.

The literal encoders expose TeX metacharacters, including the ASCII tilde, and add line-break opportunities. Complete raw UTF-8 arguments remain in the JSON evidence. The NDE macros, the inline-note guard and the dossier guards all suppress their editorial material in reading form.

## Reproduction and frozen inputs

Run `python build_scripts/human_preservation_final.py` to regenerate this audit from the source trees, source-record manifests and frozen masters. It edits audit outputs only. Run `python build_scripts/audit_en_om_branches.py` for the 338-record English one-model branch audit.

| Master | SHA256 |
|---|---|
| `fr/SGA4_FR_master_annote.tex` | `be797e8e63e61cc570075d7e2a282a189d199c6efd3917b9c4dba8befb6cf035` |
| `en/SGA4_EN_annotated_master.tex` | `24f2c7ded704eb13e6d9039879eb05cbe6fdc415cfc226e783c672e9a015be9a` |

The preservation audit contains source hashes for all 20 original French exposés and the released English master. Its source-record hash binds every exact argument and correspondence to the checked build.
