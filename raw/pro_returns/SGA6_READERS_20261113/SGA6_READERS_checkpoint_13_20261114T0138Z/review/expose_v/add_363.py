#!/usr/bin/env python3
from pathlib import Path
import json
from review_helpers import Review
r=Review();p=363
r.finding('361_365',15,'The page begins un homomorphisme;the preceding page ends est.',
 'Both main377 first strip and native374 top show the initial un. The supplied markers already agree and preserve the sentence across the boundary.',
 '362/363 marker',witness=374)
for source in ['fixes/FIXLOG_6.jsonl#1600','fixes/FIXLOG_6_CURRENT.jsonl#1689']:
 r.source(source,'The page starts un homomorphisme.',
  'The exact marker move is independently confirmed by both page363 top views and the already inspected362 ending. The supplied marker is in the observed place.',
  '362/363 marker',witness=374,page=363,change='Retain the supplied marker before un homomorphisme.')
r.finding('361_365',16,'The isolated Phi(1+Yt)=Y^k has no superscript on Phi.',
 'Native374 top confirms the blank superscript position. Existing diplomatic Phi/current Phi^k is retained. The map defined in the first paragraph is Phi^k(f)=(-1)^(k-1)[t^(k-1)](f-prime/f). Substituting f=1+Yt gives Y^k,identifying this occurrence with the same indexed map as its immediately preceding X formula.',
 'first two elementary-series evaluations',change='Retain existing diplomatic Phi/current Phi^k.',witness=374)
r.finding('361_365',17,'The multiplicativity calculation continues to ce qui donne le resultat in the same source sentence.',
 'Both scans show the complete formula and its following comma. The supplied inline formula has the same content and punctuation;the inherited inline/display arrangement is a layout decision,with no additional content patch.',
 'multiplicativity calculation',verdict='confirmed source layout;no additional content correction',witness=374)
r.finding('361_365',18,'The bottom label Phi^k is above the lower arrow of7.5.3.',
 'Both scans resolve the label above the shaft. Diplomatic already matches;current preserves that side while reversing the erroneous arrow under#19.',
 '7.5.3,bottom label position',witness=374)
arrow_reason=('The first paragraph defines Phi^k:Ghat^t(K)→K by f↦(-1)^(k-1)[t^(k-1)](f-prime/f). Hence the lower-right object is its domain and the lower-left K its codomain. More explicitly,the upper/right route sends1+Xt to lambda_u(1+Xt) and then to(1+Xt)^(circle k-prime)=1+X^(k-prime)t. Applying Phi^k gives X^(kk-prime),which is the value of the left vertical Phi^(kk-prime) on1+Xt. This is exactly the two displayed calculations immediately below the square,and fixes the lower arrow right-to-left without changing any object or label.')
r.finding('361_365',19,'The bottom arrowhead of7.5.3 is at the right,end at Ghat^t(K).',
 arrow_reason,'7.5.3,bottom arrow direction',verdict='not applied and now applied',
 change='Current lower arrow Ghat^t(K)→K;diplomatic retains K→Ghat^t(K). The label remains above.',witness=374)
r.patch(p,'current','K '+r'\arrow[r,"\Phi^k"]'+' &\n'+r'\widehat G^t(K),',
 'K &\n'+r'\widehat G^t(K), \arrow[l,"\Phi^k"'+"']",
 'check/findings/findings_361_365.json#19','Orient the bottom arrow by the explicitly defined coefficient map and the following generator calculation.')
r.finding('361_365',20,'The two displayed elementary-series calculations follow one another with no intervening word.',
 'Main third strip and native lower contain no puis or other prose between the two lines. The supplied absence of puis agrees. Their semicolon and final stop also agree.',
 'two calculations below7.5.3',witness=374)
for index,phrase in [(21,'Par suite'),(23,'Par ailleurs')]:
 r.finding('361_365',index,phrase+' begins an indented paragraph.',
  'Both lower scans show the indent and paragraph separation. The supplied blank line already agrees;the complete following composition remains on the same physical page.',
  phrase+' paragraph boundary',witness=374)
for index,phrase in [(22,'Par suite'),(24,'Par ailleurs')]:
 r.finding('361_365',index,'The '+phrase+' formula follows those words in the same source line and ends with a full stop.',
  'Native374 lower resolves every composition circle,including the faint circles after the final Phi^k in both paragraphs. The attached formulas and punctuation agree. The inherited inline/display arrangement is accepted as layout;no new content change follows from it.',
  phrase+' formula placement and complete composition',verdict='confirmed source layout;no additional content correction',witness=374)
coeff_reason=('The page first defines Phi^k(f)=(-1)^(k-1)[t^(k-1)](f-prime/f). For f=1+Xt,formal differentiation gives f-prime/f=X/(1+Xt)=sum_(j>=0)(-1)^j X^(j+1)t^j. Its(k-1)-st coefficient is(-1)^(k-1)X^k. Multiplication by the sign from the definition gives X^k. Equivalently,the coefficient of t^(k-1) in(-1)^(k-1)X/(1+Xt) is exactly X^k,so inserting that factor inside the parenthetical coefficient-series repairs only the omitted sign. The denominator parentheses group the same formal inverse;the source solidus is retained. At k=2 in Z[X],the unsigned source coefficient is-X^2,whereas Phi^2(1+Xt)=X^2. No coefficient number or exponent is changed.')
r.own_finding('ASTRA-V-COEFFICIENT-363',p,
 'The parenthesis calls X^k the(k-1)-ieme coefficient of X/1+Xt,with no sign factor and no denominator parentheses.',
 r'Current coefficient-series (-1)^{k-1}X/(1+Xt);diplomatic X/1+Xt.',
 'Restore the omitted coefficient sign and explicit denominator grouping in current only.',
 coeff_reason,'parenthetical coefficient description after Phi^k(1+Xt)=X^k',kind='formula',witness=374)
r.patch(p,'current',r'\text{$(k-1)$-ième coefficient de }X/1+Xt',
 r'\text{$(k-1)$-ième coefficient de }(-1)^{k-1}X/(1+Xt)',
 'ASTRA-V-COEFFICIENT-363','Use the exact coefficient series obtained from the definition of Phi^k.')
r.own_finding('ASTRA-V-UNIT-363',p,
 'The first1 in Phi_u^(k-prime)(1+{1+Xt}u) is plain,without an underline.',
 'Retain this plain1 occurrence.',
 'Identify the unit of the coefficient ring in the displayed formal u-series without adding an unprinted rule.',
 'The expression is a formal u-series over R=Ghat^t(K). Its scalar1 is the unit1_R,whose represented t-series is1+t by the circle-product identity. The unit map Z→R sends n to(1+t)^n under the underlying t-series representation. Thus this plain formal-series1 and the underlined1 on362 name the same explicitly identified unit in their respective displays. The source occurrence remains plain in both forms;no rule is inferred from362.',
 'first calculation below7.5.3,plain coefficient-ring unit',kind='exact_identification',verdict='confirmed and retained with exact unit map',witness=374)
r.page(p,'un homomorphisme de groupes','Par ailleurs ... Phi^k circ lambda_t circ psi^(k-prime).',
 'Full main377 four strips and native374 complete body compared. Checked the initial signed-coefficient definition and map composition,all hatted functors and script C0,the elementary X/Y evaluations including missing Phi exponent,the newly adjudicated parenthetical sign and slash grouping,complete7.5.3 square with all arrowheads and label positions,the source plain formal-series unit,the two succeeding calculations without added prose,and both last paragraphs. Native lower resolves all faint composition circles. No prose rule or author note.',
 witness='Native374 top/lower complete body;coefficient parenthesis,missing Phi exponent,wrong-way arrow,plain unit,and all final composition circles resolved.')
packet={'record_type':'exact_identification','page':363,
 'source_ids':['check/findings/findings_361_365.json#19','ASTRA-V-COEFFICIENT-363','ASTRA-V-UNIT-363'],
 'image':['scan/SGA6_scan_360dpi.pdf#page=377','scan/SGA6_witness_300dpi.djvu#page=374'],
 'bottom_arrow':arrow_reason,'coefficient_parenthesis':coeff_reason,
 'coefficient_ring_unit':'For R=Ghat^t(K),the scalar map Z→R sends n to(1+t)^n;the printed plain1 in the formal u-series is1_R represented by1+t. Retain the plain source glyph.'}
(Path(__file__).parent/'identification_363.json').write_text(json.dumps(packet,ensure_ascii=False,indent=2)+'\n')
r.commit()
