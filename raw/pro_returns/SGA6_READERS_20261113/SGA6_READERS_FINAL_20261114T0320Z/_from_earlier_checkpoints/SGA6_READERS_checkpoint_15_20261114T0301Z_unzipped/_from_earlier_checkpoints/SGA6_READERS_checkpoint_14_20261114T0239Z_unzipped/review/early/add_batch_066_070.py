"""One-shot record after direct comparison of pp.66–70 and witness79 detail."""
from pathlib import Path
import json
R=Path(__file__).resolve().parents[2];O=Path(__file__).resolve().parent
def load(n):return json.loads((O/n).read_text())
def save(n,a):(O/n).write_text(json.dumps(a,ensure_ascii=False,indent=2)+'\n')
e={
1:['boundary pp65/66','The first word of p66 is La, before formule(iv). The attached markers now precede this word.'],
2:['first sentence, i direct image','The mark below i has an exclamation stem and detached dot. The attached lower shriek matches.'],
3:['formula(v), two direct images','Both i symbols have lower exclamation marks. The adjacent p exponents and p≥1 condition match. Both attached shrieks are correct.'],
4:['qui signifie que i defines','The i has a lower exclamation mark. The attached lower shriek matches.'],
5:['last sentence, quotient and filtration','The two direct images in quotient de i_! and i_! décale each have lower exclamation marks. In the earlier pair i_* et i^*, both are genuine stars. The attached sequence preserves these distinct marks.'],
6:['pourvu qu’on se place ... et non dans','The prose segments pourvu qu’on se place dans, et, et non dans, et are underlined, with the four mathematical groups outside those rules. Both attached emphasis scopes match.'],
7:['Dans ces formules paragraph','The paragraph starts indented after the list(v bis). Both attached layers preserve the paragraph break.'],
8:['N.B. at top of p67','N.B. is ordinary typed text without an underline. It belongs to p67, where both attached markers now place it. The existing plain text matches.'],
9:['boundary pp66/67','Page66 ends de q unités. Page67 starts N.B. Toutes les formules. Both attached markers match.'],
10:['N.B., first i before resp.','The first i has a lower exclamation mark; the parenthetical resp. pair has genuine lower and upper stars. All attached symbols match.'],
11:['first display on p67','Both i symbols have lower exclamation stems and dots. The attached lower shrieks match.'],
12:['display i_*(G_p)=c^p(i_!(x))','The left i has a star and the i inside c^p has an exclamation mark. The attached distinct symbols match.'],
13:['formula(2.37), left side','The i inside c^{q+j} has a lower exclamation mark. The i on the right has a genuine star. The attached symbols match.'],
14:['Le deuxième membre paragraph','A new indented paragraph begins after(2.37). Both attached layers preserve it.'],
15:['formula(2.38), left side','The inner i has a lower exclamation mark. The right-hand direct image is a genuine lower star. The attached notation matches.'],
16:['formula(2.38), Todd factor','The handwritten looped script glyph is the Todd T, with no detached accent above it. The separate check is over N. The attached mathcal T(check N)^{-1} now matches.'],
17:['boundary pp67/68','Page68 begins Il suffit d’utiliser; p67 ends the formula reference(1.26). Both attached markers now precede Il.'],
18:['formula(2.37bis), direct images','The left inner i has a lower exclamation mark and the right i a star. Both attached symbols match.'],
19:['formula(2.37bis), lambda argument','The c before(N) has no tilde; the c before(x) does. Formula(2.37) directly above uses lambda_{−1}(c-tilde(N)), and(2.37bis) is expressly that formula written in total-class form. Restore the omitted tilde in current, preserving the plain c diplomatically.'],
20:['formula(2.38bis), Todd factor','The script Todd T has no detached check. The attached mathcal T(T_{X/Y})^{-1} matches.'],
21:['Remarques, est nulle','The ending nulle is printed clearly in both the main image and native witness79. The grammatical subject is le produit, so current must read nul. The factor before it is separately adjudicated in ASTRA-EARLY-0020.'],
22:['§6 heading','A section sign precedes6. Both attached headings include it.'],
23:['statement, morphisme propre','Propre has no underline, between underlined un morphisme and d’une variété. Both attached emphasis scopes preserve this.'],
24:['formula(2.39), left Todd factor','The handwritten glyph is the script Todd T without a check accent. The attached mathcal T(Y) matches.'],
25:['formula(2.39), right Todd factor','The second handwritten Todd glyph has the same looped T form without a detached accent. The attached mathcal T(X) matches.'],
26:['parenthetical definition of Todd class','Both handwritten Todd symbols are script T without check accents. The inner C(T_X) is an ordinary C. The attached T(X)=T(C(T_X)) matches.'],
27:['chacun de ces deux morphismes','Two adjacent full stops are printed. Keep both diplomatically and reduce them to one in current.'],
28:['boundary pp69/70','Page69 ends avec y∈K(P) et; p70 begins z∈K(X), followed by a full stop and Alors. Both attached markers match.'],
29:['formula(2.40), ch subscript','The subscript has the short capital-P bowl and foot. It is the same capital P as the space argument, while the later power p is lowercase. The attached ch_P matches.'],
30:['formula(2.40), Todd class','The script Todd glyph is T without a detached check. The attached mathcal T(P) matches.'],
31:['C_P(1−xi) display','Both letters are capital C and P. The print has no tilde over C. The attached C_P and the pair[1,1−L] match; keep this explicitly displayed local notation.'],
32:['two ch displays after et par suite','Both subscripts are capital P; the variable in1−xi and the exponent−L match. Both attached ch_P forms are correct.'],
33:['ch_P(xi^p) display','The ch subscript is capital P and the two powers are lowercase p. The attached distinctions match.'],
34:['last display, ch_P(F)','The ch subscript is capital P. The attached formula matches.'],
35:['last display, Todd class','The handwritten Todd symbol is script T without a check. The attached mathcal T(P) matches.'],
36:['Or si p est la dimension de Q dans P','The print says dimension. The class xi is the hyperplane structure-sheaf class; the transverse intersection of p hyperplanes gives xi^p=gamma_P(Q), so p counts codimension. Correct dimension to codimension in current.'],
37:['final substitution for q','The print says q=r+1−p. Writing H=L/(1−e^{-L}), the displayed product H^{r+1}(1−e^{-L})^p equals L^p H^{r+1−p}. Its L^r coefficient is the L^{r−p} coefficient of H^{r−p+1}; hence the stated coefficient identity uses q=r−p. Correct the extra+1 in current.']}
save('evidence_066_070.json',{'findings_066_070.json':e})
patches=load('extra_patches.json')
def patch(p,layer,old,new,sid,reason,kind='misprint_correction',count=1):patches.append(dict(page=p,layer=layer,old=old,new=new,source_id=sid,reason=reason,kind=kind,expected_count=count))
patch(68,'current',r'\lambda_{-1}(c(N))',r'\lambda_{-1}(\widetilde c(N))','fixes/MISPRINTS_6.json#106',e[19][1])
patch(68,'current','est nulle','est nul','fixes/MISPRINTS_6.json#107',e[21][1])
patch(69,'current','morphismes..','morphismes.','fixes/MISPRINTS_6.json#108',e[27][1])
patch(70,'current',r'la dimension de \(Q\) dans \(P\)',r'la codimension de \(Q\) dans \(P\)','fixes/MISPRINTS_6.json#109',e[36][1])
patch(70,'current',r'poser \(q=r+1-p\)',r'poser \(q=r-p\)','fixes/MISPRINTS_6.json#110',e[37][1])
proof19='The print cites(ii) and(iv) as the identities whose reductions give(iii bis) and(iv bis). Taking associated-graded classes in(iii), i^!i_!(x)=x lambda_{−1}(N), gives i^*i_*(bar x)=bar x (−1)^q c^q(N), exactly(iii bis); the degree-q term of lambda_{−1}(N) is(−1)^q c^q(N). The same passage in(iv) gives(iv bis). Formula(ii) instead gives the already listed projection formula(ii bis). Correct the first cited numeral to(iii).'
patch(66,'current','par réduction des formules (ii) et (iv)','par réduction des formules (iii) et (iv)','ASTRA-EARLY-0019',proof19)
proof20='Both scans print N^q. Let delta denote the difference of the two members, an element on X. The preceding sentence states i^*(delta)=0. Applying i_* and using formula(ii bis) gives0=i_*i^*(delta)=i_*(1)delta=xi′delta, where xi′ is defined on p66. Formula(iii bis) relates i^*(xi′) to(−1)^q N^q on Y, but the product obtained by the stated pushforward on X is with xi′. Replace the printed factor N^q by xi′ in current.'
patch(68,'current',r'leur différence par $N^q$',r"leur différence par $\xi'$",'ASTRA-EARLY-0020',proof20)
proof21='The right-hand f in(2.39) visibly carries a star, while the immediately following paragraph twice explicitly writes f_! for the Grothendieck-group direct image. Formula(2.26) defines f_!:K(Y)→K(X), and ch_X has domain K(X); thus this occurrence is ch_X(f_!(x)). The left-hand f_* acts on the Chow-valued class ch_Y(x)T(Y). Preserve the left star and correct only the right star to a lower shriek.'
patch(69,'current',r'\ch_X\bigl(f_*(x)\bigr)',r'\ch_X\bigl(f_!(x)\bigr)','ASTRA-EARLY-0021',proof21)
patch(70,'both',r'\mathcal O',r'\underline{O}','ASTRA-EARLY-TYPE-013','Both structure-sheaf letters O_Q and O_V are plain typed O with an underline. Preserve these two literal forms explicitly.','font',2)
patch(69,'both',r'\footnote{Voir',r'\SGAAuthorFootnote{*}{Voir','ASTRA-EARLY-NOTE-069-1','The call after characteristic0 and the note label are baseline parenthesized stars. The literal note reference p51 is the appendix local page number, corresponding to volume folio71.','author_note_label')
save('extra_patches.json',patches)
records=load('extra_decisions.json')
def rec(typ,p,sid,pr,region,reason,change,verdict='confirmed',**kw):records.append(dict(record_type=typ,page=p,source_id=sid,verdict=verdict,printed_reading=pr,image=f'scan/SGA6_scan_360dpi.pdf#page={p+14}',region=region,reason=reason,change=change,forms='French diplomatic and corrected; English where meaning or notation is affected',**kw))
rec('own_finding',66,'ASTRA-EARLY-0019','formules(ii) et(iv)','last paragraph',proof19,{'old':'(ii) et(iv)','new':'(iii) et(iv)'},'not applied and now applied',related_pages=[65,66])
rec('own_finding',68,'ASTRA-EARLY-0020','leur différence par N^q','Remarques, annihilating factor',proof20,{'old':'N^q','new':"xi′"},'not applied and now applied',witness_image='scan/SGA6_witness_300dpi.djvu#page=79',related_pages=[66,67,68])
rec('own_finding',69,'ASTRA-EARLY-0021','ch_X(f_*(x))','formula(2.39), right-hand side',proof21,{'old':r'\ch_X\bigl(f_*(x)\bigr)','new':r'\ch_X\bigl(f_!(x)\bigr)'},'not applied and now applied',related_pages=[53,69])
rec('typography_observation',70,'ASTRA-EARLY-TYPE-013','underlined O_Q and O_V','structure-sheaf mentions','Both sheaf letters have explicit underlines, with Q and V as subscripts. Replace the two mathcal O forms only.',{'old':r'\mathcal O','new':r'\underline{O}','count':2},'not applied and now applied')
rec('notation_observation',69,'ASTRA-EARLY-TYPE-014','f_! twice in prose, f_* twice in prose','paragraph after(2.39)','Both direct-image references for K-groups have visible lower exclamation marks, while the cycle-map references have genuine stars. These four attached prose symbols match. The formula’s right-hand star is separately corrected by ASTRA-EARLY-0021.','Retain the four distinct prose marks.')
rec('notation_observation',70,'ASTRA-EARLY-TYPE-015','f_!(x)=chi(y)z','first sentence','The direct-image symbol has a lower exclamation stem and a detached dot. The attached lower shriek matches.','Retain f_!.')
rec('typography_observation',69,'ASTRA-EARLY-NOTE-069-1','(*)','call after characteristic0 and footnote label','The call and note label each have a central star within baseline parentheses. Preserve this exact author-note mark.','Use explicit author label *.','not applied and now applied')
save('extra_decisions.json',records)
overrides=load('record_overrides.json')
overrides['check/findings/findings_066_070.json#8']={'page':67,'image':'scan/SGA6_scan_360dpi.pdf#page=81','original_record_page':66}
for name in ['FIXLOG_6.jsonl','FIXLOG_6_CURRENT.jsonl']:
 for i,line in enumerate((R/'fixes'/name).read_text().splitlines(),1):
  d=json.loads(line)
  if d.get('page')==66 and d.get('old')==r'\textbf{N.B.}':overrides[f'fixes/{name}#{i}']={'page':67,'image':'scan/SGA6_scan_360dpi.pdf#page=81','original_record_page':66}
save('record_overrides.json',overrides)
pages=load('extra_pages.json');f=json.loads((R/'check/findings/findings_066_070.json').read_text())
beg={66:'La formule(iv)',67:'N.B. Toutes les formules',68:'Il suffit d’utiliser',69:'§6. Le théorème de Riemann–Roch',70:'z∈K(X). Alors'}
for p in range(66,71):pages.append(dict(page=p,pdf_page=p+14,fully_checked=True,main_scan_viewed='four overlapping horizontal strips',witness_viewed=p==68,findings_count=sum(z['page']==p for z in f),begins=beg[p],notes='All prose, formulas and note p69 directly compared. Every lower-shriek/star distinction and all Todd glyphs inspected individually. Native witness79 middle confirms N^q and nulle in p68 remarks.'))
save('extra_pages.json',pages)
