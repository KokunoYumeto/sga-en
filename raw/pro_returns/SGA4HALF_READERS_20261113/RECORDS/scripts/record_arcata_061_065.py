from audit_support import *
reasons={
207:'PDF p.66 item d) reads Le complément; Codex already agrees.',
208:'PDF p.66 item e) reads au-dessus; Codex already agrees.',
209:'PDF p.66 defines X-hat by the ring A[[T]] although the next sentence calls it a scheme and uses base change. Supply Spec only in corrected/reading; keep the printed omission diplomatically.',
210:'PDF p.66 final inverse limit visibly has V_m; Codex already restores the subscript.',
211:'PDF p.67 final sentence includes morphismes propres; Codex already restores the missing noun.',
212:'PDF p.68 proof (3.2) has a comma after X, not a less-than symbol; Codex already agrees.',
213:'PDF p.68 proof (3.2) reads au cas où; Codex already agrees.',
214:'PDF p.68 second proof paragraph has a comma after X, not a less-than symbol; Codex already agrees.',
215:'PDF p.68 corollary (3.3) spells caractéristique without h; Codex already agrees.',
216:'PDF p.69 theorem (3.4) spells caractéristiques without h; Codex already agrees.',
217:'PDF p.69 after the second diagram prints T=A_S^{n−1}, lowercase n. The relative dimension is N while n is the coefficient modulus; correct the dimension exponent only in corrected/reading.',
218:'PDF p.69 application to g has the direct-image star; Codex already restores it.',
219:'PDF p.69 support assertion says the R^q j_* Z/n are concentrated on i(T), without an equals-zero clause; Codex already removes that added assertion.',
220:'PDF p.70 conclusion under the spectral sequence has q≥2; Codex already agrees.',
221:'PDF p.70 extension-by-zero sheaf is R^1 j_* Z/n; Codex already agrees.',
222:'PDF p.70 (3.5.1) has type fini without final e; Codex already agrees.',
223:'PDF p.70 comparison parenthesis reads supposer F constructible, with no est; Codex already agrees.',
224:'PDF p.70 (3.5.2) has caractéristique without h; Codex already agrees.',
225:'PDF p.70 final paragraph has caractéristique without h; Codex already agrees.',
226:'PDF p.70 after the Th. finitude reference has a comma before elle s’applique; Codex already restores the clause separator.'}
decide('arcata',{n:('accepted',r) for n,r in reasons.items()})
starts={61:'nous permettent de supposer que',62:'Par hypothèse, le complément de',63:r'\begin{theoremdotdash}[changement de base par un morphisme lisse]',64:'Diagram (3.4.1), U → X ← Y over S',65:r'$E_2^{pq} = \eR^p f_* \eR^q j_*\dZ/n'}
append_jsonl(ROOT/'work/arcata/pages.jsonl',[{'printed_page':str(p),'pdf_page':INDEX[str(p)]['pdf_page'],'checked_against_scan':True,'findings':sum(r['printed_page']==str(p) for r in SOL),'start_fr':a,'start_en':'Corresponding translated passage or diagram','reason':'All words, formulas, explicit tags and diagrams compared directly with the scan. Page61 begins in the final sentence of (2.3.3), page64 begins at the relative-purity diagram, and page65 begins at the spectral-sequence formula.'} for p,a in starts.items()])
append_jsonl(ROOT/'work/arcata/variants.jsonl',[
{'id':'S45-SOL-0209','page':'61','place':'completed base X-hat','printed':r'\widehat X=A\llbracket T\rrbracket','corrected':r'\widehat X=\spec A\llbracket T\rrbracket','kind':'missing','reason':'The completed base is a scheme; Spec is missing from the printed equality.','en_printed':r'\widehat X=A\llbracket T\rrbracket','en_corrected':r'\widehat X=\spec A\llbracket T\rrbracket'},
{'id':'S45-SOL-0217','page':'64','place':'base of local model in relative purity','printed':r'\dA_S^{n-1}','corrected':r'\dA_S^{N-1}','kind':'symbol','reason':'N is the relative dimension; n is the torsion modulus.','en_printed':r'\dA_S^{n-1}','en_corrected':r'\dA_S^{N-1}'}])
append_jsonl(ROOT/'work/arcata/own_findings.jsonl',[
{'id':'S45-ASTRA-A-0023','page':'61','place':'n-copies of V_0','printed_reading':'n-copies','tex_reading':'Codex corrected removes hyphen under SGA45-CORR-0022','change':'Keep printed hyphen in all French forms; English n copies is the ordinary translation','kind':'editorial correction rejected','reason':'The hyphen is unconventional typography but does not change the number or mathematical content. It does not require a corrected reading.'},
{'id':'S45-ASTRA-A-0024','page':'64','place':'four values of R^q f_* Z/n','printed_reading':r'\dZ/n,0,\dZ/n(-1),0\text{ pour }q>2','tex_reading':'Codex corrected expands to a four-row cases display with q=0,1,2,q>2','change':'Retain the printed sequential shorthand in all forms','kind':'editorial correction rejected','reason':'The sequence lists the degree0,1,2 values followed by zero for q>2; the cited formula IV6.2.1 makes that interpretation explicit. Expanding the shorthand is explanatory rewriting, not repair of a misprint.'},
{'id':'S45-ASTRA-A-0025','page':'65','place':'résolution,est','printed_reading':'résolution,est','tex_reading':'Codex corrected inserts a space under SGA45-CORR-0023','change':'Use normal comma spacing as shared typography; no apparatus variant','kind':'editorial classification','reason':'Interword spacing is part of the permitted modern typography, not a content correction.'}])
print('Arcata pp.61–65 recorded.')
