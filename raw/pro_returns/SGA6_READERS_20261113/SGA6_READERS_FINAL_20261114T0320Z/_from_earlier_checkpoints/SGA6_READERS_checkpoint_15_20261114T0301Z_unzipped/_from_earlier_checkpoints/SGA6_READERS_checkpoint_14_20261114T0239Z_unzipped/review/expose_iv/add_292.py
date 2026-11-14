#!/usr/bin/env python3
from review_helpers import Review,HERE,underline_statement,underline_words
r=Review();p=292
r.finding('291_295',4,'The heading ends with a bare K and no final stop.',
 'Both the main heading strip and native statement crop show no punctuation after K. The attached layers already omit the added full stop.', 'heading 3.2',witness=303)
r.finding('291_295',5,'The last symbol of the title is K without any lower dot.',
 'Both scans show the bare K. The two constructions named by the title are identified in 3.2.1 and 3.2.3: the former sends a vector-bundle class at Xi to its pullback class at X, while the latter sends a coherent-sheaf class at Xi to its flat pullback class in K_•(X). The latter map is explicitly displayed in the directly consulted 293 middle region. The existing current title spells out that second group as K_•; the diplomatic title preserves the missing mark. No identification between the two K groups is asserted.',
 'last symbol of heading 3.2',witness=303)
r.finding('291_295',6,'X = lim← Xi, without an index beneath lim.',
 'The leftward arrow is clear in the native crop. The subscript i belongs to X; there is no additional index beneath the limit operator.', 'definition of X',witness=303)
r.finding('291_295',7,'lim→ K^•(Xi)_naïf → K^•(X)_naïf, without an index beneath lim.',
 'The native crop resolves the rightward limit arrow, both raised K dots and the two naïf subscripts. Only Xi has an index i.', 'display (3.2.1.1)',witness=303)
r.finding('291_295',8,'l’homomorphisme and est un isomorphisme are underlined; (3.2.1.1) and final stop are plain.',
 'The separate rules and their endpoints are visible in both scans. The source grouping is correct; the explicit underline helper below preserves the actual typography.', 'sentence after (3.2.1.1)',witness=303)
r.finding('291_295',9,'E ≃ f_i^*(E_i) is in the running sentence, followed by a full stop.',
 'The attached inline form agrees with the source. The former display and current inline versions have the identical mathematical sequence E, headless bar-and-tilde sign, f_i^*(E_i), and final stop. This is a layout decision, not a content correction.',
 'bundle descent sentence',verdict='formatting only',change='Retain the attached inline layout with unchanged mathematical tokens and punctuation.',witness=303)
r.finding('291_295',10,'dans lim→ K^•(Xi)_naïf, without a separate limit index.',
 'The handwritten arrow lies under lim; the only i is the subscript of X. The attached source agrees.', 'definition of u(E)',witness=303)
r.finding('291_295',11,'u : ob Loclib(X) → lim K^•(Xi)_naïf, with no index under lim.',
 'The final line has neither a limit index nor an arrow under lim. The index decision is separate from the arrow omission recorded in the next finding.', 'final line',witness=303)
r.finding('291_295',12,'The final target has a plain lim, without its rightward arrow.',
 'The preceding sentence defines u(E) as the image of cl(E_i) in the explicitly rightward limit of (3.2.1.1). Writing G for that same group, its structure map j_i sends cl(E_i) to u(E); the displayed function u:ob Loclib(X)→G has exactly this target. Thus the current rightward limit restores the operator already used in the definition of this same u, while diplomatic preserves the observed absence. No new limit or comparison map is introduced.',
 'target of u in final line',witness=303)
r.source('fixes/RECONCILE_CODEX_6.json#291','l’homomorphisme canonique for f_i:X→X_i.',
 'Both scans explicitly print homomorphisme. The arrow is the specified projection from X=lim←Xi; on each affine chart of the inverse system it is induced by the structure ring homomorphism A_i→colim A_j, and the local maps glue to f_i. The requested word substitution changes no map, source, target, or compatibility f_ij∘f_j=f_i. Preserve the author’s term rather than classify it as a mathematical error.',
 'end of opening paragraph of 3.2',verdict='rejected',change='Retain homomorphisme canonique in both layers.',witness=303,page=p)
r.own_finding('ASTRA-IV-UNDERLINE-292',p,'The continued proposition prose is underlined, with formulas, numerical locators and punctuation plain; the 3.2 lexical title and two assertion spans have rules.',
 r'Word-only \uline spans; plain 3.2. and 3.2.1.; formulas and locator strings unchanged.',
 'Restore the inspected word rules and retain all mathematical tokens.',
 'The complete native statement crop shows the individual rules beneath the prose, including every resp., and the plain III/2.x locators. The heading has rules only beneath Passage à la limite sur and et. The lower assertion has two separate rules. Paragraph numbers are ordinary typed numerals.',
 'continued Proposition 3.1.1, heading 3.2 and assertion after (3.2.1.1)',witness=303)
t=(HERE/'page_292_diplomatic.tex').read_text();start=t.index('un\n');end=t.index('\n\n\\textbf{3.2.')
old=t[start:end];new=underline_statement(old,protected=(r'\((?:III [^)]*|2\.[^)]*)\)',r'[.,;:()]'))
r.patch(p,'both',old,new,'ASTRA-IV-UNDERLINE-292','Restore the directly inspected word rules in the continued proposition; preserve formulas, locators and punctuation.')
for layer,last in [('diplomatic',r'K'),('current',r'K_{\bullet}')]:
 old=r'\textbf{3.2. Passage à la limite sur \(K^{\bullet}_{\naif}\) et \('+last+r'\)}'
 new=r'3.2. \uline{Passage à la limite sur} \(K^{\bullet}_{\naif}\) \uline{et} \('+last+r'\)'
 r.patch(p,layer,old,new,'ASTRA-IV-UNDERLINE-292','Preserve the title’s two lexical rules, plain number, and each layer’s final K reading.')
r.patch(p,'both',r'\textbf{3.2.1.}',r'3.2.1.','ASTRA-IV-UNDERLINE-292','The paragraph number has ordinary typed weight.')
for old in [r"\emph{l'homomorphisme}",r'\emph{est un isomorphisme}']:
 new,n=underline_words(old);assert n==1
 r.patch(p,'both',old,new,'ASTRA-IV-UNDERLINE-292','Use the visible rule rather than italic emphasis.')
r.own_finding('ASTRA-IV-FONT-292',p,'Two O letters are underlined; their X and Xi subscripts are outside the rules.',
 r'\underline O_X and \underline O_{X_i}',
 'Replace the two local calligraphic O forms by the observed underlined O.',
 'Both native lower-page occurrences show a horizontal rule immediately below O, ending before the lower subscript. The bundle symbols E and Ei remain plain.',
 'two locally free module descriptions',kind='font',witness=303)
r.patch(p,'both',r'\mathcal O',r'\underline O','ASTRA-IV-FONT-292','Preserve the two observed underlined O glyphs without extending the rule to a subscript.',count=2)
r.own_finding('ASTRA-IV-NOTATION-292',p,'Eight raised round K dots; the lower dot in the proposition’s alternative K_•; headless E≃f_i^*E_i; all limit indices as observed.',
 r'K^{\bullet}; K_{\bullet}; \simeq; unindexed limit operators.',
 'Retain the attached inspected symbols.',
 'The native crops allow direct comparison between the high round K marks, the lower K dot, the ordinary apostrophes and the handwritten arrows. The two author-omission variants are separately recorded; the page has no footnote.',
 'all K and limit notation',kind='symbol',verdict='confirmed',witness=303)
r.page(p,'un carré cartésien de schémas.','ainsi définie est additive (1.5) ;',
 'Entire continued proposition and its base-change formula, all hypotheses and locators, section and paragraph headings, inverse-limit setup, pullback maps, proof of (3.2.1.1), two underlined O symbols, eight raised K marks and exact final boundary compared. The regional consultation of 293 supports the current title expansion but does not mark 293 fully checked.',
 witness='Native witness 303 statement and limits regions; witness_292_statement.png and witness_292_limits.png')
r.commit()
