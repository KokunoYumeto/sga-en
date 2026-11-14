#!/usr/bin/env python3
from review_helpers import Review
r=Review();p=311
r.finding('311_315',1,'Page311 begins 1+X de 1+completed K[X]⁺ est injective.',
 'The main first strip and witness322 top crop begin with this complete expression. Page310 was fully checked through the preceding word élément. The attached boundary agrees with both scans.',
 'page start',witness=322)
r.finding('311_315',2,'The first K[X₁,…Xₙ] has a comma after X₁ but none after the three baseline dots; the later four polynomial lists have both commas.',
 'The native top crop resolves the first list exactly as printed. The later quotient has three complete lists and the following membership formula has a fourth, each with the second comma. The repaired expression denotes the same polynomial algebra in the listed generators X₁ through Xₙ, with its missing separator restored. The attached diplomatic omission and corrected comma agree.',
 'Théorème1.13(ii), final polynomial list',witness=322)
r.finding('311_315',3,'H(B) is followed by a right-headed arrow with a separate tilde above the shaft.',
 'The native tight crop witness_311_lim.png resolves the small right arrowhead and the separate wavy upper mark. The attached xrightarrow{sim} preserves these two components.',
 'Remarque1.14, inverse-limit display',witness=322)
r.finding('311_315',4,'Lim has capital L, a left arrow directly below the word, and n below that arrow.',
 'The native tight crop resolves all three vertically arranged parts. The attached underleftarrow Lim with its lower index reproduces the observed form.',
 'Remarque1.14, inverse-limit display',witness=322)
for n,printed,region in [(5,'Immédiat à partir de1.6 et1.12. is a separate indented paragraph.','after the theorem conditions'),(6,'Pour se donner un morphisme de foncteurs… is a separate indented paragraph.','after the membership display')]:
 r.finding('311_315',n,printed,
  'The complete main page and native crop show the stated indentation. The attached paragraph break already agrees; this observation changes no mathematical token or punctuation.',
  region,verdict='formatting observed; no content error',witness=322)
r.finding('311_315',7,'On311 the rules cover est injective; son image est le sous-groupe de; formé des éléments; tels que; and notations de.',
 'Every lexical span of the theorem continuation on311 has been compared directly in both scans. Its formulas, semicolon, opening parenthesis, references1.4/1.5 and final colon are plain. The314/315 portions of this multi-page finding remain outside this record’s current inspected scope and will be separately adjudicated when those pages are read.',
 '311 theorem continuation only',verdict='311 scope confirmed and applied; later listed pages not yet adjudicated',change='Apply the five inspected word-group rules on311.',witness=322)
r.patch(p,'both',"est\ninjective; son image est le sous-groupe de \\(H(K[X])\\) formé des éléments \\(\\theta\\) tels que (notations de 1.4,1.5)~:",r"\uline{est injective}; \uline{son image est le sous-groupe de} \(H(K[X])\) \uline{formé des éléments} \(\theta\) \uline{tels que} (\uline{notations de} 1.4,1.5)~:",'check/findings/findings_311_315.json#7','Preserve the five inspected lexical rules and plain adjacent mathematics/punctuation.')
r.own_finding('ASTRA-V-ABFIL-311',p,'All three Ab fil names in1.15 have separate underlines under Ab and fil, without dots.',
 r'\underline{\mathrm{Ab}}\,\underline{\mathrm{fil}} at all three inspected targets.',
 'Render these three category names explicitly.',
 'The native lower crop resolves all six word rules in the successive targets of the three displayed functor categories. These usages are individually checked, extending the previously decided nine names on306–310.',
 '1.15, first line',witness=322)
r.patch(p,'both',r'\Abfil',r'\underline{\mathrm{Ab}}\,\underline{\mathrm{fil}}','ASTRA-V-ABFIL-311','Preserve the three observed category forms.',count=3)
r.own_finding('ASTRA-V-PLACEHOLDER-311',p,'The two completion-placeholder dots are baseline stops, one in the Pour se donner paragraph and one in the final parenthesized k-fold expression.',
 r'\,\mathord{.}\, replaces \,\cdot\, at these two inspected placeholders.',
 'Restore their baseline height.',
 'The native lower crop resolves both low dots under their completion hats, below the plus-sign midline. Each keeps the same unspecified functor argument and the same map into H; the second expression retains its surrounding parentheses and power k.',
 'last two paragraphs',kind='symbol',witness=322)
r.patch(p,'both',r'\,\cdot\,',r'\,\mathord{.}\,','ASTRA-V-PLACEHOLDER-311','Preserve the two low placeholder dots.',count=2)
r.own_finding('ASTRA-V-FONT-311',p,'The three category G letters have connected descenders; the first two source categories in1.15 are script C and script C with a typed lower o; the number1.15. is plain.',
 r'Retain the three \mathcal G forms, \mathcal C and \mathcal C_0 under the accepted o/0 convention; render1.15. without bold.',
 'Retain the inspected category forms and restore the plain paragraph number.',
 'The native top crop resolves the two G descenders in the remark and Ob expression; the lower crop resolves the third G beside the C and C_o sources in1.15. All word-level rules are confined to the theorem continuation and category targets; the remark and1.15 prose are plain. The capital Ob is directly printed.',
 'remark category forms and1.15 first line',kind='font',witness=322)
r.patch(p,'both',r'\textbf{1.15.}','1.15.','ASTRA-V-FONT-311','Preserve the inspected plain paragraph number.')
r.page(p,'1+X de1+completed K[X]⁺ est injective','un morphisme de foncteurs. Nous avons vu',
 'Complete theorem continuation, both conditions and quantifiers, baseline polynomial dots and the printed missing comma, proof references, both hatted G occurrences, entire remark with inverse-limit arrow and lower index, all B≥n and product i≥n bounds, quotient map and its semicolon, both equalities with p_n, membership formula and stop, two completion placeholders, all1.15 source/target categories and powers k, and final page words compared. No author note.',
 witness='Native witness322 top/lower crops and tight inverse-limit crop; witness_311_top.png, witness_311_lower.png, witness_311_lim.png')
r.commit()
