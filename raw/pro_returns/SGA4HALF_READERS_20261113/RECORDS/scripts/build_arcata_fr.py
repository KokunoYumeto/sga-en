"""Build Arcata's annotated French component from observed decision records."""
from audit_support import *
OUT=ROOT/'work/arcata'
def readj(n):return [json.loads(l) for l in (OUT/n).read_text().splitlines()]
DEC=readj('decisions.jsonl');VAR=readj('variants.jsonl');PG=readj('pages.jsonl')
RAW={}
for d in DEC:
 s=SOL_BY_ID[d['id']]
 if not s['printed_page'].isdigit() or int(s['printed_page'])<6:continue
 data=json.loads((SOURCE/'check/sol'/f"{s['batch']}.json").read_text())
 m=[a for a in data if str(a.get('page'))==s['printed_page'] and a.get('where')==s['where'] and a.get('kind')==s['kind']]
 if len(m)==1 and m[0].get('fix'):RAW[d['id']]=m[0]['fix']
def matches(text,old):
 if not old.strip():return []
 pat=r'\s+'.join(re.escape(x) for x in re.split(r'\s+',old.strip()))
 if old.strip()[-1].isalnum():pat+=r'(?!\w)'
 if old.strip()[0].isalnum():pat=r'(?<!\w)'+pat
 return list(re.finditer(pat,text))
LOG=[]
text=(SOURCE/'fr/codex_dip/sga4.5-1.tex').read_text()
original=text
_before=(SOURCE/'fr/miller_src/sga4.5-1.tex').read_text().splitlines(True)
_after=original.splitlines(True)
_ops=difflib.SequenceMatcher(None,_before,_after,autojunk=False).get_opcodes()
BASE_PAGE={}
for _p in range(6,74):
 _a,_b=PAGES[str(_p)]['lines'];_a-=1;_covered=[]
 for _kind,_i,_j,_k,_l in _ops:
  if _j>_a and _i<_b:
   if _kind=='equal':_covered.extend(_after[_k+max(_a-_i,0):_k+min(_b-_i,_j-_i)])
   else:_covered.extend(_after[_k:_l])
 BASE_PAGE[str(_p)]=''.join(_covered)
def patch(old,new,page,ident,all=False,optional=False):
 global text
 ms=matches(text,old)
 if not ms:
  status='already present' if matches(text,new) else 'unmatched'
  LOG.append(dict(id=ident,page=str(page),status=status,before=old,after=new));return
 # A prefix of an already-applied replacement is not an outstanding old reading.
 ns=matches(text,new)
 ms=[m for m in ms if not any(n.start()<=m.start() and m.end()<=n.end() for n in ns)] if old!=new else ms
 if not ms:
  LOG.append(dict(id=ident,page=str(page),status='already present',before=old,after=new));return
 if not all and len(ms)>1:
  if str(page) in PAGES:
   target=PAGES[str(page)]['lines'][0]
   # Source line position is used only to distinguish already-reviewed identical strings.
   ms=[min(ms,key=lambda m:abs(text[:m.start()].count('\n')-target))]
  else:raise ValueError((ident,'ambiguous',old,len(ms)))
 for m in reversed(ms):text=text[:m.start()]+new+text[m.end():]
 LOG.append(dict(id=ident,page=str(page),status='applied',occurrences=len(ms),before=old,after=new))

skip={'S45-SOL-0006'}
vsrc={x for v in VAR for x in [v['id']]+v.get('sources',[])}
for d in DEC:
 p=d['printed_page']
 if not p.isdigit() or int(p)<6 or d['verdict']=='rejected' or d['id'] in vsrc or d['kind']=='misprint_in_print' or d['id'] in skip:continue
 old,new=d['fix_old'],d['fix_new']
 if d['id'] in RAW:
  s=SOL_BY_ID[d['id']]
  if old==s['fix_old']:old=RAW[d['id']]['old']
  if new==s['fix_new']:new=RAW[d['id']]['new']
 # These accepted readings are handled explicitly below because the reviewed
 # decision preserves original label names or spans several printed places.
 if d['id'] in {'S45-SOL-0054','S45-SOL-0199','S45-SOL-0201','S45-SOL-0204','S45-SOL-0205'}:continue
 if d['id'] in {'S45-SOL-0020','S45-SOL-0059','S45-SOL-0104','S45-SOL-0106','S45-SOL-0137','S45-SOL-0158','S45-SOL-0161','S45-SOL-0172','S45-SOL-0179','S45-SOL-0206','S45-SOL-0226'}:continue
 local=BASE_PAGE[p]
 oms=matches(local,old);nms=matches(local,new)
 oms=[m for m in oms if not any(n.start()<=m.start() and m.end()<=n.end() for n in nms)]
 if not oms and nms:
  LOG.append(dict(id=d['id'],page=p,status='verified in Codex page',before=old,after=new));continue
 if not oms and d['kind']=='extra':
  LOG.append(dict(id=d['id'],page=p,status='verified absent in Codex page',before=old,after=new));continue
 if not oms:
  LOG.append(dict(id=d['id'],page=p,status='unmatched',before=old,after=new));continue
 patch(old,new,p,d['id'])

# Shared repairs established by the independent full-page review.
patch(r'\sh(\et X)\to \sh(\et Y)',r'\sh_{\mathrm{Ab}}(\et X)\to \sh_{\mathrm{Ab}}(\et Y)',23,'S45-ASTRA-A-0009')
patch('Kunneth','Künneth',27,'S45-ASTRA-A-0010')
patch('résolution,est','résolution, est',65,'S45-ASTRA-A-0025')
patch('Etant donnés','Étant donnés',54,'S45-ASTRA-A-0019',all=True)
patch(r"{k'}^\times",r"{k'}^*",14,'S45-ASTRA-A-0005',all=True)
patch(r'\item (composition) Si $f:X\to S$',r'\item Si $f:X\to S$',19,'S45-ASTRA-A-0006')
patch(r"\item Si $f:X\to S$ et $g:Y\to S$ sont deux morphismes étales",r"\item (composition) Le composé de deux morphismes étales est un morphisme étale."+'\n'+r"  \item Si $f:X\to S$ et $g:Y\to S$ sont deux morphismes étales",19,'S45-SOL-0054')
patch(r"i'_*\dZ/n = {f'}^*i_*\dZ/n",r"i'_*\dZ/n = \dZ/n",55,'S45-ASTRA-A-0017;S45-SOL-0179')
for old,new in [(r'\sO_U^\times',r'\sO_U^*'),(r'\h^0(X,\sO_X)^\times',r'\h^0(X,\sO_X)^*'),(r'k^\times',r'k^*')]:
 patch(old,new,20,'S45-SOL-0059')
# These readings are already repaired in Codex using equivalent link/macro forms.
for ident,needle in [('0020',r'\hyperref[I:1-1]{1}'),('0104','La connaissance du groupe de Brauer'),('0106',r'\emph{Corps locaux} ou'),('0137',r'\hyperlink{cite.ega}{[EGA III, 4.1]}'),('0158',r'\hyperref[I:3-3-6]{(cf. III.3.6)}'),('0161',r'\an{}'),('0172',r'\hyperref[I:2-3-1]{(II 3.1.)}'),('0206','Prouvons 2.3.'),('0226',r'\hyperref[VII:1-1]{1.1}),')]:
 assert matches(text,needle),(ident,needle)
 LOG.append(dict(id='S45-SOL-'+ident,status='verified in Codex base',after=needle))
patch(r'\h^\bullet(X,\dZ/n)',r'\h^*(X,\dZ/n)',69,'S45-SOL-0229')
patch(r'\h_c^\bullet(X,\dmu_n)',r'\h_c^*(X,\dmu_n)',69,'S45-SOL-0229')
patch(r'\h_c^\bullet',r'\h_c^*',71,'S45-ASTRA-A-0027',all=True)

# Explicit displayed numbers and stable existing cross-reference labels.
for label,num in [('I:5-2-4','2.3.1'),('I:5-2-5','2.3.2'),('I:5-2-6','2.3.3')]:
 patch(r'\label{'+label+'}',r'\label{'+label+'}',60,'NUMBER-PRESENTATION-'+label)
 # The type-specific environment retains its original name; its printed number
 # is supplied by the common build layer's label-number map.
for a,b in [('6.2.3.1','2.3.1'),('6.2.3.2','2.3.2'),('6.3.1.1','1'),('6.3.1.2','2')]:
 patch(r'\tag{'+a+'}',r'\tag{'+b+'}',70 if '2.3' in a else 71,'S45-ASTRA-A-0026')
for lab,num in [('6-1','1'),('6-2','2'),('6-3','3'),('6-4','4'),('6-5','5'),("6-5'","5'"),("6-5''","5''")]:
 patch(r'\begin{equation}\label{I:eq:'+lab+'}',r'\begin{equation}\tag{'+num+r'}\label{I:eq:'+lab+'}',66,'NUMBER-PRESENTATION')

# Each true print error is restored into the first argument, even where Codex
# silently corrected it. Use the smallest complete text/math span.
variants=[
('SGA45-CORR-0004',10,'plat est surjectif','plat et surjectif','plat est surjectif'),
('S45-SOL-0027',10,'Pour toute famille','Pour toute famille finie','Pour toute famille'),
('S45-SOL-0033',12,r"M_U=\varphi^* M'",r"M_V=\varphi^* M'",r"M_U=\varphi^* M'"),
('S45-SOL-0035',13,r'\partial_0\partial_1',r'\partial_1\partial_0',r'\partial_0\partial_1'),
('S45-SOL-0038',14,r"v'\in V",r"v'\in V'",r"v'\in V"),
('S45-SOL-0045',16,'telle que','tel que','telle que'),
('S45-SOL-0057',20,r'\hyperref[I:1-6-6]{I.6.5}',r'\hyperref[I:1-6-6]{I.6.6}',r'I.\ref{I:1-6-6}'),
('SGA45-CORR-0008',22,'induit','induits','induit'),
('S45-SOL-0085',24,r'en $y$',r'en $\bar y$',r'en $\bar y$'),
('S45-SOL-0089',25,r'polynome $F$',r'polynôme $F$',r'polynôme $F$'),
('S45-SOL-0094',28,r'A_K',r"A_{K'}",r"A_{K'}"),
('S45-SOL-0103',30,r"(\bar K\otimes_K K')^*/\bar k^*",r"(\bar K\otimes_K K')^*/\bar K^*",r"(\bar K\otimes_K K')^*/\bar K^*"),
('S45-SOL-0114',32,r'g(X_{i j})',r'g(U_{i j})',r'g(X_{i j})'),
('SGA45-CORR-0011B',32,r'N_{K/k}',r'N_{K/k(X)}',r'N_{K/k}'),
('S45-SOL-0146',45,r'\prod_{p_{i*}} C_i',r'\prod p_{i*} C_i',r'\prod p_{i*} C_i'),
('S45-SOL-0154',49,r'\eR^q f_!',r'\eR^q f_! \sF',r'\eR^q f_! \sF'),
('SGA45-CORR-0014',49,r'\eR^q f_*(j_! \sF)',r'\eR^q \bar f_*(j_! \sF)',r'\eR^q f_*(j_! \sF)'),
('SGA45-CORR-0019',54,r'\h^0\left(X_t^x,\dZ/n\right)',r'\h^0\left(\widetilde X_t^x,\dZ/n\right)',r'\h^0\left(X_t^x,\dZ/n\right)'),
('SGA45-CORR-0021',59,'algèbres locales étale','algèbres locales étales','algèbres locales étale'),
('S45-ASTRA-A-0020',56,r'\h^*(X,\varepsilon_*\x27 \dZ/n)',r'\h^*(\widetilde X,\varepsilon_*\x27 \dZ/n)',r'\h^*(X,\varepsilon_*\x27 \dZ/n)'),
('S45-ASTRA-A-0021',45,r'$n$ un entier $\geqslant 0$',r'$n$ un entier $>0$',r'$n$ un entier $\geqslant 0$'),
('S45-SOL-0209',61,r'\widehat X=A\llbracket T\rrbracket',r'\widehat X=\spec A\llbracket T\rrbracket',r'\widehat X=A\llbracket T\rrbracket'),
('S45-SOL-0217',64,r'\dA_S^{n-1}',r'\dA_S^{N-1}',r'\dA_S^{n-1}'),
('S45-SOL-0244',70,'corps de classe géométrique','corps de classes géométrique','corps de classes géométrique'),
('S45-SOL-0248',70,r'Soient $X$ une variété',r'Soit $X$ une variété',r'Soient $X$ une variété'),
('S45-SOL-0257',72,'du paragraphe précédents','du paragraphe précédent','du paragraphe précédents')]
for ident,p,printed,corrected,old in variants:
 printed=printed.replace(r'\x27',"'");corrected=corrected.replace(r'\x27',"'");old=old.replace(r'\x27',"'")
 patch(old,r'\var{'+printed+'}{'+corrected+'}{'+ident+'}',p,ident)

# Numbering variant is a genuine duplicate printed number; the label stays6-6.
patch(r'\subsubsection{}\label{I:1-6-6}',r'\subsubsection*{\var{6.5}{6.6}{SGA45-CORR-0006}}\label{I:1-6-6}',17,'SGA45-CORR-0006')
patch('le le théorème',r'le \var{le }{}{SGA45-CORR-0015}théorème',49,'SGA45-CORR-0015')

# Include the scan-restored original foreword, local contents and bibliography.
opening=(SOURCE/'fr/codex_dip/opening.tex').read_text().replace('Inputs of étale','Inputs of etale')
toc=(SOURCE/'fr/codex_dip/toc-i.tex').read_text()
text=text.replace(r'\input{opening}',opening).replace(r'\input{toc-i}',toc)
text+='\n'+(OUT/'arcata_bibliography.tex').read_text()

# Independent propagation review, with an explicitly conjectural reference
# correction recorded as a variant rather than a silent transcription repair.
supplement=ROOT/'work/rapport_cycle/records/arcata_review_supplement.json'
if supplement.exists():
 for op in json.loads(supplement.read_text())['operations']:
  if op['language']=='fr':patch(op['before'],op['after'],op['page'],op['id'])

# Exact boundaries established from the scans. A marker inside a display is
# moved to its opening delimiter when the entire display starts the page.
anchors={int(p['printed_page']):p['start_fr'] for p in PG if p['printed_page'].isdigit() and 4<=int(p['printed_page'])<=75}
anchors.update({
 23:r'Le foncteur $f_*:',26:r'\[ \h^q(\et X,\sF)',28:r"d'équivalence. C'est ce groupe",30:r'\[\xymatrix{ 1 \ar[r] & \bar K^*',
 33:r'\begin{align*} \h^0(X,\dG_m)',34:r'\[ \h^q(X, j_* \dG_{m,\eta})',36:r"d'obtenir en corollaire la",
 38:r'de $P$ un $\dP_S^1$-schéma',41:r'$\Gamma(X,\sO_X)$ pour la topologie',42:r'\[ \operatorname{Rev.et}(X)',
 43:r"à $X_0'$.",44:r'sur $\cC$ à valeurs',46:r"que $n$ est une puissance d'un nombre premier",47:r'tel point, $t_0\in\sO_{X_0,x}$',
 49:r'\var{le }{}{SGA45-CORR-0015}théorème',53:r'\[ \cosp^* : \h^*(X_t,\dZ)',
 55:r"\[\xymatrix{ X_t \ar[r]^-{\varepsilon'} \ar[d]",58:r'point géométrique $t$ de $S$',
 64:r'\begin{equation*}\tag{3.4.1}',67:r'\begin{equation}\tag{3}\label{I:eq:6-3}',68:r"\begin{equation}\tag{5'}\label{I:eq:6-5'}",
 70:r'\item La suite exacte $0\to j_!\dmu_n',72:r'\[ \h^i(f^{-1}(z),\dZ/n)',
 74:r'\section*{Bibliographie}',75:r'\item[{[12]}]'
})
cursor=0;resolved={}
for p,anchor in sorted(anchors.items()):
 ms=[m for m in matches(text,anchor) if m.start()>=cursor]
 if not ms:LOG.append(dict(page=str(p),status='marker unmatched',before=anchor));continue
 m=ms[0];pos=m.start()
 if text[pos:].startswith('\\item '):pos+=6
 # Avoid putting page markers between TeX command and its parameters.
 text=text[:pos]+f'\\PrintPage{{{p}}}'+text[pos:];cursor=pos+len(f'\\PrintPage{{{p}}}')
 resolved[str(p)]=anchor
for p in PG:
 if p['printed_page'] in resolved:p['start_fr_resolved']=resolved[p['printed_page']];p['fr_marker_present']=True
(OUT/'fr/sga4.5-1.tex').write_text(text)
(OUT/'fr_build.json').write_text(json.dumps(LOG,ensure_ascii=False,indent=2))
(OUT/'page_anchors_fr.json').write_text(json.dumps(resolved,ensure_ascii=False,indent=2))
print(json.dumps({'operations':len(LOG),'unmatched':[x for x in LOG if x['status']=='unmatched' or 'marker unmatched'==x['status']],'markers':len(resolved)},ensure_ascii=False,indent=2))
