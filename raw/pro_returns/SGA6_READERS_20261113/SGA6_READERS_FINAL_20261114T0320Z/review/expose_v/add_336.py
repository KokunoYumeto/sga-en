#!/usr/bin/env python3
from review_helpers import Review,HERE
import json
r=Review();p=336
r.finding('336_340',1,'The page begins on definit un lambda-homomorphisme:B→K;335 ends sur A;.',
 'Both main350 and native347 first lines resolve on as the first word. The previous335 ending was fully compared. The supplied marker places on on336 and leaves the normal interword space before definit.',
 '335/336 boundary',witness=347)
r.finding('336_340',2,'The first paragraph literally prints K-lambda-algebre augmentes, with masculine plural ending.',
 'Both scans resolve the line-broken augmen-tes. Its noun algebre is feminine singular, as in the immediately preceding335 definition of A. Preserve augmentes diplomatically and correct this occurrence to augmentee in the current layer.',
 'first paragraph, algebra augmentation',verdict='confirmed and now applied in current',change='Current augmentés becomes augmentée; diplomatic ending retained.',witness=347)
r.patch(p,'current','algèbre augmentés.','algèbre augmentée.','check/findings/findings_336_340.json#2','Restore the agreement of the singular feminine algebra noun in the current layer.')
r.finding('336_340',3,'The lemma statement ends with(dans A) and no terminal full stop.',
 'The main second strip and native top crop show blank space after the final parenthesis. The supplied absence of punctuation agrees.',
 'Lemme4.11 statement end',witness=347)
r.finding('336_340',4,'Si epsilon designe begins an indented new paragraph after augmentation nulle.',
 'Both main and native top crops resolve the break. The supplied separation agrees without a new content change.',
 'Lemme4.11 proof paragraph boundary',verdict='formatting observed; no content error',witness=347)
r.finding('336_340',5,
 'The336 lemma has seven word rules: Soit; le coefficient d un monome de poids; par rapport; aux; dans; est de filtration au moins; dans. Proposition4.12 has no underlined mathematical body.',
 'Each endpoint is resolved in native347. The formula, a membership statement, k-n and A remain outside the lexical rules. Restore the seven336 spans now. The listed338 statements and the337 remark/corollary remain separate page scopes until their images are personally compared.',
 '336 Lemme4.11 and Proposition4.12 only; later listed pages separately scoped',verdict='336 scope confirmed;338 continuation separately scoped',change='Restore the seven inspected336 lemma rules, with no new emphasis on4.12.',witness=347)
text=(HERE/'page_336_diplomatic.tex').read_text()
old=next(line for line in text.splitlines() if line.startswith(r'\textbf{Lemme 4.11.}'))
new=r'''\textbf{Lemme 4.11.} \uline{Soit} \(a\in A\)~; \uline{le coefficient d'un monôme de poids} \(n\) \uline{par rapport} \uline{aux} \(\gamma^j X\) \uline{dans} \(\gamma^k(aX)=P'_k(\gamma^i(a),\gamma^j X)\) \uline{est de filtration au moins} \(k-n\) (\uline{dans} \(A\))'''
r.patch(p,'both',old,new,'check/findings/findings_336_340.json#5','Restore the seven336 lexical rules only.')
r.own_finding('ASTRA-V-COEFFICIENT-PARAMETER-336',p,
 'The expansion of gamma_t(epsilon(a)X) and the following prose both print R_(n,a), without epsilon around a.',
 r'Current R_{n,\epsilon(a)} at both occurrences; diplomatic R_{n,a}.',
 'Restore the exact scalar parameter epsilon(a) in the current coefficient polynomial and its repeated name.',
 'Native347 lower and its tight R crop resolve the bare a in both indices. Definition2.9 and3.8 give R_(n,c) as the coefficient of the scalar-power operation phi↦phi^c. Here the displayed exponent is exactly epsilon(a), so the parameter map is A→K, a↦epsilon(a). In degree1 the left expression has coefficient epsilon(a)X, while the printed R_(1,a) yields aX. For K=Z and A the free lambda-ring on U augmented by U↦0, a=U gives0 versus UX in the underlying polynomial ring B. The map setting all other independent generators to0 sends UX to the nonzero monomial UX in Z[U,X]. The coordinator independently confirmed the same defect using a Laurent line element L of augmentation1. Full identification: identification_336.json.',
 'Lemme4.11 proof, two R-polynomial indices',kind='misprint_in_print',witness=347)
r.patch(p,'current',r'R_{n,a}',r'R_{n,\epsilon(a)}','ASTRA-V-COEFFICIENT-PARAMETER-336','Use the scalar epsilon(a) fixed by the displayed exponent.',count=2)
r.own_finding('ASTRA-V-LOW-DOTS-336',p,
 'Five product dots and the single ellipsis in4.12 are low typed marks: one gamma-series product dot, one R-series dot, and three module-product dots.',
 r'Use \mathbin{.} for those five product marks and \ldots for the one ellipsis.',
 'Preserve the directly observed baseline positions without changing any factor or subscript.',
 'Native347 lower shows every dot beside the lower part of the adjacent typed character, below the plus/equality bars. The ellipsis in4.12 is on that same baseline. Each replacement is anchored separately from the other dot controls.',
 'Lemme4.11 proof and4.12 display',kind='symbol',witness=347)
r.patch(p,'both',r'\cdot\gamma_t',r'\mathbin{.}\gamma_t','ASTRA-V-LOW-DOTS-336','Preserve the gamma-series product dot.')
r.patch(p,'both',r'\cdot t^n',r'\mathbin{.}t^n','ASTRA-V-LOW-DOTS-336','Preserve the R-series product dot.')
r.patch(p,'both',r'\cdot M',r'\mathbin{.}M','ASTRA-V-LOW-DOTS-336','Preserve the three module-product dots.',count=3)
r.patch(p,'both',r'\cdots',r'\ldots','ASTRA-V-LOW-DOTS-336','Preserve the one baseline ellipsis.')
r.own_finding('ASTRA-V-AUTHOR-CLAIM-336',p,
 'M_k is expressly the set of monomials of weight exactly k, and Proposition4.12 ends with B.M_(k+1).',
 r'Retain \Fil^k B=\Fil^k A+\Fil^{k-1}A.M_1+...+\Fil^0 A.M_k+B.M_{k+1} as printed in both layers.',
 'Preserve the source assertion and attach its explicit counterexample; propose no replacement theorem.',
 'Take the printed construction with K=A=Z and identity augmentation. By4.3/4.10, B=Z[X,Y_2,Y_3,...], Y_j=gamma^j X, with augmentation evaluating every generator to0. At k=1, M_1={X}, M_2={X^2,Y_2}, and Fil^1 A=0, so the displayed right side is ZX+B(X^2,Y_2). The ordinary ring map e:B→Z[T] sends X,Y_2 and every Y_j exceptY_3 to0, and Y_3 toT. It sends the entire right side to0. But Y_3=gamma^3 X lies in Fil^1 B directly from3.10.1, since epsilon(X)=0 and3>=1, and e(Y_3)=T. This concrete map proves the asserted equality fails for the explicitly defined M_k. The coordinator independently checked the example. Full packet: author_claim_issue_336.json; dependent later claims require separately viewed source records.',
 'definition of M_k and Proposition4.12',kind='author_claim_issue',verdict='source reading decided and retained; author-claim defect demonstrated',witness=347)
r.own_finding('ASTRA-V-PARENTHESIS-INK-336',p,
 'The first outer opening parenthesis after the first R_(n,a) has a short leftward ink branch; the two opening and two closing parentheses around the gamma-family remain identifiable.',
 r'Retain ((\gamma^j X)) at this locus.',
 'Record the damaged opening stroke without adding an extra mathematical symbol.',
 'The tight native R crop shows the leftward branch attached to the outer opening-parenthesis stroke. The next opening parenthesis and two closing parentheses are distinct; the coefficient polynomial is applied to the displayed family. No independent extra character is resolved from that attached ink.',
 'first R-polynomial argument, outer opening parenthesis',kind='physical_ink',verdict='damaged stroke recorded; parenthesis reading retained',witness=347)
ident={
 'source_id':'ASTRA-V-COEFFICIENT-PARAMETER-336','page':336,'record_type':'exact_identification',
 'image':['scan/SGA6_scan_360dpi.pdf#page=350','scan/SGA6_witness_300dpi.djvu#page=347'],
 'region':'coefficient expansion after gamma_t(aX) factorization',
 'printed':'gamma_t(epsilon(a)X)=(gamma_t(X))^{epsilon(a)}=sum_n>=0 R_(n,a)((gamma^j X))t^n; les R_(n,a)',
 'corrected':'Replace exactly the two scalar parameters a by epsilon(a).',
 'parameter_map':'epsilon:A→K, a↦epsilon(a). R_(n,c) is the coefficient polynomial for phi↦phi^c from2.9/3.8.',
 'degree_one_check':'R_(1,c)(Y_1,...)=cY_1, hence required coefficient epsilon(a)X rather than aX.',
 'example':{
  'K':'Z with binomial lambda-structure',
  'A':'Free lambda-ring Z[U,lambda^2U,lambda^3U,...], with the lambda-augmentation U↦0 and every higher generator↦0.',
  'a':'U',
  'B':'A[X,gamma^2X,gamma^3X,...], the exact free gamma-coordinate algebra in4.3/4.10.',
  'comparison':'epsilon(U)X=0; the printed R_(1,U) coefficient is UX.',
  'nonvanishing_map':'The underlying polynomial-ring evaluation B→Z[U,X] fixes U,X and sends every other independent generator to0, so UX maps to UX≠0.'
 },
 'independent_check':'Coordinator supplied K=Z,A=Z[L,L^-1], a=L a line element, epsilon(L)=1: the coefficient difference is(L-1)X, nonzero in the underlying polynomial extension.',
 'forms':'French diplomatic retains bare a; current and corresponding corrected English use epsilon(a).'
}
(HERE/'identification_336.json').write_text(json.dumps(ident,ensure_ascii=False,indent=2)+'\n')
issue={
 'source_id':'ASTRA-V-AUTHOR-CLAIM-336','page':336,'record_type':'author_claim_issue',
 'verdict':'printed reading decided and retained; counterexample established',
 'image':['scan/SGA6_scan_360dpi.pdf#page=350','scan/SGA6_witness_300dpi.djvu#page=347'],
 'evidence_files':['review/expose_v/witness_336_top.png','review/expose_v/witness_336_lower.png','review/expose_v/witness_336_412.png'],
 'source_definition':'M_k is explicitly the set of monomials of weight k in the independent variables gamma^j X, with weight(gamma^j X)=j.',
 'source_claim':r'\Fil^k B=\Fil^k A+\Fil^{k-1}A.M_1+\cdots+\Fil^0 A.M_k+B.M_{k+1}',
 'example':{
  'K_and_A':'K=A=Z, binomial lambda-structure, epsilon_A=id_Z.',
  'B':'Z[X,Y_2,Y_3,...], Y_j=gamma^j X; augmentation epsilon_B evaluates every displayed variable to0.',
  'k':1,'M_1':['X'],'M_2':['X^2','Y_2'],
  'right_side':'Z X+B(X^2,Y_2)',
  'left_member':'Y_3=gamma^3 X belongs to Fil^1 B by3.10.1: epsilon_B(X)=0 and3>=1.',
  'comparison_map':'e:B→Z[T], X↦0,Y_2↦0,Y_3↦T,Y_j↦0 for every j>=4; integers fixed.',
  'images':'e(ZX+B(X^2,Y_2))={0}, whereas e(Y_3)=T≠0.',
  'conclusion':'The displayed equality4.12 fails with M_k defined exactly as printed.'
 },
 'scope_limit':'This evaluation is an ordinary ring map used to separate the two indicated subsets. No lambda-homomorphism property of e is claimed or needed.',
 'editorial_action':'Retain the source body in both forms. Link an explicit author-claim note. No replacement theorem or amended tail formula is proposed.',
 'independent_review':'Coordinator independently confirmed the exact-weight definition and the k=1 evaluation obstruction.',
 'dependent_scope':'337 continuation and subsequent claims will receive their own actual image decisions.'
}
(HERE/'author_claim_issue_336.json').write_text(json.dumps(issue,ensure_ascii=False,indent=2)+'\n')
r.page(p,'on definit un lambda-homomorphisme:B→K','avec epsilon(b)=0, ces elements',
 'Complete word/symbol comparison in four main strips and native347 top/lower. Checked augmentes, exact-weight M_k definition, seven lemma rules and absent terminal stop, all P-primes and weights, both R_(n,a) occurrences and their exact parameter repair, all five low product dots and baseline ellipsis, attached damaged parenthesis stroke, literal4.12 tail and every filtration exponent, both following paragraphs and unfinished last phrase. The author-claim defect is separately decided and documented, not a pending scan reading. No author note.',
 witness='Native347 top/lower plus R and4.12 crops: witness_336_top.png, witness_336_lower.png, witness_336_R.png, witness_336_R_zoom.png, witness_336_412.png.')
r.commit()
