"""One-shot record of directly compared pp.61–65 and witness75 detail."""
from pathlib import Path
import json
R=Path(__file__).resolve().parents[2];O=Path(__file__).resolve().parent
def load(n):return json.loads((O/n).read_text())
def save(n,a):(O/n).write_text(json.dumps(a,ensure_ascii=False,indent=2)+'\n')
e={
1:['boundary pp60/61','Page61 begins A-tilde soumis aux restrictions, continuing the statement begun on p60. Both attached markers now preserve this boundary.'],
2:['first displayed eta_j expansion','In the final exponent, j sits beside n on the same raised baseline. Diplomatic retains(nj); current already lowers j to give the indexed dimension n_j defined in the statement.'],
3:['parenthetical donc eta_j^(k)=0','The parenthetical words and formula lack the statement underline. On ait resumes it. Both attached emphasis scopes match.'],
4:['on ait','A colon follows the underlined words. Both attached layers include it.'],
5:['first R display','No punctuation follows A-tilde^p. Both attached layers match.'],
6:['second R display, note call','The only call is the baseline parenthesized star to the right of K(X)^p, followed by a separate full stop. The attached display position is correct; replace its automatic footnotemark by the explicitly labeled author-note helper.'],
7:['second R display, occurrence count','The formula occurs only once, before the demonstration; the star is the author-note call. The attached layers have removed the redundant tagged copy and retain the single correctly placed display.'],
8:['second R display, parentheses','Only three parentheses close after E_j′, leaving the outer R argument unclosed. Diplomatic preserves three; current already supplies the fourth.'],
9:['reduction to a product of grassmannians','On est ramené au cas où and est un produit de grasmaniennes are underlined; the intervening X and preceding qu′ are outside the underlining. The attached emphasis matches.'],
10:['author note, implique si','There is a space and no comma between implique and si. Both attached layers now match; the earlier comma after que remains.'],
11:['author note, gamma^k(E_i−epsilon(E_i))','Both subscripts are visibly i. The statement separately indexes the x_i for1≤i≤q and the bundles E_j for1≤j≤r. In the expression giving the operations on those bundles, correct both E_i occurrences to E_j, retaining the x/xi indices.'],
12:['boundary pp61/62','The first Lemma2.15 begins on p61 and ends there sans torsion de la forme. Page62 starts A-tilde (où A...). Both attached markers match.'],
13:['first Lemma2.15, graded map','The K in G(K(X)) lacks an underline. Diplomatic preserves this omission; current already supplies the underline of the Grothendieck group. The target G(A) is considered separately in ASTRA-EARLY-TYPE-012.'],
14:['Pour le prouver le lemme','Both occurrences of le are printed. Remove the first in current, giving Pour prouver le lemme; diplomatic retains the redundancy.'],
15:['Nous considérerons paragraph','A new indented paragraph follows the short line ending(cf.§5). Both attached layers now separate it.'],
16:['product factors C_j','The letter is clearly C. This sentence introduces C_j as local names for the factors of the product X and defines E_j as pullbacks of their canonical bundles. The earlier generic grassmannian G does not impose a different name on these factors. The explicit identification G_j:=C_j would merely rename the factors and leave the projections and pulled-back bundles identical. Retain the printed C_j in both layers; reject the unsupported misprint correction to G_j.'],
17:['De a) résulte','The new paragraph is indented after the listed facts. Both attached paragraph breaks match.'],
18:['boundary pp62/63','Page62 ends est égale à and p63 begins1 pour F=O_(x). Both attached markers now precede1.'],
19:['application C-tilde ... dans A(X)-tilde','The handwritten tilde spans the complete A(X). Both attached layers now use widetilde{A(X)}.'],
20:['target G(A(X)-tilde)','The wide tilde again spans A(X) inside G. Both attached layers match.'],
21:['§5 heading','A section sign precedes5. The attached heading includes it.'],
22:['§5 heading end','A full stop follows d’injection. The attached heading includes it.'],
23:['Theorem2.16, x∈K(X)','This K lacks the underline present in the later graded terms. Diplomatic preserves plain K; current already restores the underline.'],
24:['Theorem2.16, c-tilde display','The lower bound is the typed phi glyph, with a vertical stroke through its loop. Diplomatic already retains phi. Correct current0 to1: c^0 is the class of gamma^0=1, and the leading constant1 is already written. The construction of A-tilde in ChapterI §3 uses [n,1+Σ_{i≥1}a^i], so the positive-degree sum starts at1.'],
25:['boundary pp63/64','Page63 ends et; p64 begins(2.8) résulte de(2.31). Both attached markers match.'],
26:['first cqfd on p64','No period follows cqfd, whereas p63 has a visible period. Both attached layers preserve this distinction.'],
27:['Corollaire1 label','The label ends in a colon. Both attached layers match.'],
28:['détermination explicité','An acute accent is visible on the last e. Current must use the adjective explicite; diplomatic retains explicité.'],
29:['Corollaire2 label','The label ends in a colon. Both attached layers match.'],
30:['Comme phi est surjective paragraph','The sentence starts an indented new paragraph after(2.35). Both attached paragraph breaks match.'],
31:['congruence after(2.35)','The argument of epsilon is a capital X, unlike the adjacent lower-case x. Native witness75 confirms it. Epsilon is the augmentation of the element x∈K(X), as in Theorem2.16; correct only the capital letter to lower-case x.'],
32:['Comme psi est injective','The word injective is visibly underlined. Both attached layers include its emphasis.'],
33:['Remarque label','The label ends in a colon. Both attached layers match.'],
34:['pour i-upper-shriek et i-lower-shriek','The mark below the second i consists of an exclamation stem and a detached dot. The attached lower shriek matches.'],
35:['before les formules suivantes','No comma follows the second i. The nearby stroke belongs to its lower exclamation mark. Both attached layers omit the added comma.'],
36:['formula(ii), first line','Both direct-image symbols have a lower exclamation stem and dot. The pullback i in the argument has an upper exclamation mark. The attached notation preserves all positions.'],
37:['formula(ii), second line','Both direct-image symbols carry lower exclamation marks, with upper marks on the following pullbacks. The attached lower shrieks match.'],
38:['formula(iii), first line','The inner i has a lower exclamation mark and the outer i an upper one. The attached notation matches.'],
39:['formula(iii), second line','The second i in the middle term has a lower exclamation mark. The attached notation matches.'],
40:['formula(iv), three direct images','All three i symbols carry lower exclamation marks with detached dots. All three attached lower shrieks match.'],
41:['formula(iv), closing parenthesis','The right-hand side closes only the parenthesis of lambda_{−1}(N), leaving the i_! argument unclosed. Diplomatic preserves the printed omission; current already supplies the additional close.'],
42:['boundary pp65/66','Page65 ends with formula(2.36), its enclosing parenthesis, and the author note. Page66 starts La formule(iv), directly confirmed in its top strip. Both attached markers precede La.']}
save('evidence_061_065.json',{'findings_061_065.json':e})
patches=load('extra_patches.json')
def patch(p,layer,old,new,sid,reason,kind='misprint_correction',count=1):patches.append(dict(page=p,layer=layer,old=old,new=new,source_id=sid,reason=reason,kind=kind,expected_count=count))
patch(61,'current',r'\gamma^k(E_i-\varepsilon(E_i))',r'\gamma^k(E_j-\varepsilon(E_j))','fixes/MISPRINTS_6.json#97',e[11][1])
patch(62,'current','Pour le prouver le lemme','Pour prouver le lemme','fixes/MISPRINTS_6.json#99',e[14][1])
patch(63,'current',r'\sum_{i\geq0}c^i(x)',r'\sum_{i\geq1}c^i(x)','fixes/MISPRINTS_6.json#102',e[24][1])
patch(64,'current','détermination explicité','détermination explicite','fixes/MISPRINTS_6.json#103',e[28][1])
patch(64,'current',r'\gamma^i(x-\varepsilon(X))',r'\gamma^i(x-\varepsilon(x))','fixes/MISPRINTS_6.json#104',e[31][1])
proof='The primary image and native witness75 both print C-tilde(x)∈A(X)^i without a tilde on A. Formula(2.7) defines the lambda-homomorphism C-tilde:K(X)→A-tilde(X), and p62 states its filtration compatibility. Thus x∈K(X)^i gives C-tilde(x)∈A-tilde(X)^i. Applying this lambda-homomorphism to the gamma-expression and then taking its degree-i class is exactly the associated-graded map psi used in the proof. Formula(1.22bis) concerns the gamma-operation in A-tilde. Restore the missing target tilde in current.'
patch(64,'current',r'\Ctil(x)\in A(X)^i',r'\Ctil(x)\in\Atil(X)^i','ASTRA-EARLY-0018',proof)
patch(63,'both',r'\cO',r'\underline{O}','ASTRA-EARLY-TYPE-009','The O in the opening skyscraper sheaf O_(x) is visibly underlined. Preserve it explicitly.','font')
patch(65,'both',r'\cO',r'\underline{O}','ASTRA-EARLY-TYPE-010','All four O letters in(2.36), including the Tor base-ring superscript, are plain typed O with underlines. Preserve the four observed forms explicitly.','font',4)
patch(61,'both',r'\text{\footnotemark}',r'\text{\SGAAuthorFootMark{*}}','ASTRA-EARLY-NOTE-061-1',e[6][1],'author_note_label')
patch(61,'both',r'\footnotetext{',r'\SGAAuthorFootText{*}{','ASTRA-EARLY-NOTE-061-2','The author-note label is the same baseline parenthesized star as its display call. Preserve the literal label.','author_note_label')
patch(65,'both',r'\footnote{Non',r'\SGAAuthorFootnote{*}{Non','ASTRA-EARLY-NOTE-065-1','The call after nuls! and the note label are baseline parenthesized stars. The reference page30 is the appendix local page number, corresponding to printed volume folio50; preserve the author’s literal reference.','author_note_label')
save('extra_patches.json',patches)
records=load('extra_decisions.json')
def rec(typ,p,sid,pr,region,reason,change,verdict='confirmed',**kw):records.append(dict(record_type=typ,page=p,source_id=sid,verdict=verdict,printed_reading=pr,image=f'scan/SGA6_scan_360dpi.pdf#page={p+14}',region=region,reason=reason,change=change,forms='French diplomatic and corrected; English where meaning or notation is affected',**kw))
rec('own_finding',64,'ASTRA-EARLY-0018','C-tilde(x)∈A(X)^i','last line of the proof of Corollaire2',proof,{'old':r'\Ctil(x)\in A(X)^i','new':r'\Ctil(x)\in\Atil(X)^i'},'not applied and now applied',witness_image='scan/SGA6_witness_300dpi.djvu#page=75',related_pages=[30,40,62,64])
rec('typography_observation',63,'ASTRA-EARLY-TYPE-009','underlined O_(x)','first text line','The O is a plain typed capital with a short underline. Continue the locally observed sheaf convention in this one occurrence.',{'old':r'\cO','new':r'\underline{O}'},'not applied and now applied')
rec('typography_observation',65,'ASTRA-EARLY-TYPE-010','four underlined O letters','formula(2.36)','The base-ring superscript O_X and the three O_Y letters are all visibly underlined. Replace these four cO forms only.',{'old':r'\cO','new':r'\underline{O}','count':4},'not applied and now applied')
rec('typography_observation',61,'ASTRA-EARLY-TYPE-011','Lemme2.15 on p61 and again on p62','two consecutive lemma labels','Both distinct lemmas literally bear2.15. Their content and location distinguish the two statements. No unique replacement number is supplied by the scan, so retain both printed labels.', 'Retain duplicate printed numbering.',related_pages=[61,62])
rec('notation_observation',62,'ASTRA-EARLY-TYPE-012','G(A), G(A(X))≃A(X)','associated-graded targets in Lemma2.15 and its proof','The print has plain A in these graded targets. For the Chow ring of the product of grassmannians, the canonical degree-i map from G(A-tilde(X)) to A^i(X) sends the class of [0,1+a_i+higher terms] to a_i (and degree0 sends the rank to its multiple of1). The graded ring of A(X) with its degree filtration is canonically A(X) as well. The displayed targets can therefore be read through these explicit identifications; retain the printed notation.', 'Retain G(A) and G(A(X)) with the stated associated-graded identification.')
for p,sid,region in [(61,'ASTRA-EARLY-NOTE-061-1','call after second R display'),(61,'ASTRA-EARLY-NOTE-061-2','author-note label'),(65,'ASTRA-EARLY-NOTE-065-1','call after nuls! and author-note label')]:
 rec('typography_observation',p,sid,'(*)',region,'The parentheses and central star are on the baseline. Preserve the literal mark using the explicit author-note helpers.', 'Replace the automatic note mark by explicit label *.', 'not applied and now applied')
save('extra_decisions.json',records)
overrides=load('record_overrides.json')
for sid in ['check/findings/findings_061_065.json#16','fixes/MISPRINTS_6.json#100']:overrides[sid]={'verdict':'rejected','change':'Retain printed C_j in all forms. The proposed G_j would only rename locally introduced factors; no correction is established.','reason':e[16][1]}
save('record_overrides.json',overrides)
pages=load('extra_pages.json');f=json.loads((R/'check/findings/findings_061_065.json').read_text())
beg={61:'A-tilde soumis aux restrictions',62:'A-tilde (où A est un anneau gradué)',63:'1 pour F=O_(x)',64:'(2.8) résulte de(2.31)',65:'tout cas facilement'}
for p in range(61,66):pages.append(dict(page=p,pdf_page=p+14,fully_checked=True,main_scan_viewed='four overlapping horizontal strips',witness_viewed=p==64,findings_count=sum(z['page']==p for z in f),begins=beg[p],notes='All prose, displays and author notes directly compared. Witness75 lower-middle detail confirms epsilon(X) and missing target tilde on p64. All ten lower-shriek occurrences on p65 individually inspected.'))
save('extra_pages.json',pages)
