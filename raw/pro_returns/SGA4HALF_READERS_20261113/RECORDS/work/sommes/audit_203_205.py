from audit_helpers import *
reasons={835:'The first implication in the proof visibly goes from (i) to (iii), as its construction of a descended sheaf also shows.',836:'The printed phrase is comme un caractère, with the masculine article.',837:'The full paragraph between (4.14.1) and the concluding sentence is present in the scan, including (4.14.2). Miller omits it entirely; restore every sentence and the complete display, with its independent printed errors preserved diplomatically.',838:'The restored paragraph visibly says copes. It is a misspelling of copies.',839:'The coordinate tuple is printed as an element of k^{* N+1}, but each coordinate belongs to F_q^* because k is the product of N+1 copies of F_q. Correct the coordinate field.',840:'The upper limit in the trace-zero condition is printed as lowercase n. The coordinates are indexed from 1 to N, so the bound is N.',841:'The final factor in (4.14.2) visibly has lowercase n in both chi_n and x_n, although the summation uses N coordinates. Correct both indices to N.',842:'The phrase after (4.15.1) visibly says plus souvent écrit sous la forme; restore souvent.',843:'The first sum after Dès lors lacks the restriction tr(x)=0 in print. The preceding evaluation is q times the trace-zero indicator minus 1, so that restriction is mathematically required.',844:'The source says Le second terme, not La second terme.',845:'The coefficient sheaf in (iii) visibly uses a product dot between the multiplicative and additive characters, not a comma.',846:'The proposition visibly reads caractères non tous triviaux; the extra r is a transcription error.',847:'Both Kummer sheaves in the proposition visibly have subscript m, whereas the characters are characters of mu_n and the subsequent formula uses K_n. Correct both indices to n.',848:'The extension paragraph visibly has V_0 with subscript zero.',849:'The print uses capital V_0 in T_0 V_0; the composition is with the blow-up morphism v_0. Correct the letter case.',850:'The phrase after the semicolon visibly has pi^{-1}(Q_0) without a bar. The domain is the blown-up line bundle, so the projection is bar pi.',851:'The final paragraph similarly defines a full line using pi^{-1}(x), but pi gives a punctured line. The full line is the fibre of bar pi.',852:'The source has est envoyé, without final e. The subject la droite is feminine; correct the participle.'}
for n,reason in reasons.items():decide(n,reason)
page(203,'\\[\n  \\tau\\left(\\chi\\circ N_', '\\[\n  \\tau\\left(\\chi\\circ N_')
page(204,r'\begin{proposition_}\label{VI:4-15}',r'\begin{proposition_}\label{VI:4-15}')
page(205,"L'assertion (ii) résulte de (i)",'Assertion (ii) follows from (i)')
fr=r'''Le cas le plus souvent considéré est celui où $k$ est la somme de $N+1$
\var{copes}{copies}{S45-SOL-0838} de $\dF_q$; $\chi$ correspond alors à $(N+1)$ caractères
$\chi_0,\ldots,\chi_N$ non tous triviaux de $\dF_q^\ast$, de produit égal à $1$.
Dans ce cas, une section du quotient $k^\ast/\dF_q^\ast$ de $k^\ast$
est l'ensemble des $(x_0,\ldots,x_N)\in\var{(k^\ast)^{N+1}}{(\dF_q^\ast)^{N+1}}{S45-SOL-0839}$ avec $x_0=1$;
pour un tel $x$, la condition $\tr(x)=0$ s'écrit $\sum_{i=1}^{\var{n}{N}{S45-SOL-0840}}x_i=-1$.
La somme de Jacobi s'écrit donc
\begin{equation*}\tag{4.14.2}\label{VI:eq:4-14-2}
 J(\chi)=(-1)^{N-1}\sum_{\substack{x_1,\ldots,x_N\in\dF_q^\ast\\\sum x_i=-1}}
 \chi_1^{-1}(x_1)\cdots\var{\chi_n^{-1}(x_n)}{\chi_N^{-1}(x_N)}{S45-SOL-0841} \text{.}
\end{equation*}

'''
en=r'''The most frequently considered case is that in which $k$ is the sum of $N+1$
copies of $\dF_q$; $\chi$ then corresponds to $(N+1)$ characters
$\chi_0,\ldots,\chi_N$ of $\dF_q^\ast$, not all trivial, whose product is $1$.
In this case, a section of the quotient $k^\ast/\dF_q^\ast$ of $k^\ast$
is the set of $(x_0,\ldots,x_N)\in\var{(k^\ast)^{N+1}}{(\dF_q^\ast)^{N+1}}{S45-SOL-0839}$ with $x_0=1$;
for such an $x$, the condition $\tr(x)=0$ becomes $\sum_{i=1}^{\var{n}{N}{S45-SOL-0840}}x_i=-1$.
The Jacobi sum is therefore
\begin{equation*}\tag{4.14.2}\label{VI:eq:4-14-2}
 J(\chi)=(-1)^{N-1}\sum_{\substack{x_1,\ldots,x_N\in\dF_q^\ast\\\sum x_i=-1}}
 \chi_1^{-1}(x_1)\cdots\var{\chi_n^{-1}(x_n)}{\chi_N^{-1}(x_N)}{S45-SOL-0841} \text{.}
\end{equation*}

'''
append('restorations',{'page':'203','source':'S45-SOL-0837','place':'Before On a entre sommes de Gauss','fr':fr,'en':en,'reason':'Complete directly scanned omitted paragraph and equation; English is AI translation of the restored French.'})
for n,old,new,eo,enew in [(838,'copes','copies',None,None),(839,r'(k^\ast)^{N+1}',r'(\dF_q^\ast)^{N+1}',r'(k^\ast)^{N+1}',r'(\dF_q^\ast)^{N+1}'),(840,'n','N','n','N'),(841,r'\chi_n^{-1}(x_n)',r'\chi_N^{-1}(x_N)',r'\chi_n^{-1}(x_n)',r'\chi_N^{-1}(x_N)')]:
 append('variants',{'id':f'S45-SOL-{n:04}','source':f'S45-SOL-{n:04}','page':'203','place':'Restored 4.14 paragraph and (4.14.2)','printed':old,'corrected':new,'reason':reasons[n],'kind':'misprint_in_print','english_applicable':eo is not None,'en_printed':eo,'en_corrected':enew,'embedded_in_restoration':True})
variant(204,'S45-SOL-0843',r'q\sum_{x\in k^\ast/\dF_q^\ast} \chi(x)^{-1}',r'q\sum_{\substack{x\in k^\ast/\dF_q^\ast\\\tr(x)=0}} \chi(x)^{-1}','The first term comes from the trace-zero indicator.',en_old=r'q\sum_{x\in k^\ast/\dF_q^\ast} \chi(x)^{-1}',en_new=r'q\sum_{\substack{x\in k^\ast/\dF_q^\ast\\\tr(x)=0}} \chi(x)^{-1}',place='Proof of 4.15, after Dès lors')
variant(205,'S45-SOL-0847',r'\sK_m((\chi_i)_{i\in I})',r'\sK_n((\chi_i)_{i\in I})','The Kummer exponent of the given characters is n.',en_old=r'\sK_m((\chi_i)_{i\in I})',en_new=r'\sK_n((\chi_i)_{i\in I})',place='Proposition 4.17, both occurrences')
variant(205,'S45-SOL-0849',r'$T_0 V_0$ s’annule',r'$T_0 v_0$ s’annule','Composition with the blow-up morphism v_0.',en_old=r'$T_0 V_0$ vanishes',en_new=r'$T_0 v_0$ vanishes',place='After (4.17.3)')
variant(205,'S45-SOL-0850',r'sur $\pi^{-1}(Q_0)$',r'sur $\bar\pi^{-1}(Q_0)$','Use the projection of the full line bundle.',en_old=r'on $\pi^{-1}(Q_0)$',en_new=r'on $\bar\pi^{-1}(Q_0)$',place='After (4.17.3)')
variant(205,'S45-SOL-0851',r'$D=\pi^{-1}(x)$',r'$D=\bar\pi^{-1}(x)$','The full line is the fibre of bar pi.',en_old=r'$D=\pi^{-1}(x)$',en_new=r'$D=\bar\pi^{-1}(x)$',place='Final paragraph')
variant(205,'S45-SOL-0852','est envoyé','est envoyée','Agreement with la droite.',place='Final paragraph')
for n,p in [(23,203),(24,204)]:
 own(n,p,'Unit-group notation',r'^\ast',r'^\times',r'^\ast','symbol','The corresponding unit groups carry printed asterisk superscripts.')
 append('notation_units',{'page':str(p),'source':f'S45-ASTRA-S-{n:04}','replace':r'^\times','with':r'^\ast'})
