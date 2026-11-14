#!/usr/bin/env python3
"""Save the personally compared297–341 paragraph-boundary transport.

Each join was read in both adjacent reviewed source pages and English prose.
This repair touches outer newline separators only; it makes no new image claim.
"""
from pathlib import Path
import hashlib,json,sys
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE))
from contribution import dump,build_records
def sha(s):return hashlib.sha256(s.encode()).hexdigest()
PARAGRAPH={
312:'The universal-weight calculation ends;313 begins its particular H=Ghat application in a new paragraph.',
313:'The Section2 introductory paragraph ends before Definition2.1.',
314:'The defining lambda-homomorphism equality ends before Examples2.2.',
320:'The two2.4.2 relations end before the source terminology paragraph.',
323:'The2.9 passage ends before the continuation definitions and the next On suppose toujours paragraph.',
325:'The coefficient computation ends before the separate numbered paragraph3.3.',
329:'The3.8 universal-polynomial sentence ends before Definition3.9.',
330:'The geometric augmentation paragraph ends before numbered paragraph3.10.',
331:'The filtration convention ends before Proposition3.11.',
332:'The commutativity proof ends before the paragraph introducing the4.2 universal property.',
337:'The inverse-map proof ends before Corollary4.15.',
340:'The source explicitly starts a new paragraph after the second align-star calculation; checker341_345#1 records this boundary.'
}
path=HERE/'paragraph_join_audit_297_341.json'
prior=json.loads(path.read_text()) if path.exists() else None
changes=[]
for page in range(297,342):
    p=HERE/'translations'/f'{page}.tex';old=p.read_text()
    new=old.lstrip('\n').rstrip('\n')+('\n\n' if page in PARAGRAPH else '\n')
    assert old.strip('\n')==new.strip('\n')
    if old!=new:
        changes.append(dict(page=page,old_sha256=sha(old),new_sha256=sha(new),old_leading_newlines=len(old)-len(old.lstrip('\n')),new_leading_newlines=0,old_trailing_newlines=len(old)-len(old.rstrip('\n')),new_trailing_newlines=2 if page in PARAGRAPH else 1))
        p.write_text(new)
joins=[]
for page in range(297,341):
    f=(HERE/'source_packets'/str(page)/'current.tex').read_text();g=(HERE/'source_packets'/str(page+1)/'current.tex').read_text()
    e=(HERE/'translations'/f'{page}.tex').read_text();n=(HERE/'translations'/f'{page+1}.tex').read_text()
    joins.append(dict(record_type='manually_compared_source_folio_join',after=page,before=page+1,paragraph_break=page in PARAGRAPH,source_tail=f[-450:],source_head=g[:450],English_tail=e[-300:],English_head=n[:300],reviewed_French_page_sha256s={str(page):sha(f),str(page+1):sha(g)},reason=PARAGRAPH.get(page,'The preceding source clause or display continues directly in the following source words; the English retains that same continuation without a blank TeX line.'),comparison_scope='Exact reviewed French and translated prose at this join; source image adjudications remain those of the frozen French audit.'))
report=dict(scope='297–341,all44 internal folio joins',status='all displayed adjacent source passages manually compared',implementation='The maker concatenates explicit translated line endings without adding another newline. A marker inserted before an already present newline reuses that newline. Mathematical units and every non-boundary character are unchanged.',translation_outer_newline_changes=prior['translation_outer_newline_changes'] if prior else changes,joins=joins,open_endpoint='341 ends by,continuing the source homomorphism definition on342. No paragraph break is added at that unfinished clause.')
dump(path,report)
batches=json.loads((HERE/'batches.json').read_text())
record=dict(record_type='paragraph_boundary_transport_audit',page=341,source_id='English manual source-join comparison297–341',audit='review/english/contributions/exposes_v_vi/paragraph_join_audit_297_341.json',audit_sha256=sha(path.read_text()),decision='All44 joins were compared directly as text. Twelve source paragraph boundaries retain an explicit blank line;the other32 joins continue without an inserted blank line. The original mathematical units,source variants,stable targets,and formula placements are unchanged. Prior chunk hashes and exact replacement spans are refreshed after this rendering-only transport correction.')
batch=next(b for b in batches if b['first']==337)
batch['extra_records']=[r for r in batch.get('extra_records',[]) if r.get('record_type')!='paragraph_boundary_transport_audit']+[record]
dump(HERE/'batches.json',batches);build_records()
print(json.dumps(dict(joins=len(joins),paragraph_breaks=len(PARAGRAPH),initial_translation_files_changed=len(report['translation_outer_newline_changes']))))
