#!/usr/bin/env python3
from review_helpers import Review,HERE
r=Review();p=301
r.finding('301_305',1,'H(K[X₁,…,X_n]) d’après (1.3.ii)). is the whole first line.',
 'Both scans continue the sentence from 300 directly with this subgroup. There is no extra invariant expression or isomorphism sign here. The attached layers already remove those interpolated mathematical tokens and put the page marker at the actual first expression.',
 'page start',witness=312)
for n,region,printed in [(2,'after the first line','Remarquons enfin… begins a new paragraph.'),(5,'universal-series sentence','The universal series and Le diagramme commutatif : run in the same paragraph.'),(8,'after the square and its conclusion','Or φ… begins a new paragraph.')]:
 r.finding('301_305',n,printed,
  'The complete main strips and native crops confirm this placement. The attached formatting already agrees. The paragraph/inline distinction by itself changes no mathematical token or punctuation, so no new content patch is introduced.',
  region,verdict='formatting observed; no content error',witness=312,change='Retain attached layout; mathematical token sequence and punctuation unchanged.')
r.finding('301_305',3,'son image est le sous groupe de, without a hyphen.',
 'The native theorem crop has an uninterrupted word rule beneath sous groupe but no character between the two words. Retain this source spelling diplomatically and the established French compound sous-groupe in current, matching its correctly typed use on 299 and 300.',
 'theorem statement',witness=312,change='Retain the existing sous groupe/sous-groupe layer distinction.')
r.finding('301_305',4,'The Hom subscript is Ab fil, with separate rules beneath Ab and fil and no stops.',
 'Both scans resolve these two subscript rules independently of the theorem word rules. Replace this one local Abfil use by its explicit inspected form. Other pages are not decided by this observation; no chapter-wide macro replacement is made.',
 'Hom subscript in Theorem 1.6',verdict='confirmed locally; scope amended',witness=312,
 change='At this occurrence only, Abfil→underlined Ab and underlined fil.')
r.patch(p,'both',r'\Hom_{\Abfil}(\Ghat_K,H)',r'\Hom_{\underline{\mathrm{Ab}}\,\underline{\mathrm{fil}}}(\Ghat_K,H)','check/findings/findings_301_305.json#4','Preserve the two observed subscript rules locally.')
r.finding('301_305',6,'Le diagramme commutatif : includes a colon.',
 'Both scans show the colon before the square. It is already present in both attached layers.',
 'introduction to (1.6.1)',witness=312)
r.finding('301_305',7,'u_H^n is above the lower horizontal arrow; both Φ labels are outside the square.',
 'The complete native square shows rightward horizontal arrows and downward vertical arrows, with the upper and lower u labels above their shafts. The attached labels and arrow endpoints agree. The inherited placement adjustment does not change the maps or the commutative-square relation.',
 'diagram (1.6.1)',verdict='formatting observed; map labels retained',witness=312)
r.own_finding('ASTRA-V-UNDERLINE-301',p,'Theorem 1.6 underlines its lexical word groups; formulas, the reference 1.4., parentheses, commas, semicolon and colon remain outside those rules.',
 r'\uline word spans in Theorem 1.6, with independently underlined Ab and fil in its Hom subscript.',
 'Render the inspected theorem word rules explicitly in each layer.',
 'The main first two strips and native theorem crop show every span from L’application de through pour les. The proof prose is plain. The two displayed conditions are mathematical statements without additional word rules; their full stops are present. The label follows the accepted bold-label convention.',
 'Theorem 1.6 statement before conditions i) and ii)',witness=312)
for layer in ['diplomatic','current']:
 text=(HERE/f'page_{p}_{layer}.tex').read_text()
 old=text.split(r'\textbf{Théorème 1.6.} ',1)[1].split('\n\\[',1)[0]
 old=old.replace(r'\Hom_{\Abfil}',r'\Hom_{\underline{\mathrm{Ab}}\,\underline{\mathrm{fil}}}')
 subgroup='sous groupe' if layer=='diplomatic' else 'sous-groupe'
 new=r"\uline{L'application de} \(\Hom_{\underline{\mathrm{Ab}}\,\underline{\mathrm{fil}}}(\Ghat_K,H)\) \uline{dans} \(H(K[X])\) \uline{qui}, \uline{à un morphisme de foncteurs}, \uline{associe sa valeur sur l'élément} \(1+Xt\) \uline{de} \(\Ghat_K(K[X])\), \uline{est injective}; \uline{son image est le "+subgroup+r" de} \(H(K[X])\) \uline{formé des éléments} \(\theta\) \uline{tels que} (\uline{avec les notations de} 1.4. \uline{pour les} \(f_n\))~:"
 r.patch(p,layer,old,new,'ASTRA-V-UNDERLINE-301','Preserve the observed word-rule endpoints while leaving formulas and punctuation independent.')
r.own_finding('ASTRA-V-ELLIPSES-301',p,'Six groups of baseline full stops occur in the expanded universal-series expressions.',
 r'\ldots in the initial product expansion, the two groups in the universal-series definition, the square’s conclusion, and the two expansions in the Or paragraph.',
 'Replace these six local cdots groups by ldots.',
 'The native theorem and proof crops resolve all six groups at the baseline: one before the theorem, two in the defining series, one after the square, and two in the congruence paragraph. The sentence-ending stop after the infinite series remains separate.',
 'all six expanded-series ellipses',kind='symbol',witness=312)
r.patch(p,'both',r'\cdots',r'\ldots','ASTRA-V-ELLIPSES-301','Preserve the six observed baseline ellipses.',count=6)
r.own_finding('ASTRA-V-PHI-301',p,'All five lowercase phi forms have an open upper-left curve beside a descending right loop; the uppercase Φ forms have a central stem through an oval.',
 r'\varphi in all five occurrences; \Phi for the natural transformation.',
 'Retain these locally observed phi forms.',
 'The native theorem and proof crops, including witness_301_phi_forms.png, resolve the opening in the left curve. These page-301 shapes support the attached varphi. The closed-oval form observed on 298–299 was decided separately and is not imposed on this page. The same universal series and natural transformation are identified by their printed arguments and definitions, without changing their mathematical referents.',
 'universal-series definition and congruence paragraph',kind='font',verdict='confirmed',witness=312)
r.page(p,'H(K[X₁,…,X_n]) d’après (1.3.ii)).','Soit maintenant Φ un élément quelconque de Hom(Ĝ,H), et soit',
 'Complete prose, initial product bounds, theorem and both conditions, all four square objects and labels, all congruences and their filtration exponents, six baseline ellipses, five local lowercase phi forms and all uppercase Φ forms compared. The local Hom subscript and statement rules are explicit. No author note.',
 witness='Native witness312 theorem and proof crops; witness_301_theorem.png, witness_301_proof.png and witness_301_phi_forms.png')
r.commit()
