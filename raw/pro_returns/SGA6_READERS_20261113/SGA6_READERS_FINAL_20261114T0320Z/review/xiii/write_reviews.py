"""Direct scan collation of Exposé XIII. Explicitly reviewed findings only."""
from pathlib import Path
import json,re
R=Path(__file__).resolve().parents[2];O=R/'review/xiii';F={};D=[];P=[];OWN=[];STATUS=[]
for path in sorted((R/'check/findings').glob('*.json')):
 for i,x in enumerate(json.loads(path.read_text()),1):F[f'{path.name}#{i}']={**x,'source_id':str(path.relative_to(R))+f'#{i}'}
def f(n,printed,region,reason,verdict='confirmed',change=None,batch='616_620',page=None):
 x=F[f'findings_{batch}.json#{n}'];pg=x['page'] if page is None else page
 q=dict(record_type='checker',page=pg,source_id=x['source_id'],verdict=verdict,printed_reading=printed,image=f'scan/SGA6_scan_360dpi.pdf#page={pg+14}',region=region,reason=reason,change=change if change is not None else (x.get('fix') or {}).get('new','Retain inspected reading.'),forms='French forms; English where content changes',where=x['where'],kind=x['kind'])
 if pg!=x['page']:q['original_record_page']=x['page']
 D.append(q)
def patch(page,layer,old,new,sid,reason,kind='transcription',count=1):
 if old in (r'\mathcal O',r'\mathcal O_X') and new in ('O','O_X'):
  new='{O}'+new[1:]
  reason+=' Grouping the plain letter separates it from adjacent TeX control words without changing its displayed form.'
 P.append(dict(page=page,layer=layer,old=old,new=new,source_id=sid,reason=reason,kind=kind,expected_count=count))
def own(page,where,printed,tex,change,kind,reason,verdict='not applied and now applied'):
 sid=f'ASTRA-XIII-{len(OWN)+1:04d}';OWN.append(dict(record_type='own',page=page,source_id=sid,verdict=verdict,where=where,printed_reading=printed,tex=tex,change=change,kind=kind,reason=reason,image=f'scan/SGA6_scan_360dpi.pdf#page={page+14}',region=where,forms='French forms; English where content changes'));return sid
# pp.616–620 have each been read in two full-width overlapping image strips.
f(1,'EXPOSE XIII; capitalized title on separate line','heading p.616','The title has its own double underline and no full stop after XIII. The applied words and capitals match, with accented capitals retained by convention.')
f(2,'par S. KLEIMAN, underlined','author line','The surname is capitalized and the whole author line has an underline. Retain the applied form.')
f(3,'plain O_X in body, underlined O_X in p.616 footnote','structure sheaves pp.616–619','All four pages were inspected. Each body occurrence has a plain typed O; only the p.616 footnote has a short underline, confirmed in witness627. Preserve these local forms.','not applied and now applied','Local plain O_X, except underlined O_X in footnote616.')
f(4,'H^0(G(n+1) with one closing parenthesis','first diagram p.617, lower right','The final closing parenthesis is absent. Keep the diplomatic omission and the already supplied current parenthesis.')
f(5,'three baseline full stops','proof of1.4(i), arrow chain p.618','The three dots lie on the baseline, agreeing with the applied ldots.')
f(6,'par 2.3(i)','proof of1.4(i)','The source prints2.3. Proposition1.3(i) on p.616 explicitly states n-regularity for every n≥m, which gives the two vanishings used here by the definition1.1. Correct the reference to1.3(i) in current.','not applied and now applied','1.3(i)')
f(7,'par 2.3(ii)','first line p.619','The source prints2.3. The preceding-page beta_n is the multiplication map whose surjectivity is exactly Proposition1.3(ii) on p.616. Correct to1.3(ii) in current.','not applied and now applied','1.3(ii)')
f(8,'three baseline full stops','first paragraph, arrow chain p.619','The dots are low on the line. Keep the applied ldots.')
f(9,'mapsto n^1(F(n)), no argument before arrow','first paragraph p.619','The arrow has no source variable and the following letter is n. The preceding inequality concerns h^1(F(n)); the current n↦h^1(F(n)) completes that explicitly specified function. Keep it current-only.')
f(10,'sigma_1,...,sigma_i','(1.5.2), zero-scheme description','The final index has the stem and dot of i, confirmed in witness630. Both supplied layers already read i; no further replacement is needed.')
f(11,'sigma_1,...,sigma_i','1.6(i), zero-scheme description','The final index is again dotted i, confirmed in witness630. Both supplied layers already match.')
f(12,'double-struck A_k^N','first paragraph p.620','The A has an added parallel stroke. Keep the applied double-struck A.')
f(13,'T open in S, no prime','first paragraph p.620','Main and witness631 show no prime. The same sentence defines the parameter space as S′; T parametrizes the stated regular sequences inside that very S′. Supply the missing prime in current.','not applied and now applied',r"l'ouvert de \(S'\) correspondant")
f(14,'0 -> F(1) -> F -> G -> 0','Lemma1.7 p.620','The minus position is blank in both scans. The proof explicitly subtracts chi(F(n-1)), which is the additivity formula for the sequence with F(-1). Restore that minus in current only.','not applied and now applied','F(-1)')
for pg,old,new,sid in [(618,'par 2.3 (i).','par 1.3 (i).',554),(619,'par 2.3 (ii);','par 1.3 (ii);',555),(620,r"l'ouvert de \(S\) correspondant",r"l'ouvert de \(S'\) correspondant",557),(620,r'\(0\to F(1)\to F\to G\to0\)',r'\(0\to F(-1)\to F\to G\to0\)',558)]:patch(pg,'current',old,new,f'fixes/MISPRINTS_6.json#{sid}','Apply the individually read and contextually verified misprint correction.','misprint')
old=r"section donn\'ee de \(\mathcal O_X(1)\)";new=r"section donn\'ee de \(\underline{O}_X(1)\)";sid=own(616,'footnote','underlined O_X',old,new,'underline','The footnote alone has a visible underline under O, confirmed in witness627.');patch(616,'both',old,new,sid,'Restore the local underlined O.')
for pg,n in [(616,3),(617,4),(618,3),(619,5)]:
 sid=own(pg,'structure sheaves in body','plain typed O_X',r'\mathcal O_X','O_X','font','Every body occurrence was inspected; the O has no script flourish or underline. The footnote exception on616 is handled separately.');patch(pg,'both',r'\mathcal O_X','O_X',sid,'Preserve the local plain structure-sheaf letter.',count=n)
sid=own(619,'first paragraph','strictement underlined',r'\emph{strictement}',r'\uline{strictement}','underline','The adjective has a separate underline, while normalem renders emph as italics.');patch(619,'both',r'\emph{strictement}',r'\uline{strictement}',sid,'Preserve the printed underline.')
sid=own(616,'statements and defined terms pp.616–620','statement word groups underlined; defined m-régulier and (b)-faisceau unlined','emph wrappers, including nested defined-term emph','Coordinator: apply statement-underlining convention preserving unlined mathematics and defined terms','convention','The five pages exhibit the same pattern: statements underline words around unlined formulas, with the newly defined term left unlined. This records the observed local pattern for the volume convention without a blanket patch.','confirmed')
# Pages621–625: full main-page comparison; witness633 read for the m=0 line.
f(1,'sur s et h^0(F(-1))','proof1.8(i)','No comma occurs after s. The applied omission matches the image.',batch='621_625')
f(2,'G est un (b_i,...,b_{s-1},a_s)-faisceau','proof1.8(ii)','The first index has the dot and stem of i. The opening line makes G a (b_1,...,b_r)-faisceau, and replacing its final bound by a_s retains initial index1. Keep the current correction and diplomatic i.',batch='621_625')
f(3,'P_{-1}=0 without comma','definition1.9, first display line','No punctuation follows zero on the first line; the second line has its full stop. The applied reading matches.',batch='621_625')
f(4,"l’hypothèse de récurrence on voit",'proof1.11','The space after récurrence contains no comma. Applied reading matches.',batch='621_625')
f(5,'par1.8(i) car b_i≥0','proof1.11','The reference is followed directly by car, without comma. Applied reading matches.',batch='621_625')
f(6,'X_K et on dit','1.12, equivalence of classes','No comma follows X_K. Applied reading matches.',batch='621_625')
f(7,'X_T=X×_S T où T','1.12, bounding family','No comma intervenes before où. Applied reading matches.',batch='621_625')
f(8,'F_{k(t)} avec t∈T','1.12, bounding family','No comma follows F_{k(t)}; the subsequent semicolon is printed. Applied reading matches.',batch='621_625')
f(9,'F_K avec K algébriquement clos, qui','1.12, final sentence','The comma is after clos, with no comma after F_K. Applied reading matches.',batch='621_625')
f(10,'623 ends Alors,;624 starts le nombre des polynômes','boundary623/624','Both neighbouring page images were read; the supplied markers now place the boundary exactly there.',batch='621_625')
f(11,'derang, with no typed word space','first paragraph624','The letters are intact and the sole difference is spacing, explicitly excluded by CHECKER_PROMPT_SGA. Retain the two words de rang in both forms and remove this spacing-only apparatus item.','reverted','libre de rang',batch='621_625');D[-1]['misprint']=False
patch(624,'diplomatic','libre derang','libre de rang','check/findings/findings_621_625.json#11','Ignore spacing as instructed; no content correction or apparatus entry.','spacing')
f(12,'M=max(χ(F_K(m))','proof(iii)⇒(iv)','The image has three opening parentheses and only two closing ones. The existing current closing parenthesis completes the displayed maximum; retain the variant.',batch='621_625')
f(13,'par(i)⇒(iv) prenons','first line625','There is no comma after(iv). The applied reading is correct; the original record assigned this text to624 before the boundary moved.',batch='621_625',page=625)
f(14,'624 ends En effet,;625 starts par(i)⇒(iv) prenons','boundary624/625','Both page images were read; the supplied markers now divide the sentence at the printed break.',batch='621_625')
f(15,"L'_K→E'_K→E_K",'composition γ','The prime is printed. The preceding surjection L_1→E′ induces L_{1,K}→E′_K, and γ=β composed with this map is lifted by δ:L_{1,K}→L_K. Thus the source of this composition is exactly L_{1,K}; apply that correction only in current.','not applied and now applied',r"L_{1,K}\to E'_K\to E_K",batch='621_625')
patch(625,'current',r"L'_K\to E'_K\to E_K",r"L_{1,K}\to E'_K\to E_K",'fixes/MISPRINTS_6.json#590','Use the explicitly defined base-changed surjection L_{1,K}→E′_K.','misprint')
f(16,'u_K∘α','map from L_{1,K}⊕L_{2,K}','The small circle between u_K and α is visible. The applied composition symbol matches.',batch='621_625')
f(17,'underlined Hom, plain O_{X_T}','second paragraph, donc Hom','The underline lies under Hom and stops before the plain O. Keep the applied Hom underline; structure-sheaf font is corrected separately.',batch='621_625')
f(18,'underlined Hom after R^q(f_T)_*','second paragraph, higher direct images','The second Hom has its own underline. R is plain and its superscript is q. Keep the applied Hom form.',batch='621_625')
f(19,'underlined Hom after G=(f_T)_*','second paragraph, definition of G','The third Hom is underlined. The applied form matches.',batch='621_625')
f(20,'double-struck V(G^*)','second paragraph, definition of R','V has a separate doubled left stroke. The applied double-struck V matches the print.',batch='621_625')
f(21,'625 ends désigne par;626 begins the intersection-number formula','boundary625/626','The lower strip625 and upper strip626 were read directly. The supplied marker is now before the opening angle bracket, as printed.',batch='621_625')
sid=own(622,'proof1.11, r=0','m=0',r"c'est clair car \(m=0\)",r"c'est clair car \(m\ge0\)",'misprint','Both main PDF636 and witness633 print equality. Definition1.9 gives P_0(X_0)=X_0 because P_{-1}=0 and binom(-1,0)=1; hence m=c_0≥b_0−a_0≥0 by1.8. For a length-one skyscraper with a_0=b_0=1 and permitted c_0=1, m=1. The asserted equality is therefore false; the required and proved assertion is m≥0.');patch(622,'current',r"c'est clair car \(m=0\)",r"c'est clair car \(m\ge0\)",sid,'Replace the incorrect equality by the proved nonnegativity.','misprint')
for pg,n in [(622,1),(623,6),(624,3),(625,9)]:
 sid=own(pg,'structure sheaves','plain typed O',r'\mathcal O','O','font','Every occurrence on this page was compared. The typed O is plain, including the subscripts under Hom on625.');patch(pg,'both',r'\mathcal O','O',sid,'Preserve the local plain structure-sheaf letter.',count=n)
for old,new in [(r'\emph{famille de classes de faisceaux cohérents sur les fibres de \(X/S\)}',r'\uline{famille de classes de faisceaux cohérents sur les fibres de} \(X/S\)'),(r'\emph{limitée par le faisceau cohérent}',r'\uline{limitée par le faisceau cohérent}'),(r'\emph{sur}',r'\uline{sur}'),(r'\emph{limitée}',r'\uline{limitée}'),(r'\emph{famille}',r'\uline{famille}')]:
 sid=own(622,'defined phrases in1.12','word group underlined; X/S unlined',old,new,'underline','The image shows a ruled underline under this word group; mathematical X/S is outside the first underline.');patch(622,'both',old,new,sid,'Keep the actual defined-phrase underline.')


# Pages626–630: every line and formula compared directly with the main images.
f(1,'opening angle bracket of the intersection number begins626','boundary625/626','625 ends désigne par and626 starts the formula. The current marker is exact.',batch='626_630')
f(2,'c(L), with no subscript1','proof2.4','The first c on the line lacks an index; the other two c_1 terms have it. The expression is d(L), defined in2.2 as the intersection with c_1(L), so the existing current correction is the intended first Chern class.',batch='626_630')
f(3,'Par1.7 et2.6','proof2.7','The printed reference is2.6. The immediately preceding lemma2.5 states the (0,...,a_r)-bound used for L_Y; its proof on this same page explicitly supplies the curve case (0,a_1). Correct this reference to2.5 in current.','not applied and now applied','Par1.7 et2.5',batch='626_630')
patch(627,'current','Par 1.7 et 2.6,','Par 1.7 et 2.5,','fixes/MISPRINTS_6.json#592','The curve restriction and its bound are exactly Lemma2.5.','misprint')
f(4,'h^2(L(-a_1-2)=0','first line628','One closing parenthesis is printed. Keep the omission diplomatically and the already restored parenthesis in current.',batch='626_630')
f(5,'+β(β+1)','Lemma2.8, final term of displayed bound','The plus is clear. The same-page identity is a_0=2α_2+2α_0−Σ_{i≥1}a_i binom(δ−1+i,i)−β_0, with β_0≤β(β+1). Substitution therefore gives the negative final term in the lower bound. Apply that sign correction in current.','not applied and now applied',r'-\beta(\beta+1)',batch='626_630')
patch(628,'current',r'+\beta(\beta+1).',r'-\beta(\beta+1).','fixes/MISPRINTS_6.json#594','Substitute the displayed upper bound on β_0 into the identity containing −β_0.','misprint')
f(6,'−β_0 et comme','proof2.8','There is no comma before et comme. The applied reading matches.',batch='626_630')
f(7,'underlined Ext','definition of ω','The line under Ext is visible; its O_P subscript is plain. Keep the applied Ext underline; local O is handled separately.',batch='626_630')
f(8,'h^1(L(n))=0','proof2.9(i), penultimate paragraph629','The print has no minus sign. In2.9.1 the two end groups vanish for n≥2+h_2, yielding isomorphisms H^1(L(-n-1))→H^1(L(-n)); the cited eventual vanishing must concern these same negatively twisted groups to complete(i). Restore the missing minus in current.','not applied and now applied',r'h^1(L(-n))=0\) (voir FGA',batch='626_630')
patch(629,'current',r'h^1(L(n))=0\) (voir FGA',r'h^1(L(-n))=0\) (voir FGA','fixes/MISPRINTS_6.json#595','Complete the displayed chain of isomorphisms between the negatively twisted cohomology groups.','misprint')
f(9,'630 begins déjà prouvé','boundary629/630','The lower strip629 ends Donc par(i), and630 begins déjà. The supplied boundary now matches.',batch='626_630')
f(10,'630 ends after the last displayed binomial;631 starts on ait','boundary630/631','The entire630 lower strip and631 upper strip were read. The supplied marker is already after the display.',batch='626_630')
f(11,'no punctuation after the final binomial','last display630','The region after the final right parenthesis is blank. Both supplied layers already omit the comma. Parent owns the duplicate manual-source decision.',batch='626_630')
f(12,'quelque soit','first line630','The print joins quelque. In the concessive construction governed by soit, quel agrees with the subject m and que introduces the clause; correct the lexical form to quel que soit in current.','not applied and now applied','quel que soit',batch='626_630')
patch(630,'current','quelque soit','quel que soit','fixes/MISPRINTS_6.json#596','Correct the concessive grammatical construction.','misprint')
f(13,'binom(m−1+i,j)','Remarque2.10, second display','The top index is dotted i. The exact change-of-basis identity is binom(m+n+q,q)=Σ_{i=0}^q binom(m−1+q−i,q−i) binom(n+i,i); setting q=j+i gives binom(m−1+j,j). For r=1 the translated constant coefficient is a_0+m a_1, also forcing this correction.','not applied and now applied',r'\binom{m-1+j}{j}',batch='626_630')
patch(630,'current',r'\binom{m-1+i}{j}',r'\binom{m-1+j}{j}','fixes/MISPRINTS_6.json#597','Use the explicit translation identity for the binomial polynomial basis.','misprint')
sid=own(626,'Lemma2.5, parenthetic count','avec r−1 zéros',r'avec \(r-1\) zéros',r'avec \(r\) zéros','misprint','The tuple (b_0,...,b_r)=(0,...,0,a_r) has one zero for every index0,...,r−1, hence r zeros. The proof on627 explicitly gives (0,a_1) for r=1 and adjoins the initial zero in the induction.');patch(626,'current',r'avec \(r-1\) zéros',r'avec \(r\) zéros',sid,'Correct the number of zero entries to the count proved on the next page.','misprint')
for pg,n in [(626,5),(629,2)]:
 sid=own(pg,'structure sheaves','plain typed O',r'\mathcal O','O','font','All structure-sheaf letters on this page were inspected and are plain, without script flourishes or underline.');patch(pg,'both',r'\mathcal O','O',sid,'Preserve the plain structure-sheaf letter.',count=n)
sid=own(626,'definition of degree','degré underlined',r'\emph{degré}',r'\uline{degré}','underline','The defined noun has a separate underline.');patch(626,'both',r'\emph{degré}',r'\uline{degré}',sid,'Preserve the printed defined-term underline.')
sid=own(626,'2.1 intersection-number and Snapper-polynomial formulas','three baseline dots',r'\cdots',r'\ldots','symbol','All three ellipses lie at the baseline: between c_1 factors, between n variables, and between tensor factors.');patch(626,'both',r'\cdots',r'\ldots',sid,'Use baseline ellipses as printed.',count=3)


# Pages631–635 fully compared; witness642/643/645 clarifies raised o, stray dot and I.
f(1,'631 begins on ait','boundary630/631','The last display is wholly on630, followed on631 by on ait. The supplied boundary matches.',batch='631_635')
f(2,'no punctuation after binom(mn+j,j)','last display630','The blank after the binomial was inspected on630; both attached layers already omit the comma. Parent owns the manual duplicate.',batch='631_635',page=630)
f(3,'un S schéma projectif','Lemma2.11','The print has no hyphen. CHECKER_PROMPT_SGA excludes hyphenation from errors; the phrase still gives precisely the same projective S-scheme and structure morphism. Keep the authors’ wording in both layers, without a hyphenation-only variant.','reverted',r'un \(S\) schéma projectif',batch='631_635');D[-1]['misprint']=False
f(4,'supp{d(L_K)}','proof2.11','The print has two p letters. The argument chooses an integer upper bound on all degrees and subtracts it by twisting; this is the supremum. The existing current sup correction matches that explicitly stated operation.',batch='631_635')
f(5,'full stop after the footnote call','Lemma3.1, before Alors','The period is outside the underline and after(*), visible in main and witness642. The applied period matches.',batch='631_635')
f(6,'n with raised small o','footnote631','The small upper glyph is above the n baseline in both scans; witness642 confirms its raised position. Keep the applied numéro form.',batch='631_635')
f(7,'plain O in H=O_X(1) and the two trivializations on632','structure sheaves631–632','All three locations were read. No underline or script flourish is present; local plain-O patches implement the exposé notation.',batch='631_635')
f(8,'632 begins quasi-compacts et quasi-séparés','boundary631/632','631 ends de S-schémas;632 starts the adjectives. The supplied marker already matches the images.',batch='631_635')
f(9,'inductive limit with arrow and no α index','left side3.1.1','No index is printed below the arrow. The applied varinjlim without subscript matches.',batch='631_635')
f(10,'projective limit with arrow and no α index','right side3.1.1','The α belongs only to Z_α. The applied limit without added subscript matches.',batch='631_635')
f(11,'image inverse de L_α','proof3.1, first paragraph','The prime position is blank. The map X_{Z′}→X_{Z′_α} pulls back the explicitly defined L′_α to L′; restore that prime in current.','not applied and now applied',r"image inverse de \(L'_\alpha\)",batch='631_635')
patch(632,'current',r'image inverse de \(L_\alpha\)',r"image inverse de \(L'_\alpha\)",'fixes/MISPRINTS_6.json#600','Use the defined line bundle in the displayed base-change pullback.','misprint')
f(12,'round stop immediately after the subscript α','proof3.1, second paragraph','A round mark at the subscript baseline persists in main and witness643, immediately after L′_α. It interrupts the phrase image inverse de ... sur and has no formula role. Preserve the visible stop diplomatically and the existing current omission.',batch='631_635')
f(13,'633 begins item(ii)','boundary632/633','632 ends after item(i); the(ii) label begins633. The supplied marker is above its item command, matching the print.',batch='631_635')
f(14,'Quant à(iii) begins a new paragraph','proof3.2','The source indents Quant on a new line. The applied paragraph division agrees; it introduces no text variant.',batch='631_635')
f(15,'Réciproquement begins a new paragraph','proof3.2','The new indented paragraph is visible. Retain the applied layout without an apparatus variant.',batch='631_635')
f(16,'est dit underlined; de type fini unlined; si... underlined','definition3.3','The underline stops before the defined term and restarts with si. The applied separation preserves that distinction.',batch='631_635')
f(17,'Ia famille, capital I','proof3.4','Witness645 enlarged beside un L shows the first letter of Ia with equal short upper and lower serifs, while L has its long rightward foot. The word is a typed I-for-L slip. Keep the diplomatic I and existing current La.',batch='631_635')
f(18,'La réciproque begins a new paragraph','proof3.4','The new paragraph is explicitly indented. The applied paragraph break matches the layout.',batch='631_635')
f(19,'Pic morphism appears inline','proof3.5','The source sets the morphism within the sentence. The applied inline placement agrees and adds no content variant.',batch='631_635')
f(20,'coproduct sign without lower index','last line635','The visible i belongs to X_i; the coproduct sign has no index. The applied removal matches.',batch='631_635')
f(21,"tous les X_i/S′, without prime on X",'last paragraph635','The components are explicitly named X′_i two lines earlier. Each inclusion X′_i→X_{S′}, followed by the coproduct map, gives the surjection used in the next step; restore the same component names in current.','not applied and now applied',r"tous les \(X'_i/S'\)",batch='631_635')
f(22,"coproduct X_i/S′, without prime on X",'last line635','This is the coproduct of the X′_i defined above, with its canonical surjection to X_{S′}. Restore the prime together with the preceding occurrence.','not applied and now applied',r"\coprod X'_i/S'",batch='631_635')
patch(635,'current',r"tous les \(X_i/S'\)",r"tous les \(X'_i/S'\)",'fixes/MISPRINTS_6.json#603','Name the components already defined as X′_i.','misprint')
patch(635,'current',r"\coprod X_i/S'",r"\coprod X'_i/S'",'fixes/MISPRINTS_6.json#604','Use the same components in their canonical coproduct.','misprint')
for pg,n in [(631,1),(632,2)]:
 sid=own(pg,'structure sheaves','plain typed O',r'\mathcal O','O','font','Every occurrence was inspected; O is plain and unlined.');patch(pg,'both',r'\mathcal O','O',sid,'Preserve the local plain structure-sheaf letter.',count=n)


# Pages636–640 fully read; witness650/651 read for accent, tau and diagram strokes.
f(1,'sur un X_T avec T','proof3.6','No comma occurs after X_T; the comma following sur S is printed. The applied reading matches.',batch='636_640')
f(2,'plain O at all eight specified locations','structure sheaves636,638,639','All eight occurrences were read on their pages; none is script or underlined. The local plain-O patches implement this observed form.',batch='636_640')
f(3,'636 ends On;637 begins suppose que','boundary636/637','Both neighbouring strips were read. On belongs to636 and the supplied boundary now matches.',batch='636_640')
f(4,'De plus begins an indented paragraph','statement3.8','The source begins a separate paragraph after est de type fini. Retain the applied paragraph division.',batch='636_640')
f(5,'schema, no acute accent','Lemma3.9, first line','The first e has blank space above it, while the later schéma in the same statement has an acute. Preserve the diplomatic omission and existing current accent.',batch='636_640')
f(6,'S′_α-morphisme','proof3.9','A prime is printed. The preceding object X′ is an S_α-scheme and its displayed map X′→X_{S_α} is the model over S_α of X′_K→X_K. Correct the base label to S_α in current.','not applied and now applied',r'S_\alpha',batch='636_640')
patch(638,'current',r"d'un \(S'_\alpha\)-morphisme",r"d'un \(S_\alpha\)-morphisme",'fixes/MISPRINTS_6.json#606','Use the specified base of both source and target of the modeled morphism.','misprint')
f(7,'Abhyankhar','Remarque3.10','The extra h is printed. Bibliography entry[1] on666 (main PDF680, author/title region inspected separately) spells the same resolution author Abhyankar. Correct the name in current.','not applied and now applied','Abhyankar',batch='636_640')
patch(638,'current','Abhyankhar','Abhyankar','fixes/MISPRINTS_6.json#607','Use the spelling in the exposé’s bibliography entry[1].','misprint')
f(8,'graĉe, circumflex above c','proof3.8, reference2.10','Both main and witness650 place the circumflex above c; the earlier grâce on the page has it over a. Retain the diplomatic misplaced accent and existing current grâce.',batch='636_640')
f(9,'Pic_{Y/k}→Pic_{X/k} inline','Lemma3.11','The arrow formula is part of the statement line before resp. The applied inline placement agrees.',batch='636_640')
f(10,'Pic with raised typed τ at both ends','Lemma3.11, parenthetic morphism','The small top bar curls down at the left, as seen clearly in witness650; the symbol is the τ used for this subgroup. Keep the applied tau superscripts.',batch='636_640')
f(11,'Pic^τ_{Y/k}','last line639','The same curled-bar tau occurs here. The applied tau matches.',batch='636_640')
f(12,'Pic^τ_{Y/k}','first line640','The raised symbol has the same tau form as639, confirmed in witness651. Keep the applied tau.',batch='636_640')
sid=own(639,'conclusion of the first part of3.8','Par conséquent L est limitée',r"Par cons\'equent \(\mathcal L\) est limit\'ee en vertu de 2.11",r"Par cons\'equent \((f^*)^{-1}(\mathcal L)\) est limit\'ee en vertu de 2.11",'misprint','The map is f*:Pic_{Y/S}→Pic_{X/S}. Page638 fixes a bounded family L on X; the displayed coefficients on639 belong to M_K in its inverse-image family (f*)^{-1}(L) on Y. Lemma2.11 applies to those M_K and proves boundedness of exactly that inverse image, which is the assertion required by Definition3.3. Main and witness650 print only L in the conclusion.');patch(639,'current',r"Par cons\'equent \(\mathcal L\) est limit\'ee en vertu de 2.11",r"Par cons\'equent \((f^*)^{-1}(\mathcal L)\) est limit\'ee en vertu de 2.11",sid,'Name the family whose Hilbert coefficients were bounded and to which2.11 is applied.','misprint')
for pg,n in [(636,3),(638,1),(639,4)]:
 sid=own(pg,'structure sheaves','plain typed O',r'\mathcal O','O','font','All occurrences were compared; they have plain typed O.');patch(pg,'both',r'\mathcal O','O',sid,'Preserve the local plain structure-sheaf letter.',count=n)
sid=own(640,'Remarque3.12(i)','unipotent underlined',r'\emph{unipotent}',r'\uline{unipotent}','underline','The adjective has a separate underline outside any statement wrapper.');patch(640,'both',r'\emph{unipotent}',r'\uline{unipotent}',sid,'Preserve the printed underline.')


# Pages641–645 fully compared; upper646 inspected for boundary and display punctuation.
f(1,'first Hom underlined, second Hom plain','opening two isomorphisms641','The first underline stops under Hom before gr; the next Hom is unlined. Retain the applied distinction between the two displayed isomorphisms.',batch='641_645')
f(2,'first H underlined, second H plain','opening two isomorphisms641','H has a short underline in the first isomorphism and none in the second. The applied form matches.',batch='641_645')
f(3,'sont ample','Theorem3.13(iv), final words','The printed adjective has no final s. Its subject is the two explicitly listed invertible sheaves, joined by et, and the verb is plural sont. Correct the agreement in current.','not applied and now applied','sont amples.',batch='641_645')
patch(641,'current','sont ample.}','sont amples.}','fixes/MISPRINTS_6.json#616','Restore plural agreement with the two sheaves.','misprint')
f(4,'χ(L_t^{⊗m}(n)) ne dépend','first paragraph642','No comma follows the closing parenthesis. The applied omission matches.',batch='641_645')
f(5,'N.c_1(H_K) in the first bracket only','third paragraph642','A typed product dot follows N in the first inequality; the later squared bracket has no such dot. Keep the applied localized product sign.',batch='641_645')
f(6,'643 begins(i). D’autre part','boundary642/643','642 ends ainsi(ii) implique; the complete(i) and D’autre part begin643. The supplied marker now matches.',batch='641_645')
f(7,'Pic underlined separately from the title words','section4 heading','The underline under Pic is separated from the underline under pour and stops before the subscript. It is the same functor notation used in the body. Retain the applied underline.',batch='641_645')
f(8,'un k-schéma connexe Z','4.1','The letter is small k, clear in main and witness654. The preceding field is K and z,z_0 are maps Spec(K)→Z whose composites with g:Z→G are compared in G(K); the connected parameter scheme is over that same K. Correct k to K in current.','not applied and now applied',r"il existe un \(K\)-sch\'ema connexe \(Z\)",batch='641_645')
patch(643,'current',r"il existe un \(k\)-sch\'ema connexe \(Z\)",r"il existe un \(K\)-sch\'ema connexe \(Z\)",'fixes/MISPRINTS_6.json#617','Use the algebraically closed field specified for the two parameter points.','misprint')
f(9,'Il est évident starts a new paragraph','4.1','The second paragraph is indented. The applied division matches the page.',batch='641_645')
f(10,'Φ(G′^τ)⊃G^τ, no inverse exponent','first line644','The missing exponent is visible. The map Φ:G→G′ sends G^τ into G′^τ by4.1; pulling back that inclusion gives G^τ⊂Φ^{-1}(G′^τ), the half of4.2 being recalled. Keep the existing current inverse-image correction.',batch='641_645')
f(11,'Proposition4.5. (Comportement fonctoriel).','heading645','The full stop after4.5 is printed. The applied label matches.',batch='641_645')
f(12,'4.5.1. without parentheses','projection-formula label','The label has a final stop and no parentheses. The applied tag* reproduces it; its left position is layout.',batch='641_645')
f(13,'no punctuation after the final intersection bracket','formula4.5.1','The rightmost angle bracket is followed by blank space. The applied removal of the comma matches.',batch='641_645')
f(14,'lorsque f est surjective','second paragraph of proof4.5','The feminine adjective is printed. The same map f can be referred to as an application, and its surjectivity condition is unchanged; the record itself acknowledges this normal usage. Preserve the authors’ wording in both forms instead of enforcing masculine agreement.','reverted',r'lorsque \(f\) est surjective,',batch='641_645');D[-1]['misprint']=False
patch(645,'current',r"R\'eciproquement, lorsque \(f\) est surjectif, \'etant donn\'ee",r"R\'eciproquement, lorsque \(f\) est surjective, \'etant donn\'ee",'check/findings/findings_641_645.json#14','Retain the authors’ legitimate feminine reference to the application f.','reversion')
f(15,'Théorème4.6. (La caractérisation...)','heading645','A stop follows4.6 before the opening parenthesis. The applied label matches.',batch='641_645')
f(16,'Pic underlined inside the theorem title','heading4.6','The short underline belongs to Pic separately from the title words and ends before X/k. Retain the applied functor notation.',batch='641_645')
f(17,'χ(F⊗L)=χ(F), no semicolon','first display646','The top strip646 was read directly; no punctuation follows the equality. Both attached layers already match; parent owns the duplicate manual-source decision.',batch='641_645',page=646)
f(18,'646 begins with the χ equality','boundary645/646','645 ends item(ii) at on a;646 starts its display, followed by(iii). The supplied marker already matches.',batch='641_645')
sid=own(644,'Lemma4.3, hyperplane-section parenthesis','no dimension hypothesis; proof invokes3.8',r"d'un faisceau ample \(\mathcal O_Y(1)\)). Alors",r"d'un faisceau ample \(\mathcal O_Y(1)\), sous les hypothèses de 3.8). Alors",'mathematical_source_correction','The §4 opening (643) imposes no governing dimension hypothesis:4.1 introduces arbitrary S and a commutative group functor;4.2 assumes geometric-fibre representability and finite-type Φ_K. Lemma4.3 separately introduces proper X,Y/S. Its hyperplane-section parenthesis omits the hypotheses of the theorem3.8 explicitly invoked in its proof. Theorem3.8 (636–637) assumes noetherian S, projective Y with the specified ample O_Y(1), X its section zero-scheme, and dimension at least2 for every X_s∩Y_s^i; it concludes that f*:Pic_{Y/S}→Pic_{X/S} is of finite type. That finite-type pullback is the hypothesis needed in4.2 to identify the inverse image of the τ subgroup. For the printed unrestricted claim, take Y=P¹_k and X a hyperplane point: f*:Pic(P¹_k)=Z→Pic(X)=0 is zero, so the inverse image of Pic^τ(X)=0 is Z, whereas Pic^τ(P¹_k)=0. Both the page context and this explicit counterexample confirm the missing qualification. The current-only insertion refers to the full established hypotheses of the cited3.8; it is a substantive mathematical source correction, not a typographic emendation. Coordinator independently inspected the relevant source regions and concurred.');patch(644,'current',r"d'un faisceau ample \(\mathcal O_Y(1)\)). Alors",r"d'un faisceau ample \(\mathcal O_Y(1)\), sous les hypothèses de 3.8). Alors",sid,'Restore the full hypotheses of the theorem already invoked by the proof, whose finite-type pullback conclusion permits4.2.','misprint')

for pg,n in [(641,2),(642,1),(644,2),(645,1)]:
 sid=own(pg,'structure sheaves','plain typed O',r'\mathcal O','O','font','Every structure-sheaf O on this page was compared and is plain, without underline.');patch(pg,'both',r'\mathcal O','O',sid,'Preserve the local plain structure-sheaf letter.',count=n)
for term in [r"alg\'ebriquement \'equivalent",r"\'equivalent",r"num\'eriquement \'equivalent"]:
 old=r'\emph{'+term+'}';new=r'\uline{'+term+'}';sid=own(644,'defined terms in4.4','word group underlined',old,new,'underline','Each defined phrase has a separate underline; the τ preceding the second phrase remains unlined.');patch(644,'both',old,new,sid,'Preserve the printed defined-term underline.')


# Pages646–650 fully compared with both full-width strips of each main page.
f(1,'χ(F⊗L)=χ(F), no following punctuation','first display646','The blank after the final parenthesis is clear. Both supplied layers already match; the coordinator owns the duplicate manual-source adjudication.',batch='646_650',page=646)
f(2,'646 begins with the χ(F⊗L)=χ(F) display','boundary645/646','The display begins646, following on a at the bottom of645. The supplied marker now matches.',batch='646_650')
f(3,'χ(L^{⊗m}(n))=χ(O_X(n)), no following punctuation','Theorem4.6(v)','There is no semicolon after the equality. The applied omission matches the print.',batch='646_650')
f(4,'X×_kT où T est connexe','proof4.6(i)⇒(ii)','The source has no comma between T and où. Retain the applied omission.',batch='646_650')
f(5,'plain typed O, including the standalone O in deforming L','structure sheaves646 and649','The seven occurrences on646 and two on649 were all read. Each O is plain and unlined; local font patches preserve those forms.',batch='646_650')
f(6,'baseline product dots in all four intersection pairings','4.6(vi) and proof(ii)⇒(iii)','All four product dots are present. The retained TeX cdot denotes the same intersection product: first multiply the first-Chern classes (or intersect c_1(L) with the curve class Y), then apply the displayed degree pairing. Its vertical placement follows the transcription’s typeset multiplication convention and creates no added or removed operator.','retained convention','Keep the four existing product operators.',batch='646_650')
f(7,'647 begins en vertu de4.5','boundary646/647','646 ends alors;647 begins en. The applied marker is exact.',batch='646_650')
f(8,'Il reste donc starts an indented paragraph','proof4.6','The source visibly begins a new paragraph after(X4.4.1). The applied division agrees.',batch='646_650')
f(9,'L^{⊗r} et L^{⊗q}','proof4.6, connected component argument','The first exponent is r. The two chosen integers are p,q and the quotient L^{⊗p}⊗(L^{⊗q})^{-1}=L^{⊗(p−q)} is the line bundle in the conclusion. Retain diplomatic r and the existing current p.',batch='646_650')
f(10,'648 begins est aussi représentable','boundary647/648','The(ii) sentence and Pic morphism begin on647; the predicate begins648. The supplied marker already matches.',batch='646_650')
f(11,'on a donc établit(a)','proof4.7, second paragraph','The final t is printed. After the auxiliary a the past participle is établi; keep the existing current correction.',batch='646_650')
f(12,'coproduct X′_i→X_S, no prime on S','proof4.7, canonical surjection','The target subscript has no prime; its following mark is the sentence stop. The X′_i were just defined as components of X_{S′}, and the displayed canonical coproduct map is the union of their inclusions into X_{S′}. Keep that established current target.',batch='646_650')
f(13,'Soit O_X(1) continues the same paragraph','last paragraph649','Soit follows the preceding stop on the same line. The applied paragraph join matches.',batch='646_650')
f(14,'(Pic^τ_{X/S})_K, with plain unlined Pic','proof5.1, connected-component count','The source has no underline here. The paragraph explicitly chooses a representing S-scheme P for the Picard functor; the representability isomorphism h_P≅Pic^τ_{X/S} identifies its K-fibre with the scheme whose connected components are being counted. This establishes the exact relation supporting the authors’ plain scheme notation. An added underline is unnecessary; retain the printed form in both layers and remove the putative misprint.','reverted',r'\((\Pic^\tau_{X/S})_K\)',batch='646_650');D[-1]['misprint']=False
patch(650,'current',r'\((\underline{\Pic}^\tau_{X/S})_K\)',r'\((\Pic^\tau_{X/S})_K\)','check/findings/findings_646_650.json#14','Retain the printed scheme notation, linked to the preceding functor by its explicitly assumed representability.','reversion')
f(15,'Si r est≥2 starts an indented paragraph','proof5.1, last paragraph650','The new paragraph is visible. The applied division agrees.',batch='646_650')
for pg,n in [(646,7),(649,2)]:
 sid=own(pg,'structure sheaves','plain typed O',r'\mathcal O','O','font','All occurrences on this page were compared and have plain O, without underline or script form.');patch(pg,'both',r'\mathcal O','O',sid,'Preserve the local plain structure-sheaf letter.',count=n)
for term in [r"ferm\'ee",r"repr\'esentable"]:
 old=r'\emph{'+term+'}';new=r'\uline{'+term+'}';sid=own(650,'Remarque4.8','word underlined',old,new,'underline','Each emphasized adjective has a separately drawn underline in the source.');patch(650,'both',old,new,sid,'Preserve the printed underline.')


# Pages651–655 fully read; witness662 and665 resolves the capital U and raised mark.
f(1,'inverse-limit arrow with no index below it','definition of étale cohomology651','No ν is printed beneath the arrow, in main and witness662. Keep the applied unindexed inverse limit.',batch='651_655')
f(2,'KUnneth, capital-height U with no detached diaeresis dots','proof5.2','Main and witness662 show the capital-height U. NOTE_6 permits restoring accents on typed capitals, so diplomatic KÜnneth preserves that capital while current Künneth supplies the correct internal lower-case letter. The coordinator concurred with this explained local treatment.',batch='651_655')
f(3,'〈b.a_1〉 followed by 〈b,a_m〉','last formula651','Both the dot and the final comma are clear in main and witness662. The following words define the brackets as the intersection number; the exact bilinear map is (b,a)↦deg(b·a), so comma-separated arguments and product-dot notation evaluate to the same integer. Retain the authors’ two notations and reject a consistency-only punctuation replacement.','rejected',r'\langle b,a_m\rangle',batch='651_655');D[-1]['misprint']=False
f(4,'C^1_mum(X)','Remarque5.3','The first index letter has the three stems of m. The group is the C^p_num defined in5.2, with p=1; keep the existing current num correction.',batch='651_655')
f(5,'dûe, circumflex on u','Remarque5.3','The circumflex is printed over u. The feminine past participle is due; keep the existing current correction.',batch='651_655')
f(6,'Néron-Severi, no acute on Severi','Theorem5.4','No accent is printed on the first e of Severi. The applied unaccented form matches.',batch='651_655')
f(7,'tensor sign followed by Q, with no subscript','proof5.4','There is no Z below the tensor sign. The applied omission matches.',batch='651_655')
f(8,'double-struck P in P=P^N_k','section6 heading','The second P has a doubled vertical stem. The applied mathbb form matches.',batch='651_655')
f(9,'double-struck P in P=P^N_k','6.1 first sentence','The projective-space P has the same doubled stem as in the heading. The applied mathbb form matches.',batch='651_655')
f(10,'plain typed O at all twelve specified locations','structure sheaves653–655','All twelve occurrences were read on the three pages. None has an underline or script flourish; local font patches implement the observed form.',batch='651_655')
f(11,'654 begins En effet','boundary653/654','The complete En effet begins654;653 ends after the sentence about M_1. The supplied marker is exact.',batch='651_655')
f(12,'M=Σ a_i binom(m+i,i), bare summation sign','proof6.3','No summation index is printed here. The applied omission matches.',batch='651_655')
f(13,'raised compact multiplication mark between M and the binomial','proof6.3, formula for M_1','The mark is visible in both main and witness665; the enlarged witness region shows a compact overstruck mark rather than an additional letter or a multi-ray asterisk. Retain its representation as the multiplication dot. The surrounding formula explicitly computes the product of M with the Euler characteristic binom(p+N,N).',batch='651_655')
f(14,'bare summation sign in the formula for M_1','proof6.3','No index is printed below this second sum sign either. The applied omission matches.',batch='651_655')
f(15,'(=χ(I(p)), missing final parenthesis','proof6.3, formula ending','There are three opening parentheses and two closing ones, followed by the stop. Keep the diplomatic omission and existing current closing parenthesis.',batch='651_655')
f(16,'full stop after the bottom zero row','diagram in proof6.4','The stop is at the right of the bottom row. The applied diagram punctuation matches.',batch='651_655')
f(17,'L’assertion(i) begins an indented paragraph','proof6.4','The source begins a new paragraph after d’où(i). The applied division agrees.',batch='651_655')
f(18,'graĉe, circumflex above c','last line of proof6.4','The circumflex is centered above c, with none over a. Keep the diplomatic displaced accent and the existing current grâce.',batch='651_655')
f(19,'O_X.σ with baseline product dot','proof6.5','The full stop between O_X and σ is visible. The applied baseline dot matches; the ambient-scheme subscript is adjudicated separately.',batch='651_655')
f(20,'dim.supp(F′), full stop after dim','proof6.5','The abbreviation stop is clearly present. The applied stop matches.',batch='651_655')
f(21,'full stop after the bottom diagram row','diagram in proof6.5','The final stop is visible at the right of the bottom row. The applied punctuation matches.',batch='651_655')
f(22,'655 ends with the diagram;656 begins De s≥1','boundary655/656','Both neighbouring pages were read directly. The supplied marker now precedes De and résulte is joined correctly.',batch='651_655')
sid=own(655,'proof6.5, definition of F′','F′=O_X.σ',r"F'=\mathcal O_X.\sigma",r"F'=\mathcal O_P.\sigma",'misprint','Lemma6.5 invokes6.1, which defines F as a coherent sheaf on P=ℙ^N_k; no X is introduced in these hypotheses. A section σ∈H^0(P,F) gives the evaluation morphism O_P→F, a↦aσ, and its image is exactly O_P·σ. Correct the ambient-scheme subscript to P in current. The later6.8 separately introduces X.');patch(655,'current',r"F'=\mathcal O_X.\sigma",r"F'=\mathcal O_P.\sigma",sid,'Use the source of the evaluation morphism defining the stated subsheaf.','misprint')
for pg,n in [(653,4),(654,6),(655,2)]:
 sid=own(pg,'structure sheaves','plain typed O',r'\mathcal O','O','font','All structure-sheaf letters on the page were compared and are plain and unlined.');patch(pg,'both',r'\mathcal O','O',sid,'Preserve the local plain structure-sheaf letter.',count=n)


# Pages656–660 fully compared; witness668,670,671 confirms indices and clipped margins.
f(1,'656 begins De s≥1, résulte','boundary655/656','The complete phrase starts656. The attached marker already precedes De and the accented word is joined correctly.',batch='656_660')
f(2,'L’assertion(ii) starts a new paragraph','proof6.5','The indented opening is visible after d’où(i). The applied division matches.',batch='656_660')
f(3,'three baseline dots between the plus signs','proof6.5(iii)','The three full stops lie at the baseline. The applied ldots matches.',batch='656_660')
f(4,'En effet starts a new paragraph after6.6','proof6.6','The blank line and indentation are present. The applied paragraph division matches.',batch='656_660')
f(5,'plain typed O in all twenty-nine listed occurrences','structure sheaves656–660','Every listed occurrence was compared on its page. All have plain, unlined O; local patches reproduce that form.',batch='656_660')
f(6,'Supposons q=1 begins an indented paragraph','first paragraph657','The source begins a new paragraph across the page boundary. The applied blank line after the marker matches.',batch='656_660')
f(7,'dim.supp(N_q), with a stop','first paragraph657','The full stop between dim and supp is present in main and witness668. Retain the applied abbreviation.',batch='656_660')
f(8,'h^0(F_q(-1), missing outer closing parenthesis','first paragraph657','Only the inner closing parenthesis follows −1; witness668 confirms the omission. Keep diplomatic and the existing current completion.',batch='656_660')
f(9,'et a_q^{(q)} et a_q^{(q)}=a_q','parenthetic remark after6.7(ii)','Both scans print the duplicated incomplete first phrase. The sequence 0→N_q→F→F_q→0 subtracts a Hilbert polynomial of degree≤q−1, giving a_i^{(q)}=a_i for i≥q. The existing current omission removes the duplicated fragment while preserving those equalities.',batch='656_660')
f(10,'dim.supp(N_q), with a stop','parenthetic remark after6.7(ii)','The second abbreviation stop is also present. Retain the applied form.',batch='656_660')
f(11,'0→F(-1→F→G→0','proof6.7','Both scans omit the closing parenthesis after −1. Keep diplomatic and the existing current completion.',batch='656_660')
f(12,'intègre is unlined','definition6.9','The underline stops after schéma, leaving intègre and X′_j unlined, then resumes under muni de. The applied nested emphasis preserves the source distinction.',batch='656_660')
f(13,'659 begins En effet, soit X','boundary658/659','The whole phrase starts659;658 ends the statement6.10. The supplied marker is exact.',batch='656_660')
f(14,'Raisonnant starts an indented paragraph','proof6.10','The blank line and indentation are visible in main and witness670. Retain the applied division.',batch='656_660')
f(15,'coproduct sign with no lower index','proof6.10, injection of structure sheaves','The j belongs only to X_j. No index appears under the coproduct sign in either scan; the applied omission matches.',batch='656_660')
f(16,'660 begins En effet, dans(i)','boundary659/660','659 ends the statement6.11(ii), and the entire En effet starts660. The supplied marker is exact.',batch='656_660')
f(17,'En effet, soit I starts an indented paragraph','proof6.13','The proof begins a new paragraph after the display. Retain the applied division.',batch='656_660')
sid=own(656,'proof6.6, choice of section','section of O_X(1)',r"section ``g\'en\'erale'' de $\mathcal O_X(1)$",r"section ``g\'en\'erale'' de $\mathcal O_P(1)$",'misprint','Proposition6.6 invokes6.1, where F is a coherent sheaf on P=ℙ^N_k. Its diagram is induced by multiplication by a linear section σ:O_P(-1)→O_P and the tensor maps F(-1)→F, N_q(-1)→N_q and F_q(-1)→F_q. Thus the line bundle supplying the section is O_P(1); X is not introduced in these hypotheses.');patch(656,'current',r"section ``g\'en\'erale'' de $\mathcal O_X(1)$",r"section ``g\'en\'erale'' de $\mathcal O_P(1)$",sid,'Use the line bundle on the explicit ambient projective space that supplies the displayed multiplication maps.','misprint')
sid=own(657,'Theorem6.7(ii), superscript of A',r'A_{r-i}^{(r-q)}(c_{q-1},…,c_r;m)',r'A_{r-i}^{(r-q)}',r'A_{r-i}^{(r-q+1)}','mathematical_source_correction','Both main and witness668 show the defining family A_i^{(q)}(X_0,…,X_q;Y), with q+1 X-slots, and the superscript r−q in(ii). Section6.1 specifies q≥1;6.7(ii) lists i=0,…,q−1 while its Hilbert coefficients are indexed0,…,r. In the displayed coefficient range1≤q≤r+1, the argument list c_{q−1},…,c_r has r−q+2 entries and starts at a nonnegative index. It therefore requires superscript r−q+1 under the given family definition. At q=r the list is (c_{r−1},c_r), needing A^{(1)} rather than printed A^{(0)}; at q=r+1 it is (c_r), needing A^{(0)}, and F_{r+1}=0 because N_{r+1}=F. The proof cites6.4(iii) and6.6, which use the bound beginning at c_{q−1};6.8(b_q) independently retains coefficients of degrees≥q−1. Preserve that supported argument list and correct the superscript only, without adding hypotheses or conventions for other indices.');patch(657,'current',r'A_{r-i}^{(r-q)}',r'A_{r-i}^{(r-q+1)}',sid,'Match the explicitly defined polynomial family to its displayed number of coefficient arguments.','misprint')
sid=own(660,'Remarque6.12, exact sequence for the double divisor','0→O_X(-Z)→O_X→O_Z→0',r'0\to\mathcal O_X(-Z)\to\mathcal O_X\to\mathcal O_Z\to0',r'0\to\mathcal O_Z(-Z)\to\mathcal O_{X_n}\to\mathcal O_Z\to0','mathematical_source_correction','Main and witness671 both print X in the first two subscripts, with no n. The immediately preceding definition is O_{X_n}=O_Y/O_Y(-2Z). Put I=O_Y(-Z). The quotient map O_Y/I²→O_Y/I has kernel I/I², which is isomorphic to O_Z(-Z) since Z is Cartier on Y. Hence the exact sequence used here is 0→O_Z(-Z)→O_{X_n}→O_Z→0. Its twist by −1 and the printed adjunction formula give a_0=χ(O_{X_n}(-1))=−Z²−2d+2−2p_a(Z)=(n−6)d+4−4p_a(Z), establishing the stated divergence while a_1=2d. Correct these two subscripts in current only.');patch(660,'current',r'0\to\mathcal O_X(-Z)\to\mathcal O_X\to\mathcal O_Z\to0',r'0\to\mathcal O_Z(-Z)\to\mathcal O_{X_n}\to\mathcal O_Z\to0',sid,'Restore the actual kernel and middle quotient in the exact sequence defined by I²⊂I⊂O_Y.','misprint')
sid=own(660,'Remarque6.12, consequence phrase','d’où que a_0=…',r"d'o\`u $a_0=",r"d'o\`u que $a_0=",'reversion','The main and witness671 both print que. The same consequential construction d’où que occurs in the proof4.6 on647. It expresses the stated consequence without altering its equality or limit; deleting que is an editorial wording change, not a supported source correction. Revert the deletion recorded in fixes/FIXLOG_6_CURRENT.jsonl#550.','reverted');patch(660,'current',r"d'o\`u $a_0=",r"d'o\`u que $a_0=",sid,'Retain the authors’ attested consequence phrase.','reversion')
for pg,n in [(656,1),(657,1),(658,6),(659,8),(660,13)]:
 sid=own(pg,'structure sheaves','plain typed O',r'\mathcal O','O','font','Every structure-sheaf letter on this page was read and has plain, unlined O.');patch(pg,'both',r'\mathcal O','O',sid,'Preserve the local plain structure-sheaf letter.',count=n)
for pg,n in [(658,1),(659,3),(660,2)]:
 sid=own(pg,'projective-space symbols','double-struck P',r'\mathbf P',r'\mathbb P','font','Each projective-space P has an added parallel vertical stroke, consistent with the double-struck P read on653. On659 witness670 also confirms all three occurrences.');patch(pg,'both',r'\mathbf P',r'\mathbb P',sid,'Reproduce the observed double-struck projective-space letter.',count=n)


# Pages661–666: all main-page strips compared; witnesses672,674,675 read at uncertain loci.
f(1,'tout idéal de l’anneau, without I','Corollaire6.14','Main and witness672 omit the name of the ideal, while the same sentence then uses √I and I. Supply that already used name immediately after idéal in current only.','not applied and now applied',r"tout id\'eal $I$ de l'anneau",batch='661_665')
patch(661,'current',r"tout id\'eal de l'anneau",r"tout id\'eal $I$ de l'anneau",'fixes/MISPRINTS_6.json#626','Name the ideal subsequently referred to as I and √I.','misprint')
f(2,'la racine √I de I est engendré','Corollaire6.14','Both scans print engendré without the final e. Its explicit subject is la racine, so retain the current agreement engendrée.',batch='661_665')
f(3,'auxilaire','proof6.14','Both scans lack the second i of auxiliaire. Retain the diplomatic form and existing current spelling correction.',batch='661_665')
f(4,'Soit X begins an indented paragraph','proof6.14','The paragraph division follows d’après6.13. The applied division matches.',batch='661_665')
f(5,'Par conséquent begins an indented paragraph','proof6.14','The paragraph division follows h⁰(O_Y)≤e_q. The applied division matches.',batch='661_665')
f(6,'bare product sign, no index','proof6.14, injection','No q appears beneath the product in main or witness672. The applied unindexed product matches.',batch='661_665')
f(7,'sum upper limit n, small letter','proof6.14, Hilbert polynomial of O_X','The upper limit is a small n in both scans. It is the argument of the Hilbert polynomial, whereas N is the fixed ambient dimension and the upper limit of the preceding b_i sum. Retain the existing current N.',batch='661_665')
f(8,'blank base followed by subscript i after ≤','proof6.14, bound for |a_i|','Neither scan has an f in the blank cell. The next words define f_i=A_{N−i}(e_i,…,e_N;0), identifying the missing bound. Keep the diplomatic omission and current f_i.',batch='661_665')
f(9,'plain typed O in all sixteen occurrences','structure sheaves661,663,664','The ten occurrences on661, four on663 and two on664 were each read. None is underlined or script. Local font patches preserve this form.',batch='661_665')
f(10,'et underlined in the display','Theorem7.1','A separate line is drawn under et. The applied emph produces italic type under normalem; replace it with uline to preserve the observed underline.','amended',r'\hbox{\uline{et}}',batch='661_665')
f(11,'En effet begins an indented paragraph','proof7.1.2, top663','Main and witness674 show the complete En effet at the start of663, indented after the preceding list. The applied division matches.',batch='661_665',page=663)
f(12,'baseline product stops','products662–665','The product stops are present. Retain the transcription’s cdot convention: c₁ takes tensor products to sums, intersection multiplies the displayed Chern classes or a Chern class and a curve class, and the brackets take their degree. In I·O_{X′}, multiplication is the extension of the ideal under f⁻¹O_X→O_{X′}. Thus each dot continues to denote exactly the printed multiplication operation.','retained convention','Keep the existing product operators.',batch='661_665')
f(13,'663 starts En effet, (ii) implique','boundary662/663','The preceding page ends the list; the entire En effet opens663 in both scans. The attached marker is exact.',batch='661_665')
f(14,'H²(N^{⊗n}(p−1), one closing parenthesis','exact sequence in proof7.1.2','Main and witness674 show only the closing parenthesis of p−1 before the arrow. Keep the diplomatic omission and current completion of H²’s argument.',batch='661_665')
f(15,'1/2 with a slash','last display in proof7.1.2','The numerator and denominator are on the same baseline. The applied slash matches.',batch='661_665')
f(16,'three baseline stops after n²+','last display in proof7.1.2','The stops sit on the baseline in both scans. The applied ldots matches.',batch='661_665')
f(17,'664 starts qu’un nombre fini','boundary663/664','663 ends de sorte que X n’a, and664 starts qu’un. The supplied marker matches that break.',batch='661_665')
f(18,'ideal I de O_Y','proof7.1, blowup','The printed subscript is Y. The ideal defining the curve Y⊂X is ker(O_X→O_Y); its blowup is Proj_X(⊕_{n≥0}Iⁿ). The source sheaf of this explicitly used ideal is O_X. Retain the existing current correction.',batch='661_665')
f(19,'plain M=I·O_{X′}','proof7.1','The M has the same plain typed shape as surrounding capital letters. The applied plain M matches.',batch='661_665')
f(20,'plain M in c₁(M)','proof7.1, projection formula','The second M is again plain and unlined. The applied form matches.',batch='661_665')
f(21,'etssoient, including an extra s','Corollaire7.3','Both scans show two adjacent s letters after et. This adds a letter, beyond the ignored spacing, so retain the diplomatic slip and current et soient.',batch='661_665')
f(22,'strict < with a short stray stroke above its upper arm','Corollaire7.3, conclusion','Main and witness675 show no bar beneath the sign. The printed proof also gives a strict negative self-intersection, and7.4(ii) prints an unambiguous strict <. Retain the already applied strict sign. The inadequate hypothesis for that strict conclusion is a separate substantive source correction, with its own proof.',batch='661_665')
f(23,'M^{⊗n}, with handwritten n','proof7.3','Both scans show n without an ascender. With d=M·H and h=H², the corrected L=M^{⊗h}⊗H^{⊗−d} satisfies L·H=hd−dh=0, exactly the equality used next. Retain the existing current h.',batch='661_665')
f(24,'et underlined in the display','Corollaire7.4(i)','A short underline is drawn beneath et. Replace the applied italic emph with uline.','amended',r'\hbox{\uline{et}}',batch='661_665')
f(25,'full stop after ≥0','Corollaire7.4(i), display end','The mark is a single full stop, with no upper stroke of a semicolon. The applied punctuation matches.',batch='661_665')
f(26,'quotient on the line with slash','Corollaire7.4(ii)','The fraction is typed with a slash between its two intersection numbers. The applied inline quotient matches.',batch='661_665')
f(27,'En effet begins an indented paragraph','proof7.4','The proof begins after the list on its own indented line. The applied division matches.',batch='661_665')
f(28,'Y, n’ont with comma','proof7.4, hypersurfaces containing Y','The comma is visible after Y. Retain the applied source punctuation.',batch='661_665')
f(29,'three baseline dots between intersection signs','proof7.4, definition of X′','The three stops are on the baseline. The applied ldots matches.',batch='661_665')
f(30,'Or par, without comma','proof7.4, projection formula','Or ends the line with no following punctuation; the next line begins par. The applied omission matches.',batch='661_665')
f(31,'665 ends de Y,;666 starts les composantes irréductibles','boundary665/666','Both complete page images were read. The first three lines of7.5 belong to665; the continuation begins666. The attached marker is exact.',batch='661_665')
for pg in [662,665]:
 old=r'\hbox{\emph{et}}';new=r'\hbox{\uline{et}}';sid=own(pg,'statement display','et underlined',old,new,'underline','The word has a separately drawn underline in the source.');patch(pg,'both',old,new,sid,'Preserve the printed display-word underline.')
for pg,n in [(661,10),(663,4),(664,2)]:
 sid=own(pg,'structure sheaves','plain typed O',r'\mathcal O','O','font','Every structure-sheaf O on this page was compared and is plain and unlined.');patch(pg,'both',r'\mathcal O','O',sid,'Preserve the local plain structure-sheaf letter.',count=n)
sid=own(661,'proof6.14, ambient projective space','double-struck P',r'\mathbf P',r'\mathbb P','font','The projective-space letter has a separate parallel vertical stroke in main and witness672.');patch(661,'both',r'\mathbf P',r'\mathbb P',sid,'Reproduce the observed double-struck projective-space letter.')
for pg,where in [(664,'Corollaire7.3'),(665,'Corollaire7.4(ii)')]:
 old=r"qui n'est pas num\'eriquement \'equivalent \`a $H$";new=r"qui n'est pas num\'eriquement proportionnel \`a $H$"
 reason='Both statements print non-equivalence to H, but their strict conclusions fail for X=ℙ², H=O(1), M=O(2): M and H have different degrees on a line, whereas h=H²=1, d=M·H=2 and M²=4=d²/h. The same example lies within7.4 with r=2. The proof uses the homomorphism Pic(X)→A¹_num(X)_Q induced by c₁: for L=M^{⊗h}⊗H^{⊗−d}, [L]=h[M]−d[H] and L·H=0. Numerical nonproportionality makes [L] nonzero, so the established7.1 gives L²<0. Expanding L²=h²M²−hd² yields precisely M²<d²/h. For7.4 put h=deg(c₁(H)^r), d=deg(c₁(M)c₁(H)^{r−1}); then deg(c₁(L)c₁(H)^{r−1})=0 and deg(c₁(L)²c₁(H)^{r−2})=h²deg(c₁(M)²c₁(H)^{r−2})−hd². The established7.4(i), expressly invoked by its proof, gives the same strict conclusion from [L]≠0. Replace the inadequate word equivalent by proportional in current only, restoring the hypothesis actually used by both printed proofs; no additional theorem is introduced.'
 sid=own(pg,where,'pas numériquement équivalent à H',old,new,'mathematical_source_correction',reason);patch(pg,'current',old,new,sid,'Restore the numerical nonproportionality required by the proof’s nonzero class h[M]−d[H].','misprint')
sid=own(661,'Corollaire6.14, attribution','I. Hermann','(I. Hermann).','(G. Hermann).','bibliographic_source_correction','Both main and witness672 clearly print I. Hermann. The primary Springer record for the polynomial-ideal paper identifies its author as Grete Hermann and cites Hermann, G.; the short metadata evidence is archived in review/xiii/evidence/bibliographic_verification.json. Correct the first initial to G in current only.');patch(661,'current','(I. Hermann).','(G. Hermann).',sid,'Use the verified initial of the author of the cited polynomial-ideal theorem.','misprint')
f(1,'666 begins les composantes irréductibles','boundary665/666','The beginning of the continuation is visible at the top of666, following de Y, at the bottom of665. The attached marker is exact.',batch='666_670')
f(2,'BIBLIOGRAPHIE in capitals with underline','bibliography heading','The capitals and heading underline are clear. The applied capitals match; section-title treatment follows the recorded typesetting convention.',batch='666_670')
f(3,'intègre with a short underline under ègr only','proof7.5','The isolated line begins beneath è and ends beneath r; int and the final e are outside it. Retain this partial stroke diplomatically and the current unlined word, since it identifies no coherent emphasized term.',batch='666_670')
f(4,'graĉe, circumflex centered above c','proof7.5','The circumflex is positioned above c. Retain the diplomatic form and current grâce with its accent on a.',batch='666_670')
f(5,'Amer. J. Math1967 p.94–103 printed twice','bibliography[2]','The journal, year and page range are repeated on the next line. Retain the diplomatic dittography and current single reference; the incorrect terminal page is separately checked against the journal’s primary table of contents.',batch='666_670')
f(6,'J.H.E.S., initial J with descending hook','bibliography[5]','The first letter has the hooked lower part of the nearby J in Jussila. Retain diplomatic J and the current institution initial I.',batch='666_670')
sid=own(666,'bibliography[2], terminal page','94–103, twice',r'Pathologies III, Amer. J. Math 1967 p. 94-103.',r'Pathologies III, Amer. J. Math 1967 p. 94-104.','bibliographic_source_correction','The source prints103 in both copies. The American Journal of Mathematics89(1),1967 table of contents identifies D. Mumford, Pathologies III as pp.94–104; its following article begins105. The primary journal metadata is archived in review/xiii/evidence/bibliographic_verification.json. Correct the terminal page in the current single reference only.');patch(666,'current',r'Pathologies III, Amer. J. Math 1967 p. 94-103.',r'Pathologies III, Amer. J. Math 1967 p. 94-104.',sid,'Use the journal’s verified terminal page for the referenced article.','misprint')


# ADD NEXT EXPLICIT BATCH HERE
# Duplicate records of these individually inspected changes.
for path in ['fixes/FIXLOG_6.jsonl','fixes/FIXLOG_6_CURRENT.jsonl']:
 for i,line in enumerate((R/path).read_text().splitlines(),1):
  rec=json.loads(line)
  for q in list(D):
   if q['record_type']!='checker' or str(q.get('original_record_page',q['page']))!=str(rec.get('page')):continue
   x=F[q['source_id'].split('/')[-1]];fix=x.get('fix')
   if fix and fix.get('old')==rec.get('old') and fix.get('new')==rec.get('new'):
    z={**q,'record_type':'fixlog','source_id':path+f'#{i}','related_finding':q['source_id']}
    if q['kind']=='misprint_in_print' and path.endswith('FIXLOG_6.jsonl') and q['verdict']=='amended':z['verdict']='confirmed';z['change']=rec['new'];z['reason']='The diplomatic restoration agrees with the print. '+q['reason']
    D.append(z);break
for i,x in enumerate(json.loads((R/'fixes/MISPRINTS_6.json').read_text()),1):
 for q in list(D):
  if q['record_type']=='checker' and q.get('original_record_page',q['page'])==x['page'] and q['where']==x['where']:
   D.append({**q,'record_type':'misprint','source_id':f'fixes/MISPRINTS_6.json#{i}','related_finding':q['source_id'],'misprint':q.get('misprint',q['verdict']!='amended'),'correction':q['change'] if q.get('misprint') is False or q['verdict']=='amended' else x['correct']});break
# Reconcile historical records to the individually inspected loci above.
# These explicit mappings duplicate a completed image decision, not a presumed scan check.
B={q['source_id']:q for q in D+OWN}
def ck(batch,n):return f'check/findings/findings_{batch}.json#{n}'
def copy_decision(sid,typ,ref,verdict=None,change=None,extra=''):
 q=B[ref]
 z={**q,'record_type':typ,'source_id':sid,'related_record':ref}
 if verdict is not None:z['verdict']=verdict
 if change is not None:z['change']=change
 if extra:z['reason']=q['reason']+' '+extra
 D.append(z);B[sid]=z
 return z
def direct_decision(sid,typ,page,printed,region,reason,verdict,change):
 z=dict(record_type=typ,page=page,source_id=sid,verdict=verdict,printed_reading=printed,image=f'scan/SGA6_scan_360dpi.pdf#page={page+14}',region=region,reason=reason,change=change,forms='French forms; English where content changes')
 D.append(z);B[sid]=z
 return z

# Current-layer correction logs that have no exact old/new counterpart in a checker fix.
fixmap={
536:ck('616_620',4),537:ck('616_620',9),538:ck('616_620',10),539:ck('616_620',11),
540:ck('626_630',2),541:ck('626_630',4),542:ck('631_635',4),543:ck('641_645',10),
544:ck('641_645',14),545:ck('646_650',9),546:ck('646_650',11),547:ck('656_660',8),
548:ck('656_660',9),549:ck('656_660',11),550:'ASTRA-XIII-0049',551:ck('661_665',2),
552:ck('661_665',7),553:ck('661_665',18),554:ck('661_665',23),555:ck('666_670',5),558:ck('666_670',6)}
for n,ref in fixmap.items():
 sid=f'fixes/FIXLOG_6_CURRENT.jsonl#{n}'
 z=copy_decision(sid,'fixlog',ref)
 if n in [538,539]:
  z['verdict']='amended';z['change']='Retain σ_i in both layers; classify as a transcription restoration, not a source misprint.';z['reason']+=' The recorded old σ_1 is absent from both supplied layers and contradicts the observed dotted i. The coordinator owns the two replay duplicates.'
 elif n==555:z['change']='Retain the removal of the duplicated reference; the terminal-page correction103→104 is recorded separately.'
direct_decision('fixes/FIXLOG_6_CURRENT.jsonl#556','fixlog',666,'Grothendieck A. . et Dieudonné J.','bibliography[3]','Two separate full stops are visible after the author initial A. The second repeats the abbreviation stop before the conjunction et; preserve the double stop diplomatically and the existing single stop in current.','confirmed','Retain current Grothendieck A. et Dieudonné J.')
direct_decision('fixes/FIXLOG_6_CURRENT.jsonl#557','fixlog',666,'Grothendieck A. . et alii','bibliography[5]','The source again has an extra separate stop following A. Preserve that printed duplication diplomatically and the existing single stop in current.','confirmed','Retain current Grothendieck A. et alii.')

C=json.loads((R/'fixes/RECONCILE_CODEX_6.json').read_text())['entries']
def codex(n,ref,verdict=None,change=None,extra=''):
 sid=f'fixes/RECONCILE_CODEX_6.json#{n}'
 z=copy_decision(sid,'codex',ref,verdict,change,extra);z['codex_id']=C[n-1]['id'];z['prior_status']=C[n-1]['status'];return z
def codex_direct(n,page,printed,region,reason,verdict,change):
 sid=f'fixes/RECONCILE_CODEX_6.json#{n}'
 z=direct_decision(sid,'codex',page,printed,region,reason,verdict,change);z['codex_id']=C[n-1]['id'];z['prior_status']=C[n-1]['status'];return z

codex(87,ck('646_650',11))
codex(88,ck('651_655',3),'confirmed','Confirm rejection; retain the comma in the final pairing.')
codex_direct(89,654,'p=P_r(a_{m,0},…,a_{m,r})','proof6.3','The a letters are clear in the main image. Lemma6.2 on653 allows every integer sequence c≥a. Taking that permitted sequence c=a makes c_{m,i}=a_{m,i} by the two explicit sums in6.1, and6.2 then gives exactly the printed p=P_r(a_{m,0},…,a_{m,r}). The earlier c_i=b_i−a_i on654 is used in1.11 to choose m; it does not forbid this fresh specialization of6.2. Thus the proposed replacement of a by c is unnecessary.','confirmed','Confirm rejection; retain the printed a_{m,i} in both layers.')
codex(90,'ASTRA-XIII-0042','not applied and now applied')
codex(91,'ASTRA-XIII-0046','not applied and now applied')
codex(92,ck('656_660',8))
codex(101,ck('616_620',4))
codex(102,ck('616_620',6),'not applied and now applied','Current1.3(i); diplomatic2.3(i).')
codex(103,ck('616_620',7),'not applied and now applied','Current1.3(ii); diplomatic2.3(ii).')
codex(104,ck('616_620',9))
codex(105,ck('616_620',10),'amended','Retain the printed σ_i at both endpoints in both layers.','The second endpoint in1.6(i) was separately inspected under '+ck('616_620',11)+'. This is a transcription restoration; neither printed endpoint is a source misprint.')
codex(106,ck('616_620',13),'not applied and now applied','Current S′; diplomatic S.')
codex(107,ck('616_620',14),'not applied and now applied','Current F(-1); diplomatic F(1).')
codex(108,'ASTRA-XIII-0008','not applied and now applied','Current m≥0; diplomatic m=0.','The proof of the correction includes m=c_0; that additional explanatory equality need not be inserted into the current text.')
codex_direct(109,622,'par1.8(i) car b_i≥0','proof1.11, upper bound for h¹','The scan clearly prints b_i≥0. Put s=dim supp F. Proposition1.8(i) bounds h⁰(F(n−1)) by the sum over0≤i≤s. Here n≥0, so every binomial(n−1+i,i) is nonnegative; b_i≥0 therefore permits padding to0≤i≤r, while a_i=0 for i>s. Subtracting χ gives the displayed sum of b_i−a_i. The following sentence then uses the already stated c_i≥b_i−a_i to increase the regularity bound. Both steps are justified without inserting HOLD’s intermediate explanation.','confirmed','Confirm rejection; retain b_i≥0 and the existing next sentence.')
codex(110,ck('641_645',8),'not applied and now applied','Current K-schéma; diplomatic k-schéma.')
codex(111,ck('641_645',10))
codex(112,ck('641_645',14),'reverted','Retain surjective in both layers.')
codex(113,ck('646_650',9))
codex_direct(114,648,'ouvert (resp. et fermé)','proof4.7, first paragraph','The source’s parenthesis supplies the additional adjective in case(ii). The same paragraph separates the assertions and the next paragraph explicitly says S_0 is open and also closed under(ii). The represented inverse-image subfunctor is the same S_0⊂S in both clauses, with the latter clause adding closedness. Expanding the repeated word ouvert is editorial and supplies no missing mathematical condition.','confirmed','Confirm rejection; retain ouvert (resp. et fermé).')
codex_direct(121,624,'les polynômes χ(F(n))','proof1.13, first line','The source has F without a subscript. The preceding sentence on623 makes F a flat family on X_T and the next words count the polynomials by connected components of T. The exact restriction map i_t:X_t→X_T gives F_t=i_t^*F and its Hilbert polynomial n↦χ(X_t,F_t(n)); these are precisely the fibre polynomials already quantified in1.13(ii). The context thus identifies the omitted fibre parameter, and adding it is an explanatory expansion rather than a proved textual corruption.','confirmed','Confirm rejection; retain the printed shorthand χ(F(n)).')
codex(122,ck('621_625',15),'not applied and now applied','Current L_{1,K}; diplomatic L′_K.')
codex(123,ck('626_630',2))
codex(124,ck('626_630',3),'amended','Keep lemma label2.7 and formula label2.7.1; correct only the proof citation2.6→2.5.','The printed heading is Lemme2.7, and its own formula is labelled2.7.1. Renumbering them is unsupported; the incorrect citation has an exact existing referent, the immediately preceding2.5.')
codex(125,ck('626_630',4))
codex(126,ck('626_630',8),'not applied and now applied','Current h¹(L(-n))=0; diplomatic h¹(L(n))=0.')
codex(127,ck('626_630',13),'not applied and now applied','Current top binomial index m−1+j; diplomatic m−1+i.')
codex(128,ck('631_635',4))
codex(129,ck('631_635',11),'not applied and now applied','Current L′_α; diplomatic L_α.')
codex_direct(130,634,'famille limitée de classes de faisceaux sur les fibres de Y/S','Definition3.3, continuation','The second word faisceaux is not followed by inversibles. The inverse image is taken under the stated morphism Φ:Pic_{Y/S}→Pic_{X/S}. Every element of Φ_K^{-1}(Λ_K) is therefore already a Picard class on Y_K, represented after the prescribed f.p.p.f. cover by an invertible sheaf. Proposition3.2(ii) on633 explicitly identifies these Picard points with classes of invertible sheaves. Thus the existing ambient functor supplies the property, and adding the adjective does not repair a missing hypothesis.','confirmed','Confirm rejection; retain the printed shorter phrase.')
codex(131,ck('656_660',9))
codex(132,ck('656_660',11))
codex(133,'ASTRA-XIII-0048','amended','Current0→O_Z(-Z)→O_{X_n}→O_Z→0; preserve both printed X subscripts diplomatically.','The queue’s suggestion to replace both X by X_n would give the wrong first kernel. HOLD instead has the valid Cartier sequence0→O_Y(-Z)→O_Y→O_Z→0 for Z⊂Y, which is related by the quotient ideals but does not explicitly contain the double-divisor quotient O_{X_n} used in the ensuing χ calculation. The reviewed correction records the exact I/I² kernel and O_Y/I² middle term.')
codex(134,ck('661_665',7))
codex_direct(135,662,'labels(i), (i′), (ii)','Lemme7.1.2, three-item list','All three labels are clear in the lower main strip. The middle explicit item label(i′) leaves the enumerate counter unchanged, so the supplied third automatic item already produces(ii), matching the scan and the proof references on663.','confirmed','Already present; retain the supplied list without renumbering.')
codex(136,ck('661_665',18))
codex(137,ck('661_665',23))
codex(138,'ASTRA-XIII-0064','not applied and now applied','Current nonproportionnel in7.3 and7.4(ii); diplomatic équivalent.','The parallel7.4(ii) correction is separately recorded as ASTRA-XIII-0065. The coordinator independently inspected both statements and their proofs and concurred.')
codex(139,ck('661_665',2))
codex(140,'ASTRA-XIII-0049','reverted','Retain d’où que in both layers.')
codex(141,ck('666_670',5),'confirmed','Retain current removal of the repeated journal reference and the extra period in bibliography[3].','The second operation in this record is separately inspected in fixes/FIXLOG_6_CURRENT.jsonl#556. The terminal page103→104 is an additional current-only correction, ASTRA-XIII-0067.')
codex(142,'fixes/FIXLOG_6_CURRENT.jsonl#557')
codex(143,ck('666_670',6))

# Tagged-tree rows repeat these same identified loci; preserve their separate source IDs.
first={q['codex_id']:q['source_id'] for q in D if q['record_type']=='codex'}
for n,x in enumerate(C,1):
 sid=f'fixes/RECONCILE_CODEX_6.json#{n}'
 if x['id'] in first and sid not in B:
  z=copy_decision(sid,'codex',first[x['id']],extra='The tagged-tree row repeats the same individually inspected locus.');z['prior_status']=x['status']

# HOLD has outdated folio assignments; these are its actual Exposé XIII loci.
hmap={88:102,90:106,91:107,93:121,94:122,95:123,96:124,97:126,98:127,99:128,100:129,101:110,102:111,103:133,104:139,105:134,106:136,107:138,108:137,109:141,110:143}
for n,cn in hmap.items():
 ref=f'fixes/RECONCILE_CODEX_6.json#{cn}'
 z=copy_decision(f'fr/codex/HOLD_VS_CORR.json#{n}','hold',ref,extra='The HOLD hunk was matched by its actual text, not the outdated folio inferred in the initial registry.')
 if n==107:z['change']='Use current nonproportionnel, retaining the scan’s strict <; the ≤ inherited by both historical trees is not the printed glyph.'
 if n==109:z['change']='Retain current single Mumford reference and single stop after Grothendieck A.; separately correct the terminal page to104.'
 if n==110:z['change']='Retain current single stop after A. and the verified institution initial I.';z['reason']+=' Its extra-period removal is separately confirmed in fixes/FIXLOG_6_CURRENT.jsonl#557.'
direct_decision('fr/codex/HOLD_VS_CORR.json#89','hold',619,'par2.3(ii); ↦n¹(F(n))','first paragraph','The two source readings were independently inspected and resolved in '+ck('616_620',7)+' and '+ck('616_620',9)+'. The surjection β_n is the multiplication map of1.3(ii), and the decreasing function is explicitly n↦h¹(F(n)).','not applied and now applied','Use both HOLD corrections in current, preserving the two printed slips diplomatically.')
direct_decision('fr/codex/HOLD_VS_CORR.json#92','hold',622,'m=0; par1.8(i) car b_i≥0','proof1.11','The equality m=0 is false: P_0(c_0)=c_0 and c_0≥b_0−a_0≥0, as proved in ASTRA-XIII-0008. Replace it by m≥0. The separate b_i≥0 clause correctly permits extending the1.8 sum to r; the following sentence uses c_i≥b_i−a_i. This is documented in fixes/RECONCILE_CODEX_6.json#109. HOLD’s added intermediate estimate explains an already valid step and need not be inserted.','amended','Current m≥0 only; retain the printed b_i≥0 justification and omit HOLD’s added explanatory sentence.')


for page in range(616,667):
 STATUS.append(dict(page=page,pdf_page=page+14,checked_against_scan=True,scan='scan/SGA6_scan_360dpi.pdf',regions='two overlapping full-width strips covering all body text, diagrams and footnotes,252dpi',findings=sum(q['page']==page for q in OWN),note='Entire page compared; witness consulted for unclear strokes; statement-underlining convention separately recorded.'))
for name,rows in [('decisions.jsonl',D),('patches.jsonl',P),('own_findings.jsonl',OWN),('page_status.jsonl',STATUS)]:
 (O/name).write_text(''.join(json.dumps(x,ensure_ascii=False)+'\n' for x in rows))
print('decisions',len(D),'patches',len(P),'own',len(OWN),'pages',len(STATUS))
