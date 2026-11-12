# Methodology: sga4_port_20261112

Brief (coordinator, 11 Nov 2026 about 23:34 UTC, from the user's "the important stuff is the API stuff"): set up the
SGA 4 port on the SGA 7 pattern, find the SGA 4 French fixes that are final and the translation trees that carry
SGA 4, run a pilot of about 20 fixes with GPT-6.1 Sol at high (Flex), add the ledger row, check every pilot result by
hand against the French and the translation, and apply or publish nothing.

## Model provenance

- Scripts, choice of the pilot, the hand review (`PILOT_REVIEW.md`): Claude Opus 5.5 (subagent), 12 Nov 2026.
- The pilot's proposed edits: GPT-6.1 Sol (`gpt-6.1-sol`), OpenAI Responses API, reasoning effort high, Flex tier,
  background mode; key read at run time by `enriques_api_pilot_20261106/enr_pilot.py` (never printed or stored).
- The French fixes themselves: the SGA 4 scan check of 11 Nov 2026 (`sga_scan_check_20261105/sga4_api_pass_20261111`:
  Claude Opus 5.5 high and GPT-6.1 Sol max on every page, fixes applied where both agree).

## The French source of record

- The scan-check working copy `C:\Users\user\Documents\sga_scan_check_20261105\sga4`, as `sga7i`/`sga7ii` were for
  SGA 7: `diplomatic` (the corpus diplomatic layer with the 898 agreed fixes, `FIXLOG_4.jsonl`) and `current` (the
  corrected layer with 774 of them replayed, `FIXLOG_4_CURRENT.jsonl`; 68 it already had, 56 to replay by hand,
  `REPLAY_MANUAL_4.json`). It is Orgogozo's LaTeX edition of SGA 4 (snapshot 71766d9) with Codex's source-keeping
  edits and corrections (corpus `interlanguage_parts\...\sga_french_canonical_corpus_20260804_r1\sga4`, only read).
  No French SGA 4 repository exists.
- Checked 12 Nov 2026 00:03 UTC (`final.py`): all 20 corrected-layer files have the SHA-256 that `apply_pass.py` recorded when it
  wrote them (`sga4_api_pass_20261111/APPLY_STATE.json`, 11 Nov 18:55 UTC), so every replayed fix is in place and
  nothing has changed them since; no file under `sga4` is newer than the pass's `SUMMARY.json`.
- The translations follow the corrected reading (the English sets `\setboolean{original}{false}`, so Orgogozo's
  `\sisi{printed}{corrected}` prints the corrected reading), so the port takes the corrected layer's fixes.

## Which fixes are final (`final.py`, `FINAL_4.json`)

A fix is final when it is in the corrected layer (a `FIXLOG_4_CURRENT` row whose new text is in the file, or a fix the
layer already had, "already there") and its printed page is not among the 443 pages waiting for the in-app recheck
(`PAGES_FOR_APP_CHECK.json`), which can still change those pages.

| | final | on a page of the recheck | not in the corrected layer |
|---|---|---|---|
| replayed on the corrected layer (`FIXLOG_4_CURRENT`, ids C0-C773) | 507 | 267 | |
| already in the corrected layer (`REPLAY_MANUAL_4` "already there", ids A…) | 42 | 26 | |
| to replay by hand (`REPLAY_MANUAL_4` "by hand", ids H…) | | | 56 |
| **total (898)** | **549 on 381 pages** | **293** | **56** |

Final fixes by exposé: I 61, II 24, III 13, IV 55, V 65, V bis 29, VI 125, VII 16, VIII 10, IX 14, XI 1, XII 12,
XIII 5, XIV 3, XV 8, XVI 7, XVII 56, XVIII 27, XIX 18. The 930 misprints of the print (`MISPRINTS_4.json`) are records,
not fixes; the French applies none of them, so there is nothing to port. When the recheck has been applied, `final.py`
runs again and the rest become final.

## The translations that carry SGA 4

| Edition | Tree | State |
|---|---|---|
| English (sga-en) | `rights_cc0_20261025\sga-en\sources\native\SGA4\SGA4_English_current_buildable_source_20260906\source` (git tree a76b2146 at main 202e743, unchanged since release v2026-11-10-english-edition, 864 pages) | Source of record. One open point: Codex's tree `interlanguage_parts\...\sga4_english_reader_clean_r8_20260730\source` has 7 fragments edited 23-28 Sep that are not in the repository (Exposé I lines 1347-1946, 4271-4625, 4854-5078, 5805-5940; V bis 3453-3612; audit `SOURCE_OF_RECORD_AUDIT_20261110`, sync row "behind"). Merge them before the port writes there; the pilot avoided them. |
| Spanish (sga-es) | Release assets only (r20/r21: Tome I assets 24-28, Tome II 20-23, Tome III 16-19, with the FUENTES_Y_EVIDENCIA_20260821 source zips) and Codex's workpasses `interlanguage_parts\03_projects\language_management\romance\13_sga4_tome{1,2,3}_spanish_20260820` (units with `\pageoriginale`, one French source unit per Spanish unit, Orgogozo's `\sisi` for the two editions) | Not in the repository tree. Source of record unsettled: the workpasses (files to 25 Aug-7 Sep) were never compared with the release zips (audit: "Not compared"). Settle that (`SOURCE_OF_RECORD_AUDIT_20261110\scripts\cmp_norm.py`, workpass against the r21 zips), put the sources in `sga-es/sources/`, then port with both French layers paired as for the Spanish SGA 7 (`sga7_port_20261109/build.py`). |
| Brazilian Portuguese, Vietnamese | — | No SGA 4 (pt-BR carries SGA 3 Tome II, SGA 4½ and SGA 5; vi carries EGA and FGA). |

## Method (English, target `en4`)

- **Pages** (`segment.py`): the English is 271 fragments, each the translation of lines a..b of Orgogozo's snapshot
  71766d9 (the file names say which), and it keeps the edition's `\pageoriginale` markers (1,545 of the French 1,556).
  Per fragment, the English markers are paired with the French markers of lines a..b when their numbers agree (260
  fragments); the k-th French marker of an exposé is the k-th page of the scan check's page table
  (`sga4_api_pass_20261111/PAGES.json`: Springer folio, counter, lines), so the counter offsets of Exposés II and III
  do not matter. In the 11 fragments where the English lacks a marker (or has one in the neighbouring fragment), each
  page the fragment touches is given the whole fragment.
- **Batches** (`build.py`): per printed page, the English of pages p-1..p+1, then the page's final French fixes with
  OLD, NEW and the corrected French around the fix (where NEW occurs more than once nearby, the occurrence whose
  neighbours match those of the fix in the text the scan check saw).
- **Prompt** (`run.py`): that of the SGA 7 ports, with the SGA 4 edition described and one rule added for Orgogozo's
  `\sisi` records; decisions apply / already / not_applicable / unclear, with exact edits.
- **Checks** (`apply.py`, dry run only): an edit must occur exactly once in the page window, keep the brace balance,
  the page markers, the keys of `\etiquette`, `\label`, `\hyperref`, `\hyperrefext`, `\eqhyperref`, `\ref`, `\cite`,
  and every `\sisi`, and not overlap another edit; an "already" must quote English found once in the window.
- **Money**: Flex only, one request at a time, a ledger row per run written by `run.py`
  (`compute_cost_ledger\LEDGER.jsonl`, id `sga4-port-<tag>`).

## Pilot (12 Nov 2026)

- 20 final fixes drawn at random (`pick_pilot.py`, seed 20261112) from the 536 final fixes whose page window avoids
  Codex's seven newer English fragments: 8 of mathematics, 8 of words, 2 of punctuation or accent, 2 "already there";
  13 exposés, all three tomes; two of the pages lie in fragments without page alignment.
- One request (`en4_pilot_001`, 150 KB), submitted 00:08 UTC, answered in 3.0 minutes: 58,104 input and 5,536 output
  tokens (3,988 reasoning), $0.0858 at Flex prices; ledger row `sga4-port-en4_pilot`.
- Decisions: 5 apply, 7 already, 8 not applicable; the dry run refused nothing. Hand review (`PILOT_REVIEW.md`): all
  20 right. Recommendation: Sol at high is enough for the English; the full run keeps the mechanical checks and a hand
  check of the edits. Nothing applied, nothing published.

## Merge of Codex's seven English files (12 Nov 2026, before the full run)

Codex edited seven English fragments on 23-28 Sep 2026 in its tree `interlanguage_parts\03_projects\
language_management\english_germanic\03_working_translations\sga4_english_reader_clean_r8_20260730\source`; they never
reached sga-en (audit `SOURCE_OF_RECORD_AUDIT_20261110\evidence\en_sga4_codexworking_vs_repo.txt`). In the repository
each of the seven has a single commit (656e043, 24 Oct, the 6 Sep text), so there is no later repository fix in them to
keep. Each hunk of `diff` (line endings ignored) was read against the corrected French
(`sga_scan_check_20261105\sga4\current`); every one is Codex's correction and agrees with the French, so each file was
taken from Codex whole, with the repository's CRLF line endings (`merge_codex_en4.py`, Claude Opus 5.5, 12 Nov
04:42 UTC).

| File (`<NN>/drafts/`) | Codex's change | Corrected French | Decision |
|---|---|---|---|
| `SGA4_I_LINES_1347_1496` | Prop. 5.8.3 (i), diagram (*), bottom arrow `u_{\ast}` → `u^{\ast}` | 01.tex l. 1433 `\ar[r]^{u^{\ast}}` | Codex |
| `SGA4_I_LINES_1497_1738` | `H\mapsto (H\times H\xrightarrow{\pr_2}X)` → `H\times X`; the commented-out diagram (5.13.2) of the French added as a comment | l. 1572-1573 `H\times X\xrightarrow{\pr_2}X`; l. 1612-1618 the same commented diagram | Codex |
| `SGA4_I_LINES_1739_1946` | Prop. 6.2: "notation of 5.1" → `\hyperref[I.def6.1]{6.1}`; (iii) `\varphi_i(D)` in `E_i` → `\varphi_i(F)` in `F_i`; proof: "these are monomorphisms ... they are isomorphisms" → "$u$ is a monomorphism, and hence it is an isomorphism" | l. 1791, 1838-1839, 1867-1868 | Codex |
| `SGA4_I_LINES_4271_4625` | Exercise 8.8.8: "$X_i$ the subset ... of $\NN$" → "of $X$" | l. 4605 « de $X$ » | Codex |
| `SGA4_I_LINES_4854_5078` | `R\times_{X_XX}` in `(\Ind(C))` → `R\times_{X\times X}` in `(\Ind(C))^{\wedge}`; "contains $s(Z_i)$" → "contains the diagonal of $X$, $s(Z_i)$"; `Z_n=\Sup(Z_n,...)` → `Z_{n+1}=...` | l. 4936, 4959, 4973 | Codex |
| `SGA4_I_LINES_5805_5940` | `$pi$` → `$\pi$` (three times; an English LaTeX slip) | « $\pi$ » | Codex |
| `SGA4_VBIS_LINES_3453_3612` | `\Omega_{X/k}` → `\Omega_{\sisi{X}{X_i}/k}`; `\bar{u}_+` → `\bar{u}\sisi{_+}{_{\ast}}`; `\bar{u} (\CC)` → `\bar{u}\sisi{}{_{\ast}} (\CC)`; `S/C`, `X/C` → `\sisi{C}{\CC}`; `H^{\bigdot}_{DR}` → `\sisi{H}{\HH}` (twice); `)_{\circ}\bar{\pi}` → `\sisi{_{\circ}}{\circ}` (the English prints the second argument) | 05bis.tex l. 3479, 3484-3486, 3594, 3600-3601: `X_i`, `\bar{u}_{\ast}` (three times), `\CC`, `\HH`, `\circ` | Codex |
| `tomes/SGA4_English_translation_workpass.tex` (the 8th file of the audit) | Codex's copy is older (30 Jul): no title and credits page, older notice | — | repository kept |

One adjustment: Codex's `\sisi` records inside the `\xymatrix` of V bis 5.2.8 break the build (XeLaTeX: "Illegal
parameter number in definition of \lastprentry@@", the `\sisi` record cannot be made inside the diagram), so there the
corrected readings are written out (`\HH^{\bigdot}_{DR}` twice, `\circ`), as the corrected French has them. The merge
is commit b812b0a (sga-en, not yet pushed at that point); its tree compiled by itself (`compile.py en4 --root=<copy>`,
three XeLaTeX passes): 864 pages, 0 errors, 0 undefined references.

## Full run (12 Nov 2026)

- **Requests.** The 529 final fixes not in the pilot, cut by `build.py` into 10 requests of 66, 72, 60, 59, 43, 73,
  40, 63, 6 and 47 fixes (`batches_en4_full\`), each with its pages of the English (pages p-1..p+1 of each fix).
  `run.py en4 1 --tag=en4_full` sent them one at a time, 04:45-05:31 UTC: GPT-6.1 Sol (`gpt-6.1-sol`), Responses
  API, reasoning effort high, Flex tier; key handling as in the pilot. Every answer was dry-run by `apply.py` as it
  came in: no request had a refused edit or an "unclear" decision. Cost: $1.2165 (ledger row `sga4-port-en4_full`
  in `compute_cost_ledger\LEDGER.jsonl`).
- **Hand check (Claude Opus 5.5).** Every edit Sol proposed was read with `review.py` (the French fix as a token diff,
  the English line with the edit marked, and for formulas the full old and new text) against the corrected French
  at the place: the right place, the French fix's meaning, notation kept, nothing else changed. Every "already"
  was read with its English quote, and every "not applicable" that is not a plain French spelling or grammar fix
  (`review.py --na --already`). Corrected by hand (`HANDFIX_EN4.json`, the log row carries `hand_check`):
  C96 (II p. 253: Sol also copied the French's second closing parenthesis) and C448 (VI p. 257: the French reads
  "dans $E'_{\coh}$ et dans $E'$"; the English had Pro(...) in both places, from the transcription's
  "\Hom E'_{\coh}", and Sol corrected only the first). After `apply.py`, `post_apply_en4.py` took out one link that
  the link-key check does not let `apply.py` remove: C733 (XVIII p. 482), where the French reads "généralisée en
  2.17" without a link and the English, which the translator had linked to Theorem 2.14, now reads "generalized in
  2.17." Accepted with a note: C186 (IV p. 506) shows "(12.8.1)" with its link on subsection 12.8, which holds that
  equation (changing a link key is refused by the mechanical check).
- **PILOT_REVIEW.md's "C365" is C364.** The fix that moves the label h' of V bis p. 160 off the arrow X' -> X is
  C364 (`X'  \ar[rr]^(.65){h'}` -> `X'  \ar[rr]`); it went in with batch 004, so the label now stands only on the
  arrow from Z-bar' (C363, pilot). C365 is an app_check fix of p. 162 ("1'I.H.E.S."), not ported.
- **By-hand fixes (H).** Of the 34 off the recheck pages: 20 already right in the English, 12 French only, 2 applied:
  H33 (V p. 24, `\check{\Hh}^{0}` -> `\Hh^{0}`) and H39 (VI p. 254, 4.12: the chain ends in "(ii bis)", as both scan
  readings give; settled from the proof: (ii ter) gives (iii ter), hence (iii), and (ii) for every object, hence
  (ii bis); with (ii bis) => (ii), proved next, this closes (ii) <=> (ii bis) <=> (ii ter) of 4.10.6, while
  (iii) <=> (iii bis) is proved separately in the next step; the corrected French's "(iii bis)" is a transcription
  slip). The 22 on recheck pages wait. `FRENCH_HAND_REPLAYS_4.tsv` lists all 56 for the French side: the corrected
  French layer still needs each of them replayed by hand (H39 included). Not changed here: `sga4\current` is shared
  with the in-app recheck and hash-checked by `final.py`.
- **English slips** (`fix_slips_en4.py`, not fixes of the French): "algebraic separable" -> "separable algebraic" in
  VIII (three places; Sol found two, the third is the same phrase across a line break; the French reads
  "algébriques séparables"), and "whence a isomorphism" -> "whence an isomorphism" in XVIII (across two fragments).
- **Totals.** The 549 final fixes: 157 applied (152 in the full run, 5 in the pilot), 135 already right in the
  English, 257 not applicable (French only). By hand: 2 applied, 20 already, 12 not applicable, 22 waiting. Not
  ported: the 293 fixes whose pages wait for the in-app recheck. All 583 decisions are in `PORT_EN4_LOG.jsonl`;
  `PORT_EN4_LEFT.json` is empty. The English sources changed in 88 files (86 by fixes of the French, two more by
  the slips).
- **For the French side, noticed in passing.** V 8.2.6 (C293, p. 78): the English reads "from $\Tt/V$ to $\Ss/U$",
  the corrected French "de $\Tt/V$ dans $\Ss/V$"; the fix itself (s -> \Ss) is in the English, the U/V difference is
  older and was left as it is.

## Publication (12 Nov 2026)

- sga-en commits (identity KokunoYumeto, pushed to main after `git pull --rebase`): b812b0a (the merge of Codex's
  seven files), 18468f6 (the port and the two slips; 88 files), 4a4cbac (README and release records). Public files
  were scanned before each push for cost figures, local paths, e-mail addresses and the user's first name.
- Release https://github.com/KokunoYumeto/sga-en/releases/tag/v2026-11-12-english-edition (target 18468f6, 28
  assets, the names of 10 November), built by `sga_release_20261112\en\tools\build_release_sga_en_20261112.py`:
  SGA 4 and SGA 7 II rebuilt at the release commit (SOURCE_DATE_EPOCH 1794441600; their single-file LaTeX rebuilds
  each PDF byte for byte); SGA 7 I rebuilt with the 10 November epoch at the release commit, byte-identical to the
  asset of 10 November, so copied; the other six readers, the SGA 1 source ZIP, the evidence ZIP and the SGA 1
  notation record copied (their sources and single-file LaTeX equal those of 10 November). Rebuilt: the cumulative
  reader (3,963 pp.; two assemblies byte-identical), its LaTeX, the editable-source ZIP, the SGA 7 II source ZIP,
  the source guide (it gives both epochs), the edition record and the SHA-256 manifest. The SGA 4 reader keeps 864
  pages; 124 pages change. GitHub's asset digests equal the staged files.
- The README's record of AI work names GPT-6.1 Sol for the edits that carry the scan-check corrections into SGA 4.
