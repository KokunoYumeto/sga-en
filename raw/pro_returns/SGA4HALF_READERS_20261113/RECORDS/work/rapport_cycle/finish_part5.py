from pathlib import Path
import json,re
P=Path(__file__).resolve().parent
def read(n):return [json.loads(l)for l in(P/n).read_text().splitlines()]
def write(n,a):(P/n).write_text(''.join(json.dumps(x,ensure_ascii=False)+'\n'for x in a))
changes=[]
def add(id,page,old,new,**kw):changes.append(dict(id=id,page=page,old=old,new=new,**kw))
def sol(n,page,old,new,**kw):add(f'S45-SOL-{n:04}',page,old,new,**kw)
def own(n,page,old,new,**kw):add(f'S45-ASTRA-R-{n:04}',page,old,new,**kw)

contents_fr=r'''\begin{center}\textbf{Sommaire}\end{center}
\begin{tabular}{p{0.84\textwidth}r}
1. Bidualité locale, en dimension $1$ & \var{1}{2}{S45-ASTRA-R-0056}\\
2. La dualité de Poincaré pour les courbes, d'après M.\ Artin & 5\\
3. Dualité de Poincaré et jacobienne & 8\\
4. Compatibilité SGA 4 XVIII 3.1.10.3 & \var{12}{13}{S45-ASTRA-R-0057}
\end{tabular}

'''
contents_en=r'''\begin{center}\textbf{Contents}\end{center}
\begin{tabular}{p{0.84\textwidth}r}
1. Local biduality in dimension $1$ & \var{1}{2}{S45-ASTRA-R-0056}\\
2. Poincaré duality for curves, after M.\ Artin & 5\\
3. Poincaré duality and the Jacobian & 8\\
4. Compatibility SGA 4 XVIII 3.1.10.3 & \var{12}{13}{S45-ASTRA-R-0057}
\end{tabular}

'''
anchor=r'\section{Bidualité locale, en dimension \texorpdfstring{$1$}{1}}'
(P/'supplement_fr_5.json').write_text(json.dumps([
 dict(id='S45-ASTRA-R-0042',page=154,old=anchor,new=contents_fr+anchor),
 dict(id='S45-ASTRA-R-0058',page=154,old=r'\cite[I.5.1]{sga5}',new=r'\PrintCite{(SGA~5 I 5.1)}{\cite[I.5.1]{sga5}}'),
 dict(id='S45-ASTRA-R-0058',page=166,old=r'\cite[XVIII]{sga4}',new=r'\PrintCite{SGA~4 XVIII}{\cite[XVIII]{sga4}}')
 ],ensure_ascii=False,indent=2))
anchor=r'\section{Local biduality in dimension \texorpdfstring{$1$}{1}}'
own(42,154,anchor,contents_en+anchor,ai_translated=True)
own(58,154,r'\cite[I.5.1]{sga5}',r'\PrintCite{(SGA~5 I 5.1)}{\cite[I.5.1]{sga5}}')
own(58,166,r'\cite[XVIII]{sga4}',r'\PrintCite{SGA~4 XVIII}{\cite[XVIII]{sga4}}')
sol(633,155,r'$(-)_c$',r'${}_c$')
sol(635,155,'gives\n'+r'\[\xymatrix{',r'''gives
\[
  \eR f_\ast D\sK = \eR f_\ast \rHom(\sK,\eR f^! \dZ/n) = \rHom(\eR f_! \sK,\dZ/n) = D\eR f_! \sK \text{.}
\]
The corresponding pairing between $\eR f_!\sK$ and $\eR f_\ast D\sK$ is the composite
\[\xymatrix{''',ai_translated=True)
sol(636,155,r'\eR f_\ast \sK\lotimes',r'\eR f_! \sK\lotimes')
sol(637,156,r'j_\ast\Hom(\sF,\dZ/n)',r'j_\ast\Hom(\sF,\dZ/n_U)')
own(43,156,r'\underline\h^\bullet(\sK)',r'\underline\h^*(\sK)')
own(44,156,r'\eD j_\ast \sF = j_\ast D \sF',r'D j_\ast \sF = j_\ast D \sF')
own(47,156,r'S\setminus U',r'S-U')
sol(640,157,r'\left(\underline\h^1(D j_\ast\sF)\right)_s',r'\left(\underline\h^1 D j_\ast\sF\right)_s')
own(49,159,r'\h^\bullet(D\sF) = \ext^\bullet(\sF,\sK_X)',r'\h^*(D\sF) = \ext^*(\sF,\sK_X)')
own(49,159,r'\h^\bullet(\sF)\otimes\h^\bullet(D\sF)',r'\h^*(\sF)\otimes\h^*(D\sF)')
sol(646,160,r'\h^i(X,\sF) \to \h^i(X,f_\ast\dZ/n)',r'\h^i(X,\sG) \to \h^i(X,f_\ast\dZ/n)')
sol(648,160,r'$\sF$ by \eqref{V:eq:2-5-2}. Applied to $\sQ$, this gives',r'''$\sF$ by \eqref{V:eq:2-5-2}. Applying this to $\sQ$, we find that $\h^0(X,\sG)\iso '\h^0(X,\sG)$. The same holds for $\sF$ by \eqref{V:eq:2-5-2}. Applied to $\sQ$, this gives''',ai_translated=True)
own(50,161,r'X=\bar X\setminus D',r'X=\bar X-D')
own(51,161,r'\h^\bullet(X\times \bar X,j_!\dmu_n) = \h^\bullet(X,\dZ/n)\otimes \h^\bullet(\bar X,j_!\dmu_n) = \h^\bullet(X,\dZ/n)\otimes \h_c^\bullet(X,\dmu_n)',r'\h^*(X\times \bar X,j_!\dmu_n) = \h^*(X,\dZ/n)\otimes \h^*(\bar X,j_!\dmu_n) = \h^*(X,\dZ/n)\otimes \h_c^*(X,\dmu_n)')
sol(652,161,r'\ar[r]^n',r'\ar[r]^-{x\to x^n}')
own(52,162,r'\h^\bullet(X)',r'\h^*(X)')
own(55,162,'the closed subscheme $X'+r'\times D$','the subscheme $X'+r'\times D$')
own(53,163,'obtained by replacing the degree-one term $'+r'\ker(d)$','obtained by replacing $'+r"{\sB'}^1=\ker(d)$")
own(54,163,r'\h^0(X,\eR^1\pr_{1\ast}\sG) = \hom(X,\pic_D(\bar X))',r'\h^0(X,\eR^1\pr_\ast\sG) = \hom(X,\pic_D(\bar X))')
sol(660,163,'sheaves concentrated in degree $1$ on $X$.','sheaves concentrated in degree $1$ on $X$. We have',ai_translated=True)
sol(662,164,r'\h_c^2(X,\dmu_n)$ relative',r'\h_c^1(X,\dmu_n)$ relative')
sol(667,166,'a\ncompatibility for $'+r'\sL$ a sheaf','an analogous\ncompatibility for $'+r'\sL$ a sheaf')
sol(668,166,r'k^\ast k_!\to k_! k^\ast',r'k^\ast k_!=k_! k^\ast')
sol(669,166,r'f^!:k^\ast \to',r'f^!:k^\ast f^! \to')
sol(670,166,r'f^! f_! k^\ast f^!\to',r'f^! f_! k^\ast f^!=')
(P/'en_changes_5.json').write_text(json.dumps(changes,ensure_ascii=False,indent=2))

vs=read('variants.jsonl')
for num,printed,corrected,place,reason in [
 (56,'1','2','Contents entry1','The printed local page number1 points to the introductory page; section1 actually begins on localpage2, printed155.'),
 (57,'12','13','Contents entry4','The printed local page number12 points to the end of section3; section4 actually begins on localpage13, printed166.')]:
 ident=f'S45-ASTRA-R-{num:04}'
 if ident not in {v['id']for v in vs}:vs.append(dict(id=ident,page='154',old='',printed=printed,corrected=corrected,reason=reason,english_applicability=True,place=place,kind='number',embedded=True,embedded_en=True))
for v in vs:
 if not 154<=int(v['page'])<=167:continue
 if v.get('embedded'):continue
 ident=v['id']; v['en_old']=v['old'] if v['english_applicability']else''
 v['printed_en']=v['printed'];v['corrected_en']=v['corrected']
 if ident=='S45-SOL-0639':
  v['suffix']=r'\text{.}';v['en_suffix']=r'\text{.}'
 if ident=='S45-SOL-0642':
  v.update(prefix='est $',suffix=r'$, avec $\tr_f$',en_old=r'is $f_\ast\dZ/n$, with $\tr_f$',en_prefix='is $',en_suffix=r'$, with $\tr_f$')
 if ident=='S45-SOL-0655':
  v.update(suffix=' est un triangle distingué',en_old=r'\eqref{V:eq:3-2-1} gives a distinguished triangle',en_suffix=' gives a distinguished triangle')
 if ident=='S45-SOL-0656':
  suffix=r'\ar[r]'if v['place']=='First G term'else r'\ar[r]^-\partial'
  v.update(suffix=suffix,en_old=r'\eR \pr_{1\ast}\sG '+suffix,en_suffix=suffix)
  if v['place']=='First G term':v['en_anchor']=r'\tag{3.2.2}\label{V:eq:3-2-2}'
 if ident=='S45-SOL-0657':
  v.update(prefix=r'\tag{',suffix=r'}\label{V:eq:3-2-3}',en_prefix=r'\tag{',en_suffix=r'}\label{V:eq:3-2-3}')
 if ident=='S45-SOL-0664':v['en_old']=r"u'=-c^{1,1}"
write('variants.jsonl',vs)

ps=read('pages.jsonl')
for p in ps:
 if p['printed_page']=='158':p['start_en']=r'\section{Poincaré duality for curves, after M.\ Artin}'
 if p['printed_page']=='166':p['start_en']=r'\section{Compatibility with SGA 4 XVIII 3.1.10.3}'
 if p['printed_page']=='167':p['start_en']='In the first row, we find a homomorphism'
write('pages.jsonl',ps)

# This suspected missing arrow was rechecked before application: it is already
# present in Miller as well as Codex. Retain the negative decision transparently.
ownrows=read('own_findings.jsonl')
for d in ownrows:
 if d['id']=='S45-ASTRA-R-0046':d.update(tex_reading='The lower final arrow is present in Miller and Codex.',change='No change.',kind='verification',reason='Rechecking the actual ar[r] token establishes that the suspected omission was a reading error during audit; the diagram already agrees with the scan.',verdict='rejected')
newowns=[
 dict(id='S45-ASTRA-R-0053',page='163',place='English description of the truncation',printed_reading=r"B'^1=Ker(d)",tex_reading='the degree-one term ker(d)',change='Restore the explicit notation B-prime superscript1 equals ker(d).',kind='translation',reason='The print gives the equality explicitly; preserving it avoids replacing authorial notation by paraphrase.'),
 dict(id='S45-ASTRA-R-0054',page='163',place='English image of e1 in H0',printed_reading=r'R^1pr_*G',tex_reading=r'R^1pr_{1*}G',change='Remove the unprinted projection index1 at this abbreviated occurrence.',kind='symbol',reason='Both the scan and French source abbreviate the projection here to pr; the English introduced an additional1.'),
 dict(id='S45-ASTRA-R-0055',page='162',place='English definition of G',printed_reading='au sous-schéma X×D',tex_reading='to the closed subscheme X×D',change='Remove the additional word closed.',kind='translation',reason='The English adds an adjective not present in the French statement; the subscheme is already specified.'),
 dict(id='S45-ASTRA-R-0056',page='154',place='Contents entry1, local page number',printed_reading='1',tex_reading='Contents omitted',change='Keep1 diplomatically; correct to2 with apparatus in both languages.',kind='misprint_in_print',reason='Section1 begins on printed155, whose original running local number is2, directly verified on the scan.'),
 dict(id='S45-ASTRA-R-0057',page='154',place='Contents entry4, local page number',printed_reading='12',tex_reading='Contents omitted',change='Keep12 diplomatically; correct to13 with apparatus in both languages.',kind='misprint_in_print',reason='Section4 begins on printed166, whose original running local number is13, directly verified on the scan.'),
 dict(id='S45-ASTRA-R-0058',page='154',place='Printed SGA references here and166',printed_reading='(SGA5 I5.1); SGA4 XVIII',tex_reading='Citation macros render automatically assigned numbers',change='Preserve each original cite key while displaying the printed reference through PrintCite.',kind='citation',reason='Running references give named SGA volumes and exposés. Both original citation keys are retained in the source.')]
existing={d['id']for d in ownrows}
ownrows.extend(d for d in newowns if d['id']not in existing)
write('own_findings.jsonl',ownrows)
patches=read('patches.jsonl');write('patches.jsonl',[p for p in patches if p['id']!='S45-ASTRA-R-0046'])
