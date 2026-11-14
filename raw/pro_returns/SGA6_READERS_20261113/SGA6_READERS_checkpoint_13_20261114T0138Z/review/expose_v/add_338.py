#!/usr/bin/env python3
from review_helpers import Review,HERE
import json
r=Review();p=338
r.finding('336_340',7,'The section heading ends with a full stop after lambda^p(N,x).',
 'Both main352 second strip and native349 top crop show the small final stop. Les has a word rule, covered by the accepted section-heading convention. The supplied terminal punctuation agrees.',
 'section5 heading',witness=349)
r.finding('336_340',8,'On pose starts a new indented paragraph after the displayed polynomial-ring description.',
 'The blank interval and indentation are explicit in both scans. The supplied paragraph separation preserves the observed structure without a new content change.',
 '5.1 before On pose',verdict='formatting observed; no content error',witness=349)
r.finding('336_340',9,'On pose and its lambda-minus-one definition occupy one running line.',
 'The complete main third strip and native overlap show the formula immediately after On pose, with its final full stop. The attached inline version has the identical mathematical tokens and punctuation.',
 '5.1 lambda-minus-one definition',verdict='formatting observed; no content error',witness=349)
r.finding('336_340',10,'The last gamma-hat functor formula continues the line after on a alors and ends with a comma.',
 'The main fourth strip and native lower crop resolve the two products, their upper d and lower i=1, and final comma. The main tight G crop also resolves the small caret. The attached inline formula agrees in content.',
 'last line before339 continuation',verdict='formatting observed; no content error',witness=349)
r.finding('336_340',5,
 'The336 lemma has its seven observed rules;336 Proposition4.12 and337 Remarques4.13/Corollaire4.14 have plain bodies. On338 Corollaire4.15 has eleven lexical rules and Lemme5.2 has two.',
 'The complete336–338 scopes have now been directly compared. The338 rules are Soit; le; anneau engendre sur; par l indeterminee; soumise aux relations; pour; the separate i and e of i.e.; Alors la filtration de; anneau de; est identique a la filtration par le poids par rapport aux. Lemme5.2 rules Pour tout and est divisible par only. Lambda letters, hyphens, formulas, reference4.9 and punctuation remain independent. Later339/340 contain no additional named target in this finding.',
 'all listed statement scopes336–338',verdict='confirmed and now applied in inspected scopes',
 change='Keep seven336 rule patches and add the thirteen338 lexical rules; retain337 plain bodies.',witness=349)
text=(HERE/'page_338_diplomatic.tex').read_text()
old=next(line for line in text.splitlines() if line.startswith(r'\textbf{Corollaire 4.15.}'))
new=r'''\textbf{Corollaire 4.15.} \uline{Soit} \(B'\) \uline{le} \(\lambda\)-\uline{anneau engendré sur} \(K\) \uline{par l'indéterminée} \(X\) \uline{soumise aux relations} \(\gamma^k(X)=0\) \uline{pour} \(k>n\), \uline{i}.\uline{e}. \(B'=K[X,\ldots,\gamma^n X]\) (4.9). \uline{Alors la filtration de} \(\lambda\)-\uline{anneau de} \(B'\) \uline{est identique à la filtration par le poids par rapport aux} \(\gamma^j X\).'''
r.own_finding('ASTRA-V-STATEMENT-RULES-338',p,
 'Thirteen lexical rules: eleven in4.15, including separately ruled i and e, and two in5.2.',
 'Use occurrence-scoped word rules with math and hyphens outside.',
 'Restore the thirteen directly inspected spans.',
 'Native349 top and lower resolve each endpoint. These complete the338 scope of checker336_340#5. This local patch ID keeps the earlier336 patch stable.',
 'Corollaire4.15 and Lemme5.2',witness=349)
r.patch(p,'both',old,new,'ASTRA-V-STATEMENT-RULES-338','Restore eleven4.15 lexical rules.')
r.patch(p,'both',r'\textbf{Lemme 5.2.} Pour tout',r'\textbf{Lemme 5.2.} \uline{Pour tout}','ASTRA-V-STATEMENT-RULES-338','Restore Pour tout in5.2.')
r.patch(p,'both',r'\) est divisible par \(\lambda_{-1}(N)\).',r'\) \uline{est divisible par} \(\lambda_{-1}(N)\).','ASTRA-V-STATEMENT-RULES-338','Restore the second5.2 word rule.')
r.own_finding('ASTRA-V-LOW-DOTS-338',p,
 'The two module-product marks in4.15 proof and the two x-times-lambda-minus-one product marks in5.2 are low dots.',
 r'Use \mathbin{.} at the four occurrences.',
 'Preserve the physical product-dot positions without changing any factor.',
 'All four native349 marks align with the low typed full stops rather than the horizontal middle of the equal signs. Every occurrence was also checked in the main strips.',
 '4.15 proof and5.2 statement/proof',kind='symbol',witness=349)
r.patch(p,'both',r'\cdot',r'\mathbin{.}','ASTRA-V-LOW-DOTS-338','Preserve four low product marks.',count=4)
r.own_finding('ASTRA-V-PARAGRAPH-LABEL-338',p,
 'The label5.1 is ordinary typed text, with no rule or reinforced weight.',
 r'5.1. in place of \textbf{5.1.}.',
 'Restore the inspected paragraph-number form.',
 'Main second strip and native349 top show the same type weight as the following sentence. This is a numbered paragraph rather than one of the ruled statement labels.',
 '5.1 paragraph label',kind='convention',witness=349)
r.patch(p,'both',r'\textbf{5.1.}',r'5.1.','ASTRA-V-PARAGRAPH-LABEL-338','Preserve the ordinary paragraph label.')
r.own_finding('ASTRA-V-INTEGER-FONT-338',p,
 'The first two Z letters in5.1 have visible doubled diagonal strokes. The last Z in the B-construction has joined dark diagonal ink and the same reinforced diagonal footprint.',
 r'Retain the three supplied \mathbb Z occurrences.',
 'Keep this page-local font reading without applying the earlier plain-Z occurrence rule to these loci.',
 'The native top and tight Z comparison crop resolve the separate first two diagonals. The last native zoom and corresponding main crop show the joined dark diagonal with a narrow interior light area near its upper part. The observed reinforcement is retained; no mathematical identification is changed and no global Z macro is altered.',
 '5.1 coefficient rings and final B construction',kind='convention',verdict='retained with occurrence-specific ink observation',witness=349)
r.own_finding('ASTRA-V-AUTHOR-CLAIM-338',p,
 'The proof of4.15 repeats Fil^kB-prime=K.M_k+B-prime.M_(k+1), before concluding that the canonical filtration equals the weight filtration.',
 'Retain the complete proof body and statement; attach the repeated finite-tail defect and the exact quotient verification of the statement.',
 'Separate the false intermediate equality from the valid stated filtration identification.',
 'Take K=Z,n=3,B-prime=Z[X,Y2,Y3],Yj=gamma^jX,k=1. The intermediate right side ZX+B-prime(X^2,Y2) is killed by the map e-prime:B-prime→Z[T],X,Y2↦0,Y3↦T, while Y3 is in Fil^1B-prime and maps to T. The actual quotient q:B→B-prime kills exactly Yj for j>3. More generally, q sends the canonical filtration onto that of B-prime: each augmentation-zero element lifts to one with the same zero augmentation, and every defining gamma product therefore lifts. In the A=K specialization of the proved337 coefficient test, Fil^kB is precisely the span of monomials of weight at least k. Their q-images are precisely the monomials of B-prime of weight at least k. Thus the stated4.15 identification is verified by the explicit quotient map, despite the repeated intermediate defect. Full packet: author_claim_issue_338.json.',
 'Corollaire4.15 proof',kind='author_claim_issue',verdict='source retained; intermediate defect demonstrated and stated identification verified',witness=349)
issue={
 'source_id':'ASTRA-V-AUTHOR-CLAIM-338','page':338,'record_type':'author_claim_issue',
 'verdict':'printed reading retained; repeated intermediate equality fails; corollary statement verified',
 'image':['scan/SGA6_scan_360dpi.pdf#page=352','scan/SGA6_witness_300dpi.djvu#page=349'],
 'links':['review/expose_v/author_claim_issue_336.json','review/expose_v/identification_337.json'],
 'printed_intermediate':'Fil^k B-prime=K.M_k+B-prime.M_(k+1).',
 'counterexample':{
  'parameters':'K=Z with its binomial lambda-structure,n=3,k=1.',
  'ring':'B-prime=Z[X,Y2,Y3],Yj=gamma^jX, obtained from B by the lambda-ideal generated by Yj for j>3 as in4.8/4.9.',
  'right_side':'ZX+B-prime(X^2,Y2).',
  'left_member':'Y3=gamma^3X belongs to Fil^1B-prime because X has augmentation0.',
  'map':'e-prime:B-prime→Z[T],X↦0,Y2↦0,Y3↦T,integers fixed.',
  'comparison':'The right side maps to0; Y3 maps toT≠0.'
 },
 'exact_statement_verification':{
  'map':'q:K[Y1,Y2,...]→K[Y1,...,Yn],Yj↦Yj for j<=n and Yj↦0 for j>n; this is the lambda-quotient of4.8/4.9, compatible with augmentation.',
  'surjectivity_on_filtration':'For any b-prime of augmentation0, choose a polynomial lift b. Since epsilon_B=epsilon_Bprime composed with q, this lift has augmentation0. Every product of gamma^i(b-prime) defining Fil^kB-prime lifts to the corresponding product in Fil^kB, and its arbitrary coefficient also lifts. Hence q(Fil^kB)=Fil^kB-prime.',
  'source_weight_calculation':'For A=K with identity augmentation, Fil^rK=0 for r>=1. The complete coefficient proof in identification_337.json therefore identifies Fil^kB with the K-span of all gamma-coordinate monomials of weight at least k.',
  'image_weight_calculation':'q kills a monomial containing any Yj with j>n and fixes each other monomial with its weight unchanged. Its image is exactly the K-span of weight-at-least-k monomials in B-prime. This proves the printed corollary statement through the actual quotient map.'
 },
 'editorial_action':'Retain the printed body in both forms; record the exact intermediate defect and the independently verified stated identification. No replacement theorem is inserted.'
}
(HERE/'author_claim_issue_338.json').write_text(json.dumps(issue,ensure_ascii=False,indent=2)+'\n')
r.page(p,'Corollaire4.15. Soit B-prime','product_(i=1)^d(1+N_i t),',
 'Full four main352 strips and native349 top/lower compared. Checked all4.15 rules, indices and its repeated finite tail, section-title terminal stop, ordinary5.1, three local reinforced Z forms, four baseline ellipses, exact lambda-minus-one finite sum,5.2 word rules and low products, every N_i index and bound, the final G-hat caret in a main tight crop, and the final comma. Source claims remain separate from scan decisions; no author note.',
 witness='Native349 top/lower and Z comparison/zoom; main_338_Z_last.png and main_338_G.png.')
r.commit()
