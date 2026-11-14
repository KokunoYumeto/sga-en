#!/usr/bin/env python3
from review_helpers import Review
r=Review();p=291
r.finding('291_295',1,'est donc définie, reste à montrer que c’est un isomorphisme.',
 'The first word est is on this page in the main scan, and the preceding page ends at base. The attached marker already implements this boundary.',
 'first line',witness=302)
r.finding('291_295',2,'Ordinary typed L above the tensor product in B⊗^L_A A′ → B′.',
 'The main strip and native formula crop both show a plain L. The map has an actual rightward arrowhead and a centered tilde, followed by a comma.',
 'first derived tensor display',witness=302)
r.finding('291_295',3,'Two ordinary typed L letters in E⊗^L_A A′ → E⊗^L_B B′.',
 'Both L letters have the ordinary single-stroke typewriter form. The two tensor subscripts A and B, the primes, the headed tilde-labelled arrow and the comma agree with the attached source.',
 'second derived tensor display',witness=302)
r.own_finding('ASTRA-IV-UNDERLINE-291',p,'Soit is underlined after Proposition 3.1.1.; the proof prose and the preceding translation sentence are plain.',
 r'\textbf{Proposition 3.1.1.} \uline{Soit}',
 'Add the missing rule beneath the opening word of Proposition 3.1.1.',
 'The native formula/statement crop shows a separate rule beneath Soit, in addition to the rule beneath the proposition label. This is a local observation for 3.1.1; the plain Soit in 3.1.0 on 290 is preserved.',
 'opening of Proposition 3.1.1',witness=302)
r.patch(p,'both',r'\textbf{Proposition 3.1.1.} Soit',r'\textbf{Proposition 3.1.1.} \uline{Soit}','ASTRA-IV-UNDERLINE-291','Restore the observed rule beneath Soit only.')
r.page(p,'est donc définie, reste à montrer que c’est un isomorphisme.','The four-object cartesian square after Proposition 3.1.1. Soit.',
 'All proof prose, the cocartesian ring square and its four directed arrows, both derived tensor displays, all references, proposition opening and second square compared. No footnote. The first square has rightward and upward arrows; the last has leftward and downward arrows, matching the source.',
 witness='Native witness 302 formula/statement region; witness_291_formulas.png')
r.commit()
