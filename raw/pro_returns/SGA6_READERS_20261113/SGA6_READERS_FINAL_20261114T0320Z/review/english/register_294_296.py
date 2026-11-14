#!/usr/bin/env python3
"""Register the complete relative K-group passage, bibliography and V boundary."""
from pathlib import Path
from collections import Counter
import hashlib,json,re
from reviewed_french import load_reviewed_pages
from verify_reviewed_english import split,MATH
H=Path(__file__).resolve().parent;R=H.parents[1]
sha=lambda s:hashlib.sha256(s.encode()).hexdigest()
chunk=(H/'EN_EXPOSE_IV_P294_296.tex').read_text();native=(H/'SGA6_EN_native_flattened_UNVERIFIED.tex').read_text()
a=native.index(r'\sgaStableTarget{sga6.e04.para.3-3}');b=native.index(r'\sgaStableTarget{sga6.e05.expose}',a)
record=dict(id='EN-EXPOSE-IV-294-296',page='294–296',place='Complete relative Grothendieck groups, bibliography and ExposéV continuation macros',layer='both',old=native[a:b],new=chunk,status='accepted passage comparison; exact scanned French decisions supplied by reviewer',source='build/page_packets/294–296/current.tex and diplomatic.tex; review/expose_iv/patches.jsonl',reason='Restores all relative categories, left/right group dots, all four numbered variance constructions, precise coefficient and relative domains, complete external tensor assertions, original bibliography and local V macro state. The single approved /S source correction is explicit; the separately documented author-claim defect is retained without a replacement theorem.')
d=next(json.loads(x) for x in (R/'review/expose_iv/own_findings.jsonl').read_text().splitlines() if json.loads(x)['source_id']=='ASTRA-IV-PROJECTION-295')
v=dict(id='EN-VAR-201',page=295,old=r'x\in K_{\bullet}(X/S)',printed=r'x\in K_{\bullet}(X)',corrected=r'x\in K_{\bullet}(X/S)',mode='math',source=d['source_id'],reason=d['reason'],scope_start='%%%%%%%%%%  scan idx 308  |  folio 295',scope_end=r'\sgaStableTarget{sga6.e04.para.3-3-3}',scan_image=d['image'],scan_region=d['region'])
variants=[v];ledger=[];unit_count=0
for layer,reading in [('current','corrected'),('diplomatic','printed')]:
 text=chunk;a=text.index(v['scope_start']);b=text.index(v['scope_end'],a);part=text[a:b];assert part.count(v['old'])==1
 text=text[:a]+part.replace(v['old'],v[reading],1)+text[b:]
 en=split(text);fr,reference=load_reviewed_pages(296,layer,start=294)
 for page in range(294,297):
  f=Counter(m.group() for m in MATH.finditer(fr[page]));e=Counter(m.group() for m in MATH.finditer(en[page]));assert f==e,(page,layer,f-e,e-f)
  if layer=='current':unit_count+=sum(f.values())
  ff=fr[page].split('% Expose V macros')[0];ee=en[page].split('% SGA_NATIVE_CONTINUATION_296')[0];counts={}
  for token in [r'\underline O',r'\parf',r'\coh',r'\mathrm L',r'\Id',r'\begin{tikzcd}',r'\otimes',r'\item']:
   counts[token]=dict(French=ff.count(token),English=ee.count(token));assert counts[token]['French']==counts[token]['English'],(page,layer,token)
  ledger.append(dict(page=page,layer=layer,source_id='exact reviewed page glyph inventory',decision='All complete mathematical units match literally in each branch. The complete triangle, every tensor target, relative-domain argument and original bibliography label are retained. Body glyph counts exclude the separately preserved continuation macro blocks.',source=next(x for x in reference['bases'] if x['page']==page),counts=counts,reviewed_French_page_sha256=sha(fr[page]),English_page_sha256=sha(en[page])))
for raw in (R/'review/expose_iv/patches.jsonl').read_text().splitlines():
 p=json.loads(raw)
 if 294<=p['page']<=296:ledger.append(dict(page=p['page'],source_id=p['source_id'],layer=p['layer'],decision='Transferred in the faithful English source branches.',patch_record_sha256=sha(raw),source_reason=p['reason'],expected_source_count=p.get('expected_count',1)))
ledger.extend([
 dict(page=294,source_id='complete relative definitions and3.3.2.1–2',decision='Restore the two stacked group definitions, separate relative category descriptions and all four X/Y alternative names. Preserve the source author discussion and both inline tensor expressions. The full triangle has the exact f/g/h orientation, and all subsection numerals are plain. The French morphisme/morphismes agreement repair names the same three arrows; English morphisms is unchanged in both branches.'),
 dict(page=295,source_id='ASTRA-IV-PROJECTION-295',decision='Supply /S only in the first x-domain. Keep the second coefficient a∈K_bullet(S), all proper/perfect hypotheses and the displayed formula exactly. The recorded first and second pairings are identified by their explicit III3.7 projection maps; their common perfect-input restriction is induced by the identity on those complexes. The excluded absolute-domain counterexample and both map proofs remain in the source packet.',evidence='review/expose_iv/identification_295.json',evidence_sha256=hashlib.sha256((R/'review/expose_iv/identification_295.json').read_bytes()).hexdigest()),
 dict(page=295,source_id='ASTRA-IV-AUTHOR-CLAIM-295',decision='Preserve the full author statement3.3.3 in both English forms: both category pairings, both asserted induced group maps and the reference to III4.7. The source packet gives the dual-number epsilon-periodic resolution, exact derived pullback/tensor maps and nonzero cohomology in every nonpositive degree, proving the defect of the first bounded target. It supplies no replacement theorem and assigns no defect to the second perfect/perfect pairing. This is separate audit evidence, not a diplomatic/current variant.',source_packet='review/expose_iv/author_claim_issue_295.json',source_packet_sha256=hashlib.sha256((R/'review/expose_iv/author_claim_issue_295.json').read_bytes()).hexdigest(),status='source-text/math transfer; no new image claim'),
 dict(page=296,source_id='complete final paragraph and bibliography',decision='Restore the source parenthetical special case, exact n≥1 tensor-power expression and qualified final wording. Preserve all four bibliography entries and actual[1]/[2]/[3]/[V] labels, source title spelling/capitalization, Grauert ellipsis, publication abbreviations, years and p.1-7. Titles stay in their source languages; the inherited added title italics and rewritten punctuation are removed.'),
])
start=native.index(r'\providecommand{\Chat}',native.index(r'\sgaStableTarget{sga6.e04.bibliography}'));native_block=native[start:native.index(r'\sgaStableTarget{sga6.e05.expose}',start)]
current,_=load_reviewed_pages(296,start=296);fr_block=current[296][current[296].index('% Expose V macros'):]
assert chunk.count(native_block)==1 and chunk.count(fr_block)==1
renew=r'\renewcommand{\Abfil}{\underline{\mathrm{Ab}}\,\underline{\mathrm{fil}}}'
assert chunk.endswith(renew+'\n\n')
ledger.append(dict(page=296,source_id='EN-MACRO-BOUNDARY-296',decision='Preserve the native continuation block first and the reviewed French block second after the bibliography. Keep the reviewed id/Ob renewals at their actual scope boundary. Native Abfil provides plain mathrm{Ab fil}, so the later French provide of two separate word rules would otherwise be inactive. The final explicit renewal restores the exact reviewed underline{mathrm{Ab}} thin-space underline{mathrm{fil}} expansion for the same category abbreviation. No category, object, morphism or formula argument is changed.',native_macro_block=native_block,native_macro_sha256=sha(native_block),reviewed_French_macro_block=fr_block,reviewed_French_macro_sha256=sha(fr_block),local_expansion_restoration=renew,status='both-form source-glyph transfer; first two inherited V Abfil uses directly inspected on corrected output164 in the through296 build, with separate Ab/fil rules; no surrounding V translation claim'))
ledger.append(dict(page=v['page'],source_id=v['source'],decision='explicit English printed/corrected source variant',English_variant=v['id'],printed=v['printed'],corrected=v['corrected']))
pat=re.escape(r'\sgaStableTarget{')+r'([^}]+)\}';ot=set(re.findall(pat,record['old']));nt=set(re.findall(pat,chunk));assert ot==nt and len(ot)==5,(ot,nt)
path=H/'EN_TRANSLATION_PATCHES.jsonl';rows=[json.loads(x) for x in path.read_text().splitlines()];hits=[i for i,x in enumerate(rows) if x['id']==record['id']];assert len(hits)<=1
if hits:rows[hits[0]]=record
else:rows.append(record)
path.write_text(''.join(json.dumps(x,ensure_ascii=False)+'\n' for x in rows))
path=H/'EN_VARIANTS.jsonl';rows=[json.loads(x) for x in path.read_text().splitlines() if json.loads(x)['id']!=v['id']]+variants;rows.sort(key=lambda x:int(x['id'].rsplit('-',1)[1]));path.write_text(''.join(json.dumps(x,ensure_ascii=False)+'\n' for x in rows))
path=H/'EN_APPROVED_LEXICAL_MATH_PAIRS.json';rows=[x for x in json.loads(path.read_text()) if not 294<=x['page']<=296];path.write_text(json.dumps(rows,ensure_ascii=False,indent=2)+'\n')
(H/'EN_EXPOSE_IV_TRANSFER_294_296.jsonl').write_text(''.join(json.dumps(x,ensure_ascii=False)+'\n' for x in ledger))
print(json.dumps(dict(passage=record['id'],variants=[v['id']],math_units=unit_count,lexical_pair_records=0,transfer_rows=len(ledger),stable_targets=len(ot))))
