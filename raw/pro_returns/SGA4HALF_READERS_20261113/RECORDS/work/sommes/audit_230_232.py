from audit_helpers import *
reasons={976:'The scan says Ce n’est toutefois pas toujours le cas, not par.',977:'The cohomology of G/B is printed invariante par spécialisation. Restore both the agreement and the preposition.',978:'The group acting on a maximal torus is printed groupe de Weil. The reflection group is the Weyl group, so correct the proper name in the mathematical reading.',979:'The Bourbaki reference visibly specifies Lie VIII §5 Rmq 2, not §2.',980:'The scan says le nombre de points rationnels, with masculine article.'}
for n,reason in reasons.items():decide(n,reason)
page(230,r'\section{Autres applications}',r'\section{Other applications}')
page(231,'La même formule vaut pour les groupes de Ree','The same formula applies to the Ree')
page(232,r'\section*{Bibliographie}',r'\section*{Bibliography}','Entire nine-entry bibliography directly read, including an enlarged crop of entries 6–9; absent as a local section from both components and restored in full.')
variant(230,'S45-SOL-0978','groupe de Weil $W$','groupe de Weyl $W$','The group acting on the maximal torus is the Weyl group.',en_old='Weil group $W$',en_new='Weyl group $W$',place='8.2')
id=own(46,230,'8.1, Lusztig article title','Coxeter orbits and eigenspaces of Frobenius (Inv. Math., à paraître)',r'\cite{lu76}','Restore the printed article title and publication status.','omission','The source names the article and its forthcoming status explicitly.')
edit(230,id,'fr',r'\cite{lu76}',r'``Coxeter orbits and eigenspaces of Frobenius (Inv.~Math., à paraître)'' \cite{lu76}')
edit(230,id,'en',r'\cite{lu76}',r'``Coxeter orbits and eigenspaces of Frobenius (Inv.~Math., forthcoming)'' \cite{lu76}')
id=own(47,230,'8.2, Bourbaki reference','Bourbaki, Lie VIII §5 Rmq 2',r'\cite[VIII \S 2 Rem.2]{bo05}','Restore the explicit bibliographic name and series.','omission','The scan includes Bourbaki, Lie in addition to the section information; 0979 handles the section numeral.')
edit(230,id,'fr',r'\cite[VIII \S 5 Rem.2]{bo05}',r'Bourbaki, Lie VIII \S 5 Rmq~2 \cite[VIII \S 5 Rem.2]{bo05}')
edit(230,id,'en',r'\cite[VIII \S 5 Rem.2]{bo05}',r'Bourbaki, Lie VIII \S 5 Remark~2 \cite[VIII \S 5 Rem.2]{bo05}')
id=own(48,232,'Complete local bibliography','Bibliographie; entries [1]–[9]','Omitted from component; several references updated in global bibliography','Restore all nine entries as printed, retaining preprint descriptions.','omission','The entire printed bibliography page is content and is not replaced by a modern consolidated list.')
fr=r'''\section*{Bibliographie}
\begin{enumerate}[{[}1{]}]
\item L.~Carlitz -- A note on exponential sums, Pac.~J.~Math.~\textbf{30} (1969), p.~35--37. MR~\textbf{39}~6839.
\item P.~Deligne -- Les constantes des équations fonctionnelles des fonctions $L$.
Proc.~Antwerpen conf.~Vol.~2, p.~501--597, Lecture Notes~349 (Springer Verlag).
\item P.~Deligne and G.~Lusztig -- Representations of reductive groups over finite fields,
Ann.~of Math.~\textbf{103}, 1 (1976), p.~103--161.
\item D.~Kazhdan -- Proof of Springer's Hypothesis (preprint Harvard).
\item J.P.~Serre -- Abelian $\ell$-adic representations and elliptic curves, Benjamin (1968).
\item T.A.~Springer -- Trigonometrical sums, Green functions and representations of
\var{Weil}{Weyl}{S45-ASTRA-S-0049} groups, (Preprint Utrecht).
\item A.~Weil -- Basic number theory, Springer Verlag.
\item A.~Weil -- Jacobi sums as ``gr\"ossencharaktere'', Trans.~AMS~\textbf{73} (1952), p.~487--495.
\item A.~Weil -- Sommes de Jacobi et caractères de Hecke.
\end{enumerate}
'''
en=fr.replace('Bibliographie','Bibliography')
append('restorations',{'page':'232','source':id,'place':'End of component after 8.3','fr':fr,'en':en,'reason':'The original bibliographic titles and publication descriptions are retained in both languages; only the heading is translated.'})
own(49,232,'Bibliography [6], group name','Weil groups','Entire entry omitted','Weyl groups','misprint_in_print','The cited Springer work concerns Weyl groups; the supplied consolidated bibliography sp76 also identifies that proper name.')
append('variants',{'id':'S45-ASTRA-S-0049','source':'S45-ASTRA-S-0049','page':'232','place':'Bibliography [6]','printed':'Weil','corrected':'Weyl','reason':'Correct the proper name of the reflection groups.','kind':'misprint_in_print','english_applicable':True,'en_printed':'Weil','en_corrected':'Weyl','embedded_in_restoration':True})
