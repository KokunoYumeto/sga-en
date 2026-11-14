#!/usr/bin/env python3
"""Register relative perfectness, duality, and the exchange lemma's opening."""
from pathlib import Path
from collections import Counter
import hashlib,json,re
from reviewed_french import load_reviewed_pages
from verify_reviewed_english import split,MATH
H=Path(__file__).resolve().parent;R=H.parents[1]
sha=lambda s:hashlib.sha256(s.encode()).hexdigest()
chunk=(H/'EN_EXPOSE_III_P256_260.tex').read_text();native=(H/'SGA6_EN_native_flattened_UNVERIFIED.tex').read_text()
a=native.index(r'\(E^a/B^a\) is \(h\)-flat.',native.index('On the other hand, the Tor-amplitude',native.index(r'\sgaStableTarget{sga6.e03.prop.4-6}')))
b=native.index(r'of the form \(\mathcal O_{U,X}\)',native.index(r'\sgaStableTarget{sga6.e03.lem.5-1}',a))
record=dict(id='EN-EXPOSE-III-256-260',page='256–260',place='Fibrewise perfection, external products, proper images, duality and beginning of the exchange lemma',layer='both',old=native[a:b],new=chunk,status='accepted passage comparison; exact scanned French decisions supplied by coordinator',source='build/page_packets/256–260/current.tex and diplomatic.tex; review/expose_iii/patches.jsonl',reason='Restores complete hypotheses, full fibre notation, all category names and duality formulas, all five original numerical notes, the first exchange conditions and complete canonical-arrow construction. Three supported locator differences are explicit; the author claim4.7(a) is retained with its independently documented defect, without a replacement assertion.')
decisions=[json.loads(x) for x in (R/'review/expose_iii/decisions.jsonl').read_text().splitlines()]
variants=[]
def add(no,page,old,printed,finding):
 source=f'check/findings/findings_256_260.json#{finding}';d=next(x for x in decisions if x['source_id']==source)
 variants.append(dict(id=f'EN-VAR-{no:03}',page=page,old=old,printed=printed,corrected=old,mode='text',source=source,reason=d['reason'],scope_start=f'%%%%%%%%%%  scan idx {page+13}  |  folio {page}',scope_end=f'%%%%%%%%%%  scan idx {page+14}  |  folio {page+1}' if page<260 else '',scan_image=d['image'],scan_region=d['region']))
add(172,257,r'\uline{Under the hypotheses of} (4.7)',r'\uline{Under the hypotheses of} (4.6)',3)
add(173,259,r'\uline{Under the hypotheses of} (4.9)',r'\uline{Under the hypotheses of} (4.8)',14)
add(174,259,'For the first assertion, apply (4.9)','For the first assertion, apply (4.8)',20)
cur,ref=load_reviewed_pages(260);dip,dref=load_reviewed_pages(260,'diplomatic');ledger=[];pairs=[];unit_count=0
for layer,reading,fr,rr in [('current','corrected',cur,ref),('diplomatic','printed',dip,dref)]:
 text=chunk
 for v in variants:
  a=text.index(v['scope_start']);b=text.index(v['scope_end'],a) if v['scope_end'] else len(text);part=text[a:b];assert part.count(v['old'])==1,(v['id'],part.count(v['old']))
  text=text[:a]+part.replace(v['old'],v[reading],1)+text[b:]
 en=split(text)
 for page in range(256,261):
  f=Counter(m.group() for m in MATH.finditer(fr[page]));e=Counter(m.group() for m in MATH.finditer(en[page]));missing=f-e;extra=e-f
  assert sum(missing.values())==sum(extra.values())==int(page==256),(page,layer,missing,extra)
  if layer=='current':unit_count+=sum(f.values())
  for ff,n in missing.items():
   ee=ff.replace(r'\uline{au voisinage de}',r'\uline{in a neighborhood of}').replace(r'\uline{et}',r'\uline{and}')
   assert ee!=ff and extra[ee]==n==1
   pairs.append(dict(page=page,layer=layer,French_literal_unit=ff,English_literal_unit=ee,expected_multiplicity=1,status='confirmed complete lexical formula translation: au voisinage de and et are translated; all other characters remain identical',scope='The exact Corollary4.6.1 displayed equivalence in the stated source branch.'))
  counts={}
  for token in [r'\underline{O}',r'\uparf',r'\parf',r'\Ob',r'\mathrm L',r'\mathrm R',r'\simeq',r'\underline{D}',r'\tag',r'\SGAAuthorFootnote{1}',r'\SGAAuthorFootnote{2}',r'\SGAAuthorFootnote{3}',r'\SGAAuthorFootnote{4}']:
   counts[token]=dict(French=fr[page].count(token),English=en[page].count(token));assert counts[token]['French']==counts[token]['English'],(page,layer,token)
  ledger.append(dict(page=page,layer=layer,source_id='exact reviewed page glyph inventory',decision='All mathematical units match literally apart from the one separately paired full display; all counted glyphs, display tags and original-note calls agree.',source=rr['bases'][page-1],counts=counts,reviewed_French_page_sha256=sha(fr[page]),English_page_sha256=sha(en[page])))
for raw in (R/'review/expose_iii/patches.jsonl').read_text().splitlines():
 p=json.loads(raw)
 if 256<=p['page']<=260:ledger.append(dict(page=p['page'],source_id=p['source_id'],layer=p['layer'],decision='Transferred in the faithful English source branches.',patch_record_sha256=sha(raw),source_reason=p['reason'],expected_source_count=p.get('expected_count',1)))
ledger.extend([
 dict(page=256,source_id='reviewed Corollary4.6.1 and Remark4.6.2',decision='Complete the preceding h-flat conclusion before the new corollary. Restore E_Xs, the full canonical Li_s definition, actual stalk subscript on the Tor-amplitude, complete displayed equivalence, and the exact conditions on every fiber. Preserve the printed proof substitution and regular-fiber remark.'),
 dict(page=257,source_id='reviewed product and base-change corollaries',decision='Preserve the hypothesis of4.7(b) inline and its conclusion in a separate display. Restore the four-sided Cartesian square with X on the left and X-prime on the right, complete E and interval data, both independent parf/uparf category alternatives and plain into/resp. connective spans. The subsequent direct-image proposition has its actual D-bounded hypothesis, historical2.1 provisos, and all N quantifiers.'),
 dict(page=258,source_id='ASTRA-III-AUTHOR-NOTES-258 and complete duality proposition',decision='Restore all four numerical author notes in source order, including both quasi-compact category equalities, the Lefschetz–Verdier/SGA5 attribution and the definition of f! in [H]. Preserve the D-plus hypothesis of4.8.1, all relative qualifiers, the actual R-underlined-Hom expression in4.9, and the complete factorization/duality proof split at its original folio boundary.'),
 dict(page=259,source_id='reviewed duality corollaries and ASTRA-III-AUTHOR-NOTES-259',decision='Restore all three headless duality comparisons and the complete biduality argument, with independently underlined D symbols and the baseline functor slot point. Preserve source order f!O_S=K_X and both canonical arrows. Restore the section5 numerical1 note and the complete commutative ringed-topos setting of5.1.'),
 dict(page=260,source_id='reviewed complete exchange conditions and canonical arrows',decision='Restore all four plain item labels a),a-prime),b),b-prime), their actual implications and all three starred display tags. The construction includes the literal E-dual definition, tensoring with M, Cartan adjunctionI7.4 and the full Ext-to-Hom comparison. Restore the source presentation M^1→M^0→M→0 and continue the sentence at its actual boundary; the native English had reversed these two terms.'),
])
p=R/'review/expose_iii/author_claim_256_257.json';assert p.exists()
ledger.append(dict(page=256,source_id='ASTRA-III-AUTHOR-CLAIM-256',source_packet='review/expose_iii/author_claim_256_257.json',source_packet_sha256=hashlib.sha256(p.read_bytes()).hexdigest(),decision='Preserve the full author statement4.7(a) and its proof reference in both English forms. The source packet gives the explicit Z/p finite-free-resolution example and dual-number unbounded derived tensor, including every scheme map, resolution differential and hypothesis check. Those counterexamples are audit evidence; no replacement statement or hypothesis is inserted into the source.',status='text/math transfer of the separately documented author claim; no fresh image claim'))
for v in variants:ledger.append(dict(page=v['page'],source_id=v['source'],decision='explicit English printed/corrected source variant',English_variant=v['id'],printed=v['printed'],corrected=v['corrected']))
for pair in pairs:ledger.append(dict(page=pair['page'],source_id='individually checked complete lexical display',decision='Translate only the stated lexical phrases in the complete display.',**{k:pair[k] for k in ['layer','French_literal_unit','English_literal_unit','expected_multiplicity']}))
pat=re.escape(r'\sgaStableTarget{')+r'([^}]+)\}';ot=set(re.findall(pat,record['old']));nt=set(re.findall(pat,chunk));assert ot==nt and len(ot)==12,(ot,nt)
path=H/'EN_TRANSLATION_PATCHES.jsonl';rows=[json.loads(x) for x in path.read_text().splitlines()];hits=[i for i,x in enumerate(rows) if x['id']==record['id']];assert len(hits)<=1
if hits:rows[hits[0]]=record
else:rows.append(record)
path.write_text(''.join(json.dumps(x,ensure_ascii=False)+'\n' for x in rows))
path=H/'EN_VARIANTS.jsonl';ids={v['id'] for v in variants};rows=[json.loads(x) for x in path.read_text().splitlines() if json.loads(x)['id'] not in ids]+variants;rows.sort(key=lambda x:int(x['id'].rsplit('-',1)[1]));path.write_text(''.join(json.dumps(x,ensure_ascii=False)+'\n' for x in rows))
path=H/'EN_APPROVED_LEXICAL_MATH_PAIRS.json';rows=[x for x in json.loads(path.read_text()) if not 256<=x['page']<=260]+pairs;path.write_text(json.dumps(rows,ensure_ascii=False,indent=2)+'\n')
(H/'EN_EXPOSE_III_TRANSFER_256_260.jsonl').write_text(''.join(json.dumps(x,ensure_ascii=False)+'\n' for x in ledger))
path=H/'EN_AUTHOR_NOTE_MARKS.tsv';notes=[x for x in path.read_text().splitlines() if not x.startswith(('258\t','259\t'))]
for page,label,place,body in [(258,'1','After first direct-image category conclusion','Full relative category equality and quasi-compactness explanation.'),(258,'2','After Corollary4.8.1 category conclusion','Full absolute category equality.'),(258,'3','After Proposition4.9 title before its stop','Full Lefschetz–Verdier coherent-sheaf attribution and SGA5III citation.'),(258,'4','After Proposition4.9 conclusion','Definition of f! in [H] Appendix4.'),(259,'1','After section5 heading','Statement that results are not used in the remainder of the Seminar.')]:
 notes.append(f'{page}\t{place}\traised numerical{label} inside baseline parentheses\t{label}\tASTRA-III-AUTHOR-NOTES-{page}\tcoordinator direct primary/native comparison\tSGAAuthorFootnote{{{label}}}\t{body}')
path.write_text('\n'.join(notes)+'\n')
print(json.dumps(dict(passage=record['id'],variants=sorted(ids),math_units=unit_count,lexical_pair_records=len(pairs),transfer_rows=len(ledger),stable_targets=len(ot))))
