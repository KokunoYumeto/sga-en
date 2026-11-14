#!/usr/bin/env python3
"""Register the relative-amplitude definitions and retained author-claim passage."""
from pathlib import Path
from collections import Counter
import hashlib,json,re
from reviewed_french import load_reviewed_pages
from verify_reviewed_english import split,MATH

H=Path(__file__).resolve().parent;R=H.parents[1]
sha=lambda s:hashlib.sha256(s.encode()).hexdigest()
chunk=(H/'EN_EXPOSE_III_P241_245.tex').read_text()
native=(H/'SGA6_EN_native_flattened_UNVERIFIED.tex').read_text()
a=native.index(r'\emph{Proof.} Consequence of \hyperlink{sga6.e03.thm.2-2}{Theorem 2.2},')
b=native.index(r'\sgaStableTarget{sga6.e03.prop.3-6}',a)
record=dict(id='EN-EXPOSE-III-241-245',page='241–245',place='Proof of2.5, historical scholium, relative flat-amplitude definitions and3.5 through its second corollary',layer='both',old=native[a:b],new=chunk,status='accepted passage comparison; exact scanned French decisions supplied by coordinator',source='build/page_packets/241–245/current.tex and diplomatic.tex; review/expose_iii/patches.jsonl',reason='Restores the complete original note, correct grammatical attachment of topologized to the algebras, exact source definitions and bounds, literal tensor expressions and original triangle/square orientation, complete source proof and continuation macro state. Both source locator variants are explicit. The audited author-claim defects in3.5 and its stalk equations remain in both historical source branches without a replacement assertion.')
cur,ref=load_reviewed_pages(245);dip,dref=load_reviewed_pages(245,'diplomatic')
decisions=[json.loads(x) for x in (R/'review/expose_iii/decisions.jsonl').read_text().splitlines()]
variants=[]
for number,page,old,printed,fix,region in [
 (162,241,'(2.2), (2.4) and (1.12)','(2.2), (2.5) and (1.12)',379,'Proof of Corollary2.5'),
 (163,242,'(SGA 4 IV 6.4)','(SGA 4 XVII IV 6.4)',380,'Enough-points reference in Proposition3.3')]:
 source=f'fixes/FIXLOG_6_CURRENT.jsonl#{fix}';d=next(x for x in decisions if x['source_id']==source)
 variants.append(dict(id=f'EN-VAR-{number:03}',page=page,old=old,printed=printed,corrected=old,mode='text',source=source,reason=d['reason'],scope_start=f'%%%%%%%%%%  scan idx {page+13}  |  folio {page}',scope_end=f'%%%%%%%%%%  scan idx {page+14}  |  folio {page+1}',scan_image=d['image'],scan_region=region))
native_footer=record['old'][record['old'].index(r'\providecommand{\Ob}',record['old'].index(r'\sgaStableTarget{sga6.e03.cor.3-5-2}')):].strip()
french_footer=cur[245][cur[245].index('% Additions for Exposé III'):].strip()
assert native_footer in chunk and french_footer in chunk and chunk.index(native_footer)<chunk.index(french_footer)
ledger=[];pairs=[];unit_count=0
lexical={241:(r'\text{ou }',r'\text{or }'),242:(r'\uline{pour}',r'\uline{for}'),243:(r'\text{et}',r'\text{and}')}
for layer,reading,fr,rr in [('current','corrected',cur,ref),('diplomatic','printed',dip,dref)]:
 text=chunk
 for v in variants:
  a=text.index(v['scope_start']);b=text.index(v['scope_end'],a);part=text[a:b];assert part.count(v['old'])==1
  text=text[:a]+part.replace(v['old'],v[reading],1)+text[b:]
 en=split(text)
 for page in range(241,246):
  f=Counter(m.group() for m in MATH.finditer(fr[page]));e=Counter(m.group() for m in MATH.finditer(en[page]));missing=f-e;extra=e-f
  assert sum(missing.values())==sum(extra.values())==int(page in lexical),(page,layer,missing,extra)
  if layer=='current':unit_count+=sum(f.values())
  for ff,n in missing.items():
   old,new=lexical[page];ee=ff.replace(old,new);assert ee!=ff and extra[ee]==n==1
   pairs.append(dict(page=page,layer=layer,French_literal_unit=ff,English_literal_unit=ee,expected_multiplicity=1,status='confirmed complete lexical formula translation; only the source connective is translated, with all other characters retained',scope='This exact complete mathematical unit in its stated source branch only.'))
  ft=fr[page].split('% Additions for Exposé III')[0];et=en[page].split('% Original English continuation definitions')[0]
  counts={}
  for token in [r'\underline{O}',r'\Ob',r'\mathbb',r'\toramp',r'\mathrm L',r'\simeq',r'\SGAAuthorFootnote{1}']:
   counts[token]=dict(French=ft.count(token),English=et.count(token));assert counts[token]['French']==counts[token]['English'],(page,layer,token)
  ledger.append(dict(page=page,layer=layer,source_id='exact reviewed page glyph inventory',decision='Every mathematical unit agrees literally except the individually recorded connective translation. Body glyph counts exclude the separately preserved continuation macro blocks.',source=rr['bases'][page-1],counts=counts,reviewed_French_page_sha256=sha(fr[page]),English_page_sha256=sha(en[page])))
for raw in (R/'review/expose_iii/patches.jsonl').read_text().splitlines():
 p=json.loads(raw)
 if 241<=p['page']<=245:
  ledger.append(dict(page=p['page'],source_id=p['source_id'],layer=p['layer'],decision='Transferred in the faithful English passage in both source forms.',patch_record_sha256=sha(raw),source_reason=p['reason'],expected_source_count=p.get('expected_count',1)))
ledger.extend([
 dict(page=241,source_id='reviewed Scholium2.6 and ASTRA-III-AUTHOR-NOTE-241',decision='Restore the original qualification that the analytic conjecture is quoted as proved, its exact Grauert[1] locator, and the adjective topologized attached to the C-algebras (the French feminine-plural topologisées). Preserve the full April1971 note with numerical1 call, R.Kiehl and J.L.Verdier punctuation, literal finiteness theorem1, article in preparation, simpler techniques and more general hypotheses. No modern publication information is added.'),
 dict(page=241,source_id='reviewed Definition3.1 and Notation3.2',decision='Restore the morphism inline, all independent O rules, plain newly defined predicates, explicit nonnegative a, the source lowercase tor-dimension and rel. abbreviation, absence of a final stop in the first amplitude display, and all three inline category names. The precise lexical or display translation is separately paired.'),
 dict(page=242,source_id='reviewed Proposition3.3 and proof',decision='Restore the separately stated image point y and all twelve O rules, literal restriction bars and tensor bases, ordinary derived L, complete inline tensor equality and cokernel data, original star tag and exact EGA0_I5.3.9 locator. Preserve the full finite-presentation descent to a y-pointed object and its headless P_y comparison; the inherited English L_! and altered tensor base are removed by source reconstruction.'),
 dict(page=243,source_id='reviewed continuation, Remark3.3.1 and Corollary3.4',decision='Retain the writer’s historical uncertainty without an added answer. Restore the three-column triangle, the separate implication display, exact relative tensor expressions and full proof. In the sentence joining242–243, fibres means the point inverse-image modules: the map sends a tensor of section germs to the germ of their tensor, with its inverse supplied by representatives on a common pointed neighborhood; this is the stalk tensor identification used in the displayed equality. Render this as stalks.'),
 dict(page=244,source_id='reviewed Remark3.4.2 and Proposition3.5',decision='Retain the complete source statement, including its finite-relative-amplitude hypothesis and both printed conclusions. Preserve the quoted on the stalks wording, all four pointwise module/ring assignments, both unlocalized stalk equations, original star tag and subsequent displayed derived comparison. These are retained historical assertions, with the independently demonstrated defects linked in the separate author-claim packet.'),
 dict(page=245,source_id='reviewed proof of3.5 and its corollaries',decision='Restore the exact I5.6 locator, all source inline tensor objects and the complete proof of both clauses without supplying new hypotheses. Restore the original square with X on the left and X-prime on the right, the actual Ob D(X) without a minus, ordinary derived L and the two source functor categories.'),
 dict(page=245,source_id='native and reviewed continuation macro states',decision='Retain the native continuation block verbatim followed by the reviewed French block verbatim at the same boundary. The source renewals of Ob/id and provision of uparf execute after the native providecommands. No definition is moved into an earlier passage or allowed to change an earlier apparatus reading.',native_block_sha256=sha(native_footer),reviewed_French_block_sha256=sha(french_footer),native_block=native_footer,reviewed_French_block=french_footer),
])
for relative in ['review/english/EN_INDEPENDENT_III_3_5_AUDIT_244_245.json','review/expose_iii/author_claim_244_245.json']:
 p=R/relative;packet=json.loads(p.read_text())
 ledger.append(dict(page=244,source_id=packet['id'],source_packet=relative,source_packet_sha256=hashlib.sha256(p.read_bytes()).hexdigest(),decision='Carry the recorded source-retention disposition into both English branches. The external tensor counterexample uses [F_p --0→ F_p] in degrees−1,0; the missing localizations are demonstrated by the exact map R→R_q. No English source replacement or repaired theorem is created.',status='independent text/math audit with coordinator-attributed source images; no new image-reading claim'))
for v in variants:ledger.append(dict(page=v['page'],source_id=v['source'],decision='explicit English printed/corrected source variant',English_variant=v['id'],printed=v['printed'],corrected=v['corrected']))
for pair in pairs:ledger.append(dict(page=pair['page'],source_id='individually checked exact lexical display',decision='Only the displayed lexical connective is translated.',**{k:pair[k] for k in ['layer','French_literal_unit','English_literal_unit','expected_multiplicity']}))
pat=re.escape(r'\sgaStableTarget{')+r'([^}]+)\}';ot=set(re.findall(pat,record['old']));nt=set(re.findall(pat,chunk));assert ot==nt and len(ot)==12,(ot,nt)
path=H/'EN_TRANSLATION_PATCHES.jsonl';rows=[json.loads(x) for x in path.read_text().splitlines()];hits=[i for i,x in enumerate(rows) if x['id']==record['id']];assert len(hits)<=1
if hits:rows[hits[0]]=record
else:rows.append(record)
path.write_text(''.join(json.dumps(x,ensure_ascii=False)+'\n' for x in rows))
path=H/'EN_VARIANTS.jsonl';ids={v['id'] for v in variants};rows=[json.loads(x) for x in path.read_text().splitlines() if json.loads(x)['id'] not in ids]+variants;rows.sort(key=lambda x:int(x['id'].rsplit('-',1)[1]));path.write_text(''.join(json.dumps(x,ensure_ascii=False)+'\n' for x in rows))
path=H/'EN_APPROVED_LEXICAL_MATH_PAIRS.json';rows=[x for x in json.loads(path.read_text()) if not 241<=x['page']<=245]+pairs;path.write_text(json.dumps(rows,ensure_ascii=False,indent=2)+'\n')
(H/'EN_EXPOSE_III_TRANSFER_241_245.jsonl').write_text(''.join(json.dumps(x,ensure_ascii=False)+'\n' for x in ledger))
path=H/'EN_AUTHOR_NOTE_MARKS.tsv';notes=[x for x in path.read_text().splitlines() if not x.startswith('241\t')];notes.append('241\tAfter the Grauert[1] parenthesis in Scholium2.6\traised numerical1 inside baseline parentheses\t1\tASTRA-III-AUTHOR-NOTE-241\tcoordinator direct main/native comparison\tSGAAuthorFootnote{1}\tComplete April1971 Kiehl and J.L.Verdier note; literal theorem number1 retained.');path.write_text('\n'.join(notes)+'\n')
print(json.dumps(dict(passage=record['id'],variants=sorted(ids),math_units=unit_count,lexical_pair_records=len(pairs),transfer_rows=len(ledger),stable_targets=len(ot))))
