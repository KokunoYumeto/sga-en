#!/usr/bin/env python3
from pathlib import Path
import json
from review_helpers import Review
r=Review();p=362
r.finding('361_365',4,'The page starts operations psi^k;the preceding page ends Les.',
 'Main376 first strip and native373 top agree. Both supplied page markers already precede operations psi^k,so the complete phrase remains on its physical source page.',
 '361/362 marker',witness=373)
r.finding('361_365',5,'The G in the opening functor name has a hat.',
 'Both scans resolve the separate hat. The attached widehat G agrees with this occurrence and the three hatted Gs in7.5.2.',
 'opening paragraph,functor in lambda-rings',witness=373)
r.finding('361_365',6,'The first display has an extra closing parenthesis after its denominator lambda_u(1+Xt).',
 'Both native373 top and main first strip resolve the final handwritten closing stroke. Diplomatic already retains it and current already removes it. There is only one denominator application lambda_u(a),so the extra close has no matching opening.',
 'first display,denominator close',change='Retain existing diplomatic extra close/current balanced denominator.',witness=373)
derivative_reason=('Put R=Ghat(Z[X]) and a=1+Xt in R. Its unit is underlined1=1+t,its addition is multiplication of the represented t-series,and its product is circle. The line-element identity is lambda_u(a)=underlined1+a u in R[[u]]. The formal derivation D_u(sum r_j u^j)=sum j r_j u^(j-1) sends this lambda-series to a. Multiplication by its inverse gives a/(underlined1+a u)=sum_(k>=1)(-1)^(k-1)a^(circle k)u^(k-1). The product law(1+Xt)circ(1+Yt)=1+XYt identifies a^(circle k)=1+X^k t,which is exactly7.4.1. Thus u is the differentiation variable required by the displayed coefficient map;the printed dt is preserved only in diplomatic.')
r.finding('361_365',7,'The first derivative prints d/dt although the lambda-series and coefficient expansion use u.',
 derivative_reason,'first display,differentiation variable',verdict='not applied and now applied',
 change='Current d/du;diplomatic d/dt;all derivative arguments and following coefficients remain exact.',witness=373)
r.patch(p,'current',r'\frac{d}{dt}(\lambda_u(1+Xt))',r'\frac{d}{du}(\lambda_u(1+Xt))','check/findings/findings_361_365.json#7','Use the u-adic derivation that produces the displayed series coefficients.')
r.finding('361_365',8,'The unit1 in the first stacked denominator is underlined.',
 'Native373 top resolves the short separate rule. The supplied underline agrees and distinguishes the multiplicative unit of Ghat,the t-series1+t,from the t-series1 which is its additive zero. The exact ring operations and coefficient map are recorded in identification_362.json.',
 'first display,underlined unit',witness=373)
r.finding('361_365',9,'The operation exponent in7.5(ii) is a lowercase t.',
 'Both sources resolve the ascender/cross-stroke as t. Existing diplomatic psi^t/current psi^k is confirmed. The identities7.5.1 concern the family k↦psi^k indexed by positive integers;the substitution of the family index k for this isolated t refers to those same three identities and does not change the formal series variable t elsewhere.',
 '7.5(ii),operation exponent',change='Retain existing diplomatic psi^t/current psi^k.',witness=373)
r.finding('361_365',10,'Proposition7.5 has six ruled lexical groups in(i) and eight in(ii);all K,psi,lambda-prefixes,item labels,formula numbers and punctuation are plain.',
 'All14 spans are directly visible in primary second strip and native top. They are patched separately around the unchanged formulas. The statement label Proposition remains in the accepted bold-label convention.',
 'complete proposition statement',verdict='not applied and now applied',change='Restore the14 directly observed word-group underlines in both forms.',witness=373)
old=r'i) Si \(K\) est un \(\lambda\)-anneau, les opérations \(\psi^k\) vérifient les identités :'
new=r'i) \uline{Si} \(K\) \uline{est un} \(\lambda\)-\uline{anneau}, \uline{les opérations} \(\psi^k\) \uline{vérifient} \uline{les identités} :'
# The proof begins similarly but contains no operations phrase,so this is unique.
r.patch(p,'both',old,new,'check/findings/findings_361_365.json#10','Restore the six observed groups of7.5(i).')
for layer,index in [('diplomatic','t'),('current','k')]:
 old=r'ii) Réciproquement, si les \(\psi^'+index+r'\) vérifient ces identités, et si \(K\) est de caractéristique nulle, \(K\) est un \(\lambda\)-anneau.'
 new=r'ii) \uline{Réciproquement}, \uline{si les} \(\psi^'+index+r'\) \uline{vérifient ces identités}, \uline{et si} \(K\) \uline{est de} \uline{caractéristique nulle}, \(K\) \uline{est un} \(\lambda\)-\uline{anneau}.'
 r.patch(p,layer,old,new,'check/findings/findings_361_365.json#10','Restore the eight observed groups of7.5(ii),preserving the layer-specific exponent.')
r.finding('361_365',11,'The unit logarithmic-derivative formula continues the proof sentence,followed by et par suite.',
 'The native lower crop shows its continuation punctuation on the same source line. The supplied inline arrangement has the identical mathematical token sequence and punctuation;its inherited display-to-inline change is treated as layout,with no additional content correction. The separate slash denominator is adjudicated in#12.',
 'proof7.5(i),inline formula',verdict='confirmed source layout;no additional content correction',witness=373)
slash_reason=('The source has the unparenthesized solidus1/1+t. The immediately stated lambda_t(1)=1+t gives D_t(lambda_t(1))=1 and hence the formal quotient1/(1+t). Multiplying the following series sum_(k>=1)(-1)^(k-1)t^(k-1) by1+t gives1 coefficientwise. The ungrouped left-associated1/1+t instead has coefficient+1 at t,whereas the displayed series has-1. Current therefore groups only the denominator,as in the other reviewed solidus repairs;diplomatic retains the literal print.')
r.finding('361_365',12,'The proof prints1/1+t on the line,with no enclosing denominator parentheses.',
 slash_reason,'proof7.5(i),unit quotient',verdict='amended',
 change='Diplomatic1/1+t;current1/(1+t),retaining the solidus.',witness=373)
r.patch(p,'current',r'\lambda_t(1)=1/1+t=',r'\lambda_t(1)=1/(1+t)=','check/findings/findings_361_365.json#12','Group the denominator specified by the logarithmic derivative and the geometric series.')
r.finding('361_365',13,'The circle label lies to the left of the middle vertical arrow in7.5.2.',
 'Both sources show the small open circle to the arrow left. The attached label side agrees. It names the product in Ghat(K);the two outer arrows name multiplication in K.',
 '7.5.2,middle vertical label',witness=373)
r.finding('361_365',14,'The two bottom labels lambda_t and Phi^k lie above their rightward arrows.',
 'Both scans show the positions and all arrowheads. The attached labels already agree. The top row has the product maps lambda_t×lambda_t and Phi^k×Phi^k;the lower row has their single maps,and the final comma is printed.',
 '7.5.2,lower horizontal labels',witness=373)
r.page(p,'opérations psi^k définissent','l application derivee logarithmique est',
 'Full main376 four strips and native373 complete body compared. Checked opening page boundary,hatted functor,all u/t variables and derivative arguments,underlined unit and circle powers,extra close,7.4.1 coefficient identity,all three7.5.1 identities,source psi^t,current family indexk,14 lexical rules,proof unit-series formula and slash repair,entire six-object diagram including every arrowhead/label and final comma,quotes and last sentence. No author note.',
 witness='Native373 top/lower;dt,extra close,underlined1,psi exponentt,14 rules,slash denominator,and complete diagram resolved.')
packet={'record_type':'exact_identification','page':362,
 'source_ids':['check/findings/findings_361_365.json#7','check/findings/findings_361_365.json#12'],
 'image':['scan/SGA6_scan_360dpi.pdf#page=376','scan/SGA6_witness_300dpi.djvu#page=373'],
 'u_derivative':derivative_reason,'unit_denominator':slash_reason,
 'patch_scope':'Current changes only dt→du in the first derivative and1/1+t→1/(1+t) in the unit proof;existing paired close and psi-exponent variants remain. Diplomatic retains both newly adjudicated source forms.'}
(Path(__file__).parent/'identification_362.json').write_text(json.dumps(packet,ensure_ascii=False,indent=2)+'\n')
r.commit()
