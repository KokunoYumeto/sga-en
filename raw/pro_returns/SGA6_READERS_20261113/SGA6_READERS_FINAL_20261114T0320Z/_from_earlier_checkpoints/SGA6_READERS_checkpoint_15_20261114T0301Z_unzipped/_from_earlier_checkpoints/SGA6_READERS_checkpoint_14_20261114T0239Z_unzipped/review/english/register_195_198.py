#!/usr/bin/env python3
"""Register Verdier's complete Appendix I and preserve continuation macro state."""
from pathlib import Path
import hashlib,json,re
from reviewed_french import load_reviewed_pages
from verify_reviewed_english import split

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
chunk=(HERE/'EN_EXPOSE_II_P195_198.tex').read_text()
native=(HERE/'SGA6_EN_native_flattened_UNVERIFIED.tex').read_text()
a=native.index(r'\sgaStableTarget{sga6.e02.appendix-i-a-counterexample-of-verdier}')
b=native.index(r'\sgaStableTarget{sga6.e02.appendix-ii',a)
record=dict(id='EN-EXPOSE-II-195-198',page='195–198',
 place='Complete Appendix I, A counterexample of Verdier, and continuation definitions',layer='both',
 old=native[a:b],new=chunk,
 status='accepted passage comparison; exact scanned French decisions supplied by early reviewer',
 source='build/page_packets/195–198/current.tex and diplomatic.tex; review/expose_ii/patches.jsonl',
 reason='Restores the complete Verdier letters note and exact dates, all source references, plain paragraph numbers, formal-power-series ring, individual f underlines and annihilator left indices, original Koszul superscript note, exact duality formulas and final Ext argument. Four explicit variants preserve the printed/current differences on196. Original English continuation definitions and reviewed French continuation definitions are both retained in their respective order.')
path=HERE/'EN_TRANSLATION_PATCHES.jsonl';records=[json.loads(x) for x in path.read_text().splitlines()]
hits=[i for i,x in enumerate(records) if x['id']==record['id']]
assert len(hits)<=1
if hits:records[hits[0]]=record
else:records.append(record)
path.write_text(''.join(json.dumps(x,ensure_ascii=False)+'\n' for x in records))

variants=[]
def add(number,old,printed,source,reason,mode='math',region=''):
 variants.append(dict(id=f'EN-VAR-{number:03}',page=196,old=old,printed=printed,corrected=old,mode=mode,
  source=source,reason=reason,scope_start='%%%%%%%%%%  scan idx 209  |  folio 196',
  scope_end='%%%%%%%%%%  scan idx 210  |  folio 197',
  scan_image='scan/SGA6_scan_360dpi.pdf#page=210; scan/SGA6_witness_300dpi.djvu#page=207',
  scan_region=region))
add(139,r'M=\coprod_{n>0}B/(\underline{f}^n)',r'M=\coprod_{n\ 0}B/(\underline{f}^n)',
 'check/findings/findings_196_200.json#3; fixes/MISPRINTS_6.json#185',
 'The printed relation slot between n and0 is blank. Current supplies the positive-index sum. Its canonical inclusion into the sum over n≥0 and the projection back are inverse: the n=0 term is B/(1,1)=0 for f=(x,y). This identifies the two specified module constructions without changing any summand of positive index. Diplomatic retains the blank.',
 region='Definition of the module M')
add(140,r'H_2^B(\underline{f}^n,A)\simeq H_2^B(\underline{f}^n,M).',
 r'H_2^B(\underline{f}^n,A)\simeq H_2^B(\underline{f}^n,M),',
 'check/findings/findings_196_200.json#7; fixes/MISPRINTS_6.json#186',
 'The print ends this display with a comma before the next independent capitalized sentence. Current uses a sentence stop. Every Koszul term and the isomorphism sign remain identical; diplomatic preserves the comma.',
 region='Display immediately before Finally, we have')
add(141,'Finally, we have (EGA III 1.1.3.3)','Finally, we have (EGA II 1.1.3.3)',
 'check/findings/findings_196_200.json#8; fixes/MISPRINTS_6.json#187',
 'The reviewed primary EGA III text, Part1 page83 formula1.1.3.3, gives the Koszul duality identification H^i(f,M) with H_(r-i)(f,M). For r=2 and i=0, the map sends the top exterior-basis vector tensored with m to m in the common annihilator of x^n and y^n. This is precisely the displayed H_2 to H^0 map. Current repairs only the Roman chapter numeral; diplomatic keeps II. The independent primary-text verification is recorded by the French reviewer, without a new EGA image-read claim.',
 mode='text',region='EGA citation for the Koszul H_2/H^0 identification')
add(142,r'H_2^A(\underline{f}^n,A)\simeq {}_{(\underline{f}^n)}M.',
 r'H_2^A(\underline{f}^n,A\simeq {}_{(\underline{f}^n)}M.',
 'check/findings/findings_196_200.json#11; fixes/MISPRINTS_6.json#188; fixes/RECONCILE_CODEX_6.json#254',
 'Current closes the existing argument list of H_2^A(f^n,A), the same Koszul module in the first display and the transition maps. No term or map is added. Diplomatic retains the omitted closing parenthesis in(*).',
 region='Left member of formula(*)')
path=HERE/'EN_VARIANTS.jsonl';rows=[json.loads(x) for x in path.read_text().splitlines()]
ids={v['id'] for v in variants};rows=[x for x in rows if x['id'] not in ids]+variants
rows.sort(key=lambda x:int(x['id'].rsplit('-',1)[1]))
path.write_text(''.join(json.dumps(x,ensure_ascii=False)+'\n' for x in rows))

current,ref=load_reviewed_pages(198)
diplomatic,dref=load_reviewed_pages(198,'diplomatic')
ledger=[]
for raw in (ROOT/'review/expose_ii/patches.jsonl').read_text().splitlines():
 if not raw.strip():continue
 p=json.loads(raw)
 if not 195<=p['page']<=198:continue
 ledger.append(dict(page=p['page'],source_id=p['source_id'],layer=p['layer'],
  decision='transferred in faithful English; every source branch difference has an explicit English variant',
  patch_record_sha256=hashlib.sha256(raw.encode()).hexdigest(),source_reason=p['reason'],
  expected_source_count=p.get('expected_count',1)))
for layer,reading,french,reference in [('current','corrected',current,ref),('diplomatic','printed',diplomatic,dref)]:
 text=chunk
 for v in variants:
  a=text.index(v['scope_start']);b=text.index(v['scope_end'],a)
  section=text[a:b];assert section.count(v['old'])==1,(v['id'],section.count(v['old']))
  text=text[:a]+section.replace(v['old'],v[reading],1)+text[b:]
 en=split(text)
 for page in range(195,199):
  counts={}
  for token in [r'\underline{O}',r'\underline{f}',r'\underline{\underline{R}}',r'\phi',
                r'\SGAAuthorFootnote{1}',r'\SGAAuthorFootMark{1}',r'\SGAAuthorFootText{1}']:
   counts[token]=dict(French=french[page].count(token),English=en[page].count(token))
   assert counts[token]['French']==counts[token]['English'],(layer,page,token,counts[token])
  ledger.append(dict(page=page,layer=layer,source_id='exact reviewed page glyph inventory',
   decision='literal command multiplicities agree in both materialized branches',
   source=reference['bases'][page-1],counts=counts,
   reviewed_French_page_sha256=hashlib.sha256(french[page].encode()).hexdigest(),
   English_page_sha256=hashlib.sha256(en[page].encode()).hexdigest()))
native_macro_start=record['old'].index(r'\providecommand{\Diff}')
native_macros=record['old'][native_macro_start:record['old'].index(r'\newpage',native_macro_start)].strip()
assert native_macros in chunk
fr_macros=current[198][current[198].index('% Additions for Expose II, Appendix II'):].strip()
assert fr_macros in chunk
ledger.extend([
 dict(page=195,source_id='ASTRA-II-NOTES-195; reviewed Appendix I introduction',decision='Restore the full original title note: two letters from J.-L.Verdier to the editor, dated30/9/67 and11/10/67, in reply to the editor\'s question. Restore [H]II7.14, the full-subcategory clause in0.2, the inclusion phi and II3.0 reference in0.3; keep all three paragraph numbers plain.'),
 dict(page=195,source_id='ASTRA-II-UNDERLINE-195; check/findings/findings_191_195.json#33',decision='Retain every inspected lexical rule in Lemma1.1 and both conditions, independent plain mathematical units and item labels, and the three separate individual f rules. The page boundary is after n-prime≥n, leaving such that and the transition on196.'),
 dict(page=196,source_id='reviewed Koszul construction; ASTRA-II-F-196',decision='Restore k[[x,y]] exactly, the actual coproduct symbol and individual f rules at all24 occurrences, the baseline M with lower left annihilator index at both occurrences, the entire regularity and Koszul references, and the final local-cohomology implication. The native polynomial-ring and parenthesized-pair readings are not retained as source variants because the reviewed scan has the restored expressions in both layers.'),
 dict(page=196,source_id='ASTRA-II-NOTES-196; ASTRA-II-PARAGRAPH-196',decision='Keep plain1.2 without an added stop, no added conjunction before A, and the original numerical1 call after the first display stop. Restore the complete explanation of the A/B Koszul superscripts.'),
 dict(page=197,source_id='reviewed gluing and spectral-sequence argument',decision='Restore the repeated choice of I, the literal plain I in the first local-cohomology display, the source cartesian-square label positions, both double-underlined R letters and the complete low-degree spectral-sequence explanation. The printed formula objects and domains are retained exactly; no implicit restriction is silently inserted.'),
 dict(page=198,source_id='ASTRA-II-R-198; reviewed duality argument',decision='Retain all seven double-underlined R letters, every displayed grouping and source plain I in Hom_Qcoh, the exact identity-morphism argument and complete bounded-derived-category conclusion. No tilde or extra displayed reformulation is introduced.'),
 dict(page=198,source_id='original English and reviewed French continuation macro blocks',decision='Retain the complete original English providecommand block verbatim and in order, then the complete reviewed French continuation block verbatim. The first preserves native tail dependencies such as cT, RGamma, dlim and plim; providecommand does not overwrite earlier definitions. The reviewed explicit id renewal remains at its source position. These are implementation definitions, not added body prose.',native_block_sha256=hashlib.sha256(native_macros.encode()).hexdigest(),reviewed_French_block_sha256=hashlib.sha256(fr_macros.encode()).hexdigest()),
])
for v in variants:ledger.append(dict(page=v['page'],source_id=v['source'],decision='explicit English printed/corrected variant',English_variant=v['id'],printed=v['printed'],corrected=v['corrected']))
(HERE/'EN_EXPOSE_II_TRANSFER_195_198.jsonl').write_text(''.join(json.dumps(x,ensure_ascii=False)+'\n' for x in ledger))
path=HERE/'EN_AUTHOR_NOTE_MARKS.tsv'
notes=[x for x in path.read_text().splitlines() if not any(x.startswith(str(p)+'\t') for p in [195,196])]
notes.extend([
 '195\tAppendix I title\traised numerical1 inside baseline parentheses\t1\tASTRA-II-NOTES-195\tearly reviewer direct scan comparison, main PDF209\tSGAAuthorFootnote{1}\tComplete J.-L.Verdier letters attribution and exact dates.',
 '196\tAfter the first Koszul display stop\traised numerical1 inside baseline parentheses\t1\tASTRA-II-NOTES-196\tearly reviewer direct scan comparison, main PDF210\tSGAAuthorFootMark{1}; SGAAuthorFootText{1}\tComplete original A/B superscript explanation.'
])
path.write_text('\n'.join(notes)+'\n')
pat=re.escape(r'\sgaStableTarget{')+r'([^}]+)\}'
ot=set(re.findall(pat,record['old']));nt=set(re.findall(pat,chunk))
assert ot and ot==nt,dict(missing=sorted(ot-nt),extra=sorted(nt-ot))
print(json.dumps(dict(passage=record['id'],variants=sorted(ids),transfer_rows=len(ledger),stable_targets=len(ot)),ensure_ascii=False))
