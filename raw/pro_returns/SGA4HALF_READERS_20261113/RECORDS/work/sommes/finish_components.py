"""Reproducible assembly of personally scanned component 6.
The first pass is build_components.py; this pass resolves source-tree alternatives,
English alignment, and inserts only explicitly reviewed print variants.
"""
from build_components import *
OUT=[];FAIL=[];STATE={};PRE={}
for L in ('fr','en'):
 t=(B/f'diagnostic_{L}.tex').read_text();s=re.split(r'\\PrintPage\{(\d+)\}\n',t)
 PRE[L]=s[0];STATE[L]={int(s[i]):s[i+1] for i in range(1,len(s),2)}
def op(p,L,id,old,new,count=1,which=None,after=None):
 t=STATE[L][p];off=0
 if after:
  mm=positions(t,after)
  if len(mm)!=1:raise ValueError(('selector',p,L,id,after,len(mm)))
  off=mm[0].end()
 ms=positions(t[off:],old)
 if which is not None:ms=ms[which:which+1]
 if len(ms)!=count:
  FAIL.append(dict(page=p,lang=L,id=id,old=old,new=new,count=len(ms),expected=count));return False
 for m in reversed(ms):t=t[:off+m.start()]+new+t[off+m.end():]
 STATE[L][p]=t;OUT.append(dict(page=p,lang=L,id=id,old=old,new=new,count=count,status='applied',selector=after,which=which));return True

def both(p,id,old,new,**kw):
 for L in ('fr','en'):op(p,L,id,old,new,**kw)
def sol(n):return f'S45-SOL-{n:04}'
def own(n):return f'S45-ASTRA-S-{n:04}'

# Resolve the exact source spellings and later transcription changes.
op(192,'fr',sol(776),r'\eqref{VI:eq:3-5-4}, $\h^1$ est',r'\eqref{VI:eq:3-5-4}, ce $\h^1$ est')
both(208,sol(869),r'\prod_\omega \omega(x)^{n_\omega}',r'\prod \omega(x)^{n_\omega}')
for p,id,old,new in [(216,914,r'\left\langle \frac{i a_j}{n} \right\rangle',r'\left\{ \frac{i a_j}{n} \right\}'),(216,915,r'$\langle \cdot \rangle$',r'$\{\ \}$'),(217,924,r'\left\langle \frac{i a}{n}\right\rangle',r'\left\{ \frac{i a}{n}\right\}')]:both(p,sol(id),old,new)
for L in ('fr','en'):
 op(205,L,own(50),r'(T v_0)',r'(T v)',count=3,after=r'\tag{4.17.3}')
 op(205,L,own(50),r'$T v_0$',r'$T v$')
 op(206,L,own(50),r'(T v_0)',r'(T v)',count=2)
 op(227,L,own(51),r"$x_2'=x_2\circ \pr_1$",r"$x_2'=x_2\circ \pr_2$")
 op(228,L,own(52),r'\h_c^{n-1}(V_a,\sF(\psi\sigma))',r'\h_c^{n-1}(V_a,\sF(\psi))',after='le sous-espace de' if L=='fr' else 'and the subspace of')

# Bilingual alignment of shared repairs where prose surrounds the changed content.
op(174,'en',sol(694),r'\begin{theorem_}\label{VI:1-9}',r'\subsection{Scholium}\label{VI:1-9}')
op(174,'en',sol(694),r'\end{theorem_}','')
op(177,'en',sol(700),r'\cite[App V, $3^\text{e}$ éd.]{we74}',r'\cite[App V, 3rd ed.]{we74}')
op(177,'en',sol(702),r'P.~Deligne, \emph{La conjecture de Weil II}, en préparation',r'P.~Deligne, \emph{La conjecture de Weil II}, in preparation')
op(181,'en',sol(729),r'The map induced by',r'The map $\prime$, induced by')
op(181,'en',sol(730),r'the corresponding map for the opposite',r'the map $\prime$ for the opposite')
op(192,'en',sol(776),r'the dimension of $\h^1$',r'the dimension of this $\h^1$')
op(196,'en',sol(800),r'K\"ummer','Kummer')
op(197,'en',sol(807),r'$k_i$ of degrees $N_i$, and',r'$k_i$ of degrees $N_i$ over $\dF_q$, and')
op(199,'en',sol(815),'Dès lors,','Consequently,')
op(208,'en',sol(862),r'$A\in k(X^i)$',r'where $A\in k(X^i)$')
op(210,'en',sol(876),r'$\equiv 1\pmod\fm$. We',r'$\equiv 1(\fm)$. We')
op(210,'en',sol(880),r'all of whose conjugates have',r'all of whose complex conjugates have')
op(214,'en',sol(895),r'The integral closure $M$ of $A$',r'The integral closure $M$ of $A$ in $E$')
op(221,'en',sol(936),r'Let us verify the case $a=0$ of \ref{VI:7-5}',r'Let us verify the case $a=0$ of \ref{VI:7-4}')
op(228,'en',sol(963),'Salie and Mordell','Salié and Mordell')
op(228,'en',sol(964),'our methods make it possible to study','our methods also make it possible to study')
op(228,'en',sol(965),r'The symmetric group $S_n$',r'The symmetric group $\mathfrak{S}_n$')
op(228,'en',sol(970),r'The action of $S_n$',r'The action of $\mathfrak{S}_n$')
op(228,'en',sol(967),r'$\sf(\psi\sigma)$',r'$\sF(\psi\sigma)$',count=2)
op(230,'en',sol(979),r'VIII \S 2 Rem.2',r'VIII \S 5 Rem.2')
op(230,'en',own(47),r'\cite[VIII \S 5 Rem.2]{bo05}',r'Bourbaki, Lie VIII \S 5 Remark~2 \cite[VIII \S 5 Rem.2]{bo05}')


# Revert unneeded later-tree mathematical expansions to the printed formulas.
op(201,'en',own(53),r'\chi_{-i}(x)',r'\chi_{-i}')
op(206,'en',own(54),r'\h_c^\bullet(\dG_a,\sF(\psi))',r'\h^\bullet(\dG_a,\sF(\psi))')
op(211,'en',own(55),r'\chi_\lambda:\gal(\bar F/F)^\textnormal{ab} \to E_\lambda^\ast',r'\chi_\lambda:\gal(\bar F/F)^\textnormal{ab} \to E_\lambda')
op(215,'en',own(56),r'\item If $i\in \beta$',r'\item If $i\in I$')
op(222,'en',own(57),r'\eR^i \pi_!\sF(\psi\sigma)$ are locally constant',r'\eR^i \pi_!\sF(\psi^{-1}\sigma)$ are locally constant')
op(222,'en',own(57),r'\eR^i \pi_! \sF(\psi\sigma) \iso \eR^i \pi_\ast \sF(\psi\sigma)',r'\eR^i \pi_! \sF(\psi) \iso \eR^i \pi_\ast \sF(\psi)',after=r'\begin{lemma_}')
op(224,'en',own(58),r'\delta:i_!(\sG\otimes \eR^{n-1}\pi_! \sF(\psi\sigma))',r'\delta:i_!(\sG\otimes \eR^{n-1}\pi_! \sF(\psi))')
op(225,'en',own(59),r'\eR^q \pi_! \sF(\psi\sigma))$ at',r'\eR^q \pi_! \sF(\psi))$ at')
op(225,'en',own(59),r"\dim{'E_2^{1,n-1}}",r"\dim{'E_2^{p q}}")
op(226,'en',own(60),r'\tau^\ast \eR^{n-1} \pi_! \sF(\psi\sigma)',r'\tau^\ast \eR^{n-1} \pi_! \sF(\psi)',after=r'\item the global constants')
op(200,'en',own(61),r'a $E_\lambda$-sheaf',r'an $E_\lambda$-sheaf')
op(210,'en',own(62),'is a algebraic number','is an algebraic number')
op(211,'en',own(63),r'a $\ell$-adic cohomology argument',r'an $\ell$-adic cohomology argument')
op(218,'en',own(64),'a odd character','an odd character')
op(226,'en',own(65),'are easy to calculated easily','are easy to calculate')
op(209,'en',own(66),'every ideal $a$ has a power','every ideal has a power')
op(209,'en',own(67),'also called \nWeil Hecke characters','called by Weil \nHecke characters')
op(175,'en',own(68),'after a \nextension','after an \nextension')
op(181,'en',own(69),r'$x\mapsto (y\mapsto F x\cdot y\cdot x^{-1})$)',r'$x\mapsto (y\mapsto F x\cdot y\cdot x^{-1})$')
op(181,'en',own(70),'conjugation class','conjugacy class')
op(189,'en',own(71),r'and $\sF$ as in',r'and $\sF$ be as in')
op(199,'en',own(72),'projective system of groups','inverse system of groups')
op(229,'en',own(73),'by methods \n$p$-adic methods','by \n$p$-adic methods')
op(183,'en',own(74),r'\cite[XXI, 5.2.2 et 5.4]',r'\cite[XXI, 5.2.2 and 5.4]')
op(211,'en',own(74),r'\cite[II 2.1 et 2.2]',r'\cite[II 2.1 and 2.2]')
op(204,'en',sol(842),'or equivalently as','more often written in the form')
op(216,'en',sol(908),'places of degree greater than $1$','places of degree $1$')
op(216,'en',sol(908),'disregard \nthem','disregard \nthe others')

# Prepare exact English phrasing for semantic variants, preserving the source meaning.
op(178,'en',sol(707),r'$\h_c^i(X,\sF)$ and $\h^{2n-i}(X,\sF^\vee)(n)$',r'$\h_c^i(X,\sF)$ and $\h^{2n-i}(X,\sF^\vee)(2n)$')
op(179,'en',sol(719),'be an open immersion with domain $X$,',r'be an open subset of $\bar X$,')
op(190,'en',sol(765),'for any closed point $x$',r'for every closed point $x$')
op(192,'en',sol(773),r'$\dF_q$-torsor on $\spec(\dF_q)$',r'$\dF_q$-torsor over $\spec(\dF_q)$')
op(208,'en',sol(859),'and let $k$ be a field',r'and $k$ a field')
op(210,'en',sol(882),'Since the group of ideal classes of $k$ is torsion,',r'Since the group of fractional ideals of $k$ is torsion-free,')

# Paired delimiter/index variants in the first constrained sum of p195.
for L in ('fr','en'):
 old=r'\left|\sum_{S=\lambda} \psi P(x_1,\dots,x_n)\right|' if L=='fr' else r'\left|\sum_{S_1=\lambda} \psi P(x_1,\dots,x_n)\right|'
 new=r'\var{\left.}{\left|}{S45-SOL-0794}\var{\sum_{S=\lambda}}{\sum_{S_1=\lambda}}{S45-SOL-0795} \psi P(x_1,\dots,x_n)\right|'
 op(195,L,sol(794)+';'+sol(795),old,new)

# All remaining variants are inserted with an explicit per-row resolution.
# A restored literal bibliographic reference must not acquire a second numeric
# citation. Preserve Miller's key in PrintCite's source-only second argument.
citation_ids={own(n) for n in (10,12,13,15,42,43,44,46,47)}
for r in readj('edits'):
 if r['source'] not in citation_ids:continue
 old=r['new'];m=re.search(r'\s*(\\cite(?:\[[^\]]*\])?\{[^}]+\})$',old)
 if m:
  new=r'\PrintCite{'+old[:m.start()]+r'}{'+m.group(1)+'}'
  op(int(r['page']),r['lang'],r['source'],old,new)
for L,phrase in [('fr','en préparation'),('en','in preparation')]:
 old=r'P.~Deligne, \emph{La conjecture de Weil II}, '+phrase+r' \cite{de80}'
 new=r'\PrintCite{P.~Deligne, \emph{La conjecture de Weil II}, '+phrase+r'}{\cite{de80}}'
 op(177,L,sol(702),old,new)

VARLOG=[]
for r in readj('variants'):
 p=int(r['page']);id=r['id']
 for L in ('fr','en'):
  if L=='en' and not r['english_applicable']:
   VARLOG.append(dict(id=id,page=p,lang=L,status='French spelling/grammar only; English semantic reading unchanged'));continue
  t=STATE[L][p]
  if id in t:
   VARLOG.append(dict(id=id,page=p,lang=L,status='embedded in restored passage or paired edit'));continue
  old,new=(r['printed'],r['corrected']) if L=='fr' else (r['en_printed'],r['en_corrected'])
  old,new=clean(old),clean(new)
  before=None;off=0;expected=1;which=None
  if id==sol(690):off=t.index(r'\subsection')
  if id==sol(690) and L=='en':off=t.index(r'\item with the notation')
  if id==sol(748):which=0
  if id==sol(819) and L=='en':which=1
  if id==sol(833):which=1 if L=='en' else None
  if id==sol(847):
   a=t.index(r'\begin{proposition_}');b=t.index(r'\end{proposition_}')
   off=a;before=t[:b];expected=2
  if id==sol(849) and L=='en':which=1
  if id==sol(856):expected=3
  sub=(before if before is not None else t)[off:]
  om=positions(sub,old);nm=positions(sub,new)
  # Longest printed/corrected expression wins where the printed fragment is a prefix.
  if nm and norm(old) in norm(new):use=new;ms=nm;reading='corrected reading already in supplied source'
  elif id==sol(748) and L=='en':use=new;ms=nm;reading='corrected reading already in supplied source'
  elif om:use=old;ms=om;reading='printed reading in supplied source'
  elif nm:use=new;ms=nm;reading='corrected reading already in supplied source'
  else:
   FAIL.append(dict(page=p,lang=L,id=id,status='variant unmatched',old=old,new=new));continue
  if which is not None:ms=ms[which:which+1]
  if len(ms)!=expected:
   FAIL.append(dict(page=p,lang=L,id=id,status='variant ambiguous',count=len(ms),expected=expected,old=old,new=new));continue
  replacement='\\var{'+old+'}{'+new+'}{'+id+'}'
  for m in reversed(ms):t=t[:off+m.start()]+replacement+t[off+m.end():]
  STATE[L][p]=t
  VARLOG.append(dict(page=p,lang=L,id=id,status='inserted',source_reading=reading,count=len(ms),printed=old,corrected=new))

for L in ('fr','en'):
 out=PRE[L]+''.join('\\PrintPage{'+str(p)+'}\n'+body for p,body in STATE[L].items())
 dest=B/L/('sga4.5-6.tex' if L=='fr' else 'sga4half_6_en.tex');dest.parent.mkdir(exist_ok=True);dest.write_text(out)
(B/'assembly_ops.json').write_text(json.dumps(OUT,ensure_ascii=False,indent=2))
(B/'variant_application.json').write_text(json.dumps(VARLOG,ensure_ascii=False,indent=2))
(B/'assembly_failures.json').write_text(json.dumps(FAIL,ensure_ascii=False,indent=2))
print('Manual operations',len(OUT),'variant outcomes',len(VARLOG),'failures',len(FAIL))
for r in FAIL:print(r)
