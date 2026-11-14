#!/usr/bin/env python3
"""Write source-anchored terminology and original-note inventories for VII only."""
from pathlib import Path
import json,csv,hashlib
HERE=Path(__file__).resolve().parent
def sha(s):return hashlib.sha256(s.encode()).hexdigest()
data=[
 (416,'complexe de Koszul','Koszul complex','complexe de Koszul','Koszul complex'),
 (416,'algèbre extérieure','exterior algebra','algèbre extérieure','exterior algebra'),
 (416,'multiplication intérieure','interior multiplication','multiplication intérieure','interior multiplication'),
 (416,'antidérivation','antiderivation','antidérivation','antiderivation'),
 (416,'dual','dual','dual','dual'),
 (416,'homomorphisme régulier','regular homomorphism','homomorphisme régulier','regular homomorphism'),
 (416,'changement de base','base change','changement de base','base change'),
 (419,'préschéma','prescheme','préschémas','preschemes'),
 (419,'immersion fermée','closed immersion','immersion fermée','closed immersion'),
 (419,'suite régulière','regular sequence','suite régulière','regular sequence'),
 (419,'quasi-régulier','quasi-regular','quasi-régulière','quasi-regular'),
 (419,'système minimum de générateurs','minimum system of generators','système minimum de générateurs','minimum system of generators'),
 (420,'changement de base plat','flat base change','changement de base plat','flat base change'),
 (420,'topologie fidèlement plate quasi-compacte','faithfully flat quasi-compact topology','topologie fidèlement plate quasi-compacte','faithfully flat quasi-compact topology'),
 (421,'faisceau conormal','conormal sheaf','faisceau conormal','conormal sheaf'),
 (421,'codimension','codimension','codimension','codimension'),
 (421,'suite exacte','exact sequence','suite exacte','exact sequence'),
 (422,'localement scindée','locally split','localement scindée','locally split'),
 (423,'suite spectrale de transitivité','transitivity spectral sequence','suite spectrale de transitivité','transitivity spectral sequence'),
 (425,'fibré projectif','projective bundle','fibré projectif','projective bundle'),
 (425,'morphisme structural','structural morphism','morphisme structural','structural morphism'),
 (428,'dimension cohomologique','cohomological dimension','dimension cohomologique','cohomological dimension'),
 (428,'résolution partielle graduée','partial graded resolution','résolution partielle graduée','partial graded resolution'),
 (430,'associatif','associative','associative','associative'),
 (430,'fonctorialité','functoriality','fonctorialité','functoriality'),
 (430,'alterné','alternating','alternée','alternating'),
 (441,'faisceaux d’homologie','homology sheaves',"faisceaux d'homologie",'homology sheaves'),
 (441,'somme alternée','alternating sum','somme alternée','alternating sum'),
 (442,'morphisme canonique','canonical morphism','morphisme canonique','canonical morphism'),
 (443,'présentation finie graduée','finite graded presentation','présentation finie graduée','finite graded presentation'),
 (443,'localement libre de type fini','locally free of finite type','localement libres de type fini','locally free of finite type'),
 (444,'formule de projection','projection formula','formule de projection','projection formula'),
 (445,'inverse à gauche','left inverse','inverse à gauche','left inverse'),
 (446,'anneau local','local ring','anneau local','local ring'),
 (446,'élément régulier','regular element','élément régulier','regular element'),
 (447,'faisceau cohérent','coherent sheaf','faisceaux cohérents','coherent sheaves'),
 (447,'triangle distingué','distinguished triangle','triangle distingué','distinguished triangle'),
 (447,'support','support','support','supported'),
 (453,'modulo torsion','modulo torsion','modulo torsion','modulo torsion'),
 (453,'opérations de puissance extérieure','exterior-power operations','opérations de puissance extérieure','exterior-power operations'),
 (453,'complexes parfaits','perfect complexes','complexes parfaits','perfect complexes'),
 (454,'nilidéal','nil ideal','nilidéal','nil ideal'),
 (454,'idéal localement nilpotent','locally nilpotent ideal','idéal localement nilpotent','locally nilpotent ideal'),
 (454,'augmentation','augmentation','augmentation','augmentation'),
 (454,'fonction localement constante','locally constant function','fonction localement constante','locally constant function'),
 (454,'filtration discrète','discrete filtration','est discrète','is discrete'),
 (456,'homomorphisme additif','additive homomorphism','homomorphisme additif','additive homomorphism'),
 (457,'indéterminée','indeterminate','indéterminée','indeterminate'),
 (459,'homomorphisme','homomorphism','homomorphisme','homomorphism'),
 (460,'gradués associés','associated gradeds','gradués associés','associated gradeds'),
 (461,'morphisme d’intersection complète','complete-intersection morphism',"morphisme d'intersection complète",'complete-intersection morphism'),
 (461,'dimension virtuelle relative','virtual relative dimension','dimension virtuelle relative','virtual relative dimension'),
 (464,'filtration topologique','topological filtration','filtration « topologique »','``topological\'\' filtration'),
 (464,'récurrence noethérienne','noetherian induction','récurrence noethérienne','noetherian induction'),
 (464,'sous-schémas fermés intègres','integral closed subschemes','sous-schémas fermés intègres','integral closed subschemes'),
 (465,'point générique','generic point','point générique','generic point'),
 (465,'surjection','surjection','surjection','surjection'),
]
# One source occurrence for the indeterminate is on456, before its use on457.
data=[(456,*x[1:]) if x[0]==457 and x[1]=='indéterminée' else x for x in data]
rows=[]
for page,frterm,enterm,franchor,enanchor in data:
    fr=(HERE/'source_packets'/str(page)/'current.tex').read_text()
    en=(HERE/'translations'/f'{page}.tex').read_text()
    assert franchor in fr,(page,'French',franchor)
    assert enanchor in en,(page,'English',enanchor)
    rows.append(dict(French_term=frterm,English_rendering=enterm,folio=page,French_exact_anchor=franchor,English_exact_anchor=enanchor,French_anchor_occurrences=fr.count(franchor),English_anchor_occurrences=en.count(enanchor),status='Manually selected and exact-source anchored local rendering; cross-volume terminology audit remains pending.'))
with (HERE/'terms.tsv').open('w',newline='') as f:
    w=csv.DictWriter(f,fieldnames=list(rows[0]),delimiter='\t',lineterminator='\n');w.writeheader();w.writerows(rows)
note=dict(folio=430,label='1',geometry='raised numeral within baseline parentheses',call='after the semicolon in condition2.2(a), inside the array',English_text='One can show that such a resolution always exists.',French_text="On peut montrer qu'une telle résolution existe toujours.",English_commands=r'\SGAAuthorFootMark{1} / \SGAAuthorFootText{1}',source_id='ASTRA-VII-NOTE-430-POSTFREEZE',source_evidence='review/expose_vii_amendments/author_note_430.json; own exact regional check in author_note_430.json',rendering_evidence='probe451/VISUAL_QA.json, corrected output225: complete note and call share the page')
with (HERE/'author_notes.tsv').open('w',newline='') as f:
    w=csv.DictWriter(f,fieldnames=list(note),delimiter='\t',lineterminator='\n');w.writeheader();w.writerow(note)
summary=dict(scope='VII416–465 contribution only',terms=len(rows),term_count_definition='One row per manually selected French/English lexical pair with a stated folio and validated exact text anchors. This is neither a count of all source words nor a semantic-completeness assertion.',author_note_records=1,author_note_count_definition='The complete reviewed VII interval contains one original note call and one corresponding full text, both on source430; explicit labels follow the separate directly inspected amendment.',cross_volume_semantic_alignment_complete=False)
(HERE/'INVENTORY_SCOPE.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(summary,ensure_ascii=False))
