"""One-shot record of directly read pp.51–55 and witness64 bottom detail."""
from pathlib import Path
import json
R=Path(__file__).resolve().parents[2];O=Path(__file__).resolve().parent
def load(n):return json.loads((O/n).read_text())
def save(n,a):(O/n).write_text(json.dumps(a,ensure_ascii=False,indent=2)+'\n')
e={
1:['p52, f-upper-shriek(O_Z)=O_f-inverse(Z)','Both structure-sheaf letters are typed O with an underline. Replace both cO commands on inspected p52 by explicit underline{O}, continuing the directly observed appendix convention.'],
2:['boundary pp52/53','The first part of Proposition2.8 is on p52 and ends la formule; p53 begins(2.22) est exacte. The attached split of the emphasis groups and marker now preserves that boundary.'],
3:['le faisceau image directe f_!(F)','The lower mark is a short vertical stroke with its dot underneath, an exclamation mark. The attached f_! is correct.'],
4:['des faisceaux R^q f_!(F)','The lower exclamation mark is distinct below f in the first derived-image mention. The attached f_! is correct; R is ordinary typed capital R.'],
5:['par définition R^q f_!(F)','The same explicit lower exclamation mark appears in this second derived-image mention. The attached f_! matches.'],
6:['formula(2.24), three occurrences','Both occurrences on the equality R^0f_!(F)=f_!(F) and the subsequent R^qf_!(F)=0 carry the lower vertical stroke and dot. All three attached lower shrieks match.'],
7:['formula(2.25)','The f inside Γ(U,R^qf_!(F)) has a lower exclamation mark. The attached lower shriek matches.'],
8:['noté encore f_!','The lower mark includes a short vertical stroke and detached dot. Native witness64 confirms the same shape. The attached f_! matches.'],
9:['formula(2.26), two occurrences','The left f and the f inside R^qf(F) each have a lower exclamation mark, visible in both primary and native witness64. Both attached f_! match.'],
10:['La relation, right-hand side','The f and g on the right each have a lower exclamation mark, directly confirmed in witness64. Their attached f_!g_! match. The left-hand mark is a separate print omission.'],
11:['La relation, left-hand side','Both the primary and native witness64 leave the area under(fg) blank, while the f and g on the right are explicitly marked. Diplomatic retains(fg); current already supplies the lower shriek to denote the direct-image map of the composite.'],
12:['boundary pp53/54','The last syllable on p53 is parti- and p54 begins culier. Both layers already split it as parti% / culier.'],
13:['formula(2.27), two direct images','Both outer f symbols have lower exclamation marks; the inner pullback f has an upper exclamation mark. The attached expression preserves these distinct positions.'],
14:['formula(2.27), membership condition','A separate baseline dot is visibly printed after x before ∈. Remove that stray dot in current; diplomatic retains it.'],
15:['le foncteur F→f_!(F)','The f on the right of the arrow has a lower exclamation mark, with the dot below the stroke. The attached lower shriek is correct.'],
16:['R^qf_!(F)=0 pour q>0','The derived image has a lower exclamation mark. The attached f_! and ordinary R match.'],
17:['dans ce cas ... class identity','Both occurrences in f_!(γ_X(F))=γ_Y(f_!(F)) have the lower exclamation mark. Both attached f_! match.'],
18:['injection canonique de Y dans X','The print explicitly says Y dans X. The same sentence defines X as a subspace of Y, and(2.28) has domain class γ_X(F) and target γ_Y(F). The inclusion is therefore i:X→Y; reverse the two letters in current.'],
19:['before(2.28)','A colon follows on a. The attached layers already include it.'],
20:['formula(2.28)','The i carries a lower exclamation mark. The attached i_! matches.'],
21:['heading of §4','The section sign appears before4. The attached heading now includes it.'],
22:['proof, γ_X×k(D)−p^!(y))','There are two closing parentheses after y. Current already removes the extraneous second close; the two global occurrences of the argument D are separately corrected by ASTRA-EARLY-0016.'],
23:['Corollaire label','The underlined label is followed by a colon. The attached colon matches.'],
24:['boundary pp55/56','Page55 ends homomorphismes naturels followed by a colon. The displayed exact sequence(2.30) is the first matter of p56, whose top strip was directly viewed to confirm the marker. The attached marker correctly precedes the display.']}
save('evidence_051_055.json',{'findings_051_055.json':e})
patches=load('extra_patches.json')
def patch(p,layer,old,new,sid,reason,kind='misprint_correction',count=1):patches.append(dict(page=p,layer=layer,old=old,new=new,source_id=sid,reason=reason,kind=kind,expected_count=count))
patch(52,'both',r'\cO',r'\underline{O}','check/findings/findings_051_055.json#1',e[1][1],'font',2)
patch(54,'current',r'(x.\in\underline K(X)',r'(x\in\underline K(X)','fixes/MISPRINTS_6.json#85',e[14][1])
patch(54,'current',r"l'injection canonique de $Y$ dans $X$",r"l'injection canonique de $X$ dans $Y$",'fixes/MISPRINTS_6.json#86',e[18][1])
patch(51,'current',r'exemple 2, pour la définition de $\underline K(G)$',r'exemple 1, pour la définition de $\underline K(G)$','ASTRA-EARLY-0015','ChapterI §2 example1 on p24 defines K(G) from representations and its variants continue at the top of p25. Example2 on p25 defines groups of vector bundles on X. Correct the reference to the defining example1.')
patch(55,'current',r'\gamma_{X\times k}(D)',r'\gamma_{X\times k}(Y)','ASTRA-EARLY-0016','The paragraph defines D=Y restricted to U×k. For j:U×k→X×k, restriction j^!:K(X×k)→K(U×k) sends γ_{X×k}(Y) to γ_{U×k}(D). Thus the global class whose restriction is p^!(y′) is γ(Y), and the difference with p^!(y) lies in the kernel of restriction. Replace the two global D arguments by Y; retain local γ_{U×k}(D).','misprint_correction',2)
save('extra_patches.json',patches)
records=load('extra_decisions.json')
def rec(typ,p,sid,pr,region,reason,change,verdict='confirmed',**kw):records.append(dict(record_type=typ,page=p,source_id=sid,verdict=verdict,printed_reading=pr,image=f'scan/SGA6_scan_360dpi.pdf#page={p+14}',region=region,reason=reason,change=change,forms='French diplomatic and corrected; English where meaning or notation is affected',**kw))
rec('own_finding',51,'ASTRA-EARLY-0015','Chap.I, §2, exemple2','proof of Lemma2.9','The print clearly cites example2 for the definition of K(G). Example1 on p24 defines K(G) from representations and continues with variants on p25; example2 on p25 defines the groups of vector bundles on X. Both cited pages were directly read. Correct the reference number to1 in current.',{'old':'exemple2','new':'exemple1'},'not applied and now applied',related_pages=[24,25,51])
rec('own_finding',55,'ASTRA-EARLY-0016','γ_{X×k}(D), twice','proof of Proposition2.9, global classes after extension of y′','The print gives D twice in the global group K(X×k), but defines D only on U×k as the divisor induced by Y. The restriction j^!:K(X×k)→K(U×k) for j:U×k→X×k sends γ(Y) to γ(D), since Y∩(U×k)=D. Consequently γ_{X×k}(Y)−p^!(y) is the global difference with zero restriction used in the following localization step. Correct these two global arguments to Y and leave all local γ_{U×k}(D) unchanged.',{'old':r'\gamma_{X\times k}(D)','new':r'\gamma_{X\times k}(Y)','count':2},'not applied and now applied')
rec('hold_difference',55,'fr/codex/HOLD_VS_CORR.json#34','p^!(y))','proof of Proposition2.9',e[22][1],{'hold':'p^!(y))','corrected':'p^!(y)'})
rec('typography_observation',54,'ASTRA-EARLY-TYPE-007','(*)','author note call after ouvert affine and footnote label','The literal star is enclosed in baseline parentheses at both call and label. The full note, including1957 and its exclamation mark, was read directly.','Preserve the explicit author-note mark.')
save('extra_decisions.json',records)
pages=load('extra_pages.json');f=json.loads((R/'check/findings/findings_051_055.json').read_text())
beg={51:'Lemme2.9',52:'par une formule',53:'(2.22) est exacte',54:'culier des relations',55:'vérifier que pour toute partie'}
for p in range(51,56):pages.append(dict(page=p,pdf_page=p+14,fully_checked=True,main_scan_viewed='four overlapping horizontal strips',witness_viewed=p==53,findings_count=sum(z['page']==p for z in f),begins=beg[p],notes='All prose, displays, diagram p52 and note p54 directly compared. Every lower-shriek occurrence on pp53–54 individually checked. Native witness64 confirms the bottom direct images and the omitted lower mark under(fg).'))
save('extra_pages.json',pages)
