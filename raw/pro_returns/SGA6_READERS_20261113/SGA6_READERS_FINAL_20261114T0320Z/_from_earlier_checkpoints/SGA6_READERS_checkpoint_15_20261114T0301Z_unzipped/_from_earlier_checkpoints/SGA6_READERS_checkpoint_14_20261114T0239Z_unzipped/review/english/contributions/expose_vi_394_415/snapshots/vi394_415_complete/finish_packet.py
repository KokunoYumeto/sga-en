#!/usr/bin/env python3
"""Validate and document this contribution; sealing is a separate final action."""
from pathlib import Path
import csv,hashlib,json,re,sys
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[3]
sys.path.insert(0,str(ROOT/'review/english'))
from reviewed_french import load_reviewed_pages
from verify_reviewed_english import MATH,split
def sha(s):return hashlib.sha256(s.encode()).hexdigest()
def dump(name,data):(HERE/name).write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
raw=(HERE/'EN_EXPOSE_VI_P394_415.tex').read_text()
variants=[json.loads(x) for x in (HERE/'variants.jsonl').read_text().splitlines()]
spans=[json.loads(x) for x in (HERE/'translation_spans.jsonl').read_text().splitlines()]
literal=json.loads((HERE/'literal_math_verification.json').read_text())
assert literal['unexpected_difference_units']==0
assert len(variants)==66
targets=lambda t:re.findall(r'\\sgaStableTarget(?:Inline)?\{([^}]+)\}',t)
native=(ROOT/'review/english/SGA6_EN_native_flattened_UNVERIFIED.tex').read_text()
a=native.index(r'\sgaStableTarget{sga6.e06.sec.4}')
b=native.index(r'\sgaStableTarget{sga6.e07.expose}',a)
native_span=native[a:b]
assert native_span==spans[0]['old']==(HERE/'native_span_394_415.tex').read_text()
assert raw==spans[0]['new']
assert targets(raw)==targets(native[a:b])
assert len(targets(raw))==len(set(targets(raw)))==36
assert re.findall(r'@@[^@]+@@',raw)==[]
source_states={};source_notes=[]
for layer in ['current','diplomatic']:
    pages,ref=load_reviewed_pages(415,layer,start=394)
    for p,t in pages.items():
        assert t==(HERE/'source_packets'/str(p)/f'{layer}.tex').read_text(),(p,layer,'source state changed')
        marks=re.findall(r'\\(?:SGAAuthorFoot(?:note|Mark|Text)|footnote|footnotemark|footnotetext)\b',t)
        source_notes.append(dict(page=p,layer=layer,commands=marks))
    source_states[layer]=[dict(page=p,sha256=sha(t),mathematical_units=len(MATH.findall(t))) for p,t in pages.items()]
assert all(not r['commands'] for r in source_notes)
assert not re.findall(r'\\(?:SGAAuthorFoot(?:note|Mark|Text)|footnote|footnotemark|footnotetext)\b',raw)

# Run the actual sequential apparatus wrapping, rather than only replacing one branch.
apparatus=raw;anchor_checks=[]
for v in variants:
    a=apparatus.index(v['scope_start']);b=apparatus.index(v['scope_end'],a) if v['scope_end'] else len(apparatus)
    part=apparatus[a:b];assert part.count(v['old'])==1,(v['id'],'sequential apparatus count')
    for branch in ['printed','corrected']:
        assert v[branch].count('{')==v[branch].count('}'),(v['id'],branch,'unbalanced anchor')
    replacement=(r'\ifnum\SGAReaderForm=0\relax'+'\n'+v['printed']+'\n'+r'\else'+'\n'+v['corrected']+'\n'+r'\fi') if v['mode']=='display' else r'\var{'+v['printed']+'}{'+v['corrected']+'}{'+v['id']+'}'
    apparatus=apparatus[:a]+part.replace(v['old'],replacement,1)+apparatus[b:]
    anchor_checks.append(dict(id=v['id'],page=v['page'],unique_sequential_anchor=True,mode=v['mode'],brace_balanced_branches=True))
dump('sequential_apparatus_check.json',dict(checks=anchor_checks,count=len(anchor_checks),wrapped_body_sha256=sha(apparatus),limitation='Exact sequential anchor and branch-brace check; this is not a TeX compilation. Complete display branches remain outside var arguments.'))

coverage=[]
path=ROOT/'review/expose_vi/page_status.jsonl'
for n,line in enumerate(path.read_text().splitlines(),1):
    row=json.loads(line)
    if 394<=row['page']<=415:
        assert row['fully_checked'] is True
        coverage.append(dict(page=row['page'],attributed_source_record=f'review/expose_vi/page_status.jsonl#{n}',source_line_sha256=sha(line),source_record=row,
            translation_scope='Complete prose and formula placement checked against the reviewed source; source-image inspection remains attributed to the source reviewer.'))
assert [r['page'] for r in coverage]==list(range(394,416))
dump('attributed_source_coverage.json',coverage)
native_notes=re.findall(r'\\(?:SGAAuthorFoot(?:note|Mark|Text)|footnote|footnotemark|footnotetext)\b',native_span)
assert not native_notes
dump('author_note_inventory.json',dict(scope='394–415',source=source_notes,English_commands=[],native_span_commands=native_notes,decision='No original author notes occur in this interval; no label or note has been invented.'))
(HERE/'author_notes.tsv').write_text('page\tlabel\tcall_position\tfull_text_location\tsource_id\tstatus\n')

terms=[
(394,'foncteur des drapeaux','flag functor'),
(394,'fibré de drapeaux','flag bundle'),
(394,'catégorie des ensembles','category of sets'),
(394,'représentable','representable'),
(395,'définition fonctorielle','functorial definition'),
(395,'relations isobares','isobaric relations'),
(395,'fonctions symétriques élémentaires','elementary symmetric functions'),
(396,'complexes parfaits','perfect complexes'),
(398,'sous-anneau','subring'),
(400,'système inductif','inductive system'),
(401,'séparé complété','separated completion'),
(401,'fibré projectif','projective bundle'),
(401,'suite exacte canonique','canonical exact sequence'),
(402,'formule de projection','projection formula'),
(403,'somme directe','direct-sum decomposition'),
(407,'faisceau ample','ample sheaf'),
(408,'nilidéal','nil ideal'),
(408,'sections globales','global sections'),
(409,"idéal d'augmentation",'augmentation ideal'),
(410,'morphisme propre et parfait','proper and perfect morphism'),
(411,'schéma noethérien','noetherian scheme'),
(411,'sous-groupes additifs','additive subgroups'),
(412,'point fermé','closed point'),
(412,'idéaux maximaux','maximal ideals'),
(413,'composantes irréductibles','irreducible components'),
(414,'produit fibré','fibre product')]
terms_out=[]
for p,fr,en in terms:
    f=(HERE/'source_packets'/str(p)/'current.tex').read_text();e=split(raw)[p]
    assert fr in f,(p,fr,'French term absent')
    assert en in e,(p,en,'English term absent')
    terms_out.append([fr,en,p,fr,en,f.count(fr),e.count(en),'Exact source-anchored terminology candidate; shared glossary integration remains with the assembly owner.'])
with (HERE/'terms.tsv').open('w',newline='') as f:
    w=csv.writer(f,delimiter='\t',lineterminator='\n');w.writerow(['French','English','page','French_anchor','English_anchor','French_count','English_count','status']);w.writerows(terms_out)

status=dict(scope='English VI394–415',complete_translated_pages=22,
    raw_chunk='EN_EXPOSE_VI_P394_415.tex',raw_chunk_sha256=sha(raw),
    native_span_sha256=sha(spans[0]['old']),stable_targets=targets(raw),
    mathematical_units_per_branch=778,unexpected_difference_units=0,
    approved_lexical_pairs=len(json.loads((HERE/'lexical_math_pairs.json').read_text())),
    approved_lexical_difference_side_units=literal['approved_lexical_difference_side_units'],
    provisional_variants=len(variants),source_variant_rows=sum(json.loads(x)['record_type']=='source_variant' for x in (HERE/'transfer.jsonl').read_text().splitlines()),
    transfer_records=len((HERE/'transfer.jsonl').read_text().splitlines()),
    source_states=source_states,author_notes=0,folio_joins=21,continuation_command_count=32,
    prose_and_formula_placement='All22 pages manually compared with the exact reviewed French; native omissions and shortened proofs restored in the recorded passages.',
    PDF_compiled=False,PDF_viewed=False,
    remaining='Final numbering, registration, source-local apparatus state, aggregate compilation and visual inspection are assigned to the English assembly owner. No unresolved local translation or source-branch question remains.')
dump('VALIDATION.json',status)
(HERE/'STATUS.md').write_text('''# English VI, folios 394–415

All 22 pages have a complete English prose and formula-placement comparison with the exact reviewed French forms. One raw current chunk, 66 provisional variant groups and the full transfer ledger are complete. Each branch contains 778 mathematical units. The literal comparison has zero unexpected differences; 12 approved lexical-pair records account for the 44 difference-side occurrences. All 66 sequential apparatus anchors pass with disjoint, brace-balanced branches, and all 36 stable targets retain their native order.

The 21 folio joins are individually recorded. The chunk builder adds no separator bytes at a folio boundary. There are no original author notes in this interval. Both 16-command continuation blocks remain at the end of415 before the VII heading; their command payloads are identical and their providecommand state maps agree.

No English PDF was compiled or visually inspected for this contribution. Final registration, numbering, source-local apparatus state, aggregate compilation and visual inspection remain with the English assembly owner. Exact source-image coverage is attributed to the completed French VI review and is not claimed anew by this translation check.
''')
(HERE/'HANDOFF.md').write_text('''# Complete English transfer of VI, folios 394–415

This isolated contribution begins at `sga6.e06.sec.4` and ends immediately before `sga6.e07.expose`. It composes with the preceding VI365–393 contribution at the exact section4 destination and with the sealed VII contribution at its exposé destination. The whole source interval, including its bibliography and both continuation macro blocks, is present.

## Exact checks

The two literal branches each contain778 mathematical units, with zero unexpected differences. Twelve approved complete-unit lexical-pair records cover only internal words such as “with,” “for,” “whence,” “projective” and “noetherian”; all other mathematical bytes remain literal. There are66 provisional variants, of which54 carry differing mathematical units, and eight source spelling/agreement dispositions with identical English renderings. The exact source pages still match the current shared loader byte for byte. All36 stable destinations remain in their original order. Every apparatus anchor is unique when the actual two-branch wrapper is inserted sequentially; complete displays and the397 diagram remain outside macro arguments.

No author note occurs in394–415. The empty note table is supported by both reviewed source inventories and the manual transfer. The26 selected terminology pairs are local candidates; final glossary alignment remains with assembly.

## Complete passages restored

The native English had shortened several proofs and changed some formulas. The transfer restores the complete source paragraphs and formula placement: the block-symmetric argument and full general flag proof in4.3–4.8; the definitions of x, x′ and their associated graded classes; every step of5.2–5.3, including the negative-power basis and recurrence; the full Chern-class and filtration statements of5.5–5.9; the coefficientwise pushforward and5.10 calculations; the rank and nilpotence reductions in6.1–6.2; the support-defined filtration, tensor-support argument and full Lemmas6.7–6.8; the Serre attribution, three-term complex, flag-pullback proof and final basis product. Problem6.10 retains the source inclusion. The bibliography preserves source author order, titles and series wording.

The source changes remain separately visible. They include the constant1 terms in395, the corrected bound flag-sheaf index and locators in397–398, the associated-graded sign in402, the gamma substitution in403, the two missing pushforward subscripts in406, the gamma argument in407, total-cohomology indexing in411, the stalk index in412, the X′ coefficient sheaf in414 and the r-factor product in415. Every variant links to the exact source decision and its proof. Double-rule D/G/P glyphs remain diplomatic and the authorized bold glyphs remain current, with the represented-functor identity maps attributed to the source audit.

The printed effectués / corrected affectés in396 are rendered “being effected with weight” / “being assigned weight.” Other French accent, spelling or agreement corrections that do not change English are recorded without inventing an English error. The retained phrase “their class” on400 keeps its componentwise source interpretation. The413 all-powers phrase remains in both author forms; its exact positive-power localization maps and zero-power counterexample are retained in the attributed decision record without an added hypothesis.

## Joins and continuation state

`folio_continuity.json` lists every join with source and translation hashes. In particular,398/399 continues “taking / into account,”399/400 continues “as the / quotient,”407/408 continues “We denote by / epsilon,” and412/413 continues “Then there is an / integer.” The maker uses an empty-string concatenation and adds no blank line. All display continuations remain in their source paragraphs.

`boundary_macro_state.json` preserves the native and reviewed16-command blocks with exact hashes. Each providecommand leaves an already defined control sequence unchanged and otherwise installs the same replacement text. Their composition therefore preserves the same state as either identical block, with neither block moved earlier. The contribution ends before the VII target.

## Assembly handoff

The packet is ready for registration and final numbering. No English PDF was compiled or visually inspected here. The assembly owner retains aggregate rendering, macro-state capture and final body/apparatus visual inspection. `VALIDATION.json` and `literal_math_verification.json` delimit the checks actually completed. The immutable snapshot and its manifest accompany this handoff; frozen source reviews and previous English packets remain untouched.
''')
print(json.dumps({k:status[k] for k in ['complete_translated_pages','mathematical_units_per_branch','unexpected_difference_units','provisional_variants','source_variant_rows','transfer_records','folio_joins']}))
