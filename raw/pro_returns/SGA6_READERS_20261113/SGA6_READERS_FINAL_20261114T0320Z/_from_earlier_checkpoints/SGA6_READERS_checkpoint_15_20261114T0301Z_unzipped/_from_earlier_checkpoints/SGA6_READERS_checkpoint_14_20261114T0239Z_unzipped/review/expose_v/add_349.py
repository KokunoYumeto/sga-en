#!/usr/bin/env python3
from review_helpers import Review,HERE
import json
r=Review();p=349
r.finding('346_350',13,'The page begins an indented paragraph On peut donc.',
 'Main363 top and native360 top confirm the indentation after348 final display. The supplied blank line is retained as layout.',
 '348/349 boundary',witness=360)
r.finding('346_350',14,'A descending comma follows the product defining A-hat^(>=n), before capital On.',
 'Both main second/third strips and native360 top show the small descending mark. The diplomatic comma and corrected sentence-ending period preserve the physical source and the next complete sentence respectively.',
 'after the degree-completion product',witness=360)
r.finding('346_350',15,'The6.5.2 right side ends plus two low dots, then a semicolon.',
 'Both scans resolve exactly two dots. The omitted terms are the higher-degree components of ch(phi)=eta(Log phi), with degree-n coefficient(-1)^(n-1)a_n/(n-1)!. Thus the current three-dot ellipsis denotes the same full higher-degree tail, while diplomatic retains the two physical dots.',
 '6.5.2 tail',witness=360)
r.finding('346_350',16,'The6.5.3 right side ends plus two low dots, then a comma.',
 'The main third strip and native360 lower resolve exactly two tail dots. These denote terms of degree greater than m+n after the displayed leading product coefficient. Retain diplomatic two dots and the current complete ellipsis, whose low placement is separately restored.',
 '6.5.3 tail',witness=360)
r.own_finding('ASTRA-V-UNDERLINE-349',p,
 'Definition6.4 has three lexical rule groups; Proposition6.5 has seventeen, with its formulas, item labels and K-hyphen independent.',
 'Use twenty explicit word-rule groups in those two statements.',
 'Restore the observed lexical emphasis without altering any formula or the branch-specific punctuation.',
 'All rules were resolved in main363 and native360 top/lower. Definition: L homomorphisme;qui vient d etre;defini s appelle caractere de Chern. Proposition introduction: Soit;une;algebre graduee;considerons sur;la filtration definie comme suit;filtration par le degre;ou;On a les congruences suivantes. Item i:Soient;et;posons;alors. Item ii:Soient;posons;alors. Conclusion:et par suite;la filtration par le degre est une filtration d anneau. The proof and the inverse-map paragraph are plain.',
 'Definition6.4 and complete Proposition6.5 statement',witness=360)
for layer in ('diplomatic','current'):
 t=(HERE/f'page_349_{layer}.tex').read_text()
 old=t.split(r'\textbf{Définition 6.4.} ',1)[1].split('\n\nSi ',1)[0]
 new=old.replace("L'homomorphisme",r"\uline{L'homomorphisme}").replace("qui vient d'être",r"\uline{qui vient d'être}").replace(r"défini s'appelle \emph{caractère de Chern}",r"\uline{défini s'appelle caractère de Chern}")
 assert new.count(r'\uline{')==3
 r.patch(p,layer,old,new,'ASTRA-V-UNDERLINE-349','Preserve the three Definition6.4 word rules.')
 old=t.split(r'\textbf{Proposition 6.5.} ',1)[1].split('\n\\end{enumerate}',1)[0]
 new=old
 pairs=[('Soit ',r'\uline{Soit} '),(r'\(A\) une ',r'\(A\) \uline{une} '),
  (r'\(K\)-algèbre graduée',r'\(K\)-\uline{algèbre graduée}'),
  ('considérons sur',r'\uline{considérons sur}'),
  ('la filtration définie comme suit',r'\uline{la filtration définie comme suit}'),
  ('(filtration par le degré)',r'(\uline{filtration par le degré})'),
  ('où ',r'\uline{où} '),('On a les congruences suivantes',r'\uline{On a les congruences suivantes}'),
  (r'\item Soient',r'\item \uline{Soient}'),(', et ',r', \uline{et} '),
  ('posons',r'\uline{posons}'),('alors :',r'\uline{alors} :'),
  ('et par suite,',r'\uline{et par suite},'),
  ("la filtration par le degré est une filtration d'anneau.",r"\uline{la filtration par le degré est une filtration d'anneau}.")]
 for a,b in pairs:
  n=2 if a in (r'\item Soient','posons','alors :') else 1
  assert new.count(a)==n,(layer,a,new.count(a),n)
  new=new.replace(a,b)
 assert new.count(r'\uline{')==17
 r.patch(p,layer,old,new,'ASTRA-V-UNDERLINE-349','Preserve the seventeen Proposition6.5 lexical rules with math and branch punctuation unchanged.')
r.own_finding('ASTRA-V-ELLIPSES-349',p,
 'The three complete source ellipses in the item premises are low; the two formula tails are separately decided literal two-dot marks.',
 r'Use \ldots for three diplomatic/five corrected complete ellipses.',
 'Preserve the observed baseline of the complete ellipses.',
 'The native lower crop resolves the three full premise ellipses and the two literal tail variants. No product-period control is involved.',
 'Proposition6.5 premises and formula tails',kind='symbol',witness=360)
r.patch(p,'diplomatic',r'\cdots',r'\ldots','ASTRA-V-ELLIPSES-349','Preserve three complete low source ellipses.',count=3)
r.patch(p,'current',r'\cdots',r'\ldots','ASTRA-V-ELLIPSES-349','Preserve five low complete ellipses including the corrected tail forms.',count=5)
r.own_finding('ASTRA-V-INK-MARK-349',p,
 'A small detached ink mark lies just beyond the6.5.3 fraction-bar endpoint, at bar height and over the final denominator factorial; a larger separate product dot precedes a_m.',
 'Retain the existing single multiplication period; record the extra physical mark without assigning a second punctuation token.',
 'Keep the mathematical token sequence unchanged and preserve the evidence-limited physical observation.',
 'Main main_349_product_mark.png and native witness_349_product_mark_zoom.png both show the mark. It is smaller than the following complete product dot. The images do not establish a second complete punctuation glyph, and no physical cause is asserted. The coordinator independently viewed both crops and reached the same limited glyph decision. The exact leading coefficient is c_m c_n/c_(m+n)=-(m+n-1)!/((m-1)!(n-1)!), c_r=(-1)^(r-1)/(r-1)!, multiplying a_m b_n once; the full comparison is saved in identification_349.json.',
 '6.5.3 fraction-bar endpoint and following product',kind='damaged_or_extra_ink',verdict='source retained; physical mark explicitly recorded',witness=360)
r.own_finding('ASTRA-V-Q-FORMS-349',p,
 'The two Q subscripts and the inline Q in Q-algebre have inner reinforcing strokes; the inline stroke is partly joined to its outer loop.',
 r'Retain the three \mathbb Q occurrences.',
 'Confirm these actual local number-ring forms.',
 'Both native tight Q crops, viewed at nearest-neighbour enlargement, resolve the inner stroke in the inline Q and the separated vertical inner stroke in the definition subscript. The main/native page views resolve the first subscript. The prose explicitly specifies Q-algebra in its parenthesis; the inverse is checked under that stated rational-algebra scope, with eta multiplying each positive-degree coordinate by the nonzero rational(-1)^(r-1)/(r-1)!.',
 'two completed rational targets and Q-algebra parenthesis',kind='convention',verdict='confirmed',witness=360)
packet={
 'record_type':'exact_identification','page':p,'source_id':'ASTRA-V-INK-MARK-349',
 'image':['scan/SGA6_scan_360dpi.pdf#page=363','scan/SGA6_witness_300dpi.djvu#page=360'],
 'physical_observation':'Small detached mark at fraction-bar height beyond its endpoint, above the final denominator factorial; separate larger product period before a_m. No second complete punctuation glyph is established; physical cause unassigned.',
 'coefficient_comparison':{
  'map':'ch=eta∘Log; eta restricts in degree r>=1 to multiplication by c_r=(-1)^(r-1)/(r-1)!.',
  'input_leading_terms':'For phi=1+a_m+higher and psi=1+b_n+higher, ch(phi)=c_m a_m+higher and ch(psi)=c_n b_n+higher.',
  'multiplication':'The proved multiplicativity gives ch(phi*psi)=ch(phi)ch(psi). The first possible nonconstant component has degree m+n.',
  'exact_scalar':'Writing d_(m+n) for that component of phi*psi, c_(m+n)d_(m+n)=c_m c_n a_m b_n. Thus d_(m+n)=-(m+n-1)!/((m-1)!(n-1)!) a_m b_n.',
  'integral_descent':'This comparison is performed first in the rational extension of the universal polynomial ring with independent homogeneous input coefficients. Its integral polynomial ring injects into that extension. The displayed integer scalar equals-(m+n-1)binom(m+n-2,m-1), so equality descends there and then along the evaluation homomorphism sending the independent input coefficients to the given a_i,b_j. This preserves the single multiplication in the source formula.'},
 'filtration_identification':'The printed shorthand0×1+A-hat^(>=n) is the image of u↦(0,1+u), u in product_(i>=n)A^i, in K×I(A). The symbols phi and psi in the next lines use the inverse second-coordinate projection on this image.',
 'inverse_map':'Under the explicitly printed Q-algebra scope, ch(a,phi)=a+eta(Log phi) has inverse a+psi1↦(a,exp(eta^(-1)psi1)). On degree r, eta^(-1) multiplies by(-1)^(r-1)(r-1)!, and completed Log/exp compose to the identity. Both compositions retain the same scalar a.',
 'disposition':'No new punctuation token or replacement theorem. Preserve the observed mark in the evidence and the existing single-product formula in both layers.'
}
(HERE/'identification_349.json').write_text(json.dumps(packet,ensure_ascii=False,indent=2)+'\n')
r.page(p,'On peut donc','de la congruence...on deduit',
 'Full main363 four strips and native360 top/lower compared. Checked6.3.3, Definition6.4 and its three rules, three reinforced Q forms with native tight enlargements, the explicit Q-algebra parenthesis and wavy inverse arrow, all eta/Log/exp parentheses, seventeen Proposition6.5 word groups, typed lower-o/0 convention,6.5.1 with its literal unparenthesized set shorthand, product lower bound i>=n, descending comma before On, all item indices and factorials, three full premise ellipses/two two-dot tails, additional fraction-bar-level ink with two tight views and independent review, and the plain proof continuation. No author note.',
 witness='Native360 top/lower; Q_inline/Q_index crops and zooms; product_mark crop and zoom with corresponding main tight view.')
r.commit()
