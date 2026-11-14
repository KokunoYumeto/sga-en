"""One-shot explicit author-note labels, assigned from inspected page images."""
from pathlib import Path
import json
O=Path(__file__).resolve().parent
def load(n):return json.loads((O/n).read_text())
def save(n,a):(O/n).write_text(json.dumps(a,ensure_ascii=False,indent=2)+'\n')
patches=load('extra_patches.json');records=load('extra_decisions.json')
notes=[
 (8,'raisedstar',r'\footnote{On se permettra',r'\SGAAuthorFootnote{raisedstar}{On se permettra','call after localement d’insersection complète and footnote label'),
 (15,'raisedstar',r'\footnote{Cette analogie',r'\SGAAuthorFootnote{raisedstar}{Cette analogie','call after cap-produit and footnote label'),
 (20,'*',r'\footnote{Ceci est',r'\SGAAuthorFootnote{*}{Ceci est','author byline and note label'),
 (21,'*',r'\footnote{Dans ce séminaire',r'\SGAAuthorFootnote{*}{Dans ce séminaire','definition of lambda-ring and note label'),
 (24,'*',r'\footnote{Il est inutile',r'\SGAAuthorFootnote{*}{Il est inutile','first call after characteristic0 and note label'),
 (24,'*',r'\footnotemark[\value{footnote}]',r'\SGAAuthorFootMark{*}','repeated call after algébriquement clos'),
 (25,'1',r'\footnote{On peut construire',r'\SGAAuthorFootnote{1}{On peut construire','first note, after etc..., and its label'),
 (25,'*',r'\footnote{Condition inutile',r'\SGAAuthorFootnote{*}{Condition inutile','second note, after algébriquement clos, and its label'),
 (26,'*',r'\footnote{Cf.',r'\SGAAuthorFootnote{*}{Cf.','call after représentations linéaires de G and its label'),
 (27,'*',r'\footnote{Il faut supposer',r'\SGAAuthorFootnote{*}{Il faut supposer','end of the corollary statement and its note label'),
 (35,'*',r'\footnote{Cela se prouve',r'\SGAAuthorFootnote{*}{Cela se prouve','call after algébriquement clos and its note label'),
 (39,'*',r'\footnote{Par suite',r'\SGAAuthorFootnote{*}{Par suite','Theorem2.1 label and author-note label'),
 (41,'*',r'\footnote{La notation',r'\SGAAuthorFootnote{*}{La notation','formula(2.10), call after K(X), and Hartshorne/duality note label'),
 (50,'*',r'\footnote{Non',r'\SGAAuthorFootnote{*}{Non','call after réduit à0 and footnote label'),
 (54,'*',r'\footnote{Cette dernière',r'\SGAAuthorFootnote{*}{Cette dernière','call after ouvert affine and footnote label')]
perpage={}
for p,label,old,new,region in notes:
 perpage[p]=perpage.get(p,0)+1;sid=f'ASTRA-EARLY-NOTE-{p:03d}-{perpage[p]}'
 geometry={'raisedstar':'a high star within baseline parentheses','1':'a raised numerical1 within baseline parentheses','*':'a central star within baseline parentheses'}[label]
 reason=f'The directly read call and label use {geometry}. Preserve this explicit author label with the shared SGAAuthorFootnote/FootMark helpers; ordinary automatic numbering loses the printed mark.'
 if 'repeated' in region:reason='The repeated call after algébriquement clos is the same baseline parenthesized star as the first call on p24. Preserve the literal repeated mark without creating another note text.'
 patches.append(dict(page=p,layer='both',old=old,new=new,source_id=sid,reason=reason,kind='author_note_label',expected_count=1))
 records.append(dict(record_type='typography_observation',page=p,source_id=sid,verdict='not applied and now applied',printed_reading=geometry,image=f'scan/SGA6_scan_360dpi.pdf#page={p+14}',region=region,reason=reason,change={'old':old,'new':new,'label_key':label},forms='French diplomatic, corrected and reading; same explicit author marks in English'))
save('extra_patches.json',patches);save('extra_decisions.json',records)
