from audit_helpers import *
reasons={936:'The opening of 7.7 visibly says cas a=0 de 7.4, not 7.5. Restore the theorem reference.',937:'The scan says tous les termes initiaux, with the plural quantifier.',938:'The announced induction proceeds en nous appuyant, not et nous appuyant. Restore the printed preposition.',939:'Assertion (ii) visibly says l’image directe, with only one initial l.',940:'The scan says sur l’ouvert dense A^1 où, omitting de. The intended open subset is an open subset of A^1; insert the missing preposition in corrected French.',941:'The paragraph after (7.10.1) has pi_! with a subscript shriek. Miller’s plus exclamation is a transcription error.'}
for n,reason in reasons.items():decide(n,reason)
page(221,r'\item pour $a=0$',r'\item for $a=0$')
page(222,r'\item en $0$, la monodromie',r'\item at $0$, the monodromy')
page(223,'La suite exacte longue de cohomologie de','The long exact cohomology sequence of')
variant(222,'S45-SOL-0940',r"sur l'ouvert dense $\dA^1$ où",r"sur l'ouvert dense de $\dA^1$ où",'Supply the preposition locating the dense open subset.',place='Proof, second paragraph')
own(41,221,'Unit-group notation',r'^\ast',r'^\times',r'^\ast','symbol','The finite-field unit group is printed with an asterisk.')
append('notation_units',{'page':'221','source':'S45-ASTRA-S-0041','replace':r'^\times','with':r'^\ast'})
