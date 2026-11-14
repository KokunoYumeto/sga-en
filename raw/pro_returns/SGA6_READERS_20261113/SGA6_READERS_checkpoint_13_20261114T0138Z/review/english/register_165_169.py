#!/usr/bin/env python3
"""Register the Hom comparison and exact original globalization criteria."""
from pathlib import Path
import hashlib,json,re
from reviewed_french import load_reviewed_pages
from verify_reviewed_english import MATH,split

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
chunk=(HERE/'EN_EXPOSE_II_P165_169.tex').read_text()
native=(HERE/'SGA6_EN_native_flattened_UNVERIFIED.tex').read_text()
a=native.index('whence the first assertion.',native.index(r'\sgaStableTarget{sga6.e02.lem.2-1-2}'))
b=native.index('If $F$ is quasi-coherent of finite type',a)+len('If ')
record=dict(id='EN-EXPOSE-II-165-169',page='165–169',
 place='Lemma2.1.2 proof continuation through the first sentence of the169/170 sheaf argument',
 layer='both',old=native[a:b],new=chunk,
 status='accepted passage comparison; exact scanned French decisions supplied by early reviewer',
 source='build/page_packets/165–169/current.tex and diplomatic.tex; review/middle/patches.jsonl; review/expose_ii/patches.jsonl',
 reason='Restores the exact I-to-J presentation order, all six Hom nodes and unlabelled vertical arrows, baseline placeholder points, full Yoneda/effaceability proof and both cokernel formulas, plain category A/B and closed phi, double-lower-rule derived R, complete notation2.2.1, original167 author note, the source item labels(i),(i-prime),(ii),(iii),(iii-prime), original coproduct and positive exponent bounds, the stated immersion i, and the first covering argument. Six observed source differences remain explicitly branched.')
path=HERE/'EN_TRANSLATION_PATCHES.jsonl'
records=[json.loads(x) for x in path.read_text().splitlines()]
hits=[i for i,x in enumerate(records) if x['id']==record['id']]
if hits:records[hits[0]]=record
else:records.append(record)
path.write_text(''.join(json.dumps(x,ensure_ascii=False)+'\n' for x in records))

current,ref=load_reviewed_pages(169)
diplomatic,dref=load_reviewed_pages(169,'diplomatic')
en=split(chunk)
variants=[]
def variant(number,page,old,printed,source,reason,mode='text',start=None,end=None,region=''):
 variants.append(dict(id=f'EN-VAR-{number:03}',page=page,old=old,printed=printed,corrected=old,mode=mode,
  source=source,reason=reason,
  scope_start=start or f'%%%%%%%%%%  scan idx {page+13}  |  folio {page}',
  scope_end=end or (f'%%%%%%%%%%  scan idx {page+14}  |  folio {page+1}' if page<169 else None),
  scan_image=f'scan/SGA6_scan_360dpi.pdf#page={page+14}; scan/SGA6_witness_300dpi.djvu#page={page+11}',
  scan_region=region))

variant(113,165,r'\operatorname{Hom}_{A(S)}(.,\Gamma_S(G))',
 r'\operatorname{Hom}_{A(S)}(.,\Gamma_S(F))',
 'check/findings/findings_161_165.json#18; fixes/FIXLOG_6_CURRENT.jsonl#347',
 'The second presentation is an exact sequence of A(S)-modules ending in Gamma_S(F). Applying Hom_(A(S))(-,Gamma_S(G)) gives the bottom row of the printed diagram, whose two right-hand terms explicitly fix Gamma_S(G). The vertical comparison sends a sheaf map F to G to its section map Gamma_S(F) to Gamma_S(G). Current therefore restores G in this fixed second argument. The separately inspected placeholder is a baseline period in both forms.',
 mode='math',region='Functor applied to sequence(**)')
diagram=next(m.group(0) for m in MATH.finditer(en[165]) if r'\begin{tikzcd}' in m.group(0))
node=r'\operatorname{Hom}_{A(S)}(\Gamma_S(F),\Gamma_S(G)) \arrow[r]'
assert diagram.count(node)==1
variant(114,165,diagram,diagram.replace(node,r'\operatorname{Hom}_{A(S)}(F,G) \arrow[r]'),
 'check/findings/findings_161_165.json#19; review/expose_ii/add_165.py',
 'Applying Hom_(A(S))(-,Gamma_S(G)) to the displayed section presentation(**) gives the left nonzero term Hom_(A(S))(Gamma_S(F),Gamma_S(G)). The vertical arrow is the map f↦Gamma_S(f) from sheaf morphisms F to G to section-module morphisms. Current supplies the two omitted section functors in that one bottom node; diplomatic retains F,G. Every other node, arrow, argument and punctuation is identical.',
 mode='display',region='Bottom-left nonzero term of the Hom comparison diagram')
variant(115,165,'are visibly isomorphisms; the same','are visibly isomorphisms the same',
 'check/findings/findings_161_165.json#20',
 'The printed sentence has no punctuation between its two finite clauses. Current inserts the separating semicolon; diplomatic preserves the absence. Both claims and their order are unchanged.',
 region='First sentence following the diagram')
variant(116,168,r'\mathrm D^{-}(\Qcoh(S))_{\coh}',r'\mathrm D^{-}(\Qcoh(S)_{\coh}',
 'check/findings/findings_166_170.json#18',
 'The outer parenthesis of D-minus is unclosed in print. Notation2.2.1 defines the essential-image category D-minus(Qcoh(S))_coh on167. Current adds only the missing outside close; diplomatic retains the observed omission.',
 mode='math',end=r'\uline{Proof.}',region='Proposition2.2.2 essential-image notation')
variant(117,169,r'\uline{a quasi-coherent Ideal of} $\underline{O}_S$.',
 r'\uline{a quasi-coherent Ideal of} $\underline{O}_S$',
 'check/findings/findings_166_170.json#29',
 'The complete final item(iii-prime) ends without a stop in print. Current supplies the sentence-ending full stop; diplomatic retains its absence.',
 region='End of condition(iii-prime)')
variant(118,169,r'\uline{-Module,} $f\in\Gamma(X,L)$',
 r'\uline{-Module} $f\in\Gamma(X,L)$',
 'check/findings/findings_166_170.json#31',
 'The declaration introduces the scheme X, its invertible module L, and the section f in Gamma(X,L). Current inserts the omitted comma delimiting the section declaration after the description of L. All three objects, their membership and the immersion i:X_f to X remain unchanged.',
 region='Lemma2.2.3.1 variable list')
path=HERE/'EN_VARIANTS.jsonl';rows=[json.loads(x) for x in path.read_text().splitlines()]
ids={v['id'] for v in variants};rows=[x for x in rows if x['id'] not in ids]+variants
rows.sort(key=lambda x:int(x['id'].rsplit('-',1)[1]))
path.write_text(''.join(json.dumps(x,ensure_ascii=False)+'\n' for x in rows))

ledger=[]
for sourcefile in ['review/middle/patches.jsonl','review/expose_ii/patches.jsonl']:
 for raw in (ROOT/sourcefile).read_text().splitlines():
  p=json.loads(raw)
  if not isinstance(p['page'],int) or not 165<=p['page']<=169:continue
  ledger.append(dict(page=p['page'],source_id=p['source_id'],source_file=sourcefile,layer=p['layer'],
   decision='transferred with exact ordered patch composition and the six explicit English branches',
   patch_record_sha256=hashlib.sha256(raw.encode()).hexdigest(),source_reason=p['reason'],
   expected_source_count=p.get('expected_count',1)))
for layer,reading,french,reference in [('current','corrected',current,ref),('diplomatic','printed',diplomatic,dref)]:
 text=chunk
 for v in variants:
  a=text.index(v['scope_start']);b=text.index(v['scope_end'],a) if v.get('scope_end') else len(text)
  section=text[a:b];assert section.count(v['old'])==1,(v['id'],section.count(v['old']))
  text=text[:a]+section.replace(v['old'],v[reading],1)+text[b:]
 pages=split(text)
 for page in range(165,170):
  counts={}
  for token in [r'\underline{C}',r'\underline{S}',r'\underline{O}',r'\underline{\Hom}',
                r'\underline{\underline{R}}',r'\phi',r'\varnothing',r'\SGAAuthorFootnote{raisedstar}']:
   counts[token]=dict(French=french[page].count(token),English=pages[page].count(token))
   assert counts[token]['French']==counts[token]['English'],(layer,page,token,counts[token])
  ledger.append(dict(page=page,layer=layer,source_id='exact reviewed page glyph inventory',
   decision='literal command multiplicities agree in both materialized branches',
   source=reference['bases'][page-1],counts=counts))
ledger.extend([
 dict(page=165,source_id='fixes/REPLAY_MANUAL_6.json#3; check/findings/findings_161_165.json#17',
  decision='The middle replay is composed first. The identical later II old/new patch is verified as an exact duplicate and recorded once as already present, with no generic anchor skipping.',
  already_present_exact=ref['already_present_exact_patches']),
 dict(page=165,source_id='reviewed Hom comparison',decision='Source A_S subscripts, I-to-J presentations, all parentheses around Gamma arguments and all three unlabelled vertical arrows are restored. No native isomorphism tilde labels are imported.'),
 dict(page=166,source_id='reviewed Lemma2.1.3 proof',decision='The full Yoneda extension and both implications are retained. The source defines F^n and G^n as functors with baseline-period slots; the cokernel display is copied exactly, without the native broken Cokerigl token or replacement by a pointwise definition.'),
 dict(page=167,source_id='reviewed proof continuation',decision='Restore the initial zero in the exact sequence, the complete second cokernel display, both phi^0 and phi^n comparison maps and the separate b) proof paragraph. The source lowercase comme after the displayed full stop is represented by lowercase since.'),
 dict(page=167,source_id='reviewed Notation2.2.1',decision='Repeat every source finiteness qualifier in the definition; U↦Loclib(U) is inline as printed. The two derived R glyphs retain two lower rules.'),
 dict(page=167,source_id='ASTRA-II-NOTE-167',decision='Restore the entire raisedstar author note at the proposition label, before its full stop; no invented terminal heading stop precedes the call.'),
 dict(page=168,source_id='check/findings/findings_166_170.json#19; fixes/FIXLOG_6_CURRENT.jsonl#348',
  decision='No English branch for French tous→tout: both express every quasi-coherent O_S-Module in the singular source clause. Keep the complete U=open-of-S parenthesis and the non-resp. scope of conditions(i),(ii).'),
 dict(page=169,source_id='reviewed Proposition2.2.3 and proof',decision='Restore literal labels(i),(i-prime),(ii),(iii),(iii-prime), r_i≥0 and n_i>0 alternatives, the original coproduct, sum indexed by N-plus and tensor signs. These source expressions replace the inherited alternative finite-family formulation without asserting an unproved normalization. Both resp. alternatives and reference(iii) remain plain.'),
 dict(page=169,source_id='reviewed final169/170 boundary',decision='Keep the source final words The sheaf before the170 marker in the next chunk. The inherited replacement boundary ends after its initial If so the unreviewed continuation starts with F until170 is registered. No compilation is claimed for this intermediate169 boundary.'),
])
for v in variants:ledger.append(dict(page=v['page'],source_id=v['source'],decision='explicit English printed/corrected variant',English_variant=v['id'],printed=v['printed'],corrected=v['corrected']))
(HERE/'EN_EXPOSE_II_TRANSFER_165_169.jsonl').write_text(''.join(json.dumps(x,ensure_ascii=False)+'\n' for x in ledger))
path=HERE/'EN_AUTHOR_NOTE_MARKS.tsv'
notes=[x for x in path.read_text().splitlines() if not x.startswith('167\t')]
notes.append('167\tProposition2.2.2 label, before its stop\traised star inside baseline parentheses\t1\tASTRA-II-NOTE-167\tearly reviewer direct scan comparison, main PDF181 and witness178\tSGAAuthorFootnote{raisedstar}\tComplete original ancillary-result note restored.')
path.write_text('\n'.join(notes)+'\n')
pat=re.escape(r'\sgaStableTarget{')+r'([^}]+)\}'
old_targets=set(re.findall(pat,record['old']));new_targets=set(re.findall(pat,chunk))
assert old_targets and old_targets==new_targets,dict(missing=sorted(old_targets-new_targets),extra=sorted(new_targets-old_targets))
print(json.dumps(dict(passage=record['id'],variants=sorted(ids),transfer_rows=len(ledger),stable_targets=len(old_targets)),ensure_ascii=False))
