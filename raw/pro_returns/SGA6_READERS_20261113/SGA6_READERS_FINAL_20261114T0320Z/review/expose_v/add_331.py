#!/usr/bin/env python3
from review_helpers import Review,HERE
import json
r=Review();p=331
r.finding('331_335',1,'331 begins with3.10 Soit A une K-lambda-algebre augmentee.;330 ends dans la suite.',
 'Both complete331 scans and the previously compared330 bottom confirm the boundary. The marker now precedes the paragraph numeral, as printed. Its missing terminal stop was independently decided in findings_331_335#2 at this same actual331 locus.',
 '330/331 boundary',witness=342)
r.own_finding('ASTRA-V-PARAGRAPH-331',p,'The opening paragraph number3.10 has ordinary typed weight and no rule.',
 r'Diplomatic3.10; current3.10., with textbf removed from both.',
 'Remove the added weight while retaining the already established terminal-punctuation variant.',
 'The native342 top crop and main first strip show the numeral group as plain typed text. The current-only full stop remains tied to the separately recorded source omission.',
 'paragraph number3.10',kind='font',witness=342)
r.patch(p,'diplomatic',r'\textbf{3.10}','3.10','ASTRA-V-PARAGRAPH-331','Preserve plain numeral weight and the printed absence of a terminal stop.')
r.patch(p,'current',r'\textbf{3.10.}','3.10.','ASTRA-V-PARAGRAPH-331','Preserve plain numeral weight and the recorded corrected terminal stop.')
r.own_finding('ASTRA-V-ELLIPSES-331',p,
 'The four triples of typed stops in3.10.1 and3.10.2 lie on the baseline: each gamma-product and each i_1+...+i_k sum.',
 r'Replace the four local \cdots by \ldots.',
 'Use baseline ellipses in precisely the four inspected occurrences.',
 'The native top crop resolves all four triples below the mid-height plus bars; the main strips agree. No other dots or punctuation are changed.',
 '3.10.1 and3.10.2, product and index-sum ellipses',kind='symbol',witness=342)
r.patch(p,'both',r'\cdots',r'\ldots','ASTRA-V-ELLIPSES-331','Preserve the four inspected baseline ellipses.',count=4)
r.own_finding('ASTRA-V-GENERATION-331',p,
 'The proof prints x=sum_i x_alpha_i and later x=sum_i x_alpha_i-epsilon(x_alpha_i), with no signed integer coefficients and no parentheses around the final difference.',
 'Retain the literal displayed/inline formulas in both forms.',
 'Keep the printed shorthand and record an explicit coefficient calculation covering the stated abelian-group generation hypothesis.',
 'The native top crop resolves the three sums, their i indices and the unparenthesized final difference. Set y_alpha=x_alpha-epsilon(x_alpha). For an actual finite integral representation x=sum_alpha m_alpha x_alpha with epsilon(x)=0, additivity gives x=sum_alpha m_alpha y_alpha. Relation3.4.1 gives gamma_t(x)=product_alpha gamma_t(y_alpha)^{m_alpha}. Negative exponents are expanded by(1+U)^(-q)=sum_{l>=0}(-1)^l binom(q+l-1,l)U^l, q a positive integer. Every coefficient of t^r is an integral polynomial in gamma^s(y_alpha) whose monomials have total weight r. Also every a in A has a=epsilon(a)+sum_alpha m_alpha gamma^1(y_alpha). These explicit expansions identify the K-span of the printed products3.10.2 with the ideal in3.10.1, including negative coefficients. Full calculation is recorded in identification_331.json; no replacement prose or extra term is inserted into the source.',
 'proof of the generating-family assertion3.10.2',kind='notation',verdict='printed reading decided and retained; exact calculation supplied',witness=342)
packet={
 'source_id':'ASTRA-V-GENERATION-331','page':331,'record_type':'exact_identification',
 'verdict':'printed shorthand retained; explicit coefficient identification',
 'image':['scan/SGA6_scan_360dpi.pdf#page=345','scan/SGA6_witness_300dpi.djvu#page=342'],
 'region':'paragraph following3.10.2',
 'evidence_files':['review/expose_v/page_331_s2.png','review/expose_v/witness_331_top.png'],
 'source_hypotheses':'A is the given augmented K-lambda-algebra and the displayed family(x_alpha) generates its underlying abelian group; epsilon:A→K is its augmentation.',
 'printed_readings':['x=sum_i x_alpha_i','sum_i epsilon(x_alpha_i)=0','x=sum_i x_alpha_i-epsilon(x_alpha_i)'],
 'maps':{
  'coefficient_map':'psi:K[Y_(alpha,r) | r>=1]→A, Y_(alpha,r)↦gamma^r(y_alpha), with y_alpha=x_alpha-epsilon(x_alpha); K acts via the specified K-algebra structure.',
  'augmentation':'epsilon:A→K; epsilon(y_alpha)=0.',
  'gamma':'gamma_t:(A,+)→(1+tA[[t]], multiplication), from3.4.1.'
 },
 'calculation':[
  'Give Y_(alpha,r) weight r. Let M_n be the K-span of psi-images of monomials of weight at least n, precisely the products3.10.2.',
  'For the actual finite integral representation x=sum_alpha m_alpha x_alpha and epsilon(x)=0, one has x=sum_alpha m_alpha y_alpha.',
  'gamma_t(x)=product_alpha gamma_t(y_alpha)^{m_alpha}. Nonnegative powers expand by multiplication. For m_alpha=-q<0, use(1+U)^(-q)=sum_l>=0(-1)^l binom(q+l-1,l)U^l with U=gamma_t(y_alpha)-1.',
  'For a fixed coefficient t^r only l<=r contributes. Each monomial has total weight r because the exponents of t add to r. Thus gamma^r(x) belongs to the weight-r span of psi-images.',
  'Every a in A has a=epsilon(a)+sum_alpha m_alpha y_alpha=epsilon(a)+sum_alpha m_alpha gamma^1(y_alpha). Multiplying a weight-at-least-n monomial by a gives terms of weight at least n, so M_n is an A-ideal.',
  'All generators3.10.1 lie in M_n by coefficient expansion, so Fil^n A is contained in M_n. Each printed3.10.2 product uses the augmentation-zero y_alpha and is a generator allowed in3.10.1, so M_n is contained in Fil^n A.',
  'The two inclusions are the identity maps on their common subsets of A. This proves the exact equality used by the printed assertion and handles all integer signs without altering the source.'
 ],
 'change':'No source-text emendation; retain the printed unsigned-sum shorthand and absent grouping parentheses.',
 'forms':'French diplomatic/current and corresponding English transfer'
}
(HERE/'identification_331.json').write_text(json.dumps(packet,ensure_ascii=False,indent=2)+'\n')
r.page(p,'3.10 Soit A une K-lambda-algebre augmentee.','de la filtration ci-dessus.',
 'All four main strips and both native342 crops compared in full. Checked the exact paragraph-number variant, both complete products and their index inequalities, all four baseline ellipses, epsilon augmentation arrow, alpha subscripts, all three proof sums and the absence of added coefficients/grouping, gamma^1 identity, both references, plain Fil and Ker glyphs, Fil^0/Fil^1 and every sentence of the final two paragraphs. No author note.',
 witness='Native342 top/lower: witness_331_top.png and witness_331_lower.png.')
r.commit()
