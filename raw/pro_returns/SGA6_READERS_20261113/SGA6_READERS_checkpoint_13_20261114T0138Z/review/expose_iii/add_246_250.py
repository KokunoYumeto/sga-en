#!/usr/bin/env python3
import json,re
from review_helpers import Review,ROOT,base_text,underline_words
r=Review();batch='246_250'
r.finding(batch,1,'Individually ruled statement phrases, with the new predicates of4.1 left plain','All five primary pages and native248/250 were compared. The exact word spans are restored by the page patches below, including the title Formule de projection. The unruled definition predicates remain plain; the first relatively-to phrase and explanatory repetitions have their own observed rules.','Statements246–250',verdict='amended',change='Apply ASTRA-III-WORD-RULES-246 through250.')
r.finding(batch,2,'Comma after the cartesian square','The comma is visible at the right of the bottom row. All four arrows and their f/pr1/pr2 labels agree with the retained diagram.','Proof3.6 cartesian square')
why=('The primary and native pages print rel. à f in the proof, while the immediately preceding statement247 explicitly assumes finite amplitude relative to S. '
     'Write g:Y→S and h=g∘f. The tensor used in the proof is E tensor^L_{h^{-1}O_S}h^{-1}M. The structural map is the composite h^{-1}O_S=f^{-1}g^{-1}O_S→f^{-1}O_Y→O_X; '
     'relative amplitude for f instead uses f^{-1}O_Y. These are the exact scalar maps involved. '
     'The difference is witnessed by A=k[ε]/(ε²), S=SpecA, X=Y=Speck, f=id, E=k and M=k: E is free over O_Y, but the free A-resolution ...→A --ε→A --ε→A→k has kernel=image=(ε) and pulls back to zero differentials on k in every negative degree. '
     'Thus relative amplitude for f alone does not provide the asserted bounded tensor. The statement’s S hypothesis supplies the bounded flat resolution over h^{-1}O_S used here; its tensor with a bounded representative of M has total degrees in the sums of their finite degree intervals. '
     'Correct only this recalled base letter f→S in current. The statement itself, the adjunction counit, both canonical arrows and the alternative finite-amplitude hypothesis on M remain unchanged.')
r.finding(batch,3,'rel. à f (resp. finie)',why,'Proof3.7 recalled amplitude hypothesis',verdict='amended',change='Current only: rel. à f→rel. à S, restoring the stated hypothesis on247.',witness=259)
r.patch(248,'current',r"Supposons \(E\) (resp. \(M\)) d'amplitude plate finie rel. à \(f\)",r"Supposons \(E\) (resp. \(M\)) d'amplitude plate finie rel. à \(S\)",f'check/findings/findings_{batch}.json#3',why)
for x in r.decisions:
 if x['source_id']==f'check/findings/findings_{batch}.json#3' or x.get('related_finding')==f'check/findings/findings_{batch}.json#3':x['is_misprint']=True
(ROOT/'review/expose_iii/projection_amplitude_248.json').write_text(json.dumps(dict(source='check/findings/findings_246_250.json#3',printed='f',current='S',proof=why,images=['scan/SGA6_scan_360dpi.pdf#page=262','scan/SGA6_witness_300dpi.djvu#page=259'],statement_image='scan/SGA6_scan_360dpi.pdf#page=261'),ensure_ascii=False,indent=2)+'\n')
r.finding(batch,4,'First placeholder is a baseline full stop','Both scans place the first dot low on the baseline after the derived tensor, rather than at its vertical centre. Retain the typed full stop.','First functor placeholder in proof3.7',witness=259)
r.finding(batch,5,'Second placeholder is a baseline full stop','The second dot is independently visible low immediately before the closing parenthesis. Retain the same observed baseline glyph.','Second functor placeholder in proof3.7',witness=259)
r.finding(batch,6,'Page248 ends plat;249 begins(S=Spec(A))','Both complete primary pages were read. The attached marker already places plat on248 and the parenthetical identification on249.','Boundary248/249')
r.finding(batch,7,'Page250 ends localement composé','The primary and native250 pages both end with composé. The next page’s beginning will be separately read in its own full page record. Retain the attached boundary before d’une.','End of250',witness=261)
for page,count in [(248,3),(249,3),(250,1)]:
 id=f'ASTRA-III-STRUCTURE-{page}';why='Every structure sheaf on the complete page has an ordinary typed O with an individual lower rule. The exact counted replacements restore those observed rules while preserving all indices.'
 r.own_finding(id,page,'Ruled ordinary O',r'\mathcal O',r'\underline{O}',why,'All structure-sheaf symbols',kind='font',witness=page+11 if page!=249 else None)
 r.patch(page,'both',r'\mathcal O',r'\underline{O}',id,why,count=count)
id='ASTRA-III-AUTHOR-NOTES-247';why='The primary page has two raised parenthesized author calls,1 after the projection-formula title and2 after the M membership. Both complete notes are present; preserve their original call numbers and their full wording.'
r.own_finding(id,247,'Original author notes1 and2',r'Two ordinary \footnote calls','Use the exact original author note numbers.',why,'Proposition3.7 title and final membership',kind='symbol')
r.patch(247,'both',r'\footnote{cf. (H II 5.6).}',r'\SGAAuthorFootnote{1}{cf. (H II 5.6).}',id,why)
r.patch(247,'both',r"\footnote{L'indice",r"\SGAAuthorFootnote{2}{L'indice",id,why)

def current(page,layer):
 t=base_text(page,layer)
 for p in r.patches:
  if p['page']==page and p['layer'] in ['both',layer]:
   assert t.count(p['old'])==p['expected_count'],(page,layer,p['source_id']);t=t.replace(p['old'],p['new'])
 return t
def rules(text,phrases):
 pat='(?<![A-Za-zÀ-ÿ])('+'|'.join(map(re.escape,sorted(phrases,key=len,reverse=True)))+')(?![A-Za-zÀ-ÿ])'
 return re.sub(pat,lambda m:r'\uline{'+m[0]+'}',text)
for page in range(246,251):
 id=f'ASTRA-III-WORD-RULES-{page}';why='Restore only the word-group rules read on this complete page. Formula symbols and case labels remain separate; the newly introduced predicates of4.1 retain their printed unruled state.'
 r.own_finding(id,page,'Observed upright word-group rules','Plain statement prose and italic proof labels','Restore the inspected rules',why,'Statements and proof labels',witness=page+11 if page in [248,250] else None)
 for layer in ['diplomatic','current']:
  old=current(page,layer);new=old
  if page==246:
   a=new.index(r'\textbf{Proposition 3.6.}')+len(r'\textbf{Proposition 3.6.}')
   new=new[:a]+rules(new[a:],['Soit','un triangle commutatif de schémas','où','est une immersion fermée et','un morphisme lisse','et soit','Pour que',"soit localement d'amplitude plate finie rel.",'à','il faut et il suffit que',"soit localement d'amplitude plate finie",'au sens absolu','Plus précisément','si','est de dimension relative','on a'])
  elif page==247:
   a=new.index(r'\textbf{Proposition 3.7.}')+len(r'\textbf{Proposition 3.7.}')
   # Preserve both author-note texts outside the statement rule operation.
   part=new[a:];notes=[]
   for marker in [r'\SGAAuthorFootnote{1}{cf. (H II 5.6).}',r"\SGAAuthorFootnote{2}{L'indice «~qcoh~» indique la sous-catégorie pleine formée des complexes à cohomologie quasi-cohérente.}"]:
    assert part.count(marker)==1;notes.append(marker);part=part.replace(marker,f'@@NOTE{len(notes)}@@')
   part=rules(part,['Formule de projection','Soient','un schéma quasi-compact','un','morphisme quasi-compact et quasi-séparé de schémas quasi-compacts sur','Si','est',"d'amplitude plate finie",'ou si',"est d'amplitude plate finie rel.",'à','il'])
   for i,n in enumerate(notes,1):part=part.replace(f'@@NOTE{i}@@',n)
   new=new[:a]+part
  elif page==248:
   new=new.replace('existe un isomorphisme fonctoriel canonique de',r'\uline{existe un isomorphisme fonctoriel canonique de}',1)
  elif page==249:
   a=new.index(r'\textbf{Corollaire 3.7.1.}')+len(r'\textbf{Corollaire 3.7.1.}');b=new.index(r'\emph{Preuve.}',a)
   part=rules(new[a:b],['Soient','un schéma','un','morphisme quasi-compact et quasi-séparé de schémas quasi-compacts sur','Si',"est localement d'amplitude plate finie rel.",'à','il en est de même de','Plus précisément','si','est quasi-compact','et si','est un entier tel que','pour tout','et tout','Module quasi-cohérent','et','alors on a'])
   new=new[:a]+part+new[b:]
  elif page==250:
   a=new.index(r'\textbf{Corollaire 3.7.2.}')+len(r'\textbf{Corollaire 3.7.2.}');b=new.index(r'\emph{Preuve.}',a)
   part=rules(new[a:b],['Soit','un morphisme quasi-compact','quasi-séparé','et localement de tor-dimension finie','et soit','Si',"est localement d'amplitude plate finie",'au sens absolu','il en est de même de'])
   new=new[:a]+part+new[b:]
   a=new.index(r'\textbf{Définition 4.1.}')+len(r'\textbf{Définition 4.1.}');b=new.index(r'\textbf{Exemple 4.1.1.}',a)
   parts=new[a:b].split('On dit que');assert len(parts)==6
   parts[0]=rules(parts[0],['Soient','un morphisme localement de type fini de schémas','un intervalle de'])
   parts[1]=rules(parts[1],['est','relativement à','ou',"s'il n'y a pas d'ambiguïté","et l'on écrit",'si','est pseudo-cohérent',"et d'amplitude plate contenue dans"])
   # The parenthetical display's ou has no rule.
   parts[1]=parts[1].replace(r'\text{\uline{ou} }',r'\text{ou }')
   p=parts[2].split(r'si \(\underline{O}_X\)');assert len(p)==2
   parts[2]=rules(p[0],['ou de'])+r'\uline{si} \(\underline{O}_X\)'+rules(p[1],["est d'amplitude parfaite contenue dans"])
   parts[3]=rules(parts[3],['est',"s'il existe un intervalle","tel que l'on ait"])
   parts[4]=rules(parts[4],['est','si',"est localement d'amplitude parfaite finie rel.",'à'])
   # In the new predicate parfait rel. à f, à itself remains plain.
   parts[4]=parts[4].replace(r'parfait rel. \uline{à}',r'parfait rel. à')
   p=parts[5].split(r'si \(f\)');assert len(p)==2
   parts[5]=p[0]+r'\uline{si} \(f\)'+rules(p[1],['est',"localement d'amplitude parfaite finie"])
   new=new[:a]+r'\uline{On dit que}'.join(parts)+new[b:]
  new=new.replace(r'\emph{Preuve.}',r'\uline{Preuve}.');new,_=underline_words(new)
  assert new!=old,page;r.patch(page,layer,old,new,id,why)
r.page(246,'Proposition3.6. Soit','toramp(i_*(E)) contained in[a−d,b].',notes='All three triangle arrows including the curved i tail, small ob, the two separate amplitude implications, comma and final stop read.')
r.page(247,'Preuve. Si[m,n]est un intervalle de Z','il; author notes1 and2 complete',notes='All four square arrows, projection indices, diagonal section, plain derived L letters, headless identity comparison and both author notes compared. The projection-formula statement explicitly says relative to S.')
r.page(248,'existe un isomorphisme fonctoriel canonique de D(Y)_qcoh','où P est un A-module plat',notes='Both scans read in full: all derived categories, three ruled O letters, headed projection comparison, two canonical arrows, low placeholder dots and the f/S hypothesis error recorded with exact scalar maps and counterexample.',witness=259)
r.page(249,'(S=Spec(A)). Si l’on pose A-prime=D_A(P)','et l’on gagne grâce à(3.7).',notes='Base-change comparison, both named projections, three ruled O letters, both cohomology ranges and the independent upper bound b+N compared.')
r.page(250,'Corollaire3.7.2','Un morphisme localement d’intersection complète(i.e.localement composé',notes='Both scans read: every definition phrase, exact rule exceptions, the ruled structure sheaf, five On dit que clauses, −n/0 bounds and the opening complete-intersection example compared.',witness=261)
r.commit()
