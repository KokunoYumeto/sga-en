r"""Inspected English contexts for the agreed misprints in Tomes 1--2.

The French canonical record supplies the correction. Each English context is
checked against the released translation at the recorded printed page boundary.
"""
from en_common import *
from en_extra import page_window, find_matches, compact
from build_en import page_markers

M=json.loads((SOURCES/'fixes/MISPRINTS_4.json').read_text())
S=page_markers(RELEASE.read_text())
ROWS=[]

def add(ident,printed,corrected,reason='The canonical correction changes the displayed English reading at this exact occurrence.',current=None):
    m=M[int(ident[2:])-1]
    row=dict(id=ident,expose=m['expose'],page=m['page'],place=m['where'],printed_french=m['print'],corrected_french=m['correct'],assessment='English-impact',reason=reason)
    found=[]
    for width in [0,1]:
        w=page_window(S,m['expose'],m['page'],width)
        order=[('printed',printed),('corrected',corrected)]
        if compact(printed)[0] in compact(corrected)[0] and len(compact(printed)[0])<len(compact(corrected)[0]):order.reverse()
        if current:order.append(('source-intermediate',current))
        for state,needle in order:
            hits=find_matches(needle,S[w[0]:w[1]])
            if len(hits)==1:
                a,b=hits[0];a+=w[0];b+=w[0]
                found=[dict(printed=printed,corrected=corrected,location_verified=True,current_anchor=S[a:b],current_state=state,context_before=S[max(0,a-150):a],context_after=S[b:b+150])];break
        if found:break
    if not found:raise ValueError((ident,printed,corrected))
    row['english_deltas']=found;ROWS.append(row)

def no(ident,reading,reason):
    m=M[int(ident[2:])-1];w=page_window(S,m['expose'],m['page'],1)
    assert compact(reading)[0] in compact(S[w[0]:w[1]])[0],(ident,reading)
    ROWS.append(dict(id=ident,expose=m['expose'],page=m['page'],place=m['where'],printed_french=m['print'],corrected_french=m['correct'],assessment='no English impact',reason=reason,english_reading=reading,location_verified=True))

add('MP0001','The cardinal 0 and the countably infinite cardinal are strongly\ninaccessible','The cardinal 0 and the countably infinite cardinal are strongly\ninaccessible.', 'The French spelling has one English rendering, inaccessible; the canonical record also supplies the missing full stop.')
add('MP0002',r'where at least have cardinality $\in 𝒰$',r'or at least have cardinality $\in 𝒰$')
add('MP0011',r'and therefore the functor $e_X\circ j^\ast$ is canonically',r'and therefore the functor $e_X\circ j^\ast_X$ is canonically')
add('MP0015',r'The notation is that of \hyperref[I.def6.1]{5.1}.',r'The notation is that of \hyperref[I.def6.1]{6.1}.')
add('MP0024',r"$X'\in \ob C$ is epimorphic (\resp  strictly epimorphic)",r"$X'\in \ob C$ is strictly epimorphic (\resp  epimorphic)")
add('MP0025',r'also (\hyperref[I.sec7.1.2]{7.1.2}), that $C$ is generating',r'also (\hyperref[I.sec7.1.1]{7.1.1}), that $C$ is generating')
add('MP0027',r'strict monomorphisms)\\',r'strict monomorphisms\\')
add('MP0030',r"fiber fiber product of $X'$ and $X''$ over $X$",r"fiber product of $X'$ and $X''$ over $X$",'The duplicated French modifier fibré is represented by a duplicated English fiber; the corrected technical term is fiber product.')
add('MP0043',r"such that $I$ and $I'$ are $𝒰$-small",r"such that $I$ and $I'$ are $𝒱$-small")
add('MP0045',r"preordered set $OB\,I'$",r"preordered set $\Ob\,I'$")
no('MP0061','for this\nfunctor to be essentially surjective','The missing French que is supplied by the English infinitive construction; the English phrase carries no independent missing word.')
add('MP0070',r'every object $\varphi$ of $\Hhom(C,J)$',r'every object $\varphi$ of $\Hhom(J,C)$')
add('MP0077',r'let $X_i$ be the subset $\Delta_{i+1}\amalg\Delta_i$ of $\NN$',r'let $X_i$ be the subset $\Delta_{i+1}\amalg\Delta_i$ of $X$')
add('MP0086',r'or the pair $(X,n)$',r'or the pair $(X,u)$')
add('MP0108',r'Consider the composite $X(\alpha_i)\rightarrow X(\alpha)',r'Consider the composite $X(\alpha)_i\rightarrow X(\alpha)')
add('MP0112',r'the hypothesis that $I$ is large $\pi$',r'the hypothesis that $I$ is large relative to $\Pi$')
add('MP0113',r"$S_a=\bigcup_{a<a}S_a$ if $a$ is a limit ordinal.",r"$S_a=\bigcup_{a'<a}S_{a'}$ if $a$ is a limit ordinal.")
add('MP0129','Theory of Categories, Academie Press','Theory of Categories, Academic Press')
add('MP0130','Kuratowaki','Kuratowski','The existing Orgogozo pair supplies the diplomatic transcription Kuratowaki and the agreed name Kuratowski. The scan-check record expressly reports blurred print; this does not claim an independent reading of the scan.')
add('MP0136',r'function $\varphi$ of \hyperlink{sga4.exp.I.appendix.II.sec.6.lemma.1}{Lemma 2}',r'function $\varphi$ of \hyperlink{sga4.exp.I.appendix.II.sec.6.lemma.1}{Lemma 1}')
no('MP0138',r'all coherent sequences extending $(a_1,\ldots,a_n,x)$ had lengths','The French article des corrected to les is rendered by the same English determiner construction all coherent sequences.')
add('MP0143','Theory of categories, Academie Press','Theory of categories, Academic Press')


add('MP0151',r'the presheaf. $X_i\times_X X_j$',r'the presheaf $X_i\times_X X_j$')
add('MP0152','both an epimorphism and and a monomorphism of sheaves.','both an epimorphism and a monomorphism of sheaves.')
add('MP0156',r'Then, for every object of $\widetilde{C}$',r'Then, for every object $X$ of $\widetilde{C}$')
add('MP0161',r'\setcounter{subsection}{10}\subsection{}\etiquette[1.11]{III.subsec1.11}',r'\setcounter{subsection}{1}\setcounter{subsubsection}{0}\subsubsection{}\etiquette[1.1.1]{III.subsec1.11}')
add('MP0165',r"C \widetilde{\phantom{A}} \ar[r]^{u^{s}}&  C',",r"C \widetilde{\phantom{A}} \ar[r]^{u^{s}}&  C'\widetilde{\phantom{A}},")
add('MP0166',r'\hyperref[III.prop2.2]{2.2} iv) may often',r'\hyperref[III.prop1.2]{1.2} iv) may often')
add('MP0167',r"C'\widehat{\phantom{a}}_{\underline{V}} \ar @{_{(}->}[d]",r"C'\widehat{\phantom{a}}_{\underline{U}} \ar @{_{(}->}[d]")
add('MP0169',r'In fact, it suffices that $n$ commute',r'In fact, it suffices that $u$ commute')
add('MP0171',r"\widetilde{C}'_{𝒱}$ the right adjoint relative",r"\widetilde{C}'_{𝒱}$) the right adjoint relative")
add('MP0173','(this is immediately for a cocontinuous functor','(this is immediate for a cocontinuous functor')
add('MP0175',r'the morphisms $u:F\rightarrow F$ and',r'the morphisms $u:F\rightarrow G$ and')

add('MP0180',r'III \hyperref[III.theo4.1]{5.1} provides numerous examples',r'III \hyperref[III.theo4.1]{4.1} provides numerous examples')
add('MP0184',r'(III 2.9.1).',r'(III \hyperref[III.exem1.9.1]{1.9.1}).')
add('MP0189',r'$u_{\ast}$ has a right adjoint which is left exact.',r'$u_{\ast}$ has a left adjoint which is left exact.')
add('MP0190',r'this functor has a left adjoint (\resp a right adjoint if and only if',r'this functor has a left adjoint (\resp a right adjoint) if and only if')
add('MP0192',r'denoted by $I_E$, where $I_C$ when $E$ is defined',r'denoted by $I_E$, or by $I_C$ when $E$ is defined')
add('MP0193',r'(\hyperref[IV.subsec10.2]{10.\phantom{2}}); the left action',r'(\hyperref[IV.subsec10.2]{10.2}); the left action')

add('MP0205',r'subgroup of $p^{\ast}(G)$ and hence acts',r'subgroup of $\pi^{\ast}(G)$ and hence acts')
add('MP0206',r"$X'=f^{\ast}(X)$ be its inverse image in $E$.",r"$X'=f^{\ast}(X)$ be its inverse image in $E'$.")
add('MP0209',r'To define $u$, note that $$\psi(X)=X\times X$$',r'To define $u$, note that $$j(X)=X\times X$$')
add('MP0211',r'is an isomorphism of morphisms of topoi from $E$ to $G$',r'is an isomorphism of morphisms of topoi from $F$ to $E$')
add('MP0213',r'is called the fiber of $E$ at $p$ and is',r'is called the fiber of $F$ at $p$ and is')
add('MP0214',r'the category $E_{/\varphi_x}$ (the full subcategory',r'the category $E_{/\varphi_p}$ (the full subcategory')
add('MP0214',r'$(E^\circ)^{\widehat{\phantom{,}}}_{/\varphi_x}$ formed',r'$(E^\circ)^{\widehat{\phantom{,}}}_{/\varphi_p}$ formed')
add('MP0216',r'Since $\varphi_x$ is left exact',r'Since $\varphi_p$ is left exact')
add('MP0218',r"of $p$ lying over $(X,p)$, with $X'\in \ob C$",r"of $p$ lying over $(X,u)$, with $X'\in \ob C$")
add('MP0223',r'sheaves on $C$ with values in $F$',r'sheaves on $C$ with values in $D$')
add('MP0224',r'every point of the classifying topos $E_G$ is induced',r'every point of the classifying topos $B_G$ is induced')
add('MP0225',r'either a subobject or a quotient object of $C$.',r'either a subobject or a quotient object of $X$.')
add('MP0226',r"$E$ to the topos $E'$.",r'$E$ to the topos $F$.')
add('MP0227',r'this map commutes with finite Inf arbitrary $\Sup$.',r'this map commutes with finite Inf and arbitrary $\Sup$.')
add('MP0228',r'Show that $I$ is canonically isomorphic to $\Ouv(\Oo^{\sim})$',r'Show that $\Oo$ is canonically isomorphic to $\Ouv(\Oo^{\sim})$')

add('MP0229',r'that $C$ is of local nature if and only if $R$',r'that $T$ is of local nature if and only if $R$')
add('MP0230',r'the opens of the topos $T(X)$ identify',r'the opens of the topos $\Top(X)$ identify')
add('MP0231',r'When the topology of $E$ is defined by means of a',r'When the topology of $C$ is defined by means of a')
add('MP0232',r'stable under descent), \resp of local nature) on the target',r'stable under descent, \resp of local nature) on the target')
add('MP0238',r'$f_{\ast}$ associated with a morphism of topoi $g:F\rightarrow E$',r'$g_{\ast}$ associated with a morphism of topoi $g:F\rightarrow E$',current=r'$f_{\ast}$ associated with a morphism of topoi $f:F\rightarrow E$')
add('MP0241',r'one obtains in particular from \hyperref[IV.prop9.1.4]{9.1.5}:',r'one obtains in particular from \hyperref[IV.prop9.1.4]{9.1.4}:')
add('MP0242',r'for the morphism of topoi induced by $f$,',r'for the morphism of topoi induced by $g$,')
add('MP0244',r'the \emph{subtopos generated by the} $E_i$',r"the \emph{subtopos generated by the} $E'_i$")
add('MP0245',r"induce an equivalence $f'$ of $E$ with its image",r"induce an equivalence $f'$ of $F$ with its image")
add('MP0248',r"among the subtopoi $E''_1$ of such that",r"among the subtopoi $E''_1$ of $E$ such that",current=r"among the subtopoi $E''_1$ such that")
add('MP0258',r'a) follows \hyperref[IV.prop9.3.3]{9.3.3} c).',r'a) follows from \hyperref[IV.prop9.3.3]{9.3.3} c).')
add('MP0260',r'supremum of the subtopoi of $E$ {\rm(\hyperref[IV.rem9.1.2]{9.1.2} c))}',r'supremum of the subtopoi $\mathcal{F}_i$ of $E$ {\rm(\hyperref[IV.rem9.1.2]{9.1.2} c))}')

add('MP0265',r"projective system $(\sigma(X'')_i)_{i\in I(X')}$, where $I(X')$ is",r"projective system $(\sigma(X'')_i)_{i\in I(X'')}$, where $I(X'')$ is")
add('MP0267',r"or $X''\in\Ob {C''}^{X}$ $i\in I(X'')$, and",r"where $X''\in\Ob C''$, $i\in I(X'')$, and")
add('MP0268',r'admits a left adjoint \eqhyperref[IV.eq9.5.10.2]{9.5.10.2}.',r'admits a left adjoint \eqhyperref[IV.eq9.5.10.2]{9.5.10.2}).')
add('MP0269',r'$\sigma$ of $\rho$. (N.B.',r'$\sigma$ of $\rho$). (N.B.')
add('MP0270',r'$(E,U,\mathcal{F})$ as in (\hyperref[IV.subsec9.3]{9.3}) is called',r'$(E,U,\mathcal{F})$ as in (\hyperref[IV.subsec9.3]{9.3})) is called')
add('MP0274','Reduce a case where $f$ is surjective','Reduce to the case where $f$ is surjective')
add('MP0275','the functor considered in c) is in fact an equivalence','the functor considered in b) is in fact an equivalence')
add('MP0278',r'(which is a final topos (\hyperref[IV.subsec2.2]{2.2}), nor to any topos of the form $\Top(Y)$.',r'(which is a final topos (\hyperref[IV.subsec2.2]{2.2}), nor to any topos of the form $\Top(Y)$).',current=r'(which is a final topos (\hyperref[IV.subsec2.2]{2.2})), nor to any topos of the form $\Top(Y)$.')
add('MP0279',r'$X\rightarrow\Top(Y)$) to the usual topological quotient.',r'$X\rightarrow\Top(X)$) to the usual topological quotient.',current=r'$Y\mapsto\Top(Y)$) to the usual topological quotient.')
add('MP0281',r'covering the final object of $E$, such that',r'covering the final object of $T$, such that')
add('MP0285',r'induced ringed topos $(T_{/E},{\Oo}_T/E)$',r'induced ringed topos $(T_{/S_i},{\Oo}_T|S_i)$',current=r'induced ringed topos $(T_{/S_i},{\Oo}_T/S_i)$')
add('MP0288',r'\Hom_E(Z,\scrHom_E(X,Y))\simeq \scrHom_E(Z\times X, Y)',r'\Hom_E(Z,\scrHom_E(X,Y))\simeq \Hom_E(Z\times X, Y)')
add('MP0289',r'for every object $Y$ of $E$, a bifunctorial morphism',r"for every object $Y$ of $E'$, a bifunctorial morphism")
add('MP0294',r'\item[Proof of d).] For every object $Y$ of $E_{/X}$',r'\item[Proof of b).] For every object $Y$ of $E_{/X}$')
add('MP0295',r'\Hom(j^{X}_XY,\scrHom_{A|X}(j^{\ast}_XM;P)) &\quad& \text{(adjunction)}',r'\Hom(j^{\ast}_XY,\scrHom_{A|X}(j^{\ast}_XM,P)) &\quad& \text{(adjunction)}')
no('MP0296',r'\item[Proof of d).] For every object $Y$ of $E$, there is the following sequence of isomorphisms:','The accent error in French on à for on a does not change the English existential construction there is the following sequence.')
add('MP0297',r'Let $(E,A)$ be a ringed topos, let $X$ be an object of $A$,',r'Let $(E,A)$ be a ringed topos, let $X$ be an object of $E$,')
add('MP0304',r'whose support $(\hyperref[IV.subsubsec9.3.5]{9.3.5})$ contains $F$',r'whose support $(\hyperref[IV.subsubsec9.3.5]{9.3.5})$ is contained in $F$')

add('MP0306',r'(and thus commutes with $𝒰$-small inductive limits.',r'(and thus commutes with $𝒰$-small inductive limits).')
add('MP0310',r'\otimes_{A_x}v_V^\ast(j_V^\ast M\simeq',r'\otimes_{A_x}x_V^\ast j_V^\ast M\simeq')
add('MP0313',r's_f(g)=\pr_{f(gi))}',r's_f(g)=\pr_{f(g(i))}')
add('MP0316',r"m'_i : U_i \to H'_{\phi(i)})",r"m'_i : U_i \to U'_{\phi(i)})")
add('MP0317',r'$H_q(ST_{∙}(M) \sim H_q(C, M)$',r'$H_q(ST_{∙}(M)) \sim H_q(C, M)$',current=r'$H_q(ST_{∙}(M)) \simeq H_q(C, M)$')
add('MP0319',r'presheaf $M$ a locally constant presheaf $M$ on the category',r'presheaf $M$ a locally constant presheaf $\check{M}$ on the category')
add('MP0320',r'let $C^{\wedge}$ be the topos of sheaves on $C$, and let $\epsilon: C \to C^{\wedge}$',r'let $C^{\sim}$ be the topos of sheaves on $C$, and let $\epsilon: C \to C^{\sim}$')
add('MP0325',r'and every every $𝒰$-sheaf of $A$-modules $M$',r'and every $𝒰$-sheaf of $A$-modules $M$')
add('MP0326',r'$\Leftrightarrow$ ii) of \hyperref[V.prop4.3]{4.2}.',r'$\Leftrightarrow$ ii) of \hyperref[V.prop4.3]{4.3}.')
add('MP0327',r'Since $F$ is flasque, $H^q(u^\ast(𝒳),F)$ for $q>0$',r'Since $F$ is flasque, $H^q(u^\ast(𝒳),F)=0$ for $q>0$')
add('MP0330',r"$u_{/X}:E_{/u^\ast X'}\to E'_{/X'}$ denotes",r"$u_{/X'}:E_{/u^\ast X'}\to E'_{/X'}$ denotes")
add('MP0333','send injective modules and injective modules','send injective modules to injective modules')

add('MP0334',r'ℋ^{0}_{Z_{/X}}(E_{/X},M|X){\quoi}.\tag{6.3.5}',r'H^{0}_{Z_{/X}}(E_{/X},M|X){\quoi}.\tag{6.3.5}')
add('MP0336',r'cohomological invariants $H^q_Z(E,N)$',r'cohomological invariants $H^q_Z(E,M)$')
add('MP0338',r'H^{0}((X,\Eext^{0}_A(M,N)){\quoi}.\tag{6.13.6}',r'H^{0}(X,\Eext^{0}_A(M,N)){\quoi}.\tag{6.13.6}',current=r'H^{0}_{\Phi}(X,\Eext^{0}_A(M,N)){\quoi}.\tag{6.13.6}')
add('MP0340',r'$E$ is coherent \emph{(VI},',r'$E$ is coherent \emph{(VI)},')
add('MP0342',r'the groups $H_i(K,M)$ vanish for $i>0$, or, equivalently, if the groups $H_i(K,M)$ vanish for $i>0$.',r'the groups $H_i(K,M)$ vanish for $i>0$, or, equivalently, if the groups $H_i(K)$ vanish for $i>0$.',current=r'the groups $H_i(K,M)$ vanish for $i>0$.',reason='Restore the complete equivalent-condition clause present in French D/E but absent from the released English; the canonical MP changes only the second homology expression.')
add('MP0343',r'to a morphism to $L_{∙}$. Thus $v_{∙}$ is surjective.',r'to a morphism to $K_{∙}$. Thus $v_{∙}$ is surjective.')
add('MP0344',r'is a covering isomorphism of presheaves (II \hyperref[II.rem6.2]{6.2}).',r'is a covering morphism of presheaves (II \hyperref[II.rem6.2]{6.2}).')
add('MP0354',r'=a(U\longmapsto\Gamma(U,\Ff_U){\quoi}.',r'=a(U\longmapsto\Gamma(U,\Ff_U)){\quoi}.')
add('MP0357',r'\Mm=\varinjlim_{(M,f)\in\Ll_2}M{\quoi},',r'\Mm=\varinjlim_{(M,f)\in\Ll_0}M{\quoi},')
add('MP0358','Séminaire Cartan 1957--1957.','Séminaire Cartan 1956--1957.',current='Séminaire Cartan 1957--1958.',reason='The released translation has a third date; the branches follow the canonical agreed MP and the exactly placed French diplomatic/corrected readings.')

no('MP0363',r'a $B$-functor $G$ from $J$ to $A$','The French article gender une→un has the same English article a; the functor and its source and target are unchanged.')
add('MP0366',r'\alpha_{\ast}(F(i) \longrightarrow G(j)',r'\alpha_{\ast}(F(i)) \longrightarrow G(j)')
add('MP0367','adjoint (\\resp a right adjoint, given by','adjoint (\\resp a right adjoint), given by')

add('MP0374',r'for which one verifies that $i$ is an isomorphism by',r'which is verified to be an isomorphism by')
add('MP0375',r'; $i$ is what is done, in particular,',r'; this is what is done, in particular,')
add('MP0378',r'Condition $2^{\circ}$) the preceding definition',r'Condition $2^{\circ}$) of the preceding definition')
mp380_start=S.index(r'\sisi{Every object $F$ of')
mp380_first,_,_,_=group(S,mp380_start+len(r'\sisi'))
add('MP0380',mp380_first.replace(r'\Ysheaf{\Gamma}(S\times D)',r'\Ysheaf{\Gamma}(S\times D,\mathcal{O}_S)'),mp380_first)
add('MP0382',r'S^{n,m}_2=\displaystyle\mathop{\sum}_{i=0}^{m+1}(-1)^j',r'S^{n,m}_2=\displaystyle\mathop{\sum}_{j=0}^{m+1}(-1)^j')
add('MP0384',r'\bar\theta_{\ast}$, taking values in',r'_G\bar\theta_{\ast}$, taking values in')

add('MP0391',r'To complete the proof of \hyperref[Vbis.prop3.1.1]{(3.11)},',r'To complete the proof of \hyperref[Vbis.prop3.1.1]{(3.1.1)},')
no('MP0393',r'equivalence for $G$-1-cohomological descent.','The French duplicated preposition/article pour de la is rendered by the single English preposition for in both readings; the stated descent property is unchanged.')
add('MP0394',r"t:K^+(\Gamma(h_c^{\ast}))\circ K^+(\Gamma(u'_{\alpha}))(r_0^{\ast}(J^{\bigdot}))",r"t:K^+(\Gamma(h_c^{\ast}))\circ K^+(\Gamma(u'_{\ast}))(r_0^{\ast}(J^{\bigdot}))")
add('MP0397',r'as $U$ ranges over the neighborhoods of $Y$, we have',r'as $U$ ranges over the neighborhoods of $y$, we have')
add('MP0398',r'and (\hyperref[Vbis.lem4.1.3]{4.1.3}) follows from the following lemma.',r'and (\hyperref[Vbis.cor4.1.2]{4.1.2}) follows from the following lemma.',current=r'and the result follows from the following lemma, (\hyperref[Vbis.lem4.1.3]{4.1.3}).',reason='The released English moves the reference to the following lemma. Restore the explicit source clause and retain the canonical printed/corrected reference numbers.')
add('MP0399',r'a finite union of the $V_b$ that like $B$,',r'a finite union of the $V_b$ that covers $B$,',reason='The canonical valid-word substitution comme→couvre changes the English like→covers; the deliberately defective diplomatic clause follows the recorded printed word.')
add('MP0401',r'where $X$ is a scheme and $F$ an étale sheaf on $X$',r'where $X$ is a scheme and $\mathcal{F}$ an étale sheaf on $X$')
add('MP0403',r"$MY_{\ell}\to Y_{\ell}\to Y'_{n+1}$ for every epimorphism",r"$NY_{\ell}\to Y_{\ell}\to Y'_{n+1}$ for every epimorphism")
add('MP0407',r'\item \emph{For every object $G$ of $B$, every diagram in $E_b$ of the form}',r'\item \emph{For every object $b$ of $B$, every diagram in $E_b$ of the form}')
add('MP0408',r'defined by an object $G$ of $B$.',r'defined by an object $b$ of $B$.')

add('MP0237',r'\Hhomtop(E)\tag{8.7.4}',r'\Hhomtop(F,E)\tag{8.7.4}',reason='The canonical printed target omits F. Keep the displayed equation tag outside that change and anchor the complete target to equation 8.7.4.')
add('MP0570',r'for $F$ of the form $F=i$, $G$, where',r'for $F$ of the form $F=i_{!}G$, where',reason='Keep the math delimiters in both complete English clauses while correcting the recorded comma to the extension-by-zero subscript.')


add('MP0016',r'limit of $\varphi_i(D)$ in $E_i$.',r'limit of $\varphi_i(F)$ in $F_i$.')
add('MP0022',r"They then factor as $X'\rightrightarrows u^\ast(Y)\rightarrow Y'$",r"They then factor as $X'\rightrightarrows u^\ast(Y')\rightarrow Y'$")
add('MP0037',r"such that $\varphi_i(X')\rightarrow \varphi(X)$ is not an isomorphism.",r"such that $\varphi_i(X')\rightarrow \varphi_i(X_\alpha)$ is not an isomorphism.")
add('MP0079',r'\varprojlim_j\Phi(j,i)){\quoi}',r'\varinjlim_j\Phi(j,i){\quoi}')
add('MP0119',r'(f^\ast)(X(\beta)_i))_{i\in J}',r'(f^\ast(X(\beta)_i))_{i\in J}',current=r'(f^\ast)(X(\beta)_i)_{i\in J}',reason='The final reviewed French pair preserves the extra printed closing parenthesis; the released translation has an intermediate spelling.')


add('MP0155',r'condition c) implies, by of what precedes,',r'condition c) implies, by what precedes,')
add('MP0174',r"$u:C\rightarrow C'$ a sheaf,",r"$u:C\rightarrow C'$ a functor,")
add('MP0208',r"the morphism $\Top(X')\rightarrow\Top(Y')$ deduced from the canonical continuous map $X'\rightarrow Y'$.",r"the morphism $\Top(X')\rightarrow\Top(X)$ deduced from the canonical continuous map $X'\rightarrow X$.")
add('MP0243',r'which are of one of the following three types (i) through (iv):',r'which are of one of the following four types (i) through (iv):')
add('MP0252',r'a family of subtopoi of $E$ whose intersection is $\Top(∅)$.',r'a family of subtopoi of $F$ whose intersection is $\Top(∅)$.')
add('MP0303',r'new interpretation of the functor $i_{!}i^{\ast}$.',r'new interpretation of the functor $i_{\ast}i^{!}$.')


add('MP0332',r'H^p(E,\Eext^q_A(F,G)){\quoi}.\tag{6.1.2}',r'H^p(E,\Eext^q_A(M,N)){\quoi}.\tag{6.1.2}')
add('MP0379',r'\ldots\to F^{n-1}\to F^{n-1}\to\Ker d^n',r'\ldots\to F^{n-2}\to F^{n-1}\to\Ker d^n')
add('MP0406',r"there exists an object $x'$ of $E_b$ satisfying $Q$",r"there exists an object $x'$ of $E_{b'}$ satisfying $Q$")
add('MP0426',r"with $X_i$ coherent, whence $X_i\simeq\Coker(X_1\rightrightarrows X_0)$",r"with $X_1$ coherent, whence $X'_i\simeq\Coker(X_1\rightrightarrows X_0)$")
add('MP0538',r'$\bar X=\Spec O_{X,x}$ be the corresponding strict localization',r'$\bar X=\Spec\Oo_{X,\xi}$ be the corresponding strict localization')
add('MP0550',r'two sheaves $F$, $G$ on $Y$, the natural diagram',r'two sheaves $F$, $G$ on $X$, the natural diagram')


add('MP0032',r'such that $fp_i=q_i$ for every $i\in I$.',r'such that $vp_i=q_i$ for every $i\in I$.')
add('MP0058',r'$\varphi(\alpha)h_if)=\varphi(\alpha)(h_ig)$',r'$\varphi(\alpha)(h_if)=\varphi(\alpha)(h_ig)$')
add('MP0068',r'to the inclusion $E\hookrightarrow E_{PF}$.',r'to the inclusion $E_{PF}\hookrightarrow E$.')
add('MP0102',r'$u_if_\alpha=v_i$.',r'$u_if_\alpha=v_\alpha$.')
add('MP0103',r'One then has $p_iu_i=p$,',r'One then has $p_iu_i=u$,')
add('MP0125',r'one also has $g_iu=g_iv$.',r'one also has $g_iu=g_jv$.')
add('MP0176',r'$\diag_u:F\rightarrow F\times_G G$ are covering.',r'$\diag_u:F\rightarrow F\times_G F$ are covering.')
add('MP0188',r'instead of $u^{\ast}$, \cf \phantom{13.2.3}.',r'instead of $u^{\ast}$, \cf \hyperref[IV.subsubsec13.2.3]{13.2.3}.')
add('MP0219',r'(6.8.5.2)',r'\eqhyperref[IV.eq6.8.6.1]{6.8.6.1}')
add('MP0249',r"$E'\cap E''_1=\Top(∅)$, then $E''$ is a complement of $E$.",r"$E'\cap E''_1=\Top(∅)$, then $E''$ is a complement of $E'$.")
add('MP0287',r'$\Top(X)_{/p^{\ast}(U)}\rightarrow\Top(X/r)$',r'$\Top(X)_{/p^{\ast}(U)}\rightarrow\Top(X/r)_{/U}$')
add('MP0293',r'\Hom_A(j_{X!}j^{\ast}_XM, n).',r'\Hom_A(j_{X!}j^{\ast}_XM, N).')
add('MP0341',r'\operatorname{Exp}^{p+q}_{A,\Phi}(E;M,N)',r'\Ext^{p+q}_{A,\Phi}(E;M,N)')
for ident in ['MP0372','MP0373']:
    add(ident,r'$H^n(X,\prod_{t\in T})=0$ for every $n$.',r'$H^n(X,\prod_{t\in T}F_t)=0$ for every $n>0$.',reason='The two canonical records concern the same clause. One joint pair restores the omitted factor and the missing strict inequality, with both source IDs.')
add('MP0427',r'every object $X$ of $E$ lying over a quasi-separated object $X$ of $E$ is itself quasi-separated',r'every object $X$ of $E$ lying over a quasi-separated object $Y$ of $E$ is itself quasi-separated',current=r'every object of $E$ lying over a quasi-separated object of $E$ is itself quasi-separated',reason='Restore the explicit variables present in both French branches and pair the second X→Y; the released English omits both variable names.')


add('MP0066',r'then the essential image of the functor $\bar f$ consists',r'then the essential image of the functor $\bar g$ consists')
add('MP0135',r"$g'\in S(g)$, so that",r"$g'\in S(h)$, so that")
add('MP0147',r'A topologically generating family (where, when no confusion can result, a generating family)',r'A topologically generating family (or, when no confusion can result, a generating family)')
add('MP0272',r'Give an example or $f_{\sob}$ is surjective but $f$ is not,',r'Give an example where $f_{\sob}$ is surjective but $f$ is not,')
add('MP0321',r'we put $H^q(X, M) = H^q(X, M)$',r'we put $H^q(X, M) = H^q(\epsilon(X), M)$')
no('MP0411',r'By the Lefschetz principle, we are reduced to the case $k = \CC$.','At the recorded proof of 5.2.5 the released English says the case k=C, with no independent rendering of French ou/où. Both French spellings map to this retained English construction; the separate nearby case where B=Sch/k is not this correction.')
no('MP0444',r'is finite if and only if $X$ is a finite set.','The released English renders the entire impersonal necessary-and-sufficient construction as if and only if. There is no separately rendered French et/il at this location; retain this complete biconditional and do not alter the earlier necessary-and-sufficient sentence.')
add('MP0544',r"$\varphi$ is of the form $\Ee_{\xi}$, hence",r"$\varphi$ is of the form $\Ee_{\xi'}$, hence")

add('MP0159',r'i_Aa_A(\coim(i_A(u))',r'i_Aa_A(\coim(i_A(u)))')

def finish():
    p=ROOT/'output/shared/EN_T1_T2_EXACT_PAIRS.json'
    p.write_text(json.dumps(ROWS,ensure_ascii=False,indent=2)+'\n')
    print(len(ROWS),'verified English assessments')

if __name__=='__main__':finish()
