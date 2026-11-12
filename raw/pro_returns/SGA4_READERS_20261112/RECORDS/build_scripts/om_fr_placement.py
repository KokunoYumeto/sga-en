"""Place individually accepted, undisputed one-model readings in French.

All pairs are explicit transcription decisions. No source or baseline is edited.
"""
from pathlib import Path
import json,re
from fr_core import find_exact,page_span
from review_t3 import locate
from marker_projection import carry_markers
ROOT=Path(__file__).resolve().parents[1]
PAIRS={
'OM-OPUS-0003':[(r"\Hom_{\Hhom({C'}^\circ,D)}(G,u_\ast F){\quoi}.",r"\Hom_{\Hhom({C'}^\circ,D)}(G,u_\ast F){\quoi}).")],
'OM-OPUS-0007':[('pleine fidèlité','pleine fidélité')],
'OM-OPUS-0008':[('induotives quelconques','inductives quelconques')],
'OM-OPUS-0009':[('limites inductives finies sont rerpésentables','limites inductives finies sont représentables')],
'OM-OPUS-0014':[("le cardianl de l'ensemble des flèches","le cardinal de l'ensemble des flèches")],
'OM-OPUS-0028':[(r'{Proposition 6:7}',r'{Proposition 6.7}')],
'OM-OPUS-0031':[(r'F(u(X)\rightarrow',r'F(u(X))\rightarrow'),(r'\prod_{i,j}F(u(X_i\times_X X_j)',r'\prod_{i,j}F(u(X_i\times_X X_j))')],
'OM-OPUS-0032':[('Se déduit immédiatemant','Se déduit immédiatement')],
'OM-OPUS-0036':[('famille génératrice priviligiée','famille génératrice privilégiée')],
'OM-OPUS-0040':[('peuvent se décrirent en termes','peuvent se décrire en termes')],
'OM-OPUS-0042':[(r'réconstituer $X$ à partir de',r'reconstituer $X$ à partir de')],
'OM-OPUS-0050':[('Il admet doncbien un adjoint','Il admet donc bien un adjoint')],
'OM-OPUS-0055':[('où les limmites projectives','où les limites projectives')],
'OM-OPUS-0060':[(r"Désignons par $\Point'E)$ l'ensemble",r"Désignons par $\Point(E)$ l'ensemble")],
'OM-OPUS-0063':[(r'$E$, ((Montrer que dans ce ce cas',r'$E$ (Montrer que dans ce cas')],
'OM-OPUS-0065':[(r"$E'\vee E''=E$. Où le signe",r"$E'\vee E''=E$ (où le signe")],
'OM-OPUS-0069':[('est insomorphe','est isomorphe')],
'OM-OPUS-0073':[("« pré-relation d'équivalence (ou","« pré-relation d'équivalence » (ou")],
'OM-OPUS-0077':[("un homorphisme d'anneaux de", "un homomorphisme d'anneaux de")],
'OM-OPUS-0082':[(r'\emph{Topos localement annelés}; \cf',r'\emph{Topos localement annelés} (\cf')],
'OM-OPUS-0083':[(r'\hyperref[IV.subsubsec4.2.3]{4.2.3}).',r'\hyperref[IV.subsubsec4.2.3]{4.2.3}.')],
'OM-OPUS-0090':[(r'H^q(𝒳 , \Hhom_A(F, G)',r'H^q(𝒳 , \Hhom_A(F, G))'),(r'H^q(\Hom_A (C_∙ (𝒳 ) \otimes_{\ZZ} F, G)',r'H^q(\Hom_A (C_∙ (𝒳 ) \otimes_{\ZZ} F, G))')],
'OM-OPUS-0092':[(r'ℋ^p_{\Phi}(\Eext^q_A(M, N)',r'ℋ^p_{\Phi}(\Eext^q_A(M, N))'),(r'H^p_{\Phi}(X, \Eext^q_A(M, N)',r'H^p_{\Phi}(X, \Eext^q_A(M, N))')],
'OM-OPUS-0093':[(r'un hyper-reoouvrement de type $p$',r'un hyper-recouvrement de type $p$')],
'OM-OPUS-0098':[('duun faisceau',"d'un faisceau")],
'OM-OPUS-0100':[("des sytèmes simpliciaux d'espaces","des systèmes simpliciaux d'espaces")],
'OM-OPUS-0101':[(r'au-dessus de $D$ où que $E$',r'au-dessus de $D$ ou que $E$')],
'OM-OPUS-0110':[(r'([n+1],[\ell]',r'([n+1],[\ell])')],
'OM-OPUS-0115':[(r'et de \hyperref[VI.subsec2.14]{2.14}.',r'et de \hyperref[VI.subsec2.14]{2.14}.)')],
'OM-OPUS-0116':[('noté plus haut pout tout objet','noté plus haut pour tout objet')],
'OM-OPUS-0117':[(r'Soit $E$ un topos, Si $E$ est algébrique',r'Soit $E$ un topos. Si $E$ est algébrique')],
'OM-OPUS-0122':[('Suppsons la catégorie','Supposons la catégorie')],
'OM-OPUS-0123':[("l'objet finalest connexe","l'objet final est connexe")],
'OM-OPUS-0124':[(r'Par suite $E$ se réconstitue',r'Par suite $E$ se reconstitue')],
'OM-OPUS-0125':[(r'$𝒰$-prétopos $C$ se réconstitue',r'$𝒰$-prétopos $C$ se reconstitue')],
'OM-OPUS-0127':[(r'(II 6.2 1))',r'(II 6.2.1))')],
'OM-OPUS-0152':[(r'de valeur $S$ (IV.',r'de valeur $S$ (IV).')],
'OM-OPUS-0154':[(r'localement constructible \hyperref[IX.prop2.4]{2.4} (iv))',r'localement constructible (\hyperref[IX.prop2.4]{2.4} (iv))')],
'OM-OPUS-0156':[('si et suelement si','si et seulement si')],
'OM-OPUS-0157':[(r'(\hyperref[IX.cor2.7.3]{2.7.3},',r'(\hyperref[IX.cor2.7.3]{2.7.3}),')],
'OM-OPUS-0167':[(r'\pi_n(S(\CC)',r'\pi_n(S(\CC))')],
'OM-OPUS-0172':[(r'et $g$ queldonque',r'et $g$ quelconque')],
'OM-OPUS-0173':[(r"H^{i}(\bar{X}'_{\bar{s}'},,\bar{F}')",r"H^{i}(\bar{X}'_{\bar{s}'},\bar{F}')")],
'OM-OPUS-0187':[(r"En vertu de l'aniome $TR$ 3 de",r"En vertu de l'axiome $TR$ 3 de")],
'OM-OPUS-0197':[('pout tout homomorphisme','pour tout homomorphisme')],
'OM-OPUS-0198':[('une fsmille finie','une famille finie')],
'OM-OPUS-0221':[('en un morohisme plat','en un morphisme plat')],
'OM-OPUS-0228':[(r'de $\langle \Ll,,K]$',r'de $\langle \Ll,K]$')],
'OM-OPUS-0238':[(r'\Tr_{Z(m_{2}/S}(K)',r'\Tr_{Z(m_{2})/S}(K)')],
'OM-OPUS-0244':[(r'est le composé » de $\Tr_{w}$',r'est le « composé » de $\Tr_{w}$')],
'OM-OPUS-0247':[(r'on $f^{\bigdot}_{!}=f_{!}$',r'on a $f^{\bigdot}_{!}=f_{!}$')],
'OM-OPUS-0252':[("faisoeau constant d'anneaux","faisceau constant d'anneaux")],
'OM-OPUS-0255':[(r'fonctions rationnellss sur $A$',r'fonctions rationnelles sur $A$')],
'OM-OPUS-0257':[(r'Il suffit de demontrer $(7.1)$',r'Il suffit de démontrer $(7.1)$')],
'OM-SOL-0003':[(r"Soient. $c<c'$ deux cardinaux fortement inaccessibles.",r"Soient $c<c'$ deux cardinaux fortement inaccessibles.")],
'OM-SOL-0007':[(r'Il résulte au ${\rm n^\circ}$ 1',r'Il résulte du ${\rm n^\circ}$ 1')],
'OM-SOL-0008':[(r'un sous-objet (\resp un quotient de',r'un sous-objet (\resp un quotient) de')],
'OM-SOL-0013':[(r'les $𝒰$-limites filtrates dans',r'les $𝒰$-limites filtrantes dans')],
'OM-SOL-0020':[(r'$\gamma$-objets libre engendré',r'$\gamma$-objet libre engendré')],
'OM-SOL-0030':[(r'définie par le foncteur $F:E\rightarrow (\Ens)$',r'défini par le foncteur $F:E\rightarrow (\Ens)$')],
'OM-SOL-0033':[('si et seulement la famille','si et seulement si la famille')],
'OM-SOL-0037':[(r"indexé par les $X'\in \ob C_{/X}$, telle que l'on ait",r"indexé par les $X'\in \ob C_{/X}$, tel que l'on ait")],
'OM-SOL-0046':[('et nous bornerons à signaler que','et nous nous bornerons à signaler que')],
'OM-SOL-0060':[(r'Le foncteur constant sur $I$ de valeur sur un objet $X$ de $C$',r'Le foncteur constant sur $I$ de valeur un objet $X$ de $C$')],
'OM-SOL-0062':[('et nous bornerons ici à partir','et nous nous bornerons ici à partir')],
'OM-SOL-0063':[('donne alors immédiatement','donnent alors immédiatement')],
'OM-SOL-0078':[('une limite projective de foncteurs exacts à gauche est exact à gauche','une limite projective de foncteurs exacts à gauche est exacte à gauche')],
'OM-SOL-0086':[('objet initial, somme de deux objets conoyaux de doubles flèches','objet initial, somme de deux objets, conoyaux de doubles flèches')],
'OM-SOL-0090':[('au fur et mesure','au fur et à mesure')],
'OM-SOL-0112':[(r'les éléments $\prod_j h(\infty, j)$ du deuxième membre',r'les éléments de $\prod_j h(\infty, j)$ du deuxième membre')],
'OM-SOL-0123':[(r'Soient $f:E\rightarrow F$ un foncteur accessible',r'Soit $f:E\rightarrow F$ un foncteur accessible')],
'OM-SOL-0124':[(r'pleine de $E_{\Pi}$ de $E$',r'pleine $E_{\Pi}$ de $E$')],
'OM-SOL-0136':[(r'si a un ordinal limite.',r'si $a$ est un ordinal limite.')],
'OM-SOL-0157':[(r'Soient $C$ un site',r'Soit $C$ un site')],
'OM-SOL-0162':[(r"l'ensemble des sous-objets de $X$ et l'ensemble des objets quotients de $X$ est $𝒰$-petit.",r"l'ensemble des sous-objets de $X$ et l'ensemble des objets quotients de $X$ sont $𝒰$-petits.")],
'OM-SOL-0173':[(r'F(u(X)\rightarrow',r'F(u(X))\rightarrow')],
'OM-SOL-0174':[(r'\prod_{i,j}F(u(X_i\times_X X_j)',r'\prod_{i,j}F(u(X_i\times_X X_j))')],
'OM-SOL-0180':[(r'$F(\epsilon_C(X)\rightarrow\prod_i F(\epsilon_C(X_i))$',r'$F(\epsilon_C(X))\rightarrow\prod_i F(\epsilon_C(X_i))$')],
'OM-SOL-0200':[(r'son image par $u^{\ast}$ est muni des mêmes structures',r'son image par $u^{\ast}$ est munie des mêmes structures')],
'OM-SOL-0236':[(r'est $X$, donc est $𝒰$-petite.',r'est $X$, donc est $𝒰$-petit.')],
'OM-SOL-0240':[('utilisé dans exercice',"utilisé dans l'exercice")],
'OM-SOL-0243':[('catégorie des points de ce topos est équivalent à la catégorie','catégorie des points de ce topos est équivalente à la catégorie')],
'OM-SOL-0251':[('admettant un adjoint à à droite)','admettant un adjoint à droite)')],
'OM-SOL-0252':[(r'prouver que celui-ci redonne $S$.',r'prouver que celui-ci redonne $S$).')],
'OM-SOL-0277':[(r'\paragraph{}\etiquette[9.5.4.8]{IV.par9.5.4.8}',r'\begingroup\renewcommand{\theparagraph}{9.5.8}\paragraph{}\etiquette[9.5.8]{IV.par9.5.4.8}\endgroup')],
'OM-SOL-0285':[('considérons un foncteur recollement','considérons un foncteur de recollement')],
'OM-SOL-0303':[(r'les composantes connexes $X^r$ sont ouvertes',r'les composantes connexes de $X^r$ sont ouvertes')],
'OM-SOL-0336':[(r'\mathop{\mathbf{om}}_A(A_{U}, P)',r'\scrHom_A(A_{U}, P)')],
'OM-SOL-0348':[(r'j_{V!} (P \otimes_{A/V} j^{\ast}_V M$',r'j_{V!} (P \otimes_{A/V} j^{\ast}_V M)$')],
'OM-SOL-0353':[(r'U_{f(g(1)}',r'U_{f(g(1))}')],
'OM-SOL-0359':[(r'H^q(C^{∙} (\Uu, M)',r'H^q(C^{∙} (\Uu, M))')],
'OM-SOL-0373':[(r'H^q(𝒳 , \Hhom_A(F, G)',r'H^q(𝒳 , \Hhom_A(F, G))')],
'OM-SOL-0374':[(r'H^q(\Hom_{\ZZ}^{∙}(C_∙(𝒳)\Hhom_A(F,G))',r'H^q(\Hom_{\ZZ}^{∙}(C_∙(𝒳),\Hhom_A(F,G)))')],
'OM-SOL-0375':[(r'H^q(\Hom_A (C_∙ (𝒳 ) \otimes_{\ZZ} F, G)',r'H^q(\Hom_A (C_∙ (𝒳 ) \otimes_{\ZZ} F, G))')],
'OM-SOL-0378':[(r'\Ext^{0}_{A, Z}(X;M, N) = H^{0}_Z (X, \Hhom_A(M, N)',r'\Ext^{0}_{A, Z}(X;M, N) = H^{0}_Z (X, \Hhom_A(M, N))')],
'OM-SOL-0379':[(r'H^{0} (X, \Hhom_{A, Z}(M, N)',r'H^{0} (X, \Hhom_{A, Z}(M, N))')],
'OM-SOL-0382':[(r'La famille de $\Phi_p$ des fermés',r'La famille $\Phi_p$ des fermés')],
'OM-SOL-0385':[(r'$𝚫(E)$ de catégorie des préfaisceaux',r'$𝚫(E)$ la catégorie des préfaisceaux')],
'OM-SOL-0386':[(r'$i_{n!}i^{\ast}_n$) (\resp $i_{n\ast}i^\ast_n$)',r'$i_{n!}i^{\ast}_n$ (\resp $i_{n\ast}i^\ast_n$)')],
'OM-SOL-0393':[(r'$C$ (à valeur dans la catégorie des ensembles semi-simpliciaux constant de valeur',r'$C$ (à valeur dans la catégorie des ensembles semi-simpliciaux) constant de valeur')],
'OM-SOL-0437':[('est univers tel que','est un univers tel que')],
'OM-SOL-0441':[(r'lecteur pourra se reporter à (\cite{SGA4-05bis:4} - (1.17)).',r'lecteur pourra se reporter à (\cite{SGA4-05bis:4} - (1.17))).')],
'OM-SOL-0487':[(r'quasi-compacte (\resp quasi-séparé)',r'quasi-compacte (\resp quasi-séparée)')],
'OM-SOL-0488':[(r'est quasi-compacte (\resp quasi-séparé)',r'est quasi-compacte (\resp quasi-séparée)')],
'OM-SOL-0497':[(r'p_1(\bar{k}):p_2(\bar{k}):',r'p_1(\bar{k}),p_2(\bar{k}):')],
'OM-SOL-0498':[(r'et de \hyperref[VI.subsec2.14]{2.14}.',r'et de \hyperref[VI.subsec2.14]{2.14}.)')],
'OM-SOL-0500':[(r'avec $H$ \emph{fini}.)',r'avec $H$ \emph{fini}.')],
'OM-SOL-0506':[(r'noethérien (\ie tout ouvert de $X$ est quasi-compact), \ie',r'noethérien (\ie tout ouvert de $X$ est quasi-compact, \ie')],
'OM-SOL-0524':[(r"$E''$ l'et aussi",r"$E''$ l'est aussi")],
'OM-SOL-0526':[('se relèvent chacun en un morphisme','se relèvent chacune en un morphisme')],
'OM-SOL-0536':[(r'\item[e)] Il reste seulement à prouver les implications',r'\item Il reste seulement à prouver les implications')],
'OM-SOL-0541':[(r"foncteurs quelconque $f : E'_{\coh} \to P$",r"foncteurs quelconques $f : E'_{\coh} \to P$")],
'OM-SOL-0543':[(r'finies sont représentables, que $f$ est exact à gauche',r'finies sont représentables, $f$ est exact à gauche')],
'OM-SOL-0550':[(r'Un objet de $Y$ au-dessus de $\eta$',r'Un objet $Y$ au-dessus de $\eta$')],
'OM-SOL-0582':[(r"au foncteur $i \to \sigma(i)$ $\Hom(I^{\circ}, D^{\sim})$ l'objet",r"au foncteur $i \to \sigma(i)$ de $\Hom(I^{\circ}, D^{\sim})$ l'objet")],
'OM-SOL-0585':[(r'\Mmorsite_{\Cart/I}(D\times I, (\underrightarrow{F})\times I',r'\Mmorsite_{\Cart/I}(D\times I, (\underrightarrow{F})\times I)')],
'OM-SOL-0594':[(r'\pi(Y)_{\alpha \beta \in \mathop{\coprod}_A B_{\alpha}}',r'\pi(Y))_{\alpha \beta \in \mathop{\coprod}_A B_{\alpha}}')],
'OM-SOL-0605':[(r'\Hom(\varinjlim_{I^{\circ}} \mu_{i\ast} (M_i), N))',r'\Hom(\varinjlim_{I^{\circ}} \mu_i^{\ast} (M_i), N)')],
'OM-SOL-0611':[(r"(i \mapsto K_i = \coker (\mu_{i\ast} (N') \to \mu_{i\ast} (N))",r"(i \mapsto K_i = \coker (\mu_{i\ast} (N') \to \mu_{i\ast} (N)))")],
'OM-SOL-0612':[(r'\underleftarrow{m}_{\ast} (Q^{\ast} (j \mapsto M_j)',r'\underleftarrow{m}_{\ast} (Q^{\ast} (j \mapsto M_j))')],
'OM-SOL-0613':[(r'\mu^{\ast}_j R^n m_{j\ast} \mu_{j\ast} (N))',r'\mu^{\ast}_j R^n m_{j\ast} \mu_{j\ast} (N)')],
'OM-SOL-0614':[(r'Q^{\ast} (f : j \to i) \mapsto f^{\ast}(M_i))',r'Q^{\ast} ((f : j \to i) \mapsto f^{\ast}(M_i))')],
'OM-SOL-0617':[(r'Soient $i$ un objet $I$',r'Soient $i$ un objet de $I$')],
'OM-SOL-0631':[('«\u00a0Dix exposés sur la topologie des schémas, North Holland Pub.', '«\u00a0Dix exposés sur la topologie des schémas\u00a0», North Holland Pub.')],
'OM-SOL-0632':[(r'des faisceaux de coefficients $F$ tel que',r'des faisceaux de coefficients $F$ tels que')],
'OM-SOL-0639':[(r'(\ie $(3)$) un foncteur',r'(\ie $(3)$ un foncteur')],
'OM-SOL-0643':[('préfaisceaux, On prouve de même :','préfaisceaux). On prouve de même :')],
'OM-SOL-0646':[(r"ou $A'' \simeq A [t_1, \ldots t_n]$",r"où $A'' \simeq A [t_1, \ldots t_n]$")],
'OM-SOL-0667':[(r'X_{y} \otimes_{k(y),} k(\bar{y})',r'X_{y} \otimes_{k(y)} k(\bar{y})')],
'OM-SOL-0681':[(r"$F'$, $G'$, $u'$ provient d'un morphisme",r"$F'$, $G'$, provient d'un morphisme")],
'OM-SOL-0682':[(r"Donc en vertu de \hyperref[VIII.lem9.3]{9.3}. $\Gamma'$ provient",r"Donc en vertu de \hyperref[VIII.lem9.3]{9.3}, $\Gamma'$ provient")],
'OM-SOL-0698':[(r"que un des $X_{N'}$",r"qu'un des $X_{N'}$")],
'OM-SOL-0703':[(r'nous ramène au cas où $Y$ est réduit',r'nous ramènent au cas où $Y$ est réduit')],
'OM-SOL-0709':[(r'Soient $X$ un schéma noethérien',r'Soit $X$ un schéma noethérien')],
'OM-SOL-0731':[(r'$(i=1,\ldots, n-r); j=1,\ldots,n)$',r'$(i=1,\ldots, n-r; j=1,\ldots,n)$')],
'OM-SOL-0741':[(r"$f_{\ast}$, $f'_{\ast}$, $f''_{\ast}$ remplacé par",r"$f_{\ast}$, $f'_{\ast}$, $f''_{\ast}$ remplacés par")],
'OM-SOL-0742':[(r"0 \ar[r]& (R^{1}f'_{\ast})e'_{\ast}g''^{\ast}F)",r"0 \ar[r]& (R^{1}f'_{\ast})e'_{\ast}g''^{\ast}F")],
'OM-SOL-0744':[(r'la classe $H^1(X,F^{\alpha})$ correspondant à $\beta$',r'la classe de $H^1(X,F^{\alpha})$ correspondant à $\beta$')],
'OM-SOL-0748':[(r'H^{p}(G,H^{q}(\bar{X},\bar{F})',r'H^{p}(G,H^{q}(\bar{X},\bar{F}))')],
'OM-SOL-0749':[(r'H^{p}(G,H^q,\bar{X}_0,\bar{F}_0 ))',r'H^{p}(G,H^q(\bar{X}_0,\bar{F}_0 ))')],
'OM-SOL-0760':[(r"l'image de $\eta$ de $\xi$",r"l'image $\eta$ de $\xi$")],
'OM-SOL-0765':[(r'H^{1}(Y,p_{Y^{\ast}}(\bar{h}^{\ast}(\bar{F}))',r'H^{1}(Y,p_{Y^{\ast}}(\bar{h}^{\ast}(\bar{F})))')],
'OM-SOL-0766':[(r'H^1(Y,h^{\ast}(p_{\ast}(\bar{F}))',r'H^1(Y,h^{\ast}(p_{\ast}(\bar{F})))')],
'OM-SOL-0767':[(r'H^{\circ}(Y,h^{\ast}(R^1(p_{\ast}(\bar{F}))',r'H^{\circ}(Y,h^{\ast}(R^1(p_{\ast}(\bar{F}))))')],
'OM-SOL-0774':[(r"faisceau d'ensembles $F$ (\resp tout faisceau de",r"faisceau d'ensembles (\resp tout faisceau de")],
'OM-SOL-0775':[(r"telles que l'image $\xi$ dans",r"telles que l'image de $\xi$ dans")],
'OM-SOL-0784':[(r'H^{i}(Y,h^{\ast}(\RR^jp_{\ast}(\bar{F}))',r'H^{i}(Y,h^{\ast}(\RR^jp_{\ast}(\bar{F})))')],
'OM-SOL-0786':[(r'dans \hyperref[XII.cor5.5]{5.5} sera étudié dans $XV$.',r'dans \hyperref[XII.cor5.5]{5.5}) sera étudié dans $XV$.')],
'OM-SOL-0794':[(r"ensemble des quotients de $E'$ plat au-dessus de $S'$",r"ensemble des quotients de $E'$ plats au-dessus de $S'$")],
'OM-SOL-0799':[(r'est représentée par un fibré vectoriel $Z$',r'est représenté par un fibré vectoriel $Z$')],
'OM-SOL-0811':[(r'(\hyperrefext[IX][IX.prop2.6]{2.6}). Puisque $i$ est',r'(\hyperrefext[IX][IX.prop2.6]{2.6})). Puisque $i$ est')],
'OM-SOL-0823':[(r'au cas $A$ est une',r'au cas où $A$ est une')],
'OM-SOL-0870':[(r"ouvertes et fermées des $Y'$",r"ouvertes et fermées de $Y'$")],
'OM-SOL-0899':[('sont munies de','sont munis de')],
'OM-SOL-0935':[('à homotopie près} à les mêmes objets','à homotopie près} a les mêmes objets')],
'OM-SOL-0989':[(r'$D^{-}(\Ss)$ (\resp $D^{+}(\Ss)$ est triangulée sur',r'$D^{-}(\Ss)$ (\resp $D^{+}(\Ss)$) est triangulée sur')],
'OM-SOL-1032':[(r'$K_s$ les images réciproques',r"$K_s$ l'image réciproque")],
'OM-SOL-1035':[(r'Si $L$ borné inférieurement',r'Si $L$ est borné inférieurement')],
'OM-SOL-1100':[(r'Soient $S$ un schéma cohérent',r'Soit $S$ un schéma cohérent')],
'OM-SOL-1108':[('montrent que pour les flèches de Künneth soient un isomorphisme','montrent que pour que les flèches de Künneth soient des isomorphismes')],
'OM-SOL-1135':[(r'formée des décompositions $(V_{i})_{i\in I}$ telle que',r'formée des décompositions $(V_{i})_{i\in I}$ telles que')],
'OM-SOL-1136':[(r'en vertu \eqhyperref[XVII.eq6.2.7.2]{6.2.7.2}',r'en vertu de \eqhyperref[XVII.eq6.2.7.2]{6.2.7.2}')],
'OM-SOL-1267':[(r"l'image directe $u_{\ast}$ est un $2$-foncteur.",r"L'image directe $u_{\ast}$ est un $2$-foncteur.")],
'OM-SOL-1300':[("d'anneau","d'anneaux")],
'OM-SOL-1309':[(r"\Hom(K,Rg'_{\ast} R\Hhom_{\Bb}(f'^{\ast}M,Rf'^{!}L)",r"\Hom(K,Rg'_{\ast} R\Hhom_{\Bb}(f'^{\ast}M,Rf'^{!}L))")],
'OM-SOL-1310':[(r"\Hom(g'^{\ast}K,R\Hhom_{\Bb}(f'^{\ast} M, Rf'^{!}L)",r"\Hom(g'^{\ast}K,R\Hhom_{\Bb}(f'^{\ast} M, Rf'^{!}L))")],
'OM-SOL-1319':[(r'h^{\ast}(g^{\ast}L(d_2)[2d_2])(d_1)[2d_1])',r'h^{\ast}(g^{\ast}L(d_2)[2d_2])(d_1)[2d_1]')],
'OM-SOL-1332':[(r"$\ZZ/n$ (par l'un ou l'autre des isomorphismes $\Psi(Z,Y_{i},X)$, et",r"$\ZZ/n$ (par l'un ou l'autre des isomorphismes $\Psi(Z,Y_{i},X)$), et")],
}
INTERMEDIATE={
('OM-OPUS-0063',1):r'$E$, ((Montrer que dans ce cas',
('OM-SOL-0374',1):r'H^q(\Hom_{\ZZ}^{∙}(C_∙ (𝒳 ), \Hhom_A(F, G))',
('OM-SOL-0742',1):r"0 \ar[r]& ((R^{1}f'_{\ast})e'_{\ast}g''^{\ast}F)",
}
DUPLICATES={'OM-SOL-0173':('OM-OPUS-0031',1),'OM-SOL-0174':('OM-OPUS-0031',2),
 'OM-SOL-0373':('OM-OPUS-0090',1),'OM-SOL-0375':('OM-OPUS-0090',2),'OM-SOL-0498':('OM-OPUS-0115',1)}
PLACEMENT_NOTES={
'OM-SOL-0277':'The visible heading is generated by the paragraph counter. A local theparagraph override corrects its display to 9.5.8; the optional reference text is also corrected, while the existing IV.par9.5.4.8 link anchor and counter increment are retained.',
'OM-SOL-0336':r'The source defines \scrHom as \DeclareMathOperator{\scrHom}{\mathbf{Hom}}. The diplomatic fragment removes H while retaining that bold operator typography.',
'OM-SOL-0536':r'This is the sixth outer \item in VI 4.12, after Explicitons, Or supposons, Notons, Explicitons, La condition. The corrected automatic label is f); the diplomatic override retains the reported repeated e).',
'OM-SOL-0742':'The supplied TeX has an added outer opening parenthesis. The complete diagram cell is anchored so that the diplomatic text retains the reported extra close and the corrected text deletes it, without leaving an added unmatched opener.',
'OM-SOL-0765':r'Only the missing closing delimiter is repaired. The source spelling p_{Y^{\ast}} is retained in both layers; the different p_{Y_{\ast}} token in the reported reading is not introduced.',
'OM-OPUS-0154':'The accepted correction supplies the missing opening parenthesis around the reference. An intermediate corrected source omitted the final close instead; the full reference context is replaced.',
'OM-SOL-0682':'The accepted correction changes the sentence-breaking period to a comma. An intermediate corrected source had omitted that period; the full reference context is replaced.',
}

PAIRS.update({
'OM-OPUS-0007':[(r'la pleine fidèlité de $\Ind(f)$ implique',r'la pleine fidélité de $\Ind(f)$ implique'),(r'utilisant la pleine fidèlité de $\Ind(f)$',r'utilisant la pleine fidélité de $\Ind(f)$')],
'OM-OPUS-0032':[('Se déduit immédiatemant de 1)','Se déduit immédiatement de 1)'),('Se déduit immédiatemant de la description','Se déduit immédiatement de la description')],
'OM-OPUS-0069':[(r'$\Phi(W)$ est insomorphe',r'$\Phi(W)$ est isomorphe')],
'OM-OPUS-0077':[(r"un homorphisme d'anneaux de $\Gamma(B)^{\circ}$",r"un homomorphisme d'anneaux de $\Gamma(B)^{\circ}$")],
'OM-OPUS-0093':[(r'un hyper-reoouvrement de type $p$ de $X$',r'un hyper-recouvrement de type $p$ de $X$')],
'OM-OPUS-0156':[(r'$F$ est localement constant si et suelement si',r'$F$ est localement constant si et seulement si')],
'OM-OPUS-0238':[(r'K_{2}=\Tr_{Z(m_{2}/S}(K){\quoi}.\tag{1.5.12.1}',r'K_{2}=\Tr_{Z(m_{2})/S}(K){\quoi}.\tag{1.5.12.1}')],
'OM-SOL-0353':[(r'\to U_{f(g(1)}',r'\to U_{f(g(1))}')],
})
INTERMEDIATE.update({
('OM-OPUS-0154',1):r'localement constructible \hyperref[IX.prop2.4]{2.4} (iv)',
('OM-SOL-0682',1):r"Donc en vertu de \hyperref[VIII.lem9.3]{9.3} $\Gamma'$ provient",
})

def unique_spans(hits):
    # Whitespace changes such as doncbien/donc bien share a search key but
    # still have only one physical source occurrence.
    spans={}
    for a,b,kind in hits:
        if (a,b) in spans:spans[a,b]='both whitespace readings share this span'
        else:spans[a,b]=kind
    return [(a,b,kind) for (a,b),kind in spans.items()]

def main():
    data=json.loads((ROOT/'work_fr/corrected_layers.json').read_text())
    scope=json.loads((ROOT/'work_fr/om_unplaced_scope.json').read_text())
    records={r['id']:r for r in json.loads((ROOT/'output/records/one_model_edits.json').read_text())}
    assert set(scope)==set(PAIRS),(set(scope)-set(PAIRS),set(PAIRS)-set(scope))
    rows=[]
    for ident in scope:
        rec=records[ident];f=rec['file'];page=rec['page'];assert not rec['on_disputed_page']
        for j,(printed,corrected) in enumerate(PAIRS[ident],1):
            row={'id':ident,'part':j,'file':f,'page':page,'expose':rec['expose'],'printed':printed,'corrected':corrected,'source':rec['source'],
                 'reason':rec['reason'],'place':rec['place']}
            if ident in DUPLICATES:row['represented_by']={'id':DUPLICATES[ident][0],'part':DUPLICATES[ident][1]}
            if ident in PLACEMENT_NOTES:row['placement_note']=PLACEMENT_NOTES[ident]
            for layer,target in [('dip',printed),('corr',corrected)]:
                text=data[layer][f];hits=locate(text,printed,corrected,page)
                if not hits and (ident,j) in INTERMEDIATE:
                    hits=[(a,b,'source editorial reading') for a,b in find_exact(text,INTERMEDIATE[ident,j],page)]
                if not hits:hits=locate(text,printed,corrected,None)
                hits=unique_spans(hits)
                row[layer+'_hits']=len(hits)
                if len(hits)==1:
                    a,b,kind=hits[0];actual=text[a:b];replacement=carry_markers(actual,target)
                    row[layer]={'old':actual,'new':replacement,'at':a,'state':kind,'context_before':text[max(0,a-90):a],'context_after':text[b:b+90]}
                    data[layer][f]=text[:a]+replacement+text[b:]
                else:row[layer]={'status':'needs-location-review'}
            rows.append(row)
    out=ROOT/'output/shared/ONE_MODEL_FR_PATCHES.json';out.write_text(json.dumps(rows,ensure_ascii=False,indent=2)+'\n')
    failed=[r for r in rows if r['dip_hits']!=1 or r['corr_hits']!=1]
    (ROOT/'work_fr/om_fr_unlocated.json').write_text(json.dumps(failed,ensure_ascii=False,indent=2)+'\n')
    print('Records',len(PAIRS),'Pairs',len(rows),'Unique both',len(rows)-len(failed),'Needs location',len(failed))
    for r in failed:print(r['id'],r['part'],r['dip_hits'],r['corr_hits'])

if __name__=='__main__':main()
