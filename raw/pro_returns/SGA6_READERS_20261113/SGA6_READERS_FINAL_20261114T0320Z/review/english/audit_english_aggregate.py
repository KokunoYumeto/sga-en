#!/usr/bin/env python3
"""Final-assembly structural, original-note and cross-folio formula checks."""
from pathlib import Path
from collections import Counter
import csv,hashlib,json,re
from english_typography import MARK,note_records
from source_emphasis import MATH
from reviewed_french import load_reviewed_pages
from build_english_aggregate import annotate

EN=Path(__file__).resolve().parent
ROOT=EN.parents[1]
OUT=EN/'aggregate'


def sha(text):return hashlib.sha256(text.encode()).hexdigest()
def rows(path):return [json.loads(x) for x in path.read_text().splitlines() if x.strip()]
def save(name,value):(OUT/name).write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n')


def project_folio_comments(unit):
    removed=[]
    for m in MARK.finditer(unit):
        a=m.start();b=m.end()
        if b<len(unit) and unit[b]=='\n':b+=1
        removed.append(dict(start=a,end=b,literal=unit[a:b]))
    projected=unit
    for r in reversed(removed):projected=projected[:r['start']]+projected[r['end']:]
    restored=projected
    for r in removed:restored=restored[:r['start']]+r['literal']+restored[r['start']:]
    assert restored==unit
    return projected,removed


def main():
    catalog=json.loads((OUT/'INPUT_CATALOG.json').read_text())
    raw=(OUT/'SGA6_EN_raw_current.tex').read_text()
    native=(EN/'SGA6_EN_native_flattened_UNVERIFIED.tex').read_text()
    markers=list(MARK.finditer(raw))
    keys=[m[1] for m in markers]
    visible=re.findall(r'\\SGAPrintPage\{([^}]+)\}',raw)
    assert keys==visible and len(keys)==720 and len(set(keys))==720
    targets=lambda s:Counter(re.findall(r'\\sgaStableTarget(?:Inline)?\{([^}]+)\}',s))
    before,after=targets(native),targets(raw)
    hyperlinks=Counter(re.findall(r'\\hyperlink\{([^}]+)\}',raw))
    assert all(key in after for key in hyperlinks)
    assert all(count==1 for count in after.values())
    assert dict(before-after)=={'sga6.e00.eq.4-2':1,'sga6.e07.cor.2-9':1}
    removal=ROOT/'build/review_snapshots/english_vii_complete416_465/native_insertion_436.json'
    extra=dict(after-before)
    stable=dict(native_targets=sum(before.values()),final_targets=sum(after.values()),
        final_unique_targets=len(after),internal_hyperlinks=sum(hyperlinks.values()),dangling_hyperlinks=[],
        removed_targets=[dict(target='sga6.e00.eq.4-2',
            disposition='The native target labelled a compressed cotangent-class formula as4.2. Exact source reconstruction restores the distinct4.2 complex and4.3 class formula with opening.eq.4-2/opening.eq.4-3 destinations. No final hyperlink refers to the old destination.',
            source='EN_TRANSLATION_PATCHES.jsonl; full reviewed Exposé0 source11–12'),
            dict(target='sga6.e07.cor.2-9',disposition='Documented removal of the unsupported native-English Corollary2.9; the source passes directly from2.8 and its proof to section3.',
                source=removal.relative_to(ROOT).as_posix(),record_sha256=hashlib.sha256(removal.read_bytes()).hexdigest())],
        added_exact_source_equation_targets=extra)
    save('SOURCE_SPAN_COMPLETENESS.json',dict(
        native_sha256=sha(native),assembled_current_sha256=sha(raw),
        exact_sealed_span_applications=catalog['applications'],original_marker_keys=keys,
        numeric_folios=list(range(1,701)),front_rear_leaves=[k for k in keys if not k.isdigit()],
        each_original_marker_once=True,source_comment_and_visible_command_order_identical=True,
        no_remaining_numeric_gap=True,hyperlink_audit=stable,
        qualification='Exact source-span reconstruction and marker/target audit; image coverage remains attributed to the French reviewers, and prose comparison is documented in the transfer ledger.'))
    note_checks=[];cross_checks=[]
    for layer in ['current','diplomatic']:
        en=(OUT/f'MATERIALIZED_{layer}_before_layout.tex').read_text()
        fr,states=load_reviewed_pages(700,layer,start=1)
        numeric_marks={int(m[1]):m.group() for m in markers if m[1].isdigit()}
        joined=''.join(numeric_marks[p]+fr[p] for p in range(1,701))
        en_notes=note_records(en);fr_notes=note_records(joined)
        identity=lambda row:(row['page'],row['command'],row['label'])
        assert list(map(identity,en_notes))==list(map(identity,fr_notes))
        assert len(en_notes)==len(fr_notes)==111
        assert not re.search(r'\\footnote(?:mark|text)?\b',en)
        note_checks.append(dict(layer=layer,author_note_commands=len(en_notes),
            exact_page_command_label_sequence=[dict(page=r['page'],command=r['command'],label=r['label']) for r in en_notes],
            command_label_sequence_equal=True,no_unlabelled_legacy_note_commands=True,
            French_text_sha256=sha(joined),English_text_sha256=sha(en)))
        en_cross=[m.group() for m in MATH.finditer(en) if MARK.search(m.group())]
        fr_cross=[m.group() for m in MATH.finditer(joined) if MARK.search(m.group())]
        assert len(en_cross)==len(fr_cross)==1
        for f,e in zip(fr_cross,en_cross):
            pf,rf=project_folio_comments(f);pe,recs=project_folio_comments(e)
            assert pf==pe
            assert [m[1] for m in MARK.finditer(e)]==['527']
            assert r'\SGAPrintPage' not in e
            cross_checks.append(dict(layer=layer,source_folios=[526,527],equation='1.3.9',
                French_literal=f,English_literal=e,projected_complete_unit=pf,
                French_removed_nonprinting_comments=rf,English_removed_nonprinting_comments=recs,
                exact_payload_equal=True,comment_projection_reversible=True,
                visible_marker_outside_math=True))
    save('ORIGINAL_NOTE_LABEL_AUDIT.json',dict(scope='All numbered folios1–700',branches=note_checks,
        qualification='Every explicit author-note call/text command and its observed label geometry key agrees with the reviewed French. Translated note prose is separately covered by the manual transfer ledgers.'))
    save('CROSS_FOLIO_MATH_AUDIT.json',dict(method='Supplement to per-page literal-unit multisets: locate every complete mathematical environment crossing an original folio comment, remove only the recorded nonprinting comment line by a reversible projection, and compare complete payloads.',
        total_complete_crossing_units=2,branches=cross_checks,
        qualification='Two branch occurrences of the same equation1.3.9; no other complete mathematical unit crosses an original source-folio comment.'))
    # The primary source annotation is reversible before any presentation-only
    # line-break transport. Each exact complete insertion is inverted by ID.
    support=raw
    for p in rows(EN/'EN_AGGREGATE_MACRO_TRANSPORTS.jsonl'):
        assert support.count(p['old'])==1
        support=support.replace(p['old'],p['new'],1)
    variants=rows(OUT/'VARIANTS.jsonl')
    annotated,_=annotate(support,variants)
    assert annotated==(OUT/'SGA6_EN_annotated_unrendered.tex').read_text()
    branch_records=[]
    for layer,key in [('current','corrected'),('diplomatic','printed')]:
        materialized=annotated
        for variant in reversed(variants):
            probe,_=annotate(variant['old'],[dict(variant,scope_start='',scope_end='')])
            assert materialized.count(probe)==1,variant['id']
            materialized=materialized.replace(probe,variant[key],1)
        expected=support
        for v in variants:
            a=expected.index(v['scope_start']) if v.get('scope_start') else 0
            b=expected.index(v['scope_end'],a) if v.get('scope_end') else len(expected)
            part=expected[a:b];assert part.count(v['old'])==1
            expected=expected[:a]+part.replace(v['old'],v[key],1)+expected[b:]
        assert expected==materialized
        branch_records.append(dict(layer=layer,exact_reconstruction_pass=True,sha256=sha(expected)))
    generation=json.loads((OUT/'GENERATION_STATUS.json').read_text())
    book_dir=ROOT/generation['book_directory']
    stem='SGA6_EN_' if generation['final_names'] else 'DRAFT_SGA6_EN_'
    master=(book_dir/(stem+'annotated_master.tex')).read_text()
    form_checks=[]
    for form,mode in [('diplomatic',0),('corrected_apparatus',1),('reading',2)]:
        form_text=(book_dir/(stem+form+'.tex')).read_text()
        assert form_text==master.replace(r'\providecommand{\SGAReaderForm}{1}',r'\providecommand{\SGAReaderForm}{'+str(mode)+'}',1)
        form_checks.append(dict(form=form,mode=mode,only_master_switch_differs=True,sha256=sha(form_text)))
    save('SINGLE_MASTER_BRANCH_AUDIT.json',dict(variant_groups=len(variants),
        annotated_unrendered_sha256=sha(annotated),branches=branch_records,forms=form_checks))
    print(json.dumps(dict(markers=720,original_note_commands=111,crossing_math_units_per_branch=1,
        variant_groups=len(variants),single_master_branches_exact=True,dangling_hyperlinks=0)))


if __name__=='__main__':main()
