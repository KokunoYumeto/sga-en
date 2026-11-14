from pathlib import Path
import json,sys
H=Path(__file__).resolve().parent;sys.path.insert(0,str(H))
from contribution import make_chunk
make_chunk('XIII',626,630)
b=json.loads((H/'batches.json').read_text());b=[x for x in b if x['first']!=626]
u=lambda p:json.loads((H/'source_packets'/str(p)/'units.json').read_text())
v=[]
def add(p,old,printed,s,mode='text'):v.append(dict(id=f'EN-CONTRIB-XIII-{len(v)+11:03}',page=p,old=old,printed=printed,source=s,mode=mode))
add(626,u(626)[31],u(626)[31].replace('c_1(L)','c(L)'),'fixes/MISPRINTS_6.json#591')
add(626,'(with '+u(626)[35]+' zeros)','(with '+r'\(r-1\)'+' zeros)','ASTRA-XIII-0018')
add(627,'By 1.7 and 2.5,','By 1.7 and 2.6,','fixes/MISPRINTS_6.json#592')
add(628,u(628)[2],u(628)[2].replace('2))=0','2)=0'),'fixes/MISPRINTS_6.json#593')
add(628,u(628)[12],u(628)[12].replace('-\\beta(\\beta+1)','+\\beta(\\beta+1)'),'fixes/MISPRINTS_6.json#594','display')
add(629,'for '+u(629)[37]+', '+u(629)[38]+' (see FGA','for '+u(629)[37]+', '+u(629)[38].replace('L(-n)','L(n)')+' (see FGA','fixes/MISPRINTS_6.json#595')
add(630,u(630)[25],u(630)[25].replace('m-1+j','m-1+i'),'fixes/MISPRINTS_6.json#597','display')
end='one has\n\\[\na_i^{(m)}=P_i^{(m,r)}(a_r,\\ldots,a_i).\n\\]'
s=(H.parents[1]/'SGA6_EN_native_flattened_UNVERIFIED.tex').read_text();assert s.count(end)==1
b.append(dict(expose='XIII',first=626,last=630,native_start=b[-1]['native_end'],native_end=end,source='Both exact reviewed French626–630 packets, frozen review/xiii patch stream and coordinator manual replay.',reason='Complete technical-lemma proofs and literal polynomial/cohomology bounds. Restores source inline/display placement and source lemma2.7 numbering while retaining the inherited nonprinting stable target IDs. Seven exact source/current differences are branched with their separately adjudicated proofs.',variants=v,notes=[dict(page=627,topic='Printed labels and stable target IDs',decision='Source lemma2.7 and formula labels2.7.1/2.7.2 are preserved in both English forms. Native stable target IDs ending2-6,2-6-1,2-6-2 are retained at those exact results solely for hyperlink continuity; no printed2.6 label is invented.'),dict(page=629,topic='Source sequence and twists',decision='The full dualizing-sheaf construction, exact hyperplane sequence, all degrees and both induction arguments are translated literally. The current-only final negative twist is scoped to the FGA eventual-vanishing sentence, preserving all other occurrences.'),dict(page=630,topic='French lexical spelling',decision='MISPRINT596 quelque soit/quel que soit has the same intended quantification; both English forms read for any. The source lexical correction remains recorded without an invented English variant.'),dict(page=630,topic='Paragraph continuity',decision='The opening already proved continues629 Thus, by(i), with no blank paragraph. The final polynomial equality continues into631 with its coefficient conclusion, preserving the exact display boundary.')]))
(H/'batches.json').write_text(json.dumps(b,ensure_ascii=False,indent=2)+'\n')
