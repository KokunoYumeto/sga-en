#!/usr/bin/env python3
"""Register the exact opening of ExposéIII against both reviewed source forms."""
from pathlib import Path
from collections import Counter
import hashlib,json,re
from reviewed_french import load_reviewed_pages
from verify_reviewed_english import split,MATH
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1]
chunk=(HERE/'EN_EXPOSE_III_P222_225.tex').read_text();native=(HERE/'SGA6_EN_native_flattened_UNVERIFIED.tex').read_text()
a=native.index(r'\sgaStableTarget{sga6.e03.expose}');b=native.index(r'Thus one may suppose that \(Y=Z[T_1,\ldots,T_r]\)',a)
record=dict(id='EN-EXPOSE-III-222-225',page='222–225',place='ExposéIII title, Theorem1.1 and first four lemmas through the225 proof boundary',layer='both',old=native[a:b],new=chunk,status='accepted passage comparison; exact scanned French decisions supplied by coordinator',source='build/page_packets/222–225/current.tex and diplomatic.tex; review/middle/patches.jsonl; review/expose_iii/patches.jsonl',reason='Restores the complete source theorem, original numerical1/2 notes at their actual calls, local Ob/ob distinctions, exact distinguished triangles and ticks, all source proof references, the actual term-vanishing expression E-double-prime^i=0, headless cohomology isomorphism, full descent wording, original base-change square and EGA locator, source enumeration, three hooked immersion diagrams and their exact labels. The printed n descent is retained in both forms with its separate proof audit.')
variants=[]
def add(number,page,old,printed,source,reason,region,mode='text'):
 variants.append(dict(id=f'EN-VAR-{number:03}',page=page,old=old,printed=printed,corrected=old,mode=mode,source=source,reason=reason,scope_start=f'%%%%%%%%%%  scan idx {page+13}  |  folio {page}',scope_end=f'%%%%%%%%%%  scan idx {page+14}  |  folio {page+1}' if page<225 else '',scan_image=f'scan/SGA6_scan_360dpi.pdf#page={page+14}; scan/SGA6_witness_300dpi.djvu#page={page+11}',scan_region=region))
add(152,223,r"\(H^n(i_*(E''))\)",r"\(H^n(i_*(E'')\)",'check/findings/findings_221_225.json#19','The first expression applies H^n to the complete object i_*(E-double-prime), but the printed form closes only the inner argument. The next expression applies the same composite H^n composed with i_* and prints both closers. Current adds only the missing outside parenthesis; diplomatic retains the exact first missing close. The degree n remains unchanged.','First H^n expression in final paragraph')
add(153,223,r'independent of the hypothesis on \(i_*(\underline{O}_X)\)',r'independent of the hypothesis on \(\bar i_*(\underline{O}_X)\)','check/findings/findings_221_225.json#21','The source defines the single closed immersion i:X→Y. At x, the stalk of i_*M at i(x) is M_x, and the surjection O_(Y,i(x))→O_(X,x) carries the displayed finite generators to the same generating elements over the quotient ring. This is exactly the direct image i_* from the lemma hypothesis. Current keeps that same unbarred i; diplomatic retains the observed extra bar.','Final parenthetical hypothesis on223')
add(154,224,'the Koszul complex','the Kozsul complex','check/findings/findings_221_225.json#23; fixes/FIXLOG_6_CURRENT.jsonl#372','The displayed regular-immersion construction uses the complex with exterior-power terms and differential sending the basis element epsilon_j to the corresponding ideal generator f_j, the Koszul resolution referenced in VII1.4. Diplomatic retains the transposed proper-name spelling Kozsul; current retains Koszul.','Complex name in Remark1.1.2')
add(155,225,r"i''_*(E)\ n\text{-\uline{pseudo-coherent}}",r"i''_*\ n\text{-\uline{pseudo-coherent}}",'check/findings/findings_221_225.json#28; fixes/FIXLOG_6_CURRENT.jsonl#373','The lemma fixes E in D(X) and applies the two closed-immersion direct-image functors to that object. Its proof uses the diagonal X→X-prime times_Y X-double-prime and compares those direct images; the right-hand object is therefore i-double-prime_*(E). Current restores only the omitted argument(E); diplomatic keeps the printed bare functor symbol.','Right side of the Lemma1.1.4 equivalence',mode='math')
current,ref=load_reviewed_pages(225);diplomatic,dref=load_reviewed_pages(225,'diplomatic');newpairs=[];ledger=[]
for layer,reading,french,reference in [('current','corrected',current,ref),('diplomatic','printed',diplomatic,dref)]:
 text=chunk
 for v in variants:
  a=text.index(v['scope_start']);b=text.index(v['scope_end'],a) if v['scope_end'] else len(text);section=text[a:b];assert section.count(v['old'])==1,(v['id'],section.count(v['old']))
  text=text[:a]+section.replace(v['old'],v[reading],1)+text[b:]
 en=split(text)
 for page in range(222,226):
  fu=Counter(m.group() for m in MATH.finditer(french[page]));eu=Counter(m.group() for m in MATH.finditer(en[page]));missing=fu-eu;extra=eu-fu
  assert sum(missing.values())==sum(extra.values())==int(page==225),(layer,page,missing,extra)
  for f,n in missing.items():
   e=f.replace('pseudo-cohérent','pseudo-coherent');assert extra[e]==n==1 and f!=e
   newpairs.append(dict(page=page,layer=layer,French_literal_unit=f,English_literal_unit=e,expected_multiplicity=1,status='confirmed complete lexical formula translation: only the two pseudo-cohérent predicates become pseudo-coherent; every mathematical token, source argument omission, rule command, space and line break retained',scope='This exact full display and its stated multiplicity only; current and diplomatic are separately approved.'))
  counts={}
  for token in [r'\underline{O}',r'\operatorname{Ob}',r'\ob',r'\simeq',r'\bar i',r'\SGAAuthorFootnote{1}',r'\SGAAuthorFootMark{2}',r'\SGAAuthorFootText{2}',r'"|" marking','hook']:
   counts[token]=dict(French=french[page].count(token),English=en[page].count(token));assert counts[token]['French']==counts[token]['English'],(layer,page,token,counts[token])
  ledger.append(dict(page=page,layer=layer,source_id='exact reviewed page glyph inventory',decision='All mathematical units agree literally apart from the individually approved complete predicate display; specified glyph multiplicities agree exactly.',source=reference['bases'][page-1],counts=counts,reviewed_French_page_sha256=hashlib.sha256(french[page].encode()).hexdigest(),English_page_sha256=hashlib.sha256(en[page].encode()).hexdigest()))
for directory in ['middle','expose_iii']:
 for raw in (ROOT/f'review/{directory}/patches.jsonl').read_text().splitlines():
  if not raw.strip():continue
  p=json.loads(raw)
  if not isinstance(p['page'],int) or not 222<=p['page']<=225:continue
  decision='Transferred in the exact English passage in both source forms.'
  if p['source_id']=='ASTRA-III-DESCENT-223':decision='Restore the printed n in the current French reference and retain n in both English forms. The same perfect-approximation map for n is an r-approximation for every r≥n; the repeated cone step for r=M−1,...,n ends in the printed n instance. No English n/m variant is invented.'
  if p['source_id']=='fixes/REPLAY_MANUAL_6.json#6':decision='Transfer the headless isomorphism sign; the later reviewed descent decision restores n after this earlier m-anchored replay. The final exact map is H^n(i_*E-double-prime)≃i_*H^n(E-double-prime) in both English forms.'
  ledger.append(dict(page=p['page'],source_id=p['source_id'],layer=p['layer'],decision=decision,patch_record_sha256=hashlib.sha256(raw.encode()).hexdigest(),source_reason=p['reason'],expected_source_count=p.get('expected_count',1)))
ledger.extend([
 dict(page=222,source_id='ASTRA-III-NOTES-222; exact reviewed Theorem1.1',decision='Restore single-rule EXPOSÉIII, double-rule capital title, complete underlined L.ILLUSIE author line, the inline source morphism, independent capital Ob in(i)/(iii) and lowercase ob in(ii)/proof, every source membership, exact triangle orientation and complete factorization. Keep the theorem references plain. Restore numerical1 note after D(X) and numerical2 call inside mbox before the displayed stop, with full note text including I2.15.'),
 dict(page=223,source_id='ASTRA-III-DESCENT-223; reviewed Lemma1.1.1',decision='The folio begins is indeed determined, continuing the prior sentence. Restore the full descending-induction wording, actual term condition E-double-prime^i=0 rather than replacing it with cohomology vanishing, the two triangular arrangements with transverse ticks and the stop after the second. Retain I2.13, both I2.6 uses and both I2.10(b) references. The source rule includes n inside the lemma predicate; the proof remains ordinary prose.'),
 dict(page=224,source_id='ASTRA-III-EGA-224; check/findings/findings_221_225.json#24',decision='Retain the full regular-immersion references VII1.4 and I4.8/4.14, the source square with X on the left and X-prime on the right, exact EGAIII1.4.15.4, plain the before the ruled base-change arrow, and the unlabelled first assertion followed by literal(ii). No new(i) token is inserted. Every n-prefix stays outside its independent predicate rule.'),
 dict(page=224,source_id='ASTRA-III-EGA-224 text/map identification',decision='Render fibres here as stalks: the base-change map is checked by the explicit affine module map B tensor_A M→(B/IB) tensor_(A/I)M, b tensor m↦(b mod IB) tensor m, with inverse induced by the same representatives. Restricting this map to the local rings at the source point gives the stalk map of the displayed sheaves. This records the particular source construction; it asserts no unrelated categorical distinction.'),
 dict(page=225,source_id='reviewed Lemma1.1.4 and proof diagrams',decision='Restore direct images i-prime_* and i-double-prime_* in the equivalence, the five exact source hooks, Y below the first diagram, i:X→Y and j:X→Z in the star-tagged triangle, projection label f-prime, and all bottom-level commas. Keep the attributed Lichtenbaum diagonal argument and both exact VII1.10/1.1.1 references. The raw chunk ends at the complete original225 sentence, before the next affine polynomial-ring reduction.'),
])
for v in variants:ledger.append(dict(page=v['page'],source_id=v['source'],decision='explicit English printed/corrected source variant',English_variant=v['id'],printed=v['printed'],corrected=v['corrected']))
for pair in newpairs:ledger.append(dict(page=pair['page'],source_id='individually checked complete lexical display',decision='only the two specified predicate words are translated',**{k:pair[k] for k in ['layer','French_literal_unit','English_literal_unit','expected_multiplicity']}))
pat=re.escape(r'\sgaStableTarget{')+r'([^}]+)\}';ot=set(re.findall(pat,record['old']));nt=set(re.findall(pat,chunk));assert ot==nt and len(ot)==7,(ot,nt)
path=HERE/'EN_TRANSLATION_PATCHES.jsonl';records=[json.loads(x) for x in path.read_text().splitlines()];hits=[i for i,x in enumerate(records) if x['id']==record['id']];assert len(hits)<=1
if hits:records[hits[0]]=record
else:records.append(record)
path.write_text(''.join(json.dumps(x,ensure_ascii=False)+'\n' for x in records))
path=HERE/'EN_VARIANTS.jsonl';ids={v['id'] for v in variants};rows=[json.loads(x) for x in path.read_text().splitlines() if json.loads(x)['id'] not in ids]+variants;rows.sort(key=lambda x:int(x['id'].rsplit('-',1)[1]));path.write_text(''.join(json.dumps(x,ensure_ascii=False)+'\n' for x in rows))
path=HERE/'EN_APPROVED_LEXICAL_MATH_PAIRS.json';pairs=[x for x in json.loads(path.read_text()) if not 222<=x['page']<=225]+newpairs;path.write_text(json.dumps(pairs,ensure_ascii=False,indent=2)+'\n')
(HERE/'EN_EXPOSE_III_TRANSFER_222_225.jsonl').write_text(''.join(json.dumps(x,ensure_ascii=False)+'\n' for x in ledger))
path=HERE/'EN_AUTHOR_NOTE_MARKS.tsv';notes=[x for x in path.read_text().splitlines() if not x.startswith('222\t')];notes.extend([
 '222\tAfter D(X) in Theorem1.1\traised numerical1 inside baseline parentheses\t1\tASTRA-III-NOTES-222\tcoordinator direct primary/witness comparison, main PDF236\tSGAAuthorFootnote{1}\tComplete derived-category note, separate from the theorem statement.',
 '222\tInside the equivalence display before its stop\traised numerical2 inside baseline parentheses\t2\tASTRA-III-NOTES-222\tcoordinator direct primary/witness comparison, main PDF236\tSGAAuthorFootMark{2}/SGAAuthorFootText{2}\tFull pseudo-coherent-subcategory note and I2.15; original mbox call wrapper retained.'
]);path.write_text('\n'.join(notes)+'\n')
print(json.dumps(dict(passage=record['id'],variants=sorted(ids),math_units=124,lexical_pair_records=len(newpairs),transfer_rows=len(ledger),stable_targets=len(ot))))
