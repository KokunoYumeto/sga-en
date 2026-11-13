from audit_support import *
reasons={
147:"PDF p.51 Artin–Schreier sentence prints qu’on a; Codex already agrees.",
148:'PDF p.52 divisor proof prints une section; Codex already agrees.',
149:'PDF p.52 (5.1) prints the inline H_c^q(X,F) and en posant before the defining display. Codex still omits both; restore them in all forms.',
150:'PDF p.53 after (5.2) reads que le lemme suffit; Codex already agrees.',
151:'PDF p.54 proof continuation says p est un isomorphisme; Codex already agrees.',
152:'PDF p.54 (5.3) prints une immersion ouverte; Codex already agrees.',
153:'PDF p.54 has no isolated s after images directes; Codex already removes it.',
154:'PDF p.54 defining display visibly omits F from R^q f_! on the left, although its right side is evaluated at F. Preserve the omitted argument diplomatically and supply F in corrected/reading.',
155:'PDF p.54 defining display has unbarred f on the right. Its argument j_!F lives on barred X, so direct image must be along barred f; correct only in corrected/reading, agreeing with Codex SGA45-CORR-0014.',
156:'PDF p.54 sentence before (5.4.1) prints isomorphisme; Codex already agrees.',
157:'PDF p.55 proof (6.1) prints une suite exacte; Codex already agrees.',
158:'PDF p.55 reference to III.3.6 includes cf.; Codex already restores it.',
159:'PDF p.55 proof (6.2) begins Pour démontrer; Codex already agrees.',
160:'PDF p.55 proof (6.2) prints où with grave accent; Codex already agrees.'}
decide('arcata',{n:('accepted',r) for n,r in reasons.items()})
starts={46:r"que $n$ est une puissance d’un nombre premier",47:r'tel point, $t_0\in\sO_{X_0,x}$',48:'Montrons que cette définition',49:'le théorème de changement de base',50:r'\subsection{Applications.}'}
append_jsonl(ROOT/'work/arcata/pages.jsonl',[{'printed_page':str(p),'pdf_page':INDEX[str(p)]['pdf_page'],'checked_against_scan':True,'findings':sum(r['printed_page']==str(p) for r in SOL),'start_fr':a,'start_en':'Corresponding translated passage','reason':'Every paragraph and diagram read directly from the scan. The duplicated le spans pp48/49 and is represented by a variant at the beginning of p49. Formula (5.4.1) remains wholly on p49.'} for p,a in starts.items()])
append_jsonl(ROOT/'work/arcata/variants.jsonl',[
{'id':'SGA45-CORR-0015','sources':['SGA45-CORR-0015','S45-ASTRA-A-0015'],'page':'49','place':'first word, duplicated article across pp48/49','printed':'le ','corrected':'','kind':'extra','reason':'The preceding page already ends with le; remove only the duplicated article in corrected/reading.','en_printed':'the ','en_corrected':''},
{'id':'S45-SOL-0154','page':'49','place':'(5.3), left-hand argument','printed':r'\eR^q f_!','corrected':r'\eR^q f_! \sF','kind':'missing','reason':'The displayed equality defines the value at F.','en_printed':r'\eR^q f_!','en_corrected':r'\eR^q f_! \sF'},
{'id':'SGA45-CORR-0014','sources':['SGA45-CORR-0014','S45-SOL-0155'],'page':'49','place':'(5.3), right-hand direct image','printed':r'\eR^q f_*(j_! \sF)','corrected':r'\eR^q \bar f_*(j_! \sF)','kind':'symbol','reason':'The argument is a sheaf on the compactification, whose map is barred f.','en_printed':r'\eR^q f_*(j_! \sF)','en_corrected':r'\eR^q \bar f_*(j_! \sF)'}])
append_jsonl(ROOT/'work/arcata/own_findings.jsonl',[
{'id':'S45-ASTRA-A-0015','page':'49','place':'page48 last line / page49 first line','printed_reading':'en utilisant le / le théorème','tex_reading':'Codex diplomatic keeps le le; corrected removes one, SGA45-CORR-0015','change':'Keep both diplomatically; remove the second in corrected/reading with an apparatus entry','kind':'misprint_in_print','reason':'The scan prints the same article on both sides of the page break. It is an accidental repetition, not a grammatical alternative.'}])
print('Arcata pp.46–50 recorded.')
