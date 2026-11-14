#!/usr/bin/env python3
from review_helpers import Review
r=Review();p=348
r.finding('346_350',9,'Folio348 begins6.3.Pour toute K-algebre graduee A;347 ends est un lambda-homomorphisme).',
 'Both complete boundary images were directly compared. The attached marker precedes6.3 and agrees with the source.',
 '347/348 boundary',witness=359)
r.finding('346_350',10,'Cet homomorphisme begins an indented paragraph after6.3.1.',
 'The main first strip and native359 top confirm the indentation. Retain the existing paragraph break as layout with no change to the text or formulas.',
 'after6.3.1',witness=359)
r.finding('346_350',11,'A handwritten completion hat spans K[X,Y] in the two-variable universal input.',
 'Main second strip and native359 top resolve both arms of the hat. The attached completed expression agrees.',
 'paragraph before multiplicativity computation',witness=359)
r.finding('346_350',12,'The last calculation starts ch(1+X)^a), with one opening and two closing parentheses.',
 'Main bottom strip and native359 lower resolve the exact unmatched delimiter. The following argument is exp(a Log(1+X))=(1+X)^a, so the map being applied is ch to the complete powered series. Under ch=eta∘Log the exact chain is ch((1+X)^a)=eta(a Log(1+X))=a eta(Log(1+X))=a ch(1+X). The existing corrected opening parenthesis gives precisely this map composition. In particular a=0 gives ch(1)=0, whereas interpreting the printed exponent outside ch would give ch(1+X)^0=1 in the completed rational ring.',
 'last display, initial argument',witness=359)
r.own_finding('ASTRA-V-FORMS-348',p,
 'The paragraph number6.3 is ordinary type. Four hand-drawn Q letters have an additional inner stroke, and the tensor-base Z is reinforced.',
 r'Use plain6.3.; retain the four \mathbb Q and the tensor-base \mathbb Z forms.',
 'Restore only the unruled paragraph label; retain the directly inspected number-ring forms.',
 'The main upper strip and native359 top resolve the Q in the first A subscript, the tensor factor, the ch target and the eta domain; each has the inner reinforcing stroke. The source tensor-base Z also has reinforcing ink. The number-ring maps remain the printed scalar extension A→A⊗_ZQ and its homogeneous completion; no font-based change of algebra is made.',
 'paragraph label and rational coefficient notation',kind='convention',witness=359)
r.patch(p,'both',r'\textbf{6.3.}',r'6.3.','ASTRA-V-FORMS-348','Preserve the ordinary numbered paragraph.')
r.page(p,'6.3.Pour toute K-algebre graduee A','a.ch(1+X).',
 'Full main362 four strips and native359 top/lower compared. Checked all prose, the four Q and one Z forms, headed ch arrow, every completion hat,6.3.1, all four multiplicativity rows with their signs/parentheses and sole final stop, both eta sums with lower bound k>=1 and no upper bound, factorial(k-1)! and sign(-1)^(k-1), existing low product periods, varphi and6.3.2, both Log compositions, literal de la montrer in the compatibility sentence, all parentheses of the final four-row computation and its ending stop. No lexical underline or author note.',
 witness='Native359 top/lower: witness_348_top.png and witness_348_lower.png.')
r.commit()
