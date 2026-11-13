"""One-shot recording of directly read printed pp.36–40, with witness48."""
from pathlib import Path
import json
R=Path(__file__).resolve().parents[2];O=Path(__file__).resolve().parent
def load(n):return json.loads((O/n).read_text())
def save(n,a):(O/n).write_text(json.dumps(a,ensure_ascii=False,indent=2)+'\n')
e={
1:['boundary pp35/36','Page35 ends élé- and page36 begins ment de K. The attached layers already split the word as élé% / ment across the marker.'],
2:['il est commode d’introduite','The final consonant is t in introduite. The construction commode de requires the infinitive introduire, which is still missing in current.'],
3:['boundary pp36/37','Page36 ends Dans le cas actuel, and page37 starts sa restriction. The attached marker now precedes sa.'],
4:['before formula(1.40)','The last text is combinant (1.32) et (1.37) with no following comma. Both attached layers already omit the comma.'],
5:['formula(1.38), arguments of G','The two ellipses each show comma, two dots, comma, directly confirmed in the native witness48 crop. Diplomatic retains the two-dot reading; current supplies the usual three-dot ellipsis already.'],
6:['formula(1.39), arguments of G','There are two dots between the commas after x^1. This is the same two-dot typed ellipsis as in(1.38), already retained diplomatically and expanded in current.'],
7:['boundary pp37/38','Page37 ends est; page38 starts the complete d’augmentation nulle). The attached marker is now before d’augmentation, with no inserted space after the apostrophe.']}
save('evidence_036_040.json',{'findings_036_040.json':e})
patches=load('extra_patches.json')
def patch(p,layer,old,new,sid,reason,kind='misprint_correction',count=1):patches.append(dict(page=p,layer=layer,old=old,new=new,source_id=sid,reason=reason,kind=kind,expected_count=count))
patch(36,'current',"d'introduite", "d'introduire",'fixes/MISPRINTS_6.json#63',e[2][1])
patch(37,'current',r'\binom{n-1}{i}\lambda^i(N,x)',r'\binom{n-1}{i}\lambda^{n-i}(N,x)','ASTRA-EARLY-0012','By(1.23), γ^n(x_N)=λ^n(x_N+n−1). The generating series identity λ_t(x_N+n−1)=(1+t)^(n−1)λ_t(x_N) has t^n coefficient Σ_{i=0}^{n−1} binom(n−1,i)λ^{n−i}(x_N). The printed λ^i gives λ^0=1 for n=1, whereas(1.23) explicitly gives γ^1(x_N)=x_N.')
patch(37,'current',r'pour tout entier $j\geq0$',r'pour tout entier $j\geq1$','ASTRA-EARLY-0013','The claimed formula(1.38) contains(j−1)!, which is undefined at j=0. Its proof uses(1.18) with the positive degrees j and q. Restricting the quantified range to j≥1 restores the common domain of the stated component formula and its proof; the j=0 filtration inclusion alone is the definition A-tilde^0=A-tilde.')
save('extra_patches.json',patches)
records=load('extra_decisions.json')
def rec(typ,p,sid,pr,region,reason,change,verdict='confirmed',**kw):records.append(dict(record_type=typ,page=p,source_id=sid,verdict=verdict,printed_reading=pr,image=f'scan/SGA6_scan_360dpi.pdf#page={p+14}',region=region,reason=reason,change=change,forms='French diplomatic and corrected; English where meaning or notation is affected',**kw))
rec('own_finding',37,'ASTRA-EARLY-0012',r'Σ_{i=0}^{n−1} binom(n−1,i) λ^i(N,x)','formula(1.37)','Both the primary scan and native witness48 clearly print exponent i. Formula(1.23) defines γ^n(x_N)=λ^n(x_N+n−1); multiplying the series λ_t(x_N) by(1+t)^(n−1) gives exponent n−i in the displayed summation. At n=1 the printed sum is λ^0=1 but γ^1(x_N)=x_N, explicitly stated on p31. Preserve i diplomatically and correct n−i in current.',{'old':r'\lambda^i(N,x)','new':r'\lambda^{n-i}(N,x)'},'not applied and now applied',related_pages=[31,36,37],witness_image='scan/SGA6_witness_300dpi.djvu#page=48')
rec('own_finding',37,'ASTRA-EARLY-0013','pour tout entier j≥0','Proposition1.5, quantified range','The primary and native witness48 print j≥0. Formula(1.38) subsequently contains(j−1)!, undefined at j=0; the proof uses the multiplication formula(1.18) with positive degrees j and q. The inclusion at j=0 alone is tautological from A-tilde^0=A-tilde, but the claimed component formula has domain j≥1. Correct the single quantified bound to j≥1 in current, leaving the diplomatic reading unchanged.',{'old':r'j\geq0','new':r'j\geq1'},'not applied and now applied',related_pages=[29,37,38],witness_image='scan/SGA6_witness_300dpi.djvu#page=48')
rec('typography_observation',39,'ASTRA-EARLY-TYPE-003','(*) after Théorème2.1 and at the footnote','author footnote call and label','The star is enclosed in literal parentheses at the text baseline, both at the call and at the footnote. Re-inspection of pp20,21,24,25 gives the same baseline parenthesized star; the p25 numeric note instead has baseline parentheses around a raised digit1.','Preserve explicit author marks independently of the editorial apparatus.',related_pages=[20,21,24,25,39])
save('extra_decisions.json',records)
pages=load('extra_pages.json');f=json.loads((R/'check/findings/findings_036_040.json').read_text())
beg={36:'ment de K',37:'sa restriction à K',38:'d’augmentation nulle)',39:'soit bien un anneau gradué',40:'Ainsi, relativement aux morphismes propres'}
for p in range(36,41):pages.append(dict(page=p,pdf_page=p+14,fully_checked=True,main_scan_viewed='four overlapping horizontal strips',witness_viewed=p==37,findings_count=sum(z['page']==p for z in f),begins=beg[p],notes='All body text, displays, chapter heading on p38, and author note on p39 compared directly. Native witness48 additionally read for formula(1.37), Proposition1.5 range, and formula(1.38) ellipses.'))
save('extra_pages.json',pages)
