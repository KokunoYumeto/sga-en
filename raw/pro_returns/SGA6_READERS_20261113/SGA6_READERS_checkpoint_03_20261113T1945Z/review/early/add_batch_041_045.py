"""One-shot record of directly compared pp.41–45 and the cited witness crops."""
from pathlib import Path
import json
R=Path(__file__).resolve().parents[2];O=Path(__file__).resolve().parent
def load(n):return json.loads((O/n).read_text())
def save(n,a):(O/n).write_text(json.dumps(a,ensure_ascii=False,indent=2)+'\n')
e={
1:['formula(2.8), condition','The printed relation is i≥1. The preceding identity assigns C^1(L(D))=ℓ(D); the vanishing of higher classes of this line bundle starts at i>1. Current already has the corrected bound.'],
2:['formula(2.10), after K(X)','The primary has tiny detached marks after K(X); native witness52 is clean, with no comma. The attached comma removal is confirmed.'],
3:['abbreviation note after(2.10)','Both the primary and native witness52 repeat underlined K(X). Formula(2.6) on p40 names the same group as underlined K(ξ(X)); this note introduces the abbreviation K(X). Restore ξ(X) inside the second K in current.'],
4:['diagram, bottom arrow label','The f-star label is above the horizontal arrow, as now coded in both layers. The mathematical codomains are assessed separately in ASTRA-EARLY-0014.'],
5:['author footnote, book title','Residues and Duality is plain upright type with no underline. Both attached layers now preserve this. The author note uses baseline literal(*).'],
6:['corollary, est combinaisons linéaire','The plural s is visibly printed after combinaisons, while the singular predicate and adjective require combinaison linéaire. Current already has the singular.'],
7:['corollary, closing parenthesis','No full stop follows the closing parenthesis. Both layers already omit it.'],
8:['definition of K(C_0), generating relation','The relation(E)−(E′)−(E″) and the following comma are in running text. The attached layers now have this identical formula inline; no additional layout variant is introduced.'],
9:['first paragraph, l’indicé','The main copy visibly carries an acute on the final e; native witness53 reads indice with clear blank space above e. Preserve the main-copy spelling diplomatically and use the noun indice, also attested by the witness, in current.'],
10:['second paragraph, A∈C_0','A comma follows the category symbol before les R^qF(A). Both attached layers already include it.'],
11:['category letters throughout pp42–45','The category glyph is a typed double-struck C, including C_0,C′,C_1,C_2; native witness53 confirms the doubled stroke. Replace the 27,30,23,1 occurrences of cC on inspected pp42,43,44,45 respectively with explicit mathbb{C} in both layers. No global macro definition is changed.'],
12:['boundary pp42/43','Page42 ends de C dans C′; p43 begins tel que. The attached marker correctly precedes tel que.'],
13:['Theorem2.3, à isomorphisme près','The whole parenthetical phrase is plain and heavier, outside the underline; the attached emphasis split preserves it.'],
14:['Theorem2.3(iii), first L','The first L after résolution gauche is plain, while L in Z_d(L) and in résolution finie is underlined. Diplomatic correctly has plain L here; current already restores the complex underline.'],
15:['Theorem2.3(iii), parenthetical definition of Z_d','The complete parenthetical definition is plain. The attached closing of emph before it is confirmed.'],
16:['Theorem2.3 conclusion, K(C_0) and K(C_1)','Both K symbols are plain with no underline. The attached diplomatic and current strings match.'],
17:['proof, homomorphismes surjectifs','A single underline is visible beneath surjectifs. The attached emphasis is correct.'],
18:['proof, ce qui est possible parenthesis','The opening parenthesis before ce qui remains unclosed. The dependency clause ends after(ii), before the semicolon and the next proof step; add its closing parenthesis there in current.'],
19:['proof, d’où E_C0(N)=0','This E is plain, while the surrounding Euler-characteristic symbols are underlined. Diplomatic now preserves the plain E; current already restores its underline.'],
20:['paragraph beginning On prouve','On prouve begins a fresh indented paragraph. The attached paragraph break matches; no new content variant is made.'],
21:['proof, construite est additive','The word additive has its own underline. The attached emphasis matches.'],
22:['primed complexes in proof','The underline stops beneath the L and does not extend under its primes. Change three underline{L′} and four underline{L″} to underline{L}′ and underline{L}″ in both layers, preserving the identical complex and prime sequence.'],
23:['boundary pp44/45','The corollary begins on p44 and its final line there ends O_x-module. Page45 begins de dimension cohomologique finie. The attached marker is correctly placed inside the statement group.'],
24:['p44 corollary, equivalence parenthesis','The parenthesis équivalente à la catégorie des fibrés vectoriels sur X is wholly plain, outside the underlined groups. The attached emphasis split matches. This passage belongs to physical folio44.'],
25:['formula(2.12)','The source K(ξ(X)) has both closing parentheses. Both attached layers already have the complete source expression; the replay item is stale.'],
26:['structure sheaf, p44 last line and p45','The structure-sheaf O is a plain typed O underlined: p44 O_x-module, p45 noethérien O_x and O(−n)^k. Replace the one cO on p44 and two on p45 by explicit underline{O} in both layers. No macro-wide redefinition is made.']}
save('evidence_041_045.json',{'findings_041_045.json':e})
patches=load('extra_patches.json')
def patch(p,layer,old,new,sid,reason,kind='misprint_correction',count=1):patches.append(dict(page=p,layer=layer,old=old,new=new,source_id=sid,reason=reason,kind=kind,expected_count=count))
patch(41,'current',r'au lieu de $\underline{K}(X)$',r'au lieu de $\underline{K}(\xi(X))$','fixes/MISPRINTS_6.json#73',e[3][1])
patch(42,'current',"l'indicé", "l'indice",'fixes/MISPRINTS_6.json#75',e[9][1])
patch(44,'current','(ce qui est possible grâce à (i) et (ii)~;', '(ce qui est possible grâce à (i) et (ii))~;','fixes/MISPRINTS_6.json#77',e[18][1])
patch(41,'current',r'A(Y) \arrow[r,"f^*"] & A(X).',r'\Atil(Y) \arrow[r,"f^*"] & \Atil(X).','ASTRA-EARLY-0014','Formula(2.6) gives the codomain of C-tilde as A-tilde. The map induced by f-star is [n,1+Σa_i]↦[n,1+Σf-star(a_i)]; together with(2.9) this gives the displayed commutative square in A-tilde. Restore the two omitted tildes in current.')
for p,n in [(42,27),(43,30),(44,23),(45,1)]:patch(p,'both',r'\cC',r'\mathbb{C}','check/findings/findings_041_045.json#11',e[11][1],'font',n)
for p,n in [(44,1),(45,2)]:patch(p,'both',r'\cO',r'\underline{O}','check/findings/findings_041_045.json#26',e[26][1],'font',n)
patch(44,'both',r"\underline{L'}",r"\underline{L}'",'check/findings/findings_041_045.json#22',e[22][1],'underline',3)
patch(44,'both',r"\underline{L''}",r"\underline{L}''",'check/findings/findings_041_045.json#22',e[22][1],'underline',4)
save('extra_patches.json',patches)
records=load('extra_decisions.json')
def rec(typ,p,sid,pr,region,reason,change,verdict='confirmed',**kw):records.append(dict(record_type=typ,page=p,source_id=sid,verdict=verdict,printed_reading=pr,image=f'scan/SGA6_scan_360dpi.pdf#page={p+14}',region=region,reason=reason,change=change,forms='French diplomatic and corrected; English where meaning or notation is affected',**kw))
rec('own_finding',41,'ASTRA-EARLY-0014','A(Y) → A(X)','bottom row of the commutative square','The primary and native witness52 both print plain A in the bottom row, while the vertical maps are C-tilde. Formula(2.6) defines C-tilde:K(ξ(X))→A-tilde(X). The induced map on A-tilde sends [n,1+Σa_i] to[n,1+Σf-star(a_i)]; formula(2.9) makes that square commute. Restore the tildes on the two bottom objects in current and retain plain A diplomatically.',{'old':'A(Y) → A(X)','new':'A-tilde(Y) → A-tilde(X)'},'not applied and now applied',related_pages=[40,41],witness_image='scan/SGA6_witness_300dpi.djvu#page=52')
rec('open_item',45,'fixes/REPLAY_MANUAL_6.json#2','K(ξ(X)) → K(F_0(X))','formula(2.12)','The scan includes both source parentheses. Both attached layers already contain K(ξ(X)); the old unbalanced string is absent because this correction has been placed.','Already applied; no additional patch.',related_finding='check/findings/findings_041_045.json#25')
rec('hold_difference',41,'fr/codex/HOLD_VS_CORR.json#31','i≥1','formula(2.8)',e[1][1],{'hold':'i≥1','corrected':'i>1'})
rec('hold_difference',42,'fr/codex/HOLD_VS_CORR.json#32','combinaisons linéaire','opening corollary',e[6][1],{'hold':'combinaisons linéaire','corrected':'combinaison linéaire'})
rec('typography_observation',35,'ASTRA-EARLY-TYPE-004','λ^i N and λ^q N with baseline N','first paragraph and Remarque a','The N has the ordinary running-text baseline and size; i and q alone are raised. Native witness46 directly confirms the first paragraph. Preserve λ^i N/λ^q N, not a subscript N. The hand-drawn lambda is vertically displaced but N is aligned with the adjoining text.','Existing notation retained.',witness_image='scan/SGA6_witness_300dpi.djvu#page=46')
save('extra_decisions.json',records)
pages=load('extra_pages.json');f=json.loads((R/'check/findings/findings_041_045.json').read_text())
for row in pages:
 if row['page']==35:row['witness_viewed']=True;row['notes']+=' Native witness46 subsequently read to confirm the baseline N in λ^i N and λ^q N.'
beg={41:'formula(2.8)',42:'Corollaire. Soit p',43:'tel que pour tout E',44:'alors f(A)',45:'de dimension cohomologique finie'}
for p in range(41,46):pages.append(dict(page=p,pdf_page=p+14,fully_checked=True,main_scan_viewed='four overlapping horizontal strips',witness_viewed=p in [41,42],findings_count=sum(z['page']==p for z in f),begins=beg[p],notes='All body text, formulas, diagram on p41 and its author note, statement boundaries, and folio splits compared directly. Witness52 resolves the detached marks after(2.10); witness53 confirms indice without the main-copy acute and the double-struck category glyph.'))
save('extra_pages.json',pages)
over=load('record_overrides.json')
for sid in ['check/findings/findings_041_045.json#24','fixes/FIXLOG_6.jsonl#127','fixes/FIXLOG_6_CURRENT.jsonl#112']:over[sid]={'page':44,'image':'scan/SGA6_scan_360dpi.pdf#page=58','original_record_page':45}
for i,pg in [(11,[42,43,44,45]),(22,[44]),(26,[44,45])]:over[f'check/findings/findings_041_045.json#{i}']={'related_pages':pg,'change':e[i][1]}
save('record_overrides.json',over)
