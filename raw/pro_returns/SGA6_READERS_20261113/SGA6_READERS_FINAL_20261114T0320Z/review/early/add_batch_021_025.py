"""Persist direct image comparisons for appendix pp.21–25."""
from pathlib import Path
import json
R=Path(__file__).resolve().parents[2];O=Path(__file__).resolve().parent
def load(n):return json.loads((O/n).read_text())
def save(n,a):(O/n).write_text(json.dumps(a,ensure_ascii=False,indent=2)+'\n')
e={
1:['centered title below CHAPITRE I','Only Anneaux is underlined; lambda and the hyphen are outside the rule. The task accepts heading typography changes; retain the attached title with the identical word and mathematical tokens.'],
2:['§1 heading','Définitions is visibly underlined. The latest NOTE_6 expressly accepts subsection titles without underline; retain the current heading under that convention.'],
3:['Posons, pour tout x∈K','No comma follows K before (1.3). The attached layers have removed it.'],
4:['end of paragraph after (1.3)','The map 1+Σx_i t^i→x_1 continues the same text line as nique; the attached inline expression preserves this.'],
5:['footnote, cf V2.4','The print has cf with no following stop. The attached transcription matches.'],
6:['boundary pp21/22','Page21 ends telle que, while page22 starts formula(1.4), λ_t(1)=1+t. The attached marker is correctly before that display.'],
7:['De même, les λ^i(f)','De même begins at the ordinary left margin with no new paragraph indent; the attached join matches.'],
8:['boundary pp22/23','Page22 ends la condition que; page23 starts les coefficients. The attached marker now precedes les.'],
9:['formula (1.7 bis)','The display has no trailing stop. The attached layers correctly omit it.'],
10:['homomorphimse additif','The source transposes m and s in homomorphimse. The attached current homomorphisme corrects it.'],
11:['formula (1.10), final member','Only one closing parenthesis follows the last x, leaving λ^i unclosed. Current supplies the second close.'],
12:['formula (1.11), first row ending','The first row has no terminal comma. The attached layers omit it.'],
13:['formula (1.11), first row condition','The comparison is visibly ≥. Formula(1.4) states λ_t(1)=1+t, so λ¹(1)=1 and the vanishing condition must be i>1; current has that correction.'],
14:['formula (1.11), second row ending','No comma follows the final parenthesis in the second row.'],
15:['formula (1.11), third row last argument','The last exponent is printed n. Formula(1.8) on the same page defines P_{i,n}(a_1,…,a_{in}); substituting a_j=λ^j(x) gives the final argument λ^{in}x. Apply this still-missing current correction.'],
16:['§2 heading on p24','Exemples is visibly underlined. Retain the attached subsection style under the express heading convention in NOTE_6.'],
17:['example1, présentation extension','The print reads présentation, lacking re. The preceding paragraph names representations ρ of G, and current restores représentation.'],
18:['first spécial in characteristic-zero paragraph','The first spécial has an underline; the second occurrence is plain. The attached emph marks the first, with the underline/italic rendering subject to the volume emphasis convention.'],
19:['second algébriquement clos in p24 body','A second (*) repeats the call to the same footnote. The attached footnotemark repeats the existing mark.'],
20:['p25 first footnote, algébre de Lie','The first e carries an acute, unlike the grave in théorème below. Retain algébre diplomatically; current still needs algèbre.']}
save('evidence_021_025.json',{'findings_021_025.json':e})
patches=load('extra_patches.json')
def patch(p,layer,old,new,sid,reason,kind):patches.append(dict(page=p,layer=layer,old=old,new=new,source_id=sid,reason=reason,kind=kind,expected_count=1))
patch(23,'current',r'P_{i,n}(\lambda^1x,\ldots,\lambda^n x)',r'P_{i,n}(\lambda^1x,\ldots,\lambda^{in} x)','fixes/MISPRINTS_6.json#36',e[15][1],'misprint_correction')
patch(25,'current',"d'une algébre de Lie","d'une algèbre de Lie",'fixes/MISPRINTS_6.json#38',e[20][1],'misprint_correction')
patch(23,'both','$k$ est\n','$k$ est spé%\n','ASTRA-EARLY-0007','The last line of p23 ends spé-; preserve that exact page boundary while keeping the TeX word joined across the marker.','marker')
patch(24,'both','spécial~;','cial~;','ASTRA-EARLY-0007','The first line of p24 begins cial; the initial spé% belongs immediately before the folio24 marker.','marker')
save('extra_patches.json',patches)
records=load('extra_decisions.json')
def rec(typ,p,sid,pr,region,reason,change,verdict='confirmed',**kw):records.append(dict(record_type=typ,page=p,source_id=sid,verdict=verdict,printed_reading=pr,image=f'scan/SGA6_scan_360dpi.pdf#page={p+14}',region=region,reason=reason,change=change,forms='French diplomatic and corrected; English where meaning or notation is affected',**kw))
rec('own_finding',23,'ASTRA-EARLY-0007','p23 spé- / p24 cial','last body line of p23 and first line of p24','The printed word spécial crosses the folio boundary. The attached marker stands before the whole word; move the first syllable above the marker with a TeX percent to preserve a single rendered word.',{'page23':'est spé%','page24':'cial~;'},'not applied and now applied',related_pages=[23,24])
rec('typography_observation',21,'ASTRA-EARLY-TYPE-001','underlined defined terms on pp21–24','defined terms in body text and footnote','The print underlines anneau in λ-anneau and pré-/anneau in the footnote; on p22 it underlines anneau augmenté, anneau spécial and universels, on p23 universels and spécial, and on p24 the emphasized phrases. The attached normalem setting makes emph italic. This complete observation is referred to the volume-wide emphasis rendering decision.','Volume emphasis convention; no isolated content edit.',related_pages=[21,22,23,24])
rec('typography_observation',25,'ASTRA-EARLY-TYPE-002','first note (1); second note (*)','body calls and both footnotes','The same page uses a numeric original note and a starred added note. Page20 explicitly explains that the1967 additions carry (*)/(**). The page must retain this mixed mark system in a diplomatic rendering.','Preserve numeric and added starred notes according to their printed calls; no blanket all-symbol renumbering.')
rec('hold_difference',23,'fr/codex/HOLD_VS_CORR.json#26','homomorphimse','special λ-ring paragraph',e[10][1],{'diplomatic':'homomorphimse','corrected':'homomorphisme'})
rec('hold_difference',24,'fr/codex/HOLD_VS_CORR.json#27','présentation extension','example1',e[17][1],{'diplomatic':'présentation','corrected':'représentation'})
save('extra_decisions.json',records)
pages=load('extra_pages.json');f=json.loads((R/'check/findings/findings_021_025.json').read_text())
beg={21:'CHAPITRE I',22:'(1.4) λ_t(1)=1+t.',23:'les coefficients',24:'cial ; mais nous',25:'Variantes de l’exemple précédent'}
for p in range(21,26):pages.append(dict(page=p,pdf_page=p+14,fully_checked=True,main_scan_viewed='four overlapping horizontal strips',witness_viewed=False,findings_count=sum(z['page']==p for z in f),begins=beg[p],notes='Body text, formulas and footnotes compared directly; spelling, punctuation and exact folio syllable boundaries included.'))
save('extra_pages.json',pages)
over=load('record_overrides.json')
for i in (2,16):over[f'check/findings/findings_021_025.json#{i}']={'change':'Printed underline confirmed; subsection heading accepted without underline under NOTE_6.'}
save('record_overrides.json',over)
