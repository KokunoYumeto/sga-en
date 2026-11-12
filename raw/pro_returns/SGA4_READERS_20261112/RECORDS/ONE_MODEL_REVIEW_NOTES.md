# Review of the one-model misprint records

The register contains every record from `api_pass_20261111/OPUS_ONLY_MISPRINTS.json` (258) followed by every record from `api_pass_20261111/SOL_ONLY_MISPRINTS.json` (1,343), in their original order. Stable identifiers run from OM-OPUS-0001 to OM-OPUS-0258 and OM-SOL-0001 to OM-SOL-1343. Each record was read individually. Classification in either source JSON was treated as a report to review, not as proof of a correction.

The final register has **550 accept**, **8 reject**, and **1,043 possible-not-verified** verdicts. Among the accepted records, 53 intersect existing human editorial material and remain unchanged. The machine candidate file contains the other 497 accepted records: 338 are on undisputed pages and 159 carry a disputed-page hold. These are record counts; repeated reports and multiple changes within one report prevent interpreting them as counts of distinct text replacements.

## Meaning and application of the verdicts

An acceptance records an independently supportable spelling, agreement, delimiter, or mathematical correction. For elementary textual findings, the one-line reason identifies the local defect. Mathematical acceptances based on surrounding source text identify the relevant construction or give the short derivation. A rejection means the supplied proposal did not establish a required repair: examples include consistent label numbering, optional separator conventions, and deletion of a reference lacuna. A possible-not-verified verdict preserves the proposal for review without claiming its mathematical, bibliographic, or scan-dependent assertion has been proved. In particular, these verdicts do not assert that the questions cannot be settled by further textual work.

No page image was available in this review. A statement about a printed glyph remains a supplied reading, not a new scan verification. The 443 pages listed in `api_pass_20261111/PAGES_FOR_APP_CHECK.json` were flagged at whole-page granularity. Every accepted candidate on one of those pages has `application: hold-disputed-page`; its judgment does not authorize changing the agreed disputed-page text.

All 406 records classified `recorded by the editors` contain a reference to existing human editorial material. Their application is `preserve-human-apparatus`, independently of the verdict. An uncertain review of a model's description supplies no reason to delete or rewrite Orgogozo's correction. These records do not enter the application-candidate JSON.

`one_model_edits.json` supplies candidate pairs, source-relative file references, page/place anchors and hold flags. A pair marked `record-pair` is the source record's reported reading; it may require conversion to the actual TeX spelling at its exact occurrence. A `lexical-alignment` pair suggests a local word correspondence. A `verified-local-tex` pair was checked against the local TeX context. These pairs are placement inputs, not an assertion that all candidates have already been applied. No source tree was modified by this review.

## Explicit mathematical checks

### OM-OPUS-0005 and OM-SOL-0021 — I 5.10, page 32

The two records describe the same adjunction error. They share the duplicate group `I-5.10-left-adjoint` and must produce one textual correction and one apparatus entry.

Formula (5.10.1) defines

\[
(j_{X!}F)(Y)=\coprod_{u:Y\to X}F(u).
\]

For a natural transformation from this coproduct presheaf to a presheaf \(H\), restriction to the summand indexed by \(u:Y\to X\) gives a map \(F(u)\to H(Y)=(j_X^*H)(u)\). Naturality of the original transformation gives naturality of this family on the slice category. Conversely, a natural family of these summand maps induces the unique map from the coproduct at each \(Y\), and these maps form a natural transformation. Restriction followed by coproduct extension, and coproduct extension followed by restriction, are identity operations. Thus

\[
\operatorname{Hom}(j_{X!}F,H)\cong\operatorname{Hom}(F,j_X^*H).
\]

The explicit mutually inverse operations identify the stated left adjunction. The correction is `adjoint à droite` → `adjoint à gauche`.

Source: `fr/E_corrected_after_scan_check/01/01.tex`, I 5.10, (5.10.1).

### OM-SOL-0041 — I 7.6, page 55

The proposition states that \(\Pi_0\) is infinite and \(|\operatorname{Fl}C|\leq\Pi_0\). The product cardinal is therefore

\[
|\operatorname{Fl}C\times\operatorname{Fl}C|
=|\operatorname{Fl}C|^2\leq\Pi_0^2=\Pi_0.
\]

This proves the proposed inequality at the first comparison with \(\Pi_0^2\). The supplied hypothesis does not supply equality there. The page is disputed and application is held.

Source: `fr/E_corrected_after_scan_check/01/01.tex`, Proposition 7.6 and its proof.

### OM-SOL-0118 — I, page 148

The proof explicitly gives \(v_\alpha:T_\alpha\to Y_i\) and \(v_\beta:T_\beta\to Y_i\). The two projection maps have common source \(T_\alpha\times_XT_\beta\) and respective targets \(T_\alpha\), \(T_\beta\). Their composites to \(Y_i\) are consequently \(v_\alpha\operatorname{pr}_1\) and \(v_\beta\operatorname{pr}_2\). The proposed order follows from these actual domains and codomains.

Source: `fr/E_corrected_after_scan_check/01/01.tex`, page 148, definitions immediately preceding the displayed pair.

### OM-SOL-0169 — II, page 261

The surrounding proof explicitly applies the functor \(i_Aa_A\) to the coimage–middle-object–cokernel sequence. Each first or last argument is a nested expression with three opening parentheses. The displayed first and last composite terms have only two closing parentheses. The named functor is \(i_Aa_A\); the exact pair suggestions retain it and insert the missing closes. This check also identifies the upper-case subscript through the functor named in the proof.

Source: `fr/E_corrected_after_scan_check/02/02.tex`, page 261, transformed sequence and its following explanatory sentence.

### OM-SOL-0201 — IV 3.2.1, page 328

The inverse-image functor associated to \(u:E\to E'\) has type \(u^*:E'\to E\). Sending \(u\) to this functor therefore has target \(\mathop{\mathrm{Hhom}}(E',E)\). The immediately preceding bijection between transformations of direct images and transformations \(v^*\to u^*\) supplies the same source and target categories. This establishes the reversal of the two arguments in the target category.

Source: `fr/E_corrected_after_scan_check/04/04.tex`, IV 3.1–3.2.1.

### OM-SOL-0288 — IV 9.7.2, page 475

The inclusions are \(j:U\to E\) and \(i:F\to E\). A point \(p:P\to U\) gives a point of \(E\) by the composite \(j\circ p:P\to E\); the second composite is \(i\circ q\). These are the maps of point categories displayed in the proposition. This page is disputed and application is held.

Source: `fr/E_corrected_after_scan_check/04/04.tex`, IV Proposition 9.7.2.

### OM-SOL-0472 and OM-SOL-0473 — Vbis 5.1.0–5.1.1, page 148

The text defines a simplicial object as \(X:\Delta^{\mathrm{op}}\to H\), with degeneracy \(s_i^k:X_k\to X_{k+1}\). The corresponding morphism of \(\Delta\) therefore has source \([k+1]\) and target \([k]\). This supplies the corrected direction in OM-SOL-0472.

The next paragraph expressly names \(s_\ell^{k-1}:X_{k-1}\to X_k\). Its image inside \(X_k\) is the one used in the formula defining \(NX_k\), so that formula requires the same exponent \(k-1\). This supplies OM-SOL-0473 by direct identification with the immediately preceding map.

Source: `fr/E_corrected_after_scan_check/05bis/05bis.tex`, Vbis 5.1.0–5.1.1.

### OM-SOL-0493, OM-SOL-0494 and OM-SOL-0495 — VI Exercise 1.28, pages 192–193

The exercise starts from an arbitrary parallel pair \(p_1,p_2:X_1\rightrightarrows X_0\) and claims that its relation sequence is increasing and has an equivalence relation as its union. For the specific pair from the empty set to \(X_0=\{*\}\), both images in the printed \(R_0\) are empty. Every subsequent relation produced by composition remains empty. The diagonal of this nonempty \(X_0\) is absent. Adding \(\Delta_{X_0}\) to \(R_0\) supplies precisely this required reflexivity.

The composition operation in the recursive formula has the following explicit description. The fibre product

\[
P= (R,\operatorname{pr}_2)\times_{X_0}(R,\operatorname{pr}_1)
\]

maps to \(X_0^3\) by \(((a,b),(b,c))\mapsto(a,b,c)\). Projection back to \(((a,b),(b,c))\) gives its inverse onto the intersection \(\operatorname{pr}_{12}^{-1}R\cap\operatorname{pr}_{23}^{-1}R\). These maps identify the fibre-product subobject with exactly that intersection. The outer-coordinate projection then sends the triple to \((a,c)\). Its image is the composite relation. This constructs the correction replacing the comma by the intersection in OM-SOL-0494.

For the amended \(R_0\), the diagonal is present and the relation is symmetric. The map \((a,b)\mapsto((a,b),(b,b))\) into the composable-pair object places each stage inside the next. Reversal of a triple exchanges its outer coordinates and preserves the relation, so every stage is symmetric. The union contains a composite of any two of its elements because those two elements occur in a common stage and their composite occurs in the next. Thus the added diagonal and the specified composition implement the equivalence closure described by the exercise.

The same outer-coordinate map explains OM-SOL-0495. Take \(X_0=\{0,1\}\) and the total relation \(R=X_0^2\), realized by the two projections from \(X_1=X_0^2\). The fibre product is the eight-element set \(X_0^3\). Its image is the four-element set \(X_0^2\), with the projection forgetting the middle coordinate and having two preimages over each pair. The printed isomorphism to the fibre product fails for this explicit example. The image formula records the actual relation constructed above.

These three repairs form one mathematical construction and should be read together. Each remains a separately identified source record.

Source: `fr/E_corrected_after_scan_check/06/06.tex`, VI Exercise 1.28 and part (b).

### OM-SOL-0496 — VI Exercise 1.28, page 194: unresolved replacement

Over \(\mathbf F_2\), the printed automorphism sends \((x,y)\) to \((x,x+y)\). Applying it twice gives \((x,x+x+y)=(x,y)\). It therefore has finite order over that field, contrary to the surrounding claimed example. The model proposes an entirely new quadratic automorphism. The failed assertion is established by the calculation, while the precise replacement remains an editorial reconstruction. The record stays possible-not-verified.

Source: `fr/E_corrected_after_scan_check/06/06.tex`, VI Exercise 1.28(f), continued on page 194.

### OM-SOL-0546 and OM-SOL-0605 — VI, pages 261 and 325

In Corollary 5.5 the supports are defined using the complements \(Z_i\) of the \(X_i\), and the proof takes the direct limit over these \(Z_i\). The qualifying inclusion applies to the individual closed subsets in the family. This identifies the agreement `contenus` with `fermés` in OM-SOL-0546.

For OM-SOL-0605, the proposed string changes both a parenthesis and the direct/inverse-image mark. Formulas (8.5.2.1), (8.5.2.6), (8.5.2.8), and (8.5.2.9) explicitly construct the colimit of \(\mu_i^*(M_i)\) and identify its Hom into \(N\) with the compatible family of maps \(M_i\to\mu_{i*}N\). The final Hom repeats exactly this object, and its second argument closes with one parenthesis. The surrounding chain verifies both parts of the bundled correction.

Source: `fr/E_corrected_after_scan_check/06/06.tex`, VI Corollary 5.5 and Proposition 8.5.2.

### OM-SOL-0918 — XVII 1.2.6, page 280

The displayed complex has differential \(d_i:A_i\to A_{i-1}\). Exactness at \(A_i\) identifies the kernel of this outgoing map with the image of \(d_{i+1}:A_{i+1}\to A_i\). The corresponding short exact sequence therefore begins with \(\operatorname{Im}(d_{i+1})\). This page is disputed and application is held.

Source: `fr/E_corrected_after_scan_check/17/17.tex`, XVII 1.2.6 and (1.2.6.i).

### OM-SOL-1107 — XVII 5.5.25.3, page 404

Definition 1.1.16 gives the components of both brutal truncations. The subcomplex \(\sigma_{\geq n}K\) agrees with \(K\) in degrees \(i\geq n\) and is zero in smaller degrees. Its quotient in \(K\) is therefore \(K^i\) in degrees \(i<n\) and zero in degrees \(i\geq n\). The quotient map is identity in the former degrees and zero in the latter; its kernel is exactly the specified subcomplex in every degree. This is \(\sigma_{\leq n-1}K\), with the induced differential specified by brutal truncation. The degreewise calculation proves the proposed endpoint.

Source: `fr/E_corrected_after_scan_check/17/17.tex`, XVII 1.1.16 and 5.5.25.3.

### OM-SOL-1326 — XIX, page 603

The open immediately following the divisor equation is obtained by inverting every \(x_i\). A prime belongs to its complement exactly when it contains at least one \(x_i\). Primality makes this equivalent to containing the product \(x_1\cdots x_r\). The complement is thus \(V(x_1\cdots x_r)\), supplying the proposed local equation. The original reported candidate targets the unprimed formula. The explicitly named editorial decision `OM-DEC-1326-PRIMED-PRODUCT` extends the repair to the immediately repeated primed formula, with a separate part and the following proof.

The displayed local ring map \(O_{X,p}\to O_{X',p'}\) sends \(x_i\) to \(x'_i\). For each prime ideal \(\mathfrak q\) of the target, its inverse image contains \(\prod_i x_i\) exactly when \(\mathfrak q\) contains \(\prod_i x'_i\). Thus the inverse image of the unprimed closed subset is \(V(\prod_i x'_i)\). The subsequent displayed open supplies an additional direct check: the \(B'\)-algebra morphism
\[
 B'[1/(\prod_i x'_i)]\longrightarrow B'[1/x'_1,\ldots,1/x'_r]
\]
sends the inverse product to the product of inverses. Its inverse sends \(1/x'_i\) to \((\prod_{j\ne i}x'_j)/(\prod_jx'_j)\). Both composites fix \(B'\) and all these generators, hence are the identity. These explicit inverse morphisms identify the two opens over \(\operatorname{Spec}B'\), with complementary closed subset \(V(\prod_i x'_i)\). The separate canonical change from \(Y\) to \(Y'\) is preserved in its existing branch.

Source: `fr/E_corrected_after_scan_check/19/19.tex`, XIX page 603, the local equations and the ensuing localized opens.

## Reproduction

`build_scripts/judge_misprints.py` combines the original records with the explicitly reviewed ID sets and `build_scripts/one_model_review.json`. It writes the judgment register and application-candidate JSON. It neither changes the input records nor edits the French or English source trees. The source references in the resulting records are relative to the uploaded archive structure.


### OM-SOL-0352 — V 1.10, pages 15–16: first factor of the simplicial products

A further independent reading during the English port settles the previously unverified first index. The source explicitly defines \(\Delta_n=[0,\ldots,n]\). The degree-zero term displayed in (1.10.3) is \(\bigoplus_i A_{U_i}\), whereas a fiber product starting at coordinate 1 has no factors in degree zero and is the final object \(X\) of the slice over \(X\). For example, take the topos of sets, \(X=\{0,1\}\), a singleton index set, and \(U_i=\{0\}\hookrightarrow X\). The printed empty fiber product is \(X\), and its canonical projection to \(X\) is the identity; the required degree-zero object is \(U_i\) with its inclusion into \(X\). These objects have cardinalities 2 and 1, respectively. The map \(U_i\to X\) is the stated inclusion, and no inverse map exists because 1 has no preimage. Thus this reading cannot realize the source's degree-zero term.

The correction starts the product at \(U_{f(0)}\). For a map \(g:\Delta_m\to\Delta_n\), the source defines the associated map on products through the projections indexed by \(f(g(i))\), for every \(i\in\Delta_m\), including 0. This explicitly fixes the first target factor as \(U_{f(g(0))}\). The identical first coordinate is consequently carried through six occurrences: the definition of \(S_n\) on page 15; the product on which \(s(g)\) is restricted; the canonical inclusion into \(S_m\); the source and target products of \(s_f(g)\); and the formula for \(A_n\) in (1.10.2), all on page 16. No other index or formula is changed.

The target of \(s_f(g)\) also carries OM-SOL-0353, the missing closing parenthesis. The exact joint pair retains both defects in the diplomatic branch and repairs the first index and delimiter in the corrected branch. The released English already has coordinate 0 in all six places, so its diplomatic branch must restore coordinate 1 with this source id; its corrected branch retains the released index. Neither page is in the disputed-page list.

Sources: `fr/E_corrected_after_scan_check/05/05.tex`, V 1.10–(1.10.3); `api_pass_20261111/SOL_ONLY_MISPRINTS.json`, record 352.
