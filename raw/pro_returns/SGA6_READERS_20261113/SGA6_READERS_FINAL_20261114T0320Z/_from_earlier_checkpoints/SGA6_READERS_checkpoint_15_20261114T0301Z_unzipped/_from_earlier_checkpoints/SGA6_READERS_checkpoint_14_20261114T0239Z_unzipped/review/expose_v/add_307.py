#!/usr/bin/env python3
from review_helpers import Review,HERE
r=Review();p=307
r.finding('306_310',7,'Φ_{A_g} is above the lower horizontal arrow, as Φ_A is above the upper arrow.',
 'The native top crop shows two plain downward vertical arrows and two rightward horizontal arrows. Both Φ labels stand above their horizontal shafts, with the g a subscript of A. The attached square agrees, including its comma after H∘g(A_g).',
 'square in the proof of 1.9',verdict='formatting observed; map labels retained',witness=318)
r.own_finding('ASTRA-V-GRAMMAR-307',p,'Pour le voir qu’il est injectif, on utilise…',
 "Pour le voir qu'il est injectif",
 'Current only: remove the duplicated object pronoun le.',
 'Both scans plainly type le before voir. The following subordinate clause qu’il est injectif already supplies the direct object of voir; removing le gives the grammatical construction Pour voir qu’il est injectif while keeping every word of the assertion and its proof. The diplomatic layer preserves the printed wording.',
 'first proof sentence',kind='misprint_in_print',witness=318)
r.patch(p,'current',"Pour le voir qu'il est injectif","Pour voir qu'il est injectif",'ASTRA-V-GRAMMAR-307','Remove the redundant le before the explicit que-clause, preserving it diplomatically.')
r.own_finding('ASTRA-V-ABFIL-307',p,'The single Ab fil Hom subscript in Theorem 1.10 has separate rules beneath Ab and fil.',
 r'\Hom_{\underline{\mathrm{Ab}}\,\underline{\mathrm{fil}}}(\Ghat\circ i,H)',
 'Use the observed underlined category name locally.',
 'The native lower crop resolves both letter rules and no full stops. This is the inspected 307 occurrence mentioned in checker306_310#6; no global macro is changed.',
 'Hom subscript in Theorem 1.10',witness=318)
r.patch(p,'both',r'\Abfil',r'\underline{\mathrm{Ab}}\,\underline{\mathrm{fil}}','ASTRA-V-ABFIL-307','Preserve the one inspected category-name occurrence.')
r.own_finding('ASTRA-V-UNDERLINE-307',p,'The opening est un isomorphisme and every lexical span of the 307 portion of Theorem 1.10 are underlined; the intervening proof is plain.',
 r'\uline on the inspected lemma continuation and theorem words, with formulas and punctuation independent.',
 'Render exactly those word rules.',
 'The native top crop shows one rule beneath est un isomorphisme, ending before its stop. The native lower crop shows each theorem span; in K-algèbres the K and hyphen remain outside the word rule, and algèbres is underlined. The C₀ category, H, Hom expression, H(K[X]) and all commas/stops remain outside the lexical rules. This directly checks the 307 portion named in checker306_310#5.',
 'lemma continuation and Theorem 1.10 through associe',witness=318)
r.patch(p,'both','est un\nisomorphisme.',r'\uline{est un'+ '\n'+r'isomorphisme}.','ASTRA-V-UNDERLINE-307','Preserve the initial lexical rule and its plain final stop.')
t=(HERE/'page_307_current.tex').read_text()
old=t.split(r'\textbf{Théorème 1.10.} ',1)[1].strip().replace(r'\Abfil',r'\underline{\mathrm{Ab}}\,\underline{\mathrm{fil}}')
new=r"\uline{Soit} \(H\) \uline{un foncteur sur la catégorie} \(\mathcal C_0\) \uline{des} \(K\)-\uline{algèbres}, \uline{à valeurs dans la catégorie des groupes abéliens filtrés séparés complets}, \uline{et commutant aux invariants sous un groupe fini}. \uline{Alors l'application de} \(\Hom_{\underline{\mathrm{Ab}}\,\underline{\mathrm{fil}}}(\Ghat\circ i,H)\) \uline{dans} \(H(K[X])\) \uline{qui}, \uline{à un morphisme de foncteurs}, \uline{associe}"
r.patch(p,'both',old,new,'ASTRA-V-UNDERLINE-307','Preserve every inspected theorem word span and leave its formula/punctuation boundaries unchanged.')
r.page(p,'est un isomorphisme.','… à un morphisme de foncteurs, associe',
 'All proof prose, both four-term Hom chains and final commas, the plain script-category symbols and Ob capitalization, every g-subscript/hatted G/composition circle, the complete square and its restriction conclusion, and the first portion of Theorem 1.10 compared. No author note.',
 witness='Native witness318 top and lower crops; witness_307_top.png and witness_307_lower.png')
r.commit()
