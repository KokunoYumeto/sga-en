from pathlib import Path
import json,sys,hashlib
H=Path(__file__).resolve().parent;sys.path.insert(0,str(H))
from contribution import make_chunk
u=lambda p:json.loads((H/'source_packets'/str(p)/'units.json').read_text())
lp=json.loads((H/'lexical_math_pairs.json').read_text());lp=[p for p in lp if p['page']<661]
for p,i,old,new,src in [(661,20,"\\text{degr\\'e}",r'\text{degree}','reviewed degree bound6.14'),(661,26,"\\text{degr\\'e}",r'\text{degree}','reviewed degree equality6.14'),(662,7,r'\uline{et}',r'\uline{and}','ASTRA-XIII-0058'),(665,7,r'\uline{et}',r'\uline{and}','ASTRA-XIII-0059')]:
 assert old in u(p)[i]
 lp.append(dict(page=p,layer='both',French_literal_unit=u(p)[i],English_literal_unit=u(p)[i].replace(old,new),expected_multiplicity=1,status='Exact complete-unit lexical translation only: degree or the separately underlined conjunction and; every mathematical command, bound, argument, punctuation and whitespace outside that word remains literal.',source=src))
(H/'lexical_math_pairs.json').write_text(json.dumps(lp,ensure_ascii=False,indent=2)+'\n')
make_chunk('XIII',661,666)
b=json.loads((H/'batches.json').read_text());b=[x for x in b if x['first']!=661]
v=[]
def add(p,old,printed,s,mode='text',related=None):
 d=dict(id=f'EN-CONTRIB-XIII-{len(v)+41:03}',page=p,old=old,printed=printed,source=s,mode=mode)
 if related:d['related_sources']=related
 v.append(d)
add(661,'(G. Hermann).','(I. Hermann).','ASTRA-XIII-0066')
add(661,'every ideal '+u(661)[3]+' of','every ideal of','fixes/MISPRINTS_6.json#626')
add(661,u(661)[34],u(661)[34].replace('^{N}','^{n}'),'fixes/MISPRINTS_6.json#629')
add(661,u(661)[35],u(661)[35].replace('f_i','{}_i'),'fixes/MISPRINTS_6.json#630')
add(663,u(663)[13],u(663)[13].replace('(p-1)\\bigr)','(p-1)'),'fixes/MISPRINTS_6.json#631')
add(664,u(664)[7],u(664)[7].replace('{O}_X','{O}_Y'),'fixes/MISPRINTS_6.json#632')
add(664,'not numerically proportional to','not numerically equivalent to','ASTRA-XIII-0064')
add(664,u(664)[27],u(664)[27].replace('M^{\\otimes h}','M^{\\otimes n}'),'fixes/MISPRINTS_6.json#634')
add(665,'not numerically proportional to','not numerically equivalent to','ASTRA-XIII-0065')
add(666,'is integral,','is int\\underline{egr}al,','fixes/MISPRINTS_6.json#671')
add(666,'Pathologies III, Amer. J. Math 1967 p. 94-104.','Pathologies III, Amer. J. Math 1967 p. 94-103 Amer. J. Math 1967 p.94-103.','fixes/MISPRINTS_6.json#673',related=['ASTRA-XIII-0067'])
add(666,"Grothendieck A. and Dieudonn\\'e J.","Grothendieck A. . and Dieudonn\\'e J.",'fixes/FIXLOG_6_CURRENT.jsonl#556')
add(666,'Grothendieck A. et alii','Grothendieck A. . et alii','fixes/FIXLOG_6_CURRENT.jsonl#557')
add(666,'I.H.E.S.','J.H.E.S.','fixes/MISPRINTS_6.json#674')
end=r'\sgaStableTarget{sga6.e14.expose}'
s=(H.parents[1]/'SGA6_EN_native_flattened_UNVERIFIED.tex').read_text();assert s.count(end)==1
macro=(H/'source_packets/666/current.tex').read_text().split('% Exposé XIV local notation',1)[1]
macro='% Exposé XIV local notation'+macro
e=(H/'EN_EXPOSE_XIII_P661_666.tex').read_text();a=e.index('% Expos')
e=e[:a]+macro;(H/'EN_EXPOSE_XIII_P661_666.tex').write_text(e)
# Keep the source macro comment/block byte-identical in the reusable fragment too.
t=H/'translations/666.tex';tt=t.read_text();tt=tt[:tt.index('% Expos')]+macro;t.write_text(tt)
(H/'XIII_XIV_boundary_macros.json').write_text(json.dumps(dict(boundary='666/667',reviewed_block=macro,reviewed_block_sha256=hashlib.sha256(macro.encode()).hexdigest(),native_boundary='No native local macro block follows the XIII bibliography before e14.expose.',preservation='Reviewed four-command block is retained literally at its source location. providecommand semantics are preserved; actual aggregate uses require source-local macro-state checks.',earlier_native_definitions={'Kb':r'\mathrm K','Db':r'\mathrm D'},observed_XIV_Kb_uses=0),ensure_ascii=False,indent=2)+'\n')
b.append(dict(expose='XIII',first=661,last=666,native_start=b[-1]['native_end'],native_end=end,source='Both exact reviewed French661–666 packets and frozen XIII source/proof/bibliographic decisions.',reason='Complete Hermann ideal-bound proof, full Hodge-index theorem and all reductions, both strict numerical inequalities with the exact approved nonproportionality corrections, full final bibliography and reviewed XIV boundary macros. Every printed/corrected mathematical difference is explicit, including the two separate bibliography defects within one complete reference branch.',variants=v,notes=[dict(page=661,topic='French agreement and spelling',decision='MISPRINT627 engendré/engendrée and628 auxilaire/auxiliaire translate generated and auxiliary identically in both English forms; the separate omitted ideal name I remains an explicit English variant.'),dict(page=664,topic='French duplicated letter',decision='MISPRINT633 etssoient/et soient translates and let identically; the strict inequality hypothesis and exponent corrections are independently explicit variants.'),dict(page=666,topic='Partial-word underline transport',decision='MISPRINT671 prints a short rule under ègr in intègre. English integral shares the corresponding egr letters, so the diplomatic form carries int\\underline{egr}al while current has integral; this is an explicitly recorded typographic translation transport, without importing a French accent into an English word.'),dict(page=666,topic='French misplaced accent',decision='MISPRINT672 graĉe/grâce both render by before the same projection-formula reference; no English accent error is invented.'),dict(page=666,topic='Two bibliography defects, one anchor group',decision='Variant051 combines the actual repeated journal/year/pages and the separately verified103→104 terminal page because these corrections occupy the same complete reference. Both source IDs and their independent evidence are retained in the transfer ledger.'),dict(page=666,topic='Bibliographic names and titles',decision='Preserve source author order, initials, complete titles and publication details. Translate the connective and, Extracts from and in this seminar; do not modernize or reformat the bibliographic content.'),dict(page=666,topic='XIV macro boundary',decision='XIII_XIV_boundary_macros.json records the exact reviewed post-bibliography block, which is retained before e14.expose. Native contains no corresponding local block; providecommand semantics are preserved, and earlier native Kb/Db values are explicitly recorded for aggregate state inspection.'),dict(page=665,topic='Final continuation',decision='665/666 remains one sentence and one open emphasis group, with the exact source folio comment before the irreducible-component predicate.663/664 likewise continues has/only finitely many singular points without a new paragraph.'),dict(page=664,topic='Author historical uncertainty',decision='Remark7.2 is translated faithfully as the authors’ statement of uncertainty in this source, without an assertion about present-day mathematical status.')]))
(H/'batches.json').write_text(json.dumps(b,ensure_ascii=False,indent=2)+'\n')
