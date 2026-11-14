#!/usr/bin/env python3
"""Register the source finiteness-theorem passage through Corollary2.5."""
from pathlib import Path
from collections import Counter
import hashlib,json,re
from reviewed_french import load_reviewed_pages
from verify_reviewed_english import split,MATH
H=Path(__file__).resolve().parent;R=H.parents[1]
chunk=(H/'EN_EXPOSE_III_P236_240.tex').read_text();native=(H/'SGA6_EN_native_flattened_UNVERIFIED.tex').read_text()
a=native.index(r'\sgaStableTarget{sga6.e03.cor.1-12}');b=native.index(r'\emph{Proof.} Consequence of \hyperlink{sga6.e03.thm.2-2}{Theorem 2.2},',native.index(r'\sgaStableTarget{sga6.e03.cor.2-5}',a))
record=dict(id='EN-EXPOSE-III-236-240',page='236–240',place='Final relative-pseudo-coherence corollaries, finiteness theorem and its two proofs through Corollary2.5',layer='both',old=native[a:b],new=chunk,status='accepted passage comparison; exact scanned French decisions supplied by coordinator',source='build/page_packets/236–240/current.tex and diplomatic.tex; review/expose_iii/patches.jsonl',reason='Restores both bounded-above source categories, original inline functor and centered placeholder, exact source conjecture and case enumeration, complete spectral-sequence proof with its starred target, actual projective-space diagram, full finite-twist resolution and truncated triangle, source Rf_*(E) in the first approximation assertion, local-free higher direct image and all corollary data. The sole source variant is the q/i condition; the240 inequality is retained as > in both forms after the reviewed witness correction.')
v=dict(id='EN-VAR-161',page=238,old=r'\(q>a+r\)',printed=r'\(i>a+r\)',corrected=r'\(q>a+r\)',mode='text',source='check/findings/findings_236_240.json#13; fixes/FIXLOG_6_CURRENT.jsonl#377',reason='The higher direct image is R^qf_*(E). In the stated hypercohomology computation, q=p+j is the total degree, with j≤a from the complex and p≤r from the projective-space cover, so q≤a+r for potentially nonzero terms. The stated vanishing condition is therefore q>a+r for that same R^q. Current changes only the condition index to q; diplomatic retains the printed i while preserving R^q.',scope_start='%%%%%%%%%%  scan idx 251  |  folio 238',scope_end='%%%%%%%%%%  scan idx 252  |  folio 239',scan_image='scan/SGA6_scan_360dpi.pdf#page=252; scan/SGA6_witness_300dpi.djvu#page=249',scan_region='Proof2.2.2, higher-direct-image vanishing condition')
cur,ref=load_reviewed_pages(240);dip,dref=load_reviewed_pages(240,'diplomatic');ledger=[]
for layer,reading,fr,rr in [('current','corrected',cur,ref),('diplomatic','printed',dip,dref)]:
 a=chunk.index(v['scope_start']);b=chunk.index(v['scope_end'],a);part=chunk[a:b];assert part.count(v['old'])==1
 text=chunk[:a]+part.replace(v['old'],v[reading],1)+chunk[b:];en=split(text)
 for page in range(236,241):
  f=Counter(m.group() for m in MATH.finditer(fr[page]));e=Counter(m.group() for m in MATH.finditer(en[page]));assert f==e,(page,layer,f-e,e-f)
  counts={}
  for token in [r'\underline{O}',r'\underline{L}',r'\Ob',r'\operatorname{Sup}',r'\simeq',r'\cdot',r'\mathrm L',r'\ldots','hook',r'R^*f_*']:
   counts[token]=dict(French=fr[page].count(token),English=en[page].count(token));assert counts[token]['French']==counts[token]['English'],(page,layer,token)
  ledger.append(dict(page=page,layer=layer,source_id='exact reviewed page glyph inventory',decision='Every mathematical unit and the specified literal glyph counts agree exactly in both source forms; no lexical formula exception.',source=rr['bases'][page-1],counts=counts,reviewed_French_page_sha256=hashlib.sha256(fr[page].encode()).hexdigest(),English_page_sha256=hashlib.sha256(en[page].encode()).hexdigest()))
for raw in (R/'review/expose_iii/patches.jsonl').read_text().splitlines():
 p=json.loads(raw)
 if not 236<=p['page']<=240:continue
 decision='Transferred in the faithful English passage in both source forms.'
 if p['source_id']=='check/findings/findings_236_240.json#20':decision='The coordinator’s direct native-witness reading resolves the bound as >a in both source forms. The former interpretation as a printed ≥ misprint is withdrawn. Both English forms use >a; no English source variant is invented.'
 ledger.append(dict(page=p['page'],source_id=p['source_id'],layer=p['layer'],decision=decision,patch_record_sha256=hashlib.sha256(raw.encode()).hexdigest(),source_reason=p['reason'],expected_source_count=p.get('expected_count',1)))
ledger.extend([
 dict(page=236,source_id='reviewed Corollaries1.12–1.14 and section2',decision='Restore both D-minus restrictions in1.12, inline1.13 functor with its literal raised cdot and upright L, source operatorname Sup, exact1.2.1(c)/EGAIV1.4.3 references and title stop. Preserve the historical Conjecture2.1 heading and statement, with proper plain inside the word-rule pattern. The two cases of2.2 are original enumerated prose; no new theorem or contemporary answer is added.'),
 dict(page=237,source_id='reviewed first finiteness proof and start of projective proof',decision='Restore reference1.3, plain derived R, source spectral-sequence target R-star rather than substituting p+q, original star tag, all r/N+r bounds and both proof labels with plain case numbers. Restore ordinary P at both projective-space vertices and the full eight-edge source diagram with three hooks, actual j-prime, p-prime and g-prime endpoints.'),
 dict(page=238,source_id='reviewed projective reduction and Theorem2.2.2',decision='Restore inline j-prime_*Rf_*(E), exact headless displayed comparison, ordinary P, explicit a∈Z and E∈D^b(X)_coh, full twisting parenthesis, the actual underlined L(X) category, strict n>0 in the negative twists and loc.cit. wording. Preserve I2.10(a)/II2.2.8(a), all source parentheses, literal low dots and exact two zeros of E-prime. The q/i condition alone is an explicit source variant.'),
 dict(page=239,source_id='reviewed completion of finiteness proof',decision='Restore the original starred triangle and its hooked upper tail, with no added[1] or central tick. The first approximation assertion tests Rf_*(E), as printed, rather than the inherited English E-prime. Restore I4.10, the full local-freeness assertion for R^r f_*O(-n), headless shifted comparison and every later argument. Preserve the single continuous paragraph at For this and the source bounded-degree condition on E-prime.'),
 dict(page=240,source_id='reviewed Corollaries2.3–2.5',decision='Restore embedding for plongement, actual ordinary P=P(F), complete quasi-coherent finite-type F, derived tensor in M(n), explicit a∈Z and unparenthesized Rf_*E(n). Restore the source EGAIII1.4.12/IV1.7.21 references and1.2 locator. Corollary2.4’s final display has no added stop;2.5’s retains its printed stop. Both forms use the inspected >a proof bound.'),
 dict(page=240,source_id='check/findings/findings_236_240.json#20; fixes/FIXLOG_6_CURRENT.jsonl#378',decision='The revised source decision treats the faint primary speck as a transcription issue resolved by the witness’s ordinary >. Both English source branches preserve >; no ≥/> apparatus entry is created.'),
 dict(page=v['page'],source_id=v['source'],decision='explicit English printed/corrected source variant',English_variant=v['id'],printed=v['printed'],corrected=v['corrected'])])
pat=re.escape(r'\sgaStableTarget{')+r'([^}]+)\}';ot=set(re.findall(pat,record['old']));nt=set(re.findall(pat,chunk));assert ot==nt and len(ot)==12,(ot,nt)
path=H/'EN_TRANSLATION_PATCHES.jsonl';rows=[json.loads(x) for x in path.read_text().splitlines()];hits=[i for i,x in enumerate(rows) if x['id']==record['id']];assert len(hits)<=1
if hits:rows[hits[0]]=record
else:rows.append(record)
path.write_text(''.join(json.dumps(x,ensure_ascii=False)+'\n' for x in rows))
path=H/'EN_VARIANTS.jsonl';rows=[json.loads(x) for x in path.read_text().splitlines() if json.loads(x)['id']!=v['id']]+[v];rows.sort(key=lambda x:int(x['id'].rsplit('-',1)[1]));path.write_text(''.join(json.dumps(x,ensure_ascii=False)+'\n' for x in rows))
(H/'EN_EXPOSE_III_TRANSFER_236_240.jsonl').write_text(''.join(json.dumps(x,ensure_ascii=False)+'\n' for x in ledger))
print(json.dumps(dict(passage=record['id'],variants=[v['id']],math_units=215,lexical_pair_records=0,transfer_rows=len(ledger),stable_targets=len(ot))))
