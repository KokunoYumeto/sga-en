"""Final structural and record-coverage gates for the six complete readers."""
import collections,csv,hashlib,json,re,sys
from pathlib import Path
from fr_core import strip_comments,visible_projection
from build_en import select_inline_variants
from en_common import active_matches,group as en_group,replace_spans

ROOT=Path(__file__).resolve().parents[1];REC=ROOT/'output/records'
csv.field_size_limit(100_000_000)
FORMS={'FR':['SGA4_FR_diplomatique','SGA4_FR_corrige_apparat','SGA4_FR_texte_de_lecture'],
       'EN':['SGA4_EN_diplomatic','SGA4_EN_corrected_apparatus','SGA4_EN_reading']}
MASTERS={'FR':'SGA4_FR_master_annote','EN':'SGA4_EN_annotated_master'}

def read(p):return json.loads((ROOT/p).read_text())
def table(name):return list(csv.DictReader((REC/name).open(),delimiter='\t'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()

def corrected_with_marks(text):
    edits=[]
    for m in active_matches(r'\\SGA(?:quiet)?var\b',text):
        if any(a<=m.start()<b for a,b,_ in edits):continue
        try:
            _,_,j,_=en_group(text,m.end());new,_,j,_=en_group(text,j);ident,_,j,_=en_group(text,j)
        except ValueError:continue
        selected=corrected_with_marks(new)
        if m.group()==r'\SGAvar':selected+=r'\SGAvariantmark{'+ident+'}'
        edits.append((m.start(),j,selected))
    return replace_spans(text,edits)

def main():
    checks=[]
    def check(name,passed,evidence):
        checks.append(dict(check=name,passed=bool(passed),evidence=evidence))
    expected=[(str(p['tome']),p['expose'],str(p['folio'])) for p in read('sources/api_pass_20261111/PAGES.json')]
    masters={lang:(ROOT/'output'/lang.lower()/(name+'.tex')).read_text() for lang,name in MASTERS.items()}
    for lang,forms in FORMS.items():
        for mode,name in enumerate(forms):
            actual=(ROOT/'output'/lang.lower()/(name+'.tex')).read_text()
            if lang=='FR':want=masters[lang].replace(r'\providecommand\SGAForm{1}',r'\providecommand\SGAForm{'+str(mode)+'}',1)
            else:want='%% Generated from SGA4_EN_annotated_master.tex.\n\\def\\SGAform{%d}\n'%mode+masters[lang]
            check(name+' form identity',actual==want,'Only the documented form selector differs from its master.')
            classes=re.findall(r'\\documentclass(?:\[[^]]*\])?\{([^}]+)\}',strip_comments(actual))
            check(name+' system class',classes==['amsbook'],classes)
            external=re.findall(r'\\(?:input|include|includegraphics)(?![A-Za-z@])\s*(?:\[[^]]*\])?\s*\{([^}]+)\}',strip_comments(actual))
            check(name+' standalone source',not external,external)
    frbody=masters['FR'].split(r'\backmatter',1)[0]
    parts=re.findall(r'% BEGIN EXPOSE (\w+)\s*\n\\ifnum\\SGAForm=0\s*\n(.*?)\n\\else\s*\n(.*?)\n\\fi\s*\n',frbody,re.S)
    check('French complete exposé branches',len(parts)==20,{'count':len(parts),'exposes':[r[0] for r in parts]})
    for side,k in [('diplomatic',1),('corrected/reading',2)]:
        pages=[]
        for part in parts:pages.extend((t,part[0],p) for t,p in re.findall(r'\\SGApageno\{(\d)\}\{(\d+)\}',part[k]))
        check('French '+side+' page sequence',pages==expected,{'actual':len(pages),'expected':len(expected),'first_difference':next((i for i,(a,b) in enumerate(zip(pages,expected)) if a!=b),None)})
    for corrected,label in [(False,'diplomatic'),(True,'corrected/reading')]:
        text=select_inline_variants(masters['EN'],corrected).split(r'\backmatter',1)[0]
        pages=re.findall(r'\\SGApage\{(\d)\}\{(\w+)\}\{(\d+)\}',text)
        check('English '+label+' page sequence',pages==expected,{'actual':len(pages),'expected':len(expected),'first_difference':next((i for i,(a,b) in enumerate(zip(pages,expected)) if a!=b),None)})
    vf=read('output/records/FR_VARIANTS.json');ve=read('output/records/EN_VARIANTS.json')
    fids={v['id'] for v in vf};eids={v['id'] for v in ve}
    fm=re.findall(r'\\SGAvmark\{([^}]+)\}',frbody)
    em=re.findall(r'\\SGAvariantmark\{(EN-V\d+)\}',corrected_with_marks(masters['EN'].split(r'\backmatter',1)[0]))
    check('French variant/body correspondence',set(fm)==fids and len(fm)==len(fids),{'variants':len(fids),'marks':len(fm),'missing':sorted(fids-set(fm)),'unknown':sorted(set(fm)-fids)})
    check('English variant/body correspondence',set(em)==eids and len(em)==len(eids),{'variants':len(eids),'marks':len(em),'missing':sorted(eids-set(em)),'unknown':sorted(set(em)-eids),'duplicate_marks':[k for k,v in collections.Counter(em).items() if v>1]})
    check('French apparatus targets',set(re.findall(r'\\hypertarget\{sgav\.([^}]+)\}',masters['FR']))==fids,'Each variant has an apparatus destination.')
    check('English apparatus targets',set(re.findall(r'\\hypertarget\{app:([^}]+)\}',masters['EN']))==eids,'Each variant has an apparatus destination.')
    equal=[r['id'] for r in vf if visible_projection(r['printed'])==visible_projection(r['corrected'])]
    check('French entries describe visible differences',not equal,equal)
    equal=[r['id'] for r in ve if r['printed']==r['corrected']]
    check('English entries have distinct branch readings',not equal,equal)
    missing=[r['id'] for r in vf+ve if not str(r.get('source','')).strip()]
    check('Every variant has a source',not missing,missing)
    allmp={f'MP{i:04d}' for i in range(1,931)}
    mpfr=read('output/records/AGREED_MISPRINTS_PLACEMENT.json')
    check('French 930 canonical placement rows',{r['id'] for r in mpfr}==allmp and all(r['status'] in ['represented','represented-manual'] for r in mpfr),{'rows':len(mpfr),'statuses':dict(collections.Counter(r['status'] for r in mpfr))})
    mp_sources=set(re.findall(r'\bMP\d{4}\b','\n'.join(r['source'] for r in vf)))
    check('French 930 canonical apparatus source links',mp_sources==allmp,{'linked':len(mp_sources),'missing':sorted(allmp-mp_sources)})
    audit=read('output/records/EN_SOURCE_AUDIT.json');good={'paired','represented by existing variant','no English impact'}
    covered={r['id'] for r in audit if r.get('status') in good and r['id'] in allmp}
    check('English 930 canonical coverage',covered==allmp,{'covered':len(covered),'missing':sorted(allmp-covered)})
    en_sources=set(re.findall(r'\bMP\d{4}\b','\n'.join(r['source'] for r in ve)))
    noimpact={r['id'] for r in audit if r.get('status')=='no English impact' and r['id'] in allmp}
    check('English canonical source links or common reading',en_sources|noimpact==allmp,{'paired_source_ids':len(en_sources),'unchanged_English_ids':len(noimpact),'missing':sorted(allmp-(en_sources|noimpact))})
    judged=table('ONE_MODEL_MISPRINTS_JUDGED.tsv')
    check('All one-model judgments',len(judged)==1601 and len({r['id'] for r in judged})==1601 and all(r['reason'].strip() for r in judged),dict(collections.Counter(r['verdict'] for r in judged)))
    accepted={r['id'] for r in judged if r['verdict']=='accept' and r['application']=='accepted-candidate'}
    held={r['id'] for r in judged if r['verdict']=='accept' and r['application']=='hold-disputed-page'}
    humans={r['id'] for r in judged if r['verdict']=='accept' and r['application']=='preserve-human-apparatus'}
    fr_om=set(re.findall(r'OM-(?:OPUS|SOL)-\d{4}','\n'.join(r['source'] for r in vf)))
    en_om={r['id'] for r in audit if r.get('status') in good and r['id'] in accepted}
    check('Accepted one-model application partition',len(accepted)==338 and len(held)==159 and len(humans)==53,
      {'undisputed':len(accepted),'held_for_scan':len(held),'existing_human':len(humans)})
    check('French accepted undisputed one-model source links',accepted<=fr_om,
      {'expected':len(accepted),'missing':sorted(accepted-fr_om)})
    check('English accepted undisputed one-model assessments',en_om==accepted,
      {'expected':len(accepted),'represented_or_no_impact':len(en_om),'missing':sorted(accepted-en_om)})
    dispositions=read('output/records/EN_FINAL_DISPOSITIONS.json')
    check('English final per-part disposition register complete',
      dispositions['master_sha256']==sha(ROOT/'output/en/SGA4_EN_annotated_master.tex') and
      dispositions['record_count']==1268 and
      {r['id'] for r in dispositions['records']}==allmp|accepted and
      not dispositions['missing_part_evidence'] and
      all((r['disposition']=='no English impact' and r.get('reason') and r.get('unchanged_english_reading')) or
          r.get('every_reviewed_part_has_placement_evidence',False) for r in dispositions['records']),
      {k:v for k,v in dispositions.items() if k!='records'})
    en_om_sources=set(re.findall(r'OM-(?:OPUS|SOL)-\d{4}','\n'.join(r['source'] for r in ve)))
    held_applied=held.intersection(fr_om|en_om_sources)
    check('No newly applied held one-model source IDs',not held_applied,
      {'held_ids_found':sorted(held_applied)})
    disputed=table('DISPUTED_PLACES.tsv')
    check('All disputed items',len(disputed)==643 and len({r.get('id') for r in disputed})==643,{'rows':len(disputed)})
    hand=table('HAND_REPLAYS_PLACED.tsv')
    check('All hand replay decisions',len(hand)==56 and len({r['id'] for r in hand})==56 and not any('needs-' in r['status'] for r in hand),dict(collections.Counter(r['status'] for r in hand)))
    deferred=table('EN_DEFERRED_FRENCH_FIXES.tsv')
    check('293 deferred French port records',len(deferred)==293 and len({r['id'] for r in deferred})==293,{'rows':len(deferred)})
    tf=read('output/records/AGREED_TRANSCRIPTION_FIXES_AUDIT.json')
    check('898 agreed transcription fixes accounted',len(tf)==898 and all(not r.get(k,'unresolved').startswith('unresolved') for r in tf for k in ['source_status','dip_status','corr_status']),{'rows':len(tf),'unresolved':[(r['id'],k) for r in tf for k in ['source_status','dip_status','corr_status'] if r.get(k,'unresolved').startswith('unresolved')]})
    t3=read('output/records/FR_T3_FINAL_BRANCH_AUDIT.json')
    check('Tome III independent two-sided branch audit',len({r['id'] for r in t3})==378 and all(r[s]['verified'] for r in t3 for s in ['dip','corr']),{'records':len({r['id'] for r in t3}),'parts':len(t3)})
    reviewed=read('output/records/EN_REVIEWED_FINAL_BRANCH_AUDIT.json')
    check('English inspected pairs in both final branches',reviewed['passed'] and reviewed['master_sha256']==sha(ROOT/'output/en/SGA4_EN_annotated_master.tex'),
      {'items':reviewed['item_count'],'parts':reviewed['part_count'],'master_sha256':reviewed['master_sha256'],
       'failed':[(r['id'],r['part'],s) for r in reviewed['parts'] for s in ['diplomatic','corrected'] if not r[s]['verified']]})
    automatic=read('output/records/EN_T3_AUTOMATIC_REVIEW.json')
    check('English automatic Tome III review complete',automatic['reviewed_ids']==166 and automatic['all_final_assessments_present'] and automatic['master_sha256']==sha(ROOT/'output/en/SGA4_EN_annotated_master.tex'),
      {'reviewed_ids':automatic['reviewed_ids'],'outcomes':automatic['outcome_counts']})
    changes=read('output/records/EN_CHANGE_AUDIT.json')
    check('English change-log exact reconstruction',all(r['exact_reconstruction'] for r in changes['comparisons']) and next(r for r in changes['comparisons'] if r['comparison']=='complete generated source')['after_sha256']==sha(ROOT/'output/en/SGA4_EN_corrected_apparatus.tex'),changes['comparisons'])
    changes_fr=read('output/records/FR_CHANGE_AUDIT.json')
    comparisons=changes_fr['comparisons']
    full_source=[r for r in comparisons if r.get('target_file')=='fr/SGA4_FR_corrige_apparat.tex']
    check('French complete change-log forward and inverse reconstruction',
      len(comparisons)==42 and len(full_source)==2 and
      all(r['exact_reconstruction'] and r['exact_inverse_reconstruction'] and r['serialized_tsv_forward_and_inverse_verified'] for r in comparisons) and
      all(r['after_sha256']==sha(ROOT/'output/fr/SGA4_FR_corrige_apparat.tex') for r in full_source) and
      changes_fr['change_tsv_sha256']==sha(REC/'CHANGES_FR.tsv'),
      {'comparisons':len(comparisons),'complete_source_comparisons':len(full_source),
       'total_rows':changes_fr['total_rows'],'change_tsv_sha256':changes_fr['change_tsv_sha256']})
    glossary=table('GLOSSARY_SGA4_FR_EN.tsv')
    check('Glossary rows and observed rendering census',len(glossary)>=1000 and (REC/'GLOSSARY_SOURCE_SPANS.json').exists() and (REC/'GLOSSARY_SOURCE_CENSUS.json').exists(),{'glossary_rows':len(glossary),'source_span_records':len(read('output/records/GLOSSARY_SOURCE_SPANS.json'))})
    census=read('output/records/APPARATUS_COUNTS.json')
    keys=['variant_entries','human_record_dossiers','original_human_supplement','original_note_dossiers','original_proof_rewrite_records','editorial_reference_entries','nde_notes','disputed_items','possible_misprints']
    check('Reading-form apparatus census empty',all(all(r[k]==0 for k in keys) for r in census if r['form']=='reading'),{'reading_rows':sum(r['form']=='reading' for r in census)})
    preservation=read('output/records/HUMAN_EDITORIAL_PRESERVATION_AUDIT.json')
    check('Original human editorial records and notes preserved',preservation['passed'] and
      all(preservation['masters'][lang]['sha256']==sha(ROOT/'output'/lang.lower()/(MASTERS[lang]+'.tex')) for lang in ['FR','EN']),
      {'counts':preservation['counts'],'passed':preservation['passed'],'masters':preservation['masters']})
    one_model_en=read('output/records/EN_ONE_MODEL_FINAL_BRANCH_AUDIT.json')
    check('English one-model final branch and source audit',one_model_en['passed'] and
      one_model_en['records']==338 and one_model_en['parts']==128 and
      one_model_en['master_sha256']==sha(ROOT/'output/en/SGA4_EN_annotated_master.tex'),
      {k:v for k,v in one_model_en.items() if k!='rows'})
    compile_status=read('output/records/COMPILE_STATUS.json')
    for r in compile_status:
        check(r['reader']+' compiled final PDF',r['finished'],{'source_sha256':r['tex_sha256'],'compiled_source_sha256':r['compiled_source_sha256'],'returncode':r['returncode'],'pdf_present':r['pdf_present'],'error_count':r['error_count']})
        check(r['reader']+' glyph coverage',r['missing_character_count']==0,{'missing_character_reports':r['missing_character_count']})
        check(r['reader']+' references settled',not r['unresolved_reference_warnings'],r['unresolved_reference_warnings'])
    marker_audit=read('output/records/PDF_PAGE_MARKER_AUDIT.json')
    check('All rendered original page markers',len(marker_audit)==6 and all(r['passed'] and r['original_page_labels']==1557 and r['pdf_sha256']==sha(ROOT/'output'/r['language'].lower()/(r['reader']+'.pdf')) for r in marker_audit),
      [{'reader':r['reader'],'passed':r['passed'],'original_page_labels':r.get('original_page_labels')} for r in marker_audit])
    master_renderings=read('output/records/MASTER_PDF_RENDERINGS.json')
    check('Annotated-master PDF selector correspondence',len(master_renderings)==2 and all(
      r['master_sha256']==sha(ROOT/'output'/r['language'].lower()/r['master']) and
      r['compiled_reader_sha256']==sha(ROOT/'output'/r['language'].lower()/r['compiled_reader']) and
      r['pdf_sha256']==sha(ROOT/'output'/r['language'].lower()/r['pdf']) and
      r['pdf_sha256']==sha((ROOT/'output'/r['language'].lower()/r['compiled_reader']).with_suffix('.pdf'))
      for r in master_renderings),master_renderings)
    for lang,forms in FORMS.items():
        for name in forms:
            qa=read('output/records/'+name+'_PDF_QA.json')
            check(name+' rendered page bounds and contents',
              qa['source_sha256']==sha(ROOT/'output'/lang.lower()/(name+'.tex')) and
              qa['pdf_sha256']==sha(ROOT/'output'/lang.lower()/(name+'.pdf')) and
              not qa['text_spans_outside_physical_page'] and
              not qa['consecutive_identical_pdf_contents_entries'] and
              not qa['unresolved_reference_warnings'],
              {k:v for k,v in qa.items() if k not in ['samples','sample_paths']})
    privacy=[]
    for folder in ['output','build_scripts']:
        for p in (ROOT/folder).rglob('*'):
            if not p.is_file() or p.suffix not in ['.py','.json','.tsv','.md','.tex','.log','.txt']:continue
            s=p.read_text(errors='replace').replace('univers@Dehornoy.tex','univers_source_filename')
            hits=re.findall(r'(?<![A-Za-z])/(?:Users|home|workspace|root)/[^\s<>]+|[A-Za-z0-9._%+\-]+@[A-Za-z0-9.\-]+\.[A-Za-z]{2,}',s)
            if hits:privacy.append({'file':str(p.relative_to(ROOT)),'count':len(hits)})
    check('No private paths or email addresses',not privacy,privacy)
    missing=[n for n in ['README.md','CHANGES_FR.tsv','CHANGES_EN.tsv','GLOSSARY_SGA4_FR_EN.tsv','GLOSSARY_INCONSISTENCIES.md','DECISIONS.tsv','APPARATUS_COUNTS.md'] if not (REC/n).exists()]
    check('Required report files present',not missing,missing)
    result={'passed':all(r['passed'] for r in checks),'checks':checks,'pass_count':sum(r['passed'] for r in checks),'check_count':len(checks)}
    (REC/'VERIFICATION.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    print('Verification:',result['pass_count'],'/',result['check_count'])
    for r in checks:
        if not r['passed']:print('FAIL',r['check'],str(r['evidence'])[:1600])
    return result['passed']

if __name__=='__main__':raise SystemExit(0 if main() else 1)
