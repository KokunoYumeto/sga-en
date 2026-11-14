"""Adjudicate queue claims at four already fully inspected passages."""
from review_helpers import Review
r=Review()
r.source('fixes/RECONCILE_CODEX_6.json#229','respée on162; non respée on168',
    'Both inspected passages print this abbreviated form. In Proposition1.2 it selects the parenthetical presentation-finite branch of hypothesis1.1(ii); the later non respée invocation selects the other branch. Expanding it to respectivement would replace the author’s branch label with a different expression. Retain the printed abbreviation in both layers.',
    'Hypotheses of Proposition1.2; proof of2.2.2',change='Confirm rejection of the proposed expansion; retain respée.',page=162)
r.source('fixes/RECONCILE_CODEX_6.json#230','The spectral-sequence abutment is Ext^*(G,E)',
    'The actual printed superscript is an asterisk, already restored by checker161–165#13, rather than the n assumed by the queue claim and its earlier rejection reason. Ext^* denotes the graded target; projection to degree n=p+q gives the diagonal component Ext^n. Writing p+q would select that component of the existing graded notation and does not repair a printed error. Retain the actual asterisk.',
    'Folio164 spectral sequence',verdict='amended',change='Reject the proposed p+q rewrite; replace the stale n-based rationale by the actual printed-star decision.',page=164)
r.source('fixes/RECONCILE_CODEX_6.json#231','Γ_S(F) in the second Hom functor; Hom_{A(S)}(F,G) in the diagram',
    'The fixed second argument must be Γ_S(G), as in the two right-hand bottom terms. Applying Hom_{A(S)}(−,Γ_S(G)) to(**) gives Hom_{A(S)}(Γ_S(F),Γ_S(G)) at the left. The vertical comparison sends each sheaf map F→G to its section map Γ_S(F)→Γ_S(G). The first correction was already applied; the diagram correction is now applied with the explicit section arguments under MISPRINT158. Diplomatic retains both printed readings.',
    'Folio165 Hom calculation and diagram',verdict='amended',change='Accept both linked corrections, including the formerly rejected diagram part; see checker161–165#18–19.',page=165)
r.source('fixes/RECONCILE_CODEX_6.json#232','non respée and tous O_S-Module',
    'The author’s branch label non respée is retained as printed, consistently with its earlier invocation on162. The determiner tous precedes singular Module and est, and current correctly changes only that determiner to tout. No expansion of the abbreviation is made.',
    'Folio168 proof of Proposition2.2.2',change='Confirm the applied tous→tout correction and retain non respée.',page=168)
r.commit()
