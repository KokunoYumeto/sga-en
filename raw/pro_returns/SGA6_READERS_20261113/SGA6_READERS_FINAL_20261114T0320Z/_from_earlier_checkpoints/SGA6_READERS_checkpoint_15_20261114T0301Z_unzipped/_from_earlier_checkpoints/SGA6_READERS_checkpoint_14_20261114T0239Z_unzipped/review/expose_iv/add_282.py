#!/usr/bin/env python3
from review_helpers import Review
r=Review();p=282
r.finding('281_285',9,'Ordinary upright L above the derived tensor sign.',
 'The displayed L has its single upright stroke and foot, matching the ordinary typewriter capitals; no double lower rule or separate duplicated stroke is present. The current plain-L form is retained at this inspected occurrence.',
 'derived tensor display before (2.6.4)',witness=293)
r.own_finding('ASTRA-IV-NOTATION-282',p,'Fifteen raised round K marks; three independently underlined parf terms in (2.6.4); headed rightward horizontal and downward vertical arrows in (2.6.6).',
 'Attached raised-dot notation and underlined parf macro; four-node commutative diagram.',
 'Retain the inspected content and occurrence-specific typography.',
 'The main strips cover all formulas and references. Native witness 293 confirms the three lower rules and all four arrowheads. The upper horizontal map is (2.6.2), the lower is (2.6.5), and the vertical maps are the three inclusion homomorphisms (2.6.3.1–3); the printed comma follows the lower-right object. No additional label or equality is supplied.',
 'six inclusion-group terms, tensor map, and complete diagram (2.6.6)',kind='symbol',verdict='confirmed',witness=293)
r.page(p,'Les foncteurs d’inclusion définissent de manière évidente des','nies par (2.6.3.1), (2.6.3.2) et (2.6.3.3).',
 'All words, fifteen raised K marks, primes and left/right module subscripts, three comparison maps, derived tensor, three parf rules, and four diagram arrows compared. The terminal sentence has the correct assignment of horizontal and vertical maps. No author footnote and no new patch.',witness='Native witness 293 tensor/diagram region; witness_282_tensor_diagram.png')
r.commit()
