#!/usr/bin/env python3
"""Register the final discussion, full bibliography and continuation state of II."""
from pathlib import Path
from collections import Counter
import hashlib,json,re
from reviewed_french import load_reviewed_pages
from verify_reviewed_english import split,MATH

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
chunk=(HERE/'EN_EXPOSE_II_P219_221.tex').read_text()
native=(HERE/'SGA6_EN_native_flattened_UNVERIFIED.tex').read_text()
a=native.index(r'$\operatorname{Ell}_n(F)$ formed',native.index(r'\sgaStableTarget{sga6.e02.para.3-2-3}'))
b=native.index(r'\sgaStableTarget{sga6.e03.expose}',a)
record=dict(id='EN-EXPOSE-II-219-221',page='219–221',place='Conclusion of3.2.3, final discussion and complete bibliography',
 layer='both',old=native[a:b],new=chunk,
 status='accepted passage comparison; exact scanned French decisions supplied by early reviewer',
 source='build/page_packets/219–221/current.tex and diplomatic.tex; review/expose_ii/patches.jsonl',
 reason='Restores the complete Ell inclusion, exact underlined sequence symbols and K^bullet class formula, original note at its actual call, source historical questions without an added answer, all eighteen bibliography entries with exact names, titles, ranges and trailing punctuation, and both continuation macro blocks in their specified order. The I(S)/I(H) and French title-spelling variants are explicitly retained.')
path=HERE/'EN_TRANSLATION_PATCHES.jsonl';records=[json.loads(x) for x in path.read_text().splitlines()]
hits=[i for i,x in enumerate(records) if x['id']==record['id']];assert len(hits)<=1
if hits:records[hits[0]]=record
else:records.append(record)
path.write_text(''.join(json.dumps(x,ensure_ascii=False)+'\n' for x in records))
variants=[]
def add(number,page,old,printed,source,reason,region):
 variants.append(dict(id=f'EN-VAR-{number:03}',page=page,old=old,printed=printed,corrected=old,mode='text',source=source,reason=reason,
  scope_start=f'%%%%%%%%%%  scan idx {page+13}  |  folio {page}',scope_end=f'%%%%%%%%%%  scan idx {page+14}  |  folio {page+1}',
  scan_image=f'scan/SGA6_scan_360dpi.pdf#page={page+14}; scan/SGA6_witness_300dpi.djvu#page={page+11}',scan_region=region))
add(150,219,r'the relations between the groups $[S,I(H)]$ and',r'the relations between the groups $[S,I(S)]$ and',
 'check/findings/findings_216_220.json#23',
 'The paragraph defines I(H) inside L(H,H) and the homotopy group of maps S→I(H). Its element is the class of a map with that target, and its homotopies are maps S times[0,1]→I(H). The later comparison therefore concerns that same group [S,I(H)]. Current restores H in this single later occurrence; diplomatic preserves the printed S. No relation to K-bullet(S) is added to the historical question.',
 'Later comparison between the two index groups in3.2.5')
add(151,220,'Fonctions analytiques sur un ensemble semi-analytique','Fonctions analyliques sur un ensemble semi-analytique',
 'check/findings/findings_216_220.json#29',
 'The bibliography title is retained in French in the English edition. Diplomatic therefore preserves the actually printed analyliques, with l, and current retains the recorded spelling correction analytiques, with t. The later semi-analytique, author, publication data, page range and punctuation remain unchanged.',
 'Frisch title in bibliography entry5')
path=HERE/'EN_VARIANTS.jsonl';rows=[json.loads(x) for x in path.read_text().splitlines()]
ids={v['id'] for v in variants};rows=[x for x in rows if x['id'] not in ids]+variants
rows.sort(key=lambda x:int(x['id'].rsplit('-',1)[1]));path.write_text(''.join(json.dumps(x,ensure_ascii=False)+'\n' for x in rows))
current,ref=load_reviewed_pages(221);diplomatic,dref=load_reviewed_pages(221,'diplomatic')
ledger=[]
for raw in (ROOT/'review/expose_ii/patches.jsonl').read_text().splitlines():
 if not raw.strip():continue
 p=json.loads(raw)
 if not 219<=p['page']<=221:continue
 ledger.append(dict(page=p['page'],source_id=p['source_id'],layer=p['layer'],decision='transferred in faithful English in both source forms',
  patch_record_sha256=hashlib.sha256(raw.encode()).hexdigest(),source_reason=p['reason'],expected_source_count=p.get('expected_count',1)))
for layer,reading,french,reference in [('current','corrected',current,ref),('diplomatic','printed',diplomatic,dref)]:
 text=chunk
 for v in variants:
  a=text.index(v['scope_start']);b=text.index(v['scope_end'],a);section=text[a:b];assert section.count(v['old'])==1
  text=text[:a]+section.replace(v['old'],v[reading],1)+text[b:]
 en=split(text)
 for page in range(219,222):
  fu=Counter(m.group() for m in MATH.finditer(french[page]));eu=Counter(m.group() for m in MATH.finditer(en[page]));assert fu==eu,(layer,page,fu-eu,eu-fu)
  counts={}
  for token in [r'\underline n',r'\underline F',r'\SGAAuthorFootnote{1}',r'\L{}ojasiewicz']:
   counts[token]=dict(French=french[page].count(token),English=en[page].count(token));assert counts[token]['French']==counts[token]['English']
  ledger.append(dict(page=page,layer=layer,source_id='exact reviewed page glyph inventory',decision='all literal mathematical units and specified glyph multiplicities agree exactly in both materialized branches',
   source=reference['bases'][page-1],counts=counts,reviewed_French_page_sha256=hashlib.sha256(french[page].encode()).hexdigest(),English_page_sha256=hashlib.sha256(en[page].encode()).hexdigest()))
native_footer=record['old'][record['old'].index(r'\end{enumerate}')+len(r'\end{enumerate}'):].strip()
french_footer=current[221][current[221].index('% Exposé III additions'):].strip()
assert native_footer in chunk and french_footer in chunk
assert chunk.index(native_footer)<chunk.index(french_footer)
ledger.extend([
 dict(page=219,source_id='reviewed final3.2.3–3.2.5 discussion',decision='Restore the full Ell-in-Comp.diff inclusion, all four individually ruled n occurrences, the source K^bullet class formula, exact loc.cit. wording and all historical statements of the writer. The quoted phrase opérateurs à indice is rendered operators with index without substituting an unstated contemporary definition. No answer to the historical group-comparison questions is inserted.'),
 dict(page=219,source_id='ASTRA-II-AUTHOR-NOTE-219',decision='Restore the complete weak-Hilbert-bundle/continuous-field note immediately after for simplicity inside the source parenthesis. It is not moved to the closing reference to Atiyah and Singer. Both the numerical1 call and its own outer parenthesis are retained.'),
 dict(page=219,source_id='check/findings/findings_216_220.json#22',decision='Preserve plain F_r-bullet for the Hilbert-bundle complex in3.2.5 and underlined F_r-bullet for its section sheaf in3.2.4; the source sections functor F_r-bullet→underline F_r-bullet is the explicit construction relating these occurrences.'),
 dict(page=220,source_id='reviewed bibliography entries1–13',decision='Preserve every original title and author spelling, J-L. in entry1, Roma, the uppercase Faisceaux/Analytique/Locale forms, North Holl. Pub. Comp. abbreviation, source Lecture Notes wording, CRAS/IHES forms, all seven typed range hyphens and exact trailing punctuation. Translate only descriptive prose such as cited as, to appear and course. Titles remain plain, as in the reviewed source; no modern publication data are added.'),
 dict(page=221,source_id='reviewed bibliography entries14–18',decision='Preserve all five complete entries, crossed initial L in Lojasiewicz, source abbreviated journal name and serie spelling, Princeton1963-64 hyphen, commas ending entries14/17, and distinct J.-L. punctuation in entry18. Numbering continues from13 to14 across the exact source folio boundary.'),
 dict(page=221,source_id='native and reviewed continuation macro states',decision='Retain the original native continuation definitions verbatim, then the reviewed French continuation block verbatim. The source renewal of Ob to lowercase ob is executed at the II/III boundary after the retained native providecommand. No later redefinition is moved into the apparatus or earlier body.',
  native_block_sha256=hashlib.sha256(native_footer.encode()).hexdigest(),reviewed_French_block_sha256=hashlib.sha256(french_footer.encode()).hexdigest(),native_block=native_footer,reviewed_French_block=french_footer),
])
for v in variants:ledger.append(dict(page=v['page'],source_id=v['source'],decision='explicit English printed/corrected source variant',English_variant=v['id'],printed=v['printed'],corrected=v['corrected']))
(HERE/'EN_EXPOSE_II_TRANSFER_219_221.jsonl').write_text(''.join(json.dumps(x,ensure_ascii=False)+'\n' for x in ledger))
path=HERE/'EN_AUTHOR_NOTE_MARKS.tsv';notes=[x for x in path.read_text().splitlines() if not x.startswith('219\t')]
notes.append('219\tAfter for simplicity inside the parenthesis in3.2.4\traised numerical1 inside baseline parentheses\t1\tASTRA-II-AUTHOR-NOTE-219\tearly reviewer direct scan comparison, main PDF233\tSGAAuthorFootnote{1}\tFull weak-Hilbert-bundle or continuous-field note; outer prose parenthesis retained.')
path.write_text('\n'.join(notes)+'\n')
pat=re.escape(r'\sgaStableTarget{')+r'([^}]+)\}'
ot=set(re.findall(pat,record['old']));nt=set(re.findall(pat,chunk));assert ot and ot==nt,dict(missing=sorted(ot-nt),extra=sorted(nt-ot))
print(json.dumps(dict(passage=record['id'],variants=sorted(ids),exact_lexical_pairs=0,transfer_rows=len(ledger),stable_targets=len(ot),bibliography_entries=18),ensure_ascii=False))
