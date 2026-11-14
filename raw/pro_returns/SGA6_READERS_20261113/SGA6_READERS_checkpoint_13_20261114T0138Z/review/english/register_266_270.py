#!/usr/bin/env python3
"""Register the full semicontinuity definition, rank proof and local criteria."""
from pathlib import Path
from collections import Counter
import hashlib,json,re
from reviewed_french import load_reviewed_pages
from verify_reviewed_english import split,MATH
H=Path(__file__).resolve().parent;R=H.parents[1]
sha=lambda s:hashlib.sha256(s.encode()).hexdigest()
chunk=(H/'EN_EXPOSE_III_P266_270.tex').read_text();native=(H/'SGA6_EN_native_flattened_UNVERIFIED.tex').read_text()
a=native.index(r'If \(E\) satisfies (\hyperlink{sga6.e03.lem.5-1}',native.index(r'\sgaStableTarget{sga6.e03.eq.unnamed.occ2}'))
b=native.index(r'is locally constant on \(U\). This gives constructibility.',native.index(r'\sgaStableTarget{sga6.e03.cor.5-6}',a))
record=dict(id='EN-EXPOSE-III-266-270',page='266–270',place='Completion of the base-change lemma, full semicontinuity definition, rank calculation and local-flatness criterion',layer='both',old=native[a:b],new=chunk,status='accepted passage comparison; exact scanned French decisions supplied by coordinator',source='build/page_packets/266–270/current.tex and diplomatic.tex; review/expose_iii/patches.jsonl',reason='Restores the complete source definition with f and every point, constant-sheaf notation and both examples, the entire rank identity and proof with the correct nonzero rank term, all original notes and their observed calls, full cokernel and exactness arguments and the actual local conditions. Four source differences are explicit; two French spelling/agreement repairs leave English unchanged.')
decisions=[json.loads(x) for x in (R/'review/expose_iii/decisions.jsonl').read_text().splitlines()];variants=[]
def add(no,old,printed,mode,finding):
 source=f'check/findings/findings_266_270.json#{finding}';d=next(x for x in decisions if x['source_id']==source)
 variants.append(dict(id=f'EN-VAR-{no:03}',page=269,old=old,printed=printed,corrected=old,mode=mode,source=source,reason=d['reason'],scope_start='%%%%%%%%%%  scan idx 282  |  folio 269',scope_end='%%%%%%%%%%  scan idx 283  |  folio 270',scan_image=d['image'],scan_region=d['region']))
add(177,r'(resp. \(\operatorname{rg}_{k(x)}H^1(E_{k(x)})\)) is upper semi-continuous',r'(resp. \(\operatorname{rg}_{k(x)}H^1(E_{k(x)})\) is upper semi-continuous','text',5)
add(178,r'\operatorname{rg}(E_x)=\operatorname{rg}(E_{k(x)})',r'\operatorname{rg}(E_x)=\operatorname{rg}(E_{k(X)})','math',6)
add(179,r"\(Z'^p(E)\) are flat",r"\(Z'^p(E)\)) are flat",'text',7)
add(180,r'H^1(E_{k(x)})\simeq H^1(E)_{k(x)}',r'H^1(E_{k(x)}\simeq H^1(E)_{k(x)}','math',9)
cur,ref=load_reviewed_pages(270,start=266);dip,dref=load_reviewed_pages(270,'diplomatic',start=266);ledger=[];unit_count=0
for layer,reading,fr,rr in [('current','corrected',cur,ref),('diplomatic','printed',dip,dref)]:
 text=chunk
 for v in variants:
  a=text.index(v['scope_start']);b=text.index(v['scope_end'],a);part=text[a:b];assert part.count(v['old'])==1,(v['id'],part.count(v['old']))
  text=text[:a]+part.replace(v['old'],v[reading],1)+text[b:]
 en=split(text)
 for page in range(266,271):
  f=Counter(m.group() for m in MATH.finditer(fr[page]));e=Counter(m.group() for m in MATH.finditer(en[page]));assert f==e,(page,layer,f-e,e-f)
  if layer=='current':unit_count+=sum(f.values())
  counts={}
  for token in [r'\underline{O}',r'\Ob',r'\mathrm L',r'\simeq',r'\operatorname{rg}',r'\sum',r'\tag',r'\SGAAuthorFootnote{1}',r'\SGAAuthorFootnote{*}',r'\SGAAuthorFootMark{1}',r'\SGAAuthorFootText{1}']:
   counts[token]=dict(French=fr[page].count(token),English=en[page].count(token));assert counts[token]['French']==counts[token]['English'],(page,layer,token)
  ledger.append(dict(page=page,layer=layer,source_id='exact reviewed page glyph inventory',decision='Every complete mathematical unit matches literally, including whitespace and note calls in the display. All counted glyphs, tags and original-note labels agree.',source=next(x for x in rr['bases'] if x['page']==page),counts=counts,reviewed_French_page_sha256=sha(fr[page]),English_page_sha256=sha(en[page])))
for raw in (R/'review/expose_iii/patches.jsonl').read_text().splitlines():
 p=json.loads(raw)
 if 266<=p['page']<=270:ledger.append(dict(page=p['page'],source_id=p['source_id'],layer=p['layer'],decision='Transferred in the faithful English source branches.',patch_record_sha256=sha(raw),source_reason=p['reason'],expected_source_count=p.get('expected_count',1)))
ledger.extend([
 dict(page=266,source_id='complete source conclusion5.3.1 and Remark5.3.2',decision='Preserve the complete degree-p/degree-minus-p-minus1 reasoning and both numbered conclusions before the short application remark. Folio266 is a genuinely short source leaf; do not move5.4 onto it or suppress its boundary.'),
 dict(page=267,source_id='check/findings/findings_266_270.json#1; fixes/MISPRINTS_6.json#226; fixes/FIXLOG_6_CURRENT.jsonl#384',decision='The source rep./resp. correction restores the missing s in the abbreviation for respectivement. The corresponding first list establishes its intended meaning; both English renderings use resp. for respectively. No different English relation or invented lexical error is supplied.'),
 dict(page=267,source_id='complete Definition5.4 and Examples5.4.1',decision='Restore the source function f rather than the inherited English phi, explicit x∈pt(X), all three local notions and every quantifier. Preserve M_X and H^0(X,M) exactly. Restore the complete Nakayama example, including the literal P in its rank-function formula and all stalk ring/field notation. English local stalk ring denotes exactly the source fiber x^*O_X already written O_X,x; no separate ring is introduced. Restore original note1 in full.'),
 dict(page=268,source_id='complete Lemma5.5 and ASTRA-III-AUTHOR-NOTE-268',decision='Restore the actual D-minus hypothesis, every degree restriction, both functor categories and all three conclusions. Preserve the two bare sums without added indices. Restore the numbered identity5.5.1 with its comma followed by the original numerical1 mark inside the display and matching complete note text afterward; no call is placed after We have. Retain both I5.9 and3.5 references in the proof.'),
 dict(page=269,source_id='full rank and exactness proof; ASTRA-III-AUTHOR-NOTE-269',decision='Restore E_k(x), the actual [-1,+1] interval and the complete displayed H^0=H^(-1)+H^1+rank(E_x) identity. The inherited English incorrectly inserted zero rank and a vague alternating-sign caveat. Restore every rank-function equality, both E-prime reductions, the original starred author note, Z-prime^i definition and the tagged exact sequence. The full proof retains each local-constancy argument and exactness deduction.'),
 dict(page=269,source_id='check/findings/findings_266_270.json#8; fixes/MISPRINTS_6.json#230; fixes/FIXLOG_6_CURRENT.jsonl#386',decision='French libre/libres is adjective agreement for the same two displayed cokernel modules. English locally free has the same form for singular and plural, so both English branches are identical at this adjective; the actual module formulas and joint subject remain explicit.'),
 dict(page=270,source_id='complete Lemma5.5(iii) and Corollary5.6',decision='Restore both source Mod(x) conditions, all four named stalk cokernels and literal EGA O_I locator, together with the exact finite-free conclusion on U. Preserve the plain and in the corollary opening, every hypothesis and repeated rank function, both distinct exact-functor statements, and the full initial generic-point proof. End at the actual source boundary immediately before the y-indexed rank function on271.'),
])
for v in variants:ledger.append(dict(page=v['page'],source_id=v['source'],decision='explicit English printed/corrected source variant',English_variant=v['id'],printed=v['printed'],corrected=v['corrected']))
pat=re.escape(r'\sgaStableTarget{')+r'([^}]+)\}';ot=set(re.findall(pat,record['old']));nt=set(re.findall(pat,chunk));assert ot==nt and len(ot)==5,(ot,nt)
path=H/'EN_TRANSLATION_PATCHES.jsonl';rows=[json.loads(x) for x in path.read_text().splitlines()];hits=[i for i,x in enumerate(rows) if x['id']==record['id']];assert len(hits)<=1
if hits:rows[hits[0]]=record
else:rows.append(record)
path.write_text(''.join(json.dumps(x,ensure_ascii=False)+'\n' for x in rows))
path=H/'EN_VARIANTS.jsonl';ids={v['id'] for v in variants};rows=[json.loads(x) for x in path.read_text().splitlines() if json.loads(x)['id'] not in ids]+variants;rows.sort(key=lambda x:int(x['id'].rsplit('-',1)[1]));path.write_text(''.join(json.dumps(x,ensure_ascii=False)+'\n' for x in rows))
path=H/'EN_APPROVED_LEXICAL_MATH_PAIRS.json';rows=[x for x in json.loads(path.read_text()) if not 266<=x['page']<=270];path.write_text(json.dumps(rows,ensure_ascii=False,indent=2)+'\n')
(H/'EN_EXPOSE_III_TRANSFER_266_270.jsonl').write_text(''.join(json.dumps(x,ensure_ascii=False)+'\n' for x in ledger))
path=H/'EN_AUTHOR_NOTE_MARKS.tsv';notes=[x for x in path.read_text().splitlines() if not x.startswith(('267\t','268\t','269\t'))]
notes.extend(['267\tAfter Definition5.4\traised numerical1 inside baseline parentheses\t1\tASTRA-III-AUTHOR-NOTE-267\tcoordinator direct primary/native comparison\tSGAAuthorFootnote{1}\tComplete topological-space comparison note.','268\tAfter comma within display5.5.1\traised numerical1 inside baseline parentheses\t1\tASTRA-III-AUTHOR-NOTE-268\tcoordinator direct primary/native comparison\tSGAAuthorFootMark{1}/SGAAuthorFootText{1}\tComplete definition of rg for a perfect complex with I6.11.','269\tAfter5.4.1(b) in rank proof\tbaseline parenthesized star\t*\tASTRA-III-AUTHOR-NOTE-269\tcoordinator direct primary/native comparison\tSGAAuthorFootnote{*}\tComplete headless H^1 comparison with both source parenthesis readings.'])
path.write_text('\n'.join(notes)+'\n')
print(json.dumps(dict(passage=record['id'],variants=sorted(ids),math_units=unit_count,lexical_pair_records=0,transfer_rows=len(ledger),stable_targets=len(ot))))
