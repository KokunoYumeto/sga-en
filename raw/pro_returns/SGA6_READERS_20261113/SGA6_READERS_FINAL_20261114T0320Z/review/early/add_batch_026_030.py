"""Record directly inspected pp.26–30, with p31 boundary context."""
from pathlib import Path
import json
R=Path(__file__).resolve().parents[2];O=Path(__file__).resolve().parent
def load(n):return json.loads((O/n).read_text())
def save(n,a):(O/n).write_text(json.dumps(a,ensure_ascii=False,indent=2)+'\n')
e={
1:['classes des réprésentations rationnelles','The first e has a visible acute accent. Corrected spelling removes that first accent; the later é remains.'],
2:['Z(T-hat), algébre du groupe','The e of algébre has an acute rather than a grave. Current still requires algèbre.'],
3:['p26 footnote, Groupes de Lie albébriques','The letter after al is clearly b, with an ascender and closed bowl. Current already restores algébriques.'],
4:['statement labels on pp26,27,30 and §3 heading p28','Théorème, Corollaire, Remarques and Proposition are underlined as label words, while their numbers/punctuation are outside the rule; the p28 heading underlines its text except lambda. Retain the accepted label and section-title typesetting convention in NOTE_6.'],
5:['p27 footnote, groupe dévisé','The printed word is dévisé. The note names G′, the derived group of G; current already restores dérivé.'],
6:['p28 sum following [n,x]','The printed x has both an upper i and a lower i; the sum has its separate lower i≥1. The surrounding definition names the homogeneous components x^i∈A^i, with no lower index. Current correctly omits the stray lower i.'],
7:['p28 strucutre additive','The letters are printed strucutre, with the middle t and u transposed. Current has structure.'],
8:['formula (1.16), after i≥1','No comma follows the closing parenthesis. The attached layers already match.'],
9:['boundary pp28/29','Page28 ends with (1.16); page29 starts le polynôme Q_i. Both attached markers precede le.'],
10:['before formula (1.20)','There is no colon after entiers. The attached layers already omit it.'],
11:['Proposition1.2, parenthetical remark','The words within the parentheses on a donc ... pour i>n are not underlined. The rule resumes at on a after the close; the attached split emph preserves that boundary.'],
12:['formula (1.22), closing bracket','The display ends at the right square bracket without a full stop. The attached layers already match.'],
13:['page30 ending / page31 beginning','Page30 ends pour i>n. Directly viewed p31 top strip starts La formule (1.22). The attached marker correctly precedes La.']}
save('evidence_026_030.json',{'findings_026_030.json':e})
patches=load('extra_patches.json')
def patch(p,layer,old,new,sid,reason,kind):patches.append(dict(page=p,layer=layer,old=old,new=new,source_id=sid,reason=reason,kind=kind,expected_count=1))
patch(26,'current','classes des réprésentations rationnelles','classes des représentations rationnelles','fixes/MISPRINTS_6.json#14',e[1][1],'misprint_correction')
patch(26,'current','algébre du groupe','algèbre du groupe','fixes/MISPRINTS_6.json#15',e[2][1],'misprint_correction')
save('extra_patches.json',patches)
records=load('extra_decisions.json')
def rec(typ,p,sid,pr,region,reason,change,verdict='confirmed',**kw):records.append(dict(record_type=typ,page=p,source_id=sid,verdict=verdict,printed_reading=pr,image=f'scan/SGA6_scan_360dpi.pdf#page={p+14}',region=region,reason=reason,change=change,forms='French diplomatic and corrected; English where meaning or notation is affected',**kw))
rec('formatting_decision',27,'ASTRA-EARLY-0008','Z[ρ1,…,ρr′;σ1,…,σr″;σ1⁻¹,…,σr″⁻¹] du corps des fonctions rationnelles','corollary, second printed line','The printed expression is inline, and the attached expression is displayed. Every mathematical symbol and punctuation token is identical. The task accepts this layout change.','Retain the attached display wrapper. Mapping: each symbol of the inline printed formula maps identically to the same symbol in the attached displayed formula.')
rec('formatting_decision',30,'ASTRA-EARLY-0009','automorphisme principal x=Σx^i→check x=Σ(−1)^ix^i','paragraph before Proposition1.2','The printed map is inline after principal, and the attached map is displayed. Every mathematical symbol and punctuation token is identical. The task accepts this layout change.','Retain the attached display wrapper. Mapping: each symbol of the inline printed formula maps identically to the same symbol in the attached displayed formula.')
rec('hold_difference',26,'fr/codex/HOLD_VS_CORR.json#28','Groupes de Lie albébriques','footnote',e[3][1],{'diplomatic':'albébriques','corrected':'algébriques'})
rec('hold_difference',27,'fr/codex/HOLD_VS_CORR.json#29','groupe dévisé G′','footnote',e[5][1],{'diplomatic':'dévisé','corrected':'dérivé'})
rec('hold_difference',28,'fr/codex/HOLD_VS_CORR.json#30','strucutre additive','paragraph after (1.15)',e[7][1],{'diplomatic':'strucutre','corrected':'structure'})
save('extra_decisions.json',records)
pages=load('extra_pages.json');f=json.loads((R/'check/findings/findings_026_030.json').read_text())
beg={26:'premier λ-anneau défini ici',27:'soient (ρ_i)',28:'b) Lorsque le corps',29:'le polynôme Q_i',30:'(1.19) η′(x^i)'}
for p in range(26,31):pages.append(dict(page=p,pdf_page=p+14,fully_checked=True,main_scan_viewed='four overlapping horizontal strips',witness_viewed=False,findings_count=sum(z['page']==p for z in f),begins=beg[p],notes='Complete body, formulas and footnotes compared. Page31 top strip additionally viewed to confirm the p30/31 marker.'))
save('extra_pages.json',pages)
