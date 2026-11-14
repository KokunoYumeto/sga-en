#!/usr/bin/env python3
"""Opening IX pages, personally compared in both complete source images."""
import re
from review_helpers import Review,base_text
r=Review()
obs0={
12:('EXPOSÉ IX; QUELQUES CALCULS DE GROUPES K, with plain K','Both complete498 images show the separate exposé heading and capital title, with one and two rules respectively. Its K has no dot. Retain the attached heading, with the accepted capital-accent and spacing transport.','Heading',498),
13:('par P.BERTHELOT, underlined','Both complete498 images show the capital author name and its single rule. Retain the attached author line.','Author line',498),
14:('Proposition1.1. followed by the parenthetical title','Both complete498 images show the stop after1.1. Retain it under the accepted statement-label typesetting convention.','Proposition1.1 label',498),
15:('Suite exacte d’homotopie, with capital S','Both complete498 images show the capital in the label and the lower-case s in the preceding running-text reference. Retain those occurrence-specific forms.','Proposition1.1 label and earlier reference',498),
16:('Separate word-group rules in1.1–1.2','Both complete498–500 image pairs show the individual statement word rules. Restore precisely these groups; the word plat in1.2 remains plain, as printed. Formula letters and punctuation receive only their separately observed treatment.','Statements1.1 and1.2',498),
17:('Thirty-seven ruled module/ideal letters on499 and fourteen on500','The complete primary/native499 and500 images show the specified single rules, covering only each letter and leaving primes outside. Restore F20,G6,H4,K4,I3 on499 and F5,G6,H1,K1,I1 on500. The group K letters, index-set I and Roman I of EGA I stay as independently read. The class map F↦[F] sends each coherent sheaf to the source K group; the ideal inclusion I→O_X and its multiplication actions are preserved by identity on sections.','All module/ideal occurrences499–500',499),
18:('une suite exacte de O_U-Module cohérents','Both complete500 images omit the plural s in Module, while the same phrase has plural cohérents and the displayed sequence has the three modules G-prime,G,G-double-prime. Current adds only the noun’s plural s. The objects and exact maps0→G-prime→G→G-double-prime→0 remain identical.','Proof of1.1, additive extension map',500),
19:('deux schémas noethérien','Both complete500 images omit the final s in the adjective and print a following comma. Current adds only that s, agreeing with the two named schemes X,S; the asserted noetherian property of each is unchanged.','Proposition1.2 opening',500),
20:('par l’homomorphisme:, with a colon','Both complete500 images show that colon introducing the comparison map. Retain the attached restoration.','Proposition1.2, last display',500),
21:('Four K letters with a filled raised dot','Both complete500 images show a filled raised dot at the four occurrences naming the locally-free/perfect K group. Restore K-bullet at the raised position. The following comparison sends the class of a locally free sheaf E to its coherent-sheaf class; the action on a coherent F is[E]·[F]=[E tensor F]. This records the source’s own morphism between the two notations and keeps the lower dots of the coherent groups.','Four raised K dots in1.2',500),
}
for k,(p,w,g,f) in obs0.items():
 r.finding('496_500',k,p,w,g,witness=f+11,actual_page=f,verdict='not applied and now applied' if k in [16,17,18,19,21] else 'confirmed')
obs1={
1:('A comma after K-dot(X_U)','Both complete501 images show the comma; the native image resolves its tail without an upper semicolon dot. Retain the attached comma.','First paragraph',501),
2:('No punctuation after the lower-row zero','Both complete501 images end the diagram’s lower row at0. Retain the absence of a comma.','Diagram1.2.1',501),
3:('A new indented paragraph begins Soit(x-prime_i)','Both complete501 images show this paragraph boundary after the commutative-square sentence. Retain it.','Before the two projection-formula displays',501),
5:('501 ends car i est propre et f plat.;502 begins Soit(x_i)','Both complete501/502 source pairs place the entire proper/flat phrase on501 and start502 with Soit. Retain the marker and paragraph break at that exact boundary.','Boundary501/502',502),
6:('No punctuation after j*(x_i)','Both complete502 images show no comma at the end of the second display. Retain the attached omission.','Second display',502),
7:('A comma after the lower-right K-dot(X)','Both complete502 images show the comma beside the reduced-base diagram. Retain it.','Reduced-base diagram',502),
8:('A new indented paragraph begins Soit y','Both complete502 images show this boundary after O_(S,s)=K. Retain it.','Last paragraph',502),
}
for k,(p,w,g,f) in obs1.items():r.finding('501_505',k,p,w,g,witness=f+11,actual_page=f)
for row in r.decisions:
 if row.get('kind')=='misprint_in_print' or row['type']=='misprint':row.update(is_misprint=True,correction_status='accepted paired agreement correction')
r.patch(500,'current',r'$\mathcal O_U$-Module cohérents',r'$\mathcal O_U$-Modules cohérents','check/findings/findings_496_500.json#18',obs0[18][1])
r.patch(500,'current','deux schémas noethérien,','deux schémas noethériens,','check/findings/findings_496_500.json#19',obs0[19][1])

def current(p,layer):
 t=base_text(p,layer)
 for x in r.patches:
  if x['page']==p and x['layer'] in ['both',layer]:
   assert t.count(x['old'])==x['expected_count'],(p,layer,x['source_id']);t=t.replace(x['old'],x['new'])
 return t
for p in [498,499,500,502]:
 id=f'ASTRA-IX-GLYPHS-{p}'
 why=('Both complete primary/native images show the single lower rules of the ordinary structure-sheaf O at every listed occurrence. Restore only the letter rule, with subscripts outside. The same sheaf of regular functions and its identity on local sections give the comparison with the former mathcal O rendering. '+(obs0[17][1] if p in [499,500] else ''))
 r.own_finding(id,p,'Individually ruled sheaf and module letters','mathcal O and plain module/ideal letters','Restore the observed single rules.',why,'Sheaf and module notation',kind='font',witness=p+11)
 for layer in ['diplomatic','current']:
  old=current(p,layer);s=old
  assert s.count(r'\mathcal O')=={498:1,499:5,500:4,502:1}[p]
  s=s.replace(r'\mathcal O',r'\underline{O}')
  if p in [499,500]:
   b=s.index(r'\textbf{Proposition 1.2.}') if p==500 else len(s)
   part=s[:b];counts={}
   for letter in ['F','G','H','K']:
    pattern=r'(?<![A-Za-z\\])'+letter+r'(?![A-Za-z]'+(r'|_\\bullet' if letter=='K' else '')+')'
    part,n=re.subn(pattern,lambda m:r'\underline{'+m[0]+'}',part);counts[letter]=n
   part,n=re.subn(r'(?<![A-Za-z\\])I(?=[\^$])',lambda _:r'\underline{I}',part);counts['I']=n
   assert counts=={499:{'F':20,'G':6,'H':4,'K':4,'I':3},500:{'F':5,'G':6,'H':1,'K':1,'I':1}}[p],(p,counts)
   s=part+s[b:]
  r.patch(p,layer,old,s,id,why)
 r.own[-1]['observed_rule_counts']={498:{'O':1},499:{'O':5,'F':20,'G':6,'H':4,'K':4,'I':3},500:{'O':4,'F':5,'G':6,'H':1,'K':1,'I':1},502:{'O':1}}[p]

for p,n in [(500,4),(501,2)]:
 id=f'ASTRA-IX-RAISED-K-{p}';why=obs0[21][1]+f' The{n} occurrences on{p} were each read in both complete source images.'
 r.own_finding(id,p,f'{n} filled raised K dots',r'K^\circ','Restore the raised bullet in both forms.',why,'Raised K dots',kind='symbol',witness=p+11)
 r.patch(p,'both',r'K^\circ',r'K^{\bullet}',id,why,count=n)

def rules(t,phrases):
 pat='(?<![A-Za-zÀ-ÿ])('+'|'.join(re.escape(s).replace(r'\ ',r'\s+') for s in sorted(phrases,key=len,reverse=True))+')(?![A-Za-zÀ-ÿ])'
 return re.sub(pat,lambda m:r'\uline{'+m[0]+'}',t)
for p in [498,499,500]:
 id=f'ASTRA-IX-WORD-RULES-{p}';why=obs0[16][1]
 r.own_finding(id,p,'Separate statement word-group rules','Plain statement prose','Restore the individual word groups.',why,'Statements1.1–1.2',witness=p+11)
 for layer in ['diplomatic','current']:
  old=current(p,layer);s=old
  if p==498:
   a=s.index(' Soient $X$')
   s=s[:a]+rules(s[a:],['Soient','un schéma noethérien','un sous-schéma fermé de',"l'ouvert complémentaire de",'dans',"l'immersion de",'et','Alors la suite'])
  elif p==499:
   a=s.index('est\nexacte');s=s[:a]+rules(s[a:a+len('est\nexacte')],['est exacte'])+s[a+len('est\nexacte'):]
  else:
   a=s.index(r'\textbf{Proposition 1.2.}')+len(r'\textbf{Proposition 1.2.}')
   s=s[:a]+rules(s[a:],['Soient','deux schémas noethériens','deux schémas noethérien','et','un morphisme','de','dans',"On se donne une famille d'éléments",'et on considère',"l'homomorphisme",'défini par','où',"est l'homomorphisme",'image inverse',"défini d'après",'et où','est considéré comme','-module par','On suppose que pour tout point','les images des','par','engendrent','comme groupe abélien','Alors','est surjective'])
  assert s!=old;r.patch(p,layer,old,s,id,why)

id='ASTRA-IX-PRODUCT-DOTS-499-502'
why='The complete primary/native images499–502 were personally read. The11 observed multiplication dots(2 on499,1 on500,3 on501,5 on502) retain the cdot typesetting already used for the corresponding products in VIII and XIII. On499, the operators are the ideal actions I^m tensor H→H and I^n tensor K→K,a⊗h↦ah. On500–502 they are the K action induced by a locally-free E and coherent F↦E tensor F, and finally the additive integer action n·[E]. The displayed dot represents that same bilinear operation, with the identical factors and order; no multiplication is added or removed. This is the occurrence-scoped IX supplement to findings_496_500.json#6; its historical source row remains uniquely owned by the VIII review.'
r.own_finding(id,499,'Typed product dots in the displayed actions',r'\cdot','Retain the explicit product-dot typesetting convention in both forms.',why,'Two ideal products499; K-action displays500–502',kind='symbol',verdict='confirmed',witness=510)
r.own[-1].update(related_finding='check/findings/findings_496_500.json#6',source_pages=[499,500,501,502],observed_occurrences={499:2,500:1,501:3,502:5},is_misprint=False,correction_status='Explicit product-symbol typesetting convention')
id='ASTRA-IX-LOWER-K-498-502'
why='Every complete primary/native page498–502 was personally compared. The coherent-sheaf group K has a lower dot throughout, while the title and the two category-group mentions on498 have plain K. Retain those attached occurrences. The four raised dots on500 and two on501 are separately restored. The source comparison sends the locally-free class[E] to its coherent class[E], and its tensor action sends([E],[F]) to[E tensor F]; these explicit maps retain the source relationship while preserving both printed dot positions.'
r.own_finding(id,498,'Lower dots on the coherent-group K; plain K in the title/category mentions','Same lower/plain forms','Retain those forms and the separately recorded raised-dot restoration.',why,'All K notation498–502',kind='symbol',verdict='confirmed',witness=509)
r.own[-1]['is_misprint']=False
for p,a,b in [(498,'EXPOSÉ IX; QUELQUES CALCULS DE GROUPES K','Alors la suite:'),(499,'K-dot(X-prime)→K-dot(X)→K-dot(U)→0','On peut donc dévisser H et K en extensions de Modules'),(500,'annulés par I,donc de O_(X-prime)-Modules','Alors varphi est surjective.'),(501,'Soient S-prime un sous-schéma fermé de S','car i est propre et f plat.'),(502,'Soit(x_i)_(i∈I)∈K-dot(S)^(I);on a:','y_s=sum_i xi_i·n_i.')]:
 r.page(p,a,b,notes='Complete primary/native page personally compared. Aggregate finding501_505#4 will be closed after its remaining503–504 occurrences are read; the two501 raised dots are already individually recorded. Historical HOLD53–56 are nominally in this range but belong to the later source text and are not re-adjudicated here.',witness=p+11)
r.commit()
