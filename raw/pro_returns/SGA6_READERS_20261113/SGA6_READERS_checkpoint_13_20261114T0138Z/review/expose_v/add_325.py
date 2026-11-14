#!/usr/bin/env python3
from review_helpers import Review
r=Review();p=325
r.finding('321_325',27,'The opening de E quotation closure is on325; its E has a short underline.',
 'The complete324 ending and325 opening were compared in both scans. The rule is beneath E alone; the closing quotation and semicolon follow it. The attached form and page marker agree.',
 'actual325 first line, nominal324 finding',witness=336,actual_page=325)
r.finding('321_325',28,'Page325 begins de E followed by the closing quotation and semicolon;324 ends puissances extérieures.',
 'The main and native page boundaries agree. The attached325 marker precedes de and preserves the exact split of the continuing sentence.',
 'page boundary324/325',witness=336)
for index,printed,region in [
 (29,'The E after en ramenant has an individual short underline.','first paragraph, en ramenant E'),
 (30,'The E within (cl(E)−d)+n has an individual short underline; cl and both parentheses are plain.','first paragraph, first class expression'),
 (31,'The E within x=cl(E)−d has an individual short underline; cl and both parentheses are plain.','first paragraph, second class expression')]:
 r.finding('321_325',index,printed,'The native top crop resolves this precise rule independently. The attached scope agrees and preserves the same vector-bundle class introduced on324.',region,witness=336)
r.finding('321_325',32,'The statement underlines Soit, un, anneau, Si on pose, et, alors and donc; formulas, item labels, λ and the connecting hyphen remain plain.',
 'Both scans resolve each of the seven separate lexical groups, including donc after the first substitution identity. The final full stop and colon lie outside the lexical rules. The proposition label follows the accepted bold-label convention.',
 'Proposition3.2 statement and item ii)',verdict='not applied and now applied',change='Restore the seven inspected lexical underline spans.',witness=336)
id='check/findings/findings_321_325.json#32'
for old,new in [
 (r'Soit \(K\) un \(\lambda\)-anneau.',r'\uline{Soit} \(K\) \uline{un} \(\lambda\)-\uline{anneau}.'),
 ('Si on pose ',r'\uline{Si on pose} '),
 (r'\), et \(\gamma_t',r'\), \uline{et} \(\gamma_t'),
 (r'\), alors :',r'\), \uline{alors} :'),
 (r'\text{donc}',r'\text{\uline{donc}}')]:
 r.patch(p,'both',old,new,id,'Preserve the directly observed lexical rule without extending it over the adjacent mathematical tokens.')
r.finding('321_325',33,'On voit donc begins a new indented paragraph after the proposition.',
 'The native top crop shows the indentation and the paragraph spacing. The attached break agrees without a content change.',
 'paragraph after Proposition3.2',verdict='formatting observed; no content error',witness=336)
r.finding('321_325',34,'Démonstration stands alone on its line; i) On a begins the next paragraph, indented.',
 'The native top/lower overlap resolves the separate lines and indentation. The attached break agrees. The word’s actual underline is restored separately under ASTRA-V-PROOF-RULE-325.',
 'proof label and first proof item',verdict='formatting observed; no content error',witness=336)
r.finding('321_325',35,'The dot between λ^n(x) and t^n(1−t)^(−n) is a baseline full stop.',
 'The native lower crop resolves the low mark. It denotes the same coefficient product m_K[[t]](λ^n(x),t^n(1−t)^(−n)); the attached literal period preserves this position and both factors.',
 'first line of proof ii)',witness=336)
r.finding('321_325',36,'On développe begins at the ordinary left margin, continuing proof ii).',
 'Both lower scans show no paragraph indentation at this line. The attached continuation preserves its mathematical tokens and punctuation.',
 'On développe line',verdict='formatting observed; no content error',witness=336)
r.finding('321_325',37,'The dot after λ^n(x) inside the square brackets is a baseline full stop.',
 'The native lower crop resolves the mark before the inner sum. It is the product of the same coefficient λ^n(x) with that formal-series sum; the attached period agrees.',
 'square-bracketed double sum',witness=336)
r.finding('321_325',38,'The first sum in the final line has n=0 below and no printed upper bound.',
 'The main final strip and native lower crop show the clear space above this sum. Retain the attached removal of the unprinted p. The preceding coefficient extraction [t^p] restricts contributions to0≤n≤p because the inner series starts in degree n; that implicit finite range is recorded without inserting a printed upper bound.',
 'final line, first sum',witness=336)
r.finding('321_325',39,'The second sum in the final line also has n=0 below and no printed upper bound.',
 'Both lower scans show its clear upper space. It is the coefficient convolution [t^p](λ_t(x)λ_t(p−1)), whose terms have indices n and p−n. The attached omission of an added p preserves the source’s shorthand for this same finite coefficient sum.',
 'final line, second sum',witness=336)
r.finding('321_325',40,'The dot between λ^n(x) and the binomial coefficient in the final line is a baseline full stop.',
 'The native lower crop resolves the mark independently of the terminal period after λ^p(x+p−1). It denotes multiplication of the two displayed coefficients in K; the attached low period agrees.',
 'final line, first summand',witness=336)
r.finding('321_325',41,'Page325 ends after λ^p(x+p−1) and its full stop;3.3. starts the next printed page.',
 'The complete325 final strip and the main/native326 opening were directly inspected. The attached marker places3.3. at326. Only that next-page boundary is adjudicated here; no full326 review is claimed by this decision.',
 'page boundary325/326',witness=336)
for row in r.decisions:
 if row['source_id']=='check/findings/findings_321_325.json#41':
  row['image']='scan/SGA6_scan_360dpi.pdf#page=339; scan/SGA6_witness_300dpi.djvu#page=336; scan/SGA6_scan_360dpi.pdf#page=340; scan/SGA6_witness_300dpi.djvu#page=337'
r.own_finding('ASTRA-V-ACCENT-325',p,'The quoted verb is printed interprêtera, with a circumflex over e.',
 r'Diplomatic interprêtera; corrected interprétera.',
 'Restore the verb’s acute accent in the corrected layer.',
 'The tight native crop witness_325_accent.png resolves both sides of the roof-shaped accent. The sentence instructs the interpretation of the following proposition by the explicit substitution x=cl(E)−d. Its verb is interpréter, whose corresponding traditional future form is interprétera; the substitution and quoted status remain unchanged.',
 'first paragraph, quoted interprêtera',kind='misprint_in_print',witness=336)
r.patch(p,'current','interprêtera','interprétera','ASTRA-V-ACCENT-325','Correct the observed circumflex to the acute accent in the identified verb.')
r.own_finding('ASTRA-V-PROOF-RULE-325',p,'Démonstration has a horizontal rule beneath its letters; its following full stop is plain.',
 r'\uline{Démonstration}.',
 'Restore the directly observed proof-label underline.',
 'The native top crop resolves the complete word rule and the separate terminal period. The word remains on its own line as already transcribed.',
 'proof label',witness=336)
r.patch(p,'both',r'\emph{Démonstration.}',r'\uline{Démonstration}.','ASTRA-V-PROOF-RULE-325','Preserve the inspected word underline and plain final period.')
r.own_finding('ASTRA-V-SUBSTITUTION-325',p,'The source writes the linear slash forms t/1−t, t/1+t and1/1+t without denominator parentheses.',
 r'Retain the literal forms; identify the substitutions t↦t/(1−t) and t↦t/(1+t).',
 'Retain the observed notation with its exact formal-series maps recorded.',
 'The first proof-ii equality expands the substituted monomial as t^n(1−t)^(−n), fixing the first map σ₋:K[[t]]→K[[t]], f(t)↦f(t/(1−t)). Its inverse is σ₊:f(t)↦f(t/(1+t)), since (t/(1+t))/(1−t/(1+t))=t and (t/(1−t))/(1+t/(1−t))=t. These exact inverse substitutions identify the two displayed λ/γ relations. In proof i), λ_t(−1)λ_t(1)=λ_t(0)=1 and λ_t(1)=1+t identify the printed1/1+t with the inverse series(1+t)^(−1). No denominator punctuation is inserted into the transcribed body.',
 'all slash substitutions and the inverse-series sentence',kind='mathematical_context',verdict='printed reading retained; exact substitution maps recorded',witness=336)
r.own_finding('ASTRA-V-INK-325',p,'A tiny short ink mark lies after λ^n(x+n−1) and before the equality in item i), lower and smaller than the typed terminal full stop.',
 'Retain the existing equality token sequence.',
 'Record the isolated mark physically without assigning an extra mathematical character.',
 'The main_325_identity_dot.png and witness_325_identity_dot.png crops show the mark and the terminal period in the same line for comparison. Its position is below the adjacent formula baseline and its footprint is much smaller. The explicit coefficient equality follows from [t^n](λ_t(x+n)λ_t(−1)) with λ^k(−1)=(−1)^k, as the proof gives. No extra operator is inferred from the isolated ink.',
 'item i), between the left member and equals',kind='damaged_print',verdict='source reading retained with explicit ink observation',witness=336)
r.page(p,'de E followed by the closing quotation','λ^p(x+p−1).',
 'Exact324/325 word boundary and all four E rules, quoted accent, complete proposition and seven lexical rules, every quantifier and the double-stem N, both alternating-sum bounds, all slashed indices, all γ/λ symbols, proof-label rule, complete proof-i convolution and inverse series, every exponent and binomial argument in proof ii), all n≥0/k≥0/p≥n lower bounds, three low product dots, both unbounded-above final sums, physical isolated ink mark recorded without an invented token, and final full stop compared.326 opening checked only for the boundary. No author note.',
 witness='Native witness336 top/lower and tight accent/N/ink crops; witness_325_top.png, witness_325_lower.png, witness_325_accent.png, witness_325_N.png and witness_325_identity_dot.png; main_325_identity_dot.png; boundary-only main326 first strip/native337 top crop')
r.commit()
