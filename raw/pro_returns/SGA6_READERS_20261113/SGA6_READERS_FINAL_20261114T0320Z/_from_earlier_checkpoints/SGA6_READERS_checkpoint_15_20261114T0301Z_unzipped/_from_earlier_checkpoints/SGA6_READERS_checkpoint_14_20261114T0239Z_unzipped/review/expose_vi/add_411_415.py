#!/usr/bin/env python3
"""Final five VI folios: complete primary/native comparisons and exact proofs."""
import json,re,shutil
from pathlib import Path
from review_helpers import Review,base_text
r=Review();batch='411_415'
obs={
1:('Les K-dot(X)_i ainsi définis sont, without either comma','Both complete411 images show the phrase without either comma. Retain the attached restoration.','Paragraph after6.5(ii)',411),
2:('A new indented paragraph begins Les','Both complete411 images show that paragraph boundary after6.5(ii). Retain it.','Paragraph after6.5(ii)',411),
3:('A new indented paragraph begins On a alors','Both complete411 images show this boundary after the codimension display. Retain it.','Proof of6.6',411),
4:('A struck L, with a doubled stem and no lower rule','Both complete411 images show the doubled vertical stem of the derived-tensor L. Retain mathbb L. This denotes the same derived tensor functor; on bounded locally free representatives it is computed by the same total tensor complex and identity comparison.','Derived tensor in6.6 proof',411),
5:('La filtration5.5','Both complete411 images print5.5. The immediately preceding6.5 defines the filtration K-dot(X)_i used in6.6;5.5 concerns the flag-scheme lambda presentation and supplies no such filtration. The locator map sends the displayed definition to6.5. Retain5.5 diplomatically and6.5 currently.','Proposition6.6',411),
6:('Individually ruled statement word groups','Both complete primary/native images of411–413 show separate rules under the statement word groups. Restore those precise prose groups, keeping formula symbols, numbers and punctuation independently as printed.6.5 is a plain paragraph number; the statement labels follow the accepted NOTE6 label convention.','6.6–6.9',411),
7:('Occurrence-specific sheaf, complex and class notation','Every occurrence was read on the complete primary/native images. Restore the rules under27 complex M letters and one ample L on411;9 complex M,10 sheaf E,one L and two O on412;15 sheaf E,five L and one O on413;four complex N,two L,two sheaf E in the complex and three pairs E_i,F_i in the rank/flag-sheaf phrases,plus one O on414. The module M=Gamma(X,E) on412 and the explicitly named K classes stay plain. The source class map E↦[E], and its analogous maps for F,L and complexes, connect the ruled inputs to those plain class values. Rules cover only the letters.','All sheaf/complex/class occurrences411–414',411),
8:('411 ends(EGA0_IV14.2.2.3).;412 begins Il suffit donc','Both complete411/412 source pairs confirm that Il is the first word on412. Retain the attached marker before Il.','Boundary411/412',412),
9:('A struck derived-tensor L','Both complete412 images show the doubled stem and no lower rule, matching411. Retain mathbb L with the bounded-free total-tensor comparison described for finding4.','First display',412),
10:('A new indented paragraph begins Pour montrer','Both complete412 images show the paragraph boundary after the support display. Retain it.','Second paragraph',412),
11:('et Y=X il existe, without a separator after X','Both complete412 images show no stop or semicolon here. The specialization to Y=X is the identity closed immersion X→X, and the following existence statement applies6.5 to that same closed subscheme. Supplying a semicolon changes punctuation without changing that mathematical operation. Retain the source punctuation in both forms and remove the current insertion.','Proof of6.6, specialization Y=X',412),
12:('E_(x-prime_i), with a tall prime stroke','Both complete412 images and native412_lemma_stalk_detail.png show a vertical prime at the index x; the proof prime in native412_proof_stalk_detail.png supplies a direct glyph comparison. Diplomatic retains the observed prime, without asserting the typist’s intended stroke length. The statement names only x_i and its section germ s_(x_i), whose module is E_(x_i). The proof chooses a closed specialization x-prime_i later. For primes p_i⊂m_i the localization A_(m_i)→A_(p_i) induces E_(x-prime_i) tensor_A_(m_i) A_(p_i)→E_(x_i), e⊗a↦ae, with inverse e/a↦e⊗a^(-1); it carries the constructed basis to s_(x_i). Thus current E_(x_i) matches both the bound point and the actual conclusion; the primes inside the proof remain.','End of Lemma6.7 statement',412),
13:('A closure bar over{x_i}','Both complete412 images clearly show this bar. Retain it in both forms. The relation x-prime_i∈closure{x_i} corresponds to p_i⊂m_i and gives the localization map used in the proof. This restores a printed glyph; classify the former omission as a transcription error.','Lemma6.7, choice of closed point',412),
14:('fans la famille','Both complete412 images print fans. The phrase identifies membership in the displayed finite family of maximal ideals; current dans supplies that preposition without changing the family or its index map. Retain fans diplomatically and dans currently.','Lemma6.7 proof',412),
15:('A_(m_i) d’où, without a separator','Both complete412 images show no punctuation after the displayed local module. The relative d’où refers directly to that isomorphism. Tensoring it with A/m_i gives the next displayed residue-module isomorphism. The inserted semicolon changes none of these maps, so retain the source punctuation in both forms.','Lemma6.7 proof, local isomorphism',412),
16:('x_1 ... ,x_k, with no comma after x_1','Both complete412 images show the unseparated first term followed by the ellipsis and the final comma. The named family is exactly the map i↦x_i for i=1,…,k; the optional first separator neither changes its index set nor an entry. Retain the source notation in both forms.','Lemma6.8 statement',412),
17:('Fourteen typed m letters, each singly ruled','All14 maximal-ideal letters on both complete412 images have the same single lower rule. Restore underline(m)_i in both forms. Each occurrence denotes the very same ideal m_i⊂A; identity on its elements gives the comparison with the former Fraktur rendering and induces the identical localization and quotient maps.','Lemma6.7 proof',412),
18:('Three baseline stops before the complex','Both complete414 images show typed baseline stops. Retain ldots.','First complex, beginning',414),
19:('Three baseline stops at the complex end, no additional period','Both complete414 images show exactly those stops after the last arrow. Retain the attached ldots and omit an added sentence stop.','First complex, end',414),
20:('Three baseline stops between the gamma factors','Both complete414 images show the low typed stops. Retain ldots.','Gamma-monomial display',414),
21:('Three baseline stops in i_1+...+i_k','Both complete414 images show the low typed stops. Retain ldots.','Gamma-monomial weight',414),
22:('O_X,-Modules, with a low comma after X','Both complete414 images show the low comma and its tail, unlike the raised straight primes in the nearby X-prime occurrences. Diplomatic retains that comma. The immediately defined flag scheme is X-prime, the two classes xi,eta belong to K-dot(X-prime), and their invertible sheaves enter the displayed gamma identity in that same group. Current O_(X-prime) restores this stated base. Pullback f^*:K-dot(X)→K-dot(X-prime) is the explicit map used in the following line; no base is silently identified.','Invertible modules before gamma-series identity',414),
23:('Both K letters have a raised dot','Both complete415 images show those raised dots in Problem6.10. Retain both attached K-bullet readings under the established VI convention.','Problem6.10',415),
24:('BIBLIOGRAPHIE alone, in capitals','Both complete415 images show this heading without the added exposé phrase. Retain the attached capital heading under the accepted NOTE6 section-heading convention.','Bibliography heading',415),
25:('K-Theory and stable algebra, in plain type','Both complete415 images show the complete title in plain type. Retain the attached unitalicized title.','Bibliography[1]',415),
26:('Anneaux de Chow et applications, in plain type','Both complete415 images show the complete title in plain type. Retain the attached unitalicized title.','Bibliography[2]',415),
27:('Topos localement annelés et schémas relatifs, in plain type','Both complete415 images show the complete title in plain type. Retain the attached unitalicized title, including the parenthetical preparation status.','Bibliography[3]',415),
28:('Residues and duality, in plain type','Both complete415 images show the complete title in plain type. Retain the attached unitalicized title.','Bibliography[4]',415),
29:('Le groupe de Grothendieck des schémas en groupes réductifs, in plain type','Both complete415 images show the complete title in plain type. Retain the attached unitalicized title.','Bibliography[5]',415),
30:('Lectures notes in Mathematics','Both complete415 images print Lectures notes. The volume’s own title matter gives the series name Lecture Notes in Mathematics. The bibliographic locator(R.Hartshorne,Residues and duality,Springer,series volume20) is preserved by the spelling correction; current retains Lecture Notes, diplomatic the printed wording.','Bibliography[4], series name',415),
}
for k,(p,w,g,f) in obs.items():
 r.finding(batch,k,p,w,g,witness=f+11,actual_page=f,verdict='reverted' if k in [11,15,16] else 'amended' if k==12 else 'not applied and now applied' if k in [6,7,17] else 'confirmed')
for row in r.decisions:
 key=row.get('related_finding',row['source_id']);k=int(key.rsplit('#',1)[1])
 if row.get('kind')=='misprint_in_print' or row['type']=='misprint':
  row.update(is_misprint=k not in [11,15,16],correction_status='Printed punctuation retained in both forms' if k in [11,15,16] else 'accepted paired correction')
 if k in [11,15,16] and row['type']=='fixlog':row.update(verdict='confirmed',change='Retain the diplomatic restoration and remove the corresponding unsupported current insertion.')
for n,k in [(437,5),(438,13),(439,14),(440,30)]:
 p,w,g,f=obs[k];r.source(f'fixes/FIXLOG_6_CURRENT.jsonl#{n}',p,w,g,witness=f+11,change='Retain the restored printed closure bar in both forms; correct the historical misprint classification.' if k==13 else 'Retain the paired current correction.')
 r.decisions[-1].update(is_misprint=k!=13,correction_status='Transcription repair, printed bar restored' if k==13 else 'accepted paired correction')

for old,new,k in [('$Y=X$; il','$Y=X$ il',11),("A_{\\mathfrak m_i}$; d'où","A_{\\mathfrak m_i}$ d'où",15),('$x_1,\\ldots,x_k$ des points','$x_1\\ldots,x_k$ des points',16)]:
 r.patch(412,'current',old,new,f'check/findings/findings_{batch}.json#{k}',obs[k][1])

id='ASTRA-VI-TOTAL-COHOMOLOGY-411'
why='Both complete411 images print i≥0. The source allows arbitrary integer shifts of perfect complexes(I4.7–4.11,IV1.2 and2.2). On Spec(k),M=k[2] has its only cohomology in degree−2, but class1; the printed sum is zero and puts1 in K-dot(X)_1, contradicting6.6 at d=0. The all-degree sum projects to the printed nonnegative sum by identity on nonnegative summands and zero on negative ones, with kernel the sum of the negative cohomology sheaves. The proof on412 requires empty support to mean acyclicity and requires the tensor-support inclusion; k[−2] tensor k[2]→k,a⊗b↦ab, explicitly disproves that inclusion for the printed sum. Every integer q occurs as the sole degree of the allowed k[−q], so preserving the stated perfect category and the proof forces inclusion of every integer in this index. Current uses i∈Z; diplomatic keeps i≥0. An even shift[−2N] with inverse[2N] gives the exact same-class, same-total-support comparison with representatives concentrated in nonnegative cohomological degrees. Full convention checks, maps and counterexamples are in cohomology_index_411.json.'
r.own_finding(id,411,'direct sum over i≥0','Same nonnegative index','Current-only index i∈Z; retain printed i≥0 diplomatically.',why,'Definition6.5, total cohomology',kind='misprint_in_print',witness=422)
r.own[-1].update(is_misprint=True,correction_status='accepted paired index correction',proof_file='review/expose_vi/cohomology_index_411.json')
r.patch(411,'current',r'\bigoplus_{i\ge0}H^i',r'\bigoplus_{i\in\mathbb Z}H^i',id,why)
shutil.copyfile(Path(__file__).parents[1]/'english/EN_INDEPENDENT_VI_TOTAL_COHOMOLOGY_AUDIT_411.json',Path(__file__).parent/'cohomology_index_411.json')

# The historical HOLD records are nominally attached to383; their text is on412–413.
why=obs[13][1]+' '+obs[14][1]+' The inserted semicolon in both historical candidates is separately reverted under finding15.'
r.source('fr/codex/HOLD_VS_CORR.json#41','closure bar over{x_i}; fans la famille',why,'412 Lemma6.7 proof',page=412,witness=423,change='Restore the closure bar in both forms; retain paired fans/dans; preserve source punctuation and ruled letters.')
why='Both complete413 images clearly print k and k-prime as the twist multipliers; the fixed finite family was named on412. Fix that family as(x_i)_(i∈I),I={1,…,k_0}. The multiplier renaming is the bijection I×Z_(≥1)→I×Z_(≥1),(i,k)↦(i,q=k), with inverse(i,q)↦(i,k=q); it sends E(kn),its section and its germ to the identical E(qn),section and germ. In the proof the same identity renaming sends f^(tensor k n-prime_0) to f^(tensor q n-prime_0), and likewise for k-prime and q-prime in the next paragraph. It alters no sheaf, exponent or quantifier over the already fixed family. Retain the authors’ printed bound-variable names in both forms and confirm rejection of this editorial renaming.'
for id in ['fr/codex/HOLD_VS_CORR.json#42','fr/codex/HOLD_VS_CORR.json#43','fixes/RECONCILE_CODEX_6.json:entries#244','fixes/RECONCILE_CODEX_6.json:entries#322']:
 r.source(id,'k,k-prime as printed twist multipliers',why,'Lemma6.8 and its application,412–413',page=413,witness=424,change='Retain k,k-prime in both forms; reject q,q-prime substitution.')
 r.decisions[-1].update(is_misprint=False,correction_status='Author bound-variable names retained with exact renaming comparison')

def current(p,layer):
 t=base_text(p,layer)
 for x in r.patches:
  if x['page']==p and x['layer'] in ['both',layer]:
   assert t.count(x['old'])==x['expected_count'],(p,layer,x['source_id']);t=t.replace(x['old'],x['new'])
 return t
for p in [411,412,413,414]:
 id=f'ASTRA-VI-GLYPHS-{p}';why=obs[7][1]+(' '+obs[17][1] if p==412 else '')
 r.own_finding(id,p,'Individually observed rules','Plain sheaf and complex letters; Fraktur m on412','Restore the listed rules and keep the printed class letters plain.',why,'Sheaf, complex and class notation',kind='font',witness=p+11)
 for layer in ['diplomatic','current']:
  old=current(p,layer);s=old.replace(r'\mathcal O',r'\underline{O}')
  if p in [411,412]:
   s,n=re.subn(r"(?<![A-Za-z\\])M(?=(?:'\{\})?\^\\bullet)",lambda _:r'\underline{M}',s);assert n=={411:27,412:9}[p],(p,n)
  if p in [411,412]:
   assert s.count('$L$')==1;s=s.replace('$L$',r'$\underline{L}$')
  else:
   s,nL=re.subn(r'(?<![A-Za-z\\])L(?![A-Za-z])',lambda _:r'\underline{L}',s)
   assert nL=={413:5,414:2}[p],(p,nL)
  if p==412:
   s,n=re.subn(r'(?<![A-Za-z\\])E(?![A-Za-z])',lambda _:r'\underline{E}',s);assert n==10,n
   assert s.count(r'\mathfrak m')==14;s=s.replace(r'\mathfrak m',r'\underline{m}')
  elif p==413:
   a=s.index('de classes');b=s.index('Soient $Y$',a)
   part=s[:a];part,n1=re.subn(r'(?<![A-Za-z\\])E(?![A-Za-z])',lambda _:r'\underline{E}',part)
   tail=s[b:];tail,n2=re.subn(r'(?<![A-Za-z\\])E(?![A-Za-z])',lambda _:r'\underline{E}',tail)
   assert n1+n2==15,(n1,n2);s=part+s[a:b]+tail
  elif p==414:
   s,n=re.subn(r'(?<![A-Za-z\\])N(?=\^\\bullet)',lambda _:r'\underline{N}',s);assert n==4,n
   a=s.index(r'\[');b=s.index(r'\]',a)
   part=s[a:b];part,n=re.subn(r'(?<![A-Za-z\\])E(?![A-Za-z])',lambda _:r'\underline{E}',part);assert n==2,n;s=s[:a]+part+s[b:]
   for a,b in [('$E_i$ et $F_i$ ayant même rang',r'$\underline{E}_i$ et $\underline{F}_i$ ayant même rang'),('les $E_i,F_i$ de rang constant',r'les $\underline{E}_i,\underline{F}_i$ de rang constant'),('drapeaux des $E_i,F_i$',r'drapeaux des $\underline{E}_i,\underline{F}_i$')]:
    assert s.count(a)==1,(p,a);s=s.replace(a,b)
  assert s!=old;r.patch(p,layer,old,s,id,why)
 r.own[-1]['observed_rule_counts']={411:{'M':27,'L':1},412:{'M_complex':9,'E':10,'L':1,'O':2,'m':14},413:{'E':15,'L':5,'O':1},414:{'N':4,'L':2,'E_sheaf':5,'F_sheaf':3,'O':1}}[p]

def rules(t,phrases):
 pat='(?<![A-Za-zÀ-ÿ])('+'|'.join(re.escape(s).replace(r'\ ',r'\s+') for s in sorted(phrases,key=len,reverse=True))+')(?![A-Za-zÀ-ÿ])'
 return re.sub(pat,lambda m:r'\uline{'+m[0]+'}',t)
for p in [411,412,413]:
 id=f'ASTRA-VI-WORD-RULES-{p}';why=obs[6][1]
 r.own_finding(id,p,'Separate statement word rules','Plain statement prose','Restore those word-group rules.',why,'Statements and6.5 paragraph label',witness=p+11)
 for layer in ['diplomatic','current']:
  old=current(p,layer);s=old
  if p==411:
   s=s.replace(r'\textbf{6.5.}','6.5.')
   a=s.index(r'\textbf{Proposition 6.6.}')+len(r'\textbf{Proposition 6.6.}');b=s.index('Soient',a)
   s=s[:a]+rules(s[a:b],['La filtration','de',"est une filtration d'anneau",'et'])+s[b:]
  elif p==412:
   a=s.index(r'\textbf{Lemme 6.7.}')+len(r'\textbf{Lemme 6.7.}');b=s.index('Posons',a)
   s=s[:a]+rules(s[a:b],['Soit','un schéma affine noethérien','un nombre fini de points de','un','-Module inversible','Alors','il existe une section','telle que pour tout','soit une base de'])+s[b:]
   a=s.index(r'\textbf{Lemme 6.8.}')+len(r'\textbf{Lemme 6.8.}')
   s=s[:a]+rules(s[a:],['Soient','un schéma noethérien ayant un faisceau ample','un','-Module inversible','des points de','Alors il existe un'])
  else:
   a=s.index('entier');b=s.index('On peut trouver',a)
   s=s[:a]+rules(s[a:b],['entier','tel que pour tout','il existe une section','qui soit une base de','pour tout'])+s[b:]
   a=s.index(r'\textbf{Théorème 6.9.}')+len(r'\textbf{Théorème 6.9.}');b=s.index('(Cette dernière',a)
   s=s[:a]+rules(s[a:b],['Soit','un schéma noethérien de dimension','ayant un faisceau ample','Alors','et à fortiori'])+s[b:]
  assert s!=old;r.patch(p,layer,old,s,id,why)

# The unnamed p in413 is not silently given a new quantified domain.
id='ASTRA-VI-POWER-LOCUS-413'
why='Both complete413 images say pour tout p without printing a domain. For a positive tensor power, in a local trivialization f=a and f^(tensor p)=a^p; D(a^p)=D(a) follows from the inverse ring maps A_a↔A_(a^p),1/a↦a^(p−1)/a^p and1/a^p↦(1/a)^p. At p=0, X_(f^0)=X; for example X=Spec k[t],f=t gives X≠D(t), witnessed by the closed point(t). The proof uses positive powers to preserve nonvanishing at the chosen points. Record the omitted domain and this exact comparison; retain the author’s unqualified phrase in both forms rather than inserting a new assertion.'
r.own_finding(id,413,'Comme pour tout p, X_(f^(tensor p))=X_f','Same unqualified p','Retain the printed phrase; record its positive-power map and zero-power obstruction.',why,'Lemma6.8 proof',kind='author_claim',verdict='confirmed',witness=424)
r.own[-1].update(is_misprint=False,correction_status='Unspecified author domain retained; exact scope analysis recorded')

for p,a,b in [(411,'x↝f*(x)↝f*(x)x-prime↝f_*(f*(x)x-prime)','(EGA0_IV14.2.2.3).'),(412,'Il suffit donc, pour achever la démonstration','Alors il existe un'),(413,'entier n tel que pour tout k≥1','L^(tensor−kn)→E,L^(tensor−k-prime n-prime)→E-prime,'),(414,'qui sont des isomorphismes aux points x_i.','K-dot(X-prime) sur K-dot(X),tel que:'),(415,'x-prime=product_(i=0)^r(xi_i−1),','Bibliography[5],n°34.')]:
 r.page(p,a,b,notes='Complete primary and native images personally compared word by word and symbol by symbol. Native412 tight crops additionally resolve the statement and proof primes. Total-cohomology index has an independent exact mathematical audit; final product index is recorded separately.',witness=p+11)
r.commit()
