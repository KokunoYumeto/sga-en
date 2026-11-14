#!/usr/bin/env python3
from review_helpers import Review
r=Review();p=303
r.finding('301_305',13,'Compte tenu de 1.6.ii)… begins a new paragraph after the opening parenthesis sentence.',
 'The main first strip and native top crop show the paragraph break. The attached layout agrees and the mathematical/prose token sequence is unchanged.',
 'page start and next paragraph',verdict='formatting observed; no content error',witness=314)
r.finding('301_305',14,'on posera donc Φ(φ)=ψ. ends the paragraph, with a full stop.',
 'Both scans place the assignment at the ordinary continuation line and retain its final full stop. The attached inline form agrees. Display versus inline layout alone does not require a new content patch.',
 'end of Compte tenu paragraph',verdict='formatting observed; no content error',witness=314)
r.finding('301_305',15,'un système d’application Φ_A … pour vérifier qu’elles constituent…',
 'Both scans type the singular application. The system consists of the maps Φ_A:Ĝ(A)→H(A), indexed by the object A, and the plural elles refers to those maps. Current therefore receives the plural applications; diplomatic retains the printed singular.',
 'paragraph introducing the naturality square',verdict='confirmed; current correction now applied',witness=314,
 change='Current only: un système d’application→un système d’applications.')
r.patch(p,'current',"un système d'application ","un système d'applications ",'check/findings/findings_301_305.json#15','Restore the plural noun for the indexed maps, which the following elles explicitly resumes.')
r.finding('301_305',16,'H(h) stands above the lower rightward arrow; Φ_A is left of the left arrow and Φ_{A′} right of the right arrow.',
 'The complete native lower crop resolves both primes attached to A, both downward arrowheads and both rightward arrowheads. The attached square has those same objects, labels and placements.',
 'naturality square at foot of page',verdict='formatting observed; map labels retained',witness=314)
r.own_finding('ASTRA-V-ELLIPSES-303',p,'Eight groups of three baseline dots occur in the expanded-series expressions.',
 r'\ldots at all eight inspected expanded-series positions on this page.',
 'Replace the eight local cdots groups by ldots.',
 'The main and native crops show three groups in the initial convergence paragraph, one in the definition of φ_n, one in its displayed compatibility equation, one in each of the two p-dependent congruences, and one in the final quantified congruence. The source has F^{p+1} in the first two p-dependent congruences and the weaker F^p in the last; those exponents are retained exactly.',
 'all expanded-series expressions',kind='symbol',witness=314)
r.patch(p,'both',r'\cdots',r'\ldots','ASTRA-V-ELLIPSES-303','Preserve the eight observed baseline ellipses.',count=8)
r.own_finding('ASTRA-V-NOTATION-303',p,'The category is looping script C; Ens is underlined; ten lowercase phi forms have an open upper-left curve; χ has crossed strokes distinct from typed X.',
 r'\mathcal C; \underline{\mathrm{Ens}}; \varphi and its n,m,p indices; \chi.',
 'Retain these observed local symbols and the plain body prose.',
 'The native top and lower crops resolve the category letter, the separate Ens rule, every lowercase phi loop and subscript, χ in the series argument and f_χ, and the full upper/lowercase Greek distinction. All printed prime marks belong to A′ in the final square and its introduction; none is added elsewhere.',
 'category names, Greek symbols and primes throughout the page',kind='symbol',verdict='confirmed',witness=314)
r.page(p,'(en se plaçant dans H(K[T₁,…,T_{n−1}])…','naturality square ending at H(A′)',
 'Complete convergence and compatibility arguments, every index and exponent, both p≥n clauses and the final quantifier, all filtration powers and final stops, the singular application variant, and every object/arrow/label of the naturality square compared. No author footnote.',
 witness='Native witness314 top and lower crops; witness_303_top.png and witness_303_lower.png')
r.commit()
