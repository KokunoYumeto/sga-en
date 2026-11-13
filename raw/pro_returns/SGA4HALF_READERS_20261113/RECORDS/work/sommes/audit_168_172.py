from audit_helpers import *
decide(673,"The final introductory sentence visibly reads ‘ont été faits ou peuvent être faits’; the connector is ou, so Miller's on is a transcription error.")
decide(674,"The parenthesis in 0.1 visibly prints indice. Restore the consonant order; there is no printed misprint.")
decide(675,"The support in 1.1 has a lowered zero on X. It is the base scheme X_0, also named at the start of the statement, not X minus zero.")
decide(676,"The sentence introducing the limit argument visibly includes ‘à la limite’; restore the omitted article.")
decide(677,"The parenthesis starts ‘V espace vectoriel’; the added un is absent from the scan.")
decide(678,"Equation (1.2.2) ends immediately after Isom(V,F) and continues ‘tel que’. There is no terminal stop in the print; removing the added full stop restores the single sentence.")
decide(679,"The superscript on E_lambda in the character's codomain is visibly an asterisk. Retain this author's unit-group notation in every form.")
decide(680,"The final equivariance equation visibly separates rho(a) and rho(t) with a multiplication point. Restore that printed symbol.")
decide(681,"The scan reads ‘et une factorisation’; the feminine article is clear across the line break.")
decide(682,"The notation paragraph visibly prints objects, with c before t. This is a French spelling error, corrected to objets only in corrected forms; English objects is unaffected.")
decide(683,"The lower central group of diagram (1.6.1) has subscript 1, matching the three other base-extended G_1 terms. Miller's q is a transcription error.")
decide(684,"The second argument of the left side of (1.7.2) is the roman morphism f_0. The scan has no script F in that argument.")
for p,a,b in [(168,r'\chapter{Applications de la formule',r'\chapter{Applications of the Trace Formula'),(169,r'\section*{Notations}',r'\section*{Notation}'),(170,r'\subsection{}\label{VI:1-2}',r'\subsection{}\label{VI:1-2}'),(171,r'Si $X$ est un schéma sur $S$',r'If $X$ is a scheme over $S$'),(172,r'\paragraph{Exemples}',r'\paragraph{Examples}')]: page(p,a,b)
variant(171,'S45-SOL-0682','objects','objets','French spelling: objets has no c; the printed reading is directly visible.',place='1.4, Notation')
summary_fr=r'''\begin{center}\textbf{Sommaire}\end{center}
\begin{tabular}{p{0.86\textwidth}r}
1. Principes & 2\\
2. Dictionnaire & 16\\
3. Sommes à une variable & 22\\
4. Sommes de Gauss et sommes de Jacobi & 29\\
5. Caractères de Hecke & 41\\
6. Les caractères de Hecke définis par les sommes de Jacobi & 46\\
7. Sommes de Kloosterman \var{généralisée}{généralisées}{S45-ASTRA-S-0002} & 52\\
8. Autres applications & 63
\end{tabular}'''
summary_en=r'''\begin{center}\textbf{Contents}\end{center}
\begin{tabular}{p{0.86\textwidth}r}
1. Principles & 2\\
2. Dictionary & 16\\
3. Sums in one variable & 22\\
4. Gauss sums and Jacobi sums & 29\\
5. Hecke characters & 41\\
6. Hecke characters defined by Jacobi sums & 46\\
7. Generalized Kloosterman sums & 52\\
8. Other applications & 63
\end{tabular}'''
own(1,168,'Sommaire','Eight entries with local page numbers 2, 16, 22, 29, 41, 46, 52, 63','Absent',summary_fr,'missing','The lower half of the opening page contains this printed summary. Transcribed in full; English version AI-translated from the scan-verified French.')
append('restorations',{'id':'S45-ASTRA-S-0001','page':'168','position':'before Notations','fr':summary_fr,'en':summary_en,'AI_translated':True})
own(2,168,'Sommaire item 7','généralisée','absent','généralisées','misprint_in_print','The scan visibly has the singular feminine ending -ée. The adjective qualifies the plural Sommes and requires -ées; the diplomatic form retains the printed ending.')
append('variants',{'id':'S45-ASTRA-S-0002','source':'S45-ASTRA-S-0002','page':'168','place':'Sommaire, item 7','printed':'généralisée','corrected':'généralisées','kind':'misprint_in_print','reason':'Agreement with plural Sommes; the scan has -ée.','english_applicable':False})
own(3,172,'Definition 1.7, character codomain',r'E_\lambda^\ast',r'E_\lambda^\times',r'E_\lambda^\ast','symbol','The unit-group codomain visibly uses an asterisk, as on p.170; preserve this printed notation. No mathematical correction is intended.')
edit(172,'S45-ASTRA-S-0003','fr',r'$\chi:G_0(\dF_q)\to E_\lambda^\times$',r'$\chi:G_0(\dF_q)\to E_\lambda^\ast$')
edit(172,'S45-ASTRA-S-0003','en',r'$\chi:G_0(\dF_q)\to E_\lambda^\times$',r'$\chi:G_0(\dF_q)\to E_\lambda^\ast$')
