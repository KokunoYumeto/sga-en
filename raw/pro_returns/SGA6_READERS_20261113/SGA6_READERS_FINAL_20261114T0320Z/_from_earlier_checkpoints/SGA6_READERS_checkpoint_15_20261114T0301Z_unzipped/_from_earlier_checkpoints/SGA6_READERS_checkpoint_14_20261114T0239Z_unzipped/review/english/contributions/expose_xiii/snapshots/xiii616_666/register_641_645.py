from pathlib import Path
import json,sys
H=Path(__file__).resolve().parent;sys.path.insert(0,str(H))
from contribution import make_chunk
make_chunk('XIII',641,645)
b=json.loads((H/'batches.json').read_text());b=[x for x in b if x['first']!=641]
u=lambda p:json.loads((H/'source_packets'/str(p)/'units.json').read_text())
v=[]
def add(p,old,printed,s,mode='text'):v.append(dict(id=f'EN-CONTRIB-XIII-{len(v)+26:03}',page=p,old=old,printed=printed,source=s,mode=mode))
add(643,'a connected '+u(643)[13]+'-scheme','a connected '+r'\(k\)'+'-scheme','fixes/MISPRINTS_6.json#617')
add(644,u(644)[0],u(644)[0].replace('\\Phi^{-1}','\\Phi'),'fixes/MISPRINTS_6.json#618')
add(644,u(644)[12]+', under the hypotheses of 3.8)',u(644)[12]+')','ASTRA-XIII-0030')
end='\\[\n\\chi(F\\otimes L)=\\chi(F).\n\\]'
s=(H.parents[1]/'SGA6_EN_native_flattened_UNVERIFIED.tex').read_text();assert s.count(end)==1
b.append(dict(expose='XIII',first=641,last=645,native_start=b[-1]['native_end'],native_end=end,source='Both exact reviewed French641–645 packets and frozen XIII source/proof decisions.',reason='Complete group-scheme and boundedness definitions, all four3.13 equivalences and their full proof, exact characteristic/source group functor notation, algebraic/tau/numerical equivalence and functoriality. Three current-only source changes are transferred with exact maps and the approved full3.8 qualification.',variants=v,notes=[dict(page=641,topic='French agreement',decision='MISPRINT616 ample/amples modifies an adjective whose English form is ample for either number. Both English forms retain the same two explicitly named ample sheaves; no English variant is invented.'),dict(page=644,topic='Source-supported substantive qualification',decision='The current-only phrase under the hypotheses of3.8 transfers exactly ASTRA-XIII-0030, already independently approved by coordinator. Its full source proof identifies f* and the required finite-type inverse-image map, with the P1-to-point counterexample; no additional hypothesis is supplied by the translation.'),dict(page=645,topic='French gender retained',decision='The source reviewer retained surjective in both French forms as application-compatible wording. Both English forms naturally use surjective for the same morphism, with no content difference.'),dict(page=643,topic='Defined-term typography',decision='Exact source underlined lexical groups in4.4 are preserved independently from the plain tau in tau-equivalent; formula commands remain literal. Statement emphasis is carried from the current reference and remains subject to the coordinator’s separate global typography closure.'),dict(page=641,topic='Boundary continuations',decision='641 begins within the item opened640;642(ii)implies continues643(i);645item(ii) continues with the exact646 Euler-characteristic display. No extra folio paragraph is inserted.')]))
(H/'batches.json').write_text(json.dumps(b,ensure_ascii=False,indent=2)+'\n')
