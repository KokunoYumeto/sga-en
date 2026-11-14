#!/usr/bin/env python3
"""Register the exact reviewed opening of Exposé IV, without source variants."""
from pathlib import Path
from collections import Counter
import hashlib,json,re
from reviewed_french import load_reviewed_pages
from verify_reviewed_english import split,MATH

H=Path(__file__).resolve().parent;R=H.parents[1]
sha=lambda s:hashlib.sha256(s.encode()).hexdigest()
chunk=(H/'EN_EXPOSE_IV_P274_278.tex').read_text()
native=(H/'SGA6_EN_native_flattened_UNVERIFIED.tex').read_text()
a=native.index(r'\sgaStableTarget{sga6.e04.expose}')
b=native.index('The last two categories are full subcategories',a)
record=dict(id='EN-EXPOSE-IV-274-278',page='274–278',place='Complete opening, Grothendieck-group definitions and lemmas, and the four notation definitions of2.1',layer='both',old=native[a:b],new=chunk,status='accepted passage comparison; exact scanned French decisions supplied by reviewer',source='build/page_packets/274–278/current.tex and diplomatic.tex; review/expose_iv/patches.jsonl',reason='Restores all source inline/display boundaries, exact category notation and locators, original universal-property note, recursive C-index notation, source word-rule spans and the local parf expansion. Both source layers agree here; no English source variant is introduced.')
en=split(chunk);ledger=[];units=0
for layer in ['current','diplomatic']:
 fr,reference=load_reviewed_pages(278,layer,start=274)
 for page in range(274,279):
  f=Counter(m.group() for m in MATH.finditer(fr[page]));e=Counter(m.group() for m in MATH.finditer(en[page]));assert f==e,(page,layer,f-e,e-f)
  if layer=='current':units+=sum(f.values())
  counts={}
  for token in [r'\underline{O}',r'\Ob',r'\cl',r'\sum',r'\coprod',r'\SGAAuthorFootnote{1}',r'\uparf',r'\renewcommand{\parf}{\underline{\mathrm{parf}}}']:
   counts[token]=dict(French=fr[page].count(token),English=en[page].count(token));assert counts[token]['French']==counts[token]['English'],(page,layer,token)
  ledger.append(dict(page=page,layer=layer,source_id='exact reviewed page glyph inventory',decision='Every complete mathematical unit agrees literally; no lexical exception. Category letters, bare sums, original author label, coproducts and the local macro renewal have matching occurrence counts.',source=next(x for x in reference['bases'] if x['page']==page),counts=counts,reviewed_French_page_sha256=sha(fr[page]),English_page_sha256=sha(en[page])))
for raw in (R/'review/expose_iv/patches.jsonl').read_text().splitlines():
 p=json.loads(raw)
 if 274<=p['page']<=278:
  ledger.append(dict(page=p['page'],source_id=p['source_id'],layer=p['layer'],decision='Transferred in the faithful English source branches.',patch_record_sha256=sha(raw),source_reason=p['reason'],expected_source_count=p.get('expected_count',1)))
ledger.extend([
 dict(page=274,source_id='complete source opening and Lemma1.2',decision='Restore the separately ruled exposé line and doubly ruled title, exact author capitalization, all omitted I6.3/SGA5VIII2 references, inline universal-map and triangle formulas, plain paragraph number1.1, complete Lemma1.2 and its two source letter labels. The first exposition and proof use the source underline spans.'),
 dict(page=274,source_id='local parf definition',decision='The actual source renews parf to underline{mathrm{parf}} at this exposé opening. Preserve that definition at the same boundary. Later apparatus readings capture their body-local macro meanings; this renewal does not retroactively change earlier captured variants.',literal_definition=r'\renewcommand{\parf}{\underline{\mathrm{parf}}}'),
 dict(page=275,source_id='complete Lemmas1.3/1.4 and definition1.5',decision='Restore the exact V I2.1 locator, all four resp. word groups, source D^b(A) parenthetical without adding a second E-membership, literal bare sums, and inline exact sequence. Restore the acyclic bounded-complex definition and the full universal-map introduction; the1.5.1 display closes this folio.'),
 dict(page=276,source_id='ASTRA-IV-AUTHOR-NOTE-276; complete Lemma1.6',decision='Restore the whole original numerical1 note explaining the change of k(A) convention, after the complete ambient-category parenthesis and before its stop. Preserve the note’s claim as authored. Restore the actual V I1.2.3 reference, complete canonical Db(A) functor and inverse construction, all source parentheticals and the precise map1.5.1 used in its proof.'),
 dict(page=277,source_id='ASTRA-IV-UNDERLINE-277; ASTRA-IV-O-277',decision='Preserve the source’s Remark1.6.1, including both explicit criterion references and its authorial category comparison. The two structure-sheaf O glyphs have one rule each. In Definition1.7 the defining words exact and dense remain plain; the surrounding underlined word groups and the plain EGAIII3.1.1 locator are transferred individually. The source tel/resp.telle is French grammatical gender agreement with triangle/sequence; the shared English such that covers both antecedents without an invented extra mathematical alternative.'),
 dict(page=278,source_id='check/findings/findings_276_280.json#4; fixes/MISPRINTS_6.json#233',decision='Retain the printed C_{i−1} in the extension construction. The reviewed identification gives C_i=Ob(A_i) by the identity on objects and the full-category identity on Hom_C(E,F); no substitution of a category letter or added index on the colimit is made.',evidence='review/expose_iv/identification_278.json',evidence_sha256=hashlib.sha256((R/'review/expose_iv/identification_278.json').read_bytes()).hexdigest()),
 dict(page=278,source_id='complete Exercise1.9 and2.1 notation',decision='Translate cas non respé as first case, identifying the triangulated alternative explicitly by its source order. Preserve the complete exercise and plain hint prose, K_bullet/K^bullet section title and four separately stated definitions with left A-subscript notation. In particular the finite-perfect-amplitude category uses the source uparf token. The following paragraph belongs to279 and remains outside this registered replacement.'),
])
pat=re.escape(r'\sgaStableTarget{')+r'([^}]+)\}'
ot=set(re.findall(pat,record['old']));nt=set(re.findall(pat,chunk));assert ot==nt,(ot-nt,nt-ot)
path=H/'EN_TRANSLATION_PATCHES.jsonl';rows=[json.loads(x) for x in path.read_text().splitlines()];hits=[i for i,x in enumerate(rows) if x['id']==record['id']];assert len(hits)<=1
if hits:rows[hits[0]]=record
else:rows.append(record)
path.write_text(''.join(json.dumps(x,ensure_ascii=False)+'\n' for x in rows))
path=H/'EN_APPROVED_LEXICAL_MATH_PAIRS.json';rows=[x for x in json.loads(path.read_text()) if not 274<=x['page']<=278];path.write_text(json.dumps(rows,ensure_ascii=False,indent=2)+'\n')
(H/'EN_EXPOSE_IV_TRANSFER_274_278.jsonl').write_text(''.join(json.dumps(x,ensure_ascii=False)+'\n' for x in ledger))
path=H/'EN_AUTHOR_NOTE_MARKS.tsv';notes=[x for x in path.read_text().splitlines() if not x.startswith('276\t')];notes.append('276\tAfter ambient-category parenthesis, before stop\traised numerical1 inside baseline parentheses\t1\tASTRA-IV-AUTHOR-NOTE-276\treviewer direct primary/native comparison\tSGAAuthorFootnote{1}\tComplete original note changing the k(A) convention.');path.write_text('\n'.join(notes)+'\n')
print(json.dumps(dict(passage=record['id'],variants=[],math_units=units,lexical_pair_records=0,transfer_rows=len(ledger),stable_targets=len(ot))))
