# Exposé XIII — completed scan collation

Printed folios 616–666 are fully compared, word by word and symbol by symbol, with the two overlapping full-width main-image strips for every page. Main evidence is `scan/SGA6_scan_360dpi.pdf`, PDF pages 630–680. Witness images were consulted at the recorded uncertain loci; their folio offset is +11. The page certifications are in `page_status.jsonl`.

## Frozen deliverables

The final JSONL set contains 571 decisions: 191 checker findings, 235 FIXLOG entries, 58 MISPRINT records, 64 Codex records for 43 distinct proposals, and 23 HOLD hunks. It also contains 67 own findings and 87 exact patches. All 140 layer applications pass their expected-count assertions against the original page packets. No unresolved verdict, duplicate source ID, unsafe plain-O control-word merge, absolute workspace provenance, or email appears in these outputs. `validation.json` records the counts, ownership exceptions, and SHA-256 hashes.

The coordinator owns the two p. 619 replay records and the manual punctuation records for the displays on pp. 630 and 646. Their associated checker and FIXLOG findings are decided here. HOLD hunks 116–119 were erroneously assigned to pp. 619–620 by the initial registry; their actual loci are in Exposé XIV and their decisions remain in the frozen `review/late/` handoff. The actual XIII HOLD hunks are 88–110, all decided here.

## Substantive current-layer corrections

The diplomatic source stays exact. The corresponding current corrections have local proofs in the decision records and, where newly discovered, in `own_findings.jsonl`.

| Folio | Correction | Evidence and dependency |
|---|---|---|
| 618–619 | References 2.3(i),(ii) → 1.3(i),(ii) | The two cited assertions are exactly the regularity and multiplication-map assertions of 1.3. |
| 620 | Parameter space S → S′; F(1) → F(-1) | The same sentence defines S′; the proof uses the twisted exact sequence and χ(F(n−1)). |
| 622 | m=0 → m≥0 | P₀(c₀)=c₀≥b₀−a₀≥0. A length-one skyscraper with permitted c₀=1 refutes the printed equality. |
| 625 | L′_K → L_{1,K} | The composition is induced by the previously defined surjection L₁→E′, followed by β. |
| 626 | r−1 zeros → r zeros | The displayed tuple has r initial zeros followed by its final coefficient. |
| 627 | Proof reference 2.6 → 2.5 | The immediately preceding lemma gives the required curve bound. The printed labels 2.7 and 2.7.1 remain. |
| 628 | Final +β(β+1) → −β(β+1) | Substitute the displayed upper bound for β₀ into the identity containing −β₀. |
| 629 | L(n) → L(-n) in eventual vanishing | The preceding exact sequence identifies the negatively twisted H¹ groups used in the conclusion. |
| 630 | Binomial top m−1+i → m−1+j | The exact translated-binomial identity and its r=1 instance determine the summation index. |
| 632,635 | Restore the specified primes | The base-change and coproduct maps have the explicitly defined primed sources. |
| 638–639 | S′_α → S_α; conclusion family L → (f*)⁻¹(L) | The finite-type descent and inverse-image family are identified by their actual maps. |
| 643 | k-schéma → K-schéma | The connected parameter scheme carries the two specified K-points used in G(K). |
| 644 | Add “sous les hypothèses de 3.8” within Lemma 4.3’s hyperplane case | No governing §4 dimension hypothesis is present. For P¹→point, the Picard pullback is Z→0, disproving the unrestricted parenthesis. The cited 3.8 supplies the finite-type pullback needed by 4.2 under all its stated hypotheses, including the fibre-dimension condition. Coordinator independently confirmed. |
| 655–656 | O_X → O_P in the section constructions | F is a coherent sheaf on P; the evaluation map O_P→F and multiplication map O_P(-1)→O_P determine the ambient sheaves. |
| 657 | A superscript r−q → r−q+1 | The defined Aᵢ⁽q⁾ has q+1 coefficient slots. The displayed argument list has r−q+2 entries. The proof records 1≤q≤r+1, both endpoints q=r and q=r+1, and the independent coefficient-range support in 6.8. |
| 660 | Double-divisor sequence → 0→O_Z(-Z)→O_{X_n}→O_Z→0 | For I=O_Y(-Z), the quotient O_Y/I²→O_Y/I has kernel I/I²≅O_Z(-Z). Its twist yields the stated Euler-characteristic divergence. |
| 661 | Supply I after “tout idéal”; Hermann I. → G. | The same sentence already uses I and √I. Primary publisher metadata identifies Grete Hermann; evidence is archived locally. |
| 664–665 | “numériquement équivalent” → “numériquement proportionnel” | The exact projection [M]↦h[M]−d[H] must be nonzero for the strict inequality. P², O(1), O(2) gives 4=4 under the printed hypothesis. The proof expands the intersection square in both dimensions. Strict < is also the observed printed glyph. Coordinator independently confirmed. |
| 666 | Mumford terminal page 103 → 104 | The journal’s primary issue table lists Pathologies III on pp. 94–104, with the next article beginning 105. The printed duplicate reference remains diplomatic; current contains one corrected reference. |

Existing correct current repairs, including missing parentheses, the Φ inverse image, and the h exponent in the proof of 7.3, are confirmed separately in their checker/FIXLOG/Codex decisions.

## Proposals retained or reversed

The printed mixed degree-pairing punctuation on p. 651 remains: both the comma-separated arguments and product notation evaluate under the explicit map (b,a)↦deg(b·a). The p. 650 plain Pic fibre notation is supported by the assumed representing scheme and its functor-of-points isomorphism. The feminine “surjective” on p. 645 and “d’où que” on p. 660 remain. Spacing-only “derang” and the missing hyphen in “S schéma” are excluded from the apparatus under the checker conventions.

The rejected change from a_{m,i} to c_{m,i} in 6.3 remains rejected: Lemma 6.2 permits c=a and then gives exactly the printed bound. The p. 622 b_i≥0 clause correctly permits padding the sum from the support dimension to r; the next sentence uses c_i≥b_i−a_i. HOLD’s extra explanatory estimate is unnecessary. The shorter sheaf-family wording in 3.3 remains because the inverse image lies in the explicitly stated Picard functor and hence already consists of invertible-sheaf classes.

Body structure-sheaf O is plain throughout XIII, with the separately observed underlined p. 616 footnote. Plain-O TeX replacements use `{O}` to prevent lexical merging with a preceding control word. Defined-term underlines and the two displayed underlined “et” are patched locally. The coordinator’s statement-underlining convention is recorded independently from local content corrections.

No master file was edited. `review/xiii/` is frozen after this handoff.
