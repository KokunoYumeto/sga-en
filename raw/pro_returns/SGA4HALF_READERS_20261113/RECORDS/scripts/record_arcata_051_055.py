from audit_support import *
reasons={
161:'PDF p.56 analytic notation is the bare superscript an, without a parenthesized dash. Codex an{} prints that notation; retain it in all forms.',
162:'PDF p.56 proof (6.3) has changement de base; Codex already agrees.',
163:'PDF p.56 theorem (6.4) prints H^q, consistent with q>dim(X); Codex already agrees.',
164:'PDF p.56 reference after (6.4) reads renvoyons; Codex already agrees.',
165:'PDF p.57 first paragraph has segment de droite, with final e; Codex already agrees.',
166:'PDF p.57 after the first inclusion has on peut pousser; Codex already agrees.',
167:'PDF p.57 calls X_0 la fibre spéciale; Codex already agrees.',
168:'PDF p.58 after the fibre formula has dès with grave accent; Codex already agrees.',
169:'PDF p.58 chapter description includes et pour la cohomologie étale; Codex already restores the conjunction.',
170:'PDF p.58 chapter description says Le paragraphe; Codex already agrees.',
171:'PDF p.58 parenthesis describes cohomology as localement constante; Codex already agrees.',
172:'PDF p.58 last paragraph gives the printed reference (II 3.1.); retain that explicit surface and Miller’s target label, as Codex does.',
173:'PDF p.59 notation (1.1) says localisé strict; Codex already agrees.',
174:'PDF p.59 definition (1.3) places x au-dessus de s; Codex already agrees.',
175:'PDF p.59 reduced-cohomology display is tagged (1.3.1), without chapter prefix; Codex already restores it, keeping the stable label.',
176:'PDF p.59 H^0 expression after i.e. visibly lacks the tilde on X. The defined vanishing-cycle variety and adjacent H^q expression have a tilde; correct it only in corrected/reading, agreeing with Codex SGA45-CORR-0019.',
177:'PDF p.59 proof (1.4) says toute variété; Codex already agrees.',
178:'PDF p.60 second Cartesian diagram labels the top-left horizontal map i-prime; Codex already agrees.',
179:'PDF p.60 after fournit has i-prime_* Z/n = Z/n. Restore that exact equality, including its right-hand constant sheaf. Codex instead expands the right side to f-prime^* i_* Z/n; this equivalent expression is not printed and is removed in all forms.',
180:'PDF p.60 final expression is X_s=X times_S s; Codex already agrees.'}
decide('arcata',{n:('accepted',r) for n,r in reasons.items()})
starts={51:r'\begin{theoremdotdash}[comparaison avec la cohomologie classique]',52:r'\section{Acyclicité locale des morphismes lisses}',53:r'\cosp^* : \h^*(X_t,\dZ)',54:r'\subsection{Morphismes localement acycliques.}',55:'Cartesian diagram of X_t → X over t → S'}
append_jsonl(ROOT/'work/arcata/pages.jsonl',[{'printed_page':str(p),'pdf_page':INDEX[str(p)]['pdf_page'],'checked_against_scan':True,'findings':sum(r['printed_page']==str(p) for r in SOL),'start_fr':a,'start_en':'Corresponding translated heading or formula','reason':'Entire scan page checked; enlarged crop resolves foncteur on p51. The cosp-specialization composite begins p53, and the first Cartesian diagram of (1.5) begins p55.'} for p,a in starts.items()])
append_jsonl(ROOT/'work/arcata/variants.jsonl',[
{'id':'SGA45-CORR-0019','sources':['SGA45-CORR-0019','S45-SOL-0176'],'page':'54','place':'H^0 after (1.3.1)','printed':'X_t^x','corrected':r'\widetilde X_t^x','kind':'symbol','reason':'The expression concerns the vanishing-cycle variety already defined with a tilde.','en_printed':'X_t^x','en_corrected':r'\widetilde X_t^x'}])
append_jsonl(ROOT/'work/arcata/own_findings.jsonl',[
{'id':'S45-ASTRA-A-0016','page':'51','place':'Theorem (6.3), direct-image functor','printed_reading':'foncteur image directe','tex_reading':'Codex record SGA45-CORR-0016 claims facteur is printed; delivered diplomatic component has foncteur','change':'Keep foncteur in every form, without apparatus','kind':'editorial classification','reason':'The high-resolution crop unambiguously reads foncteur; this is not a misprint of the book.'},
{'id':'S45-ASTRA-A-0017','page':'55','place':'Proof (1.5), equality after fournit','printed_reading':r"i'_*\dZ/n=\dZ/n",'tex_reading':r"i'_*\dZ/n={f'}^*i_*\dZ/n",'change':'Restore the printed constant sheaf on the right in all forms; linked to S45-SOL-0179','kind':'extra','reason':'Codex’s equivalent expansion changes the actual formula; the required diplomatic content is the shorter printed expression.'},
{'id':'S45-ASTRA-A-0018','page':'54','place':'Definition (1.3), comma after si','printed_reading':'si, la cohomologie','tex_reading':'Codex corrected removes the comma under SGA45-CORR-0018','change':'Retain printed comma in all forms','kind':'editorial correction rejected','reason':'The intrusive comma does not alter the mathematical meaning. Under NOTE_45 punctuation is an error only when it changes meaning; no semantic correction is warranted.'},
{'id':'S45-ASTRA-A-0019','page':'54–55','place':'Etant at (1.1) and (1.6)','printed_reading':'Etant donnés','tex_reading':'Codex treats Étant as corrected-only, SGA45-CORR-0017 and SGA45-CORR-0020','change':'Use modern capital accent consistently as shared typography; no apparatus variant','kind':'editorial classification','reason':'NOTE_45 explicitly permits modern accents on capitals as Miller’s form; this is typography, not a change of content.'}])
print('Arcata pp.51–55 recorded.')
