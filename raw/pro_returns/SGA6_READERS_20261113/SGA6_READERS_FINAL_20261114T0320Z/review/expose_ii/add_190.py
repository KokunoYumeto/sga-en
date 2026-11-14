"""Folio190: the finite affine-cover resolution and its unprimed terms."""
from review_helpers import Review
r=Review()
observations=[
 (30,'The page begins ainsi d’ailleurs;189 ends morphismes affines,','First printed line','The full beginning and the preceding page ending were inspected. Both attached page markers already separate these exact words.'),
 (31,'The intersections U_i0∩...∩U_ip use three baseline dots','Opening inclusions','The three dots lie on the baseline. The complete sequence of indices and intersections agrees with the attached ldots.'),
 (32,'The first coproduct in(*) has no lower index','Resolution(*), first coproduct','The region immediately below this coproduct is empty; the index occurs on f. The attached unindexed coproduct matches.'),
 (33,'The internal omission marks in(*) are baseline dots','Resolution(*), middle','Three baseline dots occur between the two arrows. The attached ldots matches.'),
 (34,'The second coproduct in(*) has no lower index','Resolution(*), second coproduct','The region immediately below this coproduct is empty; the multi-index occurs on f. This differs by an actual inspected index from the explicitly indexed coproduct in(**), which remains intact.'),
 (35,'The last arrow in(*) is followed by a single stop','Resolution(*), end','The scan ends this formula with an arrow and one sentence stop. No omitted-dots sequence is printed after that arrow; the attached text matches.'),
 (36,'The relation in(***) is a wave over a headless straight bar','Formula(***)','Both ends of the lower stroke have no arrowheads. The complete direct-image and pullback subscripts match.'),
 (37,'There is no punctuation after(***)','End of(***) and following sentence','The formula continues directly into pour tout q. The attached absence of a stop agrees.'),
 (38,'R^nQ(E) ≃ H^n(QE with a raised dot)','Derived-functor display','The relation is a wave over a headless straight bar. The degree n and bound n≥0 agree.'),
 (39,'The E in H^n(QE) carries a raised round dot','Derived-functor display','The native witness shows a small round raised dot. Apostrophes in d’après and d’où on the same lines have elongated tick shapes. The term is the complex E^bullet defined by(*).'),
 (40,'où E with a raised round dot est la résolution de E','Sentence after the derived-functor display','The same raised round dot appears in the definition of the resolution complex; the following degree terms are plain E^n. The attached E^bullet matches.'),
 (41,'on a QE^n ≃ E^n pour n≥0','Last application of(***)','The native witness shows unprimed E^n on both sides and a headless wave-over-bar relation. The cumulative middle replay supplies the headless relation; the independently adjudicated Codex prime insertions are removed below.'),
 (42,'et Q(E) ≃ E, cqfd.','End of the first proof','The relation is a wave over a headless bar. The final comma and cqfd stop match.'),
 (43,'Only Preuve de is underlined; (3.5.2). is plain','Final proof heading','The word-rule span ends before the numerical reference. The attached emphasis scope agrees and is given a literal underline helper.')]
for i,printed,region,reason in observations:
 kw={'witness':201} if i in (38,39,40,41,42,43) else {}
 if i==30:kw['change']='Retain the boundary before ainsi d’ailleurs.'
 if i==41:kw['change']='Retain the headless relation supplied by middle replay5 and restore unprimed terms as decided for Codex253.'
 if i==43:kw['change']=r'Typeset the observed scope as \uline{Preuve de} (3.5.2).'
 r.finding('186_190',i,printed,reason,region,**kw)
reason='The scan defines E^bullet as the resolution(*) and writes its degree terms E^n without primes. Concretely, E^n is the coproduct of f_{i0...in*}f_{i0...in}^*(E). Formula(***) at q=0, together with the affine-case identification Qf^*(E)≃f^*(E), identifies Q(E^n) with E^n. There is no lifted primed complex or quotient on this page. The two inserted primes arose from reading the raised round complex dot as a prime. Remove precisely those two inserted prime tokens; retain E^bullet and the same resolution and functor maps.'
for sid in ['fixes/RECONCILE_CODEX_6.json#253','fixes/FIXLOG_6_CURRENT.jsonl#360']:
 r.source(sid,'E^bullet is the resolution, and QE^n ≃ E^n has no primes',reason,'Definition of the resolution and the following use of(***)',page=190,verdict='rejected after direct scan review',change='Withdraw both inserted primes in current; retain E^bullet and the unprimed degree terms in both layers.',witness=201)
r.patch(190,'current',r"E'{}^n",r'E^n','fixes/RECONCILE_CODEX_6.json#253',reason,2)
r.source('fixes/REPLAY_MANUAL_6.json#5','The isomorphism QE^n ≃ E^n has a headless lower stroke',
 'The original replay anchor failed after the Codex prime insertion. The cumulative middle replay uses that actual primed anchor to restore the observed headless sign; the current page patch then removes the unsupported primes. These operations preserve the directly observed QE^n≃E^n expression.',
 'Last application of(***)',page=190,verdict='confirmed',change='Retain the symbol repair at the cumulative middle anchor, then remove both inserted primes under Codex253.',witness=201)
r.patch(190,'both',r'\emph{Preuve de}',r'\uline{Preuve de}','check/findings/findings_186_190.json#43','Preserve the exact inspected lexical word-rule scope, with the numerical reference plain.')
r.page(190,'ainsi d’ailleurs que les inclusions','R^pQ(H^q(E))⇒R*Q(E),',
 'All prose, every multi-index, both coproduct forms, all three numbered-star formulas, every sign and degree bound, and the final spectral sequence were compared. The native witness lower region confirms the raised round complex dots, both unprimed degree terms and the headless isomorphism signs. Every derived R on this page is plain with its printed degree index; no blanket R font replacement is applied.',witness=201)
r.commit()
