from pathlib import Path
import json,sys,hashlib,re
H=Path(__file__).resolve().parent;sys.path.insert(0,str(H))
from contribution import make_chunk
make_chunk('XIII',646,650)
b=json.loads((H/'batches.json').read_text());b=[x for x in b if x['first']!=646]
u=lambda p:json.loads((H/'source_packets'/str(p)/'units.json').read_text())
v=[]
def add(p,old,printed,s,mode='text'):v.append(dict(id=f'EN-CONTRIB-XIII-{len(v)+29:03}',page=p,old=old,printed=printed,source=s,mode=mode))
add(647,u(647)[20],u(647)[20].replace('^{\\otimes p}','^{\\otimes r}'),'fixes/MISPRINTS_6.json#609')
add(649,u(649)[26],u(649)[26].replace('X_{S\'}','X_S'),'fixes/MISPRINTS_6.json#611')
end='integral over \\(S\\), with two-dimensional fibers, and replace \\(X\\) by\n'
s=(H.parents[1]/'SGA6_EN_native_flattened_UNVERIFIED.tex').read_text();assert s.count(end)==1
block=(H/'source_packets/650/current.tex').read_text().split('% Added in pages 654--669',1)[1].split('\\subsection*',1)[0]
macro='% Added in pages 654--669'+block
(H/'continuation_macros_650.json').write_text(json.dumps(dict(page=650,status='reviewed source-local macro block preserved literally',native='The exact native replacement span contains no corresponding local macro block before section5.',reviewed_block=macro,reviewed_sha256=hashlib.sha256(macro.encode()).hexdigest(),placement='Between Remark4.8 and section5, at its actual reviewed source location.'),ensure_ascii=False,indent=2)+'\n')
b.append(dict(expose='XIII',first=646,last=650,native_start=b[-1]['native_end'],native_end=end,source='Both exact reviewed French646–650 packets and frozen XIII source/proof decisions.',reason='Complete remaining4.6 conditions and proof, all three4.7 claims and descent/generalization/specialization proof, exact4.8 uncertainty, and complete5.1 opening. The represented Pic scheme spelling is retained with the source identification, and the reviewed six-command local macro block is preserved.',variants=v,notes=[dict(page=649,topic='French participle spelling',decision='MISPRINT610 établit/établi has the same English rendering established in both forms, with the identical cited equivalence and conclusion(a).'),dict(page=650,topic='Representing Picard scheme notation',decision='MISPRINT612 and checker646650#14 were rejected/reverted: the exact representability isomorphism h_P≅Pic^tau identifies the K-fibre of the explicitly chosen representing scheme with the scheme whose connected components are counted. Plain Pic in that one expression is preserved in both English forms.'),dict(page=648,topic='Printed parenthetical addition',decision='Preserve open (resp. and closed): the inverse-image subscheme S0 is the same object, with case(ii) adding closedness. No redundant English expansion is inserted.'),dict(page=650,topic='Continuation macro state',decision='The exact reviewed six-command block between4.8 and section5 is preserved and hashed in continuation_macros_650.json; no corresponding local native block is discarded.'),dict(page=646,topic='Source folio continuity',decision='646 opens with the exact equality begun by the preceding item;646/647 continues then/by4.5,647/648 continues the same underlined statement,649/650 continues just/one Hilbert polynomial, and650/651 continues which is/still integral. No extra folio paragraph is inserted.')]))
(H/'batches.json').write_text(json.dumps(b,ensure_ascii=False,indent=2)+'\n')
