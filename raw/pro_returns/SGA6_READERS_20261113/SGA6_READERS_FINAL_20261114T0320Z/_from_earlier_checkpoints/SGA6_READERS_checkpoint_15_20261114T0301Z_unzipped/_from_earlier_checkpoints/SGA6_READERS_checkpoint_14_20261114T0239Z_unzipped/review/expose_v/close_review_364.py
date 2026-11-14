#!/usr/bin/env python3
"""Close already viewed cross-page records and audit the completed V scope.

This script adds no image verdict; it links observations saved during the
individual full-page comparisons and checks exact cumulative composition.
"""
from pathlib import Path
import collections,hashlib,json,re,sys
from review_helpers import Review,read
here=Path(__file__).resolve().parent
root=here.parents[1]
r=Review()
row=next(x for x in read('decisions.jsonl') if x['source_id']=='fixes/RECONCILE_CODEX_6.json#305').copy()
row.update(verdict='confirmed for both printed357 and360 occurrences',
 printed_reading='Both the357 introductory target and the360 lower-left square object print Ch(Gr wedge)) with one unmatched closing parenthesis.',
 region='357 introductory completed-class target;360 lower-left square object',
 change='Retain both double closes diplomatically;357 existing current repair and360 checker356_360#21 current repair remove one close each.')
row['image']+='; scan/SGA6_scan_360dpi.pdf#page=374; scan/SGA6_witness_300dpi.djvu#page=371'
row['reason']+=' The second occurrence named in the Codex queue was subsequently personally compared on360,as saved under check/findings/findings_356_360.json#21. Its source/target is the same explicit Ch(Gr B) construction,so the identical unmatched-close repair applies there. This closes both queue loci without extending the357 image claim.'
r.decisions.append(row)
row=next(x for x in read('decisions.jsonl') if x['source_id']=='fixes/RECONCILE_CODEX_6.json#297').copy()
row.update(verdict='global replacement rejected;all occurrence-specific glyph decisions completed',
 region='typed definition on326 and separately recorded later operation glyphs through the end ofV',
 change='Keep the typed v at326 and the independently observed later nablas;no global glyph substitution.')
row['reason']+=' The later pages are now fully compared. Their separately saved operation-glyph observations include ASTRA-V-PRODUCT-GLYPHS-327,ASTRA-V-PRODUCT-GLYPHS-329,ASTRA-V-PRODUCT-GLYPH-333,ASTRA-V-FORMS-344,and ASTRA-V-NABLA-353. The exact transport map remains m_rho=rho composed with m composed with(rho_inverse×rho_inverse). The per-page source records establish the glyphs independently,so no future image scope or global substitution remains outstanding.'
row['related_occurrence_ids']=['ASTRA-V-PRODUCT-GLYPHS-327','ASTRA-V-PRODUCT-GLYPHS-329','ASTRA-V-PRODUCT-GLYPH-333','ASTRA-V-FORMS-344','ASTRA-V-NABLA-353']
r.decisions.append(row)
r.commit()

sys.path.insert(0,str(root/'review/english'))
from reviewed_french import load_reviewed_pages
stream={}
for layer in ['diplomatic','current']:
 pages,record=load_reviewed_pages(364,layer,start=297)
 assert len(pages)==68
 assert all(r'\inN' not in text and r'\ObA' not in text for text in pages.values())
 assert r'\arrow[l,"\Phi^k"' + "']" in pages[363] if layer=='current' else True
 stream[layer]=record
(here/'CUMULATIVE_STREAM_AUDIT.json').write_text(json.dumps(stream,ensure_ascii=False,indent=2)+'\n')

dec=read('decisions.jsonl');own=read('own_findings.jsonl');patch=read('patches.jsonl');pages=read('page_status.jsonl')
registry=json.loads((root/'build/registry.json').read_text())
required=[x for x in registry if str(x.get('page','')).isdigit() and 297<=int(x['page'])<=364]
ids={x['source_id'] for x in dec}
assert not [x['id'] for x in required if x['id'] not in ids]
assert sorted(x['page'] for x in pages if x['fully_checked'])==list(range(297,365))
assert len(ids)==len(dec)
assert len({x['source_id'] for x in own})==len(own)
codex=json.loads((root/'fixes/RECONCILE_CODEX_6.json').read_text())['entries']
v_codex=[i for i,x in enumerate(codex,1) if str(x.get('expose','')).strip()=='V']
assert all(f'fixes/RECONCILE_CODEX_6.json#{i}' in ids for i in v_codex)
hold=[x['id'] for x in required if x['type']=='hold_difference']
assert not hold
for name in ['decisions.jsonl','own_findings.jsonl','patches.jsonl','page_status.jsonl']:
 content=(here/name).read_text()
 assert not re.search(r'/workspace/|/home/|[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}',content,re.I),name
conventions={
 'scope':'Exposé V297–364;all68 pages fully compared',
 'policy':'Occurrence-specific source forms are retained in both layers unless a separately proved current-only misprint correction is recorded. No global glyph replacement is inferred.',
 'categories':'Script C and script G are read separately at their actual occurrences. The sixteen historical G occurrences are closed by checker306_310#14;the recorded j and Gr maps explain their relationship.',
 'word_rules':'Observed theorem/definition word groups and defined terms use explicit underlining with their observed mathematical/plain exceptions. Statement-label bold and section-title layout remain the accepted NOTE_6 conventions. The351–355 aggregate is closed.',
 'paragraph_and_item_labels':'Ordinary observed numbered paragraphs and item labels have ordinary weight. This does not change accepted named-statement labels.',
 'low_marks':'Three-point ellipses,product stops,and hatted object placeholders follow the inspected baseline positions. Literal two-point and four-point source groups have separate records;359 preserves three four-point product groups.',
 'number_letters':'Plain and reinforced Q,Z,N occurrences are decided locally,without a global macro replacement.',
 'exterior_and_algebra_wedges':'The small exterior-power wedges on315–316 and the46 algebra-name wedges on356–360 are separately identified constructions. The latter count is10,7,15,6,8 on actual pages356–360;the replacement names the identical augmented ring.',
 'transported_product':'The typed v at326 and independently observed later closed nablas name the exact conjugated product rho m(rho_inverse×rho_inverse);the global Codex replacement is rejected.',
 'Id_and_Abfil':'Capital Id occurrences and separately ruled Ab/fil names are literal scoped forms. The capital Id on361 is explicit,independent of local id macro resets.',
 'phi_and_other_letters':'Closed/open phi and category/operation forms are retained as directly recorded;no single global phi mapping is imposed.',
 'author_notes':'Every inspected author note keeps its observed explicit label and source position;no auto-numbering is inferred. Individual source records and patches carry the exact calls/text.',
 'scope_resets':'The364 macro block is a nonprinted ExposéVI continuation,not evidence for an id or other glyph on364. Actual VI usage evidence belongs to its reviewer.',
 'physical_marks':'Damaged or extra ink is described without inventing a character or cause;349 and364 have explicit observations.',
 'occurrence_records':[{'source_id':x['source_id'],'page':x['page'],'kind':x.get('kind'),'printed_reading':x['printed_reading'],'change':x.get('change')} for x in dec+own if x.get('kind') in ['font','symbol','underline','physical_observation']]
}
(here/'CONVENTIONS_COMPLETED_V.json').write_text(json.dumps(conventions,ensure_ascii=False,indent=2)+'\n')
packets=sorted(x.name for x in here.glob('*.json') if x.name.startswith(('identification_','author_claim_issue_','integration_amendment_','amendment_')))
summary={'scope':[297,364],'fully_checked_pages':68,'source_decisions':len(dec),'own_findings':len(own),'patch_records':len(patch),
 'source_record_types':dict(collections.Counter(x['record_type'] for x in dec)),
 'nominal_registry_rows':len(required),'missing_registry_ids':[],
 'codex_V_entry_indices':v_codex,'HOLD_rows_in_scope':hold,
 'closed_aggregates':['check/findings/findings_306_310.json#14','check/findings/findings_351_355.json#10','check/findings/findings_356_360.json#2','fixes/RECONCILE_CODEX_6.json#297','fixes/RECONCILE_CODEX_6.json#305'],
 'author_claims':'All recorded author-claim defects retain their printed body;proof packets supply exact counterexamples/maps and no replacement theorem.',
 'proof_packets':packets,'cumulative_stream':'Both branches load exactly after the earlier middle stream and separate314 rendering repair.',
 'reader_compile':'No new reader compilation performed by this final audit;coordinator owns checkpoint builds.'}
(here/'FINAL_AUDIT.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(summary,ensure_ascii=False))
