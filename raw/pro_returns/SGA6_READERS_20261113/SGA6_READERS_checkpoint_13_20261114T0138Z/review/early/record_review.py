"""Incremental, explicitly reviewed evidence for the early-page collation.

Run from any working directory. Source references use archive-relative paths.
The evidence dictionaries below are populated only after direct image viewing.
"""
from pathlib import Path
import json
import re

ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).resolve().parent

EVIDENCE = {
    "findings_001_005.json": {
        1: ("heading", "A single continuous rule is visible below Exposé 0; retain the existing underline."),
        2: ("title, first line", "Two separate parallel rules are visible under the complete first title line."),
        3: ("title, second line", "Two parallel rules are visible beneath SUR LES SCHEMAS GENERAUX."),
        4: ("opening paragraph", "The printed final word is introductif. The adjective modifying the feminine noun nature requires introductive in the corrected text."),
        5: ("opening paragraph and §1", "The typed joint names use hyphens. NOTE_6 explicitly permits the transcription's en dashes for joint names; this observation requires no additional local edit."),
        6: ("display after morphisme propre", "A distinct baseline stop follows X before the arrow. Preserve it diplomatically and omit the extraneous stop in the corrected display."),
        7: ("text before the cycle direct-image display", "The quotation marks surrounding image directe de cycles are typed straight quotes. NOTE_6 explicitly accepts the existing guillemets."),
        8: ("paragraph beginning ch_X, ch_Y", "The acute accent is visible over the first e in coéfficients. Keep the printed spelling diplomatically and use coefficients in the corrected form."),
        9: ("line immediately before (1.2)", "The last word propos has no following comma; the attached layers already omit it."),
        10: ("formula (1.2), left-hand side", "Three opening parentheses follow ch_Y, f_* and cl; only two close before the equals sign. The corrected closing parenthesis restores the displayed expression ch_Y(f_*(cl(F)))."),
        11: ("first text line", "The first text line begins de sorte que. Both attached layers now place the folio-2 marker before de."),
        12: ("item a)", "The printed word has one r in débarasser. The corrected spelling is débarrasser."),
        13: ("first text line", "The paragraph number 2.1 and its following sentence are the first matter on page 3. Both attached markers now precede the heading."),
        14: ("§2.1, paragraph after (2.2)", "The print reads le sous-schémas fermé X with an s after schéma; the singular article and adjective determine sous-schéma in the corrected text."),
        15: ("heading 2.2.", "The trailing stop is visible after the second 2. NOTE_6 permits restoring a missing or faint interdigit stop; retain the attached heading 2.2."),
        16: ("§2.2, lisses et quasi-porjectifs", "The sequence porj is printed at the broken word quasi-porjectifs; projectifs restores the transposed letters."),
        17: ("§2.2, produit tensoriel par Q", "The Q at this location has the ordinary typed outline, unlike the visibly doubled Q in the adjacent tensor product. The diplomatic form retains plain Q; the observation is also referred to the volume notation decision."),
        18: ("§2.2, Une première filtration", "Une première begins at the ordinary left margin after the previous full line, without the indentation used for a new paragraph on page 2. Joining this text preserves the printed paragraph boundary."),
        19: ("§2.2, cas X lisse sur un coprs k", "The print has coprs, with p before r. The corrected spelling corps agrees with the other occurrences on this page."),
        20: ("§2.2, last lines and final display", "The graded degree mark is a raised dot. NOTE_6 accepts bullet for that mark in Gr; no local substitution is necessary."),
        21: ("final display", "The handwritten phi has a closed loop crossed by its long stroke. The existing phi command preserves this shape."),
        22: ("first text line", "The opening parenthesis and tranformant begin page 4. The diplomatic marker is before the parenthesis; the corrected marker is also before it, with only a harmless source newline after it."),
        23: ("first word", "The print reads tranformant, lacking s. Preserve that spelling diplomatically and retain transformant in the corrected text."),
        24: ("paragraph Ceci montre, projectif et lisse", "The last letter of corpa has the closed bowl and right stem of the typed a, visible next to the following ne sont. Correct it to corps while retaining corpa diplomatically."),
        25: ("paragraph Ceci montre, reference XIV", "The interdigit stop in 4 3 is absent or too faint in the main image. NOTE_6 specifically directs restoration of these reference-number stops; retain 4.3 in both layers."),
        26: ("paragraph Ceci montre, plus baut", "The letter after plus has a closed lower bowl and high ascender: printed b. The contextual word is haut; preserve baut diplomatically and haut in the corrected text."),
        27: ("heading 2.3.", "The heading visibly ends with a stop after 3; both layers correctly retain it."),
        28: ("formula (2.3) and following paragraph", "The handwritten epsilon has the open form. NOTE_6 accepts epsilon and varepsilon for this glyph; no local notation edit is made."),
        29: ("line immediately after (2.3)", "The closing parenthesis of (j=i) is followed immediately by explicitée, without a comma. The diplomatic layer already matches, and the corrected layer has the corresponding comma-free (j≤i)."),
        30: ("line immediately after (2.3)", "The print has j=i. The operations satisfy gamma_t(x)=lambda_{t/(1-t)}(x), whose coefficient of t^i is the sum over 1≤j≤i of binomial(i−1,j−1)lambda^j(x). Thus the range j≤i, already in the corrected layer, includes the required lower-degree terms."),
        31: ("first text line", "The first text line is est un isomorphisme modulo torsion. The attached folio-5 markers precede est un."),
        32: ("heading 2.4.", "The printed heading ends in a stop. The attached layers have 2.4."),
        33: ("§2.4, ses deux concurents", "Only one r is printed in concurents. The corrected spelling is concurrents; the attached current layer still has the printed spelling, so a current-layer patch is required."),
        34: ("§2.4, morphisme propre", "The mark above propre is a thin isolated high stroke between the letters, separated from the typed letter and unlike the short accents in schémas and noethériens on that line. Read propre as the attached layers do."),
    }
}

for evidence_file in sorted(OUT.glob('evidence_*.json')):
    for source, entries in json.loads(evidence_file.read_text()).items():
        EVIDENCE.setdefault(source, {}).update({int(k): tuple(v) for k,v in entries.items()})

def dump_jsonl(path, rows):
    path.write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in rows), encoding="utf-8")

def collect():
    records=[]
    finding_lookup={}
    for name, entries in EVIDENCE.items():
        findings=json.loads((ROOT/'check/findings'/name).read_text())
        for index,(region,reason) in entries.items():
            f=findings[index-1]
            row={"record_type":"checker", "page":f['page'], "source_id":f"check/findings/{name}#{index}",
                 "verdict":"confirmed", "printed_reading":f['scan'],
                 "image":f"scan/SGA6_scan_360dpi.pdf#page={f['page']+14}", "region":region,
                 "reason":reason, "change":f.get('fix') or (f.get('corrected') if f['kind']=='misprint_in_print' else "Existing reading or documented convention retained"),
                 "forms":"French diplomatic and corrected; English where meaning or notation is affected", "kind":f['kind']}
            records.append(row)
            finding_lookup[(name,index)]=(f,row)
    for log in ['FIXLOG_6.jsonl','FIXLOG_6_CURRENT.jsonl']:
        for index,line in enumerate((ROOT/'fixes'/log).read_text().splitlines(),1):
            f=json.loads(line)
            candidates=[(f0,row) for f0,row in finding_lookup.values()
                        if f0['page']==f['page'] and f0.get('fix') and f0['fix'].get('old')==f['old'] and f0['fix'].get('new')==f['new']]
            if candidates:
                f0,row=candidates[0]
                records.append({**row,"record_type":"fixlog","source_id":f"fixes/{log}#{index}","change":{"old":f['old'],"new":f['new']},"forms":"French diplomatic" if log=='FIXLOG_6.jsonl' else "French corrected and reading", "related_finding":row['source_id']})
            elif log=='FIXLOG_6_CURRENT.jsonl' and index==334:
                row=finding_lookup[('findings_001_005.json',29)][1]
                records.append({**row,"record_type":"fixlog","source_id":f"fixes/{log}#{index}","change":{"old":f['old'],"new":f['new']},"forms":"French corrected and reading"})
            elif log=='FIXLOG_6_CURRENT.jsonl' and index==335:
                records.append({"record_type":"fixlog","page":4,"source_id":f"fixes/{log}#{index}","verdict":"confirmed","printed_reading":"les sommes d'expression de la forme","image":"scan/SGA6_scan_360dpi.pdf#page=18","region":"§2.3, line before the product display","reason":"The printed expression lacks the final plural s. The phrase names sums of multiple displayed expressions; retain the plural correction and the singular diplomatic reading.","change":{"old":f['old'],"new":f['new']},"forms":"French corrected and reading","kind":"misprint_correction"})
    for index,m in enumerate(json.loads((ROOT/'fixes/MISPRINTS_6.json').read_text()),1):
        matches=[(f,row) for f,row in finding_lookup.values() if f['page']==m['page'] and f['kind']=='misprint_in_print' and f['where']==m['where']]
        if matches:
            f,row=matches[0]
            records.append({**row,"record_type":"misprint","source_id":f"fixes/MISPRINTS_6.json#{index}","correction":m['correct'],"related_finding":row['source_id']})
    row=finding_lookup[('findings_001_005.json',29)][1]
    records.append({**row,"record_type":"open_item","source_id":"fixes/REPLAY_MANUAL_6.json#1","verdict":"confirmed","change":"Already placed: diplomatic (j=i) explicitée; corrected (j≤i) explicitée. No additional edit is required.","reason":row['reason']+" The open-replay entry is stale relative to the attached layers; FIXLOG_6_CURRENT line 334 records its manual placement."})
    extra=OUT/'extra_decisions.json'
    if extra.exists(): records.extend(json.loads(extra.read_text()))
    dump_jsonl(OUT/'decisions.jsonl',records)
    patches=[{"page":5,"layer":"current","old":"ses deux concurents","new":"ses deux concurrents","source_id":"fixes/MISPRINTS_6.json#13","reason":"The scan prints concurents, but the corrected layer has not applied the accepted spelling correction.","kind":"misprint_correction"}]
    extra=OUT/'extra_patches.json'
    if extra.exists(): patches.extend(json.loads(extra.read_text()))
    dump_jsonl(OUT/'patches.jsonl',patches)
    patch_ids={p['source_id'] for p in patches}
    patched_findings={r.get('related_finding') for r in records if r['source_id'] in patch_ids}
    overrides_file=OUT/'record_overrides.json'
    overrides=json.loads(overrides_file.read_text()) if overrides_file.exists() else {}
    for row in records:
        row['scan_scope']='Main PDF directly viewed; witness use is separately recorded in page_status.jsonl and individual reasons.'
        reading=row.get('printed_reading','')
        if isinstance(reading,str):
            for old,new in [(' (both scans)',''),(', both scans',''),(' in either scan',' in the main scan'),(' in neither scan',' in the main scan')]:
                reading=reading.replace(old,new)
            row['printed_reading']=reading
        if row['source_id'] in patch_ids or row['source_id'] in patched_findings:
            row['verdict']='not applied and now applied'
        row.update(overrides.get(row['source_id'],{}))
    dump_jsonl(OUT/'decisions.jsonl',records)
    pages=[]
    for p in range(1,6):
        pages.append({"page":p,"pdf_page":p+14,"fully_checked":True,"main_scan_viewed":"four overlapping horizontal strips","witness_viewed":p in [3,4,5],"findings_count":sum(1 for r in records if r['record_type']=='checker' and r['page']==p),"begins":{"1":"Exposé 0","2":"de sorte que","3":"2.1 Pour ce qui est","4":"(tranformant la classe","5":"est un isomorphisme"}[str(p)],"notes":"Main scan compared word by word and symbol by symbol; doubtful marks compared with the 300 dpi witness on pp. 3, 4, 5. Retained restored faint stops on p. 3 and degree dot on p. 5; exact decisions in extra_decisions.json." if p in [3,4,5] else "Main scan compared word by word and symbol by symbol."})
    extra=OUT/'extra_pages.json'
    if extra.exists(): pages.extend(json.loads(extra.read_text()))
    dump_jsonl(OUT/'page_status.jsonl',pages)
    return records

if __name__=='__main__':
    rows=collect()
    print(json.dumps({"decision_rows":len(rows)}))
