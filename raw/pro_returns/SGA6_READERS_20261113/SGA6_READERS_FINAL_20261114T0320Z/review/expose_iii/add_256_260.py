#!/usr/bin/env python3
import json,re
from review_helpers import Review,ROOT,base_text,underline_words
r=Review();batch='256_260'
obs={
1:('toramp(E_{X_s})_x, with x outside the sole parentheses','Both complete scans show one argument pair and the exterior x subscript. Retain that exact placement.','Corollary4.6.1 display',267),
2:('Page257 begins item b)','The complete256 page contains extérieur à[a,b] and its stop. The next page starts the separately labelled b) amplitude condition. Retain the attached boundary.','Boundary256/257',268),
4:('Both parf words ruled, S-prefixes plain','The two category subscripts at the end of4.8 have individual lower rules under parf only. Keep uparf at these two positions.','End of Proposition4.8',269),
5:('First parf ruled, second parf plain','The first author note explicitly displays the ruled category on the left and the plain category on the right of the equality. Both prefixes S- remain plain.','Author note1',269),
6:('Both parf words ruled','The end of4.8.1 has a rule under each of the two parf subscripts. The independent author note2 repeats the ruled/plain equality.','End of Corollary4.8.1',269),
7:('Hom ruled, R plain','Both scans put the rule under Hom alone in the statement. The ordinary leading R remains separate.','Proposition4.9 derived Hom',269),
8:('Hom ruled, R plain','The final proof expression on258 repeats the same individual Hom rule.','Final line of258',269),
9:('Hom ruled in the first display’s left member','The f_* prefix and the plain R stand outside the Hom rule.','First duality comparison, left side',270),
10:('Headless tilde over a horizontal line','The first displayed comparison has no arrow tip in either scan.','First duality comparison sign',270),
11:('Hom ruled in the first display’s right member','The rule belongs only to Hom in RHom(f_*E,F).','First duality comparison, right side',270),
12:('Hom ruled in the second display','The second display starts with the same separately ruled Hom expression.','Perfect-dual tensor comparison, left side',270),
13:('Headless tilde over a horizontal line','The second display uses the same headless comparison as the first. Its tensor L remains ordinary.','Perfect-dual tensor comparison sign',270),
15:('Hom ruled in RHom(.,K_X)','The definition’s Hom has an individual lower rule and its R has none.','Definition of duality functor',270),
16:('Full stop on the baseline as placeholder','Both scans place the dot low before the comma in(.,K_X). Retain the baseline stop.','Duality-functor placeholder',270),
17:('D_X with D ruled','The defined duality functor has an individual rule under its D. The subscript X lies outside the rule.','Definition of D_X',270),
18:('D_X(E) with D ruled','The membership sentence repeats the individual D rule. The nearby category D(f) remains plain.','Duality-functor membership',270),
19:('Both D_X letters ruled','The biduality target has two separately ruled D letters, each with its own X subscript.','First biduality arrow',270),
21:('Two ruled D letters and a headless comparison','The global duality display reads f_*D_X≃D_Sf_*, with both D rules and no arrowhead in the middle sign.','Global duality comparison',270),
22:('Both D_S letters ruled','The final displayed target has two separately ruled D letters; the ordinary category D does not acquire these rules.','Second biduality arrow',270),
23:('Page260 begins a)Le foncteur','The preceding259 page ends the lemma introduction and its separate author note. The complete260 page begins the first item. The attached list and marker are correctly placed.','Boundary259/260',271),
24:('Page260 ends sommes directes de faisceaux','Both complete scans end at faisceaux, without the next page’s du. Retain the existing boundary.','End of260',271),
25:('Hom ruled in display(*)','The first starred display has one lower rule under Hom, with the H exponent and dual argument independently typed.','Lemma5.1(b-prime)',271),
26:('Définition de ruled;(*)plain','The words alone carry the rule; the parenthesized star and colon are outside it.','Definition label after lemma',271),
27:('Hom ruled in E-dual definition','The leading R is ordinary and unruled; Hom alone carries its lower rule.','Definition of E-dual',271),
28:('Hom ruled in display(**)','The target of the adjunction arrow has the same individual Hom rule.','Second starred display',271),
29:('Ext ruled; p+1 above it','The three-star display has a rule under Ext, with its cohomological exponent separate.','Third starred display, left side',271),
30:('Hom ruled in display(***)','The target has the individual Hom rule; the final comma is retained.','Third starred display, right side',271),
}
for k,(reading,why,region,wit) in obs.items():r.finding(batch,k,reading,why,region,witness=wit)
why=('The print cites4.6. Proposition4.7(b) is the statement whose data are the two f_i and their product f=f1×_Sf2. '
     'Substitute E_i=O_Xi and[a_i,b_i]=[−n_i,0]. Their external tensor identifies with O_X by the multiplication map O_X tensor_OX O_X→O_X, u tensor v↦uv, whose inverse sends w to w tensor1. '
     'The displayed summed interval is[−n1−n2,0], exactly the dimension bound stated in4.7.1. The Tor-independence assumptions are those of4.7. '
     'This identifies the exact cited assertion(b), independently of the separately recorded failure of4.7(a). Correct only the locator4.6→4.7 in current.')
r.finding(batch,3,'Sous les hypothèses de(4.6)',why,'Corollary4.7.1 first phrase',verdict='amended',change='Current locator4.7; diplomatic4.6.',witness=268)
r.patch(257,'current','Sous les hypothèses de (4.6)','Sous les hypothèses de (4.7)',f'check/findings/findings_{batch}.json#3',why)
why=('The print cites4.8, while the author’s next sentence specifies the substitution E=O_X. In4.9, the hypothesis that f is perfect makes O_X perfect relative to f. '
     'The complex RHom_OX(O_X,f!F) identifies with f!F by evaluation at1, with inverse m↦(a↦am); O_X is locally free of rank1, so this is also the derived identification. '
     'The resulting conclusion is exactly that f!F is perfect over S. This uses4.9’s compactifiable/noetherian setting and its actual Hom expression. Correct only the locator to4.9.')
r.finding(batch,14,'Sous les hypothèses de(4.8)',why,'Corollary4.9.1 first phrase',verdict='amended',change='Current locator4.9; diplomatic4.8.',witness=270)
r.patch(259,'current','Sous les hypothèses de (4.8)','Sous les hypothèses de (4.9)',f'check/findings/findings_{batch}.json#14',why)
why=('The print says appliquer4.8 avecY=S,F=O_S. Under these explicit substitutions in4.9, f!F=f!O_S=K_X and RHom(E,f!F)=D_X(E) by the preceding definition. '
     'O_S is the rank-one free complex over id_S, and E has the relative perfection required in4.9. The structural morphism X→S is f itself, so the resulting S-relative perfection is exactly membership in D(f)_parf. '
     'This identifies the first assertion of4.9.2 term for term and fixes the locator4.9 without changing any functor or object.')
r.finding(batch,20,'appliquer(4.8)avecY=S,F=O_S',why,'Proof4.9.2 first assertion',verdict='amended',change='Current locator4.9; diplomatic4.8.',witness=270)
r.patch(259,'current',r'appliquer (4.8) avec \(Y=S\)',r'appliquer (4.9) avec \(Y=S\)',f'check/findings/findings_{batch}.json#20',why)
for x in r.decisions:
 if any(f'check/findings/findings_{batch}.json#{k}' in {x['source_id'],x.get('related_finding')} for k in [3,14,20]):x['is_misprint']=True

why=('Both complete primary and native256–257 pages repeat3.5(a)’s relative-amplitude bound in4.7(a), with E2 additionally pseudo-coherent. '
     'The example S=SpecZ, X1=Y1=SpecFp, X2=Y2=S, identity f_i, E1=Fp and E2=Z/p in degree0 satisfies this added condition: [Z --p→Z] is a finite free resolution of E2. '
     'Its external tensor still identifies through pr1=id and pr2:SpecFp→SpecZ with[Fp --0→Fp] in degrees−1,0, violating the claimed[0,0] interval. '
     'A boundedness failure is explicit over A=k[ε]/(ε²): take S=SpecA, X1=Y1=Speck, X2=Y2=S, identity f_i and E1=E2=k. '
     'The two required scheme pairs have S as their second factor, so their higher Tor groups vanish. E1 is rank-one free over k and has relative perfect amplitude[0,0]. '
     'The exact free resolution ...→A --ε→A --ε→A→k has kernel=image=(ε) in each negative degree, proving that E2 is pseudo-coherent and concentrated in degree0. '
     'Definition1.6 identifies the external tensor on X=Speck with k tensor_A^L k. Tensoring that explicit resolution with k makes every differential zero, so H^j=k for every j≤0. '
     'The printed conclusion therefore fails even to give bounded cohomology. Preserve the author statement and the printed proof reference to3.5; no uniquely supported replacement hypothesis is supplied by these calculations.')
r.own_finding('ASTRA-III-AUTHOR-CLAIM-256',256,'Proposition4.7(a), with its printed proof on257','Same printed proposition and proof','Retain both layers; record the two exact external-tensor counterexamples.',why,'Proposition4.7(a) and its cited3.5 argument',kind='author_claim',verdict='confirmed',witness=267)
r.own[-1].update(is_misprint=False,correction_status='No unique source-supported replacement',supplemental_images=['scan/SGA6_scan_360dpi.pdf#page=271','scan/SGA6_witness_300dpi.djvu#page=268'])
(ROOT/'review/expose_iii/author_claim_256_257.json').write_text(json.dumps(dict(source='ASTRA-III-AUTHOR-CLAIM-256',proof=why,related='ASTRA-III-AUTHOR-CLAIM-244',body_action='Preserve printed statement and proof in both layers; no replacement assertion.'),ensure_ascii=False,indent=2)+'\n')
for page,count in [(258,1),(259,5),(260,3)]:
 id=f'ASTRA-III-STRUCTURE-{page}';why='Both complete scans show ordinary typed O letters with individual lower rules at these exact counted positions. Restore their contours and preserve all subscripts.'
 r.own_finding(id,page,'Ruled ordinary O',r'\mathcal O',r'\underline{O}',why,'All structure-sheaf symbols',kind='font',witness=page+11)
 r.patch(page,'both',r'\mathcal O',r'\underline{O}',id,why,count=count)
for page,numbers in [(258,[1,2,3,4]),(259,[1])]:
 id=f'ASTRA-III-AUTHOR-NOTES-{page}';why='Every complete author note and its raised parenthesized call was read in both scans. Restore the original numbers in their source order, preserving all note text, mathematics and attribution.'
 r.own_finding(id,page,'Original author calls '+','.join(map(str,numbers)),r'Continuous \footnote numbering','Restore original author-note calls.',why,'Author notes and their exact calls',kind='symbol',witness=page+11)
 old=base_text(page,'diplomatic');starts=[m.start() for m in re.finditer(re.escape(r'\footnote{'),old)];assert len(starts)==len(numbers)
 # Each longer unique anchor avoids a count-limited global substitution.
 for pos,num in zip(starts,numbers):
  anchor=old[pos:pos+60];assert old.count(anchor)==1
  r.patch(page,'both',anchor,anchor.replace(r'\footnote{',rf'\SGAAuthorFootnote{{{num}}}{{',1),id,why)

def current(page,layer):
 t=base_text(page,layer)
 for p in r.patches:
  if p['page']==page and p['layer'] in ['both',layer]:
   assert t.count(p['old'])==p['expected_count'],(page,layer,p['source_id']);t=t.replace(p['old'],p['new'])
 return t
def rules(text,phrases):
 pats=[re.escape(s).replace(r'\ ',r'\s+') for s in sorted(phrases,key=len,reverse=True)]
 pat='(?<![A-Za-zÀ-ÿ])('+'|'.join(pats)+')(?![A-Za-zÀ-ÿ])'
 return re.sub(pat,lambda m:r'\uline{'+m[0]+'}',text)
def protect_notes(s):
 notes=[]
 while r'\SGAAuthorFootnote{' in s:
  a=s.index(r'\SGAAuthorFootnote{');pos=a+len(r'\SGAAuthorFootnote');end=pos
  for unused in range(2):
   assert s[end]=='{';depth=1;end+=1
   while depth:
    if s[end]=='{' and s[end-1]!='\\':depth+=1
    elif s[end]=='}' and s[end-1]!='\\':depth-=1
    end+=1
  notes.append(s[a:end]);s=s[:a]+f'@@ANOTE{len(notes)}@@'+s[end:]
 return s,notes
def restore_notes(s,notes):
 for i,n in enumerate(notes,1):s=s.replace(f'@@ANOTE{i}@@',n)
 return s
for page in range(256,261):
 id=f'ASTRA-III-WORD-RULES-{page}';why='Restore the exact upright statement word rules read in both complete scans. Mathematical parf/Hom/D rules remain independent, author-note prose retains its own plain setting, and the unruled dans and resp. within257’s category sentence remain plain.'
 r.own_finding(id,page,'Observed upright word-group rules','Plain statement prose and italic proof labels','Restore the inspected rules',why,'Statements and proof labels',witness=page+11)
 for layer in ['diplomatic','current']:
  old=current(page,layer);new=old
  if page==256:
   a=new.index(r'\textbf{Corollaire 4.6.1.}')+len(r'\textbf{Corollaire 4.6.1.}');b=new.index(r'\emph{Preuve.}',a)
   part=rules(new[a:b],['Soient','un morphisme localement de présentation finie et plat','un intervalle de','Notons','la projection canonique','et posons','On a alors','au voisinage de','et','Par suite','est parfait si et seulement si','est parfait rel.','à','parfait pour tout'])
   new=new[:a]+part+new[b:]
   a=new.index(r'\textbf{Proposition 4.7.}')+len(r'\textbf{Proposition 4.7.}')
   new=new[:a]+rules(new[a:],['Soient','un schéma','et pour','un','morphisme localement de type fini','un intervalle de','Supposons','et','ainsi que','tor-indépendants sur','Posons','Alors on a','Si','et si','est pseudo-cohérent rel.','à','et acyclique en degré extérieur à','cf.'])
  elif page==257:
   b=new.index(r'\textbf{Corollaire 4.7.1.}');new=rules(new[:b],['pour'])+new[b:]
   a=new.index(r'\textbf{Corollaire 4.7.1.}')+len(r'\textbf{Corollaire 4.7.1.}');b=new.index(r'\textbf{Corollaire 4.7.2.}',a)
   new=new[:a]+rules(new[a:b],['Sous les hypothèses de','si','pour','est de dimension parfaite','Par suite','et','sont parfaits','il en est de même de'])+new[b:]
   a=new.index(r'\textbf{Corollaire 4.7.2.}')+len(r'\textbf{Corollaire 4.7.2.}');b=new.index(r'\textbf{Proposition 4.8.}',a)
   new=new[:a]+rules(new[a:b],['Soit','un carré cartésien de schémas','où','est localement de type fini et','et','sont supposés tor-indépendants sur','et soient','un intervalle de','On a','et par suite le foncteur','envoie'])+new[b:]
   a=new.index(r'\textbf{Proposition 4.8.}')+len(r'\textbf{Proposition 4.8.}')
   new=new[:a]+rules(new[a:],['Soient','un schéma','un','morphisme propre de','schémas localement de type fini','Alors','sous réserve de validité de','pour','donc en tout cas si','est localement noethérien','ou si','est projectif','Si','est parfait rel.','à','il en est de même de','Supposons','quasi-compact','et','de type fini sur','soient','un intervalle de','un entier tel que','pour tout'])
  elif page==258:
   a=0;b=new.index(r'\emph{Preuve.}')
   part,notes=protect_notes(new[a:b]);part=rules(part,['tout','Module quasi-cohérent',"un tel entier existe d'après",'et','on a alors','Par suite','le foncteur','envoie','dans']);new=restore_notes(part,notes)+new[b:]
   a=new.index(r'\textbf{Corollaire 4.8.1.}')+len(r'\textbf{Corollaire 4.8.1.}');b=new.index(r'\emph{Preuve.}',a)
   part,notes=protect_notes(new[a:b]);part=rules(part,['Soient','un morphisme propre et parfait','et','Alors','sous réserve de validité de','pour','si','est parfait','il en est de même de','en outre','est quasi-compact','le foncteur','envoie','dans']);new=new[:a]+restore_notes(part,notes)+new[b:]
   a=new.index(r'\textbf{Proposition 4.9}')+len(r'\textbf{Proposition 4.9}');b=new.index(r'\emph{Preuve.}',a)
   part,notes=protect_notes(new[a:b]);part=rules(part,['Soient','un schéma noethérien','et','des','schémas de type fini','un','morphisme compactifiable','i.e.',"composé d'une immersion ouverte et d'un morphisme propre",'Si','est parfait rel.','à','parfait rel.']);new=new[:a]+restore_notes(part,notes)+new[b:]
  elif page==259:
   a=new.index(r'\textbf{Corollaire 4.9.1.}')+len(r'\textbf{Corollaire 4.9.1.}');b=new.index(r'\emph{Preuve.}',a)
   new=new[:a]+rules(new[a:b],['Sous les hypothèses de','si','est parfait','envoie','dans'])+new[b:]
   a=new.index(r'\textbf{Corollaire 4.9.2.}')+len(r'\textbf{Corollaire 4.9.2.}');b=new.index(r'\emph{Preuve.}',a)
   new=new[:a]+rules(new[a:b],['Soient','un schéma noethérien','un morphisme compactifiable','Posons','Pour','on a','et la flèche canonique','est un isomorphisme'])+new[b:]
   a=new.index(r'\textbf{Lemme 5.1.}')+len(r'\textbf{Lemme 5.1.}')
   new=new[:a]+rules(new[a:],['Soit','un topos annelé','commutatif','notons','la catégorie des','Modules','Soient','et','Considérons les conditions suivantes'])
  elif page==260:
   b=new.index(r'\emph{Définition de}')
   new=rules(new[:b],['Le foncteur','de','dans','est exact à droite','La flèche canonique','est un isomorphisme pour tout','est exact à gauche','La flèche canonique définie ci-dessous','Alors on a','En outre','si','est pseudo-cohérent','les conditions','sont équivalentes'])+new[b:]
  new=new.replace(r'\emph{Preuve.}',r'\uline{Preuve}.');new,_=underline_words(new)
  assert new!=old,page;r.patch(page,layer,old,new,id,why)
r.page(256,'que E^a/B^a est h-plat','et acyclique en degré extérieur à[a,b].',notes='Both scans confirm the truncation argument’s h-flat conclusion, outer stalk index in4.6.1 and every4.7(a) hypothesis. Its false cohomology bound is preserved with exact counterexamples.',witness=267)
r.page(257,'b)parfamp_fi(E_i)contained in[a_i,b_i]pour i=1,2','R^if_*(M)=0 pour tout i>N et',notes='All four base-change square arrows, three plain derived L letters, two individually ruled parf words and the unruled dans/resp. sentence read. The4.7.1 locator is identified by E_i=O_Xi in4.7(b).',witness=268)
r.page(258,'tout O_X-Module quasi-cohérent M','f_*RHom(E,f!F)est; four complete author notes',notes='All six parf rules, two Hom rules, plain R symbols, ordinary unhooked factorization arrows, exclamation marks, one ruled O and all four complete author notes read in both scans.',witness=269)
r.page(259,'parfait rel.à S. Mais d’après le théorème de dualité','Considérons les conditions suivantes:; author note1 complete',notes='Four Hom rules, eight duality-D rules, three headless comparisons, two headed biduality arrows, five O rules and the original author note read. Both4.8 citations are corrected by the exact substitutions in4.9.',witness=270)
r.page(260,'a)Le foncteur M↦H^p(E tensor^L M)','où M0 et M1 sont sommes directes de faisceaux',notes='All four lemma conditions and both implication chains, four Hom rules, one Ext rule, three O rules, ordinary Mod and R letters, three star labels and final exact sequence read in both scans.',witness=271)
r.commit()
