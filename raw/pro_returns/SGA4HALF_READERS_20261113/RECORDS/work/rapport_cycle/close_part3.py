import json,difflib,collections
from pathlib import Path
from record import append
O=Path(__file__).resolve().parent;S=O.parents[1]/'source'
append('own_findings.jsonl',dict(id='S45-ASTRA-R-0024',page='122',place='3.6 first commutative square, bottom arrow',printed_reading='One lower horizontal arrow labelled (Phi^f) prime',tex_reading='Miller and English have a duplicate ar[r]; Codex has one.',change='Retain one arrow in French and remove the duplicated English arrow command.',kind='extra',reason='Scan square has one horizontal morphism, as in Codex. The duplicate command in English has no second printed counterpart.'))
append('own_findings.jsonl',dict(id='S45-ASTRA-R-0025',page='111',place='1.4, Dold–Puppe bibliographical parenthesis',printed_reading='(Homologie nicht additiver Funktoren. Anwendungen. Ann. Inst. Fourier XI 1961, p.201–312)',tex_reading=r'\cite{do61}',change='Restore full printed inline bibliographic wording while preserving the original cite key via PrintCite.',kind='missing',reason='The inline parenthesis is present in the scan; a bare generated citation cannot by itself reproduce its printed wording. The title remains in German in the English text.'))
changes=json.loads((O/'en_changes_3.json').read_text());changes.append(dict(id='S45-ASTRA-R-0024',page=122,old=r"F^*\sG_0 \ar[r]^-{(\Phi^f)'} \ar[r]",new=r"F^*\sG_0 \ar[r]^-{(\Phi^f)'}"))
citation=r'\PrintCite{(Homologie nicht additiver Funktoren. Anwendungen. Ann. Inst. Fourier XI 1961, p.~201--312)}{\cite{do61}}'
changes.append(dict(id='S45-ASTRA-R-0025',page=111,old=r'\cite{do61}',new=citation,ai_translated=False))
(O/'en_changes_3.json').write_text(json.dumps(changes,ensure_ascii=False,indent=2))
ss=json.loads((O/'supplement_fr_3.json').read_text());ss.append(dict(id='S45-ASTRA-R-0025',page=111,old=r'\cite{do61}',new=citation));(O/'supplement_fr_3.json').write_text(json.dumps(ss,ensure_ascii=False,indent=2))
# Explicit provenance for all inherited Codex mutations, including those omitted from its old audit CSV.
for c in (2,3):
 for mode in ('dip','corr'):
  a=(S/'fr/miller_src'/f'sga4.5-{c}.tex').read_text().splitlines(True);b=(S/f'fr/codex_{mode}'/f'sga4.5-{c}.tex').read_text().splitlines(True)
  (O/'records'/f'miller_to_codex_{mode}_{c}.diff').write_text(''.join(difflib.unified_diff(a,b,fromfile=f'fr/miller_src/sga4.5-{c}.tex',tofile=f'fr/codex_{mode}/sga4.5-{c}.tex')))
dec=[json.loads(l) for l in (O/'decisions.jsonl').read_text().splitlines()];own=[json.loads(l) for l in (O/'own_findings.jsonl').read_text().splitlines()]
ps=[json.loads(l) for l in (O/'pages.jsonl').read_text().splitlines()]
for p in ps:p['findings']=sum(d['printed_page']==p['printed_page'] for d in dec)+sum(d['page']==p['printed_page'] for d in own)
(O/'pages.jsonl').write_text(''.join(json.dumps(p,ensure_ascii=False)+'\n' for p in ps))
