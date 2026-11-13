import json,re
from pathlib import Path
from record import append,variant
from build_components import DEC,raw,SOL,matches
O=Path(__file__).resolve().parent
vs=[json.loads(l) for l in (O/'variants.jsonl').read_text().splitlines()]
for v in vs:
 if v['id'] in ('S45-SOL-0450','S45-SOL-0452'):
  for k in ['old','printed','corrected']:v[k]=v[k].replace("\\'", "'")
mp={
 'S45-SOL-0450':(r"s(\Gamma^i K'\otimes \Gamma^i K'')",None,None),
 'S45-SOL-0452':(r"$\Gamma^i K'\otimes \Gamma^i K''$, and",r"$\Gamma^i K'\otimes \Gamma^i K''$, and",r"$\Gamma^i K'\otimes \Gamma^j K''$, and"),
 'S45-SOL-0490':(r"\Phi(I^n \sG')\subset I^{p^n}\Phi(\sG')",None,None),
 'S45-SOL-0506':(r'\ker(\Phi-1)\otimes_{\dF_p}\dF \iso',None,None),
 'S45-SOL-0509':(r'each side of \eqref{III:eq:4-1-1}','each side of (3.1.1)',r'each side of \eqref{III:eq:4-1-1}'),
 'S45-SOL-0512':(r'the two sides of \eqref{III:eq:4-1-1}','the two sides of (3.1.1)',r'the two sides of \eqref{III:eq:4-1-1}'),
 'S45-SOL-0513':(r'If \eqref{III:eq:4-1-1} holds','If (3.1.1) holds',r'If \eqref{III:eq:4-1-1} holds'),
 'S45-ASTRA-R-0012':('Theory of Artin--Schreier','Theory of Artin-Scheier','Theory of Artin--Schreier'),
 'S45-ASTRA-R-0013':(r'Artin--Schreier theory \cite[IX 3.5]{sga4}',r'Artin-Scheier theory \cite[IX 3.5]{sga4}',r'Artin--Schreier theory \cite[IX 3.5]{sga4}'),
 'S45-ASTRA-R-0015':('Artin--Schreier theory provides','Artin-Scheier theory provides','Artin--Schreier theory provides'),
 'S45-ASTRA-R-0018':('Woods Hole fixed point formula',None,None),
 'S45-ASTRA-R-0019':('uF^*',None,None),
 'S45-ASTRA-R-0020':(r'the endomorphism $u_x$ of $\bar\sG_x$',r'the endomorphism $u_x$ of $\sG_x$',r'the endomorphism $u_x$ of $\bar\sG_x$'),
 'S45-SOL-0520':(r'\frac{\tr(u_x,\sG_x)}',None,None),
}
for v in vs:
 if not 110<=int(v['page'])<=128 or not v['english_applicability']:continue
 o,p,c=mp.get(v['id'],(v['old'],None,None));v.update(en_old=o,printed_en=p if p is not None else v['printed'],corrected_en=c if c is not None else v['corrected'])
(O/'variants.jsonl').write_text(''.join(json.dumps(v,ensure_ascii=False)+'\n' for v in vs))
ps=[json.loads(l) for l in (O/'pages.jsonl').read_text().splitlines()]
for p in ps:
 if p['printed_page']=='120':p['start_fr']=r'\section{\var{Théorie';p['start_en']=r'\section{\var{Theory'
 if p['printed_page']=='124':p['start_fr']=r'\[ \var{\ker(\Phi-1)';p['start_en']=r'\[ \var{\ker(\Phi-1)'
(O/'pages.jsonl').write_text(''.join(json.dumps(p,ensure_ascii=False)+'\n' for p in ps))
changes=[]
def ch(i,p,o,n,ai=False,all=False):changes.append(dict(id=i if isinstance(i,str) else f'S45-SOL-{i:04}',page=p,old=o,new=n,ai_translated=ai,all=all))
# Pure mathematical corrections, read explicitly in English source and in the scan.
for num in [441,444,457,464,465,466,467,475,476,482,486,494,495,498,499,500,502,503,504,507,516,526]:
 ident=f'S45-SOL-{num:04}';r=SOL[ident];fix=raw.get(ident,dict(old=r['fix_old'],new=r['fix_new']));ch(num,int(r['printed_page']),fix['old'],fix['new'])
ch(446,112,r'If $\Gamma$ is a functor',r'If $T$ is a functor')
ch(468,117,r'where $X$ is reduced to the',r'where $\sK$ is reduced to the')
ch(470,117,r'constant sheaf $\dZ/p$ in degree $0$,',r'constant sheaf $\dZ/p$ in degree $0$:')
ch(474,117,r'the case where $X$ is affine',r'the case where $X_0$ is affine')
ch(479,118,'More precisely,','More precisely, one has',True)
ch(485,120,r'endomorphism $f\mapsto f^p$',r'endomorphism $f\to f^p$')
ch(488,120,r'closed complement $\bar S\setminus S$',r'closed complement $\bar S-S$')
ch('S45-ASTRA-R-0014',121,r'the inverse image of $\bar S\setminus S$',r'the inverse image of $\bar S-S$')
ch('S45-ASTRA-R-0014',121,r'hence is zero near $\bar S\setminus S$',r'hence is zero near $\bar S-S$')
ch(496,122,r'every étale sheaf $\sG$ on $S$, the Frobenius correspondence $F_\text{abs}^*\sG\to\sG$',r'every étale sheaf $G$ on $S$, the Frobenius correspondence $F_\text{abs}^*G\to G$')
ch(497,122,r'F_\text{abs}^F:S_0\to S_0',r'F_\text{abs}^f=F:S_0\to S_0')
ch('S45-ASTRA-R-0016',123,r'\h^\bullet',r'\h^*',all=True) # all11 occurrences separately checked:8p123,3p126
ch('S45-ASTRA-R-0021',127,r'\h_c^\bullet',r'\h_c^*',all=True) # two p127 plus two p128, each viewed
ch(505,123,r'the respective $p$-linear extensions of $\Phi$ and $F$',r'the respective $p$-linear and linear extensions of $\Phi$ and $F$',True)
ch(514,126,r'\begin{theorem_}\label{III:4-1bis}',r'''\subsection{}\label{III:4-4}
The method of \hyperref[II]{Report} \S\ref{II:6} now reduces \ref{III:4-1} to the following statement.

\begin{theorem_}\label{III:4-1bis}''',True)
ch(517,126,r'\end{equation*} Finally, denote',r'\end{equation*}'+'\nis commutative.\n\nFinally, denote',True)
ch(521,127,r'\eqref{III:eq:4-4-3} and \eqref{III:eq:4-4-4}',r'\eqref{III:eq:4-4-3} \eqref{III:eq:4-4-4}')
ch(523,127,r'line $\dF_0^1$',r'line $\dA_0^1$')
ch(524,127,r'$\dF_0^1$:',r'$\dA_0^1$:')
ch(525,127,r'the algebra of numbers over $\dZ/2$',r'the algebra of dual numbers over $\dZ/2$',True)
ch('S45-ASTRA-R-0012',120,r'\section{Artin--Schreier theory}',r'\section{Theory of Artin--Schreier}',True)
# Restore the local printed summary (p110); its spelling variant is distinct from section heading.
frsummary=r'''\begin{center}\textbf{Sommaire}\end{center}
\begin{tabular}{@{}lr@{}}
1. Tenseurs symétriques & 2 \\
2. Le théorème & 7 \\
3. Théorie d'Artin-Scheier & 11 \\
4. Formule des traces modulo $p$ & 16
\end{tabular}'''
ensummary=r'''\begin{center}\textbf{Contents}\end{center}
\begin{tabular}{@{}lr@{}}
1. Symmetric tensors & 2 \\
2. The theorem & 7 \\
3. Theory of Artin-Scheier & 11 \\
4. Trace formula modulo $p$ & 16
\end{tabular}'''
frend=r'caractéristique $p$. Un usage essentiel sera fait de \cite[XVII 5.5]{sga4}.'
enend=r'Essential use will be made of \cite[XVII 5.5]{sga4}.'
summaryvar=r'\var{Artin-Scheier}{Artin--Schreier}{S45-ASTRA-R-0023}'
frsummary=frsummary.replace('Artin-Scheier',summaryvar);ensummary=ensummary.replace('Artin-Scheier',summaryvar)
(O/'supplement_fr_3.json').write_text(json.dumps([dict(id='S45-ASTRA-R-0011',page=110,old=frend,new=frend+'\n\n'+frsummary)],ensure_ascii=False,indent=2))
ch('S45-ASTRA-R-0011',110,enend,enend+'\n\n'+ensummary,True)
(O/'en_changes_3.json').write_text(json.dumps(changes,ensure_ascii=False,indent=2))
# Summary spelling checked independently on the page image.
append('own_findings.jsonl',dict(id='S45-ASTRA-R-0023',page='110',place='Summary entry3',printed_reading='Artin-Scheier',tex_reading='summary omitted',change='Restore printed spelling with explicit Schreier correction.',kind='misprint_in_print',reason='The summary repeats the misspelling found in the section heading and body.'))
append('variants.jsonl',dict(id='S45-ASTRA-R-0023',page='110',place='Summary entry3',old='already inserted by supplement_fr_3.json',printed='Artin-Scheier',corrected='Artin--Schreier',reason='Printed eponym misspelled.',kind='misprint_in_print',english_applicability=True,embedded=True))
