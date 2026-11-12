#!/usr/bin/env python3
"""Context-reviewed odd-index English formula reconstructions.

Run after english_stage/english_variants have written their stable ledgers.
Exact source passages, not fuzzy substitutions, are used in the decisions.
"""
import json
import re
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
WORK=ROOT/'work'
LEDGER=json.loads((WORK/'en_formula_unmapped.json').read_text())
COMPONENTS=json.loads((WORK/'en_components.json').read_text())
TEXTS={(c['volume'],c['component']):c['text'] for c in COMPONENTS}
RES={}


def source(i,page=None):
    x=LEDGER[i]
    return f"ED-EN-FORMULA-G{i:03d}; fr/{'sga7i' if x['volume']=='7I' else 'sga7ii'}/{{diplomatic,current}}/expose_{x['expose']}_body.tex; folio {page or x.get('page','see context')}"


def key_component(vol,prefix):
    matches=[k[1] for k in TEXTS if k[0]==vol and k[1].rsplit('/',1)[-1].startswith(prefix)]
    assert len(matches)==1,(prefix,matches)
    return matches[0]


def variant(i,comp,corrected,printed,reason,page=None,start=None):
    x=LEDGER[i];text=TEXTS[(x['volume'],comp)]
    if start is None:
        assert text.count(corrected)==1,(i,comp,corrected,text.count(corrected))
        start=text.index(corrected)
    assert text[start:start+len(corrected)]==corrected,(i,start)
    assert corrected!=printed,i
    RES[i]=dict(index=i,status='variant',volume=x['volume'],component=comp,
                start=start,corrected=corrected,printed=printed,source=source(i,page),
                page=str(page or x.get('page','')),reason=reason)


def exact(i,prefix,corrected,printed,reason,page=None):
    variant(i,key_component(LEDGER[i]['volume'],prefix),corrected,printed,reason,page)


def candidate(i,replacements,k=0,reason=None):
    c=LEDGER[i]['target_candidates'][k];old=c['body'];new=old
    for a,b in replacements:
        assert a in new,(i,a)
        new=new.replace(a,b)
    variant(i,c['component'],old,new,reason or 'The displayed equation and its label identify the English counterpart; restore only the attested printed mathematical reading.',start=c['start'])


def aligned(i,printed,reason):
    x=LEDGER[i]
    variant(i,x['component'],x['english'],printed,reason,start=x['start'])


def covered(i,which,reason):
    x=LEDGER[i];RES[i]=dict(index=i,status='covered',volume=x['volume'],source=which,page=str(x.get('page','')),reason=reason)


def no_counterpart(i,reason,page=None):
    x=LEDGER[i];RES[i]=dict(index=i,status='no_counterpart',volume=x['volume'],source=source(i,page),page=str(page or x.get('page','')),reason=reason)


def run():
    candidate(1,[(r'\phi_n(\sigma)',r'\phi_n(u)')])
    candidate(3,[(r'n-d(y)',r'n-d(g)')],reason='Both occurrences of n-d(y) in this combined English display correspond to the two printed n-d(g) readings on folio 16; one operation covers ledger entries 3 and 4.')
    exact(5,'08_expose_II',r'replace $U$ by $U\cap U_1$',r'replace by $U\cap U_1$',
          'The diplomatic French omits the object U after remplacer; the corrected source supplies it. Preserve that omission in diplomatic English.',27)
    covered(7,'ED-EN-FORMULA-E006','Covered by the complete Definition 2.1 reconstruction, including both extension structures.')
    covered(9,'ED-EN-FORMULA-E010','Covered by the complete closing clause of Definition 2.1, including the extension structure.')
    exact(11,'75_expose_VII',
          'trivialized over $P\\times1_Q$ by\n$e_{E/P}$, and over $1_P\\times Q$ by $e_{E/Q}$',
          'trivialized over $1_P\\times Q$ by\n$e_{E/P}$, and over $P\\times1_Q$ by $e_{E/Q}$',
          'The printed two trivialization loci are interchanged. Restore both in one passage; this covers ledger 11 and 12.',160)
    covered(13,'ED-EN-FORMULA-E014','The current explanatory morphism is part of the single corrected E_o-construction paragraph; the complete paragraph is reconstructed together.')
    covered(15,'ED-EN-FORMULA-E014','The inserted quotient morphism belongs to the corrected E_o-construction paragraph; the complete paragraph is reconstructed together.')
    no_counterpart(17,'The extracted formula occurs only in a percent-comment describing a diagram, not in rendered French text. It is not an additional source-text variant.')
    exact(19,'73_expose_VII','of $P_Q$ by\n$G_Q$','of $Q_P$ by\n$G_Q$',
          'The printed first extension clause says Q_P, where the corrected clause and English say P_Q; the contextual phrase locates the occurrence uniquely.')
    candidate(21,[(r'\operatorname{Biext}^{1}(P,Q;G)',r'\operatorname{Biext}(P,Q;G)')])
    exact(23,'83_expose_VII','and\n$G=\\underline G_{m,S}$,','and\n$G$ is the multiplicative group over $\\underline G_m$,',
          'The release compresses the corrected multiplicative-group statement into G=G_{m,S}. The print erroneously says that G is the multiplicative group over G_m. Restore that English reading without inventing a nested subscript notation; also covers ledger 22.')
    candidate(25,[(r's:L_0\longrightarrow X',r'j:L_0\longrightarrow X')])
    candidate(27,[(r'\underline\Psi_{L_\bullet}',r'\underline\Psi_L')])
    candidate(29,[(r"j't=f_0",r'jt=f_0')])
    candidate(31,[(r"L''_\bullet",r'L_\bullet')])
    candidate(33,[(r"L'_\bullet",r"L'")])
    candidate(35,[(r"L'_\bullet(P,Q)",r"L_\bullet(P',Q')")])
    exact(37,'114_expose_VIII',
          '$P$ is of finite type---then the group of classes of commutative\nextensions of $P$ by $Z_k$',
          '$Z$ is of finite type---then the group of classes of commutative\nextensions of $P$ by $G_k$',
          'The printed finite-type example names Z rather than P, and the extension-group sentence names G_k rather than Z_k. Reconstruct the complete local clause rather than pairing formulas by count.',282)
    candidate(39,[(r'\Hom(Q,D(T_n(P)))',r'\Hom(Q,D(T_n(P))')])
    candidate(41,[(r'\bigl((\mathbb Z/n\mathbb Z)_T',r'(\mathbb Z/n\mathbb Z)_T')],
              reason='Equation 2.1.8.1 lacks the opening parenthesis in the print. Remove the corresponding visible delimiter, also removing its sizing command so the TeX remains valid.')
    exact(43,'98_expose_VIII',r'\alpha^n_{P,Q}:{}_nP\otimes{}_nQ\longrightarrow\uTor_1(P,Q)',
          r'\varphi^n_{P,Q}:{}_nP\otimes{}_nQ\longrightarrow\uTor_1(P,Q;G)',
          'The image-map display in 2.2.7 retains both printed errors: varphi rather than alpha and the spurious G argument of Tor.')
    candidate(45,[(r'\mathbb L','P'),(r'\otimes','')],
              reason='The print has P in all three factors and omits the tensor-product sign. P is the ordinary group symbol, so it must not inherit the released line-bundle typeface mathbb L.')
    aligned(47,r'\mathbb M','The printed line-bundle sentence says that M is on M rather than A. In the released English the line-bundle symbol M is typeset mathbb M; retain that established English encoding.')
    candidate(49,[(r'\mathrm{Hom}}(\Psi,(\mathbb Q/\mathbb Z)_k)',r'\mathrm{Hom}}(\Psi,\mathbb Q/\mathbb Z)_k)')])
    candidate(51,[(r"(V'/\mathfrak m V')",r"(V'/\mathfrak m V)")])
    exact(53,'148_expose_IX',r"is simple over $K$.  Take $K'/K$ to be a ramified quadratic extension",r"is simple over $K'$.  Take $K'/S$ to be a ramified quadratic extension",
          'The print names K-prime in the first simplicity assertion and S as the base of the ramified quadratic extension. Restore both adjacent printed readings; this supersedes the separately aligned formula-2270 K-to-K-prime operation.',395)
    aligned(55,LEDGER[55]['english'].replace(r"T_\ell(A'{}_o^o)",r'T_\ell(A{}_o^o)'),
            'In the second Tate-module factor of 2.4.5 the print omits the prime on A. Keep the English arrangement of the remaining indices.')
    exact(57,'139_expose_IX',r'The case $\ell=p$ will be studied',r'The case $\ell\ne p$ will be studied',
          'The printed footnote says ell is not p; the corrected footnote says ell=p. This is an author footnote, not an editorial note.')
    aligned(59,r'\Gamma^{o}','The character is said to be trivial on Gamma^o in the print; the corrected source removes the superscript.')
    candidate(61,[(r'\mathbb L',r'\mathbb M')])
    candidate(63,[(r'\operatorname{Spf}(V)',r'\operatorname{Spf}(A)')])
    aligned(65,r"A_{K,K'}",'The print omits the natural superscript in this occurrence in the inductive-system sentence; preserve the other occurrences.')
    candidate(67,[(r'\operatorname{Ext}^2(Q,P)',r'\operatorname{Ext}^2(R,Q)')])
    candidate(69,[(r'\mu_m)\otimes\check H_o',r'\mu_m)\otimes\check H^o'),('D(H_{oU})','D(H_{oS})')])
    exact(71,'163_expose_IX',r"dual scheme $(A'_K)'$ of $A'_K$",r"dual scheme $(A'_K)'$ of $A_K$",
          'The printed sentence omits the prime on the scheme being dualized; the first and subsequent A_K references have different roles and remain unchanged.')
    candidate(73,[(r'\mathcal O}_{X_o,x_i}',r'\mathcal O}_{X_o,x}')])
    candidate(75,[(r'\mathcal E(B)',r'(B)')],reason='The print omits the E at the middle object of 13.4.14. Remove its complete TeX font command as well, leaving exactly the printed (B) rather than a spurious calligraphic parenthesis.')
    no_counterpart(77,'The French correction moves the already present T_1 next to schéma and makes the implied point/morphism nouns explicit. The same scheme, point, and morphism already occur in the diplomatic statement; the natural released English wording expresses both without a distinct mathematical reading.',33)
    exact(79,'002_expose_X',r'\underline{is identified with the fibre over} $x_1$.',
          r'\underline{is identified with the fibre over} $x_1$ \underline{in} $X_1$.',
          'The release leaves the ambient scheme implicit, correctly the blow-up X. To represent the printed erroneous explicit ambient scheme X_1 in diplomatic English, retain the printed qualification there; the corrected release remains unchanged.')
    candidate(81,[(r'P(r)=\dim_k(m^r/m^{r+1})',r'P(n)=\dim_k(m^n/m^{n+1})'),(r'large }r.',r'large }n.')],
              reason='Restore n in the Hilbert-polynomial argument, both exponents, and the final variable; leave the English word large unchanged.')
    candidate(83,[(r"p_*\underline{O}_{E'}",r'f_*\underline{O}_{E}')])
    candidate(85,[(r"(s^*,D')",r'(s^*,D)')])
    aligned(87,LEDGER[87]['english'].replace(r"J^n\otimes\underline{O}_{D'\cap T}",r"J^n\otimes_{D'\cap T}"),
            'The print has the intersection as a subscript on the tensor symbol and omits the structure-sheaf factor. Replace the whole syntactic unit to preserve valid TeX.')
    candidate(89,[(r"[k(t'):k(t)]",r"[k(t'):k]")])
    candidate(91,[('T_0','S_0')])
    aligned(93,LEDGER[93]['english'].replace(r'\sum_{n\geq0}',r'\sum'),
            'The printed exponential series has an unqualified summation sign; the corrected source explicitly supplies n>=0.')
    c95=LEDGER[95]['target_candidates'][0];b95=c95['body'];a95=b95.index('R^if_*',b95.index(r'\tag{i}'))
    q95=b95[a95:];p95=q95.replace('X/S','TEMP').replace('H/S','X/S').replace('TEMP','H/S')
    variant(95,c95['component'],q95,p95,'Only the second, injective row (ii) is affected by this item. Restore its printed H-to-X direction independently of row (i), handled by E094.',start=c95['start']+a95)
    candidate(97,[(r'\Omega^j_{Y/S}',r'\Omega^j_{X/S}')])
    candidate(99,[(r'\sum_{i\in P}',r'\sum')])
    exact(101,'019_expose_XII',
          '$e$ therefore factors through $S$, hence through a section of\n$\\Spec(Z(Q))$ over $S$',
          "$e$ therefore factors through a section of\n$\\mathbb E(\\bigwedge^2W')$ over $S$",
          'The printed factorization goes through a section of the affine space, not the etale center. The inherited English editorial footnote independently quotes this precise printed error.',67)
    candidate(103,[(r'T^{2r}(V)',r'T^{2r}(E)')],reason='English has consistently renamed the dimension parameter n to r in this passage. Preserve r and restore only the printed E/V distinction.')
    candidate(105,[(r'\rho((e,0))\bigr)',r'\rho((e,0))'),(r'\rho((0,f))\bigr)',r'\rho((0,f))')],
              reason='Both printed expressions omit the outer closing parenthesis. Remove the whole sized closing-delimiter command in English, leaving the two inner closings intact.')
    candidate(107,[(r'Rg_{\{y\}}',r'Rg_{\{x\}}')])
    no_counterpart(109,'Only French adjective agreement changes: revêtements universel becomes revêtements universels. The noun is plural in both readings, and English universal is indeclinable; universal coverings is unchanged.')
    candidate(111,[(r'D_{t_0}',r'D_{|t|_0}')])
    candidate(113,[(r'\widetilde D_t^*',r'D_t^*')])
    exact(115,'059_expose_XIV',
          'In particular, one may take the $p^{-1}(V)$ for\n$V$ a Stein neighborhood of $x$ in $X$.',
          'In particular, the $p^{-1}(V)$ for\n$V$ a Stein neighborhood of $x$ in $X$ form a fundamental system of neighborhoods of $X$.',
          'The release contracts the final neighborhood assertion. Expand only the diplomatic clause to retain its printed uppercase X in the place where the corrected source has the point x.')
    candidate(117,[(r'K^{mqu}',r'K^{muq}'),(r'\Psi_\eta^{mqu}',r'\Psi_\eta^{muq}')])
    aligned(119,LEDGER[119]['english'].replace(r'\xi\prod',r'\xi:\prod'),
            'The print places a colon after xi; the corrected multiplication is implicit in the released English juxtaposition. Restore the visible colon only in diplomatic English.')
    candidate(121,[(r'H^0(',r'H^o(')])
    candidate(123,[(r'\widetilde X_{s(0)}',r'X_{s(0)}')])
    aligned(125,LEDGER[125]['english'].replace(r'H^n_{\{\bar x\}}\bigl(X_{\bar s},R\psi_{\bar\eta}(\Lambda)\bigr)',
                                           r'H^n_{\{\bar x\}}\bigl(R^n\psi_\eta(\Lambda)\bigr)'),
            'The printed local-cohomology expression omits X_bar_s, uses R^n psi rather than R psi, and lacks the bar on eta; restore the entire second expression and leave the first stalk unchanged.')
    candidate(127,[(r'S_0',r'S')])
    no_counterpart(129,'The same bound and all three hypotheses occur in both French readings; only the wrapping of inline expressions into a displayed equation changes. It does not supply a new English mathematical reading.')
    exact(131,'090_expose_XVII',r'singularities presented in $n$ variables exist only',r'singularities of dimension $n$ exist only',
          'The corrected source has dimension n-1, expressed equivalently in the release as n variables. The print says dimension n; restore that dimensional statement rather than silently changing the English variable convention.')
    candidate(133,[(r'X_r^{W_r}',r'X_r^{W_o}')])
    aligned(135,'\\tag{3.3.4}\n(\\lambda_1,\\ldots,\\lambda_{r-n})\\longmapsto\n\\sum_1^{n-r}\\lambda_i g_{n+i}.\n',
            'The print uses lowercase lambda, an upper summation bound n-r, a lower limit 1, and g_{n+i}. Restore the complete formula rather than attempting unsafe individual-token alignment.')
    candidate(137,[(r'\mathbb P(N)',r'\mathbb P(\check N)')],
              reason='The release expresses the completed local ring by naming its ambient projective bundle. The printed completed-ring subscript is P(check N), so this diplomatic reading restores the dual-bundle error in that equivalent English phrase.')
    candidate(139,[(r'\binom{r+d}{d}',r'\binom{n+d}{d}')])
    candidate(141,[(r'\longrightarrow\mathcal O_X'+'\n'+r'\longrightarrow0',r'\longrightarrow\mathcal O_{\mathbb P}'+'\n'+r'\longrightarrow0')])
    candidate(143,[(r'\sum_{i=0}^{a}',r'\sum_{i=0}')])
    passage145='''\\[
H^0(\\mathbb P^1,R^n\\rho_*\\mathbb Q_\\ell(j))
\\xrightarrow[\\nu^*]{\\sim}
H^0(U,\\nu^*R^n\\rho_*\\mathbb Q_\\ell(j)).
\\]
Thus $f^*(x)$ is primitive relative to $\\mathbb P^1$ if and only if
$\\alpha^*f^*(x)$ is primitive relative to $U$.'''
    printed145=passage145.replace('H^0','H^o').replace(
        'Thus $f^*(x)$ is primitive relative to $\\mathbb P^1$ if and only if\n$\\alpha^*f^*(x)$ is primitive relative to $U$.',
        'Thus[$f^*(x)$ is primitive relative to $\\mathbb P^1\\alpha$] $\\Longrightarrow\n\\alpha^*f^*(\\alpha)$ is primitive relative to $U$.')
    exact(145,'124_expose_XVIII',passage145,printed145,
          'The count mismatch comes from rewriting the damaged conclusion of the proof, not an isolated U. Restore both printed H^o degrees and the full implication with its stray alpha and argument alpha. Keep the released arrow typography so it remains valid TeX; supersedes automatic source-formula operations 882, 884, and 885 on this folio. The independently illegible label in 5.8.3.1 is outside this passage.',303)
    candidate(147,[(r'G_0(x)',r'G_o(x)')])
    candidate(149,[(r'\mathbb Z_\ell\bigr)'+'\n'+r'\Longrightarrow',r'\mathbb Z_\ell'+'\n'+r'\Longrightarrow'),
                  (r'\widetilde X,\mathbb Z',r'\widetilde X_o\;\mathbb Z')],
              reason='The supplied diplomatic formula omits the first closing parenthesis and the comma in the abutment and prints a subscript o on X-tilde. Restore those readings while removing the sizing command belonging to the absent delimiter.')
    candidate(151,[(r'd_{s+1}^{p,q}',r'd_s^{p,q}')],reason='The release uses s for the spectral-sequence page index. Retain that English index and restore the missing +1 in the print.')
    aligned(153,LEDGER[153]['english'].replace(r'H_c^i(\widetilde\Delta',r'H_C^i(\widetilde\Delta'),
            'Only the compact-support index in the second numerator is printed uppercase C. The release places the subscript before the superscript; preserve that ordering.')
    candidate(155,[(r'b_{q-2j}',r'b_{q-j}')])
    candidate(157,[(r'(-1)^n',r'(-1)^{\eta}')])
    candidate(159,[(r'\operatorname{length}_{x_i}',r'\operatorname{rank}_{x_i}')],
              reason='The printed operator rg denotes rank where the corrected lg denotes length. The English renders these operator names as rank and length, respectively, preserving the wrong printed operation.')
    no_counterpart(161,'After percent-comments are removed, the two source diagrams are identical, including the lower inclusion label j. The added comment is not an additional rendered variant.')
    candidate(163,[(r'(b\oplus0)=',r'(b\oplus0=')])
    candidate(165,[(r'\oplus(-g_*i^*)',r'\oplus g_*i^*')])
    candidate(167,[(r'\oplus(-g_*i^*)',r'\oplus(g_*i^*)')])
    candidate(169,[(r'(\rho i)^*\underline{\mathcal O}_{\mathbb P^1}(1)'+'\n'+r'\otimes g^*\underline{\mathcal O}_\Delta(-1).',
                    r'\underline{\mathcal O}_{\mathbb P(\underline{\mathcal O}_\Delta^{,2})}(1)'+'\n'+
                    r'\otimes_{\underline{\mathcal O}_\Delta^{,2}}\underline{\mathcal O}_\Delta(-1)'+'\n'+
                    r'=\underline{\mathcal O}_{\mathbb P^1}(1)\otimes_K\underline{\mathcal O}_\Delta(-1).')],k=1,
              reason='The English contracts the tautological-bundle calculation into its final pulled-back expression. Expand that diplomatic display to the two printed targets, retaining the erroneous tensor base O_Delta^2 and uppercase K, both absent from the contracted release. No corrected English text is replaced by a newly preferred equivalent.')
    candidate(171,[(r'\xi_\Delta)\right]',r'\xi_\Delta\right]')],
              reason='The print omits the closures after xi_Delta. The release omits function-grouping parentheses around g^*, so its corresponding visible omission is the closing parenthesis of c_1; the outer left/right delimiter pair remains valid.')
    candidate(173,[(r'\wedge',r'\Lambda')])
    printed175=LEDGER[175]['english'].replace(r'\text{by (4.2.11)}',r'\text{by (4.3.2)}')
    printed175=printed175.replace('\\right)\\\\\n&=-g_*\\!', '\\right)\\qquad\\text{by (4.3.2)}\\\\\n&=-g_*\\!')
    aligned(175,printed175,
            'The printed calculation cites 4.3.2 at both intermediate steps. Restore the omitted first citation and the incorrect final citation in the single combined English calculation.')
    exact(177,'115_expose_XVIII','Formula (4.2.3.2) expresses the fact that $f^*$ is\nan algebra homomorphism.',
          'Formula (4.2.3.2), $(a\\oplus0)\\Lambda(b\\oplus0)=ab\\oplus0$, expresses the fact that $f^*$ is\nan algebra homomorphism.',
          'The release references the identity without repeating it. The diplomatic sentence repeats its printed form to retain the capital Lambda in place of the cup-product wedge.')
    exact(179,'115_expose_XVIII','Using (4.2.11) and (4.3.2),','Using (4.3.2),',
          'The release collects the citations before the calculation. The printed first step cites 4.3.2 where the corrected source cites 4.2.11; retain the incorrect printed citation in that introductory English phrase.')
    candidate(181,[(r'\tag{5.2.4.7}',r'\notag'),(r'\mathbb Q_\ell(2j+1))',r'\mathbb Q_\ell(2j+2)')],
              reason='The printed pairing has twist 2j+2 and omits the outer closing parenthesis. The equation tag is supplied only in the corrected French layer and therefore is omitted in this diplomatic branch.')
    candidate(183,[(r'E_2^{2,n-1}'+'\n'+r' &=H^2',r'E_2^{2,n-1}('+'\n'+r' &=H^2')],
              reason='The source writes the identification E_2^{2,n-1}(=H^2(...)) parenthetically, but the print lacks its final parenthesis. The release uses a chain of equalities; restoring the unmatched opening parenthesis in that chain expresses the printed defect without removing the H^2 argument closure.')
    candidate(185,[(r'\xi_X^{i+1}',r'\xi_X'),(r'R^{n+i}\rho_*',r'R^{n-1+i}'),(r'i\geq0',r'i\geq1')])
    candidate(187,[(r'\pi_1^{\mathrm{mod}}',r'\pi_1')])
    exact(189,'130_expose_XVIII',r'The action of $\operatorname{Gal}(k(\bar\eta)/k(\eta))$ on',
          r'The action of $\operatorname{Gal}(/k(\eta))$ on',
          'The displayed Galois quotient and this following inline occurrence both omit the numerator in print. This operation covers the inline occurrence, identified by its surrounding prose; the displayed occurrence is handled separately.')
    no_counterpart(191,'Only the position of the sentence period relative to the closing math delimiter changes. Both source readings render the same concluding period; the release expresses the same final membership in prose, with its period outside math. There is no distinct printed mathematical reading to transfer.')
    candidate(193,[(r'X_{\bar\eta}',r'X'),(r'\mathbb Q_\ell(m)),',r'\mathbb Q_\ell(m),')])
    candidate(195,[(r'\mathbb Q_\ell(m))^\pi',r'\mathbb Q_\ell(m)^\pi')])
    candidate(197,[(r'\sigma_i(\chi)-\chi',r'\sigma_i(x)-x')])
    for i in (199,201,203):
        no_counterpart(i,'The label occurs in both versions of the same freehand line figure. The source rewrites a tikzcd grid as an explicit tikzpicture, causing the math parser to count individual node labels separately. No label or mathematical relation is added; there is no distinct English reading.',336)
    candidate(205,[(r'\sum_i a_i',r'\sum_i d_i')])
    exact(207,'146_expose_XX','In particular, when $m=2$, for $X$ a quadric',
          'In particular (4.2), for $X$ a quadric',
          'The source parenthesis is literally (4.2), replaced in the corrected layer and release by the numerical specialization m=2. The neighboring dimension formula is a separate variant.',362)
    aligned(209,LEDGER[209]['english'].replace(r'\mathbb Q_\ell(i+b-d_1)).',r'\mathbb Q_\ell(i+b-d_1).'),
            'The print omits the outer target H^p closing parenthesis. The release has no extra grouping parentheses around g_*, so remove only the last visible closure, retaining the coefficient twist closure.')
    candidate(211,[(r'\longrightarrow C_{\bar\eta}',r'\longrightarrow C')])
    aligned(213,LEDGER[213]['english'].replace(r'\circ P_{\bar\eta}',r'\circ P'),
            'The print omits the generic-fiber index on the final correspondence P, not on Q or V.')
    candidate(215,[(r'P_{\bar\eta}-m^*Q_{\bar\eta}',r'P_{\bar\eta}m^*Q_{\bar\eta}')],k=1,
              reason='Equation number 4.4.10 identifies the counterpart; the more similar candidate 4.4.9 is a different display. Restore the missing subtraction sign only in the first equality.')
    no_counterpart(217,'The printed condition is split across inline math and prose as ell not-equal, car, (k); the corrected layer places it inside a single formula. Both assert ell unequal to the characteristic of k, rendered identically by the English condition.')
    exact(219,'147_expose_XXI','A proper scheme $X$ over a field $k$',
          'A proper scheme over a field $k$',
          'Definition 1.0 omits the name X in print and supplies it in the corrected layer. The repeated X in the preceding introduction made the formula-sequence index ambiguous; the full definition fixes the location.',365)
    exact(221,'149_expose_XXI','we can set $a_0=0$ and choose $r$ integers',
          'we can choose $r$ integers',
          'The explicit a_0=0 convention is supplied in the corrected construction and absent from print; remove that clause in diplomatic English.',369)
    passage223='''space of coinvariants under $I$, regarded as $G/I$-modules.  Put
$r=\\dim_E V^I$, and let $\\alpha_1,\\ldots,\\alpha_r$ be the eigenvalues of
$F$ on $V^I$.  Then there are integers $m_i\\geq0$ such that the eigenvalues
of $F$ on $V_I$ are
\\[
\\alpha_iq^{m_i}\\qquad(1\\leq i\\leq r).
\\]'''
    printed223=passage223.replace('Put\n$r=\\dim_E V^I$, and let','Let').replace(r'\alpha_r',r'\alpha_n').replace(r'\qquad(1\leq i\leq r)','')
    exact(223,'159_expose_XXI',passage223,printed223,
          'The printed lemma counts the invariant-space eigenvalues as alpha_1,...,alpha_n although n is the dimension of V. Restore that count, remove the added r=dim_E V^I convention, and remove its added index range. One passage covers both ledger 223 and 224.',389)
    c225=LEDGER[225]['target_candidates'][0]
    variant(225,c225['component'],c225['body'],
            '\\tag{1.2.6}\n\\left\\{\\begin{aligned}\n'
            'd_1&\\geq a_o,\\\\\n'
            'd_2&\\geq a_2-a_1,\\\\\n'
            'd_r&\\geq a_r-a_{r-1}.\n'
            '\\end{aligned}\\right.\n',
            'The release condenses the three printed inequalities into one indexed bound using the supplied a_0=0 convention. The diplomatic display restores the printed three-line list, including d_1>=a_o, rather than changing every term of the condensed formula.',start=c225['start'])
    exact(227,'152_expose_XXI',r'\text{there are projective coordinates }X_0,\dots,X_N\text{ such that}',
          r'\text{there are projective coordinates }X_o,\dots,X_N\text{ such that}',
          'The coordinate list in 1.4.2 is printed with the letter-like subscript o. The later list in the last paragraph is a distinct occurrence; equation number and context fix this one.')
    candidate(229,[(r'd_0=',r'd_o=')])
    candidate(231,[(r'1\leq i\leq n-1',r'1\leq\;\leq n-1')])
    candidate(233,[(r'\underline H_c^i',r'H_c^i')])
    exact(235,'160_expose_XXI',r'\underline H_c^i(X,\underline G)^\vee',r'H_c^i(X,\underline G)^\vee',
          'The missing underline is on the cohomology object in the statement of Theorem 5.4. The release consistently underlines the coefficient G as well; only the source-attested H underline differs.')
    exact(237,'164_expose_XXII',
          '\\subsubsection*{Proposition 1.2.}\nLet $\\varphi$ be a $q$-linear endomorphism of a finite-dimensional vector\nspace $V$ over a separably closed field $k$.',
          '\\subsubsection*{Proposition 1.2.}\nLet $\\varphi$ be a $q$-linear endomorphism of a finite-dimensional vector\nspace over a separably closed field $k$.',
          'The printed hypothesis omits the name V before using it in the displayed map. The preceding corollary names V correctly and is not changed.',405)
    exact(239,'166_expose_XXII',r'automorphism induced by $\varphi_q^{-1}$ on the right-hand side.',
          r'automorphism $\varphi_q^{-1}\otimes_{\mathbb F_q}k$ of the right-hand side.',
          'The release leaves the scalar extension implicit in this clause. Make it explicit in the diplomatic clause to preserve the printed wrong base F_q. The following fr_q tensor extension is over F_p in both source layers and must remain unchanged.')
    candidate(241,[(r'\varphi_q^{-1}',r'\varphi_q')])
    no_counterpart(243,'Only the French ordinal spelling changes, from p apostrophe ième to p-ième. Both mean a primitive p-th root of unity; the released English p-th is identical for both readings.')
    aligned(245,LEDGER[245]['english'].replace(r'(1-q^it)',r'(1-q^if)').replace(r'\right]^{-1}',r'\right]'),
            'The printed product uses f in the factor 1-q^if and lacks the inverse exponent on the bracketed expression. Restore both defects while retaining the English display layout.')
    candidate(247,[(r'H^{n+1}',r'H^{i+1}'),
                   (r'\text{the quotient of the $\mathbb F_q$-vector space with basis}',r'\text{the $\mathbb F_q$-vector space with basis}'),
                   (r'&\quad\text{by the $\mathbb F_q$-subspace',r'&=\text{the $\mathbb F_q$-subspace')],
              reason='The printed degree is i+1 and the second relation is an equality with the subspace, not a quotient by it. Restore those mathematical readings in the released English wording; no source-independent mathematical correction is introduced.')
    assert sorted(RES)==list(range(1,len(LEDGER),2)), sorted(set(range(1,len(LEDGER),2))-set(RES))
    WORK.joinpath('en_formula_resolutions_glossary.json').write_text(json.dumps(list(RES.values()),ensure_ascii=False,indent=2)+'\n')
    print('Saved',len(RES),'context-reviewed resolutions')


if __name__=='__main__':run()
