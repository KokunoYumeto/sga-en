#!/usr/bin/env python3
from pathlib import Path
import json
from review_helpers import Review,read
r=Review();p=360
r.finding('356_360',19,'The physical page begins with the triangle;the preceding page ends at the introductory colon.',
 'The main374 first strip and native371 top contain the whole triangle below the running heading. Both supplied layer markers already stand before its opening display. The arrows are rightward,downward,and diagonally up-right as attached.',
 '359/360 marker and initial triangle',witness=371)
r.finding('356_360',20,'The lower horizontal arrow of the square has Ch(tilde-c0) above it.',
 'Both native and primary square show the label above the arrow. The attached placement agrees. The exact induced map through Gr is recorded separately;no extra Gr glyph is asserted in the printed label.',
 'second diagram,lower arrow label',witness=371)
r.finding('356_360',21,'The lower-left square object prints Ch(Gr wedge)) with two closes after one opening.',
 'Both scans resolve the two distinct closing strokes. The source functor application is Ch applied to the graded ring Gr(wedge),also written correctly in the triangle and preceding sentence. Current removes only the unmatched close;the object and arrow remain unchanged.',
 'second diagram,lower-left object',verdict='not applied and now applied',change='Current has one closing parenthesis;diplomatic retains the two printed closes.',witness=371)
r.patch(p,'current',r'\Ch(\Gr\Lambda))',r'\Ch(\Gr\Lambda)','check/findings/findings_356_360.json#21','Remove the unmatched outer close from the graded-ring functor application.')
r.finding('356_360',22,'The appendix title begins APPENDICE with no preceding paragraph7 label.',
 'The primary and native title both start at APPENDICE. The attached unnumbered section title agrees;the next paragraph is separately numbered7.1.',
 'appendix title',witness=371)
r.finding('356_360',23,'APPENDICE is all capitals and Les starts with a capital L;the lexical title groups are ruled beneath.',
 'The attached capitalization agrees with both scans. The section-title rule is represented by the accepted section-title typesetting convention in NOTE_6;this does not alter any title word or formula. No prose-emphasis rule is extended to this heading.',
 'appendix title capitalization and accepted heading typography',witness=371)
r.finding('356_360',24,'Les applications starts an indented paragraph after7.1.1.',
 'Both scans show the indent. The supplied blank line after the equation already represents it. The equation number,sign exponent,k=1 lower bound,and infinite upper bound agree.',
 'paragraph after7.1.1',witness=371)
wedge_reason=('Actual360 has eight small serifless algebra-name wedges:two in the first triangle,three in the following first paragraph,two in the square,and one in the final graded-ring arrow. Native371 resolves each without a foot or serif. Together with the directly compared356–359 counts10,7,15,6,this closes the historical46-occurrence batch. The replacement names the same augmented filtered ring and acts identically on its elements,graded classes,and universal coefficient maps.')
aggregate=next(x for x in read('decisions.jsonl') if x['source_id']=='check/findings/findings_356_360.json#2').copy()
aggregate.update(verdict='confirmed;all actual356–360 occurrences decided',
 printed_reading='Actual356–360 contain respectively10,7,15,6,8 small serifless algebra-name wedges,46 total.',
 change=r'Use occurrence-scoped \mathord{\wedge} replacements on the46 directly inspected algebra-name glyphs.',
 region='all actual356–360 algebra-name glyphs')
aggregate['reason']+=' '+wedge_reason
aggregate['image']+='; scan/SGA6_scan_360dpi.pdf#page=374; scan/SGA6_witness_300dpi.djvu#page=371'
r.decisions.append(aggregate)
r.own_finding('ASTRA-V-WEDGE-360',p,
 'All eight algebra-name signs are small unadorned wedges.',r'Use eight \mathord{\wedge} glyphs.',
 'Preserve the eight observed glyphs in both forms.',wedge_reason,
 'two diagrams and surrounding proof',kind='symbol',witness=371)
r.patch(p,'both',r'\Lambda',r'\mathord{\wedge}','ASTRA-V-WEDGE-360','Preserve the eight actually observed algebra-name glyphs.',count=8)
r.own_finding('ASTRA-V-PARAGRAPH-360',p,'The paragraph label7.1. is ordinary type.',r'7.1.',
 'Use the observed ordinary paragraph-number weight in both forms.',
 'The native lower crop resolves the same ordinary numeral strokes as surrounding references. This continues the inspected paragraph-number convention for this expose;the identifier7.1 and punctuation remain exact.',
 'paragraph7.1 label',kind='font',witness=371)
r.patch(p,'both',r'\textbf{7.1.}',r'7.1.','ASTRA-V-PARAGRAPH-360','Preserve the ordinary paragraph-number weight.')
r.own_finding('ASTRA-V-INDUCED-CH-360',p,
 'The lower square arrow is labelled Ch(tilde-c0),with no printed Gr inside that label.',
 'Retain the printed abbreviated arrow label.',
 'Record the exact induced graded morphism without adding an unprinted label token.',
 'Let f=tilde-c0 from the named augmented ring B to Ch(Omega). Its filtration-preserving lambda-ring map induces Gr(f):[z] in Gr^i B maps to[f(z)] in Gr_lambda^i Ch(Omega). Ch(Gr(f)) sends(a,1+sum z_i) to(a,1+sum Gr^i(f)(z_i)). These are exactly the printed source and target objects of the bottom arrow. Naturality gives Ch(Gr(f))(tilde-c_B(x))=tilde-c_Ch(Omega)(f(x)),since both have rank epsilon(x) and i-th coefficient the class of gamma^i(f(x)-epsilon(x)). The printed shorthand is thus given a precise map by its stated objects;it is retained in both forms.',
 'second diagram,bottom arrow',kind='exact_identification',verdict='confirmed and retained with exact induced map',witness=371)
r.own_finding('ASTRA-V-SLASH-PRODUCT-360',p,
 'The middle expression of the logarithmic-derivative calculation has a slash followed by lambda_t(x)lambda_t(y),without enclosing denominator parentheses.',
 r'Current /(\lambda_t(x)\lambda_t(y));diplomatic /\lambda_t(x)\lambda_t(y).',
 'Make the entire product denominator explicit in current only.',
 'Write a=lambda_t(x),b=lambda_t(y) in K[[t]]. Both have constant1,so their inverses exist. The defining pre-lambda identity is lambda_t(x+y)=ab. Formal differentiation and multiplication by (ab)^-1 give (ab)prime/(ab)=a-prime/a+b-prime/b. The current parentheses express exactly that identity. In the binomial ring Z with x=y=1,a=b=1+t:the stated quotient is2/(1+t),whereas evaluating the ungrouped slash successively from the left gives2(1+t);their t-coefficients are-2 and2. No sign,index,or derivative argument changes.',
 'first line of final additivity calculation',kind='formula',witness=371)
r.patch(p,'current',r'\frac{d}{dt}(\lambda_t(x)\lambda_t(y))/\lambda_t(x)\lambda_t(y)',
 r'\frac{d}{dt}(\lambda_t(x)\lambda_t(y))/(\lambda_t(x)\lambda_t(y))',
 'ASTRA-V-SLASH-PRODUCT-360','Group the exact product denominator established by the pre-lambda identity and formal derivative.')
r.page(p,'the triangle with tilde-c and tilde-c0','the logarithmic-derivative sum followed by a semicolon',
 'Full main374 four strips and native371 top/lower compared word by word. Checked triangle and square objects,directions and label positions,eight algebra-name wedges,the unmatched closing parenthesis and precise induced Ch map,all surjectivity/injectivity proof clauses,Omega bounded-degree hypothesis,6.11/6.12 references,title words and accepted section typography,plain7.1,Serre attribution,derivative arguments,every Adams index/sign/bound,additivity paragraph,product denominator and final semicolon. No author note.',
 witness='Native371 complete body in two overlapping crops;both diagrams,thin wedge strokes,title rules,and all derivative slash expressions resolved.')
packet={'record_type':'exact_identification','page':360,
 'source_ids':['ASTRA-V-INDUCED-CH-360','ASTRA-V-SLASH-PRODUCT-360'],
 'image':['scan/SGA6_scan_360dpi.pdf#page=374','scan/SGA6_witness_300dpi.djvu#page=371'],
 'induced_graded_map':{'f':'tilde-c0:B→Ch(Omega)','Gr_f':'[z] in Gr^i B →[f(z)] in Gr_lambda^i Ch(Omega)',
 'Ch_Gr_f':'(a,1+sum z_i)→(a,1+sum Gr^i(f)(z_i))',
 'naturality':'Ch(Gr(f)) tilde-c_B=tilde-c_Ch(Omega) f;rank epsilon(x),coefficient_i=[gamma^i(f(x)-epsilon(x))] on both sides.',
 'textual_treatment':'Keep printed Ch(tilde-c0) in both forms,with this exact interpretation determined by the displayed objects.'},
 'product_denominator':{'source':'d/dt(lambda_t(x)lambda_t(y))/lambda_t(x)lambda_t(y)',
 'current':'d/dt(lambda_t(x)lambda_t(y))/(lambda_t(x)lambda_t(y))',
 'identity':'a(0)=b(0)=1;lambda_t(x+y)=ab;(ab)prime(ab)^-1=a-prime a^-1+b-prime b^-1.',
 'evaluation':'K=Z with binomial lambda structure,x=y=1:a=b=1+t;whole-product quotient2/(1+t),left-associated slash expression2(1+t).'}}
(Path(__file__).parent/'identification_360.json').write_text(json.dumps(packet,ensure_ascii=False,indent=2)+'\n')
r.commit()
