from pathlib import Path
import json,re
P=Path(__file__).resolve().parent
changes=[]
def add(id,page,old,new,**kw):changes.append(dict(id=id,page=page,old=old,new=new,**kw))
def sol(n,page,old,new,**kw):add(f'S45-SOL-{n:04}',page,old,new,**kw)
def own(n,page,old,new,**kw):add(f'S45-ASTRA-R-{n:04}',page,old,new,**kw)

# All total-degree bullets in this component were individually compared with
# the scan. The fixed degree in3.8 is already i in the English base.
add('S45-SOL-0530',129,r'\bullet','*',all=True,sources=['S45-SOL-0530','S45-ASTRA-R-0027','S45-ASTRA-R-0028','S45-ASTRA-R-0029','S45-ASTRA-R-0030','S45-ASTRA-R-0032','S45-ASTRA-R-0036','S45-ASTRA-R-0037','S45-ASTRA-R-0038'],reason='Each occurrence belongs to a directly inspected total-cohomology or resolution degree, recorded page by page in the cited findings.')
sol(534,131,r'of $\delta$-functors',r'of $\partial$-functors')
sol(535,131,r'The definition of $\h^*(X,\sF)$',r'\marginpar{!}The definition of $\h^*(X,\sF)$')
sol(536,131,r'The $\delta$-functor structure',r'The $\partial$-functor structure')
sol(537,132,r'Let $j:U\hookrightarrow X$. If $\sF$',r'\marginpar{!}Let $j:U\hookrightarrow X$. If $\sF$')
sol(542,134,'For a more general theory, one can no longer interpret bilinear maps','For a more general theory, it is no longer tenable to interpret bilinear maps')
sol(545,135,r'\h^n(U,\sK)\otimes',r'\h_Y^n(U,\sK)\otimes')
sol(547,135,r'We identify $\eR\Gamma_Y$ with',r'We identify $\eR\Gamma_Y(U,\sK)$ with')
sol(550,137,r"v'\otimes v\to v'(v)",r"v'\otimes v\mapsto v'(v)")
sol(553,138,r'\partial:\h^i(X\setminus D,\dG_m)\to \h_D^i(X,\dG_m)',r'\partial:\h^i(X\setminus D,\dG_m)\to \h_D^{i+1}(X,\dG_m)')
sol(554,138,r'\tag{2.1.1}',r'\tag{2.1.1.1}')
sol(562,139,r'(\hyperref[I]{Étale cohomology}, \ref{I:5-3-4})',r'(\hyperref[I]{Arcata}, V \ref{I:5-3-4})')
sol(565,139,r'\Ext^i(A/\fa,A)',r'\ext^i(A/\fa,A)')
sol(568,141,r'If $\eR^p i^! \dZ/n = 0$',r'If $\eR^p k^! \dZ/n = 0$')
sol(569,141,r'If $\eR^p i^!\dZ/n=0$ for $p\leqslant 2 c+1$',r'If $\eR^p k^!\dZ/n=0$ for $p\leqslant 2 c+1$')
sol(573,142,r'\cite[1.8, 1.10, 1.15]{sga2}',r'\cite[XIV 1.8, 1.10, 1.15]{sga2}')
sol(574,142,r'\begin{theorem}\label{IV:2-2-8}',r'\subsubsection{Recall}\label{IV:2-2-8}')
sol(574,142,r'\end{theorem}'+'\n\n'+r'Since $\eR g^!',r'Since $\eR g^!')
sol(575,142,'a morphism of $S$-schemes of finite type','a morphism of separated $S$-schemes of finite type')
sol(578,143,r'\cite{bfm75}',r'\PrintCite{(Riemann-Roch for singular varieties, Publ. Math. IHES 45 (1975) p.~101--146 -- IV 4)}{\cite[IV 4]{bfm75}}',ai_translated=True)
sol(582,143,'are homotopic on a sufficiently small neighborhood of $Y$','are homotopic on a sufficiently small $U$')
sol(587,144,r'Y \ar@{^{(}->}[r]^-i \ar[dr]_-f'+'\n'+r'    & X \ar[d] \\',r'Y \ar@{^{(}->}[r]^-i \ar[dr]_-f'+'\n'+r'    & X \ar[d]^-g \\')
sol(594,146,'We shall define the trace morphisms, and hence the class','We shall define the trace morphism, and hence the class')
sol(595,146,r'Y \ar@{^{(}->}[r] \ar[dr]_-f',r'Y \ar@{^{(}->}[r]^-i \ar[dr]_-f')
sol(596,146,r'\h^i(\sK)_y',r'\mathcal{H}^i(\sK)_y')
sol(601,147,r'\tag{2.3.4}',r'\tag{2.3.4.1}')
sol(604,147,r"\eR f_!\dZ/n(d')[2 d']",r"\eR f_!'\dZ/n(d')[2 d']")
own(34,148,r'\paragraph{(A)}',r'\paragraph{(2.3.8.1)}\label{IV:2-3-8-1}')
own(35,149,r'\paragraph{(B) Proof',r'\paragraph{(2.3.8.2) Proof')
own(35,149,'By localization (A)','By localization (2.3.8.1)')
own(35,149,r'\paragraph{(C) In',r'\paragraph{(2.3.8.3) In')
own(35,149,'covered by (C) with','covered by (2.3.8.3) with')
own(35,149,'the latter by (B)','the latter by (2.3.8.2)')
own(35,149,'to (B) and (C)','to (2.3.8.2) and (2.3.8.3)')
sol(624,151,r'\h^*(Y)\otimes \h^*(Y) \ar[r]',r'\h^*(Y)\otimes \h^*(Y) \ar[r]^-{\cdot}')
own(38,153,r'X\setminus U',r'X-U')
own(38,153,r'\bar U\setminus U',r'\bar U-U')
add('PAGE-153',153,'the smooth projective completion of $U$','the projective and smooth completion of $U$',reason='Align the printed page boundary after projective with the same adjective boundary in English.')

contents=r'''\begin{center}\textbf{Contents}\end{center}
\begin{tabular}{p{0.84\textwidth}r}
1. Cohomology with support and cup products & 3\\
1.1. $H^1$ and torsors & 3\\
1.2. Cup products & 5\\
1.3. The Koszul rule & 8\\
2. The cohomology class associated with a cycle & 10\\
2.1. The class of a divisor & 10\\
2.2. Cohomological method & 11\\
2.3. Homological method & 16\\
3. Application: the Lefschetz trace formula in the proper smooth case & 23
\end{tabular}

'''
anchor=r'\section{Cohomology with support and cup products}\label{IV:1}'
own(26,130,anchor,contents+anchor,ai_translated=True)
(P/'en_changes_4.json').write_text(json.dumps(changes,ensure_ascii=False,indent=2))

# Set each semantic English variant against the same annotated French source.
vs=[json.loads(l)for l in(P/'variants.jsonl').read_text().splitlines()]
custom={
 'S45-ASTRA-R-0031':(r'\otimes \eR^{2 d} f_!\dZ/n(d)',None,None),
 'S45-SOL-0593':('where the cup product can be computed in '+r'$\h^*(X,\dZ/n)$.','where the cup product can be computed in '+r'$\h^*(X,\dZ/n)$.','where the cup product can be computed in '+r'$\h^*(X,\dZ/n(c))$.'),
 'S45-SOL-0600':(r'u:X\to \dA_S^d',None,None),
 'S45-SOL-0603':(r'\h_Y^{2 c}\left(X,\dZ/n(c)\right)',None,None),
 'S45-SOL-0613':(r"with $Y'=X'$",r"with $X'=X'$",r"with $Y'=X'$"),
 'S45-SOL-0615':(r"\cl(Y')=1\in \h^0(X',\dZ/n)",None,None),
 'S45-SOL-0619':('By (iii), one therefore has','By (iv), one therefore has','By (iii), one therefore has'),
 'S45-SOL-0621':(r'$2(q-M)$, $\eta_{XY}:\h^*(Y)(M-q)\to \h^*(X)$',r'$2(q-N)$, $\eta_{XY}:\h^*(Y)(N-q)\to \h^*(X)$',r'$2(q-M)$, $\eta_{XY}:\h^*(Y)(M-q)\to \h^*(X)$'),
 'S45-SOL-0626':(r'The proof of \ref{IV:3-3}',r'The proof of \ref{IV:3-4}',r'The proof of \ref{IV:3-3}'),
}
for v in vs:
 if not(129<=int(v['page'])<=153)or not v['english_applicability']:continue
 a,b,c=custom.get(v['id'],(v['old'],None,None))
 v.update(en_old=a,printed_en=b if b is not None else v['printed'],corrected_en=c if c is not None else v['corrected'])
 if v['id']=='S45-SOL-0603':v['en_anchor']=r'\begin{lemma}\label{IV:2-3-5}'
(P/'variants.jsonl').write_text(''.join(json.dumps(v,ensure_ascii=False)+'\n'for v in vs))
