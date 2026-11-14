#!/usr/bin/env python3
from review_helpers import Review
r=Review();p=321
r.finding('321_325',1,'The outer1 in (1+{1+t}u)^n has a short underline; the inner1 is plain.',
 'The native top crop resolves the rule under the outer unit and the absence of a rule inside the braces. The attached form agrees with the same unit named on318–320.',
 'second displayed equality chain in a)',witness=332)
r.finding('321_325',2,'Four1 symbols are underlined in the opening b) equality chain: the first argument, the outer unit after the second equality, and both units in the last member.',
 'The native lower crop resolves all four separate rules. The1 in (1+t) and the1 inside {1+t} are plain. The attached underline scopes match each occurrence.',
 'D’abord equality chain in b)',witness=332)
r.finding('321_325',3,'The multiplication mark between the last underlined1 and u is a low full stop.',
 'The native lower crop places this dot at the ordinary letter baseline and below the equality midline. It denotes the coefficient multiplication in the formal power-series ring over Ĝ(K): the unit coefficient multiplied by the indeterminate u. The attached literal period preserves the observed position and the same multiplication.',
 'last member1̲+1̲.u in b)',witness=332)
r.finding('321_325',4,'The upper-right vertex of the left square has an opening parenthesis around the first factor, but no opening parenthesis before the second factor; both closing parentheses are present.',
 'The native lower diagram crop resolves the empty interval after the product sign and before the second Ĝ^u. The top horizontal map λ_u×λ_u takes (α,β) to (λ_u(α),λ_u(β)) in (Ĝ^u∘Ĝ^t)×(Ĝ^u∘Ĝ^t); the right vertical map multiplies these two elements by the circle law. This exact product target identifies the missing opening parenthesis. Retain the printed omission diplomatically and the supplied parenthesis in the corrected layer.',
 'left square, upper-right vertex',witness=332)
r.finding('321_325',5,'The lower horizontal λ_u label in the left square lies above its headed rightward arrow.',
 'The main and native lower crops agree. The upper map is λ_u×λ_u and both vertical labels are circle; all four arrowheads point toward the displayed lower/right vertices. The attached label placement agrees.',
 'left square, lower horizontal map',witness=332)
r.finding('321_325',6,'The lower horizontal λ_v label in the right square lies above its headed rightward arrow.',
 'The native lower crop also resolves λ_u at the left vertical arrow, Ĝ^v(λ_u) at the right, and the ordered superscripts v,u,t in the lower-right vertex. The attached labels and map directions agree.',
 'right square, lower horizontal map',witness=332)
r.own_finding('ASTRA-V-ELLIPSIS-321',p,'The three dots between (X−1) and (X−k+1) in the binomial polynomial lie on the baseline.',
 r'X(X-1)\ldots(X-k+1)',
 'Restore the directly observed baseline ellipsis.',
 'The native top crop places the three points level with the bases of the adjacent capital X and parentheses, below their mid-height. The product still ranges over the same k descending linear factors and the prefactor1/k! remains unchanged.',
 'polynomial defining the binomial coefficient',kind='symbol',witness=332)
r.patch(p,'both',r'X(X-1)\cdots(X-k+1)',r'X(X-1)\ldots(X-k+1)','ASTRA-V-ELLIPSIS-321','Preserve the inspected three baseline product dots.')
r.page(p,'On notera que nous nous écartons ici','the second diagram’s terminal comma',
 'Entire terminology paragraph, every λ and quoted spécial expression, a)/b) labels, both reinforced/doubled Z forms, all n/n′ and nn′ indices, full two equality chains and their semicolon/full stop, five underlined units across a)/b), plain inner units, binomial parentheses/factorial/polynomial and2.5.1 stop, low product dot, all eight diagram arrows, every arrow label and superscript order, one missing parenthesis and both final diagram commas compared. No author note.',
 witness='Native witness332 top/lower crops; witness_321_top.png and witness_321_lower.png')
r.commit()
