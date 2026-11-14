#!/usr/bin/env python3
from review_helpers import Review
r=Review();p=314
r.finding('311_315',23,'A colon follows de groupes abéliens before the first displayed map.',
 'The main first strip and native top crop resolve the two vertically aligned points after abéliens. The attached colon agrees.',
 'Définition2.1, before λ_t display',witness=325)
r.finding('311_315',24,'The line λ_t(x)=1+xt+… ends with its three baseline dots and no fourth sentence stop.',
 'The native top crop shows exactly three separated low dots. The attached deletion of the additional full stop agrees.',
 'end of definition statement',witness=325)
r.finding('311_315',25,'The three dots after 1+xt+ lie on the baseline.',
 'Both scans place the dots below the plus-sign midline; the attached ldots form agrees.',
 'end of definition statement',witness=325)
r.finding('311_315',26,'The sum has ∞ above and i≥0 below.',
 'The native top crop and tight sum crop resolve the upper infinity sign and the two lower strokes of ≥. The attached sum includes both limits. The nearest-neighbour inspection enlargement adds no image detail; it makes the existing lower strokes easier to compare.',
 'On posera formula',witness=325)
r.finding('311_315',27,'Only homomorphisme is underlined in λ-homomorphisme; λ, the hyphen and following comma are plain.',
 'The native top crop resolves the rule beginning after the hyphen and ending before the comma. The inherited emph span has the correct endpoint; explicit uline now supplies the observed rule.',
 'defined term before the square',verdict='span confirmed; explicit underline applied',witness=325)
r.patch(p,'both',r'\emph{homomorphisme}',r'\uline{homomorphisme}','check/findings/findings_311_315.json#27','Preserve the exact observed defined-term rule.')
r.finding('311_315',28,'Both λ_t labels stand above their rightward horizontal arrows; f is left of the downward left arrow and Ĝ(f) right of the downward right arrow.',
 'The main square and native lower crop resolve all four headed arrows and their label positions, together with the comma after the lower-right object. The attached diagram agrees.',
 'homomorphism square',witness=325)
r.own_finding('ASTRA-V-UNDERLINE-314',p,'The definition underlines On appelle; un anneau; commutatif à élément unité; muni d’un homomorphisme de groupes abéliens; and tel que pour tout.',
 r'\uline on the five inspected word groups; the term pré-λ-anneau, K and other formulas stay outside.',
 'Render these five lexical groups explicitly.',
 'The native top crop resolves each rule and its endpoints. The term being defined is plain, as are K, both commas, the colon and the entire displayed map. The first four spans precede that map; the fifth precedes x∈K. This is the314 portion of checker311_315#7.',
 'Définition2.1, opening statement',witness=325)
r.patch(p,'both',r"On appelle pré-\(\lambda\)-anneau un anneau \(K\), commutatif à élément unité, muni d'un homomorphisme de groupes abéliens~:",r"\uline{On appelle} pré-\(\lambda\)-anneau \uline{un anneau} \(K\), \uline{commutatif à élément unité}, \uline{muni d'un homomorphisme de groupes abéliens}~:",'ASTRA-V-UNDERLINE-314','Preserve the first four observed word groups.')
r.patch(p,'both',r'tel que pour tout \(x\in K\)',r'\uline{tel que pour tout} \(x\in K\)','ASTRA-V-UNDERLINE-314','Preserve the last definition word group.')
r.own_finding('ASTRA-V-N-314',p,'All three natural-number indexing letters are ordinary typed N forms, with one left stem, one diagonal and one right stem.',
 r'N replaces the three \mathbb N occurrences.',
 'Restore the three observed plain N forms.',
 'The native top crop resolves N after i∈ and after n∈; the native lower crop resolves the last i∈N. Tight native crops and their nearest-neighbour enlargements show the same ordinary serifed N outline, without an independent added vertical or diagonal stroke. This agrees with the ordinary N inspected on298. The index identification is the identity i↦i on the same nonnegative integers used by λ^0 and the displayed i≥0 sum.',
 'three indexing sets in the coefficient description, conditioniii and final formula',kind='font',witness=325)
r.patch(p,'both',r'\mathbb N','N','ASTRA-V-N-314','Preserve the three inspected ordinary indexing letters.',count=3)
r.own_finding('ASTRA-V-PRODUCT-314',p,'The multiplication dot between λ^p(x) and λ^q(y) is a low typed stop, aligned with the final full stop of the formula.',
 r'\lambda^p(x)\mathbin{.}\lambda^q(y)',
 'Restore the observed baseline multiplication dot.',
 'The native conditioniii resolves the dot at the baseline, below the plus/equality midline. Its operation is the ring multiplication m_K:K×K→K, (a,b)↦ab, evaluated at a=λ^p(x) and b=λ^q(y). The replacement keeps that exact operation and the sum p+q=n while matching the printed dot height.',
 'conditioniii, summand',kind='symbol',witness=325)
r.patch(p,'both',r'\lambda^p(x)\cdot\lambda^q(y)',r'\lambda^p(x)\mathbin{.}\lambda^q(y)','ASTRA-V-PRODUCT-314','Preserve the low multiplication dot in this inspected summand.')
r.page(p,'Définition2.1. : On appelle pré-λ-anneau','λ^i(f(x))=f(λ^i(x)).',
 'Complete definition and all lexical rules, initial map and comma, baseline series dots, both summation bounds, all three coefficient conditions and punctuation, three ordinary N glyphs, exact low multiplication dot, both K′ primes, every square arrow/label and its final comma, and the complete final commutation formula compared. No author note.',
 witness='Native witness325 top/lower and sum/N crops; witness_314_top.png, witness_314_lower.png, witness_314_sum_N.png, witness_314_N_final.png')
r.commit()
