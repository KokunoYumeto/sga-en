#!/usr/bin/env python3
"""Record and repair the independently observed double Cart underline."""
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
REASON = ("The scan has one rule under each Cart operator (2 on142,6 on143,4 on144). "
          "The active source definition is \\providecommand{\\Cart}{\\underline{\\operatorname{Cart}}}. "
          "Its exact expansion already supplies that rule; the earlier local wrapper expanded to "
          "\\underline{\\underline{\\operatorname{Cart}}} and produced two rules in the rendered reader. "
          "Withdraw that wrapper and retain the source macro at these twelve positions. "
          "The separately ruled S subscript is unchanged.")
IDS = {f'ASTRA-I-CART-{p:03d}' for p in (142,143,144)}
FINDING = 'check/findings/findings_141_145.json#12'

for name in ('patches','own_findings','decisions'):
    path = HERE / (name+'.jsonl')
    rows = [json.loads(s) for s in path.read_text().splitlines()]
    out = []
    for row in rows:
        sid = row.get('source_id')
        if name == 'patches':
            if sid in IDS:
                continue
            if row.get('page') in (142,143,144):
                for key in ('old','new'):
                    row[key] = row[key].replace(r'\underline{\Cart}',r'\Cart')
        if name == 'own_findings' and sid in IDS:
            row.update(verdict='amended',tex=r'\Cart already expands to \underline{\operatorname{Cart}}',
                       change='Withdraw the added local wrapper; retain the one-rule source macro.',reason=REASON)
        if name == 'decisions' and (sid == FINDING or row.get('related_finding') == FINDING):
            row.update(verdict='confirmed',change='Retain the original Cart macro: its active definition supplies one rule.',reason=REASON)
        out.append(row)
    path.write_text(''.join(json.dumps(r,ensure_ascii=False)+'\n' for r in out))

path = HERE/'add_141_145.py'
text = path.read_text()
start = text.index('for p,count in[(142,2),(143,6),(144,4)]:')
end = text.index("id='ASTRA-I-PARF-143'",start)
text = text[:start] + (
    'cart_reason='+repr(REASON)+'\n'
    'for p,count in[(142,2),(143,6),(144,4)]:\n'
    "    id=f'ASTRA-I-CART-{p:03d}'\n"
    "    r.own_finding(id,p,'One rule under Cart',r'\\Cart already supplies one rule','Retain the original macro; withdraw the extra wrapper',cart_reason,'Every Cart occurrence',verdict='amended',witness=153 if p==142 else 154 if p==143 else None)\n"
    "r.finding(batch,12,'Twelve Cart operators independently underlined',cart_reason,'All twelve Cart operators',change='Retain the original Cart macro: its active definition supplies one rule.',witness=154)\n"
) + text[end:]
path.write_text(text)
(HERE/'cart_macro_audit.json').write_text(json.dumps({
    'status':'rendering repair adjudicated from the recorded scan readings and exact macro expansion',
    'pages':[142,143,144], 'occurrences':12,
    'active_definition':r'\providecommand{\Cart}{\underline{\operatorname{Cart}}}',
    'withdrawn_wrapper':r'\underline{\Cart}', 'retained_macro':r'\Cart',
    'source_ids':sorted(IDS)+[FINDING], 'reason':REASON,
    'effect':'Both French layers have one Cart rule. Corresponding English transfer uses that same definition.',
    'prior_checkpoints':'Immutable; this repair begins with checkpoint04.'
},ensure_ascii=False,indent=2)+'\n')

from review_helpers import Review
Review().commit()
path = HERE/'HANDOFF.txt'
text = path.read_text().replace('"patches.jsonl": 458','"patches.jsonl": 455')
audit = 'Rendering audit: the twelve Cart occurrences retain their source macro, which already supplies one lower rule; three redundant wrapper patches were withdrawn.\n'
if audit not in text:text += audit
path.write_text(text)
root = HERE.parents[1]
files = sorted(p for p in HERE.iterdir() if p.is_file() and p.name != 'frozen_manifest.tsv')
(HERE/'frozen_manifest.tsv').write_text('path\tbytes\tsha256\n'+''.join(
    f'{p.relative_to(root).as_posix()}\t{p.stat().st_size}\t{hashlib.sha256(p.read_bytes()).hexdigest()}\n' for p in files))
print(json.dumps({'pages':[142,143,144],'one_rule_occurrences':12,'removed_wrapper_patches':3}))
