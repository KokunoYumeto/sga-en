"""Full English contexts replacing ambiguous automatic Tome III projections."""
import review_en_t3 as review

PAIRS={
557:[(r"$(i\in I)$, and hence separated over $S$",r"$(i\in I)$, and hence separated over $X$"),
     (r"It is a subsheaf of $\fprod{G}{G}{S}$",r"It is a subsheaf of $\fprod{G}{G}{X}$")],
565:(r"There exists an irreducible étale neighborhood, hence a path-connected one, $U\rightarrow X$ of $P$ such that $F(U)$ maps surjectively onto",r"There exists an irreducible étale neighborhood, hence a path-connected one, $V\rightarrow X$ of $P$ such that $F(V)$ maps surjectively onto"),
575:(r"Consider assertion (i) of \eqhyperref[X.eq3.1]{3.1}",r"Consider assertion (i) of \hyperref[X.thm2.2]{2.2}"),
581:(r"Suppose that $\ell\neq 2$ where that no residue field of $\Spec A$ is orderable",r"Suppose that $\ell\neq 2$ or that no residue field of $\Spec A$ is orderable"),
584:(r"we are reduced to the case $X=X_{0}$ where $X=X_1$",r"we are reduced to the case $X=X_{0}$ or $X=X_1$"),
590:(r"$y_j$ $(i=1,\ldots,n-r);j=1,\ldots,n)$, and these functions",r"$y_j$ $(i=1,\ldots,n-r;j=1,\ldots,n)$, and these functions"),
594:(r"\longrightarrow \pi_0(X_0(\CC))\longrightarrow \pi_n (X(\CC))",r"\longrightarrow \pi_n(X_0(\CC))\longrightarrow \pi_n (X(\CC))"),
619:(r"$h^{\circ}:Y'\to X'$ be the morphism obtained from $h$ by the base change",r"$h':Y'\to X'$ be the morphism obtained from $h$ by the base change"),
622:(r"H^1(X,F)\longrightarrow H^1(Y,h^{\ast}(F)) $$ is bijective for $i=0,1$",r"H^i(X,F)\longrightarrow H^i(Y,h^{\ast}(F)) $$ is bijective for $i=0,1$"),
625:(r"${T'}^{i}(F)=H^{i}(Y,g^{\ast}(F))$",r"${T'}^{i}(F)=H^{i}(Y,h^{\ast}(F))$"),
626:(r"since the functor $h^{\bigdot}$ is exact",r"since the functor $h^{\ast}$ is exact"),
632:(r"identifies with the homomorphism $H^1(C,-)\rightarrow H^1(Y,h^{\ast}(-))$",r"identifies with the homomorphism $H^1(X,-)\rightarrow H^1(Y,h^{\ast}(-))$"),
658:(r"the fiber $(f_*F)_{\bar S}$ is isomorphic to $D^{C(S)}$",r"the fiber $(f_*F)_{\bar s}$ is isomorphic to $D^{C(s)}$"),
663:(r"&= d(y)=d(y_{0}){\quoi},",r"&= d(y)-d(y_{0}){\quoi},"),
673:(r"where $Y'$ is as in the statement of 2.6, and where",r"where $Y'$ is as in the statement of \hyperref[XIV.cor3.4]{3.4}, and where"),
706:(r"and $H^{2c}_Y(\ZZ/n\ZZ)$ is a sheaf on $Y$ locally isomorphic",r"and $\HH^{2c}_Y(\ZZ/n\ZZ)$ is a sheaf on $Y$ locally isomorphic"),
707:(r"(for the étale topology) to the constant sheaf $\ZZ/n\ZZ$).",r"(for the étale topology) to the constant sheaf $\ZZ/n\ZZ$."),
729:(r"Y\ar[lu]_{v}\ar[rrrr]_(.4){j}",r"Y\ar[lu]_{v}\ar[rrrr]_(.4){g}"),
736:(r"$f^{\ast}:\Aa_y\rightarrow \Aa_n$ exists; then",r"$f^{\ast}:\Aa_y\rightarrow \Aa_x$ exists; then"),
781:(r"The theorem \hyperref[XVII.subsubsec5.5.9]{5.5.9} follows from this lemma",r"The theorem \hyperref[XVII.thm5.4.3]{5.4.3} follows from this lemma"),
793:(r"Such a decomposition is a final object of $\Psi(S)$",r"Such a decomposition is a final object of $\Psi_f(S)$"),
794:(r"It follows that $\Psi$ is locally filtering on the right",r"It follows that $\Psi_f$ is locally filtering on the right"),
813:(r"The system $\Sym^{h\,n}_{T}((X^{h}_{u^{-1}(Z)}/Y^{h}_{Z})^{h+1})$ is therefore likewise",r"The system $\Sym^{h\,n}_{T}((X^{h}_{u^{-1}(Z)}/Y^{h}_{Z})^{k+1})$ is therefore likewise"),
814:(r"j_{!}:D(\sheafGamma(\bar{X}),\mathcal{A})\longrightarrow D(\sheafGamma(\bar{Y},\mathcal{A}))",r"j_{!}:D(\sheafGamma(\bar{X}),\mathcal{A})\longrightarrow D(\sheafGamma(\bar{Y}),\mathcal{A})"),
815:(r"R^{+}\bar{u}_{f\ast}\circ j_{!}\circ L^{+}\bar{u}_{f'{\ast}} \] which gives the desired isomorphism",r"R^{+}\bar{u}_{f\ast}\circ j_{!}\circ L^{+}\bar{u}_{f'}^{\ast} \] which gives the desired isomorphism"),
821:(r"(\pi^{p+}_1 (K^{\bigdot}))",r"(\pi^{p\ast}_1 (K^{\bigdot}))"),
822:(r"R^{+}f'_! \circ g'^{\ast}(K)",r"R^{+}f'_! \circ g'^{\ast}(K^{\bigdot})"),
830:(r"\xleftarrow{\sim} G\ &\text{\rm if}\quad \varphi\neq 0{\quoi}.",r"\xleftarrow{\sim} G\ &\text{\rm if}\quad \varphi=0{\quoi}."),
852:(r"The arrow $\sigma_{E,D_1}$ is therefore the composite",r"The arrow $\sigma_{D,E}$ is therefore the composite"),
855:(r"\tau:\langle\Ll,\Mm\rangle\xrightarrow{\sim}\langle\Ll,\Mm\rangle{\quoi}.\tag{1.3.15.1}",r"\tau:\langle\Ll,\Mm\rangle\xrightarrow{\sim}\langle\Mm,\Ll\rangle{\quoi}.\tag{1.3.15.1}"),
868:(r"0 \mathrel{\phantom{\longrightarrow}}\Eext^{1}(\sheafPic^{0}_{X/S},G)\longrightarrow R^{1}f_{\ast}G",r"0\longrightarrow\Eext^{1}(\sheafPic^{0}_{X/S},G)\longrightarrow R^{1}f_{\ast}G"),
869:[(r"H^{0}(S,R^{1}{f}_{\ast}\Nn(n))",r"H^{0}(S,R^{1}\bar{f}_{\ast}\Nn(n))"),
     (r"for $n$ sufficiently large, $R^{1}{f}_{\ast}\Nn(n)=0$",r"for $n$ sufficiently large, $R^{1}\bar{f}_{\ast}\Nn(n)=0$"),
     (r"$\Ll|f^{-1}(U)$ such that the pairs $(m_i,k)$ satisfy",r"$\Ll|\bar{f}^{-1}(U)$ such that the pairs $(m_i,k)$ satisfy")],
880:("The Kunneth isomorphism", "The Künneth isomorphism"),
881:("the asymmetric interpretation of the Kunneth arrow", "the asymmetric interpretation of the Künneth arrow"),
885:(r"and such that $\Tr_{h'}$ and $\Tr_{g'}$ are isomorphisms",r"and such that $\Tr_{h'_0}$ and $\Tr_{g'_0}$ are isomorphisms"),
886:(r"Let $h_1$ and $h'_1$ be the morphisms deduced from $h_0$ and $h'$ by base change to $V$",r"Let $h_1$ and $h'_1$ be the morphisms deduced from $h_0$ and $h'_0$ by base change to $V$"),
898:(r"If $U:K_1\rightarrow K_2$ is a morphism of objects \hyperref[XVIII.par3.1.16.1]{3.1.16.1}, then $U$ induces",r"If $u:K_1\rightarrow K_2$ is a morphism of objects \hyperref[XVIII.par3.1.16.1]{3.1.16.1}, then $u$ induces"),
913:(r"\ar[r]^(.45){e} & H^{m-1}(Y^{0},\ZZ/n)",r"\ar[r]^(.45){e} & H^{m-1}(Y,\ZZ/n)"),
915:(r"O_{X',p'}\cap Y=",r"O_{X',p'}\cap Y'="),
922:(r"and let $F$ be the sheaf induced by $F$ on $\widetilde U$",r"and let $\widetilde F$ be the sheaf induced by $F$ on $\widetilde U$"),
923:(r"Note that $U$ is obtained from $\widetilde X$ by localizing",r"Note that $\widetilde U$ is obtained from $\widetilde X$ by localizing"),
929:[(r"\bibitem{sga4.exp.XIX.bib.1}\textsc{Abyankhar}, S.",r"\bibitem{sga4.exp.XIX.bib.1}\textsc{Abhyankar}, S."),
     (r"\bibitem{sga4.exp.XIX.bib.2}\textsc{Abyankhar}, S.",r"\bibitem{sga4.exp.XIX.bib.2}\textsc{Abhyankar}, S.")],
}
SAME={
653:(r"In the second case, one cannot have both $x\in\overline{\{z\}}$ and $z\in V(g_x)$",
     "The repeated French designation s/z in 'Mais pour s in Ass O_X du deuxième type' is realized by the released English anaphora 'In the second case'. The English introduces z in the preceding sentence and retains z in both displayed conditions of this case; no separate English token realizes the repeated French variable. The earlier English z must remain z in both forms."),
}

if __name__=='__main__':
    review.PAIRS=PAIRS;review.SAME=SAME;review.INTERMEDIATE={
      852:r"The arrow $\sigma_{E,D}$ is therefore the composite",
      898:r"If $u:K_1\rightarrow K_2$ is a morphism of objects \hyperref[XVIII.par3.1.16.1]{3.1.16.1}, then $U$ induces"}
    review.main('EN_T3_AUTO_REPAIR_PAIRS.json')
    import json
    path=review.ROOT/'output/shared/EN_T3_AUTO_REPAIR_PAIRS.json'
    rows=json.loads(path.read_text())
    for row in rows:
        if row['id']=='MP0584':
            for delta in row['english_deltas']:delta['existing_human_source']='EN-ORG-0347'
    path.write_text(json.dumps(rows,ensure_ascii=False,indent=2)+'\n')
