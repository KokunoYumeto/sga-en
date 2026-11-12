"""Exact, reviewed TeX pairs for the agreed Tome III misprint records.

Each pair is manually transcribed from the supplied reading record and located
within its recorded printed page. Whitespace search preserves an offset map to
the original TeX; only the recorded span is replaced. No model prose is inserted.
"""
from pathlib import Path
import json,re,sys
from fr_core import find_exact, page_span, EXP, INV
from marker_projection import carry_markers

ROOT=Path(__file__).resolve().parents[1]
SRC=ROOT/'sources'

PAIRS={
 553:[(r'u^{\ast}F',r"u^{\ast}F'")],
 554:[(r"Alors $F=\varinjlim F(X')$",r"Alors $F_{\xi}=\varinjlim F(X')$")],
 555:[(r"$(s'\in S)$",r'$(s\in S)$')],
 556:[(r"extension de $L''_T$ par $G$",r"extension de $L''_T$ par $F'$")],
 557:[(r'$(i\in I)$, donc séparé sur $S$',r'$(i\in I)$, donc séparé sur $X$'),(r'\fprod{G}{G}{S}',r'\fprod{G}{G}{X}')],
 558:[(r'Comme $G$ est de plus constructible',r'Comme $H$ est de plus constructible')],
 559:[(r"$F_{\ell}=\Coker(H'\rightarrow F_J)$",r"$F_{\ell}=\Coker(H'\rightarrow G_J)$")],
 560:[(r"applique $N_1$ dans $N'_1$",r"applique $N'$ dans $N'_1$")],
 561:[(r'$f^{\ast}(S_i)$',r'$f^{\ast}(s_i)$')],
 562:[(r'$s_i$ $(s_{il},\ldots,s_{in_i})$',r'$s_i=(s_{i1},\ldots,s_{in_i})$')],
 563:[(r'$x\in X$, $x$ un point géométrique sur $x$',r'$x\in X$, $\bar{x}$ un point géométrique sur $x$')],
 564:[(r'$F(V)\rightarrow F_P$',r"$F(V')\rightarrow F_P$")],
 565:[(r'$U\rightarrow X$ de $P$ tel que $F(U)$',r'$V\rightarrow X$ de $P$ tel que $F(V)$')],
 566:[(r"$(p_i:X'_i\rightarrow X_i)$",r"$(p_i:X'_i\rightarrow X)$")],
 567:[(r'0\rightarrow H^1(X,i_{\ast}F)\rightarrow H^1(\Spec R(X) F)\rightarrow',r'0\rightarrow H^1(X,i_{\ast}F)\rightarrow H^1(\Spec R(X), F)\rightarrow')],
 568:[(r'\xrightarrow{n} (X,𝒪^{\ast}_X)',r'\xrightarrow{n} Γ(X,𝒪^{\ast}_X)')],
 569:[('donc surjectif','donc surjective')],
 570:[(r'$F=i$, $G$',r'$F=i_{!}G$')],
 571:[(r"$H(g_{\ast}i'_{!}\ZZ/r)=0$",r"$H(g_{\ast}i'_{!}\ZZ/\ell)=0$")],
 572:[(r'$(Y)=\Sup (Y_i)$',r'$\varphi(Y)=\Sup \varphi(Y_i)$')],
 573:[(r'$i:U\rightarrow X$',r'$i:U\rightarrow Y$')],
 574:[(r"D'après 7.6",r"D'après \hyperref[IX.prop5.6]{5.6}")],
 575:[(r'\eqhyperref[X.eq3.1]{3.1}',r'\hyperref[X.thm2.2]{2.2}')],
 576:[("n'est utilisé","n'est utilisée")],
 577:[(r'strictement local et inversible dans $\widetilde{R}$',r'strictement local et $\ell$ inversible dans $\widetilde{R}$')],
 578:[(r'\hyperref[X.lem2.2.1]{2.2.1}',r'\eqhyperref[X.eq2.2.2]{2.2.2}')],
 579:[(r"G'=G(\bar{K}/k')",r"G'=G(\bar{K}/K')")],
 580:[(r'\ZZ/r=H^1',r'\ZZ/\ell=H^1')],
 581:[(r"où qu'aucun corps résiduel",r"ou qu'aucun corps résiduel")],
 582:[(r'intègre, a corps des fractions',r'intègre, de corps des fractions')],
 583:[(r"à une extension séparable de $R(\widetilde{A})=K$",r"à une extension séparable de $R(A)=K$")],
 584:[(r'au cas $X=X_{0}$ où $X=X_1$',r'au cas $X=X_{0}$ ou $X=X_1$')],
 585:[(r'est le fibré de $X$',r'est la fibre de $X$')],
 586:[('Hironaha, H.','Hironaka, H.')],
 587:[('der reel abgeschlossenen Körper','der reell abgeschlossenen Körper')],
 588:[("un système d'hyperplane de", "un système d'hyperplans de")],
 589:[(r"si $k$ n'est pas défini",r"si $k$ n'est pas infini")],
 590:[(r'$(i=1,\ldots, n-r); j=1,\ldots,n)$',r'$(i=1,\ldots, n-r; j=1,\ldots,n)$')],
 591:[(r'Y \ar@{<-}[l]_{i}',r'Y \ar[l]_{i}')],
 592:[(r'$Y(\CC)\rightarrow X(\CC)$ est un isomorphisme',r"$Y(\CC)\rightarrow X'(\CC)$ est un isomorphisme")],
 593:[(r'vrai{} pour $S$',r'vrai{s} pour $S$')],
 594:[(r'\longrightarrow \pi_0(X_0(\CC))\longrightarrow',r'\longrightarrow \pi_n(X_0(\CC))\longrightarrow')],
 595:[(r'{\pi}_1=\varprojlim_N \pi_1/N',r'\widehat{\pi}_1=\varprojlim_N \pi_1/N')],
 596:[('p. 345 (1958)','p. 245 (1958)')],
 597:[('Vol. 39','Vol. 79')],
}

INTERMEDIATE={(582,1):r'intègre, de corps des fractions'}

PAIRS.update({
598:[(r'sur $F_{\ast}C$',r'sur $f_{\ast}C$')],
599:[(r'f_{\ast}(R^1g_{\ast})F',r'g_{\ast}(R^1f_{\ast})F')],
600:[(r"R^q{'}fg')_{\ast}{g'}^{\ast}=\\ =(R^q(gf')_{\ast}{g'}^{\ast}",r"R^q(fg')_{\ast}{g'}^{\ast}=R^q(gf')_{\ast}{g'}^{\ast}")],
601:[(r"g^{\ast}(R^q{f'}_{\ast}){g'}^{\ast}",r"g_{\ast}(R^q{f'}_{\ast}){g'}^{\ast}")],
602:[(r'g^{\ast}(R^q f_{\ast})(R^{q} e_{\ast})F',r'g^{\ast}(R^p f_{\ast})(R^{q} e_{\ast})F')],
603:[(r"R^{p+q}(f'e')_{\ast}g'^{\ast}F",r"R^{p+q}(f'e')_{\ast}g''^{\ast}F")],
604:[(r'Soit $f$ un faisceau de groupes',r'Soit $F$ un faisceau de groupes')],
605:[(r'(\hyperref[XII.thm5.1]{5.1}) a un morphisme',r'(\hyperref[XII.thm5.1]{5.1}) à un morphisme')],
606:[(r"H^1(X,F)\xrightarrow{\sim} H^1(X',F')",r"H^1(X,F)\longrightarrow H^1(X',F')")],
607:[(r'H^{1}(\bar{X}_0,\bar{F}_0) ,',r'H^{1}(\bar{X}_0,\bar{F}_0)^G ,')],
608:[(r'H^{\circ}(X_{\circ},F_{\circ})',r'H^1(X_{\circ},F_{\circ})')],
609:[(r'H^{\circ}(\bar{X},\bar{F}^{\alpha})^G',r'H^1(\bar{X},\bar{F}^{\alpha})^G')],
610:[(r'H^{n}(\bar{X}_0,\bar{F}_0)',r'H^{n}(X_0,F_0)')],
611:[('les homomorphisme de changement de base','les homomorphismes de changement de base')],
612:[(r'point corespondant $s$ de $S$',r'point correspondant $s$ de $S$')],
613:[("qu'on se dispense se répéter ici","qu'on se dispense de répéter ici")],
614:[(r'est triviale si $n=1$',r'est triviale si $n=-1$')],
615:[(r"T'^{\bigdot}(K^{\bigdot})",r"{T'}^{i}(K^{\bigdot})")],
616:[(r'nuls en degrés $\leq m+1$',r'nuls en degrés $\leq m$')],
617:[('autours','autour')],
618:[('mapping-cylinders','mapping-cylinder')],
619:[(r"$h^{\circ}:Y'\rightarrow X'$",r"$h':Y'\rightarrow X'$")],
620:[(r"des parties de $Y'$ à la fois ouvertes et fermées dans l'ensemble des parties de $X'$",r"des parties de $X'$ à la fois ouvertes et fermées dans l'ensemble des parties de $Y'$")],
621:[(r"\Pi_{\circ}(h'):\Pi_{\circ}(X')\longrightarrow \Pi_{\circ}(Y')",r"\pi_{\circ}(h'):\pi_{\circ}(Y')\longrightarrow \pi_{\circ}(X')")],
622:[(r'H^1(X,F)\longrightarrow H^1(Y,h^{\ast}(F))',r'H^i(X,F)\longrightarrow H^i(Y,h^{\ast}(F))')],
623:[(r"H^1(X',G_{X'})\longrightarrow H^1(Y',G_{X'})",r"H^i(X',G_{X'})\longrightarrow H^i(Y',G_{Y'})")],
624:[(r"H^{i}(X',(\ZZ/\ell^{\nu}\ZZ_{X'})\longrightarrow H^{i}(Y',\ZZ/\ell^{\nu}\ZZ)_{Y'})",r"H^{i}(X',(\ZZ/\ell^{\nu}\ZZ)_{X'})\longrightarrow H^{i}(Y',(\ZZ/\ell^{\nu}\ZZ)_{Y'})")],
625:[(r'H^{i}(Y,g^{\ast}(F))',r'H^{i}(Y,h^{\ast}(F))')],
626:[(r'h^{\bigdot}',r'h^{\ast}')],
627:[(r'H^1(Y,h\xi (F))',r'H^1(Y,h^{\ast}(F))')],
628:[(r'pour $F$ le $\ZZ/\ell\ZZ$-Module libre engendré par $F$',r'pour $G$ le $\ZZ/\ell\ZZ$-Module libre engendré par $F$')],
629:[(r'$h:X\rightarrow Y$',r'$h:Y\rightarrow X$')],
630:[(r'H^{0}(Y,R^{1}(p_{Y^{\ast}}(\bar{h}^{\ast}(\bar{F}))',r'H^{0}(Y,R^{1}(p_{Y^{\ast}}(\bar{h}^{\ast}(\bar{F}))))')],
631:[(r'H^{i}(X,-)\rightarrow H^1(Y,-)',r'H^{i}(X,-)\rightarrow H^{i}(Y,-)')],
632:[(r'$H^1(C,-)\rightarrow H^1(Y,-)$',r'$H^1(X,-)\rightarrow H^1(Y,-)$')],
633:[(r'n=1',r'n=-1')],
634:[(r'in-$\LL$-finis',r'ind-$\LL$-finis')],
635:[("d'exmeple","d'exemple")],
636:[('quasi-complet','quasi-compact')],
637:[('tout partie fermée','toute partie fermée')],
638:[(r'le long dé $Y$',r'le long de $Y$')],
639:[('était un contraire anti-ample','était au contraire anti-ample')],
640:[(r'\pi',r"\pi'")],
641:[(r'\cap^n_{k=1}U_k',r'\cap^r_{k=1}U_k')],
642:[(r'$S=\Spec (A_i)$',r'$S_i=\Spec (A_i)$')],
643:[('un isomorphe','un isomorphisme')],
644:[(r'$f_1:X_1\rightarrow X$',r'$f_1:X_1\rightarrow S$')],
645:[(r'Puisque $F$ est propre',r'Puisque $f$ est propre')],
646:[('des quotients que sont plats','des quotients qui sont plats')],
647:[(r'\Hhom$ $(M\times M\otimes M, M)$',r'\Hhom$ $(M\otimes M\otimes M, M)$')],
648:[(r'(0 \leq i\leq N-n)',r'(1 \leq i\leq N-n)')],
649:[(r'f_1,\ldots,f_{\nu}',r'f_1,\ldots,f_{N-n}')],
650:[(r'\PP^N_{\bar{S}}',r'\PP^N_S')],
651:[(r'$\supp$ ($D_{\circ}$ ne rencontre',r'$\supp(D_{\circ})$ ne rencontre')],
652:[(r'satisfaite $X$ est noethérien',r'satisfaite si $X$ est noethérien')],
653:[(r'$s\in \Ass \Oo_{X}$',r'$z\in \Ass \Oo_{X}$')],
654:[(r"T_x=Y'_n-Y'_x\cap U_x",r"T_x=Y'_x-Y'_x\cap U_x")],
655:[(r"D=\Sigma_x d'_x",r"D=\Sigma_x D'_x")],
656:[(r'que pour $\LL_{\circ}$ admet',r'que $\LL_{\circ}$ admet')],
657:[(r'$f=\ZZ/p$',r'$F=\ZZ/p$')],
658:[(r'$f_{\ast}(F)_{\bar{S}}$ est isomorphe à $D^{C(S)}$',r'$f_{\ast}(F)_{\bar{s}}$ est isomorphe à $D^{C(s)}$')],
659:[(r'(f\pi_i)_{\ast}G_i',r'(f\pi_i)_{\ast}C_i')],
660:[(r"l'image de $f_{\ast}G^{\alpha}$ par $\delta$. Puisque $f_{\ast}G$ est constructible",r"l'image de $f_{\ast}C^{\alpha}$ par $\delta$. Puisque $f_{\ast}C$ est constructible")],
661:[('On la suite exacte','On a la suite exacte')],
662:[(r'le cas où $F$ est de dimension relative $\leq 0$',r'le cas où $f$ est de dimension relative $\leq 0$')],
663:[(r'd(y)=d(y_{0}){\quoi}',r'd(y)-d(y_{0}){\quoi}')],
664:[(r'2.1 (d)',r'\hyperref[XIV.thm3.1]{3.1} (d)')],
665:[(r'\hyperref[XIV.subsec2.1]{2.1}',r'\hyperref[XIV.thm3.1]{3.1}')],
666:[(r'constructible sur $X=\fprod{X}{Y_K}{Y}$',r'constructible $F_\alpha$ sur $X_\alpha = \fprod{X}{Y_\alpha}{Y}$')],
667:[(r'q>D',r'q>d')],
668:[(r'\hyperref[XIV.subsec2.1]{2.1}~(d)',r'\hyperref[XIV.thm3.1]{3.1}~(d)')],
669:[(r'XX 6',r'\hyperrefext[XIX][XIX.sec6]{6}')],
670:[(r"Pour le cas $q=1$, notons que l'hypothèse que $X$ soit de dimension~$\leq 1$. Pour le cas $q=1$, notons que l'hypothèse que $X$ soit de dimension~$\leq 1$ implique",r"Pour le cas $q=1$, notons que l'hypothèse que $X$ soit de dimension~$\leq 1$ implique")],
671:[(r"l'espace affine dimension $1$",r"l'espace affine de dimension $1$")],
672:[(r'pour $n$ convenable',r'pour $N$ convenable')],
673:[(r'2.6',r'\hyperref[XIV.cor3.4]{3.4}')],
674:[(r'$R^{q}i_{\ast}F$, pour',r"$R^{q}i_{\ast}F'$, pour")],
675:[(r"R^{1}i_{\ast}(F')",r"R^{q}i_{\ast}(F')")],
676:[(r'H^{p}(\widetilde{U},\widetilde{F})',r'H^{q}(\widetilde{U},\widetilde{F})')],
677:[(r'\hyperrefext[IX][IX.prop2.7]{2.7}',r'\hyperrefext[IX][IX.cor2.7.4]{2.7.4}')],
678:[(r"\cd(U'')<d",r"\cd(U'')\leq d")],
679:[(r'le morphism $g:X_{0}',r'le morphisme $g:X_{0}')],
680:[(r'donnée par $f_{0}',r'donné par $f_{0}')],
681:[(r"générique de $Y'$",r"générique de $Y''$")],
682:[(r'\hyperref[XIV.def2.2]{2.2} pour un schéma de dimension $\leq d$',r'\hyperref[XIV.cor3.2]{3.2} pour un schéma de dimension $<d$')],
683:[(r"H^{q}(\bar{U}',\bar{F})",r"H^{q}(\bar{U}'',\bar{F})")],
684:[(r"H^{q}(G,H^{q}(\bar{U}'',\bar{F}))\Longrightarrow H^{n}(U'',F)",r"H^{p}(G,H^{q}(\bar{U}'',\bar{F}))\Longrightarrow H^{n}(U'',F)")],
685:[(r'acyclicité locale de $f$ (\hyperref[XV.def1.11]{1.11}), implique que $f$ est acyclique',r'acyclicité locale de $g$ (\hyperref[XV.def1.11]{1.11}), implique que $g$ est acyclique')],
686:[(r'(Si $f$ est quasi-compact et quasi-séparé.)',r'(Si $g$ est quasi-compact et quasi-séparé.)')],
687:[(r'la limite projective des $g$',r'la limite projective des $g_{\alpha}$')],
688:[(r"H^{q}(\widetilde{Y}',\widetilde{F})\longrightarrow H^{q}(\widetilde{X}',{\widetilde{g}''}{}^{\ast}\widetilde{F})",r"H^{q}(\widetilde{Y}'',\widetilde{F})\longrightarrow H^{q}(\widetilde{X}'',{\widetilde{g}''}{}^{\ast}\widetilde{F})")],
689:[(r"Y'_{\alpha}=\fprod{Y}{Y'_{0}}{Y_{0}}",r"Y'_{\alpha}=\fprod{\widetilde{Y}}{Y'_{0}}{Y_{0}}")],
690:[(r'H^{0}(Y,R^{n}g_{\ast}(g^{\ast}(F)){\quoi}',r'H^{0}(Y,R^{n}g_{\ast}(g^{\ast}(F))){\quoi}')],
691:[(r'H^{0}(Y,R^{1}g_{\ast}(g^{\ast}(F)){\quoi}',r'H^{0}(Y,R^{1}g_{\ast}(g^{\ast}(F))){\quoi}')],
692:[(r"$g_Z{}^{\ast}(j^{\ast}(i_{\ast}(F_U))=j'{}^{\ast}(g^{\ast}(i_{\ast}(F_U))$",r"$g_Z{}^{\ast}(j^{\ast}(i_{\ast}(F_U)))=j'{}^{\ast}(g^{\ast}(i_{\ast}(F_U)))$")],
693:[(r"$\LL\PP$ l'ensemble",r"$\LL\subset\PP$ l'ensemble")],
694:[(r'$A_i$',r'$A_1$')],
695:[('Abyankhar','Abhyankar')],
696:[(r'x\mathrel{\phantom{\in}}X',r'x\in X')],
697:[(r"\fprod{g}{\bar{Y}}{Y}:\fprod{Y'}{\bar{Y}}{Y}\rightarrow \bar{Y}",r"\fprod{g}{\bar{X}}{Y}:\fprod{Y'}{\bar{X}}{Y}\rightarrow \bar{X}")],
698:[(r"$\widetilde{X}=\fprod{X}{Y}{Y}$, $\widetilde{X}'=\fprod{X'}{Y'}{Y'}$",r"$\widetilde{X}=\fprod{X}{\widetilde{Y}}{Y}$, $\widetilde{X}'=\fprod{X'}{\widetilde{Y}'}{Y'}$")],
699:[(r'$1$-acyclique pour $\LL$',r'$n$-acyclique pour $\LL$')],
700:[(r'\ie $g$ localement $0$-acyclique',r'\ie $f$ localement $0$-acyclique')],
701:[(r"générique en $y'_1$",r'générique en $y_1$')],
})
INTERMEDIATE[664,1]=r'\ref{XIV.thm3.1} (d)'
PAIRS.update({
601:[(r"\xrightarrow{c} g^{\ast}(R^q{f'}_{\ast}){g'}^{\ast}",r"\xrightarrow{c} g_{\ast}(R^q{f'}_{\ast}){g'}^{\ast}")],
608:[(r'image dans $H^{\circ}(X_{\circ},F_{\circ})$, et soit',r'image dans $H^1(X_{\circ},F_{\circ})$, et soit')],
615:[(r"$T^{i}(K^{\bigdot})=T'^{\bigdot}(K^{\bigdot})=0$",r"$T^{i}(K^{\bigdot})={T'}^{i}(K^{\bigdot})=0$")],
617:[('flèches verticales autours de la flèche verticale médiane','flèches verticales autour de la flèche verticale médiane')],
622:[(r'H^1(X,F)\longrightarrow H^1(Y,h^{\ast}(F)) $$ est bijective pour $i=0$',r'H^i(X,F)\longrightarrow H^i(Y,h^{\ast}(F)) $$ est bijective pour $i=0$')],
626:[(r'le foncteur $h^{\bigdot}$ est exact',r'le foncteur $h^{\ast}$ est exact')],
627:[(r'comme image dans $H^1(Y,h\xi (F))$',r'comme image dans $H^1(Y,h^{\ast}(F))$')],
629:[(r"le morphisme $h:X\rightarrow Y$ satisfait également la condition d'injectivité",r"le morphisme $h:Y\rightarrow X$ satisfait également la condition d'injectivité")],
633:[(r'dans le premier cas, on suppose $n=1$',r'dans le premier cas, on suppose $n=-1$')],
640:[(r"\bar{X}'\ar[ll]_{\pi}\ar[ld]^{\bar{f}'}",r"\bar{X}'\ar[ll]_{\pi'}\ar[ld]^{\bar{f}'}")],
647:[(r'au-dessus du fibré vectoriel correspondant à $\Hhom$ $(M\times M\otimes M, M)$',r'au-dessus du fibré vectoriel correspondant à $\Hhom$ $(M\otimes M\otimes M, M)$')],
650:[(r'soit $Z$ le sous-schéma de $\PP^N_{\bar{S}}$',r'soit $Z$ le sous-schéma de $\PP^N_S$')],
663:[(r'&= d(y)=d(y_{0}){\quoi}',r'&= d(y)-d(y_{0}){\quoi}')],
665:[(r'Inversement, supposons que \hyperref[XIV.subsec2.1]{2.1}',r'Inversement, supposons que \hyperref[XIV.thm3.1]{3.1}')],
667:[(r'$R^{q}f_{\ast}F=0$ si $q>D$',r'$R^{q}f_{\ast}F=0$ si $q>d$')],
673:[(r"comme dans l'énoncé de 2.6 et",r"comme dans l'énoncé de \hyperref[XIV.cor3.4]{3.4} et")],
684:[(r'H^{q}(G,H^{q}(',r'H^{p}(G,H^{q}('),(r'H^{n}(U,F){\quoi}',r"H^{n}(U'',F){\quoi}")],
696:[(r"l'ouvert des $x\mathrel{\phantom{\in}}X$ en lesquels",r"l'ouvert des $x\in X$ en lesquels")],
})

PAIRS.update({
811:[(r'Une solution du problème est de prendre $K=G_{Y}$',r'Une solution du problème est de prendre $\Tr_{u}(K)=G_{Y}$')],
812:[(r'avec $y=x(Z)$',r'avec $y=x(z)$')],
813:[(r'$\Sym^{h\,n}_{T}((X^{h}_{u^{-1}(Z)}/Y^{h}_{Z})^{h+1})$',r'$\Sym^{h\,n}_{T}((X^{h}_{u^{-1}(Z)}/Y^{h}_{Z})^{k+1})$')],
814:[(r'D(\sheafGamma(\bar{Y},\mathcal{A}))',r'D(\sheafGamma(\bar{Y}),\mathcal{A})')],
815:[(r"L^{+}\bar{u}_{f'\ast}",r"L^{+}\bar{u}_{f'}^{\ast}")],
816:[(r'[[X_{1}|X]]_{[n]\times[m]}=[X_{1}|S]_{n}',r'[[X_{1}|X]]_{[n]\times[m]}=[X_{1}|X]_{n}')],
817:[(r'[X_{1}|X]_{n}\times [X_{2}|X]_{n}',r'[X_{1}|X]_{n}\times [X_{2}|X]_{m}')],
818:[(r'(\resp $(p_{2},j_{2},f_{2})$)',r'(\resp $(p_{2},j_{2},g_{2})$)')],
819:[(r'R^{p}(fj_{P})_{!}',r'R^{q}(fj_{P})_{!}')],
820:[(r"R^{+}f_{!}\circ {g'}^{\ast}(K^{\bigdot})",r"R^{+}f'_{!}\circ {g'}^{\ast}(K^{\bigdot})")],
821:[(r'\pi^{p+}_1',r'\pi^{p\ast}_1')],
822:[(r"g'^{\ast}(K)",r"g'^{\ast}(K^{\bigdot})")],
823:[('213--248','213--348')],
824:[('les morphismes limifiables via une','les morphismes lissifiables via une')],
825:[(r'sur $Y$',r'sur $\bar{Y}$')],
826:[(r'\Tr_{u}',r'\Tr_{\bar{u}}')],
827:[('dégré','degré')],
828:[('premier au caractéristiques résiduelles','premier aux caractéristiques résiduelles')],
829:[(r'R^{2}F_{!}\ZZ/n(1)',r'R^{2}f_{!}\ZZ/n(1)')],
830:[(r'\xleftarrow{\sim} G(S)\ &\text{\rm si}\quad \varphi\ne 0',r'\xleftarrow{\sim} G(S)\ &\text{\rm si}\quad \varphi= 0')],
831:[(r'\Psi(\lambda v):\varphi (\lambda)\Psi(v)',r'\Psi(\lambda v)=\varphi (\lambda)\Psi(v)')],
832:[(r'$W_{n}\subset \VV(\epsilon)^{\ast}$',r'$W_{n}\subset \VV(\epsilon)$')],
833:[(r'Les groupes $G^{n}$ étant affine,',r'Les groupes $G^{n}$ étant affines,')],
834:[(r'complexe cotangent relatif d de $G_{s}$',r'complexe cotangent relatif de $G_{s}$')],
835:[(r'par 1.2.0',r'par \hyperref[XVIII.subsubsec1.2.10]{1.2.10}')],
836:[(r'ainsi qu\'on le prouvera en (1.2.7.3)',r'ainsi qu\'on le prouvera en (\hyperref[XVIII.subsubsec1.2.13]{1.2.13})')],
837:[(r'\etiquette[1.2.2.12]',r'\etiquette[1.2.12]')],
838:[(r'(1.2.2.11)',r'(\hyperref[XVIII.subsubsec1.2.11]{1.2.11})')],
839:[(r'\etiquette[1.2.2.13]',r'\etiquette[1.2.13]')],
840:[(r'bis) $\varphi$ est donc algébrisable',r'bis) $\widehat{\varphi}$ est donc algébrisable')],
841:[(r'$p:\PP_{S}\rightarrow S$',r'$p:\PP^r_{S}\rightarrow S$')],
842:[('finie, où image réciproque','finie, ou image réciproque')],
843:[(r'vérifiant (1.3.3.1)',r'vérifiant (\hyperref[XVIII.par1.3.2.1]{1.3.2.1})')],
844:[(r'$\pi^{\ast}Z_{\Ll}+Z_{\Ll_{1}}+Z_{\Ll_{2}}$',r'$\pi^{\ast}Z_{\Ll}\simeq Z_{\Ll_{1}}+Z_{\Ll_{2}}$')],
845:[(r'u^{\ast}_{s}\Oo(1)+\mathcal{U}^{\vee}_{s}',r'u^{\ast}_{s}\Oo(1)\simeq \mathcal{U}^{\vee}_{s}')],
846:[(r'\Tr_{D/S}(K)',r'\Tr_{D_u/S}(K)')],
847:[('diviseurs de Cartier relatif effectifs','diviseurs de Cartier relatifs effectifs')],
848:[(r'\Tr_{p_{\ast}E/S}(K)',r'\Tr_{u_{\ast}E/S}(K)')],
849:[(r'\Tr_{p^{\ast}E/S}(K)',r'\Tr_{u^{\ast}E/S}(K)')],
850:[(r'considérés en (1.2.9)',r'considérés en (\hyperref[XVIII.subsubsec1.3.9]{1.3.9})')],
851:[(r'relatif $t(S)$',r'relatif $t(T)$')],
852:[(r'La flèche $\sigma_{E,D_1}$ est donc composée',r'La flèche $\sigma_{D,E}$ est donc composée')],
853:[(r'et 1.3.12.2 en résulte aussitôt',r'et \eqhyperref[XVIII.eq1.3.12.1]{1.3.12.1} en résulte aussitôt')],
854:[(r'le degré (1.3.2.7)',r'le degré (\hyperref[XVIII.subsubsec1.3.7]{1.3.7})')],
855:[(r'\tau:\langle \Ll,\Mm\rangle \xrightarrow{\sim}\langle \Ll,\Mm\rangle',r'\tau:\langle \Ll,\Mm\rangle \xrightarrow{\sim}\langle \Mm,\Ll\rangle')],
856:[(r'1.2.9.7',r'\hyperref[XVIII.par1.3.8.6]{1.3.8.6}')],
857:[(r'(1.2.16.2)',r'\eqhyperref[XVIII.par1.3.16.2]{1.3.16.2}')],
858:[(r'canoniquement isomorphe à $k$',r'canoniquement isomorphes à $k$')],
859:[('effectif','effectifs')],
860:[('très ample','très amples')],
861:[(r'une application $ℱ:ℱ:M(I)\rightarrow \Ob C$',r'une application $ℱ:M(I)\rightarrow \Ob C$')],
862:[(r'F(ℱ(k),ℱ(g))',r'F(ℱ(h),ℱ(g))')],
863:[(r'F(x_1,x_2) + F(y_1,x_2) +F(y_1,x_2)+F(y_1,y_2)',r'F(x_1,x_2) + F(y_1,x_2) +F(x_1,y_2)+F(y_1,y_2)')],
864:[(r'de coordonnées $K_{i}$',r'de coordonnées $k_{i}$')],
865:[(r"{K'}^{-1}=\fprod{{K'}^{-1}}{{K'}^{0}}{K^{0}}",r"{K'}^{-1}=\fprod{K^{-1}}{{K'}^{0}}{K^{0}}")],
866:[(r'\ell^{-1}(t_{1};x_{1},y_{1})+\ell^{-1}(t_{1};x_{2},y_{2})',r'\ell^{-1}(t_{1};x_{1},y_{1})+\ell^{-1}(t_{2};x_{2},y_{2})')],
867:[(r'\tau_{\leq} R\Hhom(\ZZ^{(F)},C^{\flat})',r'\tau_{\leq 0} R\Hhom(\ZZ^{(F)},C^{\flat})')],
868:[(r'0 \mathrel{\phantom{\longrightarrow}}\Eext^{1}(\sheafPic^{0}_{X/S},G)',r'0 \longrightarrow \Eext^{1}(\sheafPic^{0}_{X/S},G)')],
869:[(r'R^{1}f_{\ast}\Nn(n), \Ll|f^{-1}(U)',r'R^{1}\bar{f}_{\ast}\Nn(n), \Ll|\bar{f}^{-1}(U)')],
870:[(r'\tag{1.3.12.3}',r'\tag{1.5.12.3}')],
871:[(r'(pour $i=0,1$)',r'(pour $i=1,2$)')],
872:[(r"D'après (1.3.13.1)",r"D'après \eqhyperref[XVIII.par1.5.13.1]{1.5.13.1}")],
873:[(r'le préfaisceaux qui à chaque section $S$ sur $k$ associe',r'le préfaisceau qui à chaque schéma $S$ sur $k$ associe')],
874:[(r'La suite exacte de Kummer 1.4.1 fournit',r'La suite exacte de Kummer \hyperref[XVIII.lem1.6.1]{1.6.1} fournit')],
875:[(r'R^{p+q}(fg)!F',r'R^{p+q}(fg)_{!}F')],
876:[(r'et tel que les fibres $X-U$ soient de dimension $< d$',r'et tel que les fibres de $X-U$ soient de dimension $< d$')],
877:[(r'(XVII 5.5.2.1)',r'\eqhyperrefext[XVII][XVII.eq5.2.2.1]{5.2.2.1}')],
878:[('Il est immédiatement, grâce à (Var 3)','Il est immédiat, grâce à (Var 3)')],
879:[(r'$a$, $u$, $e$ et $v$',r'$a$, $u$, $c$ et $v$')],
880:[('Kunneth','Künneth')],
881:[('Kunneth','Künneth')],
882:[(r'R^{i}f_V\ZZ/n',r'R^{i}f_{V!}\ZZ/n')],
883:[(r'K_{i+i}',r'K_{i+1}')],
884:[(r'le diagramme 2.12.3 relatif',r'le diagramme \eqhyperref[XVIII.eq2.14.3]{2.14.3} relatif')],
885:[(r"$\Tr_{h'}$ et $\Tr_{g'}$",r"$\Tr_{h'_0}$ et $\Tr_{g'_0}$")],
886:[(r"$h'$",r"$h'_0$")],
887:[(r'\Hom(Rf_!K)[1],L)',r'\Hom((Rf_!K)[1],L)')],
888:[(r'\Hom(Rf_!K,L[-1]',r'\Hom(Rf_!K,L[-1])')],
889:[(r'\tau_{\leq 2d}C^\ast j_{!}F',r'\tau_{\leq 2d}C^\ast_{\ell}j_{!}F')],
890:[(r"=\Hom_{K(X)}(K',L')",r"=\Hom_{K(X)}(K',f^{!}_{\bigdot}L')")],
891:[(r'H^{0}(V,R\Hom(Rf_{!}K,L))\simeq \Hhom(k^{\ast}Rf_{!}K,k^{\ast}L)',r'H^{0}(V,R\Hhom(Rf_{!}K,L))\simeq \Hom(k^{\ast}Rf_{!}K,k^{\ast}L)')],
892:[(r'Pour $V=X$',r'Pour $V=S$')],
893:[(r'$\varphi:\mathcal{B}\rightarrow \mathcal{A}$',r'$\varphi:\mathcal{A}\rightarrow \mathcal{B}$')],
894:[('vérifient chacun deux compatibilité du type','vérifient chacun deux compatibilités du type')],
895:[(r'\varphi\in \Hom(X,f^{\ast}V)',r'\varphi\in \Hom(U,f^{\ast}V)')],
896:[(r'couvrant $U$',r'couvrent $U$')],
897:[(r'adjoint à droite $f_{\Gamma\bigdot}$',r'adjoint à gauche $f_{\Gamma\bigdot}$')],
898:[(r'Si $U:K_{1}\rightarrow K_{2}$',r'Si $u:K_{1}\rightarrow K_{2}$'),(r'alors $U$ induit',r'alors $u$ induit')],
899:[(r'\Ext^{p}(ℋ^{-q}(K(W)),L)',r'\Ext^{p}(ℋ^{-q}(K(U)),L)')],
900:[(r'W_{1}=(U_{1},V_{1},\varphi_{1})\mathrel{\phantom{\to}}W_{2}=(U_{2},V_{2},\varphi_{2})',r'W_{1}=(U_{1},V_{1},\varphi_{1})\to W_{2}=(U_{2},V_{2},\varphi_{2})')],
901:[(r"R{k'}^{!}",r"R{K'}^{!}")],
902:[(r'réduit $\ZZ/n(-d)$ placé',r'réduit à $\ZZ/n(-d)$ placé')],
903:[(r"\ZZ/N(-d)=K''(U,V,\varphi))",r"\ZZ/n(-d)=K''(U,V,\varphi)")],
904:[(r'\longrightarrow Rk^{!}\simeq',r'\longrightarrow RK^{!}\simeq')],
905:[(r'définition de $t$, en termes du foncteur $f^!_\bigdot$ (3.1.9.10)',r'définition de $t_f$, en termes du foncteur $f^!_\bigdot$ \eqhyperref[XVIII.eq3.1.4.10]{3.1.4.10}')],
906:[('dont au laisse au lecteur','dont on laisse au lecteur')],
907:[(r'f^{\ast}L(d)[2d] \ar[d]',r'f^{\ast}L(d)[2d]) \ar[d]')],
908:[('de long de','le long de')],
909:[('birationel','birationnel')],
910:[(r"dont l'ensemble des images dans $A$ est encore",r"dont l'ensemble des images dans $A'$ est encore")],
911:[(r'$B=A/(x)$',r'$B=A/(x_{r})$')],
912:[(r'\hyperref[XIX.thm2.1]{2.1}',r'\hyperref[XIX.lem2.2]{2.2}')],
913:[(r'H^{m-1}(Y^{0},\ZZ/n)',r'H^{m-1}(Y,\ZZ/n)')],
914:[(r'est une résolution de $\Spec A$',r"est une résolution de $\Spec A'$")],
915:[(r"$\Spec O_{X',p'}\cap Y=V(x'_{1},\ldots,x'_{r})$",r"$\Spec O_{X',p'}\cap Y'=V(x'_{1},\ldots,x'_{r})$")],
916:[(r'(R^{1}j_{\ast})𝛍_{n})\simeq',r'(R^{1}j_{\ast})𝛍_{n}\simeq')],
917:[(r"le morphisme $(3.3')$",r'le morphisme (\hyperref[XIX.eq3.3.2]{3.3.2})')],
918:[(r'((Y,X) \boxtimes 𝛍_{n}^{\boxtimes b})',r'(\varphi(Y,X) \otimes 𝛍_{n}^{\otimes b})')],
919:[(r'$Z-C\cap \bar{Z}$',r'$\bar{Z}-C\cap \bar{Z}$')],
920:[(r'$g$ et un morphisme local',r'$g$ est un morphisme local')],
921:[(r'H^{p}(G,H^{q}(U,.))\Longrightarrow H^{p+q}(U,.)',r'H^{p}(G,H^{q}(\widetilde{U},.))\Longrightarrow H^{p+q}(U,.)')],
922:[(r'et $F$ le faisceau induit',r'et $\widetilde{F}$ le faisceau induit')],
923:[(r'Notons que $U$',r'Notons que $\widetilde{U}$')],
924:[(r'H^{q}(\widetilde{U},F)=0',r'H^{q}(\widetilde{U},\widetilde{F})=0')],
925:[('équidimensionel','équidimensionnel')],
926:[(r'A_{0}=k[[x_{1},\ldots,x_{d-1}]]',r'A^{0}=k[[x_{1},\ldots,x_{d-1}]]')],
927:[(r'le lemme de Abyankhar',r'le lemme de Abhyankar')],
928:[(r'R^{q}f^{0}_{\ast}(\ZZ/\ell))\Longrightarrow H^{p+q}(U^{0},\ZZ/\ell)',r'R^{q}f^{0}_{\alpha\ast}(\ZZ/\ell))\Longrightarrow H^{p+q}(U^{0}_{\alpha},\ZZ/\ell)')],
929:[(r'\textsc{Abyankhar}, S.',r'\textsc{Abhyankar}, S.')],
930:[('et Résolution of singularities of','et Resolution of singularities of')],
})
INTERMEDIATE.update({(820,1):r"R^{+}f_{!}'\circ {g'}^{\ast}(K^{\bigdot})",
    (831,1):r'\Psi(\lambda v)=...', (852,1):r'La flèche $\sigma_{E,D}$ est donc composée',
    (927,1):r'le lemme \nde Abhyankar'})

PAIRS.update({
815:[(r"R^{+}\bar{u}_{f\ast}\circ j_{!}\circ L^{+}\bar{u}_{f'\ast}",r"R^{+}\bar{u}_{f\ast}\circ j_{!}\circ L^{+}\bar{u}_{f'}^{\ast}")],
822:[(r"R^{+}f'_! \circ g'^{\ast}(K)",r"R^{+}f'_! \circ g'^{\ast}(K^{\bigdot})")],
826:[(r'\bar{u}_{\ast}𝛍_n \ar[r] \ar[d]^{\Tr_{u}}',r'\bar{u}_{\ast}𝛍_n \ar[r] \ar[d]^{\Tr_{\bar{u}}}')],
827:[(r'sa norme est encore de dégré $1$',r'sa norme est encore de degré $1$')],
829:[(r'\Tr_{f}:R^{2}F_{!}\ZZ/n(1)\xleftarrow{\sim}',r'\Tr_{f}:R^{2}f_{!}\ZZ/n(1)\xleftarrow{\sim}')],
830:[(r'\xleftarrow{\sim} G\ &\text{\rm si}\quad \varphi\neq 0',r'\xleftarrow{\sim} G\ &\text{\rm si}\quad \varphi= 0')],
831:[(r'\Psi(\lambda v):\varphi (\lambda)\Psi(v)',r'\Psi(\lambda v)=\Psi(v)\varphi(\lambda)')],
836:[(r"ainsi qu'on le prouvera en (1.2.7.3)",r"ainsi qu'on le prouvera en (\hyperref[XVIII.subsubsec1.2.13]{1.2.13})")],
845:[(r'u^{\ast}\Oo(1)+\mathcal{U}^{\vee}',r'u^{\ast}\Oo(1)\simeq \mathcal{U}^{\vee}')],
869:[(r'H^{0}(S,R^{1}f_{\ast}\Nn(n))',r'H^{0}(S,R^{1}\bar{f}_{\ast}\Nn(n))'),
     (r'pour $n$ assez grand, $R^{1}f_{\ast}\Nn(n)=0$',r'pour $n$ assez grand, $R^{1}\bar{f}_{\ast}\Nn(n)=0$'),
     (r'$\Ll|f^{-1}(U)$ telle que les couples',r'$\Ll|\bar{f}^{-1}(U)$ telle que les couples')],
878:[('Il est immédiatement, grâce à (Var 3)','Il est immédiatement clair, grâce à (Var 3)')],
880:[("L'isomorphisme de Kunneth","L'isomorphisme de Künneth")],
884:[(r'le diagramme 2.12.3 relatif à $K_{2k}$',r'le diagramme \eqhyperref[XVIII.eq2.14.3]{2.14.3} relatif à $K_{2k}$')],
907:[(r'\Hom^{\bigdot}(f^{\ast}K(d)[2d], f^{\ast}L(d)[2d] \ar[d]',r'\Hom^{\bigdot}(f^{\ast}K(d)[2d], f^{\ast}L(d)[2d]) \ar[d]')],
911:[(r'$B=A/(x)$',r'$B=A/(x_r)$')],
913:[(r'\ar[r]^(.45){e} & H^{m-1}(Y^{0},\ZZ/n)',r'\ar[r]^(.45){e} & H^{m-1}(Y,\ZZ/n)')],
917:[(r"le morphisme $(3.3')$",r'le morphisme \eqhyperref[XIX.eq3.3.2]{3.3.2}')],
918:[(r'((Y,X) \otimes 𝛍_{n}^{\otimes b})',r'(\varphi(Y,X) \otimes 𝛍_{n}^{\otimes b})')],
928:[(r'R^{q}f^{0}_{\ast}(\ZZ/\ell))\Longrightarrow H^{p+q}(U^{0},\ZZ/\ell)',r'R^{q}f^{0}_{\alpha\ast}(\ZZ/\ell))\Longrightarrow H^{p+q}(U^{0}_{\alpha},\ZZ/\ell)')],
929:[(r'\bibitem{SGA4-19:1} \textsc{Abyankhar}, S.',r'\bibitem{SGA4-19:1} \textsc{Abhyankar}, S.'),
     (r'\bibitem{SGA4-19:2} \textsc{Abyankhar}, S.',r'\bibitem{SGA4-19:2} \textsc{Abhyankar}, S.')],
})
INTERMEDIATE.update({(831,1):r'\Psi(\lambda v)=\varphi (\lambda)\Psi(v)',
 (913,1):r'\ar[r]^(.45){e} & H^{m-1}(Y^0,\ZZ/n)',
 (928,1):r'R^{q}f^{0}_{\alpha\ast}(\ZZ/\ell))\Longrightarrow H^{p+q}(U^{0},\ZZ/\ell)'})
INTERMEDIATE[884,1]=r'le diagramme 2.14.3 relatif à $K_{2k}$'

# These misprints concern visible heading numbers; etiquette alone is a label.
for num,label,title in [
 (837,'1.2.12',r'Algébricité de $\widehat{\varphi}$: vérification préliminaire pour un trait de base'),
 (839,'1.2.13',r'Algébricité de $\widehat{\varphi}$')]:
    bad=label.replace('1.2.','1.2.2.')
    heading=r'\subsubsection{'+title+r'}\etiquette['+label+r']{XVIII.subsubsec'+label+'}'
    wrong=(r'\let\SGAsavedsubsubsection\thesubsubsection'+
           r'\renewcommand{\thesubsubsection}{'+bad+'}'+
           heading.replace('['+label+']','['+bad+']')+
           r'\let\thesubsubsection\SGAsavedsubsubsection')
    PAIRS[num]=[(wrong,heading)]

def locate(text,old,new,page):
    choices=[]
    for kind,word in [('print',old),('corrected',new)]:
        for a,b in find_exact(text,word,page):
            choices.append((a,b,kind))
    # Remove an old reading found only as a strict substring of its correction.
    choices=[c for c in choices if not any(d[0]<=c[0] and d[1]>=c[1] and d[1]-d[0]>c[1]-c[0] for d in choices)]
    choices=list(dict.fromkeys(choices))
    return choices

def main():
    data=json.loads((ROOT/'work_fr/initial_layers.json').read_text())
    mps=json.loads((SRC/'fixes/MISPRINTS_4.json').read_text())
    rows=[]
    for n,pairs in sorted(PAIRS.items()):
        mp=mps[n-1];f=INV[mp['expose']];page=mp['page']
        for j,(printed,corrected) in enumerate(pairs,1):
            row={'id':f'MP{n:04d}','part':j,'file':f,'page':page,'printed':printed,'corrected':corrected,
                 'source':f'fixes/MISPRINTS_4.json#MP{n:04d}',
                 'reason':'Exact TeX transcription of the accepted model reading; local source context checked.'}
            if n==582:
                row['reason']=('The printed a is corrected by Orgogozo’s existing sisi{a}{de}; '
                    'retain E’s de and the human record unchanged. Sol explicitly proposes de; '
                    'Opus proposes à. Both de corps des fractions K and à corps des fractions K '
                    'give the same relation: K is the field of fractions of A. DEC-MP0582 records '
                    'the canonical top-level alternative à without replacing the human correction.')
            for layer,target in [('dip',printed),('corr',corrected)]:
                text=data[layer][f];hits=locate(text,printed,corrected,page)
                if not hits and (n,j) in INTERMEDIATE:
                    hits=[(a,b,'source editorial reading') for a,b in find_exact(text,INTERMEDIATE[n,j],page)]
                if not hits:
                    # A few recorded folios precede/follow an edition marker.
                    # Use a globally unique exact phrase only, never fuzzy text.
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
    out=ROOT/'output/shared/MP_T3_PATCHES.json';out.write_text(json.dumps(rows,ensure_ascii=False,indent=2)+'\n')
    (ROOT/'work_root').mkdir(exist_ok=True)
    (ROOT/'work_root/t3_layers.json').write_text(json.dumps(data,ensure_ascii=False))
    failed=[r for r in rows if r['dip_hits']!=1 or r['corr_hits']!=1]
    (ROOT/'work_root/t3_patch_unlocated.json').write_text(json.dumps(failed,ensure_ascii=False,indent=2)+'\n')
    print('Pairs',len(rows),'unique in both layers',len(rows)-len(failed),'need location',len(failed))
    for r in failed:print(r['id'],r['part'],'dip',r['dip_hits'],'corr',r['corr_hits'])

if __name__=='__main__':main()
