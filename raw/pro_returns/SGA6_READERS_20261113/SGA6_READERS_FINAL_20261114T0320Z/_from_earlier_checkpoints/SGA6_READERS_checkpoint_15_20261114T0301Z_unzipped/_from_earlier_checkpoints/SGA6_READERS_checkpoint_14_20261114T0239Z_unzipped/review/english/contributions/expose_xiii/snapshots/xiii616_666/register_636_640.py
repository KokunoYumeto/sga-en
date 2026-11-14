from pathlib import Path
import json,sys,hashlib
H=Path(__file__).resolve().parent;sys.path.insert(0,str(H))
from contribution import make_chunk
make_chunk('XIII',636,640)
b=json.loads((H/'batches.json').read_text());b=[x for x in b if x['first']!=636]
u=lambda p:json.loads((H/'source_packets'/str(p)/'units.json').read_text())
v=[]
def add(p,old,printed,s,mode='text'):v.append(dict(id=f'EN-CONTRIB-XIII-{len(v)+23:03}',page=p,old=old,printed=printed,source=s,mode=mode))
add(638,u(638)[14]+'-morphism',u(638)[14].replace('S_',"S'_")+'-morphism','fixes/MISPRINTS_6.json#606')
add(638,'by Abhyankar).','by Abhyankhar).','fixes/MISPRINTS_6.json#607')
add(639,'Consequently, '+u(639)[10]+' is bounded','Consequently, '+r'\(\mathcal L\)'+' is bounded','ASTRA-XIII-0025')
end='of Kummer theory the following fact of Grothendieck '
s=(H.parents[1]/'SGA6_EN_native_flattened_UNVERIFIED.tex').read_text();assert s.count(end)==1
b.append(dict(expose='XIII',first=636,last=640,native_start=b[-1]['native_end'],native_end=end,source='Exact reviewed French636–640 packets and frozen XIII decisions.',reason='Full finite-type power-map proof and hyperplane restriction argument, including all componentwise dimension hypotheses, normalization descent, Kummer diagram and author wording. Three source differences are explicit, and the newly noticed3.11 scope audit remains separate from both author bodies.',variants=v,notes=[dict(page=637,topic='French accent variant',decision='MISPRINT605 schema/schéma translates as scheme in both forms; no separate English lexical error is created.'),dict(page=639,topic='French misplaced accent',decision='MISPRINT608 graĉe/grâce translates as by in both forms with the same cited2.10 dependency; the French spelling correction has no English variant.'),dict(page=639,topic='Retained author scope audit',decision='Both source readings of Lemma3.11 and its proof are retained. An independent text/math audit identifies the immediate integral-fiber application and the standalone disjoint-union counterexample; no new hypothesis or theorem is inserted.',audit='author_claim_scope_639.json',audit_sha256=hashlib.sha256((H/'author_claim_scope_639.json').read_bytes()).hexdigest()),dict(page=636,topic='Cross-folio prose',decision='635 by the continues636 following easy lemma;636 We continues637 suppose;638 the continues639 class;639 the same continues640 in the two cases;640 using instead continues641 of Kummer theory. All joins retain the exact source boundary without adding a blank paragraph.'),dict(page=640,topic='Original full Kummer diagram',decision='Both exact rows, all maps, the lower H0 terms, multiplication labels and endpoint stop are retained as one literal mathematical unit. No diagram term is shortened or inferred.')]))
(H/'batches.json').write_text(json.dumps(b,ensure_ascii=False,indent=2)+'\n')
