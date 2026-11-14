#!/usr/bin/env python3
"""Explicit primary/native image decisions406–410, with native glyph crops."""
import json,re
from review_helpers import Review,base_text,read
r=Review();batch='406_410';earlier={x['source_id']:x for x in read('decisions.jsonl')}
obs={}
for k,previous in [(1,37),(2,38),(3,39)]:
 v=earlier[f'check/findings/findings_401_405.json#{previous}']
 obs[k]=(v['printed_reading'],v['reason'],v['region'],406)
obs.update({
4:('d’où les relations cherchées, without a final stop','Both complete406 images end this short concluding phrase without a period. Its referent is fully specified by the displayed equality bar f_*(lambda_t(F))=1: applying the coefficient map [t^i] gives f_*(lambda^i(F))=0 for i≥1. The sentence boundary is fixed by the following Proposition5.10 heading. Retain the source closure in both forms instead of supplying editorial terminal punctuation.','Conclusion of5.9 proof',406),
5:('No punctuation after z=sum a_i(x-prime)^i','Both complete406 images show the expansion without a terminal period. Retain the attached omission.','Expansion of z',406),
6:('Individually read statement word groups','Every statement and continuation on406–410 was read in both complete source images. Restore only the observed prose word rules. Formula symbols, punctuation, reference numbers and the i),ii) labels remain plain; projectif and noethérien in6.4 are individually underlined.','Statements5.10,5.11,6.1–6.4',406),
7:('407 begins Donc:','Both complete406/407 source pairs place the a_r coefficient relations at the end of406 and Donc: at the beginning of407. Retain the attached marker before Donc, outside the following display.','Boundary406/407',407),
8:('gamma^r(F−x-prime)','Both complete407 images print F−x-prime. The preceding expression is E−r−1−x-prime. In the displayed K ring, substitution E=F+xi and x-prime=xi−1 gives E−r−1−x-prime=F−r exactly. Thus current retains F−r. The next equality is verified by [t^r]((1−t)^r lambda_(t/(1−t))(F))=sum_(j=0)^r(−1)^(r−j)lambda^j(F)=lambda^r(F−1); multiplication by(−1)^r gives lambda_-1(F). Diplomatic retains the printed x-prime.','Long gamma-series display',407),
9:('Occurrence-specific sheaf and class rules','Both complete primary/native images were read for each page. Ruled sheaf occurrences are:407 L once;408 E twelve times,L three times,O four times;409 the first E_i once;410 E once. The other E,L,E_i denote the printed classes and remain plain. The source class maps E↦[E],L↦[L],E_i↦[E_i] explicitly connect the ruled inputs to those plain outputs. Underlines cover only each letter, leaving stars, tensor powers and indices outside.','All sheaf/class occurrences407–410',407),
10:('408 begins epsilon l’homomorphisme','Both complete407/408 pairs place On note at the end of407 and epsilon at the start of408. Retain the attached marker before epsilon, with l’homomorphisme unbroken.','Boundary407/408',408),
11:('Struck Z with a lower sheaf rule','Both complete408 images show the struck coefficient Z with an additional lower rule. Retain underline(mathbb Z) in the first H^0. The map n↦the constant local section n specifies this coefficient sheaf and preserves its ring of constant sections.','First line, augmentation target',408),
12:('Struck Z with a lower sheaf rule','Both complete408 images show the same ruled struck Z in the second H^0. Retain underline(mathbb Z), with the same constant-section map n↦n.','Proof, augmentation target',408),
13:('finies permet de se ramener','Both complete408 images print the singular permet. The grammatical subjects are the two coordinated nouns quasi-compacité and commutation. Current retains permettent, preserving the source argument: the finitely many rank loci are clopen, and restriction K(X)→product K(X_n) has inverse the sum of extensions by zero. No hypothesis or mathematical operation changes.','First proof paragraph',408),
14:('d’éxistence','Both complete408 images show the acute mark above the first e. Current retains existence without that accent, naming the same ample-sheaf existence hypothesis; diplomatic keeps the observed accent.','First proof paragraph, last lines',408),
15:('Ruled struck Z in H^0; unruled struck Z elsewhere','Both complete409 images show the lower rule only in H^0(X,Z); the coefficient ring Z in vers Z, the polynomial ring and Z-module has no lower rule. Retain those exact readings. The constant-section map Z→H^0(X,Z),n↦n, supplies the comparison used by the stated augmentation.','Corollaire6.2 and subsequent coefficient rings',409),
16:('No comma after x_i before soumis','Both complete409 images have no comma at this position. Retain the attached omission.','Second proof paragraph',409),
17:('c’êst-à-dire, with a small peaked mark on e','The complete409 images and the enlarged native409_accent and main409_accent crops show a short upward-peaked mark, rather than a legible acute stroke, above e. Diplomatic represents that observed shape by ê; the glyph’s intended accent is not reconstructed. Current retains unaccented est in the explanatory c’est-à-dire, with all surrounding mathematical terms unchanged. This amends the checker’s acute-accent transcription while confirming the paired removal of the erroneous accent.','Polynomial-ring explanation',409),
18:('Two stacked index ranges without comma','Both complete409 images and the native crop show1≤i≤k above2≤j≤r_i, with no separating comma. Retain the attached substack.','Polynomial-ring index',409),
19:('Three baseline stops in1+...+m','Both complete409 images show the low typed stops. Retain ldots.','Nilpotence bound',409),
20:('Ruled A in H^0(X,A)','Both complete410 images show a rule under the coefficient sheaf A; the ring A and Id_A elsewhere are plain. Retain exactly this rule. The map A→H^0(X,A),a↦the constant local section a, specifies the comparison.','Corollaire6.4 hypothesis',410),
})
for k,(p,w,g,f) in obs.items():
 r.finding(batch,k,p,w,g,witness=f+11,actual_page=f,verdict='reverted' if k==4 else 'amended' if k==17 else 'not applied and now applied' if k in [6,9] else 'confirmed')
for row in r.decisions:
 key=row.get('related_finding',row['source_id'])
 if row.get('kind')=='misprint_in_print' or row['type']=='misprint':row.update(is_misprint=key!=f'check/findings/findings_{batch}.json#4',correction_status='Source terminal punctuation retained' if key==f'check/findings/findings_{batch}.json#4' else 'accepted paired correction')
 if key==f'check/findings/findings_{batch}.json#4' and row['type']=='fixlog':row.update(verdict='confirmed',change='Retain the diplomatic restoration; remove the unsupported current final stop.')
for n,k in [(433,8),(434,13),(435,14),(436,17)]:
 p,w,g,f=obs[k];r.source(f'fixes/FIXLOG_6_CURRENT.jsonl#{n}',p,w,g,witness=f+11,change='Retain the paired current correction; the diplomatic accent shape on409 is separately amended.')
 r.decisions[-1].update(is_misprint=True,correction_status='accepted paired correction')
r.patch(406,'current',"d'où les relations cherchées.","d'où les relations cherchées",f'check/findings/findings_{batch}.json#4',obs[4][1])
r.patch(409,'diplomatic',"c'ést-à-dire","c'êst-à-dire",f'check/findings/findings_{batch}.json#17',obs[17][1])

id='ASTRA-VI-STRAY-STOP-409';why='Both complete409 images and native409_permet.png show a separate stop after permet. The source verb governs the immediately following de se ramener, with alors between them; the stop cuts that same verbal construction. Diplomatic restores the observed period, while current retains the uninterrupted permet alors de se ramener. The reduction itself is the displayed restriction to the finite clopen rank partition, with inverse extension by zero.'
r.own_finding(id,409,'L’argument standard permet. alors','L’argument standard permet alors','Restore the source period only in diplomatic.',why,'First proof paragraph',kind='misprint_in_print',witness=420)
r.own[-1].update(is_misprint=True,correction_status='accepted paired stray-stop correction')
r.patch(409,'diplomatic',"L'argument standard permet alors","L'argument standard permet. alors",id,why)

# Resolve the two historical HOLD records at their actual source location408.
r.source('fr/codex/HOLD_VS_CORR.json#39','permet; d’éxistence',obs[13][1]+' '+obs[14][1],'408 first proof paragraph',page=408,witness=419,change='Retain both paired current corrections; preserve both source readings diplomatically.')
why='Both complete408 images print son produit L^n−E par L^n. The multiplication map mu_(L^n):K(X)→K(X),a↦L^n a, sends1−EL^(−n) exactly toL^n−E; its inverse is multiplication byL^(−n). Thus L^n−E can be read as the named product in the source apposition. The proposed reordering changes prose without repairing the product or its nilpotence. Retain the source wording in both forms and confirm rejection of that rewording.'
for id in ['fr/codex/HOLD_VS_CORR.json#40','fixes/RECONCILE_CODEX_6.json:entries#239','fixes/RECONCILE_CODEX_6.json:entries#321']:
 r.source(id,'son produit L^n−E par L^n',why,'408 penultimate paragraph',page=408,witness=419,change='Retain the printed wording in both layers; reject the proposed reordering.')
 r.decisions[-1].update(is_misprint=False,correction_status='Author apposition retained')

def current(p,layer):
 t=base_text(p,layer)
 for x in r.patches:
  if x['page']==p and x['layer'] in ['both',layer]:
   assert t.count(x['old'])==x['expected_count'],(p,layer,x['source_id']);t=t.replace(x['old'],x['new'])
 return t
for p in [407,408,409,410]:
 id=f'ASTRA-VI-GLYPHS-{p}';why=obs[9][1]
 r.own_finding(id,p,'Individually observed sheaf rules','Plain sheaf letters','Restore the listed rules, retaining class letters plain.',why,'Sheaf/class notation',kind='font',witness=p+11)
 for layer in ['diplomatic','current']:
  old=current(p,layer);s=old.replace(r'\mathcal O',r'\underline{O}')
  if p==407:pairs=[('un faisceau ample $L$',r'un faisceau ample $\underline{L}$')]
  elif p==408:
   pairs=[('un faisceau ample $L$',r'un faisceau ample $\underline{L}$'),('type fini $E$,',r'type fini $\underline{E}$,'),('où $E$ est de rang',r'où $\underline{E}$ est de rang'),('fibré de drapeaux de $E$',r'fibré de drapeaux de $\underline{E}$'),('supposer $E$ inversible',r'supposer $\underline{E}$ inversible'),('le dual de $E$',r'le dual de $\underline{E}$'),('la classe de $L$',r'la classe de $\underline{L}$'),('faisceau inversible $E$',r'faisceau inversible $\underline{E}$')]
   a=s.index('Soit $E^*$');b=s.index('Le noyau',a);part=s[a:b]
   part,n=re.subn(r'(?<![A-Za-z\\])E(?![A-Za-z])',lambda _:r'\underline{E}',part);assert n==7,n
   part=part.replace(r'L^{\otimes n}',r'\underline{L}^{\otimes n}');s=s[:a]+part+s[b:]
   pairs=[x for x in pairs if x[0]!='le dual de $E$']
  elif p==409:pairs=[('Soient $E_i$,',r'Soient $\underline{E}_i$,')]
  else:pairs=[('si $E$ est un faisceau',r'si $\underline{E}$ est un faisceau')]
  for a,b in pairs:assert s.count(a)==1,(p,a);s=s.replace(a,b)
  assert s!=old;r.patch(p,layer,old,s,id,why)
 r.own[-1]['observed_rule_counts']={407:{'L':1},408:{'E':12,'L':3,'O':4},409:{'E':1},410:{'E':1}}[p]

def rules(t,phrases):
 pat='(?<![A-Za-zÀ-ÿ])('+'|'.join(re.escape(s).replace(r'\ ',r'\s+') for s in sorted(phrases,key=len,reverse=True))+')(?![A-Za-zÀ-ÿ])'
 return re.sub(pat,lambda m:r'\uline{'+m[0]+'}',t)
for p in range(406,411):
 id=f'ASTRA-VI-WORD-RULES-{p}';why=obs[6][1]
 r.own_finding(id,p,'Observed word-group rules','Plain statement prose','Restore only those word-group rules.',why,'Statement prose',witness=p+11)
 for layer in ['diplomatic','current']:
  old=current(p,layer);s=old
  if p in [406,407]:
   label='Proposition '+('5.10.' if p==406 else '5.11.')
   a=s.index(r'\textbf{'+label+'}')+len(r'\textbf{'+label+'}');b=s.index('De $E=F',a) if p==406 else s.index('La démonstration',a)
   s=s[:a]+rules(s[a:b],['Avec les notations et les hypothèses de','soit','Pour que',"il faut et il suffit qu'il existe",'tel que'])+s[b:]
  elif p==408:
   a=s.index(r'\textbf{Proposition 6.1.}')+len(r'\textbf{Proposition 6.1.}');b=s.index('Comme',a)
   s=s[:a]+rules(s[a:b],['Soit','un schéma quasi','compact ayant un faisceau ample','Alors','est un nilidéal'])+s[b:]
  elif p==409:
   a=s.index(r'\textbf{Corollaire 6.2.}')+len(r'\textbf{Corollaire 6.2.}');b=s.index('Comme',a)
   s=s[:a]+rules(s[a:b],['Avec les hypothèses de','soit','un sous',"anneau engendré par les classes d'un nombre fini de faisceaux",'Alors la filtration de','anneau de','est discrète','et','est nilpotent','De plus','est un module de type fini sur'])+s[b:]
  else:
   a=s.index(r'\textbf{Corollaire 6.3.}')+len(r'\textbf{Corollaire 6.3.}');b=s.index("L'idéal d'augmentation",a)
   s=s[:a]+rules(s[a:b],['Avec les hypothèses de','soit','un anneau commutatif',"Pour qu'un élément",'de','soit inversible','il faut et il suffit que','le soit','En particulier','si','est un faisceau localement libre de type fini sur','partout','alors sa classe dans','est inversible'])+s[b:]
   a=s.index(r'\textbf{Corollaire 6.4.}')+len(r'\textbf{Corollaire 6.4.}');b=s.index('On écrit la formule',a)
   s=s[:a]+rules(s[a:b],['Soient','un schéma quasi','compact','ayant un faisceau ample','et','un morphisme propre et parfait',"On suppose de plus vérifiée l'une des deux conditions suivantes",'projectif','noethérien','de façon que le','théorème de finitude','soit vrai','On se donne un anneau',"on considère l'homomorphisme",'image directe',"On suppose enfin qu'il existe un élément",'tel que','soit inversible',"Alors l'homomorphisme",'est injectif'])+s[b:]
  assert s!=old;r.patch(p,layer,old,s,id,why)

id='ASTRA-VI-RATIONAL-Q-410';why='Both complete410 images and native410_Q.png show an added vertical stroke inside the rational coefficient Q. Retain the attached mathbb Q under NOTE6. The rationalization map K(X)→K(X) tensor_Z Q,a↦a tensor1, is unchanged; the capital Id in epsilon tensor Id_A also matches the source macro expansion.'
r.own_finding(id,410,'Struck Q in K(X)_Q and capital Id_A','Same rendered forms','Retain both layers.',why,'Corollaire6.3',kind='font',verdict='confirmed',witness=421)
for p,a,b in [(406,'bar f(lambda_t(F))=','a_r c_0=0; pour0≤i<r,a_i=a_r c_(i+1).'),(407,'Donc:','On note'),(408,'epsilon l’homomorphisme d’augmentation','Donc E−1 est nilpotent.'),(409,'Corollaire6.2.','ce qui achève la démonstration.'),(410,'Corollaire6.3.','Par suite, l’homomorphisme composé:')]:
 r.page(p,a,b,notes='Both complete primary/native pages personally compared. Native crops additionally resolve the409 peaked accent and stray stop and the410 struck rational Q. Historical HOLD39–40 are assigned to their actual408 location.',witness=p+11)
r.commit()
