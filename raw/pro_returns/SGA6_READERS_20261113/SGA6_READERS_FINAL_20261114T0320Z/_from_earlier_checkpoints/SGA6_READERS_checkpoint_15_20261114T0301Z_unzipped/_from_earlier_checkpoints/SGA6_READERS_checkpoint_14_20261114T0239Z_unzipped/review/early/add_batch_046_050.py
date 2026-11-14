"""One-shot record of directly read pp.46–50; witness60/61 for ellipses."""
from pathlib import Path
import json
R=Path(__file__).resolve().parents[2];O=Path(__file__).resolve().parent
def load(n):return json.loads((O/n).read_text())
def save(n,a):(O/n).write_text(json.dumps(a,ensure_ascii=False,indent=2)+'\n')
e={
1:['boundary pp45/46','The last printed syllable on p45 is algé- and the first on p46 is brique. The attached layers already split it as algé% / brique.'],
2:['unnumbered two-sum display','The overbar extends over the complete F|U_i and F|U_i∩U_j, and U lies on the baseline after the full-height restriction bar. The attached overline scopes and baseline restrictions match.'],
3:['unnumbered display ending','There is no terminal comma. The attached layers already omit it.'],
4:['Comme F-bar|U=F','The bar covers only F; U is on the baseline after the vertical restriction stroke. The attached formula matches.'],
5:['qui engendrent F-bar|U','Again the bar is on F alone and U is on the baseline. The attached formula matches.'],
6:['Supposons maintenant X quasi-projective non singulière','The underline includes both non and singulière. The attached emphasis now includes non.'],
7:['Corollary2, fonctions addtives f','The first occurrence lacks the i after d; the nearby fonctions additives g has the complete word. Current already restores additives.'],
8:['boundary pp47/48','Page47 ends Comme K(ξ(X)) est; p48 starts non seulement. The attached marker correctly precedes non.'],
9:['definition of the class of F','The character inside γ(Γ) has the single top bar and vertical stem of capital Gamma. The preceding F in the sentence has the usual middle stroke. Diplomatic preserves Gamma; current correctly restores the named sheaf F.'],
10:['last paragraph, non singulière','The underline is continuous under non singulière. The attached emphasis includes both words.'],
11:['boundary pp48/49','Page48 ends des développements; page49 begins du début du §2, on définit. The attached marker now precedes du début.'],
12:['formula(2.15), ending','The last parenthesis has no following comma. The attached display matches.'],
13:['formula(2.16), product ellipsis','There are four baseline full stops between γ(F_1) and γ(F_p), directly confirmed in native witness60. The attached four-stop sequence preserves the glyph count and baseline. The right-side argument ellipsis has three dots between commas.'],
14:['formula(2.16), ending','There is no terminal comma after the last parenthesis. The attached display matches.'],
15:['Tor simultanés in quotation marks','The word Tor inside the quotes is underlined, like Tor_i immediately before it. The nearby Tor multiples and formule des Tor are plain. The attached local underline is correct.'],
16:['homomorphisme canonique de K(ξ(X)','Only one closing parenthesis follows X in the print. Current already adds the missing closing parenthesis to K(ξ(X)); diplomatic keeps the omission.'],
17:['paragraph after(2.18)','On fera attention begins with the ordinary paragraph indent. The attached blank line produces that paragraph boundary; no new content variant is made.'],
18:['definition of ε(s)','The word signature has a single underline. The attached emphasis matches.'],
19:['n’est pas de caractéristique ≠0','The print includes both n’est pas and ≠0. The immediately preceding clause limits the direct construction to characteristic0; the stated obstacle therefore concerns the complement of characteristic0. Removing the inequality sign yields n’est pas de caractéristique0 and retains the printed negation. Current still needs that correction.'],
20:['Theorem2.8, corps k de caractéristique0','The underline ends after corps and resumes at Soit F; the intervening words and characteristic0 are plain. The attached split matches.'],
21:['N.B. paragraph after(2.19)','N.B. starts at the normal paragraph indent, confirmed in native witness61. The attached blank line preserves the new paragraph.'],
22:['N.B., Tor_i(F,..,F)','Native witness61 distinctly shows two dots between commas, while display(2.19) has three dots. Diplomatic already preserves the two-dot reading and current the three-dot ellipsis.']}
save('evidence_046_050.json',{'findings_046_050.json':e})
patches=load('extra_patches.json')
patches.append(dict(page=50,layer='current',old=r"n'est pas de caractéristique $\neq0$",new="n'est pas de caractéristique $0$",source_id='fixes/MISPRINTS_6.json#82',reason=e[19][1],kind='misprint_correction',expected_count=1))
for p,n in [(46,1),(47,3),(48,2),(49,1)]:patches.append(dict(page=p,layer='both',old=r'\cO',new=r'\underline{O}',source_id='ASTRA-EARLY-TYPE-005',reason='All structure-sheaf O glyphs on this inspected page are typed O with an underline; use the explicit observed form without redefining a macro elsewhere.',kind='font',expected_count=n))
save('extra_patches.json',patches)
records=load('extra_decisions.json')
def rec(typ,p,sid,pr,region,reason,change,**kw):records.append(dict(record_type=typ,page=p,source_id=sid,verdict='confirmed',printed_reading=pr,image=f'scan/SGA6_scan_360dpi.pdf#page={p+14}',region=region,reason=reason,change=change,forms='French diplomatic and corrected; English where meaning or notation is affected',**kw))
rec('hold_difference',46,'fr/codex/HOLD_VS_CORR.json#33','fonctions addtives f','Corollary2 to Theorem2.3',e[7][1],{'hold':'addtives','current':'additives'})
rec('typography_observation',46,'ASTRA-EARLY-TYPE-005','underlined O_X,O_Y and O_X(E)','structure-sheaf symbols pp46–49','Directly viewed locations: Γ(V,O_X) on p46; three O_X(E)/O_X(E_i) on p47; two O_Y on p48; γ(O_X) on p49. Each O is a typed letter with its own underline. Apply explicit underline{O} at these seven occurrences in both layers, continuing the observed convention of pp44–45.',{'mapping':r'\cO → \underline{O}','counts':{'46':1,'47':3,'48':2,'49':1}},related_pages=[46,47,48,49])
rec('typography_observation',50,'ASTRA-EARLY-TYPE-006','(*)','author note call and label','Both the call after réduit à0 and the label before Non are literal parenthesized stars at the baseline. The note text, including the reference XIV4.7, was read in both the primary and native witness61.','Preserve this explicit author-note mark.',witness_image='scan/SGA6_witness_300dpi.djvu#page=61')
save('extra_decisions.json',records)
pages=load('extra_pages.json');f=json.loads((R/'check/findings/findings_046_050.json').read_text())
beg={46:'brique sur X',47:'formula(2.14)',48:'non seulement',49:'du début du §2',50:'formula(2.18)'}
for p in range(46,51):pages.append(dict(page=p,pdf_page=p+14,fully_checked=True,main_scan_viewed='four overlapping horizontal strips',witness_viewed=p in [49,50],findings_count=sum(z['page']==p for z in f),begins=beg[p],notes='All prose, formulas and p50 author note directly compared. Native witness60/61 additionally examined for ellipsis glyph counts and p50 note.'))
save('extra_pages.json',pages)
