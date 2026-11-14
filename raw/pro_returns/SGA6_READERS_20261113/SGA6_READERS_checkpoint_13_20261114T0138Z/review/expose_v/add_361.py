#!/usr/bin/env python3
from review_helpers import Review
r=Review();p=361
r.finding('361_365',1,'The source prints nécéssaire,with an acute on its second e.',
 'Both full native lower and primary third strip resolve the second acute. Current nécessaire removes that spelling slip while preserving the statement about the same map f:K→K prime and its commutation with the same Adams operations.',
 '7.3,nécéssaire',verdict='not applied and now applied',change='Current nécessaire;diplomatic nécéssaire.',witness=372)
r.patch(p,'current','nécéssaire','nécessaire','check/findings/findings_361_365.json#1','Remove the extra lexical acute in current only.')
r.finding('361_365',2,'The example7.4(i) summation has k=1 beneath it and no written upper bound.',
 'Both scans clearly leave the space over this sum blank;the infinity over7.2.1 on the same page provides a direct comparison. The attached sum already agrees. It denotes the formal geometric series n/(1+t)=sum_(k>=1)n(-1)^(k-1)t^(k-1);no extra bound is needed in either layer.',
 '7.4(i),geometric-series display',witness=372)
r.finding('361_365',3,'D apres7.1.1 starts a new indented paragraph after the additivity formula.',
 'Both primary first strip and native top show the indent. The supplied blank line already agrees. The three-point low index list and the two subsequent Adams examples are exact.',
 'paragraph after first display',witness=372)
r.own_finding('ASTRA-V-ID-361',p,'The identity name in7.2 is capital Id with subscript K.',r'\operatorname{Id}_K',
 'Restore the observed capital I occurrence in both forms.',
 'The native top resolves a capital I followed by lowercase d. The preceding source macro renewals make the supplied id control lowercase at this point,so its literal local expansion must change. The named map remains K→K,x→x,which is exactly the operation psi^1 required here.',
 '7.2,psi^1=Id_K',kind='symbol',witness=372)
r.patch(p,'both',r'\psi^1=\id_K',r'\psi^1=\operatorname{Id}_K','ASTRA-V-ID-361','Preserve the observed capital identity name without changing a global macro.')
r.own_finding('ASTRA-V-PARAGRAPH-361',p,'The labels7.2. and7.3. are ordinary type.',
 'Use ordinary weight for these two paragraph labels.',
 'Restore the inspected paragraph-label convention in both forms.',
 'Both main and native views show ordinary numeral strokes. The separate ruled word Exemples is already represented by the accepted bold statement-label convention and is not included in this change.',
 'paragraph labels7.2 and7.3',kind='font',witness=372)
for n in ['7.2.','7.3.']:
 r.patch(p,'both',r'\textbf{'+n+'}',n,'ASTRA-V-PARAGRAPH-361','Preserve the ordinary paragraph-label weight.')
r.own_finding('ASTRA-V-POLYNOMES-361',p,
 'Both occurrences of polynomes are printed with a bare o.',
 'Current polynômes at both occurrences;diplomatic polynomes.',
 'Supply the missing lexical circumflex in current only.',
 'Native372 top and lower show a bare o in the opening isobaric-polynomial paragraph and the last sentence of7.3. These are the same French noun polynôme already used throughout the supplied text. The exact coefficient polynomial remains unchanged:the forward coefficients are extracted from lambda-prime/lambda,and the reverse coefficients from the exponential7.2.1. This spelling correction changes neither those coefficient maps nor their variables.',
 'opening polynomial paragraph and end of7.3',kind='accent',witness=372)
r.patch(p,'current','polynomes','polynômes','ASTRA-V-POLYNOMES-361','Restore the missing lexical circumflex in the two current occurrences.',count=2)
r.own_finding('ASTRA-V-ADAMS-EXP-361',p,
 '7.2 states the exponential reconstruction for a ring of characteristic0;7.3 states the corresponding commutation criterion.',
 'Retain the printed wording and formula.',
 'Identify the actual formal-series maps under the source characteristic-zero convention.',
 'Page349 explicitly uses characteristic0 to mean a Q-algebra. For the present K under that convention,put U_x=sum_(k>=1)(-1)^(k-1)psi^k(x)t^k/k in tK[[t]]. The map exp:tK[[t]]→1+tK[[t]] and its inverse Log are well-defined coefficientwise,because each coefficient involves a finite sum and the rational denominators lie in K. Additivity gives U_(x+y)=U_x+U_y and hence lambda_t(x+y)=exp(U_x)exp(U_y);its t-coefficient is psi^1(x)=x. Differentiating Log recovers exactly7.1.1. A ring map commuting with every psi^k commutes with U coefficientwise and therefore with exp,which proves the stated reverse commutation implication. No change from the source convention to a weaker meaning of characteristic0 is made.',
 '7.2–7.3,exponential and inverse logarithmic-derivative maps',kind='exact_identification',verdict='confirmed and retained with exact coefficient maps',witness=372)
r.page(p,'et par suite,pour tout k:','ii) Plaçons nous ... (1.8). Les',
 'Full main375 four strips and native372 two overlapping body crops compared. Checked every Adams exponent,additivity equation,isobaric-weight statement,two low examples,plain7.2/7.3,capital Id_K,7.2.1 sign and infinite bound,source characteristic-zero convention and exact exp/Log maps,two bare-o spellings,extra acute of nécessaire,accepted Exemples label,three reinforced Z glyphs,script C0,lower-bound-only final sum,low multiplication period,and all paragraph boundaries and remaining words. Plaçons nous remains the printed two-word wording. No author note.',
 witness='Native372 complete body;capital Id,lexical accents,reinforced Zs,script C0,and the missing upper sum bound resolved.')
r.commit()
