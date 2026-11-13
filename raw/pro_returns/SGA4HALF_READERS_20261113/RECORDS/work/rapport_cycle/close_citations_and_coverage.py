from pathlib import Path
import json
P=Path(__file__).resolve().parent
def read(n):return [json.loads(l)for l in(P/n).read_text().splitlines()]
def write(n,a):(P/n).write_text(''.join(json.dumps(x,ensure_ascii=False)+'\n'for x in a))
citations={
 '2':{'de73':'[1]','gr95':'[2]','la83':'[3]','we48':'[4]',
      've67':'J.L. Verdier, the Lefschetz fixed point theorem in etale cohomology, Proc. of a conf. on Local Fields, Driebergen (Springer Verlag 1967)',
      'ba76':'Euler characteristics and characters of discrete groups, Inv. Math. 35 (1976) p. 155–196.',
      'sga4':'SGA 4','sga5':'SGA 5'},
 '3':{'do61':'(Homologie nicht additiver Funktoren. Anwendungen. Ann. Inst. Fourier XI 1961, p. 201–312)','sga4':'SGA 4','sga7':'SGA 7'},
 '4':{'bfm75':'(Riemann-Roch for singular varieties, Publ. Math. IHES 45 (1975) p. 101–146 – IV 4)','sga2':'SGA 2','sga4':'SGA 4','sga5':'SGA 5'},
 '5':{'sga4':'SGA 4','sga5':'SGA 5'}}
(P/'citation_display_map.json').write_text(json.dumps(dict(components=citations,notes=['Numbered references2/de73,gr95,la83,we48 are from the four-entry printed bibliography on109.','The ve67 and ba76 inline descriptions were rechecked directly on88 and90 and restored as PrintCite in both languages.','do61 and bfm75 are already restored as PrintCite in both languages.','Append the original optional cite postnote to SGA names or numbered references; do not introduce a global bibliography.','Citation keys remain in the second argument of PrintCite.']),ensure_ascii=False,indent=2))
restorations=[
 (59,88,'ve67',r'J.L. Verdier, the Lefschetz fixed point theorem in etale cohomology, Proc. of a conf. on Local Fields, Driebergen (Springer Verlag 1967)'),
 (60,90,'ba76',r'Euler characteristics and characters of discrete groups, Inv. Math. 35 (1976) p.~155--196')]
fr=json.loads((P/'supplement_fr_2.json').read_text());en=json.loads((P/'en_changes_2.json').read_text());own=read('own_findings.jsonl')
for num,n,key,literal in restorations:
 ident=f'S45-ASTRA-R-{num:04}';old=r'\cite{'+key+'}';new=r'\PrintCite{'+literal+'}{'+old+'}'
 if ident not in {x['id']for x in fr}:fr.append(dict(id=ident,page=n,old=old,new=new))
 if ident not in {x['id']for x in en}:en.append(dict(id=ident,page=n,old=old,new=new,ai_translated=True,reason='Restore the complete printed inline publication description, retaining its original English title.'))
 if ident not in {x['id']for x in own}:own.append(dict(id=ident,page=str(n),place='Inline bibliographic description',printed_reading=literal,tex_reading=old,change='Restore the full printed publication description through PrintCite in both languages, retaining the original cite key.',kind='missing',reason='The inline bibliographic wording is present in the directly re-opened scan. A bare citation key omits this authorial text and has no corresponding numbered local bibliography entry.'))
(P/'supplement_fr_2.json').write_text(json.dumps(fr,ensure_ascii=False,indent=2));(P/'en_changes_2.json').write_text(json.dumps(en,ensure_ascii=False,indent=2));write('own_findings.jsonl',own)

w={}
def put(ident,lang,status,reason,*needles,mode='corr'):
 w[ident+':'+lang]=dict(status=status,reason=reason,needles=list(needles),mode=mode)
put('S45-SOL-0335','fr','Codex repair verified at intended locus','The diagonal coefficient has exponent i; the source also retains the printed summation index i.',r'\sum_i f_i^i')
put('S45-SOL-0341','fr','restored passage verified with sourced variant','The full essential-image criterion is present; the separate0342 variant preserves the printed Lambda in diplomatic mode.',r'est formée des $(K,F)$ dans',r'\mathsf{DF}(\Lambda)$ tels que les',r'$\gr_F^p(\Lambda)$ soient',r'et presque tous nuls;',mode='dip')
put('S45-SOL-0343','fr','Codex repair verified at intended locus','The filtered object belongs to DF_parf. The later0344 unfiltered-category repair is already present in Codex and must not alter this occurrence.',r'si $(K,F)$ est dans $\mathsf{DF}_\text{parf}(\Lambda)$')
put('S45-SOL-0344','fr','Codex repair verified at intended locus','The lemma on unfiltered complexes already reads D_parf in Codex and remains so.',r'Pour que $K$ soit dans $\mathsf{D}_\text{parf}(\Lambda)$')
put('S45-SOL-0358','fr','Codex repair verified at intended locus','The exact bound is q<r, and the a fortiori clause is present; the comma follows the actual source typography.',r'$q<r$, a fortiori pour $p+q<r$')
put('S45-SOL-0321','fr','restored citation passage verified','The whole see-citation-and-definitive-version clause is present; the full inline Verdier reference has subsequently replaced its bare cite throughR0059.',r'(voir \PrintCite{J.L. Verdier',r'et la version définitive de \cite{sga5})')
put('S45-SOL-0321','en','restored citation passage verified','The entire translated clause is present, including the subsequently restored inline Verdier description.',r'(see \PrintCite{J.L. Verdier',r'and the definitive version of \cite{sga5})')
put('S45-SOL-0333','en','restored citation passage verified','The Bass introduction is present; R0060 then supplies the full inline article description.',r'Stallings and Hattori; cf. the recent article by H. Bass:',r'\PrintCite{Euler characteristics and characters of discrete groups')
for lang in ['fr','en']:
 put('S45-SOL-0382',lang,'restored formula verified after notation repair','The omitted intermediate trace is restored; own findingR0005 then restores the printed stars in the whole chain.',r'\tr\left(F^*,K^*\otimes\dQ_\ell\right) = \tr\left(F^*,K^*\right)')
put('S45-SOL-0535','fr','authorial marginal sign verified','The authorial exclamation mark is present; the later total-degree repair replaces its bullet by the scanned asterisk.',r'\marginpar{!}La définition de $\h^*(X,\sF)$ est la suivante:')
put('S45-SOL-0574','fr','numbered recall verified','The theorem environment has been replaced by the printed numbered Rappel; subsequent575/576 repairs separately restore separatedness and the source Y.',r'\subsubsection{Rappel}\label{IV:2-2-8}',r'Soit un morphisme de $S$-schémas séparés de type fini',r'Y \ar[r]^-i \ar[dr]_-f')
put('S45-SOL-0624','fr','arrow label verified after notation repair','The product dot is on the required arrow; total degrees subsequently use their printed stars.',r'\h^*(Y)\otimes \h^*(Y) \ar[r]^-{\cdot}')
put('S45-SOL-0625','fr','Hom order verified after notation repair','Hom has Y as source and X as target; total degrees subsequently use their printed stars.',r'\hom\left(\h^*(Y),\h^*(X)\right)')
put('S45-ASTRA-R-0003','en','method heading verified','The method letter B and corrected Nielsen spelling are both present.',r'\paragraph{B. Nielsen--Wecken}')
put('S45-ASTRA-R-0005','en','all degree signs verified','The first trace chain retains every scanned star, including the inserted term.',r'\h_c^*(X,\sG)',r'K^*\otimes\dQ_\ell',r'\tr\left(F^*,K^*\right)',r'K_n^*')
put('S45-ASTRA-R-0008','en','all degree signs verified','The four total-cohomology degree positions use stars.',r'\h_c^*(U,\dQ_\ell)',r'\h^*(X,\dQ_\ell)',r'\h^*(F,\dQ_\ell)')
put('S45-ASTRA-R-0010','fr','English-only target repair; French unchanged','The French already gives VI2.2 after naming SGA5; only the inherited English hyperlink targeted the wrong volume.',r'Jouanolou',r'VI 2.2')
put('S45-ASTRA-R-0017','en','all degree signs verified','All three groups in the composition use the scanned stars.',r'\h^*(\bar S,\bar\sG)',r'\h^*(\bar S,F^*\bar\sG)')
put('S45-ASTRA-R-0022','en','both degree signs verified','Both groups in the continued vanishing statement use the printed stars.',r'\h_c^*(Y\setminus 0,\dZ/2)',r'\h_c^*(\dA^1,\pi_*\dZ/2)')
put('S45-ASTRA-R-0024','fr','Codex repair verified at intended locus','The relevant lower arrow has one ar[r], as in Codex and the print.',r"F^*\bar\sG_0 \ar[r]^-{(\Phi^f)'}")
put('S45-ASTRA-R-0054','fr','English-only notation repair; French unchanged','The French already abbreviates this occurrence to pr without the unprinted1.',r'\h^0(X,\eR^1\pr_\ast\sG)')
(P/'coverage_witnesses.json').write_text(json.dumps(w,ensure_ascii=False,indent=2))
