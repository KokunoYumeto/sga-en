from audit_support import *
reasons={
227:'PDF p.71 opening sentence clearly prints une variété; restore the missing e in every form.',
228:'PDF p.71 item B defines U_a with first index i_0. Codex diplomatic already has this reading.',
229:'PDF pp.71 and74 use an asterisk for the generic cohomological degree in all three cited places. Restore that visible symbol in both languages; this is not a change of macro for the same sign.',
230:'PDF p.72 after formula (3) has Poincaré with the final accent.',
231:'PDF p.72 item b reads variété.',
232:'PDF p.72 item b reads pour lesquels.',
233:'PDF p.72 uses the French open-interval notation ]0,1[. Restore the printed brackets without changing their meaning.',
234:'PDF p.72 last line reads deuxième.',
235:'PDF p.73 after (5′) has the letter H, referring to the cohomology operator.',
236:'PDF p.73 defines the complement by a minus sign, not setminus.',
237:'PDF p.73 display for the disconnected curve has an isomorphism sign, not equality.',
238:'PDF p.74 first proof sentence separates S from les cohomologies with a comma.',
239:'PDF p.74 specialization paragraph spells caractéristique without h.',
240:'PDF p.74 trace identification includes the article in l’intégration.',
241:'PDF p.74 last proof paragraph reads i=0 ou 2; restore the printed alternative.',
242:'PDF p.74 last paragraph reads au conducteur.',
243:'PDF p.75 item a labels the homomorphism by x↦x^n, not merely n.',
244:'PDF p.75 prints corps de classe, with singular classe. Retain it diplomatically and restore the final s of the mathematical term corps de classes only in the corrected French forms. The English term class field theory is unchanged.',
245:'PDF p.75 juxtaposes the references (2.3.1) (2.3.2) without et; remove the added conjunction.',
246:'PDF p.75 numbers the formula (2.3.3). The proposed 6.2.3.3 retains an unprinted section prefix; use exactly 2.3.3 while keeping Miller’s label I:eq:6-2-3-3.',
247:'PDF p.75 contains the complete sentence Cette compatibilité est prouvée en (Dualité, 3.2.4). Restore it and its reference in both languages.',
248:'PDF p.75 begins §3 with plural Soient although only X is introduced. Keep the printed plural diplomatically and use singular Soit in corrected French. English Let has no corresponding inflection change.',
249:'PDF p.75 §3 opening says une variété; restore the missing e in every form.',
250:'PDF p.75 last paragraph says du cas des courbes, without r.'}
choices={n:('accepted',r) for n,r in reasons.items()}
choices[246]=('accepted with a corrected reading',reasons[246],{'fix_new':r'\tag{2.3.3}','change_made':r'\tag{2.3.3}','printed_reading':'(2.3.3)'})
decide('arcata',choices)
starts={66:r'\section{Dualité de Poincaré}',67:r'\begin{equation}\label{I:eq:6-3}',68:r'\begin{equation}\label{I:eq:6-5\x27}',69:r'\begin{theorem}\label{I:6-2-2}',70:'a) La suite exacte'}
starts[68]=r"\begin{equation}\label{I:eq:6-5'}"
append_jsonl(ROOT/'work/arcata/pages.jsonl',[{'printed_page':str(p),'pdf_page':INDEX[str(p)]['pdf_page'],'checked_against_scan':True,'findings':sum(r['printed_page']==str(p) for r in SOL),'start_fr':a,'start_en':'Corresponding translated heading, paragraph or formula','reason':'All text, formulas and diagrams compared directly with the scan. The automatic slices spill: p67 starts at formula (3), p68 at (5′), p69 at theorem (2.2), and p70 at item a.'} for p,a in starts.items()])
append_jsonl(ROOT/'work/arcata/variants.jsonl',[
{'id':'S45-SOL-0244','page':'70','place':'geometric class field theory','printed':'corps de classe géométrique','corrected':'corps de classes géométrique','kind':'word','reason':'The established French mathematical term is corps de classes; the final s is missing.','en_printed':'','en_corrected':''},
{'id':'S45-SOL-0248','page':'70','place':'opening of VI §3','printed':r'Soient $X$ une variété','corrected':r'Soit $X$ une variété','kind':'word','reason':'Only one object X is introduced, so the introductory verb must be singular.','en_printed':'','en_corrected':''}])
append_jsonl(ROOT/'work/arcata/own_findings.jsonl',[
{'id':'S45-ASTRA-A-0026','page':'70','place':'formula tags (2.3.1) and (2.3.2)','printed_reading':'(2.3.1), (2.3.2)','tex_reading':'(6.2.3.1), (6.2.3.2)','change':'Use the printed numbers with the existing Miller labels in all forms','kind':'number','reason':'The print has no leading 6 in these two formula numbers. Sol0246 separately covers (2.3.3).'}])
print('Arcata pp.66–70 recorded.')
