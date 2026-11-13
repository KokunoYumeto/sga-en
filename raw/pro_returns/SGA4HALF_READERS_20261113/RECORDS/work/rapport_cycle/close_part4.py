from pathlib import Path
import json,re,collections,difflib
P=Path(__file__).resolve().parent;S=P.parents[1]/'source'
def read(n):return [json.loads(l)for l in(P/n).read_text().splitlines()]
dec=read('decisions.jsonl');own=read('own_findings.jsonl');ps=read('pages.jsonl');vs=read('variants.jsonl')
for p in ps:p['findings']=sum(d['printed_page']==p['printed_page']for d in dec)+sum(d['page']==p['printed_page']for d in own)
(P/'pages.jsonl').write_text(''.join(json.dumps(p,ensure_ascii=False)+'\n'for p in ps))
changes=json.loads((P/'en_changes_4.json').read_text());ids={d['id']for d in changes}|{v['id']for v in vs if v.get('en_old')}
for d in changes:ids.update(d.get('sources',[]))
coverage=[]
already={546:'The second factor already reads Gamma_!(Y,L).',551:'The trace already has domain and codomain V.',556:'The English already says p=0,1.',558:'The English already uses dmu_n, with no spurious literal d.',559:'The group already has support D.',576:'The triangle already starts at Y.',583:'The flat morphism already has target S.',584:'The equation tag and label already read2.3.1.2.',589:'The Hom target already has shift2N.',590:'The diagram already has shift2N.',610:'The product weight already has K-prime.',611:'The first product class already has Y-prime.',614:'The structure sheaf already uses capital X-prime.',622:'The eta class already has twist q.',625:'The Hom arguments already read H(Y),H(X).',629:'The trace summand already has degree i.'}
for d in dec:
 if not 129<=int(d['printed_page'])<=153:continue
 n=int(d['id'][-4:])
 status='explicit English patch or printed/corrected variant' if d['id']in ids else already.get(n,'French spelling, agreement, or wording is already correctly conveyed in the English; no further semantic change.')
 coverage.append(dict(id=d['id'],page=d['printed_page'],status=status))
for d in own:
 if 129<=int(d['page'])<=153:coverage.append(dict(id=d['id'],page=d['page'],status='explicit English patch or variant'if d['id']in ids else'French spelling correction has no effect on English translation.'))
(P/'records/english_coverage_4.json').write_text(json.dumps(coverage,ensure_ascii=False,indent=2))
counts={}
for lang,name in [('fr','sga4.5-4.tex'),('en','sga4half_4_en.tex')]:
 t=(P/lang/name).read_text();markers=list(map(int,re.findall(r'\\PrintPage\{(\d+)\}',t)))
 assert markers==list(range(129,154)),(lang,markers)
 counts[lang+'_variants']=t.count(r'\var{');assert r'\bullet'not in t
 log=json.loads((P/f'records/{lang}_build_4.json').read_text());assert not any('unmatched'in x['status']or'ambiguous'in x['status'].lower()for x in log)
 # Durable change evidence with ZIP-relative source names.
 before=S/'fr/miller_src'/name if lang=='fr' else S/'en/sources/components'/name
 (P/f'records/{lang}_annotated_4.diff').write_text(''.join(difflib.unified_diff(before.read_text().splitlines(True),t.splitlines(True),fromfile=str(before.relative_to(S)),tofile=f'{lang}/{name}')))
d=[x for x in dec if 129<=int(x['printed_page'])<=153]
status=dict(component=4,printed_pages=[129,153],pages_visually_checked=25,sol_decisions=len(d),verdicts=dict(collections.Counter(x['verdict']for x in d)),own_findings=sum(129<=int(x['page'])<=153 for x in own),**counts,page_markers=25,compile_status='awaiting root whole-book build',restored_matter='Complete nine-entry contents page130; complete Baum–Fulton–Mac Pherson inline bibliographic parenthesis143; printed numbered proof paragraphs2.3.8.1–3 and references.',numbering_note='Rappel2.2.8 is a numbered subsubsection, not a theorem; preserve2.3.8.1–3 literal proof paragraph headings. Two variants each have Sol0605 and Sol0612 as their shared source ids.')
(P/'PART_IV_STATUS.json').write_text(json.dumps(status,ensure_ascii=False,indent=2));print(json.dumps(status,ensure_ascii=False,indent=2))
