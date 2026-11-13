"""Idempotent completion of the Arcata English audit and resolved page anchors."""
from pathlib import Path
import json

ROOT=Path(__file__).resolve().parents[1]
W=ROOT/'work/arcata'

def read(name):
    return [json.loads(x) for x in (W/name).read_text().splitlines() if x.strip()]

def write(name,rows):
    (W/name).write_text(''.join(json.dumps(x,ensure_ascii=False)+'\n' for x in rows))

findings=[
('0001','14,20–21,26,28–35','Units and multiplicative groups','Asterisk superscripts','Times superscripts','Restore the printed asterisk at the unit-group occurrences in the English, as in the independently checked French.','symbol','The complete English component was read against the checked French and the scan. The printed unit-group symbol is an asterisk; Miller macro equivalence does not justify replacing the sign by a multiplication cross.'),
('0002','32','Tsen proof, polynomial argument','f(underlined T)','f(T)','Restore the underline on the tuple argument in both occurrences.','symbol','The print distinguishes the tuple of indeterminates from the individual indeterminates. The English had dropped the underline retained by the corrected French.'),
('0003','37,47–50,61,64,68','Complements of open or closed subsets','Minus sign','Setminus sign','Restore the printed minus signs in the English complement expressions.','symbol','The relevant scanned expressions use a minus sign. This records a literal sign restoration, shared by all forms, not a correction of the print.'),
('0004','39,52–56,69','Cohomological degree placeholders and cospecialization','Asterisk superscripts','Filled-bullet superscripts','Restore the asterisk for these cohomology and cospecialization placeholders.','symbol','Each relevant scanned expression was checked. Complex degree superscripts on M and T remain bullets: they were not included in this replacement.'),
('0005','44–45','Cohomology functor arguments','Centred dot','Dash','Restore the printed centred-dot placeholders in H^q(X,·) and H^q(X_0,·).','symbol','The dot is visible in the scan. This aligns the English with the checked French without changing Miller’s Hom/sheaf conventions.'),
('0006','52–53','Half-open intervals','French-style ]0,t] and ]0,eta t]','English-style (0,t] and (0,eta t]','Restore the author’s interval notation.','symbol','The interval is mathematically unchanged, but the user requires the author’s notation in every form. This is a notation restoration and gets no apparatus entry.'),
('0007','32,66','English heading anchors','Corresponding headings of III.3 and VI','Missing English label names','Add the stable labels I:3-3 and I:6.','structural','The labels support the restored original contents and cross-references. They introduce no visible authorial text and no print-misprint variant.'),
('0008','25','Inverse functor following Proposition II.4.4','G-ensemble correspondant à A','corresponding G-set','Restore corresponding to A in the English.','missing','The scan explicitly names the algebra A again. Although the English antecedent is understandable, the original phrase is restored in full.'),
('0009','44,60–61','Formula punctuation and bare index/hat placeholders','T(u).alpha; bare subscript1 and superscript hat','T(u)alpha; (-)_1 and (-)^hat','Restore the printed dot and bare placeholders in the English.','notation','These are shared notation restorations. The author’s point and bare placeholders are legible in the scanned definitions; the English had silently replaced them with other presentation.'),
('0010','18,24','Raynaud references','M. Raynaud, Anneaux Locaux Henséliens, chapitre V; Anneaux locaux henséliens, chapitre I','Bare citation key with postnote','Restore the author/title/chapter wording through PrintCite while retaining the ra70 key.','missing','The citations are printed as bibliographic prose. A global numeric citation would omit the title and, on page18, the author; the English restores both printed references.'),
]
rows=read('own_findings.jsonl')
for row in rows:
    if row['id']=='S45-ASTRA-A-0032':
        row['change']='Restore all ten original entries as a navigable table in both languages; retain the unnumbered status of the contents page.'
known={x['id'] for x in rows}
for n,page,place,printed,old,change,kind,reason in findings:
    ident='S45-ASTRA-E-'+n
    if ident not in known:
        rows.append(dict(id=ident,page=page,place=place,printed_reading=printed,
                         tex_reading=old,change=change,kind=kind,reason=reason))
write('own_findings.jsonl',rows)

supplement=ROOT/'work/rapport_cycle/records/arcata_review_supplement.json'
if supplement.exists():
    data=json.loads(supplement.read_text());finding=data['own_finding']
    if finding['id'] not in {r['id'] for r in rows}:rows.append(finding)
    write('own_findings.jsonl',rows)
    vars=read('variants.jsonl')
    if finding['id'] not in {r['id'] for r in vars}:
        vars.append(dict(id=finding['id'],page='70',place=finding['place'],printed='3.2.4',
                         corrected=r'\ref{V:3-2} et \ref{V:3-4}',en_printed='3.2.4',
                         en_corrected=r'\ref{V:3-2} and \ref{V:3-4}',kind='reference',reason=finding['reason']))
    write('variants.jsonl',vars)

pages=read('pages.jsonl')
fr=json.loads((W/'page_anchors_fr.json').read_text())
en=json.loads((W/'page_anchors_en.json').read_text())
for p in pages:
    key=p['printed_page']
    if key in fr:p['start_fr']=fr[key]
    if key in en:p['start_en']=en[key]
    p['findings']=sum(d['printed_page']==key for d in read('decisions.jsonl'))+sum(x['page']==key for x in rows)
write('pages.jsonl',pages)

# NOTE_45 explicitly excludes Miller's label-based numbering presentation from
# content errors. These four proposals merely rename stable targets; keep the
# scan-established visible-number presentation, without treating it as an error.
decisions=read('decisions.jsonl')
presentation={
 'S45-SOL-0199':('I:5-2-4','2.3.1'),
 'S45-SOL-0201':('I:5-2-5','2.3.2'),
 'S45-SOL-0204':('I:5-2-4','2.3.1'),
 'S45-SOL-0205':('I:5-2-6','2.3.3'),
}
for d in decisions:
    if d['id'] in presentation:
        label,number=presentation[d['id']]
        d['verdict']='rejected'
        d['change_made']='Reject the proposed label renaming. Retain '+label+'; the visible printed number '+number+' is a common presentation choice, not a print correction.'
        d['reason']='The scan confirms '+number+'. The proposed change only renames a stable Miller label or its reference; NOTE_45 explicitly treats numbering through labels as presentation, not an error. Retain the existing target. The French Codex visible-number presentation is retained and aligned in English in every form, with no apparatus entry.'
        d['forms_affected']='No content correction; shared numbering presentation in all French and English forms.'
write('decisions.jsonl',decisions)

opening=[
dict(id='S45-SOL-0001',page='III',status='verified in final component',after='démonstration complète'),
dict(id='S45-SOL-0002',page='III',status='verified in final component',after="à l'utilisateur"),
dict(id='S45-SOL-0004',page='III',status='verified in final component',after='cette classe'),
dict(id='S45-SOL-0005',page='IV',status='applied',before='étaien devenues',after='étaient devenues'),
dict(id='S45-SOL-0006',page='4',status='restored full passage',after='Ce travail reprend'),
]
for ident,(label,num) in presentation.items():
    opening.append(dict(id=ident,page='60',status='rejected label rename; shared numbering presentation only',after=label,number=num))
(W/'opening_and_numbering_operations.json').write_text(json.dumps(opening,ensure_ascii=False,indent=2))
print(json.dumps(dict(pages=len(pages),sol=len(read('decisions.jsonl')),own=len(rows)),ensure_ascii=False))
