"""Exact TeX placement for agreed records MP0702–MP0810.

Canonical top-level readings determine the pairs; nested metadata supplies no
extra change. The original inputs and Orgogozo note records are not modified.
"""
from pathlib import Path
import json,re
from fr_core import find_exact,page_span,INV
from review_t3 import locate
from marker_projection import carry_markers
ROOT=Path(__file__).resolve().parents[1]
PAIRS={
702:[(r'on peut supposer $Y$ normal',r"on peut supposer $Y'$ normal")],
703:[(r'\SGA IX 4.7',r'\SGA 1 IX 4.7')],
704:[(r'localement isomorphe à $u^{\ast}w^{\ast}(F)$',r'localement isomorphe à $u^{\ast}v^{\ast}(F)$')],
705:[(r'\sheaf{\Hom}(\HH^{2c}_Y(\ZZ/n\ZZ),H^{2c}_Y(F))',r'\sheaf{\Hom}(\HH^{2c}_Y(\ZZ/n\ZZ),\HH^{2c}_Y(F))')],
706:[(r'et $H^{2c}_Y(\ZZ/n\ZZ)$',r'et $\HH^{2c}_Y(\ZZ/n\ZZ)$')],
707:[(r'au faisceau constant $\ZZ/n\ZZ$).',r'au faisceau constant $\ZZ/n\ZZ$.')],
708:[(r'supposer $Y$, donc aussi $X$',r'supposer $S$, donc aussi $X$')],
709:[(r'$(\bar{h},\bar{j}_{!}\bar{F})$',r'$(h,\bar{j}_{!}\bar{F})$')],
710:[(r'(R^{q}f_{\cl\ast})',r'(R^{q}h_{\cl\ast})')],
711:[(r'\varepsilon^{\ast}(R^{p}h_{\text{et}\ast})(R^{q}a_{\text{et}\ast})F',r'\varepsilon^{\ast}(R^{p}b_{\text{et}\ast})(R^{q}a_{\text{et}\ast})F')],
712:[(r'on a $\dim Y\leq n$',r'on a $\dim Y<n$')],
713:[(r"h_{\text{cl}\ast}\varepsilon^{\ast}f_{\ast}F'",r"h_{\text{cl}\ast}\varepsilon^{\ast}f'_{\ast}F'")],
714:[(r"D'après \hyperrefext[XI][XI.prop3.3]{3.3} et il existe un",r"D'après \hyperrefext[XI][XI.prop3.3]{3.3}, il existe un")],
715:[(r'$(R^{q}j_{\ast})F=0$ si $q>0$',r'$(R^{q}j_{\ast})F=0$ si $q>1$')],
716:[(r'F(f):F(L)[-i]\rightarrow K',r'F(f):F(L)[-i]\rightarrow F(K)')],
717:[(r'vaut $0$ si $K_i\neq k_j$',r'vaut $0$ si $k_i\neq k_j$')],
718:[(r"L'exemple standart",r"L'exemple standard")],
719:[('flèches suivante sont','flèches suivantes sont')],
720:[('sous-additives et un foncteur qui vérifie','sous-additives est un foncteur qui vérifie')],
721:[(r"d'une catégorie sous-addtive",r"d'une catégorie sous-additive")],
722:[(r'Si $A=(X,Y,Z)$',r'Si $\Delta=(X,Y,Z)$')],
723:[(r'\Delta \ar[r]^{s}&\Delta',r"\Delta' \ar[r]^{s}&\Delta")],
724:[(r'est déployé pour $RF$.',r'est déployé pour $RF^{\bigdot}$.')],
725:[('on y résoud la perplexité','on y résout la perplexité')],
726:[(r"g'f^{\ast}f_{\ast}F",r"{g'}^{\ast}f^{\ast}f_{\ast}F")],
727:[(r'extrait de (2.1.2.3)',r'extrait de \eqhyperref[XVII.eq2.1.3.3]{2.1.3.3}')],
728:[(r'de $s$, $y$ et $z$ respectivement',r'de $x$, $y$ et $z$ respectivement')],
729:[(r"Y \ar[r]^{j}& Y'",r"Y \ar[r]^{g}& Y'")],
730:[(r'additive (\resp abélienne, \resp triangulée) sur $\Bb$.',r"additive (\resp abélienne, \resp triangulée) sur $\Bb'$.")],
731:[(r'$fd^{n}=f^{n+1} d$',r'$df^{n}=f^{n+1} d$')],
732:[(r'(d[1])_n=-d_{n+1}',r'(d[1])^{n}=-d^{n+1}')],
733:[('aux catégorie','aux catégories')],
734:[(r'$X\in \Ob F(n)$',r'$X\in \Ob F(x)$')],
735:[(r'définie par (2.1.12.1)',r'définie par \eqhyperref[XVII.eq2.2.12.1]{2.2.12.1}')],
736:[(r'f^{\ast}:\Aa_y\rightarrow \Aa_n',r'f^{\ast}:\Aa_y\rightarrow \Aa_x')],
737:[('dans le cas triangulée','dans le cas triangulé')],
738:[(r"X''\ar[rrr]& & & f^{\ast}Y''",r"X''\ar[rrr]^{s}& & & f^{\ast}Y''")],
739:[(r'\Hom_f(X,Y) \ar[r]&',r"\Hom_f(X,Y') \ar[r]&")],
740:[(r'fibrée (\resp cofibrée) sur $\Aa$',r'fibrée (\resp cofibrée) sur $I$')],
741:[(r'Soit $\Aa$',r'Soient $\Aa$')],
742:[(r'\Aa_1(S^{-1})',r'\Aa_1(S^{-1}_1)')],
743:[(r"A'_0\xrightarrow{s}A_{p}",r"A'_0\xrightarrow{s}A_{0}")],
744:[(r'\Ob \Aa(S^{-1}_0)',r'\Ob \Aa_0(S^{-1}_0)')],
745:[(r'$Rf^{\ast}$ est défini en $A_1$',r'$RF^{\ast}$ est défini en $A_1$')],
746:[(r'\Aa_{(S^{-1})}',r'\Aa(S^{-1})')],
747:[(r'\Aa_1({S^1}^{-1})',r'\Aa^1((S^1)^{-1})')],
748:[(r"B \ar[r]^{s}\ar[rrrd]^{b'}",r"B' \ar[r]^{s}\ar[rrrd]^{b'}")],
749:[('qui le rende commutatif','qui le rendent commutatif')],
750:[('sont pathologique','sont pathologiques')],
751:[(r'il faut que $h$ le soit',r'il faut que $f$ le soit')],
752:[(r'$f=fh$ se factorise',r'$f=gh$ se factorise')],
753:[(r"est l'isomorphismes \hyperref[XVII.par3.3.2.1]{3.3.2.1}",r"est l'isomorphisme \hyperref[XVII.par3.3.2.1]{3.3.2.1}")],
754:[('chaque cas les hypohtèses','chaque cas les hypothèses')],
755:[(r'une famille de point de $S$',r'une famille de points de $S$')],
756:[(r'est un faisceau flasque (V 3.7)',r'est un faisceau flasque \hyperrefext[V][V.def4.1]{4.1}')],
757:[(r'\Zz^{n-1}(F^1)',r"\Zz^{n-1}(F')")],
758:[(r'0\longrightarrow \mathcal{Z}^{n+1}(F)\longrightarrow \Cc^{n}(F)\longrightarrow \mathcal{Z}^{n}(F)\longrightarrow 0',r'0\longrightarrow \mathcal{Z}^{n-1}(F)\longrightarrow \Cc^{n}(F)\longrightarrow \mathcal{Z}^{n}(F)\longrightarrow 0')],
759:[('Il permettent','Elles permettent')],
760:[('bornés supériaurement','bornés supérieurement')],
761:[(r'Tor-dimension finie sur $f^{\ast}\Bb$',r'Tor-dimension finie sur $f^{-1}\Bb$')],
762:[(r'$\forall x \in V$',r'$\forall x \in X$')],
763:[('la composé des flèches','la composée des flèches')],
764:[(r'Les foncteur $j_{!}$ sont compatibles',r'Les foncteurs $j_{!}$ sont compatibles')],
765:[(r'(j_1 j_2)=j_{1!}j_{2!}',r'(j_1 j_2)_{!}=j_{1!}j_{2!}')],
766:[(r'Scholie \hyperref[XVII.subsubsec5.1.3]{5.1.3}',r'Scholie \hyperref[XVII.sch4.1.3]{4.1.3}')],
767:[(r"X \ar[d]^{f'}",r'X \ar[d]^{f}')],
768:[(r'c_{f,g}',r'c_{g,h}')],
769:[(r'R^{1}f_{!}\simeq R^{1}\bar{f}_{\ast}\circ f_{!}',r'R^{1}f_{!}\simeq R^{1}\bar{f}_{\ast}\circ j_{!}')],
770:[('commutent aux changement de base','commutent aux changements de base')],
771:[(r'sur $X_{\cl}$ acycliques',r'sur $\bar{X}_{\cl}$ acycliques')],
772:[(r'Rf_{\cl}=Rp_{\cl \ast} j_{\cl !}',r'Rf_{\cl !}=Rp_{\cl \ast} j_{\cl !}')],
773:[(r'dans $D(S,\epsilon^{\ast}\Aa)$',r'dans $D(S_{\cl},\epsilon^{\ast}\Aa)$')],
774:[(r'L=p^{\ast}\underset{\Aa}{\otimes} q^{\ast}L',r'L=p^{\ast}K\underset{\Aa}{\otimes} q^{\ast}L')],
775:[(r'L_{1}=g_{\ast}K',r'L_{1}=g_{\ast}L'),(r'L_{1}\rightarrow g_{\ast}K',r'L_{1}\rightarrow g_{\ast}L')],
776:[(r'K_1\boxtimes^{L}_{\Aa}L_{k}',r'K_1\boxtimes^{L}_{\Aa}L_{1}')],
777:[(r"\fprod{Z'}{Z_{1}}{Z_{1}}",r"\fprod{Z'}{Z_{1}}{Z}")],
778:[(r'morphisme de diagrammes (\hyperref[XVII.subsubsec5.4.1]{5.4.1})',r'morphisme de diagrammes \eqhyperref[XVII.eq5.4.1.1]{5.4.1.1}')],
779:[(r'Rh_{!}(C^{\ast}',r'Rh_{1!}(C^{\ast}')],
780:[(r'à une flèche \eqhyperref[XVII.eq5.4.4.1]{5.4.4.1}',r'à une flèche \eqhyperref[XVII.eq5.4.3.4]{5.4.3.4}')],
781:[(r'Le théorème \hyperref[XVII.subsubsec5.5.9]{5.5.9}',r'Le théorème \hyperref[XVII.thm5.4.3]{5.4.3}')],
782:[(r'\Sym^{n}_{\Spec(A)}(\Spec(B)\underset{\dfn}{=}',r'\Sym^{n}_{\Spec(A)}(\Spec(B))\underset{\dfn}{=}')],
783:[(r'(pour le second, (\textsc{Roby} \cite[IV 6 pg.275]{SGA4-17:Ro})',r'(pour le second, \textsc{Roby} \cite[IV 6 pg.275]{SGA4-17:Ro})')],
784:[(r"\Gamma^{n'}(M)\otimes \Gamma^{n''}(M)",r"\Gamma^{n'}(M')\otimes \Gamma^{n''}(M'')")],
785:[(r'de $n$ copies de $ℱ$',r'de $k$ copies de $ℱ$')],
786:[(r"\Gamma^{k}_{\ext}(F'')",r"\Gamma^{k_{2}}_{\ext}(F'')")],
787:[(r'\lvert L\Gamma^{k}_{\ext}(\Delta))\rvert',r'\lvert L\Gamma^{k}_{\ext}(\Delta)\rvert')],
788:[(r'par la seule hypohtèses que $u$',r'par la seule hypothèse que $u$')],
789:[(r"La théorie d'Artin-Scheier",r"La théorie d'Artin-Schreier")],
790:[(r"L'hypothèse signifie donc que morphisme",r"L'hypothèse signifie donc que le morphisme")],
791:[('restent valable','restent valables')],
792:[(r'(IV 14) sur $S_{\et}$',r'(\hyperrefext[V][V.def8.1.1]{8.1.1}) sur $S_{\et}$')],
793:[(r'un élément final de $\Psi(S)$',r'un élément final de $\Psi_f(S)$')],
794:[(r'Il en résulte que $\Psi$ est localement filtrante',r'Il en résulte que $\Psi_f$ est localement filtrante')],
795:[(r'g_{!}h_{!} h^{\ast}g_{\ast}',r'g_{!}h_{!} h^{\ast}g^{\ast}')],
796:[(r'\hyperref[XVII.prop6.1.1]{6.1.1}',r'\hyperref[XVII.subsubsec6.2.1]{6.2.1}')],
797:[('chaque point géométrie','chaque point géométrique')],
798:[(r"l'hmologie simplicial d'un simplexe",r"l'homologie simpliciale d'un simplexe")],
799:[(r"TS^{n_2}(\End(L'')",r"TS^{n_2}(\End(L''))")],
800:[(r'\Gamma^n_A\Gamma^n_{B}(C)',r'\Gamma^n_A\Gamma^m_{B}(C)')],
801:[(r'[\textsc{Grothendieck} \cite{SGA4-17:Gr})',r'(\textsc{Grothendieck} \cite{SGA4-17:Gr})')],
802:[(r'(6.3.4.3)',r'\eqhyperref[XVII.eq6.3.4.2]{6.3.4.2}')],
803:[('entre schéma lisses','entre schémas lisses')],
804:[(r'\Oo_{S(\Ff )}',r'\Oo_{\delta(\Ff )}')],
805:[(r"X=A'_{S}",r'X=\AAA^1_{S}')],
806:[(r"X=\AAA'_{S}",r'X=\AAA^1_{S}')],
807:[(r'Pour $f=P(T)$',r'Pour $\varphi=P(T)$')],
808:[('mutadis mutandis','mutatis mutandis')],
809:[(r'(au sens 6.2.17)',r'(au sens \hyperref[XVII.prop6.3.17]{6.3.17})')],
810:[(r'\Spec(S[\sigma_{1}\ldots\sigma_{n}]',r'\Spec(S[\sigma_{1}\ldots\sigma_{n}])')],
}
INTERMEDIATE={
 (765,1):r'(j_1 j_2)!=j_{1!}j_{2!}',
 (777,1):r"\fprod{Z'}{Z}{Z_{1}}",
 (798,1):r"l'homologie simplicial d'un simplexe",
 (801,1):r'\textsc{Grothendieck} \cite{SGA4-17:Gr})',
}

# Contexts read in the two baseline layers resolve repeated formulas and
# preserve unrelated human corrections inside the same paragraph.
PAIRS.update({
723:[(r"\Delta \ar[r]^{s}&\Delta''",r"\Delta' \ar[r]^{s}&\Delta''")],
761:[(r'\tTor-dimension finie sur $f^{\ast}\Bb$',r'\tTor-dimension finie sur $f^{-1}\Bb$')],
707:[(r'(pour la topologie étale) au faisceau constant $\ZZ/n\ZZ$).',r'(pour la topologie étale) au faisceau constant $\ZZ/n\ZZ$.')],
722:[(r'Si $A=(X,Y,Z)$ est un triangle distingué',r'Si $\Delta=(X,Y,Z)$ est un triangle distingué')],
729:[(r'Y\ar[lu]_{v} \ar[rrrr]_(.4){j}',r'Y\ar[lu]_{v} \ar[rrrr]_(.4){g}')],
730:[(r"catégorie $\Aa'=\fprod{\Aa}{\Bb'}{\Bb}$ est additive (\resp abélienne, \resp triangulée) sur $\Bb$.",r"catégorie $\Aa'=\fprod{\Aa}{\Bb'}{\Bb}$ est additive (\resp abélienne, \resp triangulée) sur $\Bb'$.")],
732:[(r'(d[1])_n=-d_{n+1}',r'(d[1])^n=-d^{n+1}')],
738:[(r"X''\ar[rrr]^{}\ar[ldd]",r"X''\ar[rrr]^{s}\ar[ldd]")],
739:[(r'\Hom_f(X,Y) \ar[r]& \Hom_f(X,Y)\ar[r]',r"\Hom_f(X,Y') \ar[r]& \Hom_f(X,Y)\ar[r]")],
742:[(r'de fibres $\Aa_0(S^{-1}_0)$ et $\Aa_1(S^{-1})$',r'de fibres $\Aa_0(S^{-1}_0)$ et $\Aa_1(S^{-1}_1)$')],
743:[(r"A'_0{\xrightarrow[s]{}}A_{p}",r"A'_0{\xrightarrow[s]{}}A_{0}")],
745:[(r'que $Rf^{\ast}$ est défini en',r'que $RF^{\ast}$ est défini en')],
746:[(r'\Hom_{\Aa_{(S^{-1})}}(A_0,A_1)',r'\Hom_{\Aa(S^{-1})}(A_0,A_1)')],
748:[(r"B\ar[uu]^{s}\ar[rrr]^{b'}\ar[ru]_{u}",r"B'\ar[uu]^{s}\ar[rrr]^{b'}\ar[ru]_{u}")],
753:[(r"est l'isomorphismes \hyperref[XVII.par3.3.2.1]{3.3.2.1} entre deux définitions de $f_{\ast}g_{\ast}$",r"est l'isomorphisme \hyperref[XVII.par3.3.2.1]{3.3.2.1} entre deux définitions de $f_{\ast}g_{\ast}$")],
756:[(r'est un faisceau flasque \emph{(V 3.7)}',r'est un faisceau flasque \emph{\hyperrefext[V][V.def4.1]{4.1}}')],
763:[(r'la composé des flèches \ding{195}',r'la composée des flèches \ding{195}')],
767:[(r"X'' \ar[r]_{i'} \ar[d]^{f''}& X\ar[d]^{f'}",r"X'' \ar[r]_{i'} \ar[d]^{f''}& X\ar[d]^{f}")],
768:[(r'transitivité $c_{f,g}$ entre $Rf_{!}$',r'transitivité $c_{g,h}$ entre $Rf_{!}$')],
770:[(r'\hyperref[XVII.var5.1.12]{5.1.12}) commutent aux changement de base.',r'\hyperref[XVII.var5.1.12]{5.1.12}) commutent aux changements de base.')],
776:[(r'K_1\overset{\LL}{\boxtimes}_{\Aa}L_{k}',r'K_1\overset{\LL}{\boxtimes}_{\Aa}L_{1}')],
779:[(r'Rh_{!}(C^{\ast}(K',r'Rh_{1!}(C^{\ast}(K'),(r'Rh_{!}(C^{\ast}K',r'Rh_{1!}(C^{\ast}K')],
783:[(r'(pour le second, (\textsc{Roby}',r'(pour le second, \textsc{Roby}')],
792:[(r'\emph{(IV 14)} sur $S_{\text{\rm et}}$',r'\emph{(\hyperrefext[V][V.def8.1.1]{8.1.1})} sur $S_{\text{\rm et}}$')],
797:[(r'chaque point géométrie $s$ de $U$',r'chaque point géométrique $s$ de $U$')],
800:[(r'\Gamma^{n}_A \Gamma^n_{B}(C)',r'\Gamma^{n}_A \Gamma^m_{B}(C)')],
805:[(r"au cas où $X=A'_{S}$.",r'au cas où $X=\AAA^1_{S}$.')],
806:[(r"$X=\AAA'_{S}$ et si $S$ est affine",r'$X=\AAA^1_{S}$ et si $S$ est affine')],
})

def main():
    data=json.loads((ROOT/'work_fr/initial_layers.json').read_text())
    records=json.loads((ROOT/'sources/fixes/MISPRINTS_4.json').read_text())
    assert set(PAIRS)==set(range(702,811))
    rows=[]
    for n,pairs in PAIRS.items():
        mp=records[n-1];f=INV[mp['expose']];page=mp['page']
        for j,(printed,corrected) in enumerate(pairs,1):
            row={'id':f'MP{n:04d}','part':j,'file':f,'page':page,'printed':printed,'corrected':corrected,
                 'source':f'fixes/MISPRINTS_4.json#MP{n:04d}',
                 'reason':'Exact TeX transcription of the accepted top-level reading; local source occurrence checked.'}
            for layer,target in [('dip',printed),('corr',corrected)]:
                text=data[layer][f];hits=locate(text,printed,corrected,page)
                if not hits and (n,j) in INTERMEDIATE:
                    hits=[(a,b,'source editorial reading') for a,b in find_exact(text,INTERMEDIATE[n,j],page)]
                if not hits:
                    hits=locate(text,printed,corrected,None)
                row[layer+'_hits']=len(hits)
                if len(hits)==1:
                    a,b,kind=hits[0];actual=text[a:b]
                    replacement=carry_markers(actual,target)
                    row[layer]={'old':actual,'new':replacement,'at':a,'state':kind,
                                'context_before':text[max(0,a-70):a],'context_after':text[b:b+70]}
                    data[layer][f]=text[:a]+replacement+text[b:]
                else:row[layer]={'status':'needs-location-review'}
            rows.append(row)
    out=ROOT/'output/shared/MP702_810_PAIRS.json';out.parent.mkdir(parents=True,exist_ok=True)
    out.write_text(json.dumps(rows,ensure_ascii=False,indent=2)+'\n')
    failed=[r for r in rows if r['dip_hits']!=1 or r['corr_hits']!=1]
    (ROOT/'work_fr/mp702_810_unlocated.json').write_text(json.dumps(failed,ensure_ascii=False,indent=2)+'\n')
    print('Records:',len(PAIRS),'Pairs:',len(rows),'unique in both layers:',len(rows)-len(failed),'need location:',len(failed))
    for r in failed: print(r['id'],r['part'],'dip',r['dip_hits'],'corr',r['corr_hits'])

if __name__=='__main__':main()
