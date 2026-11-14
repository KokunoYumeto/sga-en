#!/usr/bin/env python3
from review_helpers import Review
r=Review();p=298
r.finding('296_300',11,'abéliens, de la façon suivante… begins this page.',
 'The complete main first strip and native top crop start with abéliens; the previous page ends at groupes. The attached marker already follows that exact split.',
 'page start',witness=309)
for n,region in [(12,'first formal-series expansion'),(16,'series in the representing-map construction'),(17,'definition of the universal series in the last paragraph')]:
 r.finding('296_300',n,'Two groups of three baseline full stops in this series.',
  'Both scans place all six stops on the baseline. The attached ldots groups preserve their height and the coefficient/exponent sequence; no additional series index is supplied.',
  region,witness=309)
r.finding('296_300',13,'K-Alg.fil. and Ab are independently underlined in the functor display.',
 'The native top crop shows a rule beneath the complete K-Alg.fil. name, including its punctuation, and another beneath Ab. The K-Alg.fil. subscript of Hom below has no underline and is retained as plain text.',
 'functor display and Hom subscript comparison',witness=309)
r.finding('296_300',14,'Le foncteur and est représentable are underlined; the intervening Ĝ_K and final stop are plain.',
 'The main lemma strip and native crop show the two separate word rules. The displayed mathematical functor remains outside both rules. Apply the statement formatting only to this inspected lemma.',
 'Lemma 1.2 statement',verdict='confirmed; now rendered with literal word rules',witness=309,
 change='Underline the two inspected lexical spans, with formula and final stop outside.')
r.patch(p,'both',r'\textbf{Lemme 1.2.} Le foncteur \(\Ghat_K\) est représentable.',r'\textbf{Lemme 1.2.} \uline{Le foncteur} \(\Ghat_K\) \uline{est représentable}.','check/findings/findings_296_300.json#14','Preserve the two visible word rules and their endpoints.')
r.finding('296_300',15,'An ordinary capital N follows the membership sign in the index of (Xi).',
 'The native lemma crop shows the membership sign touching the left stem of N. The N itself has ordinary single strokes and serifs, with no extra vertical or diagonal stroke and no lower rule. Retain the attached plain N in both layers for this occurrence.',
 'indexing set in the first proof sentence',witness=309)
r.own_finding('ASTRA-V-PHI-298',p,'The universal-series phi has a closed oval crossed by a central vertical descender.',
 r'\phi=1+X_1t+\ldots+X_nt^n+\ldots',
 'Use the closed-oval phi form for this one observed occurrence.',
 'The enlarged main crop and native witness_298_phi.png show the closed oval and central stem. The attached varphi selects an open-left cursive shape; the local phi replacement preserves the very same formal series with coefficients Xi. No macro-wide Greek-letter substitution is made, and the separate psi symbols remain unchanged.',
 'On pose… in the last paragraph',kind='font',witness=309)
r.patch(p,'both',r'\varphi=1+X_1t',r'\phi=1+X_1t','ASTRA-V-PHI-298','Preserve the closed-oval phi glyph observed in this definition.')
r.own_finding('ASTRA-V-NOTATION-298',p,'Eight hatted G symbols, script C in Ob(C), capital O and lowercase b in Ob, capital F in Fil, and a headed tilde-labelled bijection arrow.',
 r'\Ghat; \mathcal C; \operatorname{Ob}; \Fil; \xrightarrow{\sim}.',
 'Retain the inspected notation.',
 'The native top and lemma crops resolve the hats, subscript K positions, script category letter, capitalized operator names, double square brackets, superscript plus, both ≥ signs in the proof, and the actual arrowhead of the representing bijection. The initial quantifier and condition i≥1 are also present. No author note appears.',
 'all formulas and operator names',kind='symbol',verdict='confirmed',witness=309)
r.page(p,'abéliens, de la façon suivante…','il existe un homomorphisme et un seul',
 'Complete prose, all three series expansions, condition (1.1.1), every coefficient and exponent, eight hatted G occurrences, category rules and plain Hom subscript, lemma word rules, ordinary N and the closed universal-series phi compared. No author footnote.',
 witness='Native witness309 top, lemma and phi crops; witness_298_top.png, witness_298_lemma.png and witness_298_phi.png')
r.commit()
