#!/usr/bin/env python3
"""Write local, exactly anchored terminology, original notes and folio joins."""
from pathlib import Path
import csv,json,hashlib,sys,re
H=Path(__file__).resolve().parent
sys.path.insert(0,str(H.parents[1]))
from source_emphasis import braced
def sha(s):return hashlib.sha256(s.encode()).hexdigest()
def put(p,x):p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
def tsv(p,rows):
 with p.open('w',newline='') as f:
  w=csv.DictWriter(f,fieldnames=list(rows[0]),delimiter='\t',lineterminator='\n');w.writeheader();w.writerows(rows)
acc={'é':r"\'e",'è':r'\`e','à':r'\`a','ô':r'\^o','ê':r'\^e','â':r'\^a','î':r'\^i','û':r'\^u','ç':r'\c{c}'}
def anchor(s,w):
 for v in [w,''.join(acc.get(c,c) for c in w)]:
  if v in s:return v
 raise ValueError(w)
data=[
 (616,'régulier','regular'),
 (620,'polynôme de Hilbert','Hilbert polynomial'),
 (616,'faisceaux cohérents','coherent sheaves'),
 (617,'support','support'),
 (617,'diagramme commutatif','commutative diagram'),
 (619,'sous-faisceau','subsheaf'),
 (628,'polynômes universels','universal polynomials'),
 (621,'coefficients rationnels','rational coefficients'),
 (622,'famille de classes de faisceaux cohérents','family of classes of coherent sheaves'),
 (622,'limitée par le faisceau cohérent','bounded by the coherent sheaf'),
 (622,'limitée','bounded'),
 (623,'platitude générique','generic flatness'),
 (624,'composantes connexes','connected components'),
 (625,'suite exacte','exact sequence'),
 (626,"nombre d'intersection",'intersection number'),
 (626,'très ample','very ample'),
 (626,'faisceau inversible','invertible sheaf'),
 (651,'cohomologie','cohomology'),
 (631,'géométriquement intègres','geometrically integral'),
 (631,'géométriquement normales','geometrically normal'),
 (631,'foncteur de Picard','Picard functor'),
 (632,'morphismes de transition affines','affine transition morphisms'),
 (632,'localement de présentation finie','locally of finite presentation'),
 (633,'biunivoquement','bijectively'),
 (649,'morphisme surjectif','surjective morphism'),
 (635,'récurrence noethérienne','noetherian induction'),
 (637,'fidèlement plat','faithfully flat'),
 (638,'clôture algébrique','algebraic closure'),
 (638,'point générique','generic point'),
 (639,'groupe algébrique','algebraic group'),
 (640,'type multiplicatif','multiplicative type'),
 (643,'schéma en groupes','group scheme'),
 (643,'foncteurs en groupes commutatifs','commutative group functors'),
 (644,'algébriquement équivalent','algebraically equivalent'),
 (644,'numériquement équivalent','numerically equivalent'),
 (645,'corps de fonctions','function field'),
 (645,'formule de projection','projection formula'),
 (646,'présentation de Chow','Chow presentation'),
 (647,'immersion ouverte','open immersion'),
 (648,'immersion fermée','closed immersion'),
 (648,'limite','limit'),
 (648,'changement de base','base change'),
 (648,'générisation','generalization'),
 (648,'spécialisation','specialization'),
 (650,'représentable','representable'),
 (650,'groupes de Néron-Séveri',"N\\'eron-S\\'everi groups"),
 (651,'résolution des singularités','resolution of singularities'),
 (651,'équivalence numérique','numerical equivalence'),
 (651,'cohomologie étale',"\\'etale cohomology"),
 (651,'équivalence rationnelle','rational equivalence'),
 (652,'groupe fondamental modéré','tame fundamental group'),
 (652,'espace dual','dual space'),
 (654,'lignes et colonnes exactes','exact rows and columns'),
 (655,'cycle premier associé','associated prime cycle'),
 (657,'polynôme de Hilbert','Hilbert polynomial'),
 (658,'restent majorés','remain bounded above'),
 (658,'restent minorés','remain bounded below'),
 (658,'changement de base','base change'),
 (659,'extension transcendante pure','purely transcendental extension'),
 (659,'sections hyperplanes','hyperplane sections'),
 (660,'diviseur de Cartier','Cartier divisor'),
 (660,'éléments nilpotents','nilpotent elements'),
 (661,'indéterminée auxiliaire','auxiliary indeterminate'),
 (661,'idéal homogénéisé','homogenized ideal'),
 (662,'forme d\'intersection','intersection form'),
 (663,'diviseur effectif','effective divisor'),
 (663,'localement principale','locally principal'),
 (663,'normalisée','normalization'),
 (664,"l'éclatement",'blowup'),
 (664,'numériquement proportionnel','numerically proportional'),
 (665,'théorème de Bertini',"Bertini's theorem"),
]
rows=[]
for p,frword,enword in data:
 fr=(H/'source_packets'/str(p)/'current.tex').read_text();en=(H/'translations'/f'{p}.tex').read_text()
 try:fa=anchor(fr,frword);ea=anchor(en,enword)
 except ValueError as exc:raise ValueError((p,frword,enword,str(exc)))
 rows.append(dict(French_term=frword,English_rendering=enword,folio=p,French_exact_anchor=fa,English_exact_anchor=ea,French_anchor_occurrences=fr.count(fa),English_anchor_occurrences=en.count(ea),status='Manually selected local rendering with exact source anchors; aggregate terminology adjudication remains separate.'))
tsv(H/'terms.tsv',rows)

notes=[]
configs=json.loads((H/'batches.json').read_text())
for p in [616,631]:
 fr=(H/'source_packets'/str(p)/'current.tex').read_text()
 c=next(x for x in configs if x['first']<=p<=x['last'])
 raw=(H/f"EN_EXPOSE_XIII_P{c['first']}_{c['last']}.tex").read_text()
 def note(t):
  token=r'\SGAAuthorFootnote{*}'
  assert t.count(token)==1
  a=t.index(token)+len(token);return braced(t,a)[0]
 notes.append(dict(folio=p,label='*',geometry='baseline parenthesized asterisk in both call and label',call='after coherent on X before the sentence stop' if p==616 else 'after f.p.p.f. topology parenthesis before the sentence stop',English_text=note(raw),French_text=note(fr),English_command=r'\SGAAuthorFootnote{*}',source_id=f'ASTRA-XIII-NOTE-{p}-POSTFREEZE',source_evidence='author_note_labels_receipt.json; review/expose_xiii_amendments/own_findings.jsonl',rendering_evidence='Original notes directly inspected in probe635 corrected323/331 and probe655 corrected331; final PDF linkage in probe666/VISUAL_QA.json.'))
tsv(H/'author_notes.tsv',notes)

# These dispositions were compared from the actual reviewed packet tails/heads
# and their complete translations, rather than inferred from English sentence case.
paragraphs={616,619,621,622,626,627,628,637,641,643,644,648,651,652,653,656,657,658,659,660,661,662,664}
item_boundaries={632}
joins=[]
for p in range(616,666):
 fr_a=(H/'source_packets'/str(p)/'current.tex').read_text();fr_b=(H/'source_packets'/str(p+1)/'current.tex').read_text()
 en_a=(H/'translations'/f'{p}.tex').read_text();en_b=(H/'translations'/f'{p+1}.tex').read_text()
 source_break=bool(re.search(r'\n[ \t]*\n$',fr_a) or re.match(r'\n[ \t]*\n',fr_b))
 english_break=bool(re.search(r'\n[ \t]*\n$',en_a) or re.match(r'\s*\n[ \t]*\n',en_b))
 assert source_break==(p in paragraphs),(p,'source paragraph boundary',source_break)
 assert english_break==(p in paragraphs),(p,'English paragraph boundary',english_break)
 kind='explicit source paragraph break' if p in paragraphs else 'next enumerate item' if p in item_boundaries else 'continuing paragraph, statement or display'
 joins.append(dict(from_folio=p,to_folio=p+1,disposition=kind,French_tail=fr_a[-220:],French_head=fr_b[:220],English_tail=en_a[-180:],English_head=en_b[:180],source_a_sha256=sha(fr_a),source_b_sha256=sha(fr_b),translation_a_sha256=sha(en_a),translation_b_sha256=sha(en_b),added_blank_line=False,verification='Complete source-packet/translation boundary comparison; no additional image-reading claim.'))
put(H/'paragraph_join_audit_616_666.json',dict(scope='All50 internal XIII source-folio joins',counts={'joins':len(joins),'explicit_source_paragraph_breaks':len(paragraphs),'next_enumerate_item':len(item_boundaries),'other_continuations':50-len(paragraphs)-len(item_boundaries)},maker='Concatenates existing fragment endings without adding blank lines; first-item marker does not duplicate its newline.',joins=joins))
put(H/'INVENTORY_SCOPE.json',dict(scope='XIII616–666 only',selected_terminology_rows=len(rows),term_count_definition='One manually selected French/English local rendering with a stated folio and exact validated anchors; not a count of all source words or a semantic-completeness claim.',original_author_note_records=len(notes),note_count_definition='The two original notes in the inspected interval, on616 and631; each has an explicit shared star call/label and complete text.',internal_folio_joins=len(joins),cross_volume_semantic_alignment_complete=False))
print(json.dumps(dict(selected_terms=len(rows),author_notes=len(notes),folio_joins=len(joins))))
