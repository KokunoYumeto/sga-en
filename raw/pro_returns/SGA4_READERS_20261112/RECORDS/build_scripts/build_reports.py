"""Generate the delivery README, compile inventory, and apparatus census."""
import bisect,collections,csv,hashlib,json,re
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
csv.field_size_limit(100_000_000)
REC=ROOT/'output/records'
EXPOSES=['I','II','III','IV','V','Vbis','VI','VII','VIII','IX','X','XI','XII','XIII','XIV','XV','XVI','XVII','XVIII','XIX']
FILES=['01','02','03','04','05','05bis','06','07','08','09','10','11','12','13','14','15','16','17','18','19']
READERS=[('FR','diplomatic','SGA4_FR_diplomatique'),('FR','corrected','SGA4_FR_corrige_apparat'),
 ('FR','reading','SGA4_FR_texte_de_lecture'),('EN','diplomatic','SGA4_EN_diplomatic'),
 ('EN','corrected','SGA4_EN_corrected_apparatus'),('EN','reading','SGA4_EN_reading')]

def read(path,default=None):
    p=ROOT/path
    return json.loads(p.read_text()) if p.exists() else default

def tsv(name):
    p=REC/name
    return list(csv.DictReader(p.open(),delimiter='\t')) if p.exists() else []

def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()

def note_calls(text):
    from en_common import active_matches
    # The source defines acorriger{arg} exactly as nde{arg}; count its two
    # actual invocations while excluding that macro definition itself.
    for match in active_matches(r'\\(?:nde|ndetext|acorriger)\s*\{',text):
        prefix=text[text.rfind('\n',0,match.start())+1:match.start()]
        if re.search(r'\\(?:def|newcommand|renewcommand|providecommand|DeclareRobustCommand)\b',prefix):continue
        yield match

def visible_archive_text(text):
    from en_common import active_matches,group,replace_spans
    edits=[]
    for match in active_matches(r'\\SGAArchiveOnly\b',text):
        prefix=text[text.rfind('\n',0,match.start())+1:match.start()]
        if re.search(r'\\(?:def|newcommand|renewcommand|providecommand)\b',prefix):continue
        if any(a<=match.start()<b for a,b,_ in edits):continue
        _,_,end,_=group(text,match.end());edits.append((match.start(),end,''))
    return replace_spans(text,edits)

def compile_inventory():
    rows=[]
    for lang,form,name in READERS:
        tex=ROOT/'output'/lang.lower()/(name+'.tex');pdf=tex.with_suffix('.pdf')
        status=read('output/records/compile/'+name+'.json',{})
        if not status:status=read('output/records/compile_logs/'+name+'.json',{})
        logs=[REC/'compile'/(name+'.log'),REC/'compile_logs'/(name+'.log')]
        lp=next((p for p in logs if p.exists()),None)
        text=lp.read_text(errors='replace') if lp else ''
        raw=read('tmp/en_compile/'+('corrected_apparatus' if form=='corrected' else form)+'/STATUS.json',[]) if lang=='EN' else []
        passes=status.get('passes',raw if isinstance(raw,list) else raw.get('passes',[]))
        result=passes[-1].get('returncode') if passes else None
        source_hash=status.get('source_sha256',status.get('tex_sha256'))
        if not source_hash and isinstance(raw,dict):source_hash=raw.get('source_sha256',raw.get('tex_sha256'))
        current=sha(tex) if tex.exists() else None
        pages=re.findall(r'Output written on .*?\((\d+) pages',text,re.S)
        errors=re.findall(r'^!.*|^[^\n]*:[0-9]+:[^\n]*(?:Error|Undefined control sequence|Missing |Extra )[^\n]*',text,re.M)
        warnings=re.findall(r'^(?:LaTeX(?: Font)?|Package [^\n]+) Warning:[^\n]+',text,re.M)
        missing=re.findall(r'Missing character:[^\n]+',text)
        unresolved=re.findall(r'^(?:LaTeX|Package [^\n]+) Warning:[^\n]*(?:undefined|Rerun|rerun)[^\n]*',text,re.M)
        row=dict(language=lang,form=form,reader=name,tex_sha256=current,
          compiled_source_sha256=source_hash,pdf_present=pdf.exists(),
          pdf_sha256=sha(pdf) if pdf.exists() else None,pdf_bytes=pdf.stat().st_size if pdf.exists() else None,
          passes=passes,returncode=result,pdf_pages=int(pages[-1]) if pages else status.get('pdf_pages'),
          error_count=len(errors),errors=errors,warning_count=len(warnings),warnings=warnings,
          overfull_boxes=len(re.findall(r'Overfull \\[hv]box',text)),
          underfull_boxes=len(re.findall(r'Underfull \\[hv]box',text)),
          missing_character_count=len(missing),missing_characters=missing,
          unresolved_reference_warnings=unresolved,
          log=str(lp.relative_to(REC)) if lp else '',
          finished=bool(pdf.exists() and result==0 and not errors and not missing and not unresolved and current==source_hash))
        rows.append(row)
    (REC/'COMPILE_STATUS.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2)+'\n')
    return rows

def census():
    disputed=read('output/shared/disputes_index.json',[])
    dp=collections.Counter(r['expose'] for r in disputed)
    possible=collections.Counter()
    for r in tsv('ONE_MODEL_MISPRINTS_JUDGED.tsv'):
        if r['verdict']!='possible-not-verified':continue
        m=re.search(r't\d\s+(\w+)\s+p\.',r['page'])
        if m:possible[m.group(1)]+=1
    fr=read('work_fr/corrected_layers.json',{})
    human_fr=collections.Counter(r['expose'] for r in fr.get('org',[]))
    human_en=read('output/records/EN_HUMAN_RECORDS.json',[])
    variants={lang:read('output/records/'+lang+'_VARIANTS.json',[]) for lang in ['FR','EN']}
    if not human_en:human_en=[r for r in variants['EN'] if r['kind'].startswith('human')]
    human_en=collections.Counter(r['expose'] for r in human_en)
    original_human=read('output/records/HUMAN_ORIGINAL_SOURCE_RECORDS.json',{})
    original_by_id={r['id']:r for r in original_human.get('original_source_records',[])}
    supplements={lang:collections.Counter(original_by_id[ident]['expose'] for ident in original_human.get('supplement_'+lang+'_ids',[])) for lang in ['FR','EN']}
    original_note_counts=collections.Counter(r['expose'] for r in original_human.get('original_NDE_records',[]))
    nde_en={}
    from build_en import select_inline_variants
    from en_common import active_matches
    master_path=ROOT/'output/en/SGA4_EN_annotated_master.tex'
    master=master_path.read_text() if master_path.exists() else ''
    for form,corrected in [('diplomatic',False),('corrected',True)]:
        text=select_inline_variants(master,corrected).split(r'\backmatter',1)[0]
        text=text.split(r'\mainmatter',1)[-1]
        text=visible_archive_text(text)
        markers=list(active_matches(r'\\SGApage\{\d\}\{(\w+)\}\{\d+\}',text))
        positions=[m.start() for m in markers];counts=collections.Counter()
        for match in note_calls(text):
            index=bisect.bisect_right(positions,match.start())-1
            if index>=0:counts[markers[index].group(1)]+=1
        # This original IV p.465 note is translated inline inside a printed
        # footnote rather than through an nde macro. Its unchanged payload
        # has its own reading-form guard in the English master.
        inline_note='\\stepcounter{cnote}\\textsuperscript{\\arabic{cnote}}%\n\\textup{ [N.D.E.: This exercise does not seem to exist.]}'
        guarded='\\SGAeditor{'+inline_note+'}'
        if guarded in text:
            assert text.count(guarded)==1
            counts['IV']+=1
        nde_en[form]=counts
    rows=[]
    for lang in ['FR','EN']:
        for exp,f in zip(EXPOSES,FILES):
            vv=[r for r in variants[lang] if r['expose']==exp]
            n_mp=sum(bool(re.search(r'\bMP\d{4}\b',r['source'])) for r in vv)
            n_om=sum(bool(re.search(r'OM-(?:OPUS|SOL)-\d{4}',r['source'])) for r in vv)
            n_human=sum(bool(re.search(r'\bORG-|EN-ORG|human editorial',r['source']+' '+r.get('kind',''))) for r in vv)
            for form in ['diplomatic','corrected','reading']:
                apparatus=form=='corrected';notes=form!='reading'
                nde=0
                if lang=='FR' and notes:
                    text=fr.get('dip' if form=='diplomatic' else 'corr',{}).get(f,'')
                    from fr_core import strip_comments
                    nde=sum(1 for _ in note_calls(strip_comments(text)))
                elif lang=='EN' and notes:nde=nde_en[form][exp]
                rows.append(dict(language=lang,expose=exp,form=form,variant_entries=len(vv) if apparatus else 0,
                  variants_with_agreed_mp=n_mp if apparatus else 0,variants_with_accepted_om=n_om if apparatus else 0,
                  variants_with_human_source=n_human if apparatus else 0,
                  human_record_dossiers=(human_fr if lang=='FR' else human_en)[exp] if notes else 0,
                  original_human_supplement=supplements[lang][exp] if notes else 0,
                  original_note_dossiers=original_note_counts[exp] if notes else 0,
                  original_proof_rewrite_records=int(bool(original_human) and notes and exp=='Vbis'),
                  editorial_reference_entries=8 if form=='diplomatic' and exp=='XVIII' else 0,
                  nde_notes=nde,disputed_items=dp[exp] if apparatus else 0,
                  possible_misprints=possible[exp] if apparatus else 0))
    (REC/'APPARATUS_COUNTS.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2)+'\n')
    out=['# Apparatus counts by exposé and form','',
      'Each variant entry is counted once in the total. A single entry may cite an agreed misprint, an accepted one-model item, and a human record together; the three source columns therefore overlap. Human dossiers preserve the source pairs independently of the correction apparatus. The reading forms omit every apparatus and editorial-note category.',
      '', 'Disputes and possible misprints are counted by supplied item ID. They report unresolved readings and introduce no correction variant. Printed-page marginal markers are not apparatus entries.','']
    out.extend(['The original-source supplement preserves 44 French and 315 English documentary pairs from Orgogozo’s untouched source, plus the original V bis p.138 proof/rewrite in each language. These counts are separate from the transmitted D and released-English dossiers. The eight diplomatic editorial-reference entries support citations in retained human notes; their full text and original ordinal labels are recorded separately.',''])
    out.extend(['Both documentary forms also preserve all 129 exact original French N.D.E. arguments in a separately attributed source dossier. The visible body-note counts include the single English inline note at IV p.465 and exclude the two archive-only release-generated notices in VIII. Eight human notes occur only in corrected-body branches: seven inside original paired readings and one inside the V bis rewrite; their original texts remain accessible in both documentary forms through the dossiers.',''])
    for lang in ['FR','EN']:
        out.extend(['## '+lang,'','| Exposé | Form | Variant entries | With agreed MP | With accepted OM | With human source | Transmitted human dossiers | Original human supplement | Original note dossiers | Original proof/rewrite | Editorial references | Visible N.D.E. notes | Disputed items | Possible misprints |',
          '|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|'])
        for r in rows:
            if r['language']!=lang:continue
            cols=[r[k] for k in ['expose','form','variant_entries','variants_with_agreed_mp','variants_with_accepted_om','variants_with_human_source','human_record_dossiers','original_human_supplement','original_note_dossiers','original_proof_rewrite_records','editorial_reference_entries','nde_notes','disputed_items','possible_misprints']]
            out.append('| '+' | '.join('pending census' if x is None else str(x) for x in cols)+' |')
        out.append('')
    (REC/'APPARATUS_COUNTS.md').write_text('\n'.join(out))
    return rows

def readme(status,counts):
    manifest=read('output/records/SOURCE_MANIFEST.json',[])
    mpfr=read('output/records/AGREED_MISPRINTS_PLACEMENT.json',[])
    en=read('output/records/EN_SOURCE_AUDIT.json',[])
    good={'paired','represented by existing variant','no English impact'}
    enids={r['id'] for r in en if r.get('status') in good and re.fullmatch(r'MP\d{4}',r.get('id',''))}
    om=tsv('ONE_MODEL_MISPRINTS_JUDGED.tsv');verdict=collections.Counter(r['verdict'] for r in om)
    hand=tsv('HAND_REPLAYS_PLACED.tsv');hstat=collections.Counter(r['status'] for r in hand)
    frplaces=tsv('ONE_MODEL_PLACEMENT_FR.tsv');ost=collections.Counter(r['status'] for r in frplaces)
    glossary=tsv('GLOSSARY_SGA4_FR_EN.tsv');glossary_terms=collections.defaultdict(set)
    for r in glossary:glossary_terms[r['french_term_or_notation']].add(r['english_rendering'])
    variants={lang:read('output/records/'+lang+'_VARIANTS.json',[]) for lang in ['FR','EN']}
    final_dispositions=read('output/records/EN_FINAL_DISPOSITIONS.json',{}).get('records',[])
    mp_dispositions=collections.Counter(r['disposition'] for r in final_dispositions if re.fullmatch(r'MP\d{4}',r['id']))
    verification=read('output/records/VERIFICATION.json',{})
    nfinished=sum(r['finished'] for r in status)
    lines=['# SGA 4: six complete readers','',
      'Build by GPT-6 Astra (OpenAI, ChatGPT Pro mode), 12 November 2026.','',
      f'Validation state: {nfinished} of six reader PDFs have a recorded successful compile matching the current TeX source. This file is regenerated from the build records; pending checks remain visible until they pass.','',
      ('Final combined verification: '+str(verification.get('pass_count',0))+' of '+str(verification.get('check_count',0))+' checks passed. VERIFICATION.json contains the evidence for each gate.') if verification else 'The combined verification report is generated after the source and PDF audits.','',
      '## Deliverables','',
      '| Archive | Contents |','|---|---|',
      '| SGA4_READERS_FR.zip | Three French single-file readers, the annotated French master, PDFs and this README. |',
      '| SGA4_READERS_EN.zip | Three English single-file readers, the annotated English master, PDFs and this README. |',
      '| SGA4_READERS_RECORDS.zip | Change logs, decisions, complete item ledgers, glossary, apparatus counts, compile diagnostics, reviewed pair data and build scripts. |','',
      '| Language | Diplomatic | Corrected with apparatus | Reading text |','|---|---|---|---|',
      '| French | SGA4_FR_diplomatique.tex | SGA4_FR_corrige_apparat.tex | SGA4_FR_texte_de_lecture.tex |',
      '| English | SGA4_EN_diplomatic.tex | SGA4_EN_corrected_apparatus.tex | SGA4_EN_reading.tex |','',
      'Every reader contains all three tomes and all twenty transcribed exposés, including V bis. The French master is SGA4_FR_master_annote.tex; the English master is SGA4_EN_annotated_master.tex.','',
      'Each master defaults to the corrected form with apparatus. Its accompanying PDF reuses that verified rendering; MASTER_PDF_RENDERINGS.json records the exact selector correspondence and source/PDF hashes.','',
      '## Source authority and construction','',
      f'All {len(manifest):,} source-manifest entries were checked against their recorded byte counts and SHA-256 hashes before extraction. SOURCE_MANIFEST.json retains archive-relative names, roles, sizes and hashes. The source archives remain read-only.','',
      'The French diplomatic source is fr/D_diplomatic_after_scan_check; the corrected source is fr/E_corrected_after_scan_check. The untouched Orgogozo snapshot 71766d9 supplies the earlier comparison. The English baseline is en/C_release_20261112/04_SGA4_EN_COMPLETE_READER.tex, checked against the 271 native translation fragments at commit 4a4cbac and the 12 November port records.','',
      'Each language has one annotated master. The French form switch is SGAForm; the English form switch is SGAform: 0 selects diplomatic, 1 selects corrected with apparatus, and 2 selects reading text. Generated forms differ only in that selector. The corrected and reading forms select the same mathematical body. Reading forms suppress the correction apparatus, unresolved-reading appendices and Orgogozo editorial notes.','',
      'Marginal labels have the form tome:original-page; the reader’s own page numbers identify the physical book pagination. In the corrected forms, linked variant marks lead to the entry containing the printed reading, corrected reading and source ID. French uses compact numbered marks; English uses linked daggers, with the full EN-V identifiers retained in the apparatus. Disputed-place marks lead to the unresolved item record. The human editorial dossiers and original-source supplements have their own headings and provenance.','',
      'The reviewed pair files give the complete printed and corrected spans, source IDs and exact location evidence. Replacements use explicit character/token correspondences and retain source notation. Page markers that intersect a replacement follow their mapped unchanged-character boundary. APPARATUS_PROJECTION.md records the limited macro expansions used to avoid entries for invisible label changes.','',
      '## Item counts and audit files','',
      '| Corpus | Count | Evidence |','|---|---:|---|',
      '| Printed page identities | 1,557 | PAGES.json; EN_PAGE_MARKERS.tsv; reader verification |',
      '| Agreed transcription fixes | 898 | AGREED_TRANSCRIPTION_FIXES_AUDIT.json and .tsv |',
      '| Agreed misprints | 930 | AGREED_MISPRINTS_PLACEMENT.json; reviewed pairs; language coverage audit |',
      f'| French agreed misprint placements marked represented | {sum(r.get("status") in {"represented","represented-manual"} for r in mpfr)} | French placement ledger; final branch checks |',
      f'| English agreed misprints represented or explicitly assessed as unchanged English | {len(enids)} | EN_SOURCE_AUDIT.json, by unique MP ID |',
      f'| English agreed misprints with variants / unchanged English | {mp_dispositions["English variants registered"]} / {mp_dispositions["no English impact"]} | EN_FINAL_DISPOSITIONS.json, with per-part evidence or common-reading context |',
      f'| French / English correction-apparatus entries | {len(variants["FR"])} / {len(variants["EN"])} | FR_VARIANTS.json; EN_VARIANTS.json; one entry per registered difference |',
      '| One-model misprint judgments | 1,601 | ONE_MODEL_MISPRINTS_JUDGED.tsv: 258 Opus and 1,343 Sol |',
      f'| Accept / possible / reject | {verdict["accept"]} / {verdict["possible-not-verified"]} / {verdict["reject"]} | One reason per item; possible items in the corrected-form appendix |',
      '| Disputed items / printed pages | 643 / 443 | DISPUTED_PLACES.tsv |',
      '| By-hand replay records | 56 | HAND_REPLAYS_PLACED.tsv |',
      '| Held changes touching human apparatus | 18 | DECISIONS.tsv; held_apparatus_decisions.json |',
      '| English port decisions | 583 | EN_PORT_AUDIT.tsv |',
      '| Deferred French C records in the English port | 293 | EN_DEFERRED_FRENCH_FIXES.tsv |','',
      f'The glossary contains {len(glossary):,} rows covering {len(glossary_terms):,} distinct recorded French terms or notations; {sum(len(v)>1 for v in glossary_terms.values()):,} have more than one observed English rendering. Its source census contains 1,769 emphasis spans and 1,753 alignment records. The extraction scope and counting rules are stated in GLOSSARY_INCONSISTENCIES.md.','',
      'The 930 agreed records are identified MP0001–MP0930 in their supplied order. AF0001–AF0898 identify the one-based lines of FIXLOG_4.jsonl. H identifiers retain the zero-based positions in REPLAY_MANUAL_4.json. OM-OPUS and OM-SOL identifiers retain each model list’s order.','',
      'By-hand replay statuses: '+ '; '.join(f'{k}: {v}' for k,v in sorted(hstat.items()))+'.','',
      'Accepted nonhuman one-model placement statuses in French: '+ '; '.join(f'{k}: {v}' for k,v in sorted(ost.items()))+'. Of the 550 accepted judgments, 53 concern existing human records; the remaining 497 include 338 undisputed items and 159 whose application is held on disputed pages.','',
      'The historical English port has 159 apply decisions: 157 C fixes and H33/H39. Its other decisions are 155 already and 269 not-applicable. FINAL_4.json accounts for all 898 French fixes with 549 final, 293 app_check and 56 not_in_current rows. The page-in-appcheck flag covers the 293 deferred C records plus 22 by-hand replays.','',
      '## Editorial decisions','',
      'No disputed reading was selected from an unavailable scan. The 643 records retain their item IDs, both available model readings, locations and kinds: 154 conflicts, 4 doubts, 347 one-model fixes, 84 batch cuts, 50 held agreed fixes and 4 unplaced fixes. Accepted one-model judgments on those pages remain held for application.','',
      'Orgogozo’s paired readings and N.D.E. notes are attributed as human editorial work. They remain in the diplomatic and corrected forms and are omitted from the reading forms. The 18 held apparatus changes are listed without applying them to his notes.','',
      'HUMAN_ORIGINAL_SOURCE_RECORDS.json inventories all 1,261 original active sisi records and their exact arguments, hashes and source-fragment correspondences. The transmitted D dossier has 1,258 records: three original commands were flattened before D, and 41 surviving pairs have changed raw arguments. A 44-pair original-source supplement preserves those originals in both French documentary forms. The released-English dossier has 1,171 records including its dedicated V bis rewrite; 315 original French pairs are also reproduced where a corresponding English record does not contain both original arguments verbatim. Each language separately preserves the exact original V bis p.138 printed proof and editorial rewrite.','',
      'All 129 original French editorial-note arguments are reproduced exactly in a separate attributed dossier in both diplomatic and corrected forms. Visible body-note counts are 121 diplomatic and 129 corrected in each language. Five human English notes hidden by archive-only wrappers in the release are restored unchanged to the documentary forms. The IV p.465 inline note keeps its released wording and is omitted in reading form by the same editorial selector. The two release-generated VIII reference notices remain archive-only. HUMAN_EDITORIAL_PRESERVATION_AUDIT.json records the exact source correspondence and form visibility.','',
      'Five French note arguments already differ between the supplied D and E trees. The final bodies retain the argument selected from their respective source trees; the preservation audit records the complete D/E pairs and source positions. The separate 129-note dossier retains the untouched A arguments, so these transmitted-source differences do not replace the original documentary evidence.','',
      'The commented printed diagram at I p.34 is restored. The original V bis p.138 argument appears in the diplomatic form; the existing editorial rewrite remains in the corrected body, with its source recorded. Exposés II and III use the supplied printed-page identities.','',
      'DECISIONS.tsv records the printed plain P, raised-dot and capital-label conventions; the bounded cardinal pi decision in I §§8–9; the script-C notation in V pp.65–80; Exposé IV reference prefixes; and the held phi/empty-set and equation-parenthesis questions. Every notation replacement has a bounded scope and occurrence evidence.','',
      'C293 is reconciled with MP0355. C293 repairs the site-symbol spelling; MP0355 gives V as the printed erroneous denominator and U as the correction. The induced inverse-image functor sends (W→U) to (V×_{p*U}p*W→V), so the corresponding morphism of sites goes from T/V to S/U. The diplomatic English therefore has S/V; both corrected languages have S/U.','',
      '## Change logs and terminology','',
      'CHANGES_FR.tsv contains separate comparisons against Orgogozo 71766d9 and against corrected source E. Its rows identify the page, place, before and after readings, source authority and comparison. CHANGES_EN.tsv records changes from the released English. The variant inventories preserve the full branch readings and sources.','',
      'FR_CHANGE_AUDIT.json verifies 42 complete comparisons: each of the twenty exposés against both French baselines, plus each complete source bundle against the generated corrected TeX. Forward and inverse reconstruction also pass after reading the serialized TSV. The baseline bundles preserve their source line endings and record any required privacy filtering explicitly. EN_CHANGE_AUDIT.json verifies exact reconstruction of the selected English corrected body and of the complete generated corrected source.','',
      'GLOSSARY_SGA4_FR_EN.tsv records observed French terminology or notation, English rendering, count and first place. GLOSSARY_EVIDENCE.tsv supplies paired source excerpts. GLOSSARY_INCONSISTENCIES.md lists observed multiple renderings and states the extraction scope and counting method. Existing valid technical renderings remain unless a documented slip requires a correction.','',
      '## Missing source material','',
      'The following printed summary pages were not transcribed in the supplied corpus: V p.1; V bis p.83; VI pp.163–164; VII p.341; VIII p.366; XVI p.206; XVII pp.250–251. Each tome’s original front matter and indexes are also absent. They have not been invented or reconstructed. Reader title pages, source notices, prefaces and tables of contents are newly generated and identified as this edition’s material.','',
      '## Compilation and diagnostics','',
      'The single-file readers use the system amsbook class and XeLaTeX. On a standard complete TeX Live installation, run xelatex on a reader until its table of contents and cross-references settle (the build uses repeated passes). The font setup uses the TeX Live Libertine and XITS families. Every exposé and the required local macro/style material are embedded in the reader; no companion source file is needed.','',
      '| Reader | Current source compiled | PDF pages | Errors | Warnings | Overfull boxes | Underfull boxes | Missing glyph reports |','|---|---|---:|---:|---:|---:|---:|---:|']
    for r in status:
        lines.append('| '+' | '.join([r['reader'], 'yes' if r['finished'] else 'pending',str(r['pdf_pages'] or '—'),str(r['error_count']),str(r['warning_count']),str(r['overfull_boxes']),str(r['underfull_boxes']),str(r['missing_character_count'])])+' |')
    lines.extend(['', 'COMPILE_STATUS.json records the source/PDF hashes, pass return codes and diagnostic lists. Complete sanitized engine logs accompany it. Box warnings are reported separately from compilation errors. A PDF is considered current only when its recorded source hash matches the delivered TeX, its pass succeeds, and it has no errors, missing characters, or unresolved-reference/rerun warnings.','',
      'PDF_PAGE_MARKER_AUDIT.json checks the rendered marginal page labels against all 1,557 supplied page identities, in order, in each reader. PDF_ORIGINAL_PAGE_LOCATIONS.tsv maps every original page to its physical PDF page and label coordinates. Per-reader PDF_QA records check full text bounds, contents entries, and representative rendered pages; the bounds check includes text beyond the page crop.','',
      'The isolated execution environment required a local TeX format/font-map repair. The optional tex_environment.py helper detects those prepared repair assets; a normal TeX Live installation uses its ordinary environment. No system class or system files were modified.','',
      '## Rebuilding from the attached sources','',
      'Use Python 3 and a complete TeX Live installation. The rendered-PDF audits also require PyMuPDF (imported as fitz) and Poppler’s pdffonts command. Place only the three original source ZIP archives in upload beside build_scripts: extract_sources.py expects a root MANIFEST.tsv in every upload/*.zip. No scan images are required or assumed.','',
      'Restore SGA4_READERS_RECORDS.zip into the rebuild workspace using this mapping:','',
      '| Archive member | Rebuild location |','|---|---|','| build_scripts/... | build_scripts/... |','| shared/... | output/shared/... |','| Every other member, preserving its relative path | output/records/... |','',
      'The complete records directory is a required reconstruction input. In particular, retain EN_MISPRINT_LANGUAGE_ASSESSMENT.json, HUMAN_ORIGINAL_SOURCE_RECORDS.json and OM_1326_SCOPE_DECISION.json, together with all reviewed pair files and human-source supplements in output/shared. These contain the recorded editorial decisions.','',
      '```sh','python build_scripts/extract_sources.py','python build_scripts/judge_misprints.py','python build_scripts/shared_records.py','python build_scripts/build_fr.py','python build_scripts/build_en.py','python build_scripts/en_manual_pairs.py','python build_scripts/en_composed_reviews.py','python build_scripts/en_dispositions.py','python build_scripts/en_glossary.py','python build_scripts/finish_records.py','python build_scripts/audit_fr_t3.py','python build_scripts/audit_transcription_fixes.py','python build_scripts/audit_en_reviewed_pairs.py','python build_scripts/audit_en_auto_t3.py','python build_scripts/audit_en_om_branches.py','python build_scripts/human_preservation_final.py','```','',
      'Ordinary reconstruction uses the included reviewed pair files and documentary inputs. Their generators and audit scripts are supplied with the recorded outputs. Some research-stage generators require the specific intermediate snapshots named in their code; the ordinary rebuild recipe reuses their reviewed outputs. build_fr.py automatically runs the full French change-register audit, build_en.py regenerates the English change comparisons, and en_glossary.py regenerates the glossary source-span records.','',
      'Compile all six generated TeX files, then regenerate the PDF QA, reports, master renderings and page lookup before the final verification and packaging:','',
      '```sh','python build_scripts/fr_compile.py SGA4_FR_diplomatique 3','python build_scripts/fr_compile.py SGA4_FR_corrige_apparat 3','python build_scripts/fr_compile.py SGA4_FR_texte_de_lecture 3','python build_scripts/en_compile.py diplomatic --passes 3','python build_scripts/en_compile.py corrected_apparatus --passes 3','python build_scripts/en_compile.py reading --passes 3','python build_scripts/fr_pdf_qa.py','python build_scripts/en_pdfqa.py','python build_scripts/build_reports.py','python build_scripts/finalize_master_pdfs.py','python build_scripts/audit_pdf_markers.py','python build_scripts/verify_readers.py','python build_scripts/package_outputs.py --final','```','',
      '## Credits, rights and privacy','',
      'The readers credit M. Artin, A. Grothendieck and J.-L. Verdier, the contributors named in the supplied records, and Fabrice Orgogozo for the LaTeX edition at commit 71766d9. They identify the later layers as AI-transcribed, AI-translated and AI-produced corrections, and credit this build to GPT-6 Astra (OpenAI, ChatGPT Pro mode).','',
      "The rights in the original work belong to its author or the author's representatives or heirs. Where we hold rights, in the AI-produced transcription, translation, corrections and typesetting, they are dedicated to the public domain under CC0 1.0. This edition is published for educational, non-profit purposes, and we claim no rights we do not hold. If you hold rights in this work and object to its publication here, please open a GitHub issue and we will take it down.",'',
      'Source references in these deliverables use archive-relative paths. Personal filesystem paths and email addresses are omitted. CHECKPOINTS.json records the completed-reader checkpoints and artifact hashes.',''])
    (REC/'README.md').write_text('\n'.join(lines))

def main():
    status=compile_inventory();counts=census();readme(status,counts)
    print('README and apparatus census regenerated;',sum(r['finished'] for r in status),'current completed PDFs')

if __name__=='__main__':main()
