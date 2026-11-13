"""Add the two scan-verified English repairs disclosed by mathematical alignment.
Idempotent ledger append; source scan p209 was directly inspected again.
"""
from pathlib import Path
import json
B=Path(__file__).parent
p=B/'own_findings.jsonl';rs=[json.loads(x) for x in p.read_text().splitlines()];ids={r['id'] for r in rs}
for n,place,pr,tex,change,why in [
 (66,'5.2, uniqueness of extension to fractional ideals','tout idéal a une puissance','every ideal $a$ has a power','every ideal has a power','The scanned a is the French verb avoir, not a variable naming the ideal. Remove the unintended mathematical symbol in every English form.'),
 (67,'5.3, attribution of the name of Hecke characters','appelés par Weil caractères de Hecke','also called Weil Hecke characters','called by Weil Hecke characters','The scan attributes the nomenclature to Weil; it does not name a separate class of Weil Hecke characters. Restore the grammatical agency in English.'),
 (68,'1.12, English indefinite article','après extension du corps fini de base','after a extension','after an extension','Repair the indefinite article before extension in the English translation; no source-content change.'),
 (69,'1.22, end of formula for the target action',r'$x\mapsto (y\mapsto F x\cdot y\cdot x^{-1})$',r'$x\mapsto (y\mapsto F x\cdot y\cdot x^{-1})$)', 'Remove the second closing parenthesis in English.','The full scan p181, directly re-inspected, prints only the closing parenthesis belonging to the inner map. The further parenthesis in the English component is an extra transcription mark; the French component already has the correct punctuation.'),
 (70,'1.24(ii), English group-theoretic term','classe de conjugaison','conjugation class','conjugacy class','Use the same English term conjugacy class as in part(iii) and the proof on182; the source uses the same French term throughout.'),
 (71,'3.3, opening sentence','Soient ... comme en 3.2','Let ... as in','Let ... be as in','Restore the missing English verb in the opening instruction; all mathematical arguments and references remain the same.'),
 (72,'4.7, two uses of système projectif in one sentence','système projectif de torseurs sous le système projectif de groupes','inverse system of torsors under the projective system of groups','inverse system of torsors under the inverse system of groups','The same French technical term is used twice in one sentence. Use inverse system for both, consistently with every other occurrence in the SGA4HALF English components; the supplied SGA7 glossary admits both terms, while SGA4 uses projective system.'),
 (73,'7.21, description of Sperber’s methods','par des méthodes p-adiques','by methods p-adic methods','by p-adic methods','Remove the duplicated English noun; the French has only one occurrence of méthodes.'),
 (74,'2.2 and 5.7, connecting word within citation postnotes','et','et','and','Translate the two French conjunctions inadvertently retained in the English citation postnotes; citation keys and reference numbers are unchanged.')]:
 id=f'S45-ASTRA-S-{n:04}'
 page={68:175,69:181,70:181,71:189,72:199,73:229,74:183}.get(n,209)
 entry=dict(id=id,page=str(page),place=place,printed_reading=pr,tex_reading=tex,change=change,kind='extra' if n==69 else 'translation',reason=why)
 if id not in ids:rs.append(entry)
 else:rs=[entry if r['id']==id else r for r in rs]
p.write_text(''.join(json.dumps(r,ensure_ascii=False)+'\n' for r in rs))
