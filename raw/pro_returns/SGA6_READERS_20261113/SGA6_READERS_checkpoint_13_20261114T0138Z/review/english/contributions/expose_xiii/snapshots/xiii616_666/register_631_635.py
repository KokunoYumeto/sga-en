from pathlib import Path
import json,sys
H=Path(__file__).resolve().parent;sys.path.insert(0,str(H))
from contribution import make_chunk
make_chunk('XIII',631,635)
b=json.loads((H/'batches.json').read_text());b=[x for x in b if x['first']!=631]
u=lambda p:json.loads((H/'source_packets'/str(p)/'units.json').read_text())
v=[]
def add(p,old,printed,s,mode='text'):v.append(dict(id=f'EN-CONTRIB-XIII-{len(v)+18:03}',page=p,old=old,printed=printed,source=s,mode=mode))
add(631,u(631)[16],u(631)[16].replace('\\sup','\\operatorname{supp}'),'fixes/MISPRINTS_6.json#599')
add(632,'the pullback of '+u(632)[15]+', where','the pullback of '+u(632)[15].replace("L'","L")+', where','fixes/MISPRINTS_6.json#600')
add(632,'the pullback of '+u(632)[26]+' to '+u(632)[27],'the pullback of '+u(632)[26]+'. to '+u(632)[27],'fixes/MISPRINTS_6.json#601')
add(635,u(635)[33],u(635)[33].replace("X'",'X'),'fixes/MISPRINTS_6.json#603')
add(635,u(635)[34],u(635)[34].replace("X'",'X'),'fixes/MISPRINTS_6.json#604')
end='following easy lemma, then for \\(X_{S\'}/S\'\\) by '
s=(H.parents[1]/'SGA6_EN_native_flattened_UNVERIFIED.tex').read_text();assert s.count(end)==1
b.append(dict(expose='XIII',first=631,last=635,native_start=b[-1]['native_end'],native_end=end,source='Exact reviewed French631–635, frozen XIII and separate explicit note amendment631.',reason='Restores complete bounded-family criteria, source Picard-functor descent proof and all equivalent subset statements, preserving plain versus underlined Pic at each occurrence, exact diagrams, original note and source-statement word groups. Five explicit source differences are branched.',variants=v,notes=[dict(page=631,topic='Original author note',decision='Full SGA3/FGA232 note and its exact fpqc-to-fppf statement are translated. Both forms use observed baseline parenthesized star under ASTRA-XIII-NOTE-631-POSTFREEZE; fresh source reading is attributed in author_note_labels_receipt.json.'),dict(page=631,topic='Hyphenation-only source row',decision='MISPRINT598 is reverted in the frozen source under the checker hyphenation convention. Both English forms use S-scheme with the same structure morphism; no content variant is created.'),dict(page=634,topic='Source typo Ia',decision='MISPRINT602 identifies capital I for L in the French article La. Both English forms use The, preserving the same family and its pullback; no invented English typo is introduced.'),dict(page=634,topic='Short source sheaf-family wording',decision='The source says classes of sheaves in the target family, with no added invertible adjective. English preserves this wording; the frozen Picard inverse-image identification remains in source records.'),dict(page=632,topic='Cross-folio statement scope',decision='The open emph scope from631 continues into632 without a blank paragraph. The633 item marker is placed after the actual item command. The633 and634 displayed statements continue into the following folios, and635 by the continues636 without an added blank.')]))
(H/'batches.json').write_text(json.dumps(b,ensure_ascii=False,indent=2)+'\n')
