from pathlib import Path
import sys,json
sys.path.insert(0,str(Path(__file__).parent))
from audit_support import *
W=ROOT/'work/arcata'
decide('arcata',{
1:('accepted','PDF p.3, paragraph beginning Le Rapport: complète is split complè-/te; accent grave and final unaccented e are visible. Codex already restored it.',{'codex_ids':['SGA45-TX-0003']}),
2:('accepted',"PDF p.3, Rapport paragraph: à l'utilisateur visibly includes the elided article. Codex already restored it.",{'codex_ids':['SGA45-TX-0004']}),
3:('accepted','PDF p.3 prints singular digression, followed by plural certaines très intéressantes; retain the singular in diplomatic and correct the agreement in corrected/reading.',{'codex_ids':['SGA45-CORR-0001']}),
4:('accepted','PDF p.3, Cycle paragraph: cette classe has no final s; the singular agrees with cette. Codex already restored it.',{'codex_ids':['SGA45-TX-0005']}),
5:('accepted',"PDF p.4, first paragraph, far-right end of line 2: a damaged remnant follows étaien. A 600-dpi crop (page coordinates 350,65–440,88 points) confirms the broken terminal stroke, not a colon. The plural subject Elles and the compound tense uniquely support étaient. Codex's decision SGA45-TX-0006 says étaient, but its supplied diplomatic file actually ends at étaien; restore the full verb in every French form.",{'codex_ids':['SGA45-TX-0006'],'region':'first paragraph, line 2, right edge; PDF crop (350,65,440,88) points'})})
own=[
{'id':'S45-ASTRA-A-0001','page':'IV','place':'sga4.5-intro.tex, étaien devenues','printed_reading':'étaient (terminal stroke damaged)','tex_reading':'étaien','change':'étaien → étaient in all French forms','kind':'word','reason':'Damaged t recoverable from residual stroke and Elles ... devenues; Codex record and delivered file disagree. See S45-SOL-0005.'},
{'id':'S45-ASTRA-A-0002','page':'2','place':"ariane.tex, une autre démonstration, elle complète",'printed_reading':'une autre démonstration, elle complète','tex_reading':'Codex corrected: une autre démonstration, complète','change':'Retain elle in all forms; reverse SGA45-CORR-0003','kind':'editorial correction rejected','reason':"The scan clearly prints elle. It is the ordinary contrastive detached pronoun: the other proof, this one complete, contrasts with the preceding conjectural establishment. It is grammatical, intentional in context, and is not a demonstrable misprint."},
{'id':'S45-ASTRA-A-0003','page':'1','place':'ariane.tex, second paragraph','printed_reading':'dimension cohomologiques','tex_reading':'dimension cohomologiques (diplomatic); dimension cohomologique (corrected)','change':'Retain plural only in diplomatic; singular adjective in corrected/reading','kind':'misprint_in_print','reason':'The scan visibly has cohomologiques; singular dimension governs singular adjective. Confirm SGA45-CORR-0002.'}
]
append_jsonl(W/'own_findings.jsonl',own)
starts={'III':r'\chapter*{Introduction}','IV':'Je remercie enfin','1':r'\markboth{}{}','2':'Les exposés XV et XVI','3':'et XIII, rédigés par I. Bucur'}
append_jsonl(W/'pages.jsonl',[{'printed_page':p,'pdf_page':INDEX[p]['pdf_page'],'checked_against_scan':True,'findings':sum(r['page']==p for r in own)+sum(r['printed_page']==p for r in SOL),'start_fr':starts[p],'start_en':{'III':r'\chapter*{Introduction}','IV':'Finally, I thank','1':"A thread of Ariadne",'2':'Exposés XV and XVI','3':'and XIII, written by I. Bucur'}[p],'reason':'Entire printed page compared visually with Codex diplomatic source; all words, references, formulas and bibliography entries checked. Miller form conventions retained.'} for p in starts])
append_jsonl(W/'variants.jsonl',[
{'id':'SGA45-CORR-0001','sources':['SGA45-CORR-0001','S45-SOL-0003'],'page':'III','place':'Introduction, Rapport paragraph','printed':'digression','corrected':'digressions','kind':'word','reason':'Plural series and certaines require digressions; print has singular.','en_printed':'digression','en_corrected':'digressions'},
{'id':'SGA45-CORR-0002','sources':['SGA45-CORR-0002','S45-ASTRA-A-0003'],'page':'1','place':'Ariane, second paragraph','printed':'cohomologiques','corrected':'cohomologique','kind':'word','reason':'Singular dimension requires a singular adjective.','en_printed':'','en_corrected':'','english_applicability':'No English variant: cohomological has no agreement inflection.'}
])
(W/'fr').mkdir(exist_ok=True);(W/'en').mkdir(exist_ok=True)
t=(SOURCE/'fr/codex_dip/sga4.5-intro.tex').read_text()
t=t.replace(r'\chapter*{Introduction}',r'\PrintPage{III}'+'\n'+r'\chapter*{Introduction}').replace('Je remercie enfin',r'\PrintPage{IV}'+'\nJe remercie enfin').replace('étaien devenues','étaient devenues').replace('série de digression,',r'série de \var{digression}{digressions}{SGA45-CORR-0001},')
(W/'fr/sga4.5-intro.tex').write_text(t)
t=(SOURCE/'en/sources/components/sga4half_intro_en.tex').read_text().replace(r'\chapter*{Introduction}',r'\PrintPage{III}'+'\n'+r'\chapter*{Introduction}').replace('Finally, I thank',r'\PrintPage{IV}'+'\nFinally, I thank').replace('series of digressions,',r'series of \var{digression}{digressions}{SGA45-CORR-0001},')
titles={'II':'Report on the trace formula','III':r'Functions $L$ modulo $\ell^n$ and modulo $p$','IV':'The cohomology class associated with a cycle','V':'Duality','VI':'Applications of the trace formula to trigonometric sums','VII':r'Finiteness theorems in $\ell$-adic cohomology','VIII':'Derived categories (State 0)'}
for k,v in titles.items():t=t.replace(r'\nameref{'+k+'}',r'\hyperref['+k+']{'+v+'}')
(W/'en/sga4half_intro_en.tex').write_text(t)
t=(SOURCE/'fr/codex_dip/ariane.tex').read_text().replace(r'\markboth{}{}',r'\PrintPage{1}'+'\n'+r'\markboth{}{}').replace('cohomologiques,',r'\var{cohomologiques}{cohomologique}{SGA45-CORR-0002},').replace('\\newpage\n\nLes exposés XV',r'\PrintPage{2}'+'\n\nLes exposés XV').replace('\\newpage\n\net XIII',r'\PrintPage{3}'+'\n\net XIII')
(W/'fr/ariane.tex').write_text(t)
print('Recorded opening: 5 scanned pages; 5 Sol decisions; 3 own findings; 2 print variants.')
