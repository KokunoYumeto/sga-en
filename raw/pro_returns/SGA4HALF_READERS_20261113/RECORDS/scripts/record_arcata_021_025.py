from audit_support import *
reasons={
63:'PDF p.26 category-equivalence sentence prints et celle, not est celle; Codex already agrees.',
64:"PDF p.26 (2.4) visibly reads à la puissance; restore the article still missing in Codex.",
65:'PDF p.26 (2.4) prints n-ième with grave accent; Codex already agrees.',
66:'PDF p.26 paragraph before Kummer has mu_n, matching the preceding definition; Codex already agrees.',
67:'PDF p.26 first formula of the Kummer proof has an asterisk on O_U; restore it in all forms, consistently with p.20.',
68:'PDF p.26 Kummer proof prints au-dessus; Codex already agrees.',
69:"PDF p.26 final words are d'où le résultat, with article le; Codex already agrees.",
70:'PDF p.27 (3.1) prints point géométrique without terminal e on point; Codex already agrees.',
71:'PDF p.27 (3.1) prints sous-entendant; Codex already agrees.',
72:'PDF p.27 strict-localization definition has localisé strict; Codex already agrees.',
73:'PDF p.27 after the direct limit explicitly prints étant prise sur; Codex still omits prise.',
74:'PDF p.27 (3.2) ends the stalk definition with neighbourhoods of barred x, not X; Codex already agrees.',
75:'PDF p.27 stalk criterion has the acute accent on épi; Codex already agrees.',
76:'PDF p.27 criterion says des homomorphismes for the induced stalk maps; Codex still shortens this to morphismes.',
77:'PDF p.27 visibly has singular induit after plural homomorphismes. Correct the agreement only in corrected/reading; English induced is unchanged.',
78:'PDF p.27 reads sur les fibres en tout point, not et tout; Codex already agrees.',
79:'PDF p.27 reads points rationnels in the masculine plural; Codex already agrees.',
80:'PDF p.28 second paragraph has localisé strict; Codex already agrees.',
81:'PDF p.28 after F(U-tilde) reads la limite inductive; Codex already agrees.',
82:'PDF p.28 immediately before Leray prints composé with acute accent; Codex already agrees.',
83:'PDF p.29 corollary (3.5) uses the direct image f_* inside R^p g_*; it is lowercase f, not script F. Codex already agrees.',
84:'PDF p.29 proof of (3.6) prints point géométrique without extra e; Codex already agrees.',
85:'PDF p.29 first proof paragraph introduces barred y but then prints en y without the bar. Strict localization depends on the chosen geometric point, so retain y diplomatically and restore barred y only in corrected/reading. Codex diplomatic has silently supplied the bar.',
86:'PDF p.29 exact global-sections functor uses a centred dot argument, not a dash. Restore the printed sign in all forms.',
87:'PDF p.29 final sentence visibly includes une before clôture; Codex already agrees.',
88:'PDF p.30 first sentence reads une clôture séparable; Codex already agrees.',
89:'PDF p.30 first paragraph splits poly-/nome without a circumflex. The 600-dpi crop confirms no accent over o. Keep polynome diplomatically; correct French spelling in corrected/reading; English polynomial does not vary.',
90:'PDF p.30 inverse-functor description prints correspondant à A, with A visible before the semicolon; Codex already agrees.'}
decide('arcata',{n:('accepted',r) for n,r in reasons.items()})
starts={21:r'\item la notion de faisceau inversible',22:r'\subsection{Fibres, images directes.}',23:'Le foncteur\n$f_*',24:r'\begin{corollarydotdash}\label{I:2-3-5}',25:r'\subsubsection{}\label{I:2-4-2}'}
append_jsonl(ROOT/'work/arcata/pages.jsonl',[{'printed_page':str(p),'pdf_page':INDEX[str(p)]['pdf_page'],'checked_against_scan':True,'findings':sum(r['printed_page']==str(p) for r in SOL),'start_fr':a,'start_en':'Corresponding translated item or paragraph/display','reason':'Every line and formula compared directly with the scan, including diagrams and page boundaries. Page25 ends before its cohomology formula, which belongs to page26.'} for p,a in starts.items()])
append_jsonl(ROOT/'work/arcata/variants.jsonl',[
{'id':'SGA45-CORR-0008','sources':['SGA45-CORR-0008','S45-SOL-0077'],'page':'22','place':'stalk criterion','printed':'induit','corrected':'induits','kind':'word','reason':'Plural homomorphismes governs the participle.','english_applicability':'No English change.'},
{'id':'S45-SOL-0085','page':'24','place':'strict localization in proof (3.6)','printed':'y','corrected':r'\bar y','kind':'symbol','reason':'Strict localization is at the chosen geometric point.','en_printed':'y','en_corrected':r'\bar y'},
{'id':'S45-SOL-0089','page':'25','place':'polynomial roots','printed':'polynome','corrected':'polynôme','kind':'accent','reason':'Circumflex missing in the printed spelling.','english_applicability':'No English change.'}
])
append_jsonl(ROOT/'work/arcata/own_findings.jsonl',[
{'id':'S45-ASTRA-A-0007','page':'21','place':'Kummer proof opening','printed_reading':'Soient U→X un morphisme étale et a∈G_m(U)','tex_reading':'Codex corrected has Soit','change':'Retain printed Soient in all forms; reverse SGA45-CORR-0007','kind':'editorial correction rejected','reason':'The plural verb governs two data, the morphism U→X and the element a; the construction is grammatical.'},
{'id':'S45-ASTRA-A-0008','page':'23','place':'injective preservation sentence','printed_reading':'transforme donc faisceau injectif en faisceau injectif','tex_reading':'Codex corrected adds two indefinite articles','change':'Retain printed generic construction in all forms; reverse SGA45-CORR-0009','kind':'editorial correction rejected','reason':'The abbreviated generic mathematical construction is intelligible and has no missing mathematical content; adding articles is stylistic editing, not a certain misprint repair.'},
{'id':'S45-ASTRA-A-0009','page':'23','place':'first formula, domain/codomain of f_*','printed_reading':'Faisc. Ab./X_et → Faisc. Ab./Y_et','tex_reading':r'\sh(\et X)\to \sh(\et Y)','change':r'Use \sh_{\mathrm{Ab}}(\et X)\to\sh_{\mathrm{Ab}}(\et Y) in both languages and all forms','kind':'missing','reason':'The scan explicitly restricts to abelian sheaves at the passage to derived functors. Unqualified sh loses that distinction; the added Ab subscript preserves Miller’s operator while restoring content.'}
])
print('Arcata pp.21–25 recorded.')
