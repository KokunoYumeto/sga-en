from audit_support import *
decide('arcata',{
6:('accepted','PDF p.9 contains all three paragraphs below the byline, including the six Arcata lectures, seventh Rapport lecture, and quasi-compact/quasi-separated convention. Codex opening.tex already restores the passage; use that independently verified transcription, not a second insertion.'),
7:('accepted','PDF p.11 first paragraph visibly has plural théories; Codex already agrees.'),
8:('accepted','PDF p.11 first paragraph has feminine suivie; Codex already agrees.'),
9:('accepted','PDF p.11, after (§1,2,3), clearly reads on dégage; Codex already agrees.'),
10:('accepted','PDF p.11 first paragraph ends with descente fidèlement plate; Codex already agrees.'),
11:('accepted','PDF p.11 explicitly names théorème 90 de Hilbert; the numeral is content and is present in Codex.'),
12:('accepted','PDF p.11 second paragraph reads plus complète, with l between p and è; Codex already agrees.'),
13:('accepted','PDF p.11 gives exposés I à VI, including final I; Codex already agrees.'),
14:('accepted','PDF p.11 §1 reads à valeurs réelles, with s on valeurs; Codex already agrees.'),
15:('accepted','PDF p.11 final line reads tous les ouverts; Codex already agrees.'),
16:('accepted','PDF p.12 heading (2.2) reads Point, not Pointe; Codex already agrees.'),
17:('accepted','PDF p.13 equation below the first triangle has rho indexed U,W on the left, as on its horizontal arrow; Codex already agrees.'),
18:('accepted','PDF p.14 (3.3) begins Un fibré vectoriel; Codex already agrees.'),
19:('accepted','PDF p.14 (3.3) has a colon after E_U, introducing the defining restriction system; Codex already agrees.'),
20:('accepted','PDF p.14 (3.4) points to numbered paragraph 1 (Cribles), not Roman section I; retain the corrected label I:1-1 already used in Codex.'),
21:('accepted','PDF p.14 (3.4) explicitly assumes espace normal; its omission changes the hypothesis. Codex already restores it.'),
22:('accepted','PDF p.14 §4 title visibly ends plate; Codex already agrees.'),
23:('accepted',"PDF p.15 first paragraph has s'exprimer, including the apostrophe; Codex already agrees."),
24:('accepted','PDF p.15 bracketed definition unmistakably prints plat est surjectif. The definition requires conjunction et; retain est only in diplomatic.',{'codex_ids':['SGA45-CORR-0004']}),
25:('accepted','PDF p.15 proposition (4.2)(i) prints dès with grave accent; Codex already agrees.'),
26:('accepted','PDF p.15 proposition (4.2)(ii) prints dès with grave accent; Codex already agrees.'),
27:('accepted','PDF p.15 proof (ii) prints toute famille without finie. The asserted containment in a finitely generated submodule is false for an arbitrary infinite family (already with A=B and an infinite free module). The following finite-generation argument requires a finite family; insert finie only in corrected/reading.'),
28:('accepted',"PDF p.15 last paragraph has d'après with grave accent; Codex already agrees."),
29:('accepted','PDF p.15 last paragraph visibly prints the French word plat. Supplied Codex diplomatic still has flat; restore plat in every French form.')
})
starts={4:r'\chapter{Cohomologie étale',5:r'\begingroup',6:r'\section{Topologies de Grothendieck.}',7:'Etant donnée une famille',8:r'\item un fibré vectoriel $E_U$',9:r'isomorphisme $\rho_{y x}',10:'De ce point de vue, les techniques'}
append_jsonl(ROOT/'work/arcata/pages.jsonl',[{'printed_page':str(p),'pdf_page':INDEX[str(p)]['pdf_page'],'checked_against_scan':True,'findings':sum(r['printed_page']==str(p) for r in SOL),'start_fr':a,'start_en':'Align with the same paragraph/item; see annotated English component','reason':'Full page, including diagrams and all labels/indices, compared visually with diplomatic text. Automatic spans include neighbouring text; boundary is the stated exact anchor. Miller typography conventions retained.'} for p,a in starts.items()])
append_jsonl(ROOT/'work/arcata/variants.jsonl',[
{'id':'SGA45-CORR-0004','sources':['SGA45-CORR-0004','S45-SOL-0024'],'page':'10','place':'faithfully flat definition','printed':'plat est surjectif','corrected':'plat et surjectif','kind':'word','reason':'The printed est is a typographical substitution for conjunction et.','en_printed':'flat is surjective','en_corrected':'flat and surjective'},
{'id':'S45-SOL-0027','page':'10','place':'proof of (4.2)(ii)','printed':'Pour toute famille','corrected':'Pour toute famille finie','kind':'missing','reason':'The containment claim is valid for finite families; for infinite families it fails in an infinite free module.','en_printed':'For any family','en_corrected':'For any finite family'}
])
print('Arcata pp.4–10 recorded.')
