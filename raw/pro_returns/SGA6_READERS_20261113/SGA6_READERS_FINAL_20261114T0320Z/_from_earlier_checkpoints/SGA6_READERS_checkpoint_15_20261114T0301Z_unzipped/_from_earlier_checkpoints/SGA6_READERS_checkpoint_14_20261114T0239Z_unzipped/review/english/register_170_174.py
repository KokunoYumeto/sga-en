#!/usr/bin/env python3
"""Register the complete ample-family proof and the divisorial resolution lemma."""
from pathlib import Path
import hashlib,json,re
from reviewed_french import load_reviewed_pages
from verify_reviewed_english import split

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
chunk=(HERE/'EN_EXPOSE_II_P170_174.tex').read_text()
native=(HERE/'SGA6_EN_native_flattened_UNVERIFIED.tex').read_text()
start=native.index(r'\sgaStableTarget{sga6.e02.lem.2-2-3-1}')
a=native.index('If $F$ is quasi-coherent of finite type',start)+len('If ')
prop=native.index(r'\sgaStableTarget{sga6.e02.prop.2-2-9}',a)
b=native.index('are fully faithful and have as essential image',prop)
record=dict(id='EN-EXPOSE-II-170-174',page='170–174',
 place='Continuation of the ample-family proof through the two174 K-minus-b functors',
 layer='both',old=native[a:b],new=chunk,
 status='accepted passage comparison; exact scanned French decisions supplied by early reviewer',
 source='build/page_packets/170–174/current.tex and diplomatic.tex; review/expose_ii/patches.jsonl; frozen_manifest.tsv',
 reason='Restores the finite generating sections h_ijk, their multiplied extensions, the positive n_i and all n≥n_i statement, both tensor-identity lines, the exact complete implications, Borelli–Kleiman author note, three-column Cartesian diagram with Y, local-cohomology coefficient sheaves and dimension n, printed affine-plane E forms and p-star, source Lemma2.2.8 label with its unchanged legacy target, full proof of the lifting assertions, all L rules and K-minus-b superscripts. Printed/current source differences are explicit; no normalization to the inherited alternative formulas is asserted.')
path=HERE/'EN_TRANSLATION_PATCHES.jsonl';rows=[json.loads(x) for x in path.read_text().splitlines()]
hits=[i for i,x in enumerate(rows) if x['id']==record['id']]
if hits:rows[hits[0]]=record
else:rows.append(record)
path.write_text(''.join(json.dumps(x,ensure_ascii=False)+'\n' for x in rows))

variants=[
 dict(id='EN-VAR-119',page=171,old=r"Y'=X'-U'",printed=r"Y'=X'-U",corrected=r"Y'=X'-U'",mode='math',
 source='check/findings/findings_171_175.json#4; fixes/MISPRINTS_6.json#151',
 reason='In the displayed Cartesian diagram, with g:X-prime to X, the upper open is U-prime=U times_X X-prime=g inverse(U). Therefore Y-prime=g inverse(X minus U)=X-prime minus U-prime. This exact inverse-image identity gives the corrected prime. Diplomatic retains the printed U.',
 scope_start='%%%%%%%%%%  scan idx 184  |  folio 171',
 scope_end='%%%%%%%%%%  scan idx 185  |  folio 172',
 scan_image='scan/SGA6_scan_360dpi.pdf#page=185; scan/SGA6_witness_300dpi.djvu#page=182',
 scan_region='Lemma2.2.6 proof, definition of Y-prime below the diagram'),
 dict(id='EN-VAR-120',page=174,old='assertions c) follow',printed='assertions c)) follow',corrected='assertions c) follow',mode='text',
 source='check/findings/findings_171_175.json#10; fixes/MISPRINTS_6.json#153',
 reason='The item reference has a second closing parenthesis without an opening parenthesis in print. Current removes that unmatched delimiter; the reference remains the same item c).',
 scope_start='%%%%%%%%%%  scan idx 187  |  folio 174',
 scope_end=r'\sgaStableTarget{sga6.e02.prop.2-2-9}',
 scan_image='scan/SGA6_scan_360dpi.pdf#page=188; scan/SGA6_witness_300dpi.djvu#page=185',
 scan_region='Final sentence applying1.2 in the proof of Lemma2.2.8'),
 dict(id='EN-VAR-121',page=174,old='This completes the proof.',printed='This completes the proof',corrected='This completes the proof.',mode='text',
 source='check/findings/findings_171_175.json#11; fixes/MISPRINTS_6.json#154',
 reason='The complete final proof sentence has no following full stop in either scan. Current supplies the sentence-ending stop; diplomatic retains the absence.',
 scope_start='%%%%%%%%%%  scan idx 187  |  folio 174',
 scope_end=r'\sgaStableTarget{sga6.e02.prop.2-2-9}',
 scan_image='scan/SGA6_scan_360dpi.pdf#page=188; scan/SGA6_witness_300dpi.djvu#page=185',
 scan_region='Proof end immediately before Proposition2.2.9')
]
path=HERE/'EN_VARIANTS.jsonl';rows=[json.loads(x) for x in path.read_text().splitlines()]
ids={v['id'] for v in variants};rows=[x for x in rows if x['id'] not in ids]+variants
rows.sort(key=lambda x:int(x['id'].rsplit('-',1)[1]))
path.write_text(''.join(json.dumps(x,ensure_ascii=False)+'\n' for x in rows))
current,ref=load_reviewed_pages(174)
diplomatic,dref=load_reviewed_pages(174,'diplomatic')
ledger=[]
for raw in (ROOT/'review/expose_ii/patches.jsonl').read_text().splitlines():
 p=json.loads(raw)
 if not 170<=p['page']<=174:continue
 decision='transferred in faithful English with independently marked source branches'
 if p['source_id']=='check/findings/findings_171_175.json#9':
  decision='English unchanged: plural canonical functors follows the printed plural article/adjective and the two actual displayed functors; the French noun agreement correction has no separate English reading'
 ledger.append(dict(page=p['page'],source_id=p['source_id'],layer=p['layer'],decision=decision,
  patch_record_sha256=hashlib.sha256(raw.encode()).hexdigest(),source_reason=p['reason'],
  expected_source_count=p.get('expected_count',1)))
for layer,reading,french,reference in [('current','corrected',current,ref),('diplomatic','printed',diplomatic,dref)]:
 text=chunk
 for v in variants:
  a=text.index(v['scope_start']);b=text.index(v['scope_end'],a)
  section=text[a:b];assert section.count(v['old'])==1
  text=text[:a]+section.replace(v['old'],v[reading],1)+text[b:]
 en=split(text)
 for page in range(170,175):
  counts={}
  for token in [r'\underline{C}',r'\underline{S}',r'\underline{O}',r'\underline{L}',
                r'\underline{\underline{E}}',r'\mathbb E',r'\varnothing',
                r'\mathrm K^{-,b}',r'\SGAAuthorFootnote{raisedstar}']:
   counts[token]=dict(French=french[page].count(token),English=en[page].count(token))
   assert counts[token]['French']==counts[token]['English'],(layer,page,token,counts[token])
  ledger.append(dict(page=page,layer=layer,source_id='exact reviewed page glyph inventory',
   decision='literal command multiplicities agree in both materialized branches',
   source=reference['bases'][page-1],counts=counts))
ledger.extend([
 dict(page=170,source_id='reviewed ample-family proof',decision='Restore the exact restriction F|S_fij, named finite generators h_ijk, cited extension references, h_ijk tensor f_ij^q_i, positivity n_i>0 and quantifier for every n≥n_i. Both Im identities, both Id factors and all source tensor exponents are retained.'),
 dict(page=170,source_id='reviewed170/171 boundary',decision='The split French quasi- | cohérent is translated as a | quasi-coherent Ideal across the marker; the complete sentence and all mathematical units are retained.'),
 dict(page=171,source_id='ASTRA-II-NOTE-171',decision='Restore the complete raisedstar author note crediting M. BORELLI and S. L. KLEIMAN and attributing the term ample family to the editor; preserve the printed initials and uppercase surnames.'),
 dict(page=171,source_id='reviewed Definition2.2.4/2.2.5 and Lemma2.2.6',decision='Defined ample family and divisorial remain plain. The inner or between dim(O_X,x)=0 and1 remains plain, independently of the outer underlined or. The full three-column diagram, source dimension n, headless local-cohomology isomorphism and separate zero display are restored.'),
 dict(page=172,source_id='reviewed proof2.2.7',decision='The reference is2.2.3(i-prime), matching the affine-open covering criterion on169; inherited English(ii) is not retained. Only Proof is underlined in the heading Proof of2.2.7.'),
 dict(page=172,source_id='reviewed affine-plane counterexample',decision='All172 E glyphs retain their two lower rules; the distinct173 mathbb E command is copied exactly. Restore k as a field, all sheaf subscripts, source p-star and the plain long arrow in the section isomorphism. No replacement by native A^2 is made.'),
 dict(page=172,source_id='reviewed172/173 boundary',decision='French tout faisceau | inversible becomes English every | invertible sheaf; the same adjective and noun remain in the continuous argument.'),
 dict(page=173,source_id='reviewed Lemma2.2.8',decision='The printed heading is Lemma, while the native stable target is named thm. Preserve that existing identifier for links without changing the displayed source label. Restore N-plus indexing, every independent L rule and the varnothing quotient superscripts.'),
 dict(page=174,source_id='reviewed complete proof of2.2.8',decision='Restore the full lifting construction, variable-open definition of L(U), restricted generators, explicit non-resp. condition, and the subcategory C_(1S) index. The opening conclusion and final and between the two functors remain plain. Both displayed source K complexes have superscript minus,b.'),
 dict(page=174,source_id='check/findings/findings_171_175.json#9; fixes/MISPRINTS_6.json#152',
  decision='French singular foncteur→plural foncteurs has no English variant: both render the two displayed canonical functors, already specified by the plural article and adjective.'),
])
for v in variants:ledger.append(dict(page=v['page'],source_id=v['source'],decision='explicit English printed/corrected variant',English_variant=v['id'],printed=v['printed'],corrected=v['corrected']))
(HERE/'EN_EXPOSE_II_TRANSFER_170_174.jsonl').write_text(''.join(json.dumps(x,ensure_ascii=False)+'\n' for x in ledger))
path=HERE/'EN_AUTHOR_NOTE_MARKS.tsv'
notes=[x for x in path.read_text().splitlines() if not x.startswith('171\t')]
notes.append('171\tDefinition2.2.4, after ample family\traised star inside baseline parentheses\t1\tASTRA-II-NOTE-171\tearly reviewer direct scan comparison, main PDF185 and witness182\tSGAAuthorFootnote{raisedstar}\tComplete original Borelli–Kleiman attribution and editor terminology note.')
path.write_text('\n'.join(notes)+'\n')
pat=re.escape(r'\sgaStableTarget{')+r'([^}]+)\}'
ot=set(re.findall(pat,record['old']));nt=set(re.findall(pat,chunk))
assert ot and ot==nt,dict(missing=sorted(ot-nt),extra=sorted(nt-ot))
print(json.dumps(dict(passage=record['id'],variants=sorted(ids),transfer_rows=len(ledger),stable_targets=len(ot)),ensure_ascii=False))
