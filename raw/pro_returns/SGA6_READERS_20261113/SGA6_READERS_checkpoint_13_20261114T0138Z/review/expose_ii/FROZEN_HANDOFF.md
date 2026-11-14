# Exposé II: completed scan collation

Printed folios **160–221**, including both appendices and the bibliography, have been compared against the main scan word by word and symbol by symbol. Each page was viewed in four overlapping strips. The comparison includes text, formulas, diagrams, underlining, individual mathematical glyphs, headings, author notes, punctuation and exact folio boundaries. Printed221 is the final II bibliography page; ExposéIII starts222.

The main source is `scan/SGA6_scan_360dpi.pdf`, physical PDF page = folio +14. The independent witness is `scan/SGA6_witness_300dpi.djvu`, physical page = folio +11. Witness use is regional and is specified in the individual records; this handoff makes no claim of complete word-by-word collation of the second scan.

## Frozen merge inputs

| File | Content |
|---|---|
| `review/expose_ii/decisions.jsonl` | 871 inherited-record decisions with stable source IDs |
| `review/expose_ii/own_findings.jsonl` | 198 additional, occurrence-specific observations |
| `review/expose_ii/patches.jsonl` | 336 exact patches:280 both-layer,41 current-only,15 diplomatic-only |
| `review/expose_ii/page_status.jsonl` | 62 complete page records, one per folio160–221 |
| `review/expose_ii/coverage_audit.json` | Expected IDs, source coverage, exact composition checks and counts |
| `review/expose_ii/author_claim_issue_206.json` | Decided and retained source statement with a separately demonstrated author-claim issue |
| `review/expose_ii/frozen_manifest.tsv` | Sizes and SHA-256 hashes of every frozen evidence file and script |

The page-status records are keyed by folio; their physical JSONL order changed during several amended readings and is not the reading order. The audit verifies the exact complete set160–221.

These are inputs to the coordinator’s annotated masters and reader builds. The English reconstruction, final compilation and final rendered typography are separately owned and checked by the coordinator and English reviewer.

## Complete inherited-source coverage

| Source family | Decided records |
|---|---:|
| Checker findings | 315 |
| Diplomatic FIXLOG rows | 235 |
| Current FIXLOG rows | 243 |
| MISPRINT register | 49 |
| Manual replay records | 3 |
| Hand-placed manual findings | 1 |
| ExposéII Codex queue records | 25 |

Every expected ID in these families has a decision. The audit includes string-valued page keys for six nonprinting macro-transition logs on183,198 and221. Their syntax/definition decisions leave the supplied macro blocks unchanged and do not claim printed macro text.

All six rejected Codex claims were adjudicated: entries229,230,250,255,256 and260. Their reasons identify the inspected glyphs or exact maps. There are no additional tagged-source aliases for II. The HOLD comparison has no difference within the supplied Codex II span: the exact II heading is at line3509 and the III heading at4996 in `fr/codex/sga6_fr_r1_fr.tex`; neighboring HOLD entries35 and36 concern I andIII respectively.

Marker-keyed records were assigned their actual printed folio. Examples include the manual/checker observation nominally on195 but printed196, the Ell term nominally on218 but printed219, and the bibliography heading nominally on219 but printed220. Each record retains its original stable ID while recording the actual image locus.

## Material mathematical and source decisions

The records distinguish a printed source reading from a justified corrected reading. Each mathematical correction has its local map, identity or reduction recorded rather than an unsupported change of notation. Examples include the pullback open subset in the171 argument; the vanishing complement of the interval on182; the target category of the section-derived functor on183; the normalization point and local algebra on185; the complex identification on190; the citation and Koszul computation on196; the principal-parts tensor and base sheaf on201; and the Sobolev target on214.

On183, the section functor on bounded locally free complexes is identified with the restriction of the derived section functor. The rejected Codex objection was amended on that exact identification; the first inclusion into the derived category of the space is retained, while the later section-induced target is the derived category of its ring of sections.

On185, the normalization discussion records the actual point map `p(tilde s)=s`. The finite normalization algebra over the henselian local ring is a finite product of local rings; the domain condition leaves one factor. The printed point label is retained without adding an inverse-image expression.

On190, the comparison is `Q(E^n) ≃ E^n`, from the acyclicity and section identification for the stated affine-cover terms. The inherited primes are withdrawn in the corrected layer after the coordinator’s earlier arrow repair. The printed raised complex dot is recorded separately.

On196, the locator is corrected from EGAII to EGAIII,1.1.3.3. The retrieved primary text identifies the relevant local-cohomology/Koszul relation; for `r=2,i=0`, the map `(e1∧e2)⊗m ↦ m` identifies the top Koszul kernel with the common annihilator. `external_reference_ega_iii_1_1_3_3.json` preserves the primary URL, locator, specialization and text-evidence status. Retrieval of that external reference is not reported as viewing its page image.

The final pages retain the actual range and order-sequence notation, repair the missing plural in216 in the corrected layer, and remove the extra inherited prime on Γ_S in217 in both layers. The latter stroke is the attached downturned serif of the printed Γ, as confirmed by the same unprimed glyph in the inspected176 diagrams. The displayed arrow on216 is retained without a tilde: its detached upper head stroke ends at the same right edge as the shaft and lower branch, and the coordinator independently confirmed that reading.

On219, the diplomatic `[S,I(S)]` remains; the corrected `[S,I(H)]` agrees with the explicitly defined homotopy class of a map `S→I(H)` and its homotopies `S×[0,1]→I(H)`. The printed historical questions about its relation with `K•(S)` remain questions in both layers.

## Folio206: decided source and separate author-claim issue

The general Hom-sheaf softness claim and the displayed unrestricted surjectivity assertion of Corollary2.3 are plainly printed. They are retained in both layers. The source reading is **decided**, and no replacement theorem is proposed. The coordinator independently inspected the witness wording.

The exact allowed example and obstruction are in `author_claim_issue_206.json`. In the category defined on200 and204, take the point base, smoothness class∞, `X=R²` and `Y=S¹`. The circle is allowed by its ordinary smooth interval charts. Let the closed set `A=S¹⊂R²` and the annular neighborhood `W={1/2<|z|<3/2}`. The smooth map `h(z)=z/|z|` defines a ringed-space morphism by pullback of smooth functions and hence a germ `[h]_A` in the printed target.

The displayed restriction is exactly `q:C∞(R²,S¹)→H⁰(A,Hom-underlined(R²,S¹))`, `g↦[g]_A`. A preimage would give `g∘i=id` for the inclusion `i:S¹→R²`. The explicit contraction `(1−t)z` makes `π₁(R²)=0`, so `g_*∘i_*=0`; the identity of `π₁(S¹)=Z` is nonzero. Thus the specified germ has no global preimage. This directly contradicts the unrestricted assertion while leaving its transcription unambiguous.

The continuation on207 explicitly takes the closed set empty and then the base reduced to the point. That continuation is retained and separately recorded. The local target-chart inclusion argument on205 only identifies germs locally factoring through the chosen chart; it supplies no unrestricted global extension in this example. No theorem replacing the printed claim is supplied.

## Literal glyphs, emphasis and author notes

Occurrence-specific font decisions preserve individual lower rules and their scope. A letter with two horizontal rules beneath it is transcribed with nested underlines; a genuinely doubled vertical stem is preserved as such. The two derived R symbols in the176 diagrams retain their vertical doubling, while the inspected derived R occurrences elsewhere use their actual lower-rule construction. The two R glyphs on181 were amended after enlarged main-scan inspection and composed with the coordinator’s earlier replay.

The category C, category L, structure-sheaf O, site S and complex E forms are scoped to inspected occurrences. Primes, degree indices and complex dots remain outside the letter rule when the scan shows that placement. No global font-macro redefinition is introduced by these records. Plain category A and B replacements include explicit TeX token delimiters; the166 and179 delimiter repairs preserve the same printed glyph sequence.

Lexical underlining is recorded separately from mathematical notation. The saved patches use `uline` on the inspected word groups, protecting formulas, references and author-note helpers. Defined words or paragraph numbers that are plain in the source remain plain. The accepted NOTE_6 section-title, statement-label and joint-name dash conventions remain in force. Layout-only findings preserve identical mathematical tokens and punctuation without content patches.

Author notes use the shared explicit helpers `SGAAuthorFootnote`, `SGAAuthorFootMark` and `SGAAuthorFootText`. Their literal label keys preserve the observed numerical or starred geometry, including raised stars where printed. Both distinct numerical1 labels on205 are retained and paired with their own calls; the proposed renumbering to2 was rejected. Calls following display punctuation and separate note text retain their observed placement.

## Validation and frozen authority

`freeze_audit.py` verifies complete source coverage, unique IDs and folios, exact patch anchors, cumulative composition after `review/middle/patches.jsonl`, newly introduced control words, private-reference absence and the retained-source status of the206 packet. The latest run has **zero coverage, anchor or control errors**. It performs620 layer applications across160–221 and records one already-present exact duplicate on165; no patch is blocked. The known181 and190 cumulative results are asserted explicitly.

The canonical frozen JSONL files and hashes are the merge authority. The incremental `add_*.py` scripts preserve the history and reasoning of entry, but older scripts must not be replayed blindly: later amendments and dependent patches were intentionally appended in a specific order. Rendering and crop helpers, visual evidence and all scripts are included in the manifest. The source masters were never edited by this reviewer.

There are **no unresolved in-scope source readings**. The separate author-claim issue on206 remains documented without textual emendation. Exposé0 remains frozen in its own earlier handoff. This II directory is now frozen; subsequent work proceeds in `review/expose_iv/`.
