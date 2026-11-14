#!/usr/bin/env python3
"""Explicit readings from personally inspected full source pages231–235."""
import re,json
from review_helpers import Review,ROOT,base_text,underline_words
r=Review();batch='231_235'
obs={
1:('C’est une begins231','The complete231 image begins with these words;230 ends the EGA6.5 sentence. The attached marker is already correct.','Top boundary231',242),
2:('Two lowercase ob tokens','Both scans show small ob in the two memberships of Notation1.6.','Notation1.6',242),
3:('Lowercase ob','Both scans show small ob in E_i’s membership.','Lemma1.7 membership',242),
4:('Ordinary L above the first tensor sign','The L has the same single-stroke type as the L in Lpr on the same page. Retain this occurrence-specific plain L.','Opening derived tensor map',242),
5:('Ordinary L above both tensor signs','Both printed superscripts use the ordinary typed L; the left Lpr symbols are separately retained.','Notation1.6 display',242),
6:('Ordinary L above both tensor signs','Both printed superscripts are plain L and the central arrow has a head with a separate tilde above.','Lemma1.7 display',242),
7:('232 starts with the displayed canonical map','The last prose word canonique is still on231;232 begins the two-tensor display. The supplied marker is correctly placed.','Boundary231/232',None),
8:('Two ordinary L superscripts','The complete232 image shows the ordinary typed letter over each tensor.','First display',None),
9:('Two ordinary L superscripts with distinct B_1 and B_2 bases','The first derived tensor is over B_1 and the second over B_2, with B between them. All four indices were inspected.','Second display',None),
10:('Lowercase ob','The membership uses the two small letters ob.','Proposition1.8 membership',None),
11:('Plain L above the tensor in the conclusion','The formula agrees with the preceding derived tensors; the ordinary L stroke is directly visible.','Proposition1.8 conclusion',None),
12:('Plain L in f-prime_*(E_1 tensor E_2)','Both the prime on f and the L above the tensor are visible and independently placed.','Proposition1.8 proof',None),
13:('Plain L in f_1*(E_1) tensor f_2*(E_2)','The ordinary typed L is retained at this last tensor occurrence.','Proposition1.8 proof conclusion',None),
14:('233 begins Corollaire1.9','The entire grâce à(1.7). sentence ends232;233 begins the corollary heading. The attached marker is correct.','Boundary232/233',244),
15:('Ordinary L above the first external tensor functor','The superscript is a plain L; all three D superscript minus signs and X_1/X_2/X arguments are visible.','Corollary1.9 first functor',244),
16:('Ordinary L above the restricted functor','The second formula uses the same ordinary L and plain coh subscripts.','Corollary1.9 second functor',244),
17:('Lowercase ob','Both scans show small ob in the membership of E.','Corollary1.10(b)',244),
19:('Two lowercase ob memberships','E belongs to D(X) and F to D(Y), each preceded by small ob and with no minus on D.','Proposition1.11 introduction',245),
20:('Plain L in E tensor_Y F','The ordinary superscript is visible above the one tensor in the statement.','Proposition1.11(a)',245),
21:('Preuve de ruled, a). plain','The lower rule ends after de; the item letter and its following punctuation remain plain.','First proof label',246),
22:('Preuve de ruled, b). plain','The second proof label has the same exact span, ending before b).','Second proof label',246),
23:('Plain L in h_*(E tensor_Y F)','The L is ordinary type; h occurs explicitly in the derived direct-image expression.','Proof(a) opening',246),
24:('Plain L over both displayed tensors','Both scans show two ordinary L superscripts, a headed central arrow and a tilde above it.','Proof(a) projection formula',246),
25:('Plain L, baseline placeholder dot','The superscript is L and the dot before the tensor is on the ordinary baseline. The source literal period is retained.','Proof(a) g_* functor',246),
}
for k,(printed,reason,region,wit) in obs.items():r.finding(batch,k,printed,reason,region,witness=wit)
reason=('Both scans label the diagonal X→Z by f, while the horizontal X→Y is also f. The immediately stated relative conditions name the composite h, and the proof uses h_*(E tensor_Y^L F). '
        'The corrected diagonal is h=g∘f:X→Z; the induced direct-image identity h_*=g_*f_* identifies exactly the functor used in the proof. Retain the printed diagonal f diplomatically.')
r.finding(batch,18,'f on X→Z',reason,'Proposition1.11 top triangle',change='Retain diplomatic f and current h on the diagonal.',witness=245)
r.source('fixes/FIXLOG_6_CURRENT.jsonl#375','f on X→Z',reason,'Proposition1.11 top triangle',change='Retain current h.',witness=245)
reason=('The first hypothesis in the proof of(b) prints f_*(E). Proposition1.11(b) assumes pseudo-coherence relative to h. After the printed reduction to closed immersions, this hypothesis is pseudo-coherence of h_*(E)=g_*f_*(E). '
        'Set E_0=f_*(E), replace X by Y and f by Id_Y as the printed proof does: the same hypothesis becomes g_*(E_0), exactly the expression later used. '
        'The conclusion remains pseudo-coherence of E_0=f_*(E). Thus only the first f_* becomes h_* in current; the other f_* occurrences remain unchanged.')
r.finding(batch,27,'supposons f_*(E)',reason,'Proof(b) first hypothesis',change='Retain diplomatic f_* and current h_* at this first occurrence only.',witness=246)
r.source('fixes/FIXLOG_6_CURRENT.jsonl#376','supposons f_*(E)',reason,'Proof(b) first hypothesis',change='Retain current h_* at the first occurrence.',witness=246)
reason=('Both full scans print l’isomorphisme(*) de la preuve de(1.8). The inspected231–232 text has no starred formula in either proof. The displayed isomorphism is exactly the Lemma1.7 map at S=Y, f_1=f:X→Y and f_2=Id_Y, using X×_Y Y≅X. '
        'The proof has already reduced f to a closed immersion. At y=f(x), put R=O_{Y,y}, B=O_{X,x}; for a flat resolution P of F_y the chain maps e⊗p↦e⊗(1⊗p) and e⊗(b⊗p)↦be⊗p are inverse between E_x⊗_R P and E_x⊗_B(B⊗_R P). '
        'They realize the stalk of the canonical adjunction projection map. Off X both stalks are zero, since f is closed. This proves the displayed map in the actual proof scope, including complexes not assumed quasi-coherent. '
        'Current cites l’isomorphisme de(1.7), removing the nonexistent star and proof locator; diplomatic retains the complete printed phrase. This is an explicit editorial repair, with no claim about an unseen author draft.')
r.finding(batch,28,'l’isomorphisme(*) de la preuve de(1.8)',reason,'Proof(a) projection-formula reference',verdict='amended',change='Current: l’isomorphisme de(1.7); diplomatic unchanged.',witness=246)
r.patch(235,'current',"l'isomorphisme (*) de la preuve de (1.8)","l'isomorphisme de (1.7)",f'check/findings/findings_{batch}.json#28',reason)
(ROOT/'review/expose_iii/projection_formula_235.json').write_text(json.dumps({'source_id':f'check/findings/findings_{batch}.json#28','source_images':['scan/SGA6_scan_360dpi.pdf#page=249','scan/SGA6_witness_300dpi.djvu#page=246'],'related_source_folios':[231,232,234,235],'decision':'Correct the locator only in current; retain original diplomatic wording.','exact_morphism_proof':reason,'independent_review':'The English reviewer independently checked the chain maps and their agreement with the adjunction projection map.'},ensure_ascii=False,indent=2)+'\n')
reason=('Both scans show E-prime→E→E-double-prime→E-prime in triangular arrangement, followed by a comma. The native witness crop also shows a small curved mark at the tail of the E-double-prime→E-prime edge. '
        'Retain the three printed vertices and reproduce that curved tail with a hook; no unprinted [1] or inferred degree label is added.')
r.finding(batch,26,'Triangle with a curved tail on E-double-prime→E-prime and a final comma',reason,'Proof(b) distinguished triangle',verdict='amended',change='Keep the restored triangle and add the observed curved tail in both layers.',witness=246)
r.patch(235,'both',r"& E'' \arrow[dl] &",r"& E'' \arrow[dl,hook] &",f'check/findings/findings_{batch}.json#26',reason)
for row in r.decisions:
 if row.get('related_finding','') in [f'check/findings/findings_{batch}.json#{n}' for n in [18,27,28]] or row['source_id'] in [f'check/findings/findings_{batch}.json#{n}' for n in [18,27,28]]:row['is_misprint']=True

for page,count in [(232,1),(234,1),(235,3)]:
 id=f'ASTRA-III-STRUCTURE-{page}';why='The complete source page shows an ordinary typed O with its own lower rule and an external subscript. Every stated occurrence was individually inspected; this replaces only the script-font spelling at those locations.'
 r.own_finding(id,page,'Ruled ordinary O',r'\mathcal O',r'\underline{O}',why,'All structure-sheaf occurrences',kind='font',witness=page+11 if page!=232 else None)
 r.patch(page,'both',r'\mathcal O',r'\underline{O}',id,why,count=count)
id='ASTRA-III-AUTHORNOTE-231';why='The author’s call and footnote label both use the raised digit1 inside baseline parentheses, not a running editorial footnote number. The note text is preserved in full, including D(X_i) without a minus.'
r.own_finding(id,231,'Raised1 in parentheses',r'\footnote{...}',r'\SGAAuthorFootnote{1}{...}',why,'Lemma1.7 author note',kind='symbol',witness=242)
r.patch(231,'both',r'\footnote{',r'\SGAAuthorFootnote{1}{',id,why)

def current(page,layer):
 t=base_text(page,layer)
 for p in r.patches:
  if p['page']==page and p['layer'] in ['both',layer]:
   assert t.count(p['old'])==p.get('expected_count',1),(page,layer,p['source_id']);t=t.replace(p['old'],p['new'])
 return t

def rules(text,phrases):
 pat='(?<![A-Za-zÀ-ÿ])('+'|'.join(map(re.escape,sorted(phrases,key=len,reverse=True)))+')(?![A-Za-zÀ-ÿ])'
 return re.sub(pat,lambda m:r'\uline{'+m[0]+'}',text)
for page in range(231,236):
 id=f'ASTRA-III-WORD-RULES-{page}';why=('Exact word rules were compared with the full source page. The statement’s mathematical indices and S-prefixes remain outside the rules. '
   'On231 only the opening sentence of1.5.1 is ruled; its following tor-independence assertion and the body of Notation1.6 stay plain. '
   'On233 the author’s missing rel. before the second à f-prime is retained. Proof-label rules stop before their item letters.')
 r.own_finding(id,page,'Occurrence-specific upright word rules','Mostly plain statements and italic proof labels','Apply the personally inspected word-group rules',why,'Statements and proof labels',witness=page+11 if page!=232 else None)
 for layer in ['diplomatic','current']:
  old=current(page,layer);new=old
  if page==231:
   new=new.replace('Soient des carrés cartésiens de schémas',r'\uline{Soient des carrés cartésiens de schémas}')
   a=new.index(r'\textbf{Lemme 1.7.}')+len(r'\textbf{Lemme 1.7.}');b=new.index(r'\emph{Preuve.}',a)
   s=rules(new[a:b],['Soient','un schéma','et pour','une','immersion fermée','On suppose que','et','ainsi que','sont tor-indépendants sur','Alors','pour','il existe un isomorphisme canonique'])
   new=new[:a]+s+new[b:]
  elif page==232:
   a=new.index(r'\textbf{Proposition 1.8.}')+len(r'\textbf{Proposition 1.8.}');b=new.index(r'\emph{Preuve.}',a)
   s=rules(new[a:b],['Soient','un schéma','et','pour','un','morphisme localement de type fini','On suppose','ainsi que','tor-indépendants sur','un intervalle de','un complexe','pseudo-cohérent rel.','à','et acyclique en degré','Alors','est','avec'])
   new=new[:a]+s+new[b:]
  elif page==233:
   b=new.index(r'\emph{Preuve.}');s=new[:b]
   s=rules(s,['Sous les hypothèses de','le foncteur','induit un foncteur','En particulier','si','et','sont pseudo-cohérents','il en est de même de','Soit','un carré cartésien','avec','localement de type fini','Alors','Supposons','tor-indépendants sur','Pour','est','pseudo-cohérent','fidèlement plat','soient','un complexe à cohomologie quasi-cohérente','Pour que','soit','pseudo-cohérent rel.','à','il faut et il suffit que','pour que','le soit'])
   new=s+new[b:]
  elif page==234:
   b=new.index(r'\emph{Preuve.}');s=new[:b]
   s=rules(s,['Soit','un triangle commutatif de morphismes localement de type fini','soient','et','des intervalles de','Si','est','pseudo-cohérent rel.','à','et acyclique en degré','et si','alors','où','pseudo-cohérent'])
   new=s+new[b:]
  new=new.replace(r'\emph{Preuve.}',r'\uline{Preuve}.')
  new,_=underline_words(new)
  assert new!=old,page;r.patch(page,layer,old,new,id,why)
r.page(231,'C’est une condition de nature locale','flèche canonique; author note1',notes='All seven arrows in the double square, five derived tensor L letters, three lowercase ob memberships and the exact author-note text and call were compared. Native rule span begins after the S-prefix in S-immersion.',witness=242)
r.page(232,'Displayed f_1*(E_1) tensor f_2*(E_2)→f_*(E_1 tensor E_2)','On conclut grâce à(1.7).',notes='Every affine ring, tensor base/index, Sup argument, immersion prime and reference inspected; no uncertain stroke required a second witness.')
r.page(233,'Corollaire1.9','g*L est de type fini.',notes='Both functors, cartesian square and all four labels, two negative-infinity alternatives, ordinary g* in the flat case and all statement word rules compared.',witness=244)
r.page(234,'Proposition1.11. Soit','quand f et g sont des immersions fermées.',notes='The printed diagonal f is preserved diplomatically and its current h has the composite map proof. The affine-space diagram has three hooked edges i,j,k; other arrowheads, E exponents, Cartesian incidence and comma were individually inspected.',witness=245)
r.page(235,'Preuve de a).','les corollaires que voici :',notes='Projection formula, stale reference, first f_* in proof(b), three ruled structure sheaves, exact proof labels and the triangular diagram’s small curved tail were all checked against the native witness.',witness=246)
r.commit()
