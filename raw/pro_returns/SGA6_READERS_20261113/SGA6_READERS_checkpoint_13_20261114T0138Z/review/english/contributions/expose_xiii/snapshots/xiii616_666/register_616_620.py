from pathlib import Path
import json,sys
H=Path(__file__).resolve().parent
sys.path.insert(0,str(H))
from contribution import make_chunk
C=make_chunk('XIII',616,620)
units=lambda p:json.loads((H/'source_packets'/str(p)/'units.json').read_text())
v=[]
def add(page,old,printed,source,mode='text'):
 v.append(dict(id=f'EN-CONTRIB-XIII-{len(v)+1:03}',page=page,old=old,printed=printed,mode=mode,source=source))
add(617,units(617)[16],units(617)[16].replace('H^0(G(n+1)) \\arrow[d]','H^0(G(n+1) \\arrow[d]'),'fixes/MISPRINTS_6.json#553','display')
add(618,'by 1.3 (i).','by 2.3 (i).','fixes/MISPRINTS_6.json#554')
add(619,'by 1.3 (ii);','by 2.3 (ii);','fixes/MISPRINTS_6.json#555')
add(619,units(619)[6],r'\(\mapsto n^1(F(n))\)','fixes/MISPRINTS_6.json#556')
add(620,r'the open subset of \(S\prime\)',r'the open subset of \(S\)','fixes/MISPRINTS_6.json#557')
v[-1]['old']=r"the open subset of \(S'\)"
add(620,units(620)[18],units(620)[18].replace('F(-1)','F(1)'),'fixes/MISPRINTS_6.json#558')
native=(H.parents[1]/'SGA6_EN_native_flattened_UNVERIFIED.tex').read_text()
start=r'\sgaStableTarget{sga6.e13.expose}'
end='with \\(G\\) a \\((b_1,\\ldots,b_r)\\)-sheaf and\n'
assert native.count(end)==1
config=dict(expose='XIII',first=616,last=620,native_start=start,native_end=end,source='Exact coordinator page_packets616–620 plus frozen review/xiii and middle patches, in both layers.',reason='Complete source-aligned reconstruction of the first five XIII folios, retaining all original theorem wording, inline/display placement, diagram objects and arrows, original footnote, plain body O and separately ruled note O, exact reference variants and explicit stable target positions.',variants=v,notes=[dict(page=616,topic='Original author footnote',decision='Full original note translated at its exact source call; bare source label awaits separately requested observation before final rendering. No note-number inference is made.'),dict(page=617,topic='Diagram transport',decision='All three exact reviewed diagrams are kept as literal mathematical units. The missing close in the617 lower-right term is a complete-display variant, retaining TikZ ampersands outside macro arguments.'),dict(page=619,topic='Source replay',decision='Both source endpoints sigma_i in1.5.2 and1.6(i) are retained; coordinator replay14/15 confirm those exact supplied readings without a further variant.'),dict(page=620,topic='Paragraph continuity',decision='The final display continues into621 with the qualifying sheaf clause; the maker adds no blank line at this boundary. The617 display is likewise immediately followed by the618 explanatory where clause.'),dict(page=616,topic='Continuation macros',decision='Root’s sealed XII supplies the exact reviewed post615 XIII macro block. This chunk begins at e13.expose and does not duplicate or move that preceding state.')])
(H/'batches.json').write_text(json.dumps([config],ensure_ascii=False,indent=2)+'\n')
