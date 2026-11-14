"""Record explicit, image-read editorial decisions. No automated scan verdicts."""
from pathlib import Path
import json,re
R=Path(__file__).resolve().parents[2]; O=R/'review/late'
F={}; D=[]; P=[]; OWN=[]; STATUS=[]
for path in sorted((R/'check/findings').glob('*.json')):
 for i,x in enumerate(json.loads(path.read_text()),1): F[f'{path.name}#{i}']={**x,'source_id':str(path.relative_to(R))+f'#{i}'}
def f(n,reading,region,reason,verdict='confirmed',change=None,batch='671_675'):
 key=f'findings_{batch}.json#{n}'; x=F[key]
 D.append(dict(record_type='checker',page=x['page'],source_id=x['source_id'],verdict=verdict,printed_reading=reading,image=f"scan/SGA6_scan_360dpi.pdf#page={x['page']+14}",region=region,reason=reason,change=change if change is not None else (x.get('fix') or {}).get('new','Retain verified printed text.'),forms='French forms; English transfer subject to aligned text',where=x['where'],kind=x['kind']))
def patch(page,layer,old,new,source_id,reason,kind='transcription',count=1):
 P.append(dict(page=page,layer=layer,old=old,new=new,source_id=source_id,reason=reason,kind=kind,expected_count=count))
def own(page,place,printed,tex,change,kind,reason):
 sid=f'ASTRA-LATE-{len(OWN)+1:04d}'
 OWN.append(dict(record_type='own',page=page,source_id=sid,verdict='not applied and now applied',where=place,printed_reading=printed,tex=tex,change=change,kind=kind,reason=reason,image=f'scan/SGA6_scan_360dpi.pdf#page={page+14}',region=place,forms='French forms; English transfer subject to aligned text'))
 return sid
# pp.672–675: full-page strips were visually read at 252 dpi; targeted crops at 576 dpi.
f(13,'SGA 4 XVI 3.7), et, conjecturalement,','first body line','The first body line begins with SGA; the existing page marker is at that beginning.')
f(14,'Atiyah et Hirzebruch; the two surnames separately underlined','body lines 6–7','The scan underlines each surname. The applied \\emph commands render italics with the supplied normalem option; replace them with \\uline.', 'amended',r'par \uline{Atiyah} et \uline{Hirzebruch} [1]')
f(15,r'K^\bullet "naif"','body line 8','The superscript is a single raised dot; preserve the raised-dot notation already applied.')
f(16,'sur un corps k de caractéristique nulle k, lorsque','end of §3.3','The second k is visibly printed. It repeats the same field name after the characteristic adjective; delete only this duplicate in the corrected forms.','not applied and now applied',r'de caractéristique nulle, lorsque')
f(17,'(n° 6)','§3.4, third line','The superscript o is visible in the abbreviation; the applied numéro macro reproduces it.')
f(18,'(cf n° 8 pour un cas plus général)','last body line','The print omits the abbreviation point. This is an intelligible abbreviation of confer; adding a point changes only editorial punctuation. Retain cf in both forms.','amended',r'corps $k$ (cf n\textsuperscript{o}~8')
f(19,'n° 8','last body line','The raised o is visible. Retain the applied numéro macro.')
patch(672,'both',r'par \emph{Atiyah} et \emph{Hirzebruch} [1]',r'par \uline{Atiyah} et \uline{Hirzebruch} [1]','check/findings/findings_671_675.json#14','Separate underline strokes on the surnames.')
patch(672,'current',r'de caractéristique nulle $k$, lorsque',r'de caractéristique nulle, lorsque','fixes/MISPRINTS_6.json#644','Delete the visibly printed duplicate field letter only in corrected text.','misprint')
patch(672,'current',r'corps $k$ (cf. n\textsuperscript{o}~8',r'corps $k$ (cf n\textsuperscript{o}~8','fixes/MISPRINTS_6.json#645','Retain the source abbreviation without adding punctuation.','rejected_misprint')
for txt in ['algébriquement clos et de caractéristique nulle','à support dans']:
 sid=own(672,'§3.3 or §3.5 underline',txt+' underlined',r'\emph{'+txt+'}',r'\uline{'+txt+'}','underline','The scan visibly underlines these word groups; normalem leaves \\emph italic.')
 patch(672,'both',r'\emph{'+txt+'}',r'\uline{'+txt+'}',sid,'Preserve the printed underline.')
# p.673
f(20,'rationelle','first body line','The print has a single n. French rationnelle has two; correct only corrected forms.','not applied and now applied','rationnelle')
f(21,r'c_i(\underline{E})','first display','A short horizontal underline is present immediately beneath E; keep it.')
f(22,r'\underline{E}','line below first display','The same bundle letter is underlined in running text; keep it.')
f(23,r'H^{2*}(X,\underline{Z}_\ell(*))','diagram (4.1) and display below','Both the degree marker and the Tate-twist argument are typed asterisks. The raised dots of K and Gr have another visible shape; preserve both marks.','not applied and now applied',r'H^{2*} and (*) in these cohomology groups')
f(24,r'\underline{Z}_\ell','first display, diagram and following display','The coefficient letter has a baseline underline in every occurrence on this page. Retain this underline in both forms.','not applied and now applied',r'\Zell -> \underline{Z}_\ell locally')
f(25,'j left of the upward arrow','diagram (4.1), lower vertical arrow','The label j is printed to the left; the applied unprimed tikz-cd label places it there.')
f(26,'comma after lower-right Gr group','diagram (4.1), lower right','The comma is visible to the right of the bottom object; keep the applied comma.')
f(27,r'\coprod_i H^{2i}','display below (4.1)','The summation mark is an inverted product sign, with lower horizontal stroke and two upright strokes. Keep \\coprod, as printed.')
f(28,'est defini par exemple','paragraph after diagram','The initial e has no accent. The accented spelling is required in corrected French; retain the unaccented print diplomatically.')
f(29,'de X codimension i','paragraph after diagram','The print has no second de before codimension. The noun phrase requires de codimension i; insert only in corrected forms.','not applied and now applied',r'de $X$ de codimension $i$')
f(30,r'c\ell^\bullet(\underline{O}_Y)','paragraph after diagram; targeted crop','The mark after the handwritten ell is a raised dot, not a letter i. The O has a distinct underline; amend the implementation to preserve that underline as well.','amended',r'\mathrm{c}\ell^\bullet(\underline{O}_Y)')
f(31,r'Filt^i_top(K^\bullet(X)) mod Filt^{i+1}_top(K^\bullet(X))','paragraph after diagram','The four-letter Filt, enclosing parentheses and word mod are all visible in the running text; keep the applied expression.')
f(32,'ses anneaux','third-to-last paragraph line','The scan prints ses. The antecedent is the three rings just enumerated; the demonstrative ces supplies that reference. Correct only corrected forms.','not applied and now applied','ces anneaux')
for old,new,sid in [('rationelle','rationnelle','fixes/MISPRINTS_6.json#646'),(r'de $X$ codimension $i$',r'de $X$ de codimension $i$','fixes/MISPRINTS_6.json#648'),('de ses anneaux','de ces anneaux','fixes/MISPRINTS_6.json#649')]: patch(673,'current',old,new,sid,'Apply the individually reviewed misprint correction.','misprint')
# p.674
f(33,'(régulier ou non). Il a par contre','first body line','The opening parenthesis is the first character of this page; current marker position is correct.')
f(34,'par Q. Autre avantage de A(X)','body line 4','Both clauses share a printed line. Retain the joined paragraph; this affects layout only.')
f(35,r'Gr^\bullet_top et Gr^\bullet(X)','body line 5','The first group omits its argument X while the second includes it. The whole paragraph has fixed X and explicitly names the group with X in the preceding sentence; this is unambiguous contextual notation. Preserve the source abbreviation in both forms.','amended',r'concurrents $\Gtop^\bullet$')
f(36,'(Cf.. n° 5)','body lines 10–11','Two successive full stops are visible after Cf. Remove one duplicate point in corrected forms.')
f(37,'n° 5','body line 11','The raised o is visible and the applied numéro macro agrees.')
f(38,r'\underline{Q}','body line 12','The Q at the start of this line has a distinct underline; retain the applied local letter form.')
f(39,r'K^\bullet(X) -> Ch(A(X))','display preceding (4.3)','There is no comma or full stop after the expression. Keep the applied removal.')
f(40,'mod. torsion','(4.4), first row','The abbreviation has a full stop after mod; keep it.')
f(41,'A^i(X) with no following punctuation','(4.4), first row end','The first row ends with the closing parenthesis, without a comma; retain the removal.')
f(42,'mod. torsion','(4.4), second row','The second row also prints the abbreviation point; keep it.')
f(43,'comma after Gr group','(4.4), second row end','The final mark is a comma below the baseline, with no upper dot; keep the comma.')
patch(674,'current',r'concurrents $\Gtop^\bullet(X)$',r'concurrents $\Gtop^\bullet$','fixes/MISPRINTS_6.json#650','The printed abbreviation suppresses a fixed argument; restore it without editorial expansion.','rejected_misprint')
# p.675
f(44,'(4.5) begins this printed page','first body display','The complete display (4.5) begins below the running head; the applied marker precedes the display.')
f(45,'classe de Y dans A^i(Y)','body line 3','The print visibly gives Y. The displayed Chern class is on X and the next sentence explicitly uses A^i(X); corrected X restores the same ambient cycle group.')
f(46,'arrow label f_* without an X index','end of §4.2, field-extension map','The printed arrow has only f and its lower asterisk. The additional X was removed correctly; the star-height issue is separately recorded.')
f(47,'f_* on A(X) -> A(X tensor_k k\')','end of §4.2, field-extension map','The star lies below f. The map in this direction is base change f^*, while the next map is its trace f_* and their displayed composite is f_* f^*. Preserve the printed subscript diplomatically; use the superscript in corrected text.')
f(48,'comme on voit un utilisant','end of §4.2','The scan visibly reads un. The French gerund is en utilisant; the current correction is appropriate.')
f(49,r'f_*: A(X tensor_k k\prime) -> A(X)','end of §4.2, trace map','The trace label consists of f and its lower asterisk only; keep removal of the added X.')
f(50,r'f_* f^* = n id','end of §4.2','The composite has only lower/upper stars and no X indices; keep removal of the added indices.')
f(51,'footnote (*) without a body call mark','whole page and bottom footnote','No body call mark is printed. The note concerns the exact Riemann–Roch formula discussed in §4.3; the current call at the end of §4.2 assigns an unsupported location. Preserve the uncalled editorial note in both forms.','amended',r'\sgastandalonefootnotetext{xiv-jouanolou}{...} in both forms')
f(52,'P. JOUANOLOU','bottom footnote','The surname is printed in capitals; retain those capitals.')
f(53,'la formule 4.5. soit vraie','§4.3, third line','The source gives an unparenthesized reference with a terminal point. It identifies the displayed formula unambiguously; adding parentheses is editorial normalization. Keep the printed citation in both forms.','amended','la formule 4.5. soit')
f(54,'au n° 3','§4.3 middle','The raised o is visible; keep the applied numéro macro.')
f(55,'ou ce qui revient au même','§4.3 near page end','There is no comma directly after ou; the applied removal agrees with the scan.')
f(56,'une fois at page end; résolu de begins the following page','last body line','The scanned body ends with une fois; the existing marker follows these words. Following-page beginning is checked separately with p.676.')
patch(675,'current',r'\footnote{Elle est donc',r'\sgastandalonefootnotetext{xiv-jouanolou}{Elle est donc','fixes/MISPRINTS_6.json#655','Keep the source note without an invented body anchor.','rejected_misprint')
patch(675,'current','la formule (4.5) soit','la formule 4.5. soit','fixes/MISPRINTS_6.json#656','Keep the printed reference style.','rejected_misprint')
# Record local notation, without changing uninspected pages.
for pg in [673,674,675]:
 text=(R/'fr/sga6/diplomatic/main.tex').read_text(); m=re.search(r'^%+\s*scan idx\s+\d+\s*\|\s*folio\s+'+str(pg)+r'\s+%+\n',text,re.M); nextm=re.search(r'^%+\s*scan idx',text[m.end():],re.M); chunk=text[m.end():m.end()+nextm.start()] if nextm else text[m.end():]
 for old,new,why in [(r'H^{2\bullet}',r'H^{2*}','The cohomology degree marker is the typed asterisk.'),(r'(\bullet)',r'(*)','The Tate-twist argument is the typed asterisk.'),(r'\Zell',r'\underline{Z}_\ell','The coefficient Z has a printed underline.'),(r'\Qell',r'\underline{Q}_\ell','The coefficient Q has a printed underline.'),(r'\varphi',r'\phi','The printed phi is the straight-stroke slashed-o form.'),(r'\mathcal O_Y',r'\underline{O}_Y','The structure-sheaf letter is a typed underlined O.'),(r'\cl',r'\mathrm{c}\ell','The class notation has a handwritten looped ell after c.')]:
  if pg==675 and old==r'\cl': old,new=r'$\cl(Y)$',r'$\mathrm{c}\ell(Y)$'
  n=chunk.count(old)
  if n:
   sid=own(pg,'notation in visually inspected page',new,old,new,'notation',why)
   patch(pg,'both',old,new,sid,why,'notation',n)
 for em in re.findall(r'\\emph\{([^{}]*)\}',chunk):
  sid=own(pg,'underlined words in running text',em+' underlined',r'\emph{'+em+'}',r'\uline{'+em+'}','underline','The scan underlines the words; normalem renders \\emph in italics.')
  patch(pg,'both',r'\emph{'+em+'}',r'\uline{'+em+'}',sid,'Preserve the printed underline.')
# Explicit collation of pp.676–680; witness checked at 676, 678, 680.
def g(n,reading,region,reason,verdict='confirmed',change=None):
 return f(n,reading,region,reason,verdict,change,batch='676_680')
g(1,'résolu de façon satisfaisante','first body line','The visible first words are résolu de; the existing marker is correct.')
g(2,'n° 1','first body line','The raised o is visible; keep the applied numéro macro.')
g(3,r'\phi','four occurrences in §4.3','The four phi forms are typed slashed o; use the straight phi at these inspected occurrences. Other pages are handled on their own evidence.','not applied and now applied',r'\varphi -> \phi')
g(4,r'c\ell(Y)','§4.3, text and display','The class symbol has the looped handwritten ell in all three occurrences on this page. The typed cl on p.677 is retained separately.','not applied and now applied',r'\cl -> \mathrm{c}\ell on p.676')
g(5,r'\deg(Y\cdot\xi^i)>0','§4.3, polarization argument','The printed exponent is i. The degree map is A^{dim X}(X) -> Z, while [Y] has codimension i and ξ has degree 1. Thus [Y]ξ^m has degree i+m and the zero-cycle degree uses m=dim X-i=dim Y. Change the exponent to dim Y in corrected forms.','not applied and now applied',r'\deg(Y\cdot\xi^{\dim Y})>0')
g(6,'map φ^i inline','§4.3 second paragraph','The displayed formula in the earlier source is printed inline; keep the already-applied inline form.')
g(7,'[9, n°4, 3°]','end of §4.3','Both raised o marks are visible; keep the applied macros.')
g(8,'f: Y   X, with an empty arrow space','§4.4 before (4.6)','Both main PDF page690 and witness page687 show completely blank space between Y and X. It is an omitted arrow in the declared immersion; preserve the blank diplomatically and supply the arrow in corrected forms.')
g(9,r'c_d(\underline{N})','(4.6)','N has a visible underline; keep the applied underline.')
g(10,r'Gr^\bullet_top(X)','line after (4.6)','The print says X. The maps are f_*:Gr_top(Y)->Gr_top(X) followed by f^*:Gr_top(X)->Gr_top(Y); both f^*f_*(y) and y c_d(N) therefore lie on Y. Correct the ambient argument to Y.','not applied and now applied',r'formule valable dans $\Gtop^\bullet(Y)$')
g(11,r'\underline{N}','last body line','The conormal-sheaf letter is underlined; keep it.')
patch(676,'current',r'\deg(Y\cdot\xi^i)>0',r'\deg(Y\cdot\xi^{\dim Y})>0','fixes/MISPRINTS_6.json#714','The Chow grading forces exponent dim Y for a zero-cycle degree.','misprint')
patch(676,'current',r'formule valable dans $\Gtop^\bullet(X)$',r'formule valable dans $\Gtop^\bullet(Y)$','fixes/MISPRINTS_6.json#716','The composite f^*f_* has domain and codomain on Y.','misprint')
old=r'\emph{que $\varphi^2:A^2(X)\to\Gtop^2(X)$ est un isomorphisme}'
new=r'\uline{que} $\varphi^2:A^2(X)\to\Gtop^2(X)$ \uline{est un isomorphisme}'
sid=own(676,'§4.3 underlined conclusion','que and est un isomorphisme underlined, formula unlined',old,new,'underline','Only the word groups carry underline strokes; the formula between them is not underlined.')
patch(676,'both',old,new,sid,'Preserve the extent of the source underlining.')
g(12,'de Y dans X','first body line of p.677','The first words are de Y, and the applied marker precedes them.')
g(13,'modulo torsion underlined','first paragraph','The source has an underline, while normalem keeps \\emph italic. Amend the implementation to \\uline.','amended',r'mais seulement \uline{modulo torsion}.')
g(14,'(*) and (**) around the shared bottom note','footnote area','The note text is accompanied by a star above and two stars below. The orphan (**) is visible and must be preserved. Explicit printed-mark rendering remains the coordinator’s footnote implementation task.')
g(15,r'c_d(\underline{N})','(4.7)','N is underlined; cl in this formula uses a typed l and remains \\cl.')
g(16,'On se heurte begins a new paragraph','after (4.7)','The new line is indented, agreeing with the added paragraph break.')
g(17,'algébre','§4.5 near page end','An acute accent is visible over e; the word algèbre requires the grave accent in corrected French.','not applied and now applied','algèbre')
g(18,'Or at left margin of following p.678','p.677/678 boundary','The beginning Or on p.678 is not indented; retaining the removed empty line follows the continuous paragraph. This is a layout decision.')
patch(677,'both',r'\emph{modulo torsion}',r'\uline{modulo torsion}','check/findings/findings_676_680.json#13','The scanned phrase is underlined.')
patch(677,'current','comme algébre sur','comme algèbre sur','fixes/MISPRINTS_6.json#717','Correct the printed accent in corrected forms.','misprint')
g(19,'Or prenons pour X une variété de drapeaux','first body line p.678','The main scan is faint, but witness page689 clearly begins Or. Current marker is correctly placed.')
g(20,r'H^*(X(C),Z)','(**) on p.678','The superscript is a typed asterisk, clearly preserved in witness page689. Use asterisk, while K and Gr keep raised dots.','not applied and now applied',r'H^\bullet -> H^*')
g(21,'L. HODGKIN','paragraph following (**)','Witness page689 clearly prints the surname in capitals; keep the applied capitalization.')
g(22,'φ:A(X)->Gr_top(X) in running text','paragraph following (**)','The arrowed expression is on the same body line as the surrounding prose. Keep the applied inline setting.')
g(23,'la cohomologie ... est engendré','§4.5 near page bottom','The witness clearly lacks the final feminine e. Add it in corrected French to agree with la cohomologie.','not applied and now applied',r'est engendrée par les éléments de degré $2$')
g(24,r'S\ell(n)','classification sentence','The lower-case letter is a looped handwritten ell; the applied symbol agrees with witness page689.')
g(25,r'A(X)\simeq Gr_top(X) inline','§4.6 first sentence','The isomorphism stands in the running text; retain the applied inline setting.')
g(26,'apparait','§4.6','Both scans omit the circumflex. Restore the historical French spelling apparaît in corrected forms.','not applied and now applied','apparaît')
patch(678,'current',r'est engendré par les éléments de degré $2$',r'est engendrée par les éléments de degré $2$','fixes/MISPRINTS_6.json#718','Agreement with the feminine noun cohomologie.','misprint')
patch(678,'current','apparait comme','apparaît comme','fixes/MISPRINTS_6.json#719','Restore the missing circumflex in the corrected historical text.','misprint')
sid=own(678,'first line','variété de drapeaux underlined',r'\emph{variété de drapeaux}',r'\uline{variété de drapeaux}','underline','Witness page689 shows a continuous underline beneath the three words.')
patch(678,'both',r'\emph{variété de drapeaux}',r'\uline{variété de drapeaux}',sid,'Preserve the printed underline.')
g(27,'Gr(X) à un caractère covariant','first paragraph p.679','The print visibly uses à. The sentence requires the verb a; change only corrected French.','not applied and now applied','a un caractère')
g(28,r'c\ell^\bullet(Y)','first paragraph','The superscript is a dot, and the class symbol has a looped ell. Keep the dot; the local ell rendering is recorded separately.')
g(29,'Filt^i(X)','first paragraph','The print spells Filt with four letters; keep the applied operator spelling.')
g(30,'Filt^{i+1}(X)=Filt_top^{i+1}(X)','first paragraph','Both operators have final t; keep the applied spellings.')
g(31,r'c\ell^\bullet(Y\prime)','first paragraph','The raised dot is present after the class symbol; keep it.')
g(32,r'Filt^i(X\prime)','first paragraph','The printed operator has final t; keep it.')
g(33,'Filt_top^{i+1}(X)=Filt_top^{i+1}(X)','kernel expression','Both operators spell Filt; preserve this spelling. The repeated top index is adjudicated separately.')
g(34,'second Filt also indexed top','kernel expression','The source visibly repeats the same top filtration. The preceding sentence supplies Filt^{i+1}(X)=Filt_top^{i+1}(X); the correction writes precisely that established equality in the kernel argument. Remove the repeated top index in corrected forms, retaining both printed occurrences diplomatically.','not applied and now applied',r'=\operatorname{Filt}^{i+1}(X)')
g(35,r'Filt^i(X\prime)','end of §4.6','The final t is visible; keep the applied spelling.')
g(36,'HODGKIN','§4.7','The surname is in capitals; keep them.')
g(37,r'c\ell^\bullet(\underline L)-1','§4.7','Both a raised dot and an underline beneath L are visible. Keep these independently recorded features.')
g(38,r'\underline L','§4.7 running text','The repeated letter L is underlined as well; keep it.')
g(39,r'B -> \underline G_m','first representation map','The typed G has a short underline and subscript m; keep that local form.')
g(40,r'B -> \underline G_m','second representation map','The second occurrence has the same printed underline; keep it.')
g(41,'A^0(X)=Z','last body line','X=G/B is defined in this same paragraph. The quotient homomorphism π^*:A(G/B)->A(G) restricts in degree zero to Z[X]->Z[G], sending [X] to [G], hence an isomorphism. Identifying the quotient’s degree-zero part with A^0(X) is valid through this specified map; retain X in both forms.','amended',r'A^0(X)=\Z')
patch(679,'current',r'(X)$ à un caractère',r'(X)$ a un caractère','fixes/MISPRINTS_6.json#720','The sentence uses the verb avoir.','misprint')
patch(679,'current',r'=\operatorname{Filt}_{\mathrm{top}}^{i+1}(X)$). Considérons',r'=\operatorname{Filt}^{i+1}(X)$). Considérons','fixes/MISPRINTS_6.json#721','Use the explicit equality stated in the preceding sentence rather than duplicate its left member.','misprint')
patch(679,'current',r'réduit à $A^0(G)=\Z$',r'réduit à $A^0(X)=\Z$','fixes/MISPRINTS_6.json#722','The displayed quotient induces a canonical isomorphism on degree zero; the printed X is valid.','rejected_misprint')
for old,new in [(r'\emph{telle que}',r'\uline{telle que}'),(r'\emph{ne soit pas compatible avec les $\lambda$-filtrations (modulo décalage par $i$)}',r'\uline{ne soit pas compatible avec les} $\lambda$-\uline{filtrations} (\uline{modulo décalage par} $i$)')]:
 sid=own(679,'underlined conclusion of §4.6',new,old,new,'underline','The scan underlines the word groups, leaving the mathematical symbols outside the underline strokes.');patch(679,'both',old,new,sid,'Preserve source underline extents.')
g(42,r'S\ell(n)','second body line p.680','The lower-case letter is handwritten ell; keep the applied symbol.')
g(43,r'\underline Z_\ell','(4.9)','The coefficient Z is underlined and the index is handwritten ell; restore that underline.','not applied and now applied',r'\Zell -> \underline{Z}_\ell')
g(44,'coéfficient','paragraph after (4.10)','The print visibly has an acute accent on the first e; the corrected spelling is coefficient.','not applied and now applied','coefficient')
g(45,r'\coprod_{i\geq0} A^i(G)','A^+(G) formula','The witness crop of page691 shows the extra slanted lower stroke of ≥. Including i=0 supplies the direct summand A^0(G)=Z, with inclusion and projection splitting the sum; this contradicts the printed description groupe fini. Correct the index to i>0, keeping the printed coproduct symbol.','not applied and now applied',r'\coprod_{i>0}')
g(46,r'G=\underline G_2','last paragraph','The G identifying the exceptional group is underlined; keep it.')
g(47,'degré >0, de façon précise','last paragraph','The printed separator after zero is a comma; keep the applied punctuation.')
g(48,r'\underline G_2','last paragraph, repeated group name','The repeated G has the same underline; keep it.')
g(49,'J.P. SERRE','last body line','The initials have full stops but no hyphen; the surname is in capitals. Keep the applied spelling.')
patch(680,'current','coéfficient de torsion','coefficient de torsion','fixes/MISPRINTS_6.json#723','Correct the printed accent.','misprint')
patch(680,'current',r'\coprod_{i\geq0}A^i(G)',r'\coprod_{i>0}A^i(G)','fixes/MISPRINTS_6.json#724','Positive-degree part excludes the split infinite summand A^0(G)=Z.','misprint')
# Additional local notation changes, limited to these five fully read pages.
for pg in [676,677,678,679,680]:
 text=(R/'fr/sga6/diplomatic/main.tex').read_text(); m=re.search(r'^%+\s*scan idx\s+\d+\s*\|\s*folio\s+'+str(pg)+r'\s+%+\n',text,re.M); nextm=re.search(r'^%+\s*scan idx',text[m.end():],re.M); chunk=text[m.end():m.end()+nextm.start()] if nextm else text[m.end():]
 pairs=[(r'\varphi',r'\phi','The printed phi has the straight-stroke slashed-o form.'),(r'H^{2\bullet}',r'H^{2*}','The cohomological degree sign is an asterisk.'),(r'H^\bullet',r'H^*','The cohomological degree sign is an asterisk.'),(r'(\bullet)',r'(*)','The twist argument is a typed asterisk.'),(r'\Zell',r'\underline{Z}_\ell','The coefficient Z is underlined.')]
 if pg in [676,679]:pairs.append((r'\cl',r'\mathrm{c}\ell','These class symbols have handwritten looped ell.'))
 for old,new,why in pairs:
  n=chunk.count(old)
  if n:
   sid=own(pg,'notation in inspected page',new,old,new,'notation',why);patch(pg,'both',old,new,sid,why,'notation',n)

# Explicit direct comparison of pp.681–685.
def h(n,reading,region,reason,verdict='confirmed',change=None):
 return f(n,reading,region,reason,verdict,change,batch='681_685')
h(1,'g with a raised dot','§5.1 first display','The raised dot has the same shape and level as the dot on Gr; retain the applied dot.')
h(2,'g with a raised dot','last sentence of §5.1','The mark is visibly a raised dot; keep the applied notation.')
h(3,'g with a raised dot','§5.2, sentence beginning la question','The mark is a raised dot, agreeing with the applied notation.')
h(4,"un homomorphisme d'anneaux :",'§5.2 before g_Q display','Both vertically aligned dots of the colon are visible; keep it.')
h(5,r'\otimes_{Z_\ell}','g_Q display, tensor base','The small Z of the tensor base has no doubled stroke or underline. The neighbouring larger Z is doubled; retain the locally plain tensor-base letter.')
h(6,'tels que pour tout Module','first sentence after §5.1 display','The printed s is visible. The antecedent is the singular homomorphisme, so use tel in corrected forms.','not applied and now applied','tel que pour tout Module')
h(7,r'H^2(X,Z_\ell(*))','§5.2 following g_Q display','There is no star after 2. The map g_Q is graded and its degree-i component lands in H^{2i}(X,Q_ell(i)); the integral image referred to here is therefore the direct sum of those groups, represented by H^{2*}. Keep the current added degree star, with the printed asterisk shape.',change=r'H^{2*}(X,\Zell(*))')
h(8,'se résoud affirmativement','§5.2','The final letter is d. The present singular form is résout; the current spelling correction is retained.')
h(9,'hypothètique','§5.2 near page end','The first accent is grave. The correct spelling hypothétique uses acute; change corrected forms only.','not applied and now applied','hypothétique')
h(10,'H^{2*}, coefficient twists (*), and H_Y^* -> H^*','all cohomology occurrences pp.681–685','All five pages have now been read. Their degree and twist placeholders are six-armed typed asterisks; K, Gr and g use raised dots. Preserve these observed shapes locally.','not applied and now applied','Local cohomology placeholders: asterisk.')
h(11,'E and L underlined','all bundle letters pp.681–682','Both pages have now been read; every listed bundle letter has an underline. Restore only those underlines.','not applied and now applied',r'E -> \underline{E}; L_j -> \underline{L}_j locally')
patch(681,'current','tels que pour tout Module','tel que pour tout Module','fixes/MISPRINTS_6.json#692','Singular agreement with homomorphisme.','misprint')
patch(681,'current','hypothètique','hypothétique','fixes/MISPRINTS_6.json#695','Correct the printed accent in corrected forms.','misprint')
sid=own(681,'§5.1, generators of Gr',r'c^i(E)',r'c_i(E)',r'c^i(E)','rejected_misprint','The superscript is visible on p.681. Exposé V 6.7.1, p.353/PDF367, explicitly defines c^i(x)=cl_{Gr^i A}(gamma^i(x-epsilon(x))); this is the defined class notation and is retained. The definition image was inspected directly.')
OWN[-1]['additional_image']='scan/SGA6_scan_360dpi.pdf#page=367'
patch(681,'current',r'engendré par les $c_i(E)$, on voit',r'engendré par les $c^i(E)$, on voit',sid,'Restore the notation defined in V 6.7.1, not an error.','rejected_misprint')
D.append(dict(record_type='fixlog',page=681,source_id='fixes/FIXLOG_6_CURRENT.jsonl#564',verdict='amended',printed_reading=r'c^i(E)',image='scan/SGA6_scan_360dpi.pdf#page=695',additional_image='scan/SGA6_scan_360dpi.pdf#page=367',region='§5.1 generators; V 6.7.1 definition',reason=OWN[-1]['reason'],change=r'Restore c^i(E) in current French and corresponding English notation.',forms='current French and English'))
for old,new,why in [(r'\(H^{2\bullet}(X,\Zell(\bullet))\)',r'\(H^{2\bullet}(X,\underline{Z}_\ell(\bullet))\)','The title has a typed underlined Z.'),(r'g^\bullet:\operatorname{Gr}^\bullet(X)\longrightarrow H^{2\bullet}(X,\Zell(\bullet)),',r'g^\bullet:\operatorname{Gr}^\bullet(X)\longrightarrow H^{2\bullet}(X,\underline{Z}_\ell(\bullet)),','The §5.1 display has an underlined Z; the later §5.2 displays use doubled Z.')]:
 sid=own(681,'title or first display',new,old,new,'font',why);patch(681,'both',old,new,sid,why)
h(12,'K with a raised dot','§6.1, naive K','The mark is level with the top of K and round; keep the applied raised dot.')
h(13,'K with a raised dot','(6.1)','The mark is a raised dot; keep the applied notation.')
h(14,'reflexions','§5.3','The first e has no accent. Add the acute accent in corrected forms.','not applied and now applied','réflexions')
h(15,'lui-même without a full stop','end of §5.3','The line ends immediately after the final e; the next paragraph starts 5.4. Keep the diplomatic omission and the current supplied sentence stop.')
patch(682,'current','les reflexions qui précèdent','les réflexions qui précèdent','fixes/MISPRINTS_6.json#696','Restore the missing accent in corrected French.','misprint')
h(16,'underlined Q, blank, (i)','(6.2), source','The main scan and witness page694 show the underline and a blank with no ell. Supply ell only in current forms; preserve the underline in both.',change=r'Diplomatic \underline{Q}(i); current \underline{Q}_\ell(i)')
h(17,'underlined Q, blank, (i-d)','(6.2), target','The second coefficient has the same empty ell position in both images. Supply ell only in current forms and preserve the underline.',change=r'Diplomatic \underline{Q}(i-d); current \underline{Q}_\ell(i-d)')
h(18,'dimension relative virtuelle de d','line after (6.2)','The final printed letter is d. The integer d is the virtual relative dimension of the morphism f:X->Y, whose Gysin map lowers cohomological degree by 2d. Replace this second d with f in corrected forms.','not applied and now applied',r'dimension relative virtuelle de $f$.')
h(19,'Gr with a raised dot','paragraph before (6.3)','The mark is a round raised dot; retain the applied dot.')
h(20,'Gr with a raised dot','(6.3), top-left object','The scan shows a dot, agreeing with the applied notation.')
h(21,'Gr with a raised dot','(6.3), bottom-left object','The lower-left object also carries a round raised dot; keep it.')
h(22,'flêches horizontales','paragraph after (6.3)','The accent is circumflex, clear in both images. Retain diplomatically; current grave accent is correct.')
h(23,'flĉhes verticales','paragraph after (6.3), close crop','The main scan crop shows c with a circumflex, followed by hes; the e is absent. Retain the existing diplomatic fl\\^{c}hes and corrected flèches.')
h(24,'flê-che','same paragraph across line end','The circumflex is printed over e. Keep it diplomatically and the grave accent in corrected forms.')
h(25,'analogue à (6.3) :','line immediately before (6.4)','A complete colon is visible. The applied colon agrees with the scan.')
patch(683,'current',r'dimension relative virtuelle de $d$.',r'dimension relative virtuelle de $f$.','fixes/MISPRINTS_6.json#700','The dimension is attached to the declared morphism f.','misprint')
for layer,old,new in [('diplomatic',r'H^n(X,\Q(i))',r'H^n(X,\underline{Q}(i))'),('diplomatic',r'(Y,\Q(i-d))',r'(Y,\underline{Q}(i-d))'),('current',r'H^n(X,\Qell(i))',r'H^n(X,\underline{Q}_\ell(i))'),('current',r'(Y,\Qell(i-d))',r'(Y,\underline{Q}_\ell(i-d))'),('both',r'H^{2\bullet}(X,\Qell(\bullet))',r'H^{2\bullet}(X,\underline{Q}_\ell(\bullet))')]:
 sid=own(683,'coefficient Q in (6.2) or upper-right (6.3)',new,old,new,'underline','The specified Q has a clear underline. The lower-right Q of (6.3) has no underline and is retained separately.');patch(683,layer,old,new,sid,'Preserve the locally printed underline.')
h(26,'rationelle','first two body lines','There is one n. Correct French rationnelle has two; change current forms only.','not applied and now applied','rationnelle')
h(27,'n° 3','§6.3','The abbreviation has a raised o and no abbreviation point; the applied form matches.')
h(28,'tranformer','§6.4 after first display','There is no s after n. Supply it in corrected forms.','not applied and now applied','transformer')
h(29,'se résoud affirmativement','§6.4','The final letter is d. Correct present-tense spelling is résout.','not applied and now applied','résout')
h(30,'est elle nulle','§6.4','The inverted subject has no printed hyphen. Supply the required hyphen in corrected forms.','not applied and now applied','est-elle')
for old,new,sid in [('équivalence rationelle','équivalence rationnelle','704'),('à tranformer intersections','à transformer intersections','705'),('question se résoud affirmativement','question se résout affirmativement','706'),('la classe de Chern est elle nulle','la classe de Chern est-elle nulle','707')]:patch(684,'current',old,new,'fixes/MISPRINTS_6.json#'+sid,'Apply the individually verified spelling correction.','misprint')
h(31,'ccmplexe','§7.1','Both main and witness page696 show two initial c glyphs; the o in pour and Modules on the same line is closed. Keep ccmplexe diplomatically and complexe in current.')
h(32,'L with a lower dot','§7.1 before first display','The dot is on the baseline, following L. The applied lower-dot form agrees.')
h(33,'L with a lower dot','§7.1 Chern-class display','The dot is again at the baseline; keep the applied lower dot.')
h(34,'K with a raised dot','§7.1, compact-space discussion','The dot is raised above the baseline. Retain it.')
h(35,'L with a lower dot, then |(X-Y)','§7.2 first sentence','The dot is low and the restriction argument remains on the line. The applied lower dot and existing restriction layout agree.')
h(36,'L with a lower dot','§7.2, cohomology sheaves','The printed dot lies on the baseline. Keep the applied form.')
h(37,'L with a lower dot','§7.2 display','The last L on the page also carries a low dot; keep it.')
# Local typography, checked across the five whole pages. Specific edits above precede these.
for pg in [681,682,683,684,685]:
 text=(R/'fr/sga6/diplomatic/main.tex').read_text(); m=re.search(r'^%+\s*scan idx\s+\d+\s*\|\s*folio\s+'+str(pg)+r'\s+%+\n',text,re.M); nextm=re.search(r'^%+\s*scan idx',text[m.end():],re.M); chunk=text[m.end():m.end()+nextm.start()] if nextm else text[m.end():]
 pairs=[(r'H^{2\bullet}',r'H^{2*}','The degree placeholder is a typed asterisk.'),(r'(\bullet)',r'(*)','The coefficient twist placeholder is a typed asterisk.'),(r'H_Y^\bullet',r'H_Y^*','The supported-cohomology placeholder is an asterisk.'),(r'H^\bullet',r'H^*','The cohomology placeholder is an asterisk.')]
 if pg in [681,682]:pairs += [(r'$E$',r'$\underline{E}$','The locally free Module E is underlined.'),(r'(E)',r'(\underline{E})','Every bundle E in these Chern-class expressions is underlined.')]+[(f'L_{j}',r'\underline{L}_'+str(j),'The invertible-sheaf L is underlined.') for j in [1,2,3]]
 if pg==684:pairs.append((r'\mathcal O_X',r'\underline{O}_X','The structure-sheaf symbol is a typed underlined O.'))
 for old,new,why in pairs:
  n=chunk.count(old)
  if n:
   sid=own(pg,'notation in inspected page',new,old,new,'notation',why)
   if pg==681 and old==r'H^{2\bullet}':
    patch(pg,'diplomatic',old,new,sid,why,'notation',n)
    patch(pg,'current',old,new,sid,why+' Current additionally includes the separately verified correction of printed H^2 after g_Q.','notation',n+1)
   else:patch(pg,'both',old,new,sid,why,'notation',n)
 for em in re.findall(r'\\emph\{([^{}]*)\}',chunk):
  sid=own(pg,'underlined word group',em+' underlined',r'\emph{'+em+'}',r'\uline{'+em+'}','underline','The text is underlined in the scan; the supplied normalem option leaves emphasis italic.');patch(pg,'both',r'\emph{'+em+'}',r'\uline{'+em+'}',sid,'Preserve printed underline.')

# Whole-page comparison of pp.686–690, with full witness views of 688–690.
def k(n,reading,region,reason,verdict='confirmed',change=None):
 return f(n,reading,region,reason,verdict,change,batch='686_690')
k(1,'7.1 (*) with no terminal point','first paragraph of p.686','The call follows 7.1 without a sentence stop. Retain the applied deletion and preserve the printed star mark.')
k(2,'L. ILLUSIE','p.686 footnote','The surname is in capitals; keep them.')
k(3,'cf. [13] with no terminal point','p.686 footnote end','The note ends at the closing bracket. Keep the applied removal.')
k(4,'rationelle','§8 first sentence','There is one n. Correct the spelling to rationnelle in current forms only.','not applied and now applied','rationnelle')
k(5,'Gr with a raised dot','§8, substitutes for A(X)','The printed dot is round, like the dot on the following Gr_top. Keep the applied dot.')
k(6,'à singularité','p.686 last line','No s follows singularité; the next page begins isolée. The applied singular agrees with both pages.')
patch(686,'current','équivalence rationelle des cycles','équivalence rationnelle des cycles','fixes/MISPRINTS_6.json#657','Correct the spelling in current forms only.','misprint')
sid=own(686,'bottom note','cohomologie de Hodge underlined',r'\emph{cohomologie de Hodge}',r'\uline{cohomologie de Hodge}','underline','A continuous underline is visible under this word group.');patch(686,'both',r'\emph{cohomologie de Hodge}',r'\uline{cohomologie de Hodge}',sid,'Preserve the printed underline.')
k(7,'isolée sont des invariants','first line p.687','The adjective is singular, qualifying singularité across the page break. Keep it.')
k(8,'étude "arithmétiques"','first paragraph p.687','The final s is visible, but the adjective qualifies the singular étude. Delete the s only in corrected forms.','not applied and now applied','arithmétique')
k(9,'n° 4','second paragraph p.687','The raised o is visible. Keep the applied numéro sign.')
k(10,'n° 3','end of second paragraph p.687','The raised o is visible. Keep the applied numéro sign.')
k(11,'BIBLIOGRAPHIE','heading p.687','Only this capitalized word appears; the applied heading matches.')
k(12,'The Riemann-Roch theorem for analytic embeddings, plain','entry [1]','The title has no underline or italic form. Keep the removed emphasis.')
k(13,'p. 151-166','entry [1]','The abbreviation has one p and the range a single typed hyphen. Keep the applied reading.')
k(14,'J.P. Serre','entry [2]','The initials have no intervening hyphen. Keep the applied form.')
k(15,'Le théorème de Riemann-Roch, plain','entry [2]','No underline or italics occur; retain the removed emphasis.')
k(16,'p. 97-136','entry [2]','One p and a typed hyphen are visible. Keep them.')
k(17,'vol 80','entry [3]','The abbreviation has no point, but identifies the volume unambiguously. Adding a point standardizes punctuation; preserve the source abbreviation in both forms.','amended','vol 80')
k(18,"Les classes d'équivalence rationelle, plain",'entry [4]','The title has no emphasis stroke. Keep it plain.')
k(19,'rationelle','entry [4] title','One n is printed. Restore the second n only in current forms.','not applied and now applied','rationnelle')
k(20,'Classification des groupes de Lie algébriques, plain','entry [5]','The title has no underline or italics. The applied plain form matches.')
k(21,'Homologie nicht-additiver Funktoren. Anwendungen, plain','entry [6]','The title is entirely plain. Keep the applied removal of emphasis.')
k(22,'Fourier t. XI','entry [6]','No comma follows Fourier. Keep the applied deletion.')
k(23,'p. 201-312','entry [6]','The single-p abbreviation and hyphen are visible. Keep them.')
k(24,'Ein Theorem der analytischen Garbentheorie, plain','entry [7]','The title has no underline or italics. Keep it plain.')
k(25,'n° 5','entry [7]','The o is raised. Keep the applied numéro sign.')
k(26,'p. 5-64','entry [7]','The print has p. and a single typed hyphen. Keep the applied form.')
k(27,'Classes de faisceaux et théorème de Riemann-Roch, plain','entry [8]','The title carries no emphasis. Keep it plain.')
k(28,'La théorie des classes de Chern, plain','entry [9]','The title carries no emphasis. Keep it plain.')
k(29,'France vol. 86, p. 137-154','entry [9]','There is no comma after France; the page range has one p and a typed hyphen. The applied reading matches all three features.')
patch(687,'current',"``arithmétiques''","``arithmétique''",'fixes/MISPRINTS_6.json#658','Agreement with the singular étude.','misprint')
patch(687,'current','vol. 80','vol 80','fixes/MISPRINTS_6.json#659','Preserve the unambiguous source abbreviation without editorial punctuation.','rejected_misprint')
patch(687,'current','équivalence rationelle','équivalence rationnelle','fixes/MISPRINTS_6.json#660','Correct the printed spelling in current forms.','misprint')
k(30,'[10] A. Grothendieck','first body line p.688','Entry [10], including the author initial, begins this page. The existing marker now stands before the item, correctly.')
k(31,'Classes de Chern et représentations linéaires des groupes discrets, plain','entry [10]','The title is plain in the main image and witness page699. Keep the applied plain form.')
k(32,'Dix exposés sur la cohomologie des schémas, plain','entry [10]','The book title is also plain. Keep the removed emphasis.')
k(33,'Pub. Cie with no terminal point','entry [10] end','Both images end at Cie. Keep the applied deletion.')
k(34,'Resolution of singularities of an algebraic variety over a field of characteristic zero, plain','entry [11]','Every word is plain. Keep the applied removal of emphasis.')
k(35,'p. 109-326','entry [11]','The abbreviation and single hyphen match the applied form.')
k(36,'J.P. Serre','entry [14]','No hyphen separates J. and P.; retain the applied initials.')
k(37,'Algébre Locale, Multiplicités, plain','entry [14]','The title is plain. Keep that form independently of its accent correction.')
k(38,'Algébre','entry [14]','The e has an acute accent in both images. Correct French uses Algèbre.','not applied and now applied','Algèbre')
k(39,'n° 11','entry [14]','The o is raised; keep the applied numéro sign.')
k(40,'Sous-groupes commutatifs et torsion des groupes de Lie compacts connexes, plain','entry [15]','The title has no underline or italics. Keep it plain.')
k(41,'p. 216-240','entry [15]','The print has one p and a typed hyphen. Keep the applied form.')
k(42,'Théorie des topos et cohomologie étale des schémas (SGA 6), plain','entry [16]','Both images show the complete title without emphasis. The current SGA 4 correction changed the matched substring and left its emphasis intact; remove it there too.','not applied and now applied',r'\emph{Théorie des topos et cohomologie étale des schémas (SGA 4)} -> Théorie des topos et cohomologie étale des schémas (SGA 4)')
k(43,'(SGA 6)','entry [16]','The printed numeral is 6. The named topos and étale-cohomology seminar is identified as SGA 4 in the surrounding citations (including XIV 6.2); keep the current bibliographical numeral correction to 4.')
k(44,'U. Mausin','entry [17]','The main image and witness page699 clearly print U. Mausin. The following page names MANIN in its citation 17. Correct the surname to Manin; preserve the printed initial U. The supplied replacement Yu. I. expands initials absent from the source.','amended','U. Manin')
D[-1]['misprint']=True
k(45,'Correspondances, motifs et transformations monoïdales, plain','entry [17]','The title is plain in both images. Retain the applied removal of emphasis.')
k(46,'MAt.','entry [17] journal','The second letter is an uppercase A. Keep MAt. diplomatically and Mat. in corrected forms.')
k(47,'Sborik','entry [17] journal','The printed word lacks n. The corrected journal name Sbornik is retained.')
k(48,'t 77','entry [17]','The abbreviation is printed without a point but clearly indicates the volume. Adding the point is punctuation standardization; retain t 77 in both forms.','amended','t 77')
k(49,'(119) n° 4','entry [17]','There is no comma after the closing parenthesis. The applied deletion agrees with the witness.')
k(50,'Ajouté en février 1969, without final point','bottom footnote p.688','The witness shows the complete note and its star, with no terminal point. Keep the applied deletion.')
patch(688,'current','Algébre Locale','Algèbre Locale','fixes/MISPRINTS_6.json#661','Correct the accent only.','misprint')
patch(688,'current',r'\emph{Théorie des topos et cohomologie étale des schémas (SGA 4)}','Théorie des topos et cohomologie étale des schémas (SGA 4)','fixes/REPLAY_MANUAL_6.json#20','Remove the emphasis using the already corrected numeral 4.')
patch(688,'current','Yu. I. Manin','U. Manin','fixes/MISPRINTS_6.json#663','Correct only the corrupted surname and retain the source initial.','misprint')
patch(688,'current','t. 77','t 77','fixes/MISPRINTS_6.json#666','Preserve the unambiguous source abbreviation.','rejected_misprint')
D.append(dict(record_type='replay',page=688,source_id='fixes/REPLAY_MANUAL_6.json#20',verdict='not applied and now applied',printed_reading='Plain title of SGA 6 in [16]',image='scan/SGA6_scan_360dpi.pdf#page=702',witness='scan/SGA6_witness_300dpi.djvu#page=699',region='entry [16]',reason='The current corrected numeral 4 prevented the old font-only edit from matching. Both images show the title without emphasis.',change='Remove emphasis around the SGA 4 title in current.',forms='current French; corresponding English title'))
sid=own(688,'entry [12]','paraitre','paraitre','paraître','misprint','Both images have an undiacritized i. Corrected historical French uses paraître, as the second reading also gives.');patch(688,'current','à paraitre','à paraître',sid,'Restore the missing circumflex only in corrected forms.','misprint')
k(51,'Note pour la page 1.','first heading p.689','The source includes the full stop after 1. Retain the applied stop; the heading layout is a volume convention.')
k(52,'K with a raised dot','first note, operations on K','The mark is a round raised dot, clearly visible in witness page700. Keep it.')
k(53,'K with a raised dot','first note, pré-λ-anneau','The mark is round and raised. Keep it.')
k(54,'K with a raised dot','first note, λ-anneau','The third occurrence also has the dot. Keep it.')
k(55,'débarasser','last sentence of first note','The word has a single r. Corrected débarrasser has two.','not applied and now applied','débarrasser')
k(56,'sans hyperplan quasi-projectif','note (*)','The wording hyperplan quasi-projectif is printed in both images. The parenthetical removes the quasi-projectivity restriction on the schemes and adds the relative smooth setting; keep the current correction hypothèse quasi-projective.')
k(57,'MANIN 17','note (**)','The reference number is bare in both images, and identifies entry 17 immediately preceding. Adding brackets changes citation punctuation without resolving an ambiguity; preserve the printed citation.','amended','MANIN 17')
k(58,'dans 16','note (**)','The bare number identifies bibliography entry 16, explicitly the cited work of Deligne. Retain the source citation without adding brackets.','amended','dans 16')
patch(689,'current','débarasser','débarrasser','fixes/MISPRINTS_6.json#667','Correct the printed spelling.','misprint')
sid=own(689,'note (*) opening','démonstration de (9.6)','démonstration de (9.6)','démonstration de (4.6)','misprint','The call on p.677 is attached to the assertion about formula (4.6) in A(Y). This note reports that same Chow-ring result, whereas Exposé XIV has no section 9 or formula (9.6). Correct the reference to (4.6).');OWN[-1]['additional_image']='scan/SGA6_scan_360dpi.pdf#page=691';patch(689,'current','démonstration de (9.6)','démonstration de (4.6)',sid,'Restore the local formula reference identified by its footnote call.','misprint')
for old,new,why in [(r'\mathcal O_X',r'\underline{O}_X','The source has a typed underlined O in both occurrences.'),(r'\emph{anneau de Chow}',r'\uline{anneau de Chow}','The words anneau de Chow are underlined.')]:
 sid=own(689,'notation in notes',new,old,new,'underline',why);patch(689,'both',old,new,sid,why,count=2 if old==r'\mathcal O_X' else 1)
sid=own(690,'entire page','Blank verso','No folio-690 marker','Add empty-page marker between p.689 text and p.691 index','marker','PDF page704 and witness page701 are entirely blank. No text is missing. Insert the marker after the last p.689 paragraph, before the final-index setup or its page break.');OWN[-1]['witness']='scan/SGA6_witness_300dpi.djvu#page=701';OWN[-1]['exact_anchor_before']='pour conclure la même relation dans le cas général.';OWN[-1]['exact_anchor_after']='% Final-index helper macros';OWN[-1]['marker']='%%%%%%%%%%  scan idx 703  |  folio 690  %%%%%%%%%%'

# Directly collated terminology and notation indices, pp.691–700.
def j(n,reading,region,reason,verdict='confirmed',change=None):
 return f(n,reading,region,reason,verdict,change,batch='691_695')
def l(n,reading,region,reason,verdict='confirmed',change=None,page=None):
 f(n,reading,region,reason,verdict,change,batch='696_700')
 if page is not None and page!=D[-1]['page']:
  D[-1]['original_record_page']=D[-1]['page'];D[-1]['page']=page;D[-1]['image']=f'scan/SGA6_scan_360dpi.pdf#page={page+14}'
j(1,'K with raised dot','algebraic equivalence entry','The dot is raised and round; keep the applied dot.')
j(2,'[a,b] complexe)','first I 4.7 entry','The opening parenthesis is absent although the closing one is printed. Keep this omission diplomatically and the supplied opening parenthesis in corrected text.')
j(3,'[a,b] complexe)','I 4.8 entry','The second entry has the same missing opening parenthesis. Keep the diplomatic omission and the current supplied parenthesis.')
j(4,'amplitude C_0 parfaite','I 4.8 entry','The underlined C_0 is visibly printed. I 4.8 on p.122/PDF136 defines this perfect amplitude using the category C_0 of summands of finite free Modules; its footnote explicitly permits omission of C_0 when unambiguous. Retaining C_0 names that very category, so no deletion is justified.','amended',r"d'amplitude \(\underline{C}_0\) parfaite contenue")
D[-1]['additional_image']='scan/SGA6_scan_360dpi.pdf#page=136'
j(5,'relativement a f','III 3.1 flat-amplitude entry','The a lacks the grave accent. The French preposition requires à.','not applied and now applied',r'relativement à \(f\)')
patch(691,'current',r'relativement a \(f\)',r'relativement à \(f\)','fixes/MISPRINTS_6.json#638','Restore the missing grave accent.','misprint')
j(6,'Gr raised dot, then Gr lower dot','numerical equivalence entry','The first dot is raised, the second lies on the baseline. The applied forms preserve both.')
j(7,'ditto mark under equivalence','second tau-equivalence entry','The entry consists of a ditto mark and XIII 4.4. Keep the applied ditto mark.')
j(8,'two ditto marks','second specialization-homomorphism entry','One mark stands under homomorphisme and one under spécialisation. Keep the applied two marks.')
j(9,'relativement a f','n-pseudo-coherent entry','The a has no accent. Supply the grave accent in corrected French only.','not applied and now applied',r'relativement à \(f\)')
patch(694,'current',r'relativement a \(f\)',r'relativement à \(f\)','fixes/MISPRINTS_6.json#639','Restore the missing grave accent.','misprint')
j(10,'p.695 ends with variété mixte; p.696 begins Index des notations; p.697 begins D^-(Qcoh(S))','pp.695–697 boundaries','All three pages were read directly. The five entries on p.695 and the first notation-index page now occupy their correct markers; retain the applied moves.')
j(11,'de tor-dimension finie','first row p.695','The compound has no internal space. The applied joined source line reproduces it.')
l(1,'D(_A underlined S followed by coh, no closing parenthesis','I 2.15 entry','The first object lacks the closing parenthesis; the second has one. Preserve the omission diplomatically and keep the supplied parenthesis in current.')
l(2,'C^P_num(X)','XIII 5.2 entry','The index types a capital P. The cited definition XIII 5.2 on p.651/PDF665, confirmed in witness662, uses handwritten lowercase p and describes codimension p cycles. Correct this index entry to the explicitly defined C^p_num(X); both denote the quotient of codimension-p cycles by numerical equivalence, with identity on cycle classes. Retain the printed capital diplomatically.')
D[-1]['additional_image']='scan/SGA6_scan_360dpi.pdf#page=665';D[-1]['additional_witness']='scan/SGA6_witness_300dpi.djvu#page=662'
l(3,'K with raised dot','f^*, IV 2.7','The superscript is a round dot. Keep the applied notation.')
l(4,'K with raised dot','f_*, IV 2.12','The superscript is a round dot. Keep the applied notation.')
l(5,"F' with >n and ≤n below the line",'I 2.12 truncation entry','The two truncation bounds are lower indices. Keep the applied lower >n; the entry is physically on p.697.',page=697)
l(6,'Gr raised dot, then Gr lower dot','X 3.1 entry','The two dot heights are distinct and correctly transcribed. The entry is on p.697.',page=697)
l(7,'Gr raised dot indexed alg, then Gr lower dot with alg above','X App.7.11 entry','Both grade placements agree with the main image and witness708. The entry ends p.697.',page=697)
l(8,'Gr_num begins; Mod(U) ends p.698','page boundaries','The main image has exactly these first and last entries. The existing marker is now correct.')
l(9,'Gr raised dot indexed num','first row p.698','The mark is a raised round dot. Keep it.')
l(10,'K raised dot indexed alg','X App.7.11 entry','The raised dot is visible. Keep it.')
l(11,'K raised/lower dots, A as left lower index of X','IV 2.2 entry','A lies to the lower left of X in both objects. The applied correction reproduces those indices and the raised dot.')
l(12,'K raised/lower dots, A as left lower index of X, naïf','second IV 2.2 entry','The same left indices are printed in both naive groups. Keep the applied expression.')
l(13,'K raised dot of f','IV 3.3.1 entry','The raised dot agrees with the applied notation.')
l(14,'K raised dot indexed num','X App.7.9.4 entry','The raised dot agrees with the applied notation.')
l(15,'K raised dot of X','IV 2.2 entry','The first dot is raised; the second is on the line. Keep the applied pair.')
l(16,'K raised dot of X, naïf','second IV 2.2 entry','The first dot is raised; keep the applied form.')
l(17,'K raised dot of X/Y','IV 3.3.1 entry','The raised dot agrees with the source.')
l(18,'par.amp_f(E), par.amp_Y(E)','first row p.699','Both abbreviations omit the f of parfait. The abbreviations remain unambiguous in the index entry pointing to III 4.1 and denote the same amplitude functions. Adding the letter merely standardizes the abbreviation; retain par.amp in both forms.','amended',r'\operatorname{par.amp}_f(E),\ \operatorname{par.amp}_Y(E)',page=699)
patch(699,'current',r'\parfamp_f(E),\ \parfamp_Y(E)',r'\operatorname{par.amp}_f(E),\ \operatorname{par.amp}_Y(E)','fixes/MISPRINTS_6.json#711','Preserve the unambiguous printed abbreviation.','rejected_misprint')
l(19,'Parf with A as left lower index of underlined S','I 4.9 entry','The left A index is clear in main and witness710. Keep the applied formula.',page=699)
l(20,'underlined Proj with lower 0','VI 2.3.2 entry','The underline stroke is visible and the applied local form restores it.',page=699)
l(21,'raised r to the left of underlined O, lower U×V','II App.II 1.1 entry','There is no extra zero. The applied left superscript r is correct; also preserve the visible underline beneath O.','amended',r'{}^r\underline{O}_{U\times V}',page=699)
l(22,'3,4','rho_t entry','The section reference is printed with a comma between 3 and 4. The item identifies the numbered section V 3.4; keep that supplied reference separator in corrected text and the comma diplomatically.',page=699)
l(23,'psi with k below','V 7.1 entry','The k is below the baseline. The cited definition on p.360/PDF374 explicitly writes psi^k(x), the coefficient of (-1)^{k-1}t^{k-1} in the logarithmic derivative of lambda_t(x). The operation recorded here is that same coefficient map K->K. Use its defined superscript k in corrected forms.','not applied and now applied',r'\psi^k(x)',page=699)
D[-1]['additional_image']='scan/SGA6_scan_360dpi.pdf#page=374'
patch(699,'current',r'\psi_k(x)',r'\psi^k(x)','fixes/MISPRINTS_6.json#713','Restore the notation of the explicitly cited definition V 7.1.','misprint')
l(24,'x dot_N y','V 5.5 entry on p.700','The main image is blurred here; witness711 clearly shows both x and y, the product dot and its lower N. Keep the applied product.',page=700)
D[-1]['witness']='scan/SGA6_witness_300dpi.djvu#page=711'
l(25,'p.699 begins par.amp and ends nabla','page boundaries','The complete page was compared; the inserted folio-699 marker correctly precedes par.amp.')
l(26,'p.700 begins 1+A[[t]]^+ and ends Z(x)','page boundaries','Six entries occupy this page and the remainder is blank. The inserted marker correctly precedes the first entry.')
# Newly observed local letter forms; exact page evidence, not a global substitution.
for pg in [691,694,695,696,699]:
 chunk=(R/f'build/page_packets/{pg}/diplomatic.tex').read_text()
 # cl_C has no underline; the category letters elsewhere on these pages do.
 if pg==696:
  old=r'\cl_{\mathcal C}';new=r'\cl_C'
  sid=own(pg,'cl_C index entry','plain typed C',old,new,'font','The subscript C has no underline; the other category C letters on this page have distinct strokes.');patch(pg,'both',old,new,sid,'Preserve this local plain letter.');chunk=chunk.replace(old,new)
 n=chunk.count(r'\mathcal C')
 if n:
  sid=own(pg,'category letters in index','underlined typed C and C_0',r'\mathcal C',r'\underline{C}','underline','Every category C on the inspected page has a short underline; preserve the actual typewriter form.')
  patch(pg,'both',r'\mathcal C',r'\underline{C}',sid,'Preserve the inspected underlined category letters.',count=n)
for pg in [692,693,694]:
 chunk=(R/f'build/page_packets/{pg}/diplomatic.tex').read_text();n=chunk.count(r'\(S\)')
 sid=own(pg,'S-category or S-functor entries','underlined S',r'\(S\)',r'\(\underline S\)','underline','The site/category letter S carries a distinct underline in these entries.')
 patch(pg,'both',r'\(S\)',r'\(\underline S\)',sid,'Preserve the inspected underline.',count=n)
sid=own(698,'Hom entry','underlined M below underlined Hom',r'_{\mathcal M}',r'_{\underline{M}}','underline','The main image shows the typed M with a short underline.');patch(698,'both',r'_{\mathcal M}',r'_{\underline{M}}',sid,'Preserve the local underlined category letter.')
sid=own(699,'Parf entry','third S underlined',r'\Parf(S)',r'\Parf(\underline S)','underline','The last S in the row has an underline, confirmed by witness710.');patch(699,'both',r'\Parf(S)',r'\Parf(\underline S)',sid,'Preserve the printed underline.')
sid=own(699,'left superscript r structure sheaf','underlined typed O',r'\mathcal O_{U\times V}',r'\underline{O}_{U\times V}','underline','The O has a distinct underline in main and witness710.');patch(699,'both',r'\mathcal O_{U\times V}',r'\underline{O}_{U\times V}',sid,'Preserve the printed underline.')
sid=own(697,'G_g entry','hat G with subscript g',r'\Gg',r'\Gg','damaged_print','The main image has an ink blot in the subscript. Witness708 clearly shows a lowercase g; the existing macro expands to this reading.');OWN[-1]['witness']='scan/SGA6_witness_300dpi.djvu#page=708';OWN[-1]['verdict']='confirmed'

# Opening five pages of XIV, fully compared after the later pages.
def m(n,reading,region,reason,verdict='confirmed',change=None,page=None):
 f(n,reading,region,reason,verdict,change,batch='666_670')
 if page is not None and page!=D[-1]['page']:
  D[-1]['original_record_page']=D[-1]['page'];D[-1]['page']=page;D[-1]['image']=f'scan/SGA6_scan_360dpi.pdf#page={page+14}'
m(7,'Exposé XIV; capitalized title on the next line','heading','The title occupies its own double-underlined line and has no full stop. The applied words and capitalization agree; accented capitals are the declared transcription convention.')
m(8,'par A. Grothendieck underlined','author line','The underline extends beneath the whole author line; retain it.')
m(9,'quelques uns','first body line','The compound lacks its hyphen. Keep the diplomatic space and the corrected French hyphen.')
m(10,'S. KLEIMAN','first paragraph reference','The surname is capitalized. Retain the applied capitals.')
m(11,'Algebraic cycles and the Weil conjectures dans Dix exposés sur la cohomologie des schémas','first paragraph reference','Both titles are plain; no comma follows conjectures. Keep the applied plain titles and punctuation. The erased line-end remnants do not form additional words.')
m(12,'n° 4','first paragraph near end','The o is raised and no abbreviation point follows n. Keep the applied numéro sign.')
m(13,'Modules','paragraph below the K display','The M is capital. Retain it.')
m(14,'K raised dot at both ends','K_naif -> K display','Both K marks are round raised dots. Keep the applied dot.')
m(15,'un [blank] -homomorphisme','paragraph below the K display','Main and witness678 show an empty space before the hyphen. This is the homomorphism of the two lambda-ring structures just described; keep the supplied lambda in corrected forms and the blank diplomatically.')
m(16,'-homomorphisme with no terminal point','same line and following Dans ce but','Both images omit the sentence stop. Keep the current supplied stop and diplomatic omission.')
m(17,'non addifs','paragraph before the exterior-power display','The printed word lacks it. Correct additifs is already present in current; retain it.')
m(18,'(non addifs en général de "puissance extérieure)','same paragraph','The print omits the closing quotation mark and places the parenthesis after extérieure. In corrected French the parenthetical qualifies the functors as nonadditive; close it after général, then complete the phrase de puissance extérieure with its quotation mark.','amended',"(non additifs en général) de ``puissance extérieure''")
D[-1]['misprint']=True
patch(667,'current',"(non additifs en général de ``puissance extérieure'')","(non additifs en général) de ``puissance extérieure''",'fixes/MISPRINTS_6.json#679','Close the qualification after général and the quotation after extérieure.','misprint')
m(19,'vis à vis','paragraph before (1.1)','Both images omit the compound hyphens. Keep them absent diplomatically and supplied in current French.')
m(20,'cℓ raised dot at both occurrences','(1.1)','The class symbols carry a round raised dot and handwritten looped ell. Retain the applied dots and restore the ell shape locally.','amended',r'\mathrm{c}\ell^\bullet')
m(21,'L with lower dot throughout pp.667–669','complexes in §§1–2','All three pages were read directly, with witnesses678–680 for ambiguous strokes. The dot on L lies on the baseline; the two primes on p.668 stand above it. Restore lower dots only at these inspected occurrences.','not applied and now applied',r'L^\bullet -> L_\bullet; L^{\prime\bullet} -> L\prime_\bullet')
m(22,'typed Q','first paragraph p.668','Witness679 confirms the typed Q without a separate added double stroke. Keep the local plain Q already applied.')
m(23,'Q-algébres','first paragraph','The e has acute accent. Keep the printed accent diplomatically and corrected algèbres in current.')
m(24,'se résoud','first paragraph','The final d is visible in both images. The singular present form is résout; correct current only.','not applied and now applied','se résout')
patch(668,'current','le problème se résoud','le problème se résout','fixes/MISPRINTS_6.json#682','Correct the printed verb ending.','misprint')
m(25,'tensor sign with i above, double-struck L at upper right; alt as superscript','(1.2)','The corrected tensor layout agrees with the print. The L complex dots are handled separately by the inspected lower-dot decision.')
m(26,'i.ème','line below (1.2)','The separator is a full stop. Retain the applied point.')
m(27,'sysmétrique','line describing the group algebra','The extra s is visible. Keep it diplomatically and the current correction symétrique.')
m(28,'coéfficients','same line','The first e bears acute accent. Keep the current corrected coefficients.')
m(29,'Module semi-simplicial','second paragraph, first occurrence','The M is capital. Retain it.')
m(30,'Module semi-simplicial','second paragraph, second occurrence','The repeated M is also capital. Retain it.')
m(31,r'Lambda^i(L.[1]) ≃ (Lambda^i L.)[i] inline','last sentence before §2','The formula is on the running line and its right parenthesis encloses Lambda^i L. before [i]. The applied arrangement matches; lower dots are handled separately.')
m(32,'Exp. 0 4.4,','§2.1','No comma separates the exposé and section numbers. Keep the applied deletion.')
m(33,"d'une démonstration",'first body line p.669','The preceding page ends la clef; this page begins d’une. The current marker is correct.')
m(34,'colon before first §3.1 display','after K raised dot (Y)','The two dots of the colon are visible. Retain it.')
m(35,'colon after (Exp. VII)','before second §3.1 display','A complete colon is printed. Retain it.')
m(36,'f without lower asterisk','right side of second §3.1 display','The asterisk position is empty in both main and witness680. The right member is the pushforward f_*(y′y″c_d(N)) from Gr(Y) to Gr(X), matching the two pushforwards on the left. Keep the supplied star in corrected forms.')
m(37,'Gr(Y) without raised dot, Q underlined','end of second §3.1 display','The omission of the grading dot does not introduce another group: Gr(Y) is the associated graded ring, the direct sum of its graded pieces, and its rationalization is the same ring Gr^bullet(Y)_Q through the identity on every graded piece. Preserve the printed abbreviation, restoring its visible Q underline.','amended',r'\operatorname{Gr}(Y)_{\underline Q}')
patch(669,'current',r"y',y''\in \operatorname{Gr}^\bullet(Y)_\Q",r"y',y''\in \operatorname{Gr}(Y)_\Q",'fixes/MISPRINTS_6.json#686','Retain the unambiguous associated-graded notation without adding a grading placeholder.','rejected_misprint')
m(38,'C-algébres','§2.2','The e has acute accent. Correct it to grave in current French only.','not applied and now applied',r'$\C$-algèbres')
patch(669,'current',r'$\C$-algébres',r'$\C$-algèbres','fixes/MISPRINTS_6.json#687','Correct the printed accent.','misprint')
m(39,'espéces analytiques','§2.2','Both images print espéces. The clause is enumerating spaces (locally compact, C^m, analytic); keep current espaces.')
m(40,'leurs groupes propres sur Y','§2.3','Both images print groupes. The properness condition on a cohomology sheaf is the properness of the restricted morphism Supp H^i(L)->Y. The current supports expresses this condition and is retained.')
m(41,'two commas','end of (3.1), physically p.670','Main and witness681 show two adjacent comma marks. Keep both diplomatically and the single comma in current.',page=670)
m(42,'(3.1) is the first displayed line','top p.670','The complete equation begins this page. The existing marker before its environment is correct.')
m(43,'essentielle- / ment','p.670/671 boundary','The last line of p.670 ends essentielle- and the first line of p.671 begins ment. The exact boundary lies inside essentiellement. Preserve the split in the page marker without inserting a space in the word.')
D[-1]['split_word']={'whole':'essentiellement','before':'essentielle','after':'ment','next_page':671}
m(44,'sans dénominateurs. En fait','first paragraph','En fait continues the same printed paragraph. Keep the applied joining.')
m(45,'f_*:Gr^bullet(Y)->Gr^bullet(X) inline','first paragraph','The map is part of the running line before donnant. Keep the applied inline setting.')
m(46,'f:Gr^bullet(Y)_Q -> Gr^bullet(X)_Q','first paragraph','Both images show f without its star. The rational homomorphism is the extension of the pushforward denoted f_* immediately before, so retain the same pushforward label by adding the lower star in current only.','not applied and now applied',r'$f_*:\operatorname{Gr}^\bullet(Y)_\Q')
patch(670,'current',r"naturel $f:\operatorname{Gr}^\bullet(Y)_\Q",r"naturel $f_*:\operatorname{Gr}^\bullet(Y)_\Q",'fixes/MISPRINTS_6.json#691','Restore the lower star on the rationalized pushforward.','misprint')
m(47,'Gr^bullet(X)_Q. Mais lorsque','first paragraph','Mais lorsque continues the same printed paragraph. Keep the applied joining.')
m(48,'isomorphism arrow with tilde; right K has no dot','middle of first paragraph','The arrow is visible, but both main and witness681 leave the right K dot position empty. Retain the applied isomorphism arrow; remove the supplied right dot from the diplomatic form only.','amended',r'Diplomatic K^\bullet(X)\xrightarrow{\sim}K(X); current retains K_\bullet(X)')
sid=own(670,'regularity isomorphism','right K(X) with blank dot position',r'K^\bullet(X)\xrightarrow{\sim} K_\bullet(X)',r'Diplomatic: K^\bullet(X)\xrightarrow{\sim} K(X); current retains lower dot','misprint','Both scans have no dot after the right K. The next two lines explicitly identify its topological filtration as that of K_·(X), the coherent-sheaf group. The isomorphism takes a vector-bundle class to its coherent-sheaf class. Preserve the blank diplomatically and retain the identifying lower dot in current.');OWN[-1]['witness']='scan/SGA6_witness_300dpi.djvu#page=681'
patch(670,'diplomatic',r'K^\bullet(X)\xrightarrow{\sim} K_\bullet(X)',r'K^\bullet(X)\xrightarrow{\sim} K(X)',sid,'Restore the printed omission of the right K dot.','misprint')
f(1,'n° 1','first paragraph p.671','The abbreviation has a raised o; keep the applied sign.')
f(2,', -ces dernières','§3.2','The hyphen stands directly before ces after the comma. Retain it.')
f(3,'rationelle','§3.2','One n is printed. Correct to rationnelle only in current forms.','not applied and now applied','rationnelle')
f(4,'convainquante','§3.2','The adjective is printed with qu. Corrected French convaincante has c.','not applied and now applied','convaincante')
f(5,'vue notre ignorance','§3.2','The print adds e to the preposition vu. Use the invariable preposition in corrected forms.','not applied and now applied','vu notre ignorance')
f(6,'g_*:A(X)->A(Z) inline','end of §3.2','The map is in the running text and followed by où on the same line. Keep the applied arrangement.')
f(7,'Gysin display ends without punctuation','§3.3','No full stop follows its final parenthesis. Keep the applied removal; the sentence continues below.')
f(8,'(cf. n° 6)','line below the display','The o is raised. Keep the applied form.')
f(9,'relatif SGA 4 XVI 3.7)','p.671/672 boundary','The opening parenthesis is before grâce on p.671. The citation on p.672 begins with SGA, without a second opening parenthesis; the printed closing parenthesis after 3.7 completes that first parenthesis.')
D[-1]['original_record_page']=671;D[-1]['page']=672;D[-1]['image']='scan/SGA6_scan_360dpi.pdf#page=686';D[-1]['additional_image']='scan/SGA6_scan_360dpi.pdf#page=685'
f(10,'prouvée depu','bottom note','Both main and witness682 end the line at depu, with a complete margin. Retain diplomatically and keep current depuis.')
f(11,'P. JOUANOLOU','bottom note','The surname is capitalized. Retain it.')
f(12,'straight-stroke phi','§3.2 display and pp.673–675','All stated occurrences were inspected directly. The printed phi is a typed slashed o. Restore the corresponding straight phi locally.','not applied and now applied',r'\varphi -> \phi locally in XIV')
for old,new,num in [('rationelle','rationnelle',640),('convainquante','convaincante',641),('vue notre ignorance','vu notre ignorance',642)]:patch(671,'current',old,new,f'fixes/MISPRINTS_6.json#{num}','Apply the individually verified French correction.','misprint')
for pg in [667,668,669]:
 chunk=(R/f'build/page_packets/{pg}/diplomatic.tex').read_text()
 for old,new in [(r'L^\bullet',r'L_\bullet'),(r'L^{\prime\bullet}',r"L'_\bullet")]:
  n=chunk.count(old)
  if n:
   sid=own(pg,'complexes in §§1–2','L with baseline dot',old,new,'notation','Every inspected complex L on this page carries a lower dot; primes remain upper indices.');patch(pg,'both',old,new,sid,'Preserve the source dot height.',count=n)
for pg in [667,668,669,670,671]:
 chunk=(R/f'build/page_packets/{pg}/diplomatic.tex').read_text()
 for em in re.findall(r'\\emph\{([^{}]*)\}',chunk):
  sid=own(pg,'underlined words in running text',em+' underlined',r'\emph{'+em+'}',r'\uline{'+em+'}','underline','A separate underline stroke runs beneath this word group; normalem renders emph italic.');patch(pg,'both',r'\emph{'+em+'}',r'\uline{'+em+'}',sid,'Preserve the printed underline.')
sid=own(667,'(1.1)','c followed by looped ell',r'\cl',r'\mathrm{c}\ell','notation','Both class symbols contain a handwritten looped ell, visible in main and witness678.');patch(667,'both',r'\cl',r'\mathrm{c}\ell',sid,'Restore the printed ell shape.',count=2)
for old,new,count in [(r'\mathcal O_i',r'\underline{O}_i',2),(r'\mathcal O_X',r'\underline{O}_X',1)]:
 sid=own(668,'group algebra and structure sheaf','underlined typed O',old,new,'underline','Main and witness679 show a short underline beneath each O.');patch(668,'both',old,new,sid,'Preserve the printed underline.',count=count)
sid=own(669,'second §3.1 display, coefficient Q','underlined typed Q',r'\operatorname{Gr}(Y)_\Q',r'\operatorname{Gr}(Y)_{\underline Q}','underline','The Q in this display is underlined in both scans; the final Q of the page has a doubled stroke and no underline.');patch(669,'both',r'\operatorname{Gr}(Y)_\Q',r'\operatorname{Gr}(Y)_{\underline Q}',sid,'Preserve the local coefficient form.')
sid=own(671,'§3.2 display','straight phi',r'\varphi',r'\phi','notation','The printed slashed-o form has a straight crossing stroke.');patch(671,'both',r'\varphi',r'\phi',sid,'Preserve the printed phi shape.')
sid=own(673,'p.672/673 boundary','dis- / pose','whole dispose displaced across marker','Set folio-673 boundary between dis and pose, preserving dispose as one word','marker','The last line of p.672 ends dis- and p.673 begins pose. A zero-width printed-page boundary must sit inside dispose.');OWN[-1]['additional_image']='scan/SGA6_scan_360dpi.pdf#page=686';OWN[-1]['split_word']={'whole':'dispose','before':'dis','after':'pose','next_page':673}

# Record-level audit after direct collation, including prior Codex proposals.
def codex(index,page,verdict,printed,region,reason,change):
 rec=json.loads((R/'fixes/RECONCILE_CODEX_6.json').read_text())['entries'][index-1]
 D.append(dict(record_type='codex',page=page,source_id=f'fixes/RECONCILE_CODEX_6.json#{index}',codex_id=rec['id'],prior_status=rec['status'],verdict=verdict,printed_reading=printed,image=f'scan/SGA6_scan_360dpi.pdf#page={page+14}',region=region,reason=reason,change=change,forms='French forms and aligned English where the content changes'))
codex(93,667,'confirmed','non addifs','§1 before exterior-power display','The missing it is visible in main and witness678; current additifs is the spelling correction already retained.','Keep current non additifs; preserve addifs diplomatically.')
codex(94,668,'confirmed','coéfficients','§1 group algebra','The acute accent is printed. Keep corrected coefficients and the diplomatic accent.','Retain the existing correction.')
codex(95,669,'confirmed','espéces analytiques','§2.2','The printed word is espéces; the enumerated objects are spaces, and current espaces repairs that word.','Retain current espaces.')
codex(96,669,'confirmed','groupes propres sur Y','§2.3','The morphism whose properness is required is Supp H^i(L)->Y, obtained by restricting f. The current supports names that support and is retained.','Retain current supports; printed groupes diplomatically.')
codex(97,670,'amended','f:Gr^bullet(Y)_Q -> Gr^bullet(X)_Q','§3.1 first paragraph','The star is absent in both images. The rational map is the extension of the pushforward f_* immediately discussed, with the same domain and target. Accept the lower-star correction rejected by reconciliation.','Add the star in current, as MISPRINT691.')
codex(98,671,'confirmed','classes de Chern style Chow','§3.2','The phrase is printed without de. It identifies the same Chow-style Chern classes unambiguously. Adding de edits the author’s elliptical wording.','Confirm rejection; retain style Chow.')
codex(99,671,'confirmed','morphisme propre dans un Z','end of §3.2','The source says dans; the displayed g:X->Z already gives the exact target. Replacing the preposition does not correct a mathematical or textual ambiguity.','Confirm rejection; retain dans.')
codex(100,671,'confirmed','i ≥ d','§3.2 after A^i(X)','Both main and witness682 show the extra lower stroke of the nonstrict inequality. The current inequality already matches the print.','Retain i≥d in both forms.')
codex(115,681,'amended','tels que','§5.1 after first display','The immediately preceding noun phrase is un homomorphisme d’anneaux g^bullet, singular. Its components g^i occur later, inside the quantified clause. Correct tel in current; reconciliation’s rejection is amended.','Apply tel que, as MISPRINT692.')
codex(116,681,'confirmed','Module','§5.1','The M is capital in the source and denotes the sheaf in the author’s convention. Lowercasing it would alter that printed convention.','Confirm rejection; retain Module.')
codex(117,681,'amended','c^i(E)','§5.1 generators of Gr','The source has superscript i. The inspected definition V6.7.1 on p.353 defines c^i(x) through the associated-graded class of gamma^i(x-epsilon(x)); the printed notation is defined and requires no lower-index replacement.','Revert the applied Codex change to c^i(E) in current.')
D[-1]['additional_image']='scan/SGA6_scan_360dpi.pdf#page=367'
codex(118,681,'confirmed','H^2(X,Z_ell(*))','§5.2','The printed exponent is 2, with no star. The full graded map has components in H^{2i}(X,Q_ell(i)); its integral image is in the corresponding direct sum H^{2*}, not solely its i=1 part. Keep the supplied degree asterisk.','Retain current H^{2*}, with printed H^2 diplomatically.')
codex(119,681,'confirmed','se résoud','§5.2','The final d is visible. Keep the corrected present-tense résout.','Retain current spelling correction.')
codex(120,681,'confirmed','à priori','§5.2','The printed locution has à. It is intelligible as written; replacing it with a Latinized spelling is editorial standardization.','Confirm rejection; retain à priori.')
codex(144,674,'confirmed','Gr_top^bullet et Gr^bullet(X)','§4.1','The first group suppresses X while the second writes it. Both refer to the fixed X of the paragraph; the identity of each already specified associated-graded object is unchanged by the abbreviation.','Confirm rejection; retain the omitted argument, as MISPRINT650 decision.')
codex(145,676,'confirmed','c_i(Y)=n(Y)cℓ(Y)','§4.3 first display','The paragraph explicitly calls its left side the first member of (4.5), namely c_i(O_Y). Here Y abbreviates the class of i_*O_Y in K(X); applying c_i to that same class gives the printed shorthand. No added O_Y is required.','Confirm rejection; retain c_i(Y).')
codex(146,676,'amended','deg(Y·ξ^i)>0','§4.3 polarization argument','The printed exponent is i. The class of Y has codimension i, ξ has codimension one, and degree is defined on codimension dim X cycles. Hence its exponent is dim X-i=dim Y. Accept this correction with the explicit grading calculation, as MISPRINT714.','Change the exponent to dim Y in current.')
codex(147,678,'confirmed','SO(n) for n≥7','§4.5 classification sentence','The source prints SO(n). The central spin covering q:Spin(n)->SO(n), with Borel preimage B_tilde=q^{-1}(B), induces the isomorphism Spin(n)/B_tilde -> SO(n)/B. The flag variety example is therefore the same through this specified quotient map; replacing the group name is unnecessary.','Confirm rejection; retain SO(n).')
codex(148,679,'amended','cℓ raised dot (Y)','§4.6, class in K^bullet(X)','The scan’s superscript is a round dot. The earlier Codex surface c_l^i is a transcription error, and its HOLD version without the dot also omits the observed mark. The present checker-corrected expression already has the right dot.','Use the observed cℓ^bullet(Y), already applied, instead of either old Codex surface.')
codex(149,679,'confirmed','Im(K(Z)->K(X))','§4.6 localization clause','Both K letters lack dots. Localization supplies G_0(Z)->G_0(X)->G_0(X-Z)->0; regularity identifies K_0(X) and K_0(X-Z) with these coherent groups by the vector-bundle-to-coherent-class maps. Z is the singular locus and is not given a resolution hypothesis. Replacing its K(Z) by the perfect-complex K^bullet(Z) is unsupported; keep the printed shorthand for the coherent source of localization.','Confirm rejection; retain K(Z)->K(X).')
codex(150,679,'amended','A^0(X)=Z','end of §4.7','For X=G/B, the pullback π^*:A^0(X)->A^0(G) sends [X] to [G] and is an isomorphism Z->Z. The printed use of A^0(X) through this specified degree-zero identification is valid.','Revert the applied replacement A^0(G) to printed A^0(X).')
codex(151,679,'confirmed','Modules inversibles','§4.7','The capital M is visible in the author’s sheaf terminology. Keep it; the later lowercase modules in the parenthesis is also printed and remains unchanged.','Confirm rejection; retain the source capitalization.')
codex(152,686,'confirmed','cône projetant C','§8.1 near page end','The scan clearly prints projetant. It is the author’s term for the cone projecting the given projective variety; no corruption of this word is visible. The proposed projectif is an editorial replacement of that valid term.','Confirm rejection; retain projetant.')
codex(153,688,'confirmed','(SGA 6)','bibliography [16]','The printed number is 6; the topos and étale-cohomology title and its references elsewhere in XIV identify SGA4. Keep current 4 and diplomatic6.','Retain SGA4 correction.')
codex(154,688,'amended','U. Mausin','bibliography [17]','Both images print U. Mausin; the next page explicitly names MANIN for entry17. Correct the surname to Manin, without expanding the printed initial to Yu. I.','Use U. Manin in current, as amended MISPRINT663.')
codex(155,689,'confirmed','sans hyperplan quasi-projectif','note (*)','Both images print hyperplan. The clause removes the quasi-projectivity hypothesis and adds the smooth relative setting; retain current hypothèse quasi-projective.','Retain the applied correction.')
codex(156,689,'confirmed','MANIN 17; dans 16','note (**)','The numbers are bare in both images and refer unambiguously to the bibliography. Added brackets standardize citation punctuation.','Confirm rejection; retain the bare numbers.')
codex(157,696,'confirmed','D(f)_parf, D(f)_underlined-parf','III4.2 entry','The second parf has its own underline, visible in the main image. The current index already preserves this distinction.','Retain the two different printed forms.')
codex(158,697,'confirmed','D(X)_{f-parf}, D(X)_{f-underlined-parf}','III4.2 first pair','Only the second parf is underlined; its f is not. The current index agrees.','Retain the current underlining.')
codex(159,697,'confirmed','D(X)_{Y-parf}, D(X)_{Y-underlined-parf}','III4.2 second pair','The second parf is underlined, with Y unlined in both objects. The current index agrees.','Retain the current underlining.')
# The tagged-tree records repeat these exact, individually reviewed proposals.
for tag,queue in [(376,100),(377,146),(378,148),(379,149),(380,150),(381,117),(382,152),(383,154),(384,155),(385,156)]:
 q=next(z for z in D if z['source_id']==f'fixes/RECONCILE_CODEX_6.json#{queue}')
 rec=json.loads((R/'fixes/RECONCILE_CODEX_6.json').read_text())['entries'][tag-1]
 D.append({**q,'source_id':f'fixes/RECONCILE_CODEX_6.json#{tag}','prior_status':rec['status'],'related_record':q['source_id'],'reason':'The tagged-tree proposal has the same inspected locus. '+q['reason']})
# Remaining FIXLOG rows use differing anchors for the same inspected changes.
for line,source in [(559,93),(560,94),(561,95),(562,96),(563,150),(565,118),(566,119),(567,153),(568,155)]:
 q=next(z for z in D if z['source_id']==f'fixes/RECONCILE_CODEX_6.json#{source}')
 D.append({**q,'record_type':'fixlog','source_id':f'fixes/FIXLOG_6_CURRENT.jsonl#{line}','related_record':q['source_id']})
for path,line in [('fixes/FIXLOG_6.jsonl',347),('fixes/FIXLOG_6_CURRENT.jsonl',312)]:
 D.append(dict(record_type='fixlog',page=689,source_id=f'{path}#{line}',verdict='confirmed',printed_reading='No Ob text occurs in the final notes or either index.',image='scan/SGA6_scan_360dpi.pdf#page=703',region='after the final note, macro setup before index',reason='This row changes an unused macro declaration from providecommand to renewcommand. Direct reading of pp.689–700 finds no printed Ob to alter, and source inspection finds no later use. It has no visible textual effect and may remain as implementation.',change='Retain the inert declaration change; no reader-text variant.',forms='Both French source layers; no English text change.'))
# HOLD comparisons111–119 all lie in the inspected late pages.
def hold(index,page,verdict,printed,region,reason,change):
 D.append(dict(record_type='hold',page=page,source_id=f'fr/codex/HOLD_VS_CORR.json#{index}',verdict=verdict,printed_reading=printed,image=f'scan/SGA6_scan_360dpi.pdf#page={page+14}',region=region,reason=reason,change=change,forms='French forms and aligned English where content changes'))
hold(111,671,'confirmed','i≥d','§3.2','The only listed tree difference is an editorial source comment; the displayed inequality is source-correct in both. Main and witness682 confirm ≥.','No body-text change; retain the source comment only as provenance.')
hold(112,676,'amended','deg(Y·ξ^i)>0','§4.3','The main image prints i. The explicit codimension calculation i+dimY=dimX proves that degree uses ξ^{dimY}; the HOLD correction is accepted only in corrected forms.','Keep i diplomatically, dimY in current; linked MISPRINT714 and Codex001450.')
hold(113,679,'amended','cℓ^bullet(Y), cℓ^bullet(Y′); K(Z)->K(X)','§4.6, beginning on p.678','The main image shows raised class dots and no dots on the two K letters in the localization image. Restore those actual class dots, retaining K(Z)->K(X); the coherent localization maps and regular-X identifications justify that shorthand.','Use source dots for cℓ and preserve the printed K abbreviations; linked Codex001452/001453.')
D[-1]['additional_image']='scan/SGA6_scan_360dpi.pdf#page=692'
hold(114,679,'amended','A^0(X)=Z','end §4.7','The print has X. Pullback for π:G->G/B identifies A^0(G/B)=Z with A^0(G)=Z by [G/B]↦[G]. The source notation is valid through this specific map.','Reject the HOLD replacement G; retain X in both forms.')
hold(115,681,'amended','tels; Module; c^i(E); g raised dot','§5.1','The scan prints all four readings. Singular homomorphisme requires tel in current; the author’s capital Module stays; c^i is explicitly defined in V6.7.1; g has an observed raised dot.','Keep current tel, retain Module and c^i(E), and render g with its raised dot.')
D[-1]['additional_image']='scan/SGA6_scan_360dpi.pdf#page=367'
hold(116,686,'confirmed','cône projetant C','§8.1','The source reads projetant and the term is valid. HOLD projectif is an editorial substitution. The surrounding arithmétiques error is separately corrected in current on p.687.','Retain projetant in both forms.')
hold(117,688,'confirmed','U. Mausin','bibliography[17]','The listed tree difference is only the Codex comment. Direct image reading additionally settles the edited name as U. Manin, retaining the initial rather than expanding it.','No comment-derived text change; name follows amended MISPRINT663.')
hold(118,689,'confirmed','sans hyperplan quasi-projectif','note (*)','The source visibly has hyperplan. The corrected reading hypothèse quasi-projective repairs the stated removed hypothesis, as separately reviewed in MISPRINT668.','Retain HOLD/current correction hypothèse quasi-projective.')
hold(119,689,'confirmed','MANIN 17; dans 16','note (**)','The bare numerals are clearly printed and unambiguously identify entries17 and16. HOLD brackets are punctuation standardization.','Retain the bare source citations in both forms.')

# Duplicate fixlog and misprint records receive the same explicitly reviewed decision.
for path in ['fixes/FIXLOG_6.jsonl','fixes/FIXLOG_6_CURRENT.jsonl']:
 for i,x in enumerate((R/path).read_text().splitlines(),1):
  rec=json.loads(x)
  for q in list(D):
   if q['record_type']!='checker' or q.get('original_record_page',q['page'])!=rec.get('page'): continue
   source=F[q['source_id'].split('/')[-1]]; fix=source.get('fix')
   if fix and fix.get('old')==rec.get('old') and fix.get('new')==rec.get('new'):
    z={**q,'record_type':'fixlog','source_id':path+f'#{i}','related_finding':q['source_id']}
    # Diplomatic restoration itself stands even where misprint status is rejected.
    if q['kind']=='misprint_in_print' and path.endswith('FIXLOG_6.jsonl') and q['verdict']=='amended': z['verdict']='confirmed'; z['change']=rec['new']; z['reason']='The diplomatic restoration agrees with the printed text. '+q['reason']
    D.append(z); break
for i,x in enumerate(json.loads((R/'fixes/MISPRINTS_6.json').read_text()),1):
 for q in list(D):
  if q['record_type']=='checker' and q.get('original_record_page',q['page'])==x['page'] and q['where']==x['where']:
   D.append({**q,'record_type':'misprint','source_id':f'fixes/MISPRINTS_6.json#{i}','related_finding':q['source_id'],'misprint':q.get('misprint',q['verdict']!='amended'),'correction':q['change'] if q['verdict']=='amended' else x['correct']});break
for page in [667,668,669,670,671,672,673,674,675,676,677,678,679,680,681,682,683,684,685,686,687,688,689,690,691,692,693,694,695,696,697,698,699,700]:
 STATUS.append(dict(page=page,pdf_page=page+14,checked_against_scan=True,scan='scan/SGA6_scan_360dpi.pdf',regions='two overlapping full-width strips covering all body text and footnotes, 252 dpi',findings=sum(q['page']==page for q in OWN),second_reading='fr/codex/sga6_fr_r1_fr.tex' if 672<=page<=689 else None,note='Full body compared; document-wide notation choices and exact split-word page-break representation are recorded for coordinator.'))
for row in STATUS:
 if row['page']==690:
  row['regions']='entire blank verso in main PDF and witness'
  row['witness']='scan/SGA6_witness_300dpi.djvu#page=701'
  row['note']='No printed text or folio on this verso; add marker between the final p.689 note and the p.691 index setup.'
for name,rows in [('decisions.jsonl',D),('patches.jsonl',P),('own_findings.jsonl',OWN),('page_status.jsonl',STATUS)]:
 (O/name).write_text(''.join(json.dumps(x,ensure_ascii=False)+'\n' for x in rows))
print('decisions',len(D),'patches',len(P),'own findings',len(OWN),'pages',len(STATUS))
