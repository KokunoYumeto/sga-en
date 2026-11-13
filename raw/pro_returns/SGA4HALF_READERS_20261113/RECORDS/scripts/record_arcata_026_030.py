from audit_support import *
reasons={
91:'PDF p.32 introduction clearly prints nuls, not nuis; Codex already agrees.',
92:'PDF p.32 definition (1.1)c prints à une algèbre; Codex already restores the article.',
93:'PDF p.32 final paragraph prints ont même dimension; Codex already agrees.',
94:"PDF p.33 (1.2) prints A_K without a prime, despite the extension K′ just introduced. Preserve that reading diplomatically and use A_{K′} in corrected/reading, since this is extension of scalars to K′.",
95:'PDF p.33 automorphism paragraph prints linéaire with i; Codex already agrees.',
96:'PDF p.33 the exact sequence is explicitly tagged (*). Codex restores it, retaining Miller’s label for references.',
97:'PDF p.34 proof (1.4) prints suite exacte; Codex already agrees.',
98:'PDF p.34 proof (1.4) prints on interprète; Codex already agrees.',
99:'PDF p.34 lemma (1.5) prints une extension finie; Codex already agrees.',
100:"PDF p.34 geometric bracket prints lowercase x′ in the left sheaf subscript; Codex already agrees.",
102:'PDF p.34 last prose paragraph prints le choix; Codex already agrees.',
103:'PDF p.35 cohomology diagram, upper-left quotient denominator, visibly prints barred lowercase k. The field is K throughout this proof; preserve k diplomatically and correct to K in corrected/reading. The earlier group diagram on the same printed page already has capital K.',
104:'PDF p.35 paragraph beginning La connaissance du groupe de Brauer appears between the cohomology diagram and (1.6); Codex already restores it completely.',
105:'PDF p.35 (1.6) visibly reads toute extension finie; Codex already agrees.',
106:'PDF p.35 square-bracketed reference names both Corps locaux and Cohomologie galoisienne. Restore both titles in all forms and retain Miller’s se94 citation key as source metadata through PrintCite; Codex already has both titles.'}
choices={n:('accepted',r) for n,r in reasons.items()}
choices[101]=('rejected',"A high-resolution crop of PDF p.34 (geometric bracket, both H^q expressions) shows the same lowercase x′ in both sheaf subscripts. The claimed uppercase X′ is not supported by the image. Keep lowercase x′ in all forms, agreeing with the Codex diplomatic reading.",{'printed_reading':r'\h^q(x,\pi_*\dG_{m,x\prime})','region':'PDF p.34, geometric bracket, 8x crop of points (65,450)–(270,475).'})
decide('arcata',choices)
starts={26:r'\h^q(\et X,\sF) = \h^q(G,\sF_{\bar K})',27:r'\section{Cohomologie des courbes.}',28:"d’équivalence. C’est ce groupe",29:r'\begin{propositiondotdash}\label{I:3-1-3}',30:'Group diagram with two exact rows beginning 1 → barred K*'}
append_jsonl(ROOT/'work/arcata/pages.jsonl',[{'printed_page':str(p),'pdf_page':INDEX[str(p)]['pdf_page'],'checked_against_scan':True,'findings':sum(r['printed_page']==str(p) for r in SOL),'start_fr':a,'start_en':'Corresponding translated passage or formula','reason':'All text, symbols, exact sequences and diagrams compared with the full scan; high-resolution crops resolve Künneth and the two x-prime subscripts. Page30 starts at the group diagram, not at the later cohomology diagram.'} for p,a in starts.items()])
append_jsonl(ROOT/'work/arcata/variants.jsonl',[
{'id':'S45-SOL-0094','page':'28','place':'(1.2), extension of scalars','printed':'A_K','corrected':"A_{K'}",'kind':'symbol','reason':'The indicated extension of scalars is to K′.','en_printed':'A_K','en_corrected':"A_{K'}"},
{'id':'S45-SOL-0103','page':'30','place':'cohomology diagram upper-left denominator','printed':r'\bar k^*','corrected':r'\bar K^*','kind':'symbol','reason':'The closure is that of K; lowercase k is undefined.','en_printed':r'\bar k^*','en_corrected':r'\bar K^*'}])
append_jsonl(ROOT/'work/arcata/own_findings.jsonl',[
{'id':'S45-ASTRA-A-0010','page':'27','place':'first paragraph, Künneth formula','printed_reading':'Künneth','tex_reading':'Kunneth in Codex diplomatic','change':'Restore Künneth in both languages and all forms','kind':'accent','reason':'The 8x crop of PDF p.32 shows two dots above the u. This is a transcription repair, not a misprint of the book.'}])
print('Arcata pp.26–30 recorded.')
