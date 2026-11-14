#!/usr/bin/env python3
"""Build the final review packet from explicit inputs and dispositions.

The output remains in this contribution directory. Shared edition sources,
sealed packets, registries and builds are never written by this script.
"""
from pathlib import Path
from collections import defaultdict,Counter
import csv,hashlib,json,re
from lexical_inventory import prose_view,term_view,match_term,read,pages,strip_nonbody,MATH,fields as lex_fields
from terminology_decisions import DECISIONS,FALSE_PAIRS,NONTERMS

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]

def put(name,value):
    (HERE/name).write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n')

def tsv(name,rows,fields):
    with (HERE/name).open('w') as out:
        writer=csv.DictWriter(out,fieldnames=fields,delimiter='\t',lineterminator='\n')
        writer.writeheader();writer.writerows(rows)

def j(value):return json.dumps(value,ensure_ascii=False,separators=(',',':'))

def key(f,e,notation=False):
    if notation:return f,e
    # Capital Module is deliberately retained as its own source-written word.
    def fold(s):
        low=s.casefold()
        if re.search(r'\bModules?\b',s):low=low.replace('module','Module')
        return low
    return fold(f),fold(e)

def page_name(p):
    if p.isdigit():
        n=int(p)
        ranges=[(1,77,'0'),(78,159,'I'),(160,221,'II'),(222,273,'III'),(274,296,'IV'),(297,364,'V'),(365,415,'VI'),(416,465,'VII'),(466,497,'VIII'),(498,518,'IX'),(519,594,'X'),(595,615,'XII'),(616,666,'XIII'),(667,689,'XIV')]
        expose=next((x for a,b,x in ranges if a<=n<=b),'indexes' if n>=691 else 'blank leaf')
        return f'Exposé {expose}, printed p.{p}' if expose not in ['indexes','blank leaf'] else f'{expose}, printed p.{p}'
    return 'original leaf '+p

def main():
    corpus=json.loads((HERE/'SEARCH_CORPUS.json').read_text())
    order={p['page']:p['order'] for p in corpus}
    attested=json.loads((HERE/'LEXICON_ATTESTATIONS.json').read_text())
    unattested=json.loads((HERE/'LEXICON_UNATTESTED.json').read_text())
    index=json.loads((HERE/'PRINTED_INDEX_PAIRS.json').read_text())
    # Dollar-delimited full formula labels from SGA5 do not belong in a prose
    # projection. Account for every such input row explicitly and test its
    # complete mathematical token core, without any algebraic normalization.
    def math_core(s):
        s=s.strip()
        if s.startswith('$') and s.endswith('$'):return s[1:-1].strip()
        if s.startswith(r'\(') and s.endswith(r'\)'):return s[2:-2].strip()
        if s.startswith(r'\[') and s.endswith(r'\]'):return s[2:-2].strip()
        return s
    indexed_source_rows={f"{p['path']}#{p['line']}" for r in attested+unattested for p in r['provenance']}
    cat=json.loads(read('review/english/aggregate/INPUT_CATALOG.json'))
    census_paths=['review/english/GLOSSARY_SGA6_REVIEWED_001_296.tsv','review/english/GLOSSARY_SGA6_CANDIDATES.tsv']+[str(Path(p['directory'])/'terms.tsv') for p in cat['packets']]+[str(p.relative_to(HERE/'input_snapshots')) for p in (HERE/'input_snapshots/en/glossaries').glob('*.tsv')]
    missing_inputs=[]
    for relative in census_paths:
        for line,row in enumerate(csv.DictReader((HERE/'input_snapshots'/relative).open(),delimiter='\t'),2):
            if f'{relative}#{line}' not in indexed_source_rows:
                f,e=lex_fields(row);missing_inputs.append((relative,line,row,f,e))
    fm_pages=pages(read('build/FR_current_revised.tex'));em_pages=pages(read('review/english/aggregate/SGA6_EN_raw_current.tex'))
    f_units={p:Counter(math_core(m.group()) for m in MATH.finditer(strip_nonbody(t['text']))) for p,t in fm_pages.items()}
    e_units={p:Counter(math_core(m.group()) for m in MATH.finditer(strip_nonbody(t['text']))) for p,t in em_pages.items()}
    reference_math=[];math_pairs={}
    for relative,line,row,f,e in missing_inputs:
        assert MATH.fullmatch(f) and MATH.fullmatch(e),(relative,line,'unclassified input row',f,e)
        hits=[dict(page=p,French_count=f_units[p][math_core(f)],English_count=e_units[p][math_core(e)]) for p in fm_pages if f_units[p][math_core(f)] and e_units[p][math_core(e)]]
        record=dict(source=f'{relative}#{line}',French_literal_label=f,English_literal_label=e,attestations=hits,
            disposition='Complete formula-token core compared literally after removing only its outer math delimiters. No source occurrence or mathematical identification is inferred when there is no exact match.')
        reference_math.append(record)
        r=math_pairs.setdefault((f,e),dict(French=f,English=e,notation=True,complete_math_label=True,aliases_French=[f],aliases_English=[e],provenance=[],
            paired_page_attestations=hits,paired_page_English_count=sum(x['English_count'] for x in hits),paired_page_French_count=sum(x['French_count'] for x in hits),formula_bounded_interval_attestations=[],formula_bounded_pair_count=0))
        r['provenance'].append(dict(path=relative,line=line,kind='reference_complete_formula_label',row=row))
    for r in math_pairs.values():(attested if r['paired_page_attestations'] else unattested).append(r)
    put('REFERENCE_MATH_LABELS_AUDIT.json',reference_math)
    decisions=[]
    for term,(verdict,loci,reason) in DECISIONS.items():
        decisions.append(dict(id='TERM-'+re.sub(r'[^A-Za-z0-9]+','-',term).strip('-').upper(),French=term,verdict=verdict,loci=loci,reason=reason,
            evidence=[f'build/FR_current_revised.tex#folio{p.strip()}' for p in loci.split(';')],source_text_changed=False))
    put('TERMINOLOGY_DECISIONS.json',decisions)
    combined={};dispositions=[]
    for r in attested+unattested:
        f,e=r['French'],r['English'];lookup=(f.casefold(),e.casefold());notation=r['notation']
        reviewed=any(p['kind'].startswith('reviewed') for p in r['provenance'])
        reason=None;status='admitted'
        if not notation and f.casefold() in NONTERMS:
            status='excluded_nonterm_or_unscoped_notation';reason=NONTERMS[f.casefold()]
        elif lookup in FALSE_PAIRS:
            status='excluded_unpaired_or_superseded_pair';reason=FALSE_PAIRS[lookup]
        elif not r['paired_page_attestations']:
            status='not_exactly_coattested';reason='No complete lexical French/English pair was found on one printed leaf in the declared search view. A lemma form, different number, intervening qualifier, or a source phrase absent from this view is not assigned a fabricated occurrence count.'
        elif not (reviewed or notation or r['formula_bounded_pair_count'] or lookup==('de type fini','finite-type')):
            status='excluded_page_only_candidate';reason='A shared printed page alone did not provide the required reviewed passage or formula-bounded phrase witness.'
        provenance=[f"{p['path']}#{p['line']}" for p in r['provenance']]
        dispositions.append(dict(French=f,English=e,status=status,reason=reason,source_rows=provenance,reviewed_inventory=reviewed,
                                 paired_page_count=r['paired_page_English_count'],formula_interval_pair_count=r['formula_bounded_pair_count']))
        if status!='admitted':continue
        k=key(f,e,notation)
        if k not in combined:
            record=dict(r)
            # Keep the first source-inventory display spelling. Case aliases
            # are search-index keys only; proper names are never lowercased.
            record['index_rows']=[];record['entry_kind']='reference_formula_label' if r.get('complete_math_label') else ('named_TeX_token' if notation else 'lexical_phrase')
            combined[k]=record
        else:
            record=combined[k]
            # Identical search keys with case aliases count the same hits once.
            assert record['paired_page_English_count']==r['paired_page_English_count'],(k,'case-alias count mismatch')
            for field in ['aliases_French','aliases_English']:
                for v in r[field]:
                    if v not in record[field]:record[field].append(v)
            record['provenance'].extend(r['provenance'])

    def phrase_census(f,e):
        hits=[]
        for p in corpus:
            a,b=match_term(p['French_view'],f),match_term(p['English_view'],e)
            if a and b:hits.append(dict(page=p['page'],French_count=len(a),English_count=len(b)))
        return hits

    # Include the fully paired author indexes. Math-bearing labels stay exact
    # TeX labels, except for the declared simple lambda search alias.
    for row in index:
        f,e=row['French_resolved_label'],row['English_resolved_label']
        fm=[m.group() for m in MATH.finditer(f)]
        simple_greek=all(re.fullmatch(r'\\\(\\(?:lambda|gamma|tau|beta|alpha)\\\)',x) for x in fm)
        use_phrase=not fm or (simple_greek and any(ch.isalpha() for ch in MATH.sub('',f)))
        fn,en=(term_view(f),term_view(e)) if use_phrase else (re.sub(r'\s+',' ',f),re.sub(r'\s+',' ',e))
        k=key(fn,en,not use_phrase)
        if k not in combined:
            hits=phrase_census(fn,en) if use_phrase else []
            combined[k]=dict(French=fn,English=en,notation=not use_phrase,aliases_French=[f],aliases_English=[e],provenance=[],
                paired_page_attestations=hits,paired_page_English_count=sum(x['English_count'] for x in hits),paired_page_French_count=sum(x['French_count'] for x in hits),
                formula_bounded_interval_attestations=[],formula_bounded_pair_count=0,index_rows=[],entry_kind='lexical_phrase' if use_phrase else 'exact_printed_index_label')
        r=combined[k];r['index_rows'].append(row)
        r['provenance'].append(dict(path='review/english/terminology_final/PRINTED_INDEX_PAIRS.json',line=index.index(row)+1,kind='paired_printed_index',row=row))
        for field,val in [('aliases_French',f),('aliases_English',e)]:
            if val not in r[field]:r[field].append(val)

    # Macro expansion decisions are source-scoped and have already been adopted
    # by the English assembly owner.  They do not rewrite our captured body.
    macros=json.loads((HERE/'input_snapshots/macro_decisions_final/review/english/EN_MACRO_EXPANSION_DECISIONS.json').read_text())
    macro_by_id={r['id']:r for r in macros}
    french_pages=pages(read('build/FR_current_revised.tex'))
    english_pages=pages(read('review/english/aggregate/SGA6_EN_raw_current.tex'))
    composite_evidence=[]
    for f,e,fr_anchor,en_anchor,folios,reason in [
        ("foncteur d'oubli",'forgetful functor',r"\(\underline{S}\)-foncteur d'oubli",r'forgetful \(\underline{S}\)-functor',[157],DECISIONS["foncteur d'oubli"][2]),
        ('catégorie scindée','split category',r'\(\underline{S}\)-catégorie scindée',r'split \(\underline{S}\)-category',[88,89],
         'The same S-category U -> (category of left k_U-Modules) and the same specified splitting are retained. The identity functor fixes its objects, morphisms and chosen reindexing functors. The S qualifier interrupts the English lexical noun phrase; the count is of the two complete literal qualified anchors, not an invented uninterrupted phrase.'),
    ]:
        hits=[]
        for page in folios:
            a=french_pages[str(page)]['text'].count(fr_anchor);b=english_pages[str(page)]['text'].count(en_anchor)
            assert a==b==1,(f,page,a,b)
            assert [m.group() for m in MATH.finditer(fr_anchor)]==[m.group() for m in MATH.finditer(en_anchor)]
            hits.append(dict(page=str(page),French_count=a,English_count=b,French_literal_anchor=fr_anchor,English_literal_anchor=en_anchor))
        provenance=[p for r in attested+unattested if r['French']==f and r['English'] in [e,'forgetful'] for p in r['provenance']]
        combined.pop(key(f,'forgetful'),None)
        combined[key(f,e)]=dict(French=f,English=e,notation=False,aliases_French=[f,fr_anchor],aliases_English=[e,en_anchor],provenance=provenance,
            paired_page_attestations=hits,paired_page_English_count=sum(x['English_count'] for x in hits),paired_page_French_count=sum(x['French_count'] for x in hits),
            formula_bounded_interval_attestations=[],formula_bounded_pair_count=0,index_rows=[],entry_kind='reviewed_phrase_with_intervening_math',composite_reason=reason)
        composite_evidence.append(dict(French_headword=f,English_headword=e,occurrences=hits,reason=reason,mathematical_qualifiers_identical=True))
        for d in dispositions:
            if d['French']==f and d['English']==e:
                d.update(status='admitted_reviewed_composite_phrase',reason=reason,reviewed_anchor_count=len(hits))
            elif d['French']==f and d['English']=='forgetful':
                d.update(status='admitted_as_qualified_phrase_alias',reason='The complete qualified source anchor supports forgetful functor as the headword; the shorter adjective is not listed as a separate rendering.')
    put('QUALIFIED_PHRASE_ATTESTATIONS.json',composite_evidence)
    macro_specs=[
       ('EN-AGG-MACRO-GL-393',r'\GL',r'\operatorname{Gl}',r'\operatorname{Gl}',393,700),
       ('EN-AGG-MACRO-RED-502',r'\red',r'\text{réd}',r'\mathrm{red}',502,700),
       ('EN-AGG-MACRO-LENGTH-520',r'\longg',r'\operatorname{long}',r'\operatorname{length}',520,520),
       ('EN-AGG-MACRO-ZELL_QELL-681',r'\Zell',r'\mathbb Z_\ell',r'\mathbb Z_\ell',681,685),
       ('EN-AGG-MACRO-ZELL_QELL-681',r'\Qell',r'\mathbb Q_\ell',r'\mathbb Q_\ell',681,685),
       ('EN-AGG-MACRO-NAIF-698',r'\naif',r'\text{naïf}',r'\text{naive}',698,698),
    ]
    macro_evidence=[]
    for sid,token,f,e,start,end in macro_specs:
        hits=[]
        for page in range(start,end+1):
            a=len(match_term(strip_nonbody(french_pages[str(page)]['text']),token,True))
            b=len(match_term(strip_nonbody(english_pages[str(page)]['text']),token,True))
            if a or b:
                assert a==b,(sid,token,page,a,b)
                hits.append(dict(page=str(page),French_count=a,English_count=b))
        count=sum(r['English_count'] for r in hits)
        assert count,(sid,token)
        evidence=dict(source_id=sid,token=token,French_expansion=f,English_expansion=e,count=count,occurrences_by_page=hits,
                      reason=macro_by_id[sid]['proof'],scope=[start,end],status='accepted source-scoped expansion decision; edition application owned by English builder')
        macro_evidence.append(evidence)
        k=(f,e)
        combined[k]=dict(French=f,English=e,notation=True,aliases_French=[token,f],aliases_English=[token,e],provenance=[dict(path='review/english/EN_MACRO_EXPANSION_DECISIONS.json',line=list(macro_by_id).index(sid)+1,kind='source_scoped_macro_decision',row=evidence)],
            paired_page_attestations=hits,paired_page_English_count=count,paired_page_French_count=count,formula_bounded_interval_attestations=[],formula_bounded_pair_count=0,
            index_rows=[],entry_kind='source_scoped_macro_expansion',macro_decision=evidence)
    put('NOTATION_EXPANSION_CHOICES.json',macro_evidence)
    literal_notation=[]
    for page,f,e,n in [(545,r'\mathrm{red}',r'\mathrm{red}',3),(597,r'\text{réd}',r'\text{red}',1)]:
        a=sum(m.group().count(f) for m in MATH.finditer(french_pages[str(page)]['text']))
        b=sum(m.group().count(e) for m in MATH.finditer(english_pages[str(page)]['text']))
        assert a==b==n,(page,a,b,n)
        record=dict(page=page,French=f,English=e,count=n,reason=macro_by_id['EN-AGG-MACRO-RED-502']['proof'],source='review/english/terminology_final/MACRO_COUNT_CLARIFICATION.json',
                    scope='Literal labels in complete mathematical units, separately counted from red macro invocations.')
        literal_notation.append(record)
        combined[(f,e)]=dict(French=f,English=e,notation=True,aliases_French=[f],aliases_English=[e],provenance=[dict(path=record['source'],line=len(literal_notation),kind='source_scoped_literal_notation',row=record)],
            paired_page_attestations=[dict(page=str(page),French_count=n,English_count=n)],paired_page_English_count=n,paired_page_French_count=n,
            formula_bounded_interval_attestations=[],formula_bounded_pair_count=0,index_rows=[],entry_kind='source_scoped_literal_notation',literal_notation_reason=record['reason'])
    put('LITERAL_NOTATION_CHOICES.json',literal_notation)

    rows=[];evidence=[]
    for number,r in enumerate(sorted(combined.values(),key=lambda x:(x['French'].casefold(),x['English'].casefold())),1):
        rid=f'SGA6-TERM-{number:04d}'
        ix=r['index_rows'];kind=r['entry_kind'];hits=r['paired_page_attestations']
        if kind=='exact_printed_index_label':
            count=len(ix);loci=sorted({str(x['page']) for x in ix},key=lambda p:order[p]);first=loci[0]
            count_scope='Exact complete paired index-label rows on691–700, including explicitly resolved ditto labels; no body-token frequency is inferred.'
        else:
            count=r['paired_page_English_count'];loci=[x['page'] for x in hits];first=loci[0] if loci else str(ix[0]['page'])
            count_scope=('Exact named TeX command occurrences in the cited source-scoped folios; macro definitions and comments excluded.' if kind in ['named_TeX_token','source_scoped_macro_expansion'] else
                'Exact complete literal labels inside mathematical units on the named folio; distinct from macro-command invocation counts.' if kind=='source_scoped_literal_notation' else
                'Exact reviewed qualified phrase anchors containing the identical intervening mathematical qualifier; the complete anchors are preserved in QUALIFIED_PHRASE_ATTESTATIONS.json.' if kind=='reviewed_phrase_with_intervening_math' else
                'Complete formula-token core matched literally on a co-attesting leaf after removing only outer math delimiters; no algebraic or font normalization.' if kind=='reference_formula_label' else
                'English surface-form occurrences within original printed leaves that also contain the complete French search phrase; case-insensitive except explicit Module/Modules, TeX accents/formatting projected only in the search view; overlapping phrases counted independently.')
        refs=sorted(set(f"{p['path']}#{p['line']}" for p in r['provenance']))
        reviewed_loci=[]
        for p in r['provenance']:
            if p['kind'].startswith('reviewed'):
                a=p['row'];loc=next((a[k] for k in ['passage','folio','page','first_place'] if a.get(k)),None)
                if loc and str(loc) not in reviewed_loci:reviewed_loci.append(str(loc))
        term_decision=DECISIONS.get(r['French'].casefold())
        reason=term_decision[2] if term_decision else ('Literal printed index label paired with its unchanged definition reference.' if ix else 'Retain the source-anchored rendering. Supplied reference entries and local occurrence evidence are cited; no source or mathematical notation change is inferred from lexical matching.')
        if r.get('macro_decision'):reason=r['macro_decision']['reason']
        if r.get('literal_notation_reason'):reason=r['literal_notation_reason']
        if r.get('composite_reason'):reason=r['composite_reason']
        row=dict(id=rid,french_term_or_notation=r['French'],english_rendering=r['English'],count=count,first_place=page_name(first),
            kind=kind,count_scope=count_scope,source_loci='; '.join(dict.fromkeys(loci)),reviewed_loci='; '.join(reviewed_loci),
            French_aliases=j(r['aliases_French']),English_aliases=j(r['aliases_English']),definition_references='; '.join(dict.fromkeys(f"{x['expose']} {x['section']}" for x in ix)),
            paired_index_rows=len(ix),formula_bounded_pair_count=r['formula_bounded_pair_count'],sources='; '.join(refs),decision=reason)
        rows.append(row)
        evidence.append(dict(id=rid,French=r['French'],English=r['English'],kind=kind,count=count,paired_page_attestations=hits,
            formula_bounded_interval_attestations=r['formula_bounded_interval_attestations'],index_rows=[x['id'] for x in ix],source_rows=refs,case_and_TeX_aliases=dict(French=r['aliases_French'],English=r['aliases_English'])))
    fields=['french_term_or_notation','english_rendering','count','first_place','id','kind','count_scope','source_loci','reviewed_loci','French_aliases','English_aliases','definition_references','paired_index_rows','formula_bounded_pair_count','sources','decision']
    tsv('GLOSSARY_SGA6_FR_EN.tsv',rows,fields)
    put('GLOSSARY_ATTESTATIONS.json',evidence)
    put('LEXICON_DISPOSITIONS.json',dispositions)

    # Compare every admitted headword to every supplied glossary row for that
    # same headword. Original reference spellings and references stay explicit.
    reference=defaultdict(lambda:defaultdict(list))
    for path in sorted((HERE/'input_snapshots/en/glossaries').glob('*.tsv')):
        volume=path.stem.replace('GLOSSARY_','').replace('_FR_EN','')
        for line,r in enumerate(csv.DictReader(path.open(),delimiter='\t'),2):
            vals=list(r.values());f,e=vals[:2]
            notation=(f.startswith('\\') and e.startswith('\\')) or bool(MATH.search(f) and MATH.search(e))
            fn,en=(f,e) if notation else (term_view(f),term_view(e))
            reference[key(fn,en,notation)[0]][volume].append(dict(French=f,English=e,reference=f'en/glossaries/{path.name}#{line}'))
    groups=defaultdict(list)
    for r in rows:groups[key(r['french_term_or_notation'],r['english_rendering'],r['kind'] not in ['lexical_phrase','reviewed_phrase_with_intervening_math'])[0]].append(r)
    cross=[]
    for k,group in sorted(groups.items()):
        if k not in reference:continue
        choices=list(dict.fromkeys(r['english_rendering'] for r in group));vols=reference[k]
        choicekeys={term_view(e).casefold() for e in choices}
        different=any({term_view(v['English']).casefold() for v in entries} != choicekeys for entries in vols.values())
        if not different:continue
        term=group[0]['french_term_or_notation'];d=DECISIONS.get(term.casefold())
        reason=d[2] if d else 'Keep the locally attested SGA6 phrase and grammatical number. The supplied volume rows are preserved as explicit reference renderings; a broader reference phrase or inflection is not automatically appended to a source passage. No source/body change is authorized by a reference-table difference alone.'
        cross.append(dict(french_term_or_notation=term,SGA4_renderings=j(list(dict.fromkeys(v['English'] for v in vols.get('SGA4',[])))),
            SGA4HALF_renderings=j(list(dict.fromkeys(v['English'] for v in vols.get('SGA4HALF',[])))),SGA5_renderings=j(list(dict.fromkeys(v['English'] for v in vols.get('SGA5',[])))),
            SGA7_renderings=j(list(dict.fromkeys(v['English'] for v in vols.get('SGA7',[])))),SGA6_choice=j(choices),reason=reason,
            SGA6_loci='; '.join(dict.fromkeys(r['first_place'] for r in group)),source_ids='; '.join(r['id'] for r in group),reference_sources='; '.join(v['reference'] for entries in vols.values() for v in entries),
            disposition=d[0] if d else 'retain exact attested source wording; reference inventory difference recorded'))
    # GL/Gl is an explicitly proved cross-volume symbol spelling difference.
    gl=next(r for r in macro_evidence if r['token']==r'\GL')
    cross.append(dict(french_term_or_notation='Gl (general linear group)',SGA4_renderings='[]',SGA4HALF_renderings='[]',SGA5_renderings='[]',SGA7_renderings=j(['GL']),
        SGA6_choice=j([r'\operatorname{Gl}']),reason=gl['reason'],SGA6_loci='printed pp.'+', '.join(r['page'] for r in gl['occurrences_by_page']),source_ids=gl['source_id'],
        reference_sources='en/glossaries/GLOSSARY_SGA7_FR_EN.tsv#10; review/english/EN_MACRO_EXPANSION_DECISIONS.json#3',disposition='restore the source lower-case l by the explicit identity on invertible matrices'))
    current_cross_difference_count=len(cross)
    cross.append(dict(french_term_or_notation='générisation',SGA4_renderings=j(['generization']),SGA4HALF_renderings=j(['generization']),SGA5_renderings='[]',SGA7_renderings=j(['generization']),
        SGA6_choice=j(['generization']),reason=DECISIONS['générisation'][2],SGA6_loci='XIII, printed pp.648–649',source_ids='EN-TERM-GENERIZATION-648; EN-TERM-GENERIZATION-649',
        reference_sources='en/glossaries/GLOSSARY_SGA4_FR_EN.tsv#596; en/glossaries/GLOSSARY_SGA4HALF_FR_EN.tsv#440; en/glossaries/GLOSSARY_SGA7_FR_EN.tsv#435',
        disposition='resolved prior cross-volume lexical deviation: the captured input generalization is corrected to generization'))
    cf=['french_term_or_notation','SGA4_renderings','SGA4HALF_renderings','SGA5_renderings','SGA7_renderings','SGA6_choice','reason','SGA6_loci','source_ids','reference_sources','disposition']
    tsv('CROSS_VOLUME_TERMS.tsv',cross,cf)
    (HERE/'CROSS_VOLUME_DECISIONS.tsv').write_bytes((HERE/'CROSS_VOLUME_TERMS.tsv').read_bytes())

    # SGA4's notation records are scoped source changes, not unrestricted
    # rewrite instructions for SGA6. Retain each scope and its disposition.
    notation=json.loads(read('en/glossaries/SGA4_EN_NOTATION_DECISIONS.json'))
    put('REFERENCE_NOTATION_DECISIONS.json',[dict(reference=row,disposition='Retain as a source-scoped SGA4 decision. Its SGA4 source labels/scopes do not identify an SGA6 occurrence to rewrite. SGA6 literal glyph decisions and the separately proved macro transports govern its own occurrences.',SGA6_source_changed=False) for row in notation])

    multiples=[]
    for k,group in sorted(groups.items()):
        english={r['english_rendering'].casefold() for r in group}
        if len(english)>1:
            term=group[0]['french_term_or_notation'];d=DECISIONS.get(term.casefold())
            if not d:
                # Ordinary nested negation is explicitly lexical, with no
                # theorem or mathematical object affected.
                if term.casefold()=="n'est pas":d=('retain local negation syntax','1', 'Is not and the shorter not preserve the same negated predicate. The short word also occurs inside is not, so these lexical counts overlap and do not establish two translations of each source token.')
                else:raise AssertionError(('Unadjudicated admitted multiple rendering',term,english))
            multiples.append(dict(French=term,entries=[dict(id=r['id'],English=r['english_rendering'],count=r['count'],first_place=r['first_place']) for r in group],verdict=d[0],loci=d[1],reason=d[2]))
    put('MULTIPLE_RENDERING_DECISIONS.json',multiples)

    stats=dict(record_type='final_SGA6_terminology_audit',
        scope='Declared source lexicon, all reviewed prefix/contribution term inventory rows, and every printed terminology/notation index row, tested against all720 original leaves of the captured corrected bodies.',
        source_leaf_pairs=len(corpus),prefix_inventory_rows=269,sealed_contribution_inventory_rows=316,manual_final_lexicon_rows=len(json.loads((HERE/'MANUAL_LEXICON.json').read_text())),
        lexicon_pair_candidates=len(dispositions),lexicon_dispositions=dict(Counter(x['status'] for x in dispositions)),
        printed_index_rows=len(index),printed_terminology_index_rows=sum(r['index']=='terminology' for r in index),printed_notation_index_rows=sum(r['index']=='notation' for r in index),
        source_index_ditto_rows=sum(r['repeated_label'] for r in index),glossary_rows=len(rows),glossary_entry_kinds=dict(Counter(r['kind'] for r in rows)),
        distinct_French_headword_keys=len(groups),admitted_multiple_rendering_groups=len(multiples),cross_volume_difference_rows=len(cross),
        cross_volume_retained_difference_rows=current_cross_difference_count,cross_volume_resolved_prior_deviation_rows=1,
        source_scoped_macro_expansion_rows=len(macro_evidence),reference_notation_decisions=len(notation),English_terminology_patches=2,
        source_scoped_literal_notation_rows=len(literal_notation),reviewed_qualified_phrase_entries=len(composite_evidence),
        complete_reference_math_label_input_rows=len(reference_math),
        English_terminology_patch_ids=['EN-TERM-GENERIZATION-648','EN-TERM-GENERIZATION-649'],
        source_and_sealed_files_changed=False,
        count_definition='Each row states its own count scope. Lexical count means English surface-form occurrences on a leaf co-attesting the complete French search phrase; first_place is the first such leaf in print order. Exact index labels instead count paired index rows. Macro/token rows count literal command uses in their declared folios. These quantities are not added as word totals or asserted as one-to-one semantic translation frequencies.',
        search_projection='TeX formatting wrappers and accents are projected in a separate search view; mathematical operands are excluded from prose except simple Greek term prefixes and lexical text labels. Comments, macro definitions and structural labels are excluded. Original author notes, contents, indexes, bibliographic matter and original advertisements are included when present on those leaves. Phrases crossing original leaf boundaries are not joined for lexical counting.',
        completeness='Every input row and every printed index row has a disposition. This is not an assertion that an arbitrary phrase-extraction procedure has found every possible technical term in the volume. A phrase omitted from the glossary is not asserted absent from the book.',
        semantic_evidence='Passage-level reviewed inventories, exact paired index labels, the explicit multi-rendering decisions, and source-linked mathematical identity maps are separated from lexical count evidence. Unpaired page matches and known co-occurrence false positives are excluded.',
        outputs=['GLOSSARY_SGA6_FR_EN.tsv','CROSS_VOLUME_TERMS.tsv','CROSS_VOLUME_DECISIONS.tsv','GLOSSARY_INCONSISTENCIES.md','EN_TERMINOLOGY_PATCHES.jsonl'])
    put('GLOSSARY_AUDIT.json',stats)
    md=['# SGA 6: English terminology and observed alternatives','',
        '## Scope and counts','',
        f'This packet compares the 269 reviewed prefix inventory rows and 316 rows from the ten sealed contribution inventories, the supplied SGA 4, SGA 4½, SGA 5 and SGA 7 lexicons, and 26 additional source-linked lexical entries. It pairs all {len(index)} printed index rows: 129 terminology rows and 105 notation rows. Two ditto rows are explicitly resolved to their preceding headwords, each retaining both definition references.', '',
        f'The deduplicated glossary contains **{len(rows)} rows** for **{len(groups)} French headword keys**. There are **{len(multiples)} admitted French headwords with multiple English renderings** in this inventory and **{len(cross)} cross-volume decision rows** ({current_cross_difference_count} retained differences and one resolved prior deviation). Case and TeX-encoding aliases are listed within an entry; formula-bearing source labels retain their literal notation.', '',
        stats['count_definition'], '',stats['search_projection'], '',stats['completeness'], '',
        'The first mechanically co-attesting leaf is not claimed to be the first semantically aligned translation token. Reviewed passage loci and exact index definition references are separate columns. Formula-bounded interval counts provide an additional check, with their entire bilingual intervals retained in `GLOSSARY_ATTESTATIONS.json`; shared intervals can still contain several words or constructions. The exclusions below prevent those coincidences from becoming unsupported terminology decisions.', '',
        '## English corrections','',
        'Two English-only corrections replace **generalization** by **generization** at XIII 648(a) and 649. The French word is *générisation*. The local point relation is `s ∈ closure{t}`; on a common affine neighbourhood the prime inclusion `p_t ⊆ p_s` gives the localization map `A_{p_s} → A_{p_t}`. SGA 4, 4½ and 7 use **generization** for this relation. Ordinary *généralisation* elsewhere retains **generalization**. The exact patches are `EN-TERM-GENERIZATION-648` and `EN-TERM-GENERIZATION-649`; both English source forms receive them, with identical mathematical units and no French source variant.', '',
        'The English assembly owner has accepted those patches. This packet computes its English lexical counts after applying them virtually to the captured input. `VIRTUAL_PATCH_APPLICATION.json` records the source hashes and exact assertions; this script changes no shared edition source.', '',
        '## Multiple English renderings retained','']
    for item in multiples:
        md += ['### '+item['French'],'','| English rendering | Count | First co-attesting place | Entry |','|---|---:|---|---|']
        for v in item['entries']:md.append('| '+v['English'].replace('|','\\|')+' | '+str(v['count'])+' | '+v['first_place']+' | '+v['id']+' |')
        md += ['',item['verdict']+'. '+item['reason'],'','Source loci: '+item['loci']+'.','']
    md += ['## Source-scoped notation expansions','',
        'These choices are recorded by the English assembly owner in `EN_MACRO_EXPANSION_DECISIONS.json` and `EN_AGGREGATE_MACRO_TRANSPORTS.jsonl`. The glossary cites those records without duplicating their body patches.','',
        '| Source notation | English rendering | Uses in declared scope | Decision |','|---|---|---:|---|']
    for r in macro_evidence:md.append('| `'+r['French_expansion']+'` | `'+r['English_expansion']+'` | '+str(r['count'])+' | '+r['source_id']+' |')
    md += ['', 'The reduction count is20 literal `\\red` invocations. Three literal `\\mathrm{red}` labels on545 and one `\\text{réd}` / `\\text{red}` pair on597 are counted separately in `LITERAL_NOTATION_CHOICES.json`; the earlier metadata figure30 was an arithmetic error corrected by the English assembly owner. Both metadata snapshots and the clarification are retained.', '']
    md += ['', 'Each exact identity proof and all counted folios are in `NOTATION_EXPANSION_CHOICES.json`. In particular, the naïf/naive identity sends every class [E] to [E] in each stated exact category and preserves every short-exact-sequence relation; the Gl/GL comparison fixes every invertible matrix. The red/réd identity fixes A/√0, and long/length fixes the same module and its composition-series quotients.', '',
        'The seven SGA 4 notation records retain their original volume scopes in `REFERENCE_NOTATION_DECISIONS.json`. Their labels do not identify an SGA 6 occurrence to rewrite. The local SGA 6 source glyph decisions are preserved.', '',
        '## Rejected candidate inferences and inventory qualifications','',
        'The full input-pair disposition is in `LEXICON_DISPOSITIONS.json`. Examples checked in their bilingual intervals include:','',
        '- **entier → integral:** on339 the integer n and an integral-domain assertion are separate French phrases.',
        '- **homomorphisme → map:** on457,531,547 map translates application, while homomorphism is separately retained.',
        '- **immersion → embedding:** on251 the two English words belong to separate source clauses.',
        '- **flèche → morphism:** on360 the vertical arrow and the resulting morphism are separately named.',
        '- **recouvrement → cover:** on169 cover translates the verb recouvrent; the noun recouvrement is covering.',
        '- Singular/plural page coincidences such as faisceau/sheaves, fibre/fibres and trace/traces are excluded when the local plural translates a separate French plural. Genuine collective plurals, including stable under kernels/cokernels and homomorphism of functors, have explicit local decisions.',
        '- Punctuation, Roman reference numerals and single-letter prose matches are not promoted to mathematical notation. Exact named TeX tokens, complete printed notation-index labels and the separately checked macro expansions have their own count scopes.', '',
        'A number of provisional contribution headwords were lemma forms, condensed labels or phrases interrupted by a source qualifier. Their zero literal attestations are retained in the audit rather than assigned invented counts. Exact source plurals or fuller labels were added where inspected, including résolutions injectives, tores déployés, épimorphismes effectifs and complexe de Modules parfait. The candidate classe fondamentale at674 has no such literal source/English phrase there; the separately attested classe d’homologie fondamentale / fundamental homology class is indexed at15.', '',
        '## Cross-volume choices','',
        '`CROSS_VOLUME_TERMS.tsv` lists every admitted headword whose rendering set differs from at least one supplied glossary for that exact headword, the source-scoped Gl/GL notation choice, and the resolved prior generalization/generization deviation. Every volume’s original rendering and row reference are retained. `CROSS_VOLUME_DECISIONS.tsv` is an identical audit alias. Grammatical inflection, ordinary synonyms and spelling alternatives are preserved when the local object, diagram or formula is unchanged, with the explicit maps given above. The two source-proved generization slips are corrected.', '',
        '## Reproducibility','',
        'Run `make_terminology_patches.py`, `lexical_inventory.py`, `index_inventory.py`, and `finalize_glossary.py` in this directory after verifying the captured manifests. `prepare_inputs.py` creates the initial immutable input copy and refuses to overwrite it with changed shared inputs. All outputs are local to this review packet; shared edition sources, sealed contributions and their manifests remain unchanged.','']
    (HERE/'GLOSSARY_INCONSISTENCIES.md').write_text('\n'.join(md))
    print(json.dumps({k:stats[k] for k in ['glossary_rows','distinct_French_headword_keys','admitted_multiple_rendering_groups','cross_volume_difference_rows','printed_index_rows','English_terminology_patches']}))

if __name__=='__main__':main()
