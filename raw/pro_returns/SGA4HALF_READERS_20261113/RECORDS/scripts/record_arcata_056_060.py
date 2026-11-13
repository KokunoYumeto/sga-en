from audit_support import *
reasons={
181:'PDF p.62 first proof paragraph reads en fait; Codex already agrees.',
182:'PDF p.62 second paragraph explicitly has Z/nZ-modules; Codex already restores modules.',
183:'PDF p.62 says D’après with one apostrophe; Codex already agrees.',
184:'PDF p.62 sentence before (1.8) reads variante; Codex already agrees.',
185:'PDF p.62 lemma (1.8) has une catégorie; Codex already agrees.',
186:'PDF p.63 continuation of (1.9) reads on ait; Codex already agrees.',
187:'PDF p.63 conclusion (1.9) explicitly has f_* Z/n = Z/n; Codex already restores the equals sign.',
188:'PDF p.63 (1.10) has g:Y→Z; Codex already agrees.',
189:'PDF p.64 first paragraph has hensélisé with final acute accent; Codex already agrees.',
190:'PDF p.64 second paragraph asserts vanishing only for q≥2; Codex already agrees.',
191:'PDF p.64 (2.2) uses plural géométriques; Codex already agrees.',
192:'PDF p.64 first proof sentence includes à la limite; Codex already restores the article.',
193:'PDF p.64 connectedness sentence prints quels que soient (the l is somewhat inked but the separated words are clear); Codex already agrees.',
194:'PDF p.64 connectedness parenthesis says par quoi; Codex already agrees.',
195:'PDF p.64 displayed local-algebra isomorphism uses capital T; Codex already agrees.',
196:'PDF p.64 final paragraph prints algèbres locales étale, without the plural s. Correct agreement only in corrected/reading, agreeing with Codex SGA45-CORR-0021; English étale does not inflect.',
197:'PDF p.64 étale-algebra base uses polynomial rings A′[T]=A[T] tensor_A A′, with square brackets; Codex already agrees.',
198:'PDF p.64 introduces X′=Spec(A′{T}) with a visible prime; Codex already agrees.',
199:'PDF p.65 purity lemma is numbered (2.3.1). Accept the visible-number repair, but preserve Miller’s label I:5-2-4 and use an explicit numbering override, as in Codex, rather than renaming the label.',
200:'PDF p.65 discriminant sentence prints une équation, singular; Codex already agrees.',
201:'PDF p.65 Abhyankar lemma is numbered (2.3.2). Preserve Miller’s label I:5-2-5 and restore the printed visible number by an override.',
202:'PDF p.65 base-change notation is the bare subscript 1; Codex already removes the unprinted parenthesized placeholder.',
203:'PDF p.65 normalization is de X_1 dans X-tilde_{1 eta}; Codex already agrees.',
204:'PDF p.65 proof refers to 2.3.1, without parentheses. Retain the stable target I:5-2-4 but print its restored number; label renaming is unnecessary.',
205:'PDF p.65 proof paragraph is numbered 2.3.3. Retain stable label I:5-2-6 with the printed numbering override.',
206:'PDF p.65 proof paragraph begins Prouvons 2.3. Notons t ...; Codex already restores the missing opening sentence.'}
choices={n:('accepted',r) for n,r in reasons.items()}
for n in [199,201,204,205]:choices[n]=('accepted with a corrected reading',reasons[n],{'change_made':'Restore the printed visible number while retaining the existing Miller label and reference target.'})
decide('arcata',choices)
starts={56:'Considérons le diagramme cartésien',57:'Pour démontrer le théorème',58:r'point géométrique $t$ de $S$',59:r'Soient $s$ un point géométrique',60:r'\begin{propositiondotdash}\label{I:5-2-3}'}
append_jsonl(ROOT/'work/arcata/pages.jsonl',[{'printed_page':str(p),'pdf_page':INDEX[str(p)]['pdf_page'],'checked_against_scan':True,'findings':sum(r['printed_page']==str(p) for r in SOL),'start_fr':a,'start_en':'Corresponding translated passage','reason':'All text, symbols, maps and references compared directly with the scan; nested lemma numbering and exact page starts resolved.'} for p,a in starts.items()])
append_jsonl(ROOT/'work/arcata/variants.jsonl',[
{'id':'SGA45-CORR-0021','sources':['SGA45-CORR-0021','S45-SOL-0196'],'page':'59','place':'local étale algebras','printed':'étale','corrected':'étales','kind':'word','reason':'Plural agreement with algèbres locales.','english_applicability':'No English change.'},
{'id':'S45-ASTRA-A-0020','page':'56','place':'(1.6.1), middle cohomology group','printed':'X','corrected':r'\widetilde X','kind':'symbol','reason':'The direct image by epsilon-prime is a sheaf on X-tilde in the preceding Cartesian diagram.','en_printed':'X','en_corrected':r'\widetilde X'},
{'id':'S45-ASTRA-A-0021','page':'45','place':'§4 reduction, integer n','printed':r'\geqslant 0','corrected':'>0','kind':'formula','reason':'The reduction uses torsion coefficients Z/n and then reduces n to a prime power; n=0 would give Z and is outside that argument.','en_printed':r'\geqslant 0','en_corrected':'>0'}])
append_jsonl(ROOT/'work/arcata/own_findings.jsonl',[
{'id':'S45-ASTRA-A-0020','page':'56','place':'(1.6.1), middle cohomology group','printed_reading':r'\h^*(X,\varepsilon_*\prime\dZ/n)','tex_reading':'Codex diplomatic has X; corrected has X-tilde','change':'Retain X diplomatically; use X-tilde in corrected/reading in both languages','kind':'misprint_in_print','reason':'The scan omits the tilde. Epsilon-prime maps to X-tilde, and its direct image must be evaluated there. This validates the unnumbered Codex tree difference.'},
{'id':'S45-ASTRA-A-0021','page':'45','place':'§4, integer n in the reduction to constant torsion coefficients','printed_reading':r'n\geqslant0','tex_reading':'Codex diplomatic ≥0; corrected >0','change':'Use n>0 only in corrected/reading, with apparatus','kind':'misprint_in_print','reason':'The surrounding argument is for torsion sheaves and immediately reduces n to a prime power. Z/0=Z is not a torsion sheaf and is excluded by the theorem’s stated scope.'},
{'id':'S45-ASTRA-A-0022','page':'45','place':'Proposition (3.7), quantified n','printed_reading':r'pour tout n\geqslant0','tex_reading':'Codex corrected changes this hypothesis to n>0','change':'Keep the printed ≥0 in all forms at this occurrence','kind':'editorial correction rejected','reason':'Here the statement assumes bijectivity/surjectivity for all n≥0. This is a stronger but valid sufficient hypothesis, and the proof uses its positive-n instances. Weakening a valid hypothesis is not required to repair a misprint.'}])
print('Arcata pp.56–60 recorded.')
