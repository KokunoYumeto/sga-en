# Exposé IV: frozen scan-collation handoff

## Coverage and evidence

Printed folios **274–296**, including the bibliography, have been fully compared against the main scan, word by word and symbol by symbol. All **23** folios have one `fully_checked` record. The main PDF physical page is the printed folio plus 14.

Native witness images were consulted on every folio for the recorded glyph, underline, punctuation and diagram regions. Witness physical page is the folio plus 11. These are explicit regional witness checks; this handoff does not claim a second complete word-by-word collation of the witness.

The canonical files are:

- `review/expose_iv/decisions.jsonl`: **271** inherited-source decisions.
- `review/expose_iv/own_findings.jsonl`: **52** additional observations, including one separately documented author-claim issue.
- `review/expose_iv/patches.jsonl`: **83** exact patches: 79 both-layer, 3 current-only and 1 diplomatic-only.
- `review/expose_iv/page_status.jsonl`: **23** complete-page records, folios 274–296.
- `review/expose_iv/coverage_audit.json`: source coverage, exact patch composition, scope and validation results.
- `review/expose_iv/frozen_manifest.tsv`: byte sizes and SHA-256 hashes for the frozen review directory, excluding the manifest itself and Python cache files.

The source decisions comprise 103 checker records, 141 ordinary FIXLOG records, 13 MISPRINT records, 10 Codex reconciliation entries and 4 unprinted macro-scope records. The Codex entries are 286–295, including the originally rejected entries. The applicable HOLD interval in the supplied corrected Codex tree is lines 6123–6714; it contains no HOLD record. There are **zero registry gaps and zero unresolved source readings** in this scope.

## Exact patch validation

All patches compose against the supplied marker-delimited page packets in their saved order, with each `expected_count` checked. The audit records **162 successful layer applications, zero blocked applications**, and no other owner’s patch affecting these folios. It also checks source-ID linkage, duplicate keys, required decision fields, added TeX control names, accidental control-word concatenation, residual automatic footnotes, residual italic emphasis and residual calligraphic O forms. These checks do not assign image verdicts.

The inspected author-note calls and labels on 276, 279 and 290 use explicit numerical labels. Local word rules, ordinary paragraph numerals and individual underlined O glyphs are represented explicitly. Statement-label and section-title conventions remain those accepted in the supplied conventions. No image decision has been inferred from a bulk replacement.

## Mathematical decisions needing particular attention

**278, the recursive construction.** The printed `C_{i−1}` is retained. `identification_278.json` gives the identity-on-objects and identity-on-morphisms identification `C_i=Ob(A_i)`, including the zero-object extensions, subobject and quotient arguments required by the construction. The proposed substitution by `A_{i−1}` is rejected with this explicit identification.

**283, the references to the two tensor pairings.** The current reference interchange is confirmed by the actual flat-resolution and degree-zero maps. The source references remain in the diplomatic form.

**285, Deligne’s bibliography reference.** Printed `[5]` remains diplomatic; current `[1]` is confirmed directly against the bibliography on296. The two interpolation stars have their individually observed heights.

**288, the projection expression.** The inherited current expansion `f^*(a)f^*(y)` is reversed to the printed `a f^*(y)`. `identification_288.json` identifies the action through the already stated restriction along `f^*`; both expressions denote the same explicitly given module action. No mathematical error is assigned to the printed expression.

**293, duplicate equation number.** Both source displays have `(3.2.2.1)`. The second current tag and its two later references are `(3.2.3.1)`. The decision identifies the map `β:colim K_•(Xi)→K_•(X)` and the final diagram’s vertical maps `α⊗β` and `β`, together with the perfect-to-coherent inclusion square. It does not infer the reference solely from numbering style.

**295, the first projection-formula domain.** `identification_295.json` supports supplying `/S` only in the first current domain, `x∈K_•(X/S)`. The diplomatic source keeps `x∈K_•(X)`. The second coefficient remains the printed `a∈K_•(S)`: the relative-perfect/coherent tensor pairing gives its exact meaning. The packet records both projection maps and the closed-immersion example over `k[x1,x2,…]` that obstructs the unrestricted absolute first domain. Codex entry295 is therefore split: its first proposal is applied, its second is rejected.

## Separate author-claim issue on295

`author_claim_issue_295.json` and `ASTRA-IV-AUTHOR-CLAIM-295` concern the **first external tensor pairing in 3.3.3** and its asserted induced Grothendieck homomorphism. Both French layers retain the printed claim.

The packet uses `A=k[ε]/(ε²)`, with identity maps on `Spec k` and `Spec A`. Both Tor-independent scheme pairs required by III4.7 satisfy the hypothesis. The exact derived-pullback definition of III1.6 yields `k⊗^L_A k`. Its explicit ε-periodic free resolution becomes a zero-differential complex with one copy of `k` in every nonpositive degree. Thus the indicated tensor output cannot be isomorphic to an object in the image of `D^b(k)_coh→D^−(k)_coh`. This contradicts the claimed bounded target for those inputs.

The packet proposes **no replacement theorem** and makes no claim about the existence of unrelated abstract bilinear maps. It does not assign the same defect to the second perfect/perfect pairing. Regional images of III231 and III256 document the invoked definition and hypotheses; no additional folio is marked fully checked by those consultations. The separate regional III247–248 images document the projection isomorphism used in the domain correction.

## Scope passed forward

FIXLOG rows `fixes/FIXLOG_6.jsonl#339`, `#340`, `fixes/FIXLOG_6_CURRENT.jsonl#304` and `#305` are Exposé V macro resets placed after the final bibliography text and before marker297. They are recorded as scoped implementation decisions. Neither Id nor Ob is printed on296. Later usage requires its own image check; the first post-reset `id` use is on317. This is a forward scope item, not an unresolved reading of296.

The II178 post-checkpoint05 reference amendment remains separately in `review/expose_ii_amendments/`. Frozen Exposé0 and II directories were not modified by this IV review. Subsequent work belongs in `review/expose_v/`; this IV directory is frozen after its final audit and manifest generation.
