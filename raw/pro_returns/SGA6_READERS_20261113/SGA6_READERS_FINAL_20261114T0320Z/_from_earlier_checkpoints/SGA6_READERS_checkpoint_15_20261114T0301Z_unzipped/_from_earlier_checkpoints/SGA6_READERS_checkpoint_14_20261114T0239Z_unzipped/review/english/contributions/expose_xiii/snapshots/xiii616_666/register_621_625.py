from pathlib import Path
import sys,json
H=Path(__file__).resolve().parent
sys.path.insert(0,str(H))
from contribution import make_chunk
make_chunk('XIII',621,625)
b=json.loads((H/'batches.json').read_text()); b=[x for x in b if x['first']!=621]
u=lambda p:json.loads((H/'source_packets'/str(p)/'units.json').read_text())
v=[]
def add(page,old,printed,source,mode='text'):v.append(dict(id=f'EN-CONTRIB-XIII-{len(v)+7:03}',page=page,old=old,printed=printed,source=source,mode=mode))
add(621,u(621)[11],u(621)[11].replace('b_1','b_i'),'fixes/MISPRINTS_6.json#587')
add(622,u(622)[2],r'\(m=0\)','ASTRA-XIII-0008')
add(624,u(624)[22],u(624)[22].replace('m)))','m))'),'fixes/MISPRINTS_6.json#589')
add(625,u(625)[15],u(625)[15].replace('L_{1,K}',"L'_K"),'fixes/MISPRINTS_6.json#590')
end='\\[\n\\bigl\\langle c_1(L_1)\\cdots c_1(L_s)\\cdot Y\\bigr\\rangle\n\\]'
native=(H.parents[1]/'SGA6_EN_native_flattened_UNVERIFIED.tex').read_text();assert native.count(end)==1
b.append(dict(expose='XIII',first=621,last=625,native_start=b[-1]['native_end'],native_end=end,source='Both exact reviewed French page packets621–625, frozen review/xiii patches and coordinator source replay.',reason='Complete transfer of the (b)-polynomial argument, bounded-family definition, all five equivalent conditions and full proof, including the exact universal presentation and source inline/display placement. Four current-only source differences are branched.',variants=v,notes=[dict(page=622,topic='Source proof versus inherited English expansion',decision='Restore the literal m≥0 only in current and m=0 diplomatically. Native m=c0≥0 is not copied into the author body; the equality and skyscraper counterexample remain in the independent source proof. The added native separate c_i estimate is omitted because the source proceeds directly from the displayed upper bound to regularity.'),dict(page=624,topic='Spacing-only correction',decision='Printed derang is retained as the two words de rang by source decision MISPRINT588 under the checker spacing convention; both English forms use of rank and no variant is invented.'),dict(page=623,topic='Paragraph continuity',decision='The final Then, continues immediately into624;624 Indeed, continues immediately into625. No extra blank line is inserted at either folio boundary.'),dict(page=625,topic='Boundary into626',decision='The source sentence ends this folio immediately before the intersection-number display. English preserves this exact mathematical boundary, with the lexical phrase Recall that we denote by continuing into626.')]))
(H/'batches.json').write_text(json.dumps(b,ensure_ascii=False,indent=2)+'\n')
