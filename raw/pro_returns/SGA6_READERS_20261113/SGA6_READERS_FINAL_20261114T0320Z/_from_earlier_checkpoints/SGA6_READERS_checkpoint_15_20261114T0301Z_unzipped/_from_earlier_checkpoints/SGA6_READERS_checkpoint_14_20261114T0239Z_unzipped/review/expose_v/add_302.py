#!/usr/bin/env python3
from review_helpers import Review
r=Review();p=302
r.finding('301_305',9,'θ=Φ(1+Xt) ; montrons que… begins the page.',
 'The main first strip and native top crop begin with the complete theta assignment. The preceding page ends et soit. The attached marker already separates these exact words and formulas.',
 'page start',witness=313)
r.finding('301_305',10,'On détermine d’abord… begins a new paragraph.',
 'Both scans show the paragraph indentation and break. The attached layout already agrees, with identical prose and mathematical tokens; no additional content patch is needed.',
 'after tel que θ=Φ(1+Xt).',verdict='formatting observed; no content error',witness=313)
r.finding('301_305',11,'σ′_n is left of the right downward arrow.',
 'The native square crop shows the detached prime above n and the whole label left of the shaft. The arrow is downward, and its endpoint is K[T₁,…,T_n]. The attached positioning and label agree.',
 'right vertical arrow of (1.6.2)',verdict='formatting observed; map label retained',witness=313)
r.finding('301_305',12,'f′_n is above the lower rightward arrow; the left vertical label is σ_n without an independent tilde.',
 'The native square crop confirms f′_n above the shaft. The inherited note calls the left label sigma-tilde, but its upper wavy stroke joins the letter’s loop and is the sigma tail; the same connected tail appears in σ′_n and in both following prose definitions. The lower-arrow placement is retained; the separate local sigma-glyph repair is recorded as ASTRA-V-SIGMA-302.',
 'lower horizontal and left vertical labels of (1.6.2)',verdict='placement confirmed; accompanying sigma description amended',witness=313)
r.own_finding('ASTRA-V-SIGMA-302',p,'The left vertical label and its following prose definition each have plain handwritten σ_n, with a connected upper tail and no detached accent.',
 r'\sigma_n in both occurrences.',
 'Remove the added tilde from these two sigma occurrences.',
 'The native witness_302_square.png resolves the upper curved stroke as connected to the loop. In the primed sigma at right and in its definition the same letter tail is present, followed by a separate prime; no detached tilde is present on either unprimed sigma. The polynomial map remains Xi↦the i-th symmetric function of T₁,…,T_n exactly as printed.',
 'left arrow of (1.6.2) and its prose definition',kind='symbol',witness=313)
r.patch(p,'both',r'\widetilde{\sigma}_n',r'\sigma_n','ASTRA-V-SIGMA-302','Preserve the two plain sigma glyphs; the connected tail is part of the letter.',count=2)
r.own_finding('ASTRA-V-ELLIPSES-302',p,'Ten three-dot groups in the expanded-series formulas lie on the baseline.',
 r'\ldots at all ten inspected expanded-series positions on this page.',
 'Replace the ten local cdots groups by ldots.',
 'The native top crop resolves five groups in ii), two in the determination paragraph and one in On recolle. The native square crop resolves the remaining two groups in the concluding equality. Every coefficient, exponent and existing sentence stop stays unchanged.',
 'expanded-series formulas throughout the page',kind='symbol',witness=313)
r.patch(p,'both',r'\cdots',r'\ldots','ASTRA-V-ELLIPSES-302','Preserve the ten observed baseline ellipses.',count=10)
r.page(p,'θ=Φ(1+Xt) ; montrons que…','=Φ(1+…+X_{n−1}t^{n−1})',
 'Complete proof paragraphs and equations, all composition circles, Φ and θ forms, hatted G symbols, both i<n clauses, all four square objects and arrows, f primes, sigma forms, three sum bounds, and the final equality without a stop compared. All body prose is plain. No author note.',
 witness='Native witness313 top and square crops; witness_302_top.png and witness_302_square.png')
r.commit()
