#!/usr/bin/env python3
from review_helpers import Review
r=Review();p=304
r.finding('301_305',17,'H(h)∘H(f_χ(ψ)) has no closing parenthesis between f_χ and (ψ).',
 'The native top crop shows the two closes after ψ. Preserve that printed grouping diplomatically. On 303, ψ belongs to H(K[Xi]) and f_χ:K[Xi]→A, so H(f_χ):H(K[Xi])→H(A) applies to ψ; H(h):H(A)→H(A′) then applies to its value. This exact typed composite supports the existing current H(h)∘H(f_χ)(ψ).',
 'second member of the opening equality',witness=315,change='Retain the existing source/current parenthesis distinction.')
r.finding('301_305',18,'The last member is Φ_{A′}(Ĝ(h)(χ)., with only one close after χ.',
 'Both scans show the full stop immediately after the single closing parenthesis. The opening parenthesis of the outer Φ_{A′} application is unmatched. The source layer keeps it; the current layer supplies exactly that one missing close, giving Φ_{A′}(Ĝ(h)(χ)).',
 'last member of the opening equality',witness=315,change='Retain the existing current-only closing parenthesis.')
r.finding('301_305',19,'Il reste donc… begins a new indented paragraph.',
 'The native top crop confirms the break. The attached layout already agrees; this formatting decision changes no words, symbols or punctuation.',
 'after the opening equality',verdict='formatting observed; no content error',witness=315)
r.finding('301_305',20,'The vertical downward arrow in the additivity triangle has a hook curling right at its upper tail.',
 'The native triangle crop clearly shows the curved upper tail and lower arrowhead. The attached hooked arrow preserves those two features. Its source and target are respectively K[X₁,…,X_{2n}] and the displayed invariant ring.',
 'vertical arrow in the triangle',witness=315)
r.finding('301_305',21,'f′_χ is on the upper-left side of the diagonal arrow toward A.',
 'The native triangle crop resolves the prime on f and the handwritten χ beneath it, to the upper-left of the shaft. The attached label placement agrees and preserves the same morphism.',
 'diagonal arrow in the triangle',verdict='formatting observed; map label retained',witness=315)
r.finding('301_305',22,'A comma follows the diagram at the lower-row level.',
 'Both scans have this comma to the right of the invariant-ring expression. The attached last-cell comma preserves it.',
 'end of triangle',witness=315)
for ids,printed,region in [
 (['fixes/FIXLOG_6.jsonl#375','fixes/FIXLOG_6_CURRENT.jsonl#400'],'χ₁,χ₂','Soient donc…'),
 (['fixes/FIXLOG_6.jsonl#376','fixes/FIXLOG_6_CURRENT.jsonl#401'],'χ leur produit','same paragraph'),
 (['fixes/FIXLOG_6.jsonl#377','fixes/FIXLOG_6_CURRENT.jsonl#402'],'f_χ','horizontal arrow label'),
 (['fixes/FIXLOG_6.jsonl#378','fixes/FIXLOG_6_CURRENT.jsonl#403'],'f′_χ','diagonal arrow label')]:
 for sid in ids:
  r.source(sid,printed,
   'Both main and native triangle crops show handwritten crossed chi strokes with curved ends, agreeing with the chi already used earlier on this page and on 303. The typed polynomial variables X_i have the separate capital typewriter shape. Retain the applied transcription repair in both layers; the full two-page Codex entry is adjudicated after inspection of its 305 continuations.',
   region,witness=315,change='Retain the applied χ transcription.')
r.own_finding('ASTRA-V-ELLIPSES-304',p,'Both expanded-series ellipses are three baseline dots.',
 r'\ldots in the two filtration congruences.',
 'Replace the two local cdots groups by ldots.',
 'The native top crop resolves the three stops in each congruence below the g_n definition. Both groups are below the plus-sign midline. The same crop confirms the inclusive lower bounds 1≤i≤n−1 and i≥n, three open-left lowercase phi forms, and all F^n exponents.',
 'filtration congruences',kind='symbol',witness=315)
r.patch(p,'both',r'\cdots',r'\ldots','ASTRA-V-ELLIPSES-304','Preserve the two observed baseline ellipses.',count=2)
r.page(p,'est commutatif. Soit χ∈Ĝ(A)…','où les flèches… S_n×S_n opère sur K[T₁,…,T_{2n}]',
 'Complete naturality equality including both printed parenthesis errors, filtration factorization and inclusive bounds, both congruences, additivity introduction and all triangle vertices/arrows/labels, symmetric-group forms and final comma compared. Body prose is plain; no author note.',
 witness='Native witness315 top and triangle crops; witness_304_top.png and witness_304_triangle.png')
r.commit()
