#!/usr/bin/env python3
from review_helpers import Review,HERE
r=Review();p=351
r.finding('351_355',1,'Folio351 starts ou A est l anneau;350 ends dans le cas.',
 'Both complete boundary images were compared. The attached marker is already at the correct word boundary.',
 '350/351 boundary',witness=362)
r.finding('351_355',2,'On plonge begins an indented new paragraph.',
 'Main365 upper strip and native362 top show the indentation. Retain the supplied paragraph break as layout.',
 'second paragraph',witness=362)
for n,printed,region in ((3,'The first sum display has no final stop.','first displayed equality'),(4,'The formula ending(1,1+X1) has no final stop.','lambda^n computation')):
 r.finding('351_355',n,printed,'Both main and native top resolve the blank after the final closing parenthesis; the attached punctuation agrees.',region,witness=362)
layout_reason=('The source places the formula after Enfin in running text and ends it with a full stop. The diplomatic inline and corrected displayed forms have the same formula-token sequence and final stop, apart from the independently justified lower-bound0 correction. The prompt accepts this layout choice, so no additional content patch is warranted and the old i=1 anchor must not overwrite the corrected i=0.')
r.finding('351_355',5,'The Enfin formula is inline and has a final full stop.',layout_reason,
 'Enfin formula placement',verdict='formatting decision; retain existing layouts',change='No content patch for inline/display layout.',witness=362)
sum_reason=('Both scans explicitly show i=1. The lambda-series identity is lambda_t(x)=product_(j=1)^n(1+L_j t), L_j=(1,1+T_j); evaluation t=-1 includes the constant coefficient lambda^0(x)=(1,1). Thus the alternating sum begins at0. Under the scalar projection pi:Ch(A)→K, the printed sum for positive n maps to sum_(i=1)^n(-1)^i binom(n,i)=-1, while lambda_(-1)(x) maps to(1-1)^n=0. In the concrete case n=1,K=Z this is already-1 versus0. Retain the existing current0 and diplomatic1. The symmetric-polynomial map X_i↦e_i(T1,...,Tn) is injective: ordered monomials in the e_i have distinct leading monomials with leading coefficient1; their coefficient comparison is unchanged after base extension to K. The induced Ch map is id_K on the scalar factor and the product of the graded injections on the completed ideal factor.')
r.finding('351_355',6,'The Enfin sum has lower bound i=1 and upper bound n.',sum_reason,
 'Enfin alternating sum lower bound',witness=362)
r.finding('351_355',7,'The Or formula is inline and its closing parenthesis has no following comma.',
 'Main second/third strips and native top show the missing comma precisely. The attached formula preserves that punctuation. Inline/display placement is accepted layout; only the actual punctuation is a source-content decision.',
 'Or formula ending',witness=362)
r.finding('351_355',8,'The soit formula is inline and followed by a full stop.',
 'The main third strip and native lower crop confirm the formula and its stop. Retain the attached token sequence; its inline placement needs no further content correction.',
 'soit formula ending',verdict='formatting decision; punctuation confirmed',change='Retain the existing formula and final full stop.',witness=362)
r.finding('351_355',9,'There is no comma between the gamma-formula closing parenthesis and les.',
 'The main third strip and native lower crop resolve the immediate space before les. The tail itself has two source dots, separately restored in the diplomatic form by ASTRA-V-TWO-DOT-351.',
 'gamma formula before les',witness=362)
r.finding('351_355',10,'The Corollary6.6.2 and Lemma6.6.3 each have three underlined lexical groups.',
 'Only the actual351 portion of this multi-page finding is decided here. Native362 lower resolves Corollary:La relation;est vraie pour tout element;d augmentation. Lemma:Pour tout;est un;ideal de. Mathematics and lambda-hyphen remain plain. The listed352–355 occurrences remain for their own direct comparisons.',
 'two statement bodies on351',verdict='confirmed for inspected351 scope',change='Restore these six word-rule groups; later pages pending.',witness=362)
r.source('fixes/FIXLOG_6_CURRENT.jsonl#412','Printed i=1 in the alternating sum.',sum_reason,'Enfin sum lower bound',page=p,witness=362)
r.source('fixes/RECONCILE_CODEX_6.json#300','Printed i=1 in the alternating sum.',sum_reason,'Enfin sum lower bound',page=p,witness=362)
r.source('fixes/REPLAY_MANUAL_6.json#8','The source Enfin formula is inline with final stop and lower bound1.',layout_reason,
 'historical replay of inline layout',page=p,witness=362,verdict='formatting decision; no further patch',change='Keep current lower bound0 and its accepted display layout.')
r.own_finding('ASTRA-V-UNDERLINE-351',p,
 'The two statements each underline three lexical groups; their mathematical letters, locators and lambda-hyphen are plain.',
 'Six explicit uline groups.',
 'Restore the observed source rules on351 only.',
 'The native lower crop shows all six rule endpoints. The proof paragraphs are unruled.',
 'Corollary6.6.2 and Lemma6.6.3',witness=362)
for old,new in (
 (r"La relation 6.6.1.iii) est vraie pour tout élément \(X\) d'augmentation \(n\).",r"\uline{La relation} 6.6.1.iii) \uline{est vraie pour tout élément} \(X\) \uline{d'augmentation} \(n\)."),
 (r'Pour tout \(n\), \((\Ch A)_n\) est un \(\lambda\)-idéal de \(\Ch A\).',r'\uline{Pour tout} \(n\), \((\Ch A)_n\) \uline{est un} \(\lambda\)-\uline{idéal de} \(\Ch A\).')):
 r.patch(p,'both',old,new,'ASTRA-V-UNDERLINE-351','Preserve the three inspected lexical groups of this statement.')
r.own_finding('ASTRA-V-TWO-DOT-351',p,
 'The final tail of gamma^i(0,phi) after Q-double-prime_(i,j) has exactly two low dots; the earlier tail after Q-double-prime_(i,1) has three.',
 'Diplomatic final tail+..; corrected complete low ellipsis.',
 'Restore the literal source two-dot ending in diplomatic only.',
 'Main third strip and native362 lower clearly separate the two final dots before the closing parenthesis, while the earlier three-dot tail is visible in the same line. The full formal series is1+sum_(j>=1)Q-double-prime_(i,j); both abbreviations refer to that same higher-j tail. Current retains the complete three-dot notation.',
 'last gamma formula, final tail',kind='misprint_in_print',witness=362)
r.patch(p,'diplomatic',r"Q''_{i,j}+\cdots)\) les",r"Q''_{i,j}+..)\) les",'ASTRA-V-TWO-DOT-351','Preserve the two physically printed final dots and the absence of a comma.')
r.own_finding('ASTRA-V-ELLIPSES-351',p,
 'All complete source series ellipses are low.',
 r'Use \ldots for five diplomatic/six corrected remaining centered ellipsis controls.',
 'Preserve the baseline of the complete source ellipses.',
 'Main/native views resolve the introductory pair, first display, Or/soit tails and the two gamma-series positions. The two already low polynomial-list ellipses are retained; the literal final two-dot variant is independently recorded.',
 'complete series ellipses',kind='symbol',witness=362)
r.patch(p,'diplomatic',r'\cdots',r'\ldots','ASTRA-V-ELLIPSES-351','Preserve five remaining complete low ellipses.',count=5)
r.patch(p,'current',r'\cdots',r'\ldots','ASTRA-V-ELLIPSES-351','Preserve six complete low corrected ellipses.',count=6)
r.own_finding('ASTRA-V-CONNECTED-STROKE-351',p,
 'In the opening word pour, a narrow peaked ink stroke rises from the left part of the u and ends above it.',
 'Retain pour and record the additional connected stroke; do not assign an unestablished separate accent token.',
 'Keep the readable letters and explicitly preserve the physical observation.',
 'The native tight pour crop and nearest-neighbour zoom show the stroke attached to the u-side ink. The word remains readable as pour. Its cause and a separate circumflex character are not established by the connected shape, so neither is asserted.',
 'opening sentence, et pour l element',kind='damaged_or_extra_ink',verdict='source retained; physical mark explicitly recorded',witness=362)
r.page(p,'ou A est l anneau','appartiennent a(Ch A)_n,et',
 'Full main365 four strips and native362 top/lower compared. Checked the opening weights and connected ink above pour, both symmetric-polynomial rings and prime, all product/sum limits, lambda series and strict k>n, all ordered-pair coordinates, source alternating lower bound1, current0 proof, every end punctuation, inline/display decisions without new layout-only content fixes, six statement word rules, capital X in the corollary, gamma indices and Q single/double primes, newly observed final two-dot tail and no comma, all remaining prose and the final et. No author note.',
 witness='Native362 top/lower; witness_351_pour.png and nearest-neighbour zoom; full lower gamma line.')
r.commit()
