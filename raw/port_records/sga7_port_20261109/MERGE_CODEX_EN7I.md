# English SGA 7 I: Codex's working components merged into the ported repository source

Made by Claude (Opus 5.5, session 329fb1e6) on 10 Nov 2026. Written into the working tree of
`C:\Users\user\Documents\rights_cc0_20261025\sga-en`, folder
`sources\native\SGA7I\SGA7I_English_current_buildable_source_20260823\components`. Not committed, not pushed.

## The three versions

- **BASE**: the files at commit `437d6d0` (4 Nov), the parent of the port commit `6ec1c2e` (9 Nov, the only commit
  of the port rounds 1-3 that touches `sources/native/SGA7I`). These are the public bytes of 24 Aug.
- **OURS**: the working-tree files at `6ec1c2e` (clean before the merge), with the port edits of
  `PORT_EN7I_LOG.jsonl`.
- **THEIRS**: `interlanguage_parts\03_projects\language_management\english_germanic\03_working_translations\sga7i_english_complete_translation_successor_20260731_r1\source\components`.

## Method

Codex's files are in a different format from the repository: LF line endings, TeX comments (scan and folio
markers), and no `\SGARefTarget`/`\SGARefLink`/`\SGARefAliasTarget` macros. A plain `git merge-file` on the raw
files would have counted every format difference as a Codex change. So, per file:

1. The text differences BASE -> THEIRS were listed after removing comments and link macros and collapsing white
   space (the normalization of the audit's `cmp_norm.py`). The result was the same 15 files and the same changes
   as the audit (85 lines).
2. Each change was checked against the French corrected layer `sga_scan_check_20261105\sga7i\current\` (for
   Exposé VI, which Rim wrote in English, that layer is the English original), and against the diplomatic layer to
   see what the printing has.
3. THEIRS' was built: BASE in repository format (CRLF, no comments, link macros) with the accepted Codex changes
   and the resolutions below. Where Codex corrected a cross-reference, the corrected number is linked to the
   existing target in the repository's own style (`eix.n6-3`, `eix.n6-3-2`, `eix.n7-2-2`, `eix.n14-3-4`,
   `evi.n3-15`, `evi.n6-2`); all six targets exist in the tree. After normalization, THEIRS' equals Codex's
   file except at the two places resolved differently (120, 185).
4. `git merge-file -p OURS BASE THEIRS'` for each file. All 15 merged without a textual conflict (the port's
   edits and Codex's are on different lines in every file). The merged files were checked: no conflict markers,
   CRLF throughout, merged - OURS = the Codex changes only, merged - THEIRS' = the port changes only.

## Per file

The "printed" readings are from the diplomatic layer; "French corrected" from the current layer.

| File | From Codex | From the port (log ids) | Conflict / resolution |
|---|---|---|---|
| `120_expose_VIII_remarks_6_8_and_autocritique_6_9.tex` | nothing taken (see right) | none | **Disagreement on the reading.** Codex has "with closed immersion $i$, and $E$ is a set"; BASE has "and if $E$ is a set". The printed text has "et $E$ un ensemble"; the French corrected layer has "si $i:Y\hookrightarrow X$ désigne l'immersion fermée, et si $E$ est un ensemble". BASE matches the corrected layer, so BASE is kept. The file is unchanged |
| `155_expose_IX_section_8_1.tex` | "(4.1 and 6.5)" -> "(4.1 and 6.3)"; "(6.5.2)" -> "(6.3.2)", both now linked. Printed: 6.5, 6.5.2; French corrected: 6.3, 6.3.2 | C531 (underlining of the heading of § 8) | none |
| `158_expose_IX_section_9_2.tex` | "where $g\longmapsto u(g)$ is a homomorphism from $U$ to $V^\perp$" -> "where $u(g)$ is a homomorphism …"; in (9.2.9) the invariants $(\ldots)^I$ -> $(\ldots)^{\pi_o}$ | C532 ($T_\ell(T'_o(\overline k))$) | None in the text. The first Codex change departs from the printed text ("où $g \longmapsto u(g)$ est …") and agrees with the French corrected layer ("où $u(g)$ est …"); it is also the correct mathematics: by (9.2.2) $gx=x+u(g).x$ for $x\in U$, so for fixed $g\in I$ it is $u(g)$ that is a homomorphism $U\to V^\perp$. Taken. $\pi_o$: the text just before says the element is invariant under $\pi_o=\pi/I$, and the French has $(\ldots)^{\pi_o}$. Taken |
| `172_expose_IX_section_12_1_through_12_2.tex` | `^{,o}` -> `^{\,o}` twice (a backslash lost in BASE) | C590, C553, C554, C555, C943 (special -> generic fibre), C944 (12.5.4 -> 10.5.4) | none |
| `184_expose_IX_section_14_3.tex` | "7.22" -> "7.2.2", now linked. Printed: 7.22; French corrected: 7.2.2 | C572 (vertical arrow $\wr$) | none |
| `185_expose_IX_sections_14_4_and_14_5.tex` | the reference 4.3 -> 14.3.4 | none | **Partly taken.** Codex wrote "and Lemma 14.3.4 may be applied"; BASE "the uniqueness result of 4.3". Printed: "le résultat d'unicité de 4.3"; French corrected: "le résultat d'unicité de 14.3.4". Merged: "the uniqueness result of 14.3.4" (link to `eix.n14-3-4`), which matches the corrected layer word for word |
| `20_expose_VI_2_8_through_2_9.tex` | $\alpha_n:a'_n\to a_n$ -> $\alpha'_n:a'_n\to a_n$. Printed: $\alpha_n$; corrected: $\alpha'_n$ | C29, C30 (arrow-label sides) | none |
| `23_expose_VI_2_11_and_2_12_ab.tex` | `(S_1\times_SS_2,,f_1\times s_2(v))` -> `(S_1\times_SS_2,f_1\times s_2(v))` (stray comma, the remains of a lost `\,`) | none | none |
| `26_expose_VI_2_18_through_2_22.tex` | $\widetilde\xi:\underline h_{R_0}\to[\underline A]$ -> $\widetilde\xi:h_{R_0}\to[\underline A]$, as in the original (2.20 proof: "$\tilde{\xi} : h_{R_0} \longrightarrow [\underline{A}]$") | C665 (Isom over $\underline A(R_1)$) | none |
| `27_expose_VI_section_3_opening_through_3_1_b.tex` | `^{,0}` -> `^{\,0}` twice (lost backslash) | none | none |
| `28_expose_VI_3_1_c_through_3_4.tex` | `^{,0}` -> `^{\,0}`, `^{,n}` -> `^{\,n}` (lost backslash) | none | none |
| `38_expose_VI_section_4_opening_through_4_1.tex` | the structure functor $p:\underline M_{X_0}\to\underline C_\Lambda$ -> $P$, as in the original ("a functor $P : \underline{M}_{X_0} \to \underline{C}_\Lambda$") | none | none |
| `41_expose_VI_theorem_4_5.tex` | "by 2.13(a)" -> "by 3.15(a)" twice, link retargeted to `evi.n3-15`. Printed: 2.13(a); corrected: 3.15(a) | C68-C72 ($\mathcal X,\mathcal Y$ -> $\mathfrak X,\mathfrak Y$) | none |
| `53_expose_VI_5_5_through_5_6.tex` | `\underline I_{\mathfrak X}^{,2}` -> `\underline I_{\mathfrak X}^{2}` (stray comma) | none | none |
| `59_expose_VI_corollary_6_3.tex` | the proof repair of Cor. 6.3 (1), 28 Sep (SGA-SRC-002356): the step "since $k=k^2$ and $R$ is complete, $u=v^2$" is replaced by a successive-approximation construction of $T\in\mathrm{GL}_n(R)$ with $F(TX)=uF(X)$, with the editorial footnote; "The converse is immediate" -> "The converse follows from invariance of $I_R$ under $R$-isomorphisms". The same repair, word for word, is in the French corrected layer (`expose_VI_body.tex`, Cor. 6.3) | none | none. The argument was checked: $T_1=cI_n$ with $\bar c^2=\bar u$ uses only $k=k^2$; the forms $\partial F/\partial X_i(T_\nu X)$ are an $R$-basis of the linear forms, so $E_\nu=\sum_i L_i\,\partial_iF(T_\nu X)$ with $L_i$ in $\mathfrak m^\nu$; for a quadratic form $F(Y+Z)=F(Y)+\sum_i Z_i\partial_iF(Y)+F(Z)$ in every characteristic, which gives the congruence mod $\mathfrak m^{\nu+1}$; completeness gives $T$, and $X\mapsto TX$ sends $(F-a)$ onto $(u(F-b))=(F-b)$. The printed step does fail when the residue characteristic is 2 (e.g. $1+s$ is not a square in $k[[s]]$, $\operatorname{char}k=2$) |

The two reading disagreements are 120 (BASE kept) and 185 (Codex's number, BASE's wording). In both, the merged
text follows the French corrected layer. Everywhere else Codex's reading is the corrected one, and BASE has the
printed misprint (155, 184, 185, 20, 41), a reading the corrected layer changes (158), or a lost backslash or stray
comma (172, 23, 27, 28, 53).

## Port edits

`PORT_EN7I_LOG.jsonl` has 17 `applied` entries for these 15 files: C29, C30, C68, C69, C70, C71, C72, C531, C532,
C553, C554, C555, C590, C572, C665, C943, C944. For each one, `tr_new` is present in the merged file and `tr_old`
is gone. The log's other outcomes (`already`, `not_applicable`, `left`, `unclear`) changed no English text.

Seen in passing, not changed (it is the port's, not this merge's): in `172_…`, equation (12.1.6) now reads
`P^o\cap E=\underline{\text{the zero section of }}P. \quad .`, with two full stops (C553 kept the period and C554
added `\quad .`).

## Compilation

`python -I compile.py en7I --passes=2`: OK, 0 errors, 291 pages (290 before the merge; the repaired proof is
longer). No undefined references. The log's one warning ("Command \footnotesize invalid in math mode on input
line 16") was there before the merge.
