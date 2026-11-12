# SGA 4 port pilot: review of every item (12 Nov 2026)

**Pilot**: 20 final French fixes (`PILOT_IDS.json`, drawn at random with seed 20261112 from the 549 final fixes
outside the seven Codex-newer English fragments: 8 of mathematics, 8 of words, 2 of punctuation or accent, 2 that the
corrected layer had before the scan check), carried into the English SGA 4 (sga-en `sources/native/SGA4`, tree
a76b2146) by GPT-6.1 Sol, reasoning effort high, Flex tier, in one request (batch `en4_pilot_001`, 150 KB). Submitted
12 Nov 00:08 UTC, answered in 3.0 minutes; 58,104 input and 5,536 output tokens (3,988 of them reasoning), **$0.0858**
at Flex prices (ledger row `sga4-port-en4_pilot`). Answer: `answer_en4_pilot_001.md`, `decisions_en4_pilot_001.json`;
mechanical checks: `CHECK_decisions_en4_pilot_001.json` (5 edits would apply, 7 "already" quotes found once in the
page window, 8 not applicable, nothing refused).

**Review** (Claude Opus 5.5, 12 Nov 00:10-00:25 UTC): for each item I read the corrected French at the fix
(`sga_scan_check_20261105/sga4/current`) and found the English passage myself before reading Sol's answer; then I
compared. Questions for each: right place, meaning carried, notation kept, nothing else changed. Nothing was applied.

## Verdicts

| Id | Exposé, page | French fix | Sol | English (file in `<NN>/drafts/`, line) | Verdict |
|---|---|---|---|---|---|
| C37 | I p. 144 | `\varinjlim_j:\Hhom(J,F)` → `\varprojlim_j:…` in (9.8.3) | apply: `\varinjlim_j` → `\varprojlim_j` in (9.8.3) | `SGA4_I_LINES_6011_6089`:20, the functor of (9.8.3), which the sentence before says commutes with projective limits of type J; the English had the error | **Right.** Only the limit symbol changes; the tag and the rest of the line stay. |
| C41 | I p. 148 | `$Y_i\rightarrow Y_i$` → `$Y_i\rightarrow Y_{i'}$` | already | `SGA4_I_LINES_6090_6222`:110-111 "composites … with $Y_i\rightarrow Y_{i'}$ are equal" | **Right.** |
| C106 | III p. 267 | "pour les foncteur" → "foncteurs" | not applicable (French agreement) | `SGA4_III_LINES_31_241`:118 "… functors." | **Right.** |
| C120 | III p. 283 | `$𝒯_{𝒰}=𝒯_{𝒰}$` → `$𝒯_{𝒰}=𝒯_{𝒱}$` | already | `SGA4_III_LINES_862_1113`:11 `$𝒯_{𝒰}=𝒯_{𝒱}$` | **Right.** |
| C211 | V p. 26 | `\Hom_{C^{}\wedge_{A, 𝒱}}` → `\Hom_{C^{\wedge}_{A, 𝒱}}` | already | `SGA4_V_LINES_1362_1552`:22 `\Hom_{C^{\wedge}_{A,𝒱}}` | **Right.** |
| C289 | V p. 77 | "sur $s/U$" → "sur $\Ss/U$" | already | `SGA4_V_LINES_4066_4380`:51 "a sheaf $\Ff_U$ on $\Ss/U$" | **Right.** |
| C359 | V bis p. 148 | "projectives finis" → "finies" | not applicable (French agreement) | `SGA4_VBIS_LINES_3151_3452`:9 "nonempty finite inverse limits" | **Right.** |
| C363 | V bis p. 160 | diagram: `\bar{Z}' … '[d][dd]` gets the label `^{h'}` | apply: the same label on the same arrow | `SGA4_VBIS_LINES_3613_3730`:86, the English diagram had no label there | **Right.** Only `^{h'}` is added. |
| C378 | VI p. 184 | « $X$ quasi-compact » → « $f$ quasi-compact » | apply: "reduced to the case \`\`$X$ quasi-compact''" → "\`\`$f$ quasi-compact''" | `SGA4_VI_LINES_678_1095`:29-30; the English had $X$ | **Right.** The case « $X$ quasi-séparé » just before, which the fix does not touch, keeps its $X$. |
| C385 | VI p. 193 | "qui admit" → "qui admet" | not applicable (French verb) | `SGA4_VI_LINES_678_1095`:358 "admitting an automorphism $f$" | **Right.** |
| A50 | VII p. 361 | "Sont $F_\infty$ =" → "Soit" | not applicable (French grammar) | `SGA4_VII_LINES_666_1032`:193 "Let $F_{\infty} =" | **Right** ("already" would also have been right). |
| C596 | VIII p. 394 | "la catégories" → "la catégorie" (inside a `\sisi` of the French corrected layer, now `\sisi{la catégorie}{la catégorie}`) | not applicable; notes that the English has no matching `\sisi` | `SGA4_VIII_LINES_1012_1556`:189 "to the category of $X$-schemes" | **Right**, and it applied the prompt's `\sisi` rule correctly. |
| C624 | XII p. 85 | stray ")" after `\eqhyperref[XII.eq4.1]{4.1}` moved to after "de groupes" | already | `SGA4_XII_LINES_234_382`:51-52 "Restricting 4.1 to abelian sheaves (respectively, to sheaves of groups) gives" | **Right.** This page's fragment is one of the 11 without page alignment (the whole fragment was shown); Sol still found the one place. |
| C625 | XII p. 96 | "ne donnerons par ici" → "pas ici" | not applicable (French typo rendered correctly) | `SGA4_XII_LINES_383_784`:430 "We shall not give the proof of 5.11.1" | **Right.** I had expected "already"; the prompt files "a wrong French word that the translation renders correctly anyway" under not applicable, and Sol followed it. |
| C646 | XIII p. 136 | "êtale" → "étale" | not applicable (accent) | `SGA4_XIII_LINES_43_316`:151 "is étale" | **Right.** |
| C651 | XIII p. 142 | `\Oo_{U_x}=\phi$` → `\Oo_{U_x}=∅$` | already | `SGA4_XIII_LINES_317_549`:155-156 `…\Ass\Oo_{U_x}=\varnothing$` | **Right**: the English writes the empty set as `\varnothing`, its own convention, and Sol did not replace it. Unaligned fragment, found anyway. |
| C683 | XVII p. 298 | "défini on $A_0$" → "défini en $A_0$" | not applicable (French preposition) | `SGA4_XVII_LINES_1801_2200`:158-159 "defined at $A_0\in\Ob\Aa(S^{-1}_0)$" | **Right.** |
| C724 | XVII p. 467 | `\bigl[[T_{1},T_{2}]\bigr]` → `\bigl[[T_{1},T_{2}\|S]\bigr]` | apply: the same in `…\bigr]_{[n]\times[m]}` | `SGA4_XVII_LINES_8601_9000`:287; the English lacked `\|S` (it writes `[[T_{1},T_{2}\|S]]` 25 lines earlier, so the fix also makes the English consistent) | **Right.** Unaligned fragment (399 lines shown); the edit is unique there. |
| C740 | XVIII p. 503 | (1.3.3.4) `K]=\langle` → `K]\simeq\langle` | apply: `=` → `\simeq` in (1.3.3.4) | `SGA4_XVIII_LINES_1251_1650`:21, introduced as "a canonical isomorphism" | **Right.** |
| A110 | XIX p. 608 | `(R^{1}v^{!})F=0$` → `(R^{q}v^{!})F=0$` | already | `SGA4_XIX_LINES_451_850`:357 "$(R^{q}v^{!})F=0$ if $q\neq 2$" | **Right.** |

**Score: 20 of 20 decisions right.** Five edits, each at the right place, carrying the fix's meaning, keeping the
English notation, and changing nothing else (each `tr_old` and `tr_new` differ only in the corrected symbol or label;
the checks found each `tr_old` once in its page window, with braces, page markers and reference keys unchanged). The
seven "already" decisions quote the right English passage. The eight "not applicable" decisions are all French-only
slips (agreement, verb, preposition, accent, a typo the translation renders correctly).

## What Sol noticed beyond the fixes (checked; nothing changed)

- **V bis p. 160**: the English labels the arrow X'→X with h', the French does not. Right, and it is the other half of
  the same page's correction: the scan check moved the label h' from X'→X (fix C365, `X'  \ar[rr]^(.65){h'}` →
  `X'  \ar[rr]`) to the arrow from Z̄' (C363). C365 is final but was not drawn for the pilot. A full run gives each page
  all its fixes together, so C365 goes with C363 there.
- **VIII pp. 393-394**: "\emph{algebraic separable}" (lines 180-181 and 189 of `SGA4_VIII_LINES_1012_1556`) for
  « algébriques séparables »: clumsy English ("separable algebraic"). A translation slip, not covered by any French fix.
- **XVIII p. 503**: "whence a / isomorphism" across the end of `SGA4_XVIII_LINES_856_1250` and the start of
  `…_1251_1650`: should be "an". A translation slip.

These two slips belong to a separate English proofreading list; the port does not touch them.

## Recommendation: GPT-6.1 Sol at high is enough for the English SGA 4

- On this sample it made no error, on mathematics (limits, indices, a diagram label, a relation symbol), on prose
  that the English renders differently, on the edition's `\sisi` records, and in the two page windows that had to be
  given as whole fragments. Twenty items bound the error rate only loosely (zero errors in 20 is compatible with a rate
  up to about 14 % at 95 % confidence), so the full run keeps the SGA 7 safeguards: the mechanical checks of
  `apply.py`, every refused or "unclear" item by hand, and a hand check of the edits it makes (about a quarter of the
  items, judging from the pilot's 5 of 20).
- Max effort is not needed for the English: Sol high answered in three minutes for $0.09, and nothing in the pilot
  called for more reasoning. No item needs a person beyond that review.
- Expected cost of the English port of all 549 final fixes: about 2.9 thousand input tokens and 280 output tokens per
  fix in the pilot, so about 1.6 million input and 0.15 million output tokens, roughly **$2.5 at Flex prices** (likely
  less, since fixes of the same page share their pages of English).

Before the full run writes anything:
1. The user approves applying and publishing the SGA 4 port (the brief allows neither yet; `apply.py` has writing
   switched off).
2. Merge Codex's seven newer English fragments (Exposé I and V bis, 23-28 Sep) into sga-en, or confirm they can be
   dropped; otherwise the port would edit superseded text there.
3. After writing: `compile.py en4` (XeLaTeX, three passes; the release has 864 pages, 0 errors) and the push as for
   SGA 7.
4. The 349 fixes that are not final yet (293 on the 443 pages of the in-app recheck, 56 replays by hand) follow when
   the recheck has been applied: run `final.py` again; `build.py` skips what is already logged.
5. **Spanish SGA 4**: settle its source of record first (Codex's workpasses against the r21 release zips; it is not in
   the sga-es tree), then run a separate small pilot: the Spanish has two editions, so its batches pair the fixes of
   both French layers (both / corrected only / diplomatic only) as for the Spanish SGA 7, which this English pilot does
   not test.
