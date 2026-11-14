"""Direct scan collation of Exposé XII. Explicitly reviewed findings only."""
from pathlib import Path
import json,re
R=Path(__file__).resolve().parents[2];O=R/'review/expose_xii';F={};D=[];P=[];OWN=[];STATUS=[]
for path in sorted((R/'check/findings').glob('*.json')):
 for i,x in enumerate(json.loads(path.read_text()),1):F[f'{path.name}#{i}']={**x,'source_id':str(path.relative_to(R))+f'#{i}'}
def f(n,printed,region,reason,verdict='confirmed',change=None,batch='596_600',page=None):
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
 sid=f'ASTRA-XII-{len(OWN)+1:04d}';OWN.append(dict(record_type='own',page=page,source_id=sid,verdict=verdict,where=where,printed_reading=printed,tex=tex,change=change,kind=kind,reason=reason,image=f'scan/SGA6_scan_360dpi.pdf#page={page+14}',region=where,forms='French forms; English where content changes'));return sid
def layer_text(page,layer):
 text=(R/f'build/page_packets/{page}/{layer}.tex').read_text()
 for line in (R/'review/middle/patches.jsonl').read_text().splitlines():
  z=json.loads(line)
  if z['page']==page and z['layer'] in (layer,'both'):
   assert text.count(z['old'])==z.get('expected_count',1),(page,layer,z['source_id'],'root anchor')
   text=text.replace(z['old'],z['new'])
 for z in P:
  if z['page']==page and z['layer'] in (layer,'both'):
   assert text.count(z['old'])==z['expected_count'],(page,layer,z['source_id'],text.count(z['old']),z['expected_count'])
   text=text.replace(z['old'],z['new'])
 return text
def statement(page,start,end,where,exceptions=(),plain_fragments=(),once_exceptions=()):
 # The selected spans and exclusions are explicitly read from the page images.
 # Math and list commands remain separate; no rule is drawn across a formula.
 reason='The directly inspected statement underlines its prose word groups; mathematical symbols retain their independently observed local underlines. Named statement headings follow NOTE_6. '
 if exceptions:reason+='Printed unlined terms retained: '+', '.join(exceptions)+'. '
 if plain_fragments:reason+='Unlined intervening fragments retained: '+', '.join(repr(t) for t in plain_fragments)+'. '
 if once_exceptions:reason+='Only the first occurrence of each of these terms is unlined: '+', '.join(once_exceptions)+'. '
 sid=own(page,where,'Prose word groups underlined, formulas independently styled','Roman statement prose','Insert explicit word-group \\uline commands in both layers.','underline',reason)
 totals={}
 for layer in ('diplomatic','current'):
  text=layer_text(page,layer);assert text.count(start)==1,(page,start)
  a=text.index(start)+len(start);b=text.index(end,a) if end else len(text)
  old=text[a:b]
  protect=r'(\\\([\s\S]*?\\\)|\\\[[\s\S]*?\\\]|\\begin\{equation\}[\s\S]*?\\end\{equation\}|\\begin\{enumerate\}(?:\[[^\]]*\])?|\\end\{enumerate\}|\\item\b)'
  pieces=re.split(protect,old);count=0;seen=set();terms=exceptions+once_exceptions
  for k in range(0,len(pieces),2):
   chunk=pieces[k]
   if chunk in plain_fragments:continue
   ss=re.split('('+'|'.join(re.escape(t) for t in terms)+')',chunk) if terms else [chunk]
   for j in range(len(ss)):
    if j%2:
     if ss[j] in exceptions:continue
     if ss[j] in once_exceptions and ss[j] not in seen:seen.add(ss[j]);continue
    core=ss[j].strip()
    if not re.search(r'[A-Za-zÀ-ÿ]',core):continue
    lead=ss[j][:len(ss[j])-len(ss[j].lstrip())];tail=ss[j][len(ss[j].rstrip()):]
    ss[j]=lead+r'\uline{'+core+'}'+tail;count+=1
   pieces[k]=''.join(ss)
  new=''.join(pieces);assert new!=old
  patch(page,layer,old,new,sid,reason+f'Exact local count: {count} prose underline groups in this {layer} span.','underline')
  totals[layer]=count
 OWN[-1]['local_counts']=totals
 OWN[-1]['change']='Insert explicit word-group \\uline commands; '+', '.join(f'{k}: {v} groups' for k,v in totals.items())+'.'
CHECKED=[]
# Each of595–600 compared in both main strips; witness608 and611 resolves small indices.
f(21,'EXPOSE XII; two capital title lines, double underlined','heading595','The chapter number has a single underline and no stop. Both title lines have double underlines. The applied wording and capitals match; restored capital accents follow NOTE_6.',batch='591_595')
f(22,'par M. Raynaud (rédigé par S. Kleiman), underlined','author line595','The full mixed-case author line has one continuous underline. The applied form matches.',batch='591_595')
f(23,'C07-C11, typed hyphen','Avertissement, FGA reference','The range has one short typed hyphen. The applied reading matches; no bibliographic content changes.',batch='591_595')
f(24,'Fondements de la Géométrie Algébrique in straight double quotes','Avertissement','The source has quotes and no underline or italics around the book title. Retain the applied quotation marks under the volume quotation convention.',batch='591_595')
f(25,'I. Castelnuovo','Avertissement, second paragraph','The capital I and its stop are clear. The historical university archive identifies the algebraic geometer as Guido Castelnuovo (1865–1952); the concise primary metadata is archived in review/expose_xii/evidence/castelnuovo.json. Correct the initial to G in current only.','not applied and now applied','G. Castelnuovo',batch='591_595')
patch(595,'current','I. Castelnuovo','G. Castelnuovo','fixes/MISPRINTS_6.json#534','Use the verified initial of Guido Castelnuovo.','misprint')
f(1,'first Pic underlined','Theorem1.1 display','The separate rule under Pic ends before Y/S. The applied underline matches.')
f(2,'restriction |V, V on the baseline','Theorem1.1 display, source','The V is level with Pic, not subscripted. The applied form matches.')
f(3,'second Pic underlined','Theorem1.1 display','The target Pic has its own rule, ending before X/S. The applied underline matches.')
f(4,'restriction |V, V on the baseline','Theorem1.1 display, target','The second V is also level with Pic. The applied form matches.')
f(5,'plain Pic followed by baseline |V','Corollaire1.2','The rule under the preceding words stops before Pic; V is on the line. Retain this local plain Pic and the applied restriction.')
f(6,'Pic underlined','recalled FGA result, representing group scheme','The source explicitly underlines Pic here despite calling it a representing scheme. The applied underline preserves the printed local notation.')
f(7,'La considération begins an indented paragraph','proof1.2','The new paragraph begins after présentation finie. The applied division matches.')
f(8,'Pic underlined after décomposer','proof1.2, Hilbert polynomials','The short rule under Pic is visible. The applied underline matches.')
f(9,'Pic^q underlined under Pic only','proof1.2, sum of opens','The rule lies under Pic and ends before X/S. The applied form matches.')
f(10,'Pic^q underlined under Pic only','proof1.2, type-finite assertion','The later Pic^q again has a short underline. The applied form matches.')
f(11,'uti- at line end, then sant','last sentence before1.3','Joining the printed word across the line gives utisant, with li absent. Retain the diplomatic omission and existing current utilisant.')
f(12,'statement word groups underlined around unlined mathematical symbols','statements596–600','All five full pages were compared. Theorem1.1, Corollaries1.2,1.5,1.6, Lemmas1.3,1.4 and assertionsI,II,II′ show the recorded word-group underlining. Explicit local patches now supply the missing prose underlines, with counts. The unlined intègre and surjectif in1.1/1.2, f.p.p.f abbreviation and Murre attribution remain plain; local Pic underlines remain individually specified.','not applied and now applied','Apply the exact statement-underlining spans recorded in ASTRA-XII own findings.')
f(13,'S′→V tels, no comma','first line597','No comma follows V before tels. The applied omission matches.')
f(14,'X_{S_i}, dotted i','proof1.3','Main and witness608 show a dotted i, unlike the nearby flagged1. The sentence chooses the open S_2⊂S_1 on which the reduced components become integral over the base. Their restriction is X×_S S_2; the final S′=h^{-1}(V) lies inside S_2 because V excludes h(S_1−S_2). Thus current must use X_{S_2}, not the attached X_{S_1}.','amended',r'X_{S_2}')
patch(597,'current',r'\(X_{S_1}\), munie',r'\(X_{S_2}\), munie','fixes/MISPRINTS_6.json#571','Use the explicitly chosen open restriction on which the component property holds.','misprint')
f(15,'muni without final e','proof1.3','The printed participle lacks e. Its subject is toute composante, also explicitly feminine in the opening statement; retain current munie.')
f(16,'sur S_i, dotted i','proof1.3','The second index is the same dotted i in main and witness608. The integrality holds over the chosen open S_2, and the final S′ maps into that open. Correct the attached current S_1 to S_2 together with the preceding X restriction.','amended','S_2')
patch(597,'current',r'sur \(S_1\) (EGA',r'sur \(S_2\) (EGA','fixes/MISPRINTS_6.json#573','Use the same open base as in X_{S_2}.','misprint')
f(17,'v=v_1−h(S_1−S_2), small v twice','proof1.3','Both v letters are visibly lower than the capital V in h^{-1}(V). The expression constructs the open V from V_1, so retain the current capitalization.')
f(18,'both Pic symbols underlined','proof1.2, product formula','Both rules are visible in main and witness608; the product index i and the scheme subscripts are outside them. The applied forms match.')
f(19,'Enfin,1.1 begins an indented paragraph','proof1.2','The new paragraph follows the type-finite group-scheme assertion. The applied division matches.')
f(20,'both Pic symbols underlined','proof1.2, f* morphism','Both source and target Pic have separate short rules. The applied underlines match.')
f(21,'Pic_{Z′/S′}, prime on Z','proof1.2, target of f*','A prime is printed after Z. The immediately defined map is f:Z=∐Z_i→X′; its pullback sends a line bundle on X′ to its pullback on Z. Retain current Z, without the spurious prime.')
f(22,'réprésentable, acute over first e','proof1.2','The extra acute is visible. Retain diplomatic réprésentable and current représentable.')
f(23,'plain Pic followed by |V on the line','end of proof1.2','The Pic is unlined here and V is baseline. The applied form matches.')
sid=own(597,'proof1.2, integrality of Chow components','Z_i intègre sur S',r'on peut supposer \(Z_i\) intègre sur \(S\)',r"on peut supposer \(Z_i\) intègre sur \(S'\)",'mathematical_source_correction','Both main and witness608 have S without a prime. The components X′_i are geometrically integral over S′ by1.3; the birational Chow maps Z_i→X′_i preserve their generic function fields, so the cited openness argument applies to Z_i→S′. Their structure maps to S are the composites Z_i→S′→S and need not have geometrically integral fibres. Explicitly, take S=Spec R, X=Spec C and S′=Spec C. Then X_{S′}=Spec(C⊗_R C)=Spec(C×C), each component and its identity Chow presentation is Spec C, geometrically integral over S′. Over S its geometric base change has two components, and S has no smaller nonempty open. The printed unprimed assertion is therefore false. Restore S′ in current, matching the following Pic_{Z_i/S′} construction.');patch(597,'current',r'on peut supposer \(Z_i\) intègre sur \(S\)',r"on peut supposer \(Z_i\) intègre sur \(S'\)",sid,'Use the base of the stated geometrically integral components and their relative Picard schemes.','misprint')
f(24,'SGA3 1.4.2, digit1 and stop','first paragraph598','The first character has the flagged shape of1, followed by its stop. Retain the applied reference; the exposé is implicit from the preceding SGA3 VI_B citation.')
f(25,'Pic underlined','Corollaire1.5(a)','The short rule ends before X/k. The applied underline matches.')
f(26,'both Pic symbols underlined','Corollaire1.5(b)','Both rules are separately visible. The applied forms match.')
f(27,'both Pic symbols underlined','Corollaire1.6(a)','The source and target functor symbols each have a rule. The applied forms match.')
f(28,'Pic underlined','Corollaire1.6(b), opening','The first Pic in this assertion is separately underlined. The applied form matches.')
f(29,'voluatif','Corollaire1.6(b)','The source types o after v. The established criterion is valuatif; retain the existing current spelling correction.')
f(30,'both Pic symbols underlined','Corollaire1.6(b), concluding morphism','Both functor symbols have their own rules. The applied forms match.')
f(31,'En effet begins an indented paragraph','proof1.6','The proof is visibly separated from the two-item statement. The applied paragraph division matches.')
f(32,'i at right of left downward arrow','first diagram599','The label i is on the inner, right side of the arrow X_red→X. The applied placement matches.')
f(33,'f above the bottom horizontal arrow','first diagram599','The label is above X→Y. The applied placement matches.')
f(34,'comma after the first diagram','first diagram599','The comma is visibly aligned with the bottom row at its right. The applied punctuation matches.')
f(35,'both Pic symbols underlined in top row','second diagram599','Each top-row Pic has a short rule, ending before its scheme subscript. The applied forms match.')
f(36,'both Pic symbols underlined in bottom row','second diagram599','Each bottom-row Pic also has a short rule. The applied forms match.')
f(37,'comma after the second diagram','second diagram599','The comma is visible to the right of Pic_{Y/S}. The applied punctuation matches.')
f(38,'comma after the first diagram','first diagram600','The comma follows the bottom-right coproduct node. The applied punctuation matches.')
f(39,'no word between the two diagrams','top600','The blank area between diagrams contains no et. The applied omission matches.')
f(40,'top-left Pic underlined','second diagram600','The separate rule under Pic_{Y/S} is visible. The applied form matches.')
f(41,'both top-right Pic symbols underlined','second diagram600','Both Pic in the equality have short rules. The applied forms match.')
f(42,'bottom-left Pic underlined','second diagram600','The separate rule under Pic_{X/S} is visible. The applied form matches.')
f(43,'circled3 above the lower arrow','second diagram600','The numeral and its circle are above the arrow. The applied placement matches.')
f(44,'both bottom-right Pic symbols underlined','second diagram600','Both Pic in the equality have short rules. The applied forms match.')
f(45,'bare coproduct in the scheme sequence','first sequence600','No index appears under this coproduct. The i belongs only to X_i; retain the applied omission.')
f(46,'no word between the two sequences','middle600','The two displays are separated by blank space, with no et. The applied omission matches.')
f(47,'bare coproduct in the middle Pic subscript','second sequence600','The coproduct has no index in main or witness611. The diplomatic form already matches, and the coordinator’s replay18 patch removes the extra current index together with the next occurrence.')
f(48,'short prime after X','second sequence600','Main and witness611 both show a separate short mark above and to the right of X. Preserve that prime diplomatically. The preceding scheme sequence uses ∐X_i, and pullback of its two maps gives Pic_{X_0/S}←Pic_{∐X_i/S}←Pic_{Y/S}; retain the current removal of the prime.')
f(49,'Pic_{X_i/S} underlined; following coproduct Pic plain','sentence after the sequences','Only the first Pic has a short rule. The two forms are separately clear in witness611; retain the applied local distinction.')
f(50,'bare coproduct in the following plain Pic','sentence after the sequences','No index is printed beneath the coproduct in either scan. The coordinator’s replay18 patch handles the two current occurrences; no duplicate patch is issued here.')
f(51,'600 ends si et seulement si;601 begins the fibre-intersection equality','boundary600/601','The600 lower image and the directly inspected601 upper image place the boundary before (X_i)_η∩(X_j)_η=∅. The attached marker is exact.')
CHECKED.extend(range(595,601))

statement(596,r'\textbf{Théorème 1.1.}',r'\textbf{Corollaire 1.2.}','Theorem1.1 statement',exceptions=('intègre','surjectif.','f.p.p.f)'))
statement(596,r'\textbf{Corollaire 1.2.}','\n\nEn effet rappelons','Corollary1.2 statement',exceptions=('intègre.',))
statement(596,r'\textbf{Lemme 1.3.}',None,'Lemma1.3 first part')
statement(597,'%%%%%%%%%%  scan idx 610  |  folio 597  %%%%%%%%%%\n','\n\nEn effet il existe','Lemma1.3 continuation')
statement(597,r'\textbf{Lemme 1.4.}','\n\nEn effet soit','Lemma1.4 statement')
statement(598,r'\textbf{Corollaire 1.5.}',r'\textbf{Corollaire 1.6.}','Corollary1.5 statement',exceptions=('(J. P. Murre).',))
statement(598,r'\textbf{Corollaire 1.6.}','\n\nEn effet dans','Corollary1.6 statement')
statement(599,r'\begin{enumerate}[label=\Roman*.]',r'\end{enumerate}','Assertions I and II',exceptions=('1.1',))
statement(600,"à démontrer II'.",'\n\nPour','Assertion II prime',exceptions=('1.1',))

# Page601 read in both full-width strips.
f(1,'601 begins with (X_i)_η∩(X_j)_η=∅','top601','The equality is the first body text on the page, continuing the final clause on600. The attached marker is exact.',batch='601_605')
f(2,'de la, followed by the Proposition2.3 heading','end of first paragraph601','The typescript has neither proposition suivante nor a closing stop before the heading. The applied text matches.',batch='601_605')
f(3,'g_i=g|Y_i, Y_i on the baseline','Proposition2.3(b)','The restriction places Y_i at the height of g, not below the bar. The applied form matches.',batch='601_605')
f(4,'Après begins an indented paragraph','last paragraph601','The paragraph is visibly separate from the preceding section construction. The applied break matches.',batch='601_605')
f(5,'both Pic symbols underlined','Proposition2.3 conclusion','Both short rules lie beneath Pic and end before the scheme indices. The applied local underlines match.',batch='601_605')
f(6,'Pic underlined after μ:S→','last two lines601','The short rule under Pic is clear. The applied form matches.',batch='601_605')
f(9,'target Y_k without a coproduct','first paragraph601','Each f_k maps its component coproduct into Y_k; the displayed map ∐_k f_k has domain the coproduct over all k and codomain ∐_k Y_k=X. The source omits the outer target coproduct. Retain its existing current correction.',batch='601_605')
f(10,'celà with grave accent','proof2.3, first paragraph','The grave is visible. The current cela corrects this spelling error.',batch='601_605')
sid=own(601,'all six structure-sheaf letters','plain typed O','six occurrences of \\mathcal O','Use plain O, retaining each subscript.','font','Both the four letters in hypothesis(b) and the two letters in the first exact sequence are plain typed O. No script form or underline is printed. Preserve the source form in both layers.');patch(601,'both',r'\mathcal O','{O}',sid,'Restore the six locally observed plain structure-sheaf letters; braces delimit adjacent control words.','font',count=6)
statement(601,r'\textbf{Proposition 2.3.}','\n\nEn effet notons','Proposition2.3 statement',plain_fragments=(' et ',))
CHECKED.append(601)

# Page602 read in both main strips and witness613.
f(7,'first Pic underlined','first line602','The short rule is present in main and witness613. This occurrence belongs to602 after the corrected marker, not601 as in the old finding.',batch='601_605',page=602)
f(11,'Pic_{Y/S} qui est begins602','boundary601/602','601 ends sous-foncteur de; both scans of602 begin with the underlined Pic. The attached marker matches.',batch='601_605')
f(12,'Pic underlined after λ:S→','first paragraph602','The λ-associated Pic has a short rule; the later Pic_{Y_1∐Y_2/S} is visibly plain. Preserve both local forms.',batch='601_605')
f(13,'Pic underlined after point λ de','end of second paragraph602','The rule is clear in both scans and ends before the subscript. The applied form matches.',batch='601_605')
f(14,'Pic underlined after image réciproque de μ dans','third paragraph602','Both scans show a separate short rule. The applied form matches.',batch='601_605')
f(15,'Isom underlined, parentheses and arguments unlined','Lemma2.4 introduction','The rule covers the operator name only. The applied form matches.',batch='601_605')
f(16,'Isom underlined in item(i)','Lemma2.4(i)','The operator has its own underline, separate from the following prose rule. The applied form matches.',batch='601_605')
f(17,'both Y_1∩Y_2 restrictions on the baseline','first paragraph602, φ','Both scans place each restricted scheme at the height of L. The applied forms match.',batch='601_605')
f(18,'first Y_1∩Y_2 restriction on the baseline','Réciproquement, source of φ','The Y letters are level with L_1. The applied form matches.',batch='601_605')
f(19,'second Y_1∩Y_2 restriction on the baseline','Réciproquement, target of φ','The Y letters are level with the target L. The applied restriction is exact; its Z index is separately retained diplomatically.',batch='601_605')
f(20,'both (Y_1∩Y_2)_T restrictions on the baseline','Finalement, family of isomorphisms','Both leading parentheses are on the line with (L_i)_T. The applied forms match.',batch='601_605')
f(21,'Réciproquement begins an indented paragraph','middle602','The printed paragraph is separated and indented. The applied break matches.',batch='601_605')
f(22,'colon before Lemma2.4','end of paragraph preceding Lemma2.4','Witness613 resolves two round dots, unlike the comma tail in the earlier semicolon after suivant φ. Retain the applied colon.',batch='601_605')
f(23,'capital Z as target index','Réciproquement, target L_Z','Both scans show the straight diagonal and horizontal strokes of Z, unlike the curved2 in the adjacent Y_2. The target is the already defined L_2 on Y_2, so retain current L_2.',batch='601_605')
sid=own(602,'two rigidification targets','plain O_S twice','two occurrences of \\mathcal O_S','Use plain O_S in both targets.','font','The two O letters in the rigidification isomorphisms are plain typed letters, clear in main and witness613.');patch(602,'both',r'\mathcal O','{O}',sid,'Preserve the two plain structure-sheaf letters and safe TeX token boundaries.','font',count=2)
statement(602,r'\textbf{Lemme 2.4.}',None,'Lemma2.4 first part')
CHECKED.append(602)

# Page603 read in both main strips and witness614.
f(24,'first Isom underlined','Lemma2.4(ii), continuation603','Both scans show the operator rule. Diplomatic already has it; the coordinator’s replay16 patch restores the current rule lost beside formé. Our prose patch is anchored after that replay.',batch='601_605')
f(25,'final Isom underlined','Lemma2.4(ii), final line','The final operator has a distinct short rule, clear in both scans. The attached form matches.',batch='601_605')
f(26,'En effet begins an indented paragraph','proof2.4','The proof is visibly separated from the end of the statement. The applied break matches.',batch='601_605')
f(27,'formée with final e','Lemma2.4(ii)','The extra e is visible. The grammatical subject le sous-foncteur is masculine; retain current formé.',batch='601_605')
f(28,'small s in V(E)×_sV(F)','proof2.4','Witness614 confirms that the fibre-product index is the small form s. Both representing vector bundles are over S, and a T-point is a pair (u,v) over the same T→S. Thus their representing product is over S; retain the current capital S.',batch='601_605')
f(29,'f_*O_Y','display(*)','Both scans plainly print subscript Y. The map f has source X, and its direct image sends sheaves on X to sheaves on Y; the unit O_Y→f_*O_X followed by the two pullbacks from X×_YX is the displayed descent sequence. Retain the current O_X.',batch='601_605')
f(30,'small y in X×_yX','display(*)','The index descends below the baseline and is a small y in both scans. The two projections have common target X over the specified f:X→Y, so their fibre product is X×_YX. Retain the current capital Y.',batch='601_605')
f(31,'small y in X×_yX','parenthesis after(*)','The same small y is printed again. The structural map g is f∘p_1=f∘p_2:X×_YX→Y; retain the existing capital Y.',batch='601_605')
f(32,'η as the final index of f and Y','factorization display','Main and witness614 show η with a descending right stroke, unlike n in Lemma2.6. This does not force an error: for the finite tower supplied by2.6, put η=n and keep each Y_i and f_i. That relabelling gives precisely this displayed terminal arrow and endpoint, with no morphism changed. Reusing the letter previously used for a geometric point is insufficient evidence of a mathematical misprint. Retain η in both layers.','amended','Retain f_η and Y_η in both layers.',batch='601_605');D[-1]['misprint']=False
sid=own(603,'eight structure-sheaf letters, including the Stein paragraph','five plain O and three independently underlined O','eight occurrences of \\mathcal O','Use plain typed O with three local underlines.','font','Both scans show plain O in the three terms of(*) and the two letters in Lemma2.6. In the intervening Stein paragraph, each of O_X, O_X and O_{Y_0} has its own short underline. These are independently observed marks.');patch(603,'both',r'\mathcal O','{O}',sid,'Restore typed O before applying its three local underlines.','font',count=8);patch(603,'both',r'\Spec(f_*({O}_X))',r'\Spec(f_*(\underline{O}_X))',sid,'The O_X inside the Stein spectrum has a short underline.','underline');patch(603,'both',r'f_{0*}({O}_X)\xleftarrow{\sim}{O}_{Y_0}',r'f_{0*}(\underline{O}_X)\xleftarrow{\sim}\underline{O}_{Y_0}',sid,'Both O letters in the Stein isomorphism are independently underlined.','underline')
statement(603,'%%%%%%%%%%  scan idx 616  |  folio 603  %%%%%%%%%%\n',r'\end{enumerate}','Lemma2.4 continuation')
statement(603,r'\(\mathrm{II}^*\).','\n\nEn fait','Assertion II star',exceptions=('1.1',))
statement(603,r'\textbf{Lemme 2.6.}',None,'Lemma2.6 first part')
CHECKED.append(603)

# Page604 read in both main strips.
f(33,'604 begins with the complete O_{Y_i} descent sequence','top604','The displayed sequence starts the page;603 ends tel que la suite. The attached marker is exact.',batch='601_605')
f(34,'Bull. soc. math. France plain','Proposition3.1 attribution','The entire parenthetical attribution is unlined, independently of the underlined statement word groups that follow. The applied removal of journal emphasis matches.',batch='601_605')
f(35,'Sinons with terminal s','proof2.6','The extra s is clear. Retain diplomatic Sinons and current Sinon.',batch='601_605')
sid=own(604,'proof2.6, ring-letter cluster','tensor base A_i; B-modules; Spec(A_i); B⊂A_i; B=A_i','same printed letters retained in current','Use tensor base B_i; A-modules; Spec(B_i); A⊂B_i; A=B_i.','mathematical_source_correction','The paragraph defines A=O_Y and B_0=f_*O_X, with A injected into B_0, then B_i=Eq(B_{i−1}⇉B_{i−1}⊗_A B_{i−1}). For every b∈B_i, b⊗1=1⊗b. Thus the quotient map B_{i−1}⊗_A B_{i−1}→B_{i−1}⊗_{B_i}B_{i−1} has inverse x⊗_{B_i}y↦x⊗_Ay: the equalizer relation multiplied by x⊗y makes this rule B_i-balanced, so the tensor universal property defines it and both composites fix pure tensors. The original f is finite and Y is noetherian; hence B_0 is a finite A-module and each A-submodule B_i is finite. Thus B_i/A is a finite A-module and A→B_i is a finite ring map. After the printed localization and stabilization B_i=B_{i+1}, multiplication B_i⊗_A B_i→B_i is inverse to b↦b⊗1, since every b lies in the equalizer. Hence Spec(B_i)→Spec(A)=Y is the finite monomorphism used in the proof. The printed Nakayama step makes A→B_i surjective; its original injectivity forces A=B_i and contradicts the nonempty stabilized support. This exact algebra calculation fixes all five corrupt expressions and also supplies the effective epimorphisms in the tower. The undefined A_i and B cannot supply these maps. Preserve the entire printed cluster diplomatically; this is a substantive source correction, also deciding rejected Codex SGA-SRC-001365.')
for old,new in [(r'\otimes_{A_i}',r'\otimes_{B_i}'),(r'de \(B\)-modules',r'de \(A\)-modules'),(r'\Spec(A_i)',r'\Spec(B_i)'),(r'\(B\subset A_i\)',r'\(A\subset B_i\)'),(r'\(B=A_i\)',r'\(A=B_i\)')]:patch(604,'current',old,new,sid,'Restore the named rings using the equalizer and finite-monomorphism calculation recorded in the finding.','misprint')
sid=own(604,'all ten structure-sheaf letters','plain typed O throughout','ten occurrences of \\mathcal O','Use plain O with existing indices.','font','The five O letters in the opening sequence, the two in the A/B_0 definitions, the local-ring O and both O_S letters in Proposition3.1 are all unlined typed O.');patch(604,'both',r'\mathcal O','{O}',sid,'Restore the ten locally observed plain letters with safe control-word delimiters.','font',count=10)
statement(604,'%%%%%%%%%%  scan idx 617  |  folio 604  %%%%%%%%%%\n','\n\nPosons','Lemma2.6 conclusion')
statement(604,r'\textbf{Proposition 3.1.} (Oort, Bull. soc. math. France, t. 90-1962).',None,'Proposition3.1 hypotheses',exceptions=('(EGA III 7.8.1).','EGA III 7.4.6'))
CHECKED.append(604)

# Page605 read in both main strips; witness616 resolves the diagram glyphs.
f(8,'statement prose underlined; mathematical notation independently marked','statements601–605','The full pages601–605 have now been compared. Explicit word-group patches cover Proposition2.3, Lemma2.4, assertionII*, Lemma2.6 and Proposition3.1. Journal and EGA references and f.p.p.f abbreviations retain their printed plain form. Local Hom, Isom, Pic and O rules are handled independently.','not applied and now applied','Apply the exact statement spans recorded in ASTRA-XII own findings, with per-layer group counts.',batch='601_605')
f(36,'Hom underlined in the opening R² formula','top605','The short rule ends before the O_S subscript. The applied operator underline matches.',batch='601_605')
f(37,'both Pic symbols underlined','Proposition3.1 conclusion','Each Pic has its own rule, separate from the prose underline. The applied forms match.',batch='601_605')
f(38,'both Pic symbols underlined in the four-term sequence','first Pic display605','Both displayed Pic operators are underlined. The three later occurrences are visibly plain; preserve the observed distinction.',batch='601_605')
f(39,'plain typed V in sous le groupe V(Ě)','Proposition3.1 conclusion','This V lacks the doubled stroke of the two display V symbols. The applied plain letter matches.',batch='601_605')
f(40,'both vertical O*→O arrows hooked at their feet','first proof diagram605','Main and witness616 show the two hooks. The left vertical arrow of the second diagram is plain. The applied arrows match each local form.',batch='601_605')
f(41,'no comma after the lower-row zero','first proof diagram605','Both scans continue directly to the separate parenthetical α(i)=1+i. No comma is printed after the zero.',batch='601_605')
f(42,'On fera attention begins an indented paragraph','after the second diagram605','The paragraph is visibly separated from the diagram. The applied break matches.',batch='601_605')
f(43,'R prime before (f_T)_*(O*_{X′_T})','second proof diagram605','Witness616 shows a short prime, not the stem and head of1 used in the neighbouring R^1. The map comes after R^1(f_T)_*O*_{X_T} and before the connecting map to R²(f_T)_*I_T in the cohomology sequence of 1→I_T→O*_{X_T}→O*_{X′_T}→1. Its degree is therefore1; retain the current R^1.',batch='601_605')
sid=own(605,'all thirteen structure-sheaf letters','plain typed O throughout','thirteen occurrences of \\mathcal O','Use plain O with existing indices and unit stars.','font','The five letters in the statement and the eight letters in the two proof diagrams are unlined typed O, including the Hom subscript. Main and witness616 agree on the diagram forms.');patch(605,'both',r'\mathcal O','{O}',sid,'Restore all thirteen locally observed plain structure-sheaf letters.','font',count=13)
sid=own(605,'between the two proof diagrams','no intervening word','et between the display environments','Delete the added et.','extra','The main lower strip and witness616 both show uninterrupted blank space between the first diagram and the upper row of the second. No et appears at the left margin or between the diagram blocks.');patch(605,'both','\\]\net\n\\[\n\\begin{tikzcd}[column sep=tiny]','\\]\n\\[\n\\begin{tikzcd}[column sep=tiny]',sid,'Delete text absent from both scans.')
sid=own(605,'warning after the second diagram',"n'est pas nécessairement commutatif underlined",r"\emph{n'est pas nécessairement commutatif}",r"\uline{n'est pas nécessairement commutatif}",'underline','Both scans draw a rule under the entire warning phrase. The source preamble uses normalem, so emph would produce italics rather than the observed rule.');patch(605,'both',r"\emph{n'est pas nécessairement commutatif}",r"\uline{n'est pas nécessairement commutatif}",sid,'Preserve the directly observed underline as an explicit prose rule.','underline')
statement(605,'%%%%%%%%%%  scan idx 618  |  folio 605  %%%%%%%%%%\n','\n\nConsidérons','Proposition3.1 continuation and conclusion',exceptions=('f.p.p.f.,','f.p.p.f.'))
CHECKED.append(605)

# Page606 read in both main strips and witness617.
f(1,'En effet indented after the page break','first line606','The proof begins a new paragraph after the displayed3.2. The attached blank line matches.',batch='606_610')
f(2,'D’après i) begins an indented paragraph','middle606','Both scans show a new paragraph after the nilradical membership formula. The applied break matches.',batch='606_610')
f(3,'t_α in the Finalement sum','Finalement paragraph606','The index has the alpha form, unlike β in the adjacent g and all summands of the same decomposition. Each g_β is paired with its coefficient t_β, so retain current t_β.',batch='606_610')
f(4,'v(h), with no index','Finalement paragraph606','Both scans show no β after h. This is the repeated coefficientwise lift g_β=v(h_β)+n_β established above; retain the current index.',batch='606_610')
f(5,'nilrad Γ(X,O_X), X unprimed','Finalement paragraph606','The prime is absent in both scans. Here n_β=g_β−v(h_β) is an element of Γ(X,O_{X′}), the codomain of v; retain the current prime.',batch='606_610')
f(6,'small t in f_t','first exact sequence606','Witness617 confirms the small index, distinct from the capital T in the next term. The sequence is obtained by applying f_T to the sheaves on X_T; retain the current capital T.',batch='606_610')
f(7,'no units star on O_{X′_T}','first exact sequence606','The blank space after O is clear in witness617. The preceding units sequence on605 gives the degree-one map from O*_{X_T} to O*_{X′_T} and its connecting map to R²I_T; retain the current units star.',batch='606_610')
f(8,'no commas around par passage ... associés','between the two sequences606','The sentence runs without either comma in both scans. The applied punctuation matches.',batch='606_610')
f(9,'both Pic symbols underlined','second exact sequence606','Each Pic has a separate short rule. The applied forms match.',batch='606_610')
f(10,'first Pic underlined; last Pic plain','last paragraph606','The P↪Pic immediately after le monomorphisme has an underline; the repeated P↪Pic in the final line has none in either scan. Preserve this local distinction.',batch='606_610')
f(11,'Si P=Ker(u) begins an indented paragraph','last paragraph606','Both scans separate this proof paragraph from the preceding sequence. The applied break matches.',batch='606_610')
sid=own(606,'definition of h after D’après i)','h=Σ v(h_β)⊗t_β ∈ Γ(X_T,O_{X_T})','same in both layers',r'h=\sum h_\beta\otimes t_\beta\in\Gamma(X_T,\mathcal O_{X_T})','mathematical_source_correction','Main and witness617 both print v(h_β) inside the defining sum. The already defined v maps Γ(X,O_X) to Γ(X,O_{X′}), so this expression lies on X′_T, while the following calculation requires a lift acting O_{X_T}-linearly on the additive exact sequence. Put h=Σh_β⊗t_β. Then v_T(h)=g−n, where n=Σn_β⊗t_β is nilpotent and nI_T=0 by(i). Since g is a unit, g−n is a unit. The nilpotent closed immersion X′_T⊂X_T then makes h a unit in every stalk of O_{X_T}, and the local inverses glue to a global inverse. Multiplication by h on 0→I_T→O_{X_T}→O_{X′_T}→0 induces the identity δ_T(h⁻¹g)=h⁻¹δ_T(g). On I_T the actions of h and g agree because nI_T=0. Thus the corrected definition proves exactly the next printed equality and inclusion; no extra assumption or changed theorem is introduced.');patch(606,'current',r'h=\sum v(h_\beta)\otimes t_\beta',r'h=\sum h_\beta\otimes t_\beta',sid,'Use the actual lift to O_{X_T} needed for the displayed linearity calculation.','misprint')
sid=own(606,'nineteen structure-sheaf letters','seventeen plain O; two underlined O','nineteen occurrences of \\mathcal O','Use typed O and the two observed local rules.','font','Both scans show unlined typed O throughout except O_{X′_T} in the action sentence en tenant compte and O_{X_T} in the membership of h. Each of those two has a distinct short underline beneath O alone.');patch(606,'both',r'\mathcal O','{O}',sid,'Restore typed O throughout before its two local underlines.','font',count=19);patch(606,'both',r"l'opération de \(\Gamma(X_T,{O}_{X'_T})\)",r"l'opération de \(\Gamma(X_T,\underline{O}_{X'_T})\)",sid,'The action-ring O has a short rule.','underline');patch(606,'both',r'\otimes t_\beta\in\Gamma(X_T,{O}_{X_T})',r'\otimes t_\beta\in\Gamma(X_T,\underline{O}_{X_T})',sid,'The O in the membership formula for h has a short rule.','underline')
CHECKED.append(606)

# Page607 read in both main strips.
f(12,'Pic underlined in the torsor sequence','first paragraph607','The rule is visible beneath Pic and ends before X/S. The applied form matches.',batch='606_610')
f(13,'Commutative group schemes in straight double quotes, unlined','Oort reference607','The title has quotation marks and no underline. The applied guillemets follow the accepted volume quotation convention.',batch='606_610')
f(14,'first two Pic underlined; next two plain','Corollary3.3(i)','Only the pair with X′/S has short rules; the X/S pair is plain. Preserve the inspected local forms.',batch='606_610')
f(15,'target Pic underlined; source Pic(X′_T) plain','Corollary3.3(ii), first map','The short rule lies only under the target Pic name. The applied forms match.',batch='606_610')
f(16,'target Pic underlined; source Pic(X_T) plain','Corollary3.3(ii), second map','The second map repeats the same local distinction. The applied forms match.',batch='606_610')
f(17,'En effet(i) begins an indented paragraph','proof3.3','The proof is visibly separated from the two-item statement. The applied break matches.',batch='606_610')
f(18,'both upper Pic underlined','first diagram607','Both top-row Pic operators have short rules. The applied forms match.',batch='606_610')
f(19,'both lower Pic underlined','first diagram607','Both bottom-row Pic operators also have short rules; the preceding V→Pic link is a plain line as transcribed. The applied forms match.',batch='606_610')
f(20,'no punctuation after the last H⁰ term','second diagram607','The last parenthesis is followed by blank space. Unlike the first diagram, no comma is printed. The applied omission matches.',batch='606_610')
sid=own(607,'four structure-sheaf letters in the second diagram','plain O in each units sheaf','four occurrences of \\mathcal O','Use plain O with existing indices and stars.','font','All four O letters in the cohomology diagram are unlined typed letters.');patch(607,'both',r'\mathcal O','{O}',sid,'Restore the four locally observed plain structure-sheaf letters.','font',count=4)
statement(607,r'\textbf{Corollaire 3.3.}','\n\nEn effet (i)','Corollary3.3 statement',exceptions=('3.1',))
own(607,'last term in the second diagram','H⁰(T,R²f_*I_T)','same in both layers','Retain the printed abbreviation f in this final term.','notation','The omitted base-change subscript is recoverable from the displayed diagram. Its vertical edge is H²(X_T,I_T)→H⁰(T,R²(f_T)_*I_T), with f_T the projection X×_S T→T, and each preceding column explicitly uses that same map. The source denotes this base-changed structural morphism by f in its final term; retaining the local abbreviation does not change the edge map. No distinct morphism or changed cohomology claim is asserted.','retained author shorthand')
CHECKED.append(607)

# Pages608–609 read in both main strips; witnesses619–620 verify the linked reversals.
f(21,'first Pic underlined; remaining three Pic plain','Corollary3.4 and Proposition3.5','The Pic of X_red/k alone has a short rule. The later Pic_{X/k} and both Pic symbols in f* are unlined. Preserve the applied local forms.',batch='606_610')
f(22,'three baseline dots in the ideal filtration','proof3.5','The dots lie at the baseline, not at the vertical midpoint of the inclusion signs. The applied ldots matches.',batch='606_610')
sid=own(608,'proof3.5, successive ideals and immersions','NI_i⊂I_{i−1}; X_i↪X_{i−1}','same in both layers','NI_{i−1}⊂I_i; X_{i−1}↪X_i','mathematical_source_correction','Both main and witness619 print these two directions. The defined filtration is I_0=I⊃I_1⊃…⊃I_n=0 and X_i=V(I_i). The quotient O_Y/I_i→O_Y/I_{i−1} induces the closed immersion X_{i−1}↪X_i, whose ideal is J_i=I_{i−1}/I_i. For 1≤i≤n, NI_{i−1}⊂I_i gives (N/I_i)J_i=0, exactly hypothesis3.1(i) for this immersion. The printed example I_k=N^kI supplies NI_{i−1}=I_i. The printed reverse inequality is automatic and does not establish the needed annihilation. The reverse immersion is actually false for Y=Spec(k[ε]/ε²), I_0=(ε), I_1=0: it would make Spec(k[ε]/ε²) a closed subscheme of Spec k, requiring an impossible surjection k→k[ε]/ε². Correct both expressions together in current, preserving the filtration and all scheme definitions.');patch(608,'current',r'NI_i\subset I_{i-1}',r'NI_{i-1}\subset I_i',sid,'Restore the annihilation of each successive ideal required by3.1(i).','misprint');patch(608,'current',r'X_i\hookrightarrow X_{i-1}',r'X_{i-1}\hookrightarrow X_i',sid,'Use the closed immersion induced by the quotient of the defined ideal sheaves.','misprint')
sid=own(608,'two structure-sheaf letters','plain O_Y; underlined O_{X′}','two occurrences of \\mathcal O','Use plain O_Y and independently underlined O_{X′}.','font','Main and witness619 show no rule under the nilradical’s O_Y; the O_{X′} to which generic flatness is applied has a separate short rule.');patch(608,'both',r'\mathcal O_Y','{O}_Y',sid,'Preserve the plain typed O_Y.','font');patch(608,'both',r"\mathcal O_{X'}",r"\underline{O}_{X'}",sid,'Preserve the local underline under O_{X′}.','underline')
statement(608,r'\textbf{Corollaire 3.4.}','\n\nFinalement','Corollary3.4 statement',exceptions=('p.g.c.d.',))
statement(608,r'\textbf{Proposition 3.5.}','\n\nEn effet','Proposition3.5 statement',exceptions=('SGA 3 XVII',))
own(608,'proof3.5 after the reference to hypothesis3.1(i), continued609','O_{X′}, R^if_*I and the two reduced direct images in3.1 notation','same in both layers','Retain the source notation and reject the proposed extra prose insertion.','notation','The proof explicitly reduces to hypotheses(i)–(v) of3.1. Its notation is matched exactly by (ambient X, closed X′, structural f) in3.1=(Y, X, Y→S) in3.5; for each filtration step the same triple is (X_i,X_{i−1},X_i→S). Thus O_{X′} is the closed-scheme structure sheaf in hypothesis(ii), and R^if_*I and E are precisely the direct images and cokernel in hypotheses(iii),(iv). Page609 uses the same triple when imposing(v), and closes Enfin on applique3.1. This explicit identification supplies the referenced morphisms without adding an unprinted explanatory sentence. It decides rejected Codex SGA-SRC-001315 independently of the genuine filtration-direction errors above.','retained author shorthand')
CHECKED.append(608)
f(23,'both Pic symbols underlined','Remark3.6, first exact sequence','Main and witness620 show separate operator rules. The applied underlines are exact; the source’s reversed scheme indices are addressed by a separate mathematical correction.',batch='606_610')
f(24,'both Pic symbols underlined','Remark3.6, cokernel display','Both operator names have short rules. The underlines match; the source’s reversed pullback direction is separately corrected.',batch='606_610')
f(25,'coker with lowercase c','Remark3.6 display','The source clearly prints a small c. The explicit operatorname form avoids the earlier macro definition with capital C and matches the print.',batch='606_610')
sid=own(609,'Remark3.6, two pullback directions','Pic_{X_{i−1}/S}→Pic_{X_i/S}; coker(Pic⁰_{X_s/s}→Pic⁰_{Y_s/s})','same in both layers','Pic_{X_i/S}→Pic_{X_{i−1}/S}; coker(Pic⁰_{Y_s/s}→Pic⁰_{X_s/s})','mathematical_source_correction','Both directions are unambiguous in main and witness620. With the defined X_i=V(I_i), the quotient O_Y/I_i→O_Y/I_{i−1} gives j_i:X_{i−1}↪X_i; the map on Picard functors sends L to j_i^*L, hence Pic_{X_i/S}→Pic_{X_{i−1}/S}. Proposition3.1 appends its obstruction map to V(Q_i) to that direction. The composite j_n∘…∘j_1 is the original f:X=X_0↪X_n=Y; on the fibre over s its pullback is f_s^*:Pic⁰_{Y_s/s}→Pic⁰_{X_s/s}. These are the maps whose successive obstruction quotients the remark invokes. Restore both pullback directions in current as the continuation of the linked608 correction; preserve both printed formulas diplomatically.');patch(609,'current',r'\underline{\Pic}_{X_{i-1}/S}\longrightarrow\underline{\Pic}_{X_i/S}',r'\underline{\Pic}_{X_i/S}\longrightarrow\underline{\Pic}_{X_{i-1}/S}',sid,'Use pullback along X_{i−1}↪X_i.','misprint');patch(609,'current',r'\underline{\Pic}^0_{X_s/s}\longrightarrow\underline{\Pic}^0_{Y_s/s}',r'\underline{\Pic}^0_{Y_s/s}\longrightarrow\underline{\Pic}^0_{X_s/s}',sid,'Use f_s^*, the pullback of the original immersion.','misprint')
sid=own(609,'all ten structure-sheaf letters','plain typed O throughout','ten occurrences of \\mathcal O','Use plain O with existing indices.','font','The three direct-image letters at the top, three letters in the recalled descent sequence, and four letters in4.1(2) are all unlined typed O.');patch(609,'both',r'\mathcal O','{O}',sid,'Restore the ten locally observed plain letters.','font',count=10)
statement(609,r'\textbf{Proposition 4.1.}',None,'Proposition4.1 first part')
CHECKED.append(609)

# Page610 read in both main strips and witness621; first exponent separately enlarged.
f(26,'610 begins with the item label3)','boundary609/610','609 ends with universellement in item2;610 begins at3) Pour i,j≥0. The attached marker, before the item command, is exact.',batch='606_610')
f(27,'coker with lowercase c','Proposition4.1(4)','Main and witness621 both print a small c. The applied explicit operatorname form matches.',batch='606_610')
sid=own(610,'Proposition4.1(3), first derived-image exponent','R^1f_*O_X, with digit1',r'R^if_*\mathcal O_X','Restore R^1 in diplomatic; retain R^i in current.','misprint_in_print','The enlarged main crop and witness621 show a connected flagged stem and base of digit1, with no separate dot; the adjacent j and the later i exponents have separate dots. The hypothesis quantifies i,j≥0 and the next paragraph explicitly applies the Künneth base-change formula to all R^if_*O_X and R^ig_*O_{X×_YX}. Thus i is the required varying exponent. Both attached layers had silently supplied it. Restore the printed1 only in diplomatic, retaining the correct current i.');patch(610,'diplomatic',r'\(R^if_*\mathcal O_X\) et',r'\(R^1f_*\mathcal O_X\) et',sid,'Restore the source digit1 without losing the justified current i.','misprint')
sid=own(610,'proof4.1, first base-change assertion','la formation ... commutent','same in both layers','la formation ... commute','misprint_in_print','Both scans print commutent. The grammatical subject is the singular la formation; the intervening derived-image names are complements introduced by des. Correct the verb to singular commute in current.');patch(610,'current','commutent aux changements','commute aux changements',sid,'Agree the verb with the printed singular subject la formation.','misprint')
sid=own(610,'all eleven structure-sheaf letters','plain typed O throughout','eleven occurrences of \\mathcal O','Use plain O with existing indices.','font','Both scans show plain unlined O in the two item3 terms, all three descent-sequence terms, the O_Y-module clause, the two later derived-image terms, the two terms of π_1−π_2, and the final universal O_Y.');patch(610,'both',r'\mathcal O','{O}',sid,'Restore all eleven locally observed plain letters.','font',count=11)
statement(610,'%%%%%%%%%%  scan idx 623  |  folio 610  %%%%%%%%%%\n','\n\nEn effet','Proposition4.1 continuation and conclusion')
CHECKED.append(610)

# Page611 read in both main strips; witness622 clarifies the reference and missing parenthesis.
f(2,'sheaf Hom underlined; three Hom in the statement diagram plain','Lemma4.2 and first proof line','Both scans show a short rule only under Hom in N=Hom_{O_Y}(L,M). The three global Hom operators in the diagram are plain. Preserve the applied forms.',batch='611_615')
f(3,'Γ Y,N), opening parenthesis absent','first proof display611','Both scans show a blank gap after Γ and a closing parenthesis after N. The three-term global-section sequence requires Γ(Y,N); retain the existing current restoration.',batch='611_615')
f(4,'catégoire','description of Deff(S)','The letters o and i are transposed in the print. Retain the existing current catégorie.',batch='611_615')
f(5,'l’ensemble Z(S) de S-points','last paragraph611','The source clearly has de. The construction l’ensemble Z(S) de S-points is grammatical: de introduces the type of elements of the named set. The preceding identification sends each β-rigidified line bundle class (M,v), with f*(M,v)≃(L,u), to its point of the fibre Z(S); no mathematical content or quantifier is missing. Adding s to force des is an editorial preference, not a demonstrated source error. Restore de in current.','amended',r'de \(S\)-points',batch='611_615');D[-1]['misprint']=False
patch(611,'current',r'des \(S\)-points',r'de \(S\)-points','fixes/MISPRINTS_6.json#581','Retain the grammatical source wording and its unchanged class-to-point identification.','revert_misprint')
sid=own(611,'EGA reference between the two proof displays','EGA0 with subscript digit1',r'EGA \(0_{\mathrm I}\)',r'EGA \(0_1\)','number','Witness622 shows the flagged stem and base of digit1, matching nearby numeral1 and unlike capital I. Restore this printed reference form in both layers.');patch(611,'both',r'EGA \(0_{\mathrm I}\)',r'EGA \(0_1\)',sid,'Preserve the directly observed subscript digit in the reference.','number')
sid=own(611,'all eight structure-sheaf letters','plain typed O throughout','eight occurrences of \\mathcal O','Use plain O with existing indices.','font','Both scans show unlined typed O in the sheaf-Hom subscript, the four letters of the tensor-product global-section sequence, and the three letters of the recalled descent sequence.');patch(611,'both',r'\mathcal O','{O}',sid,'Restore all eight locally observed plain letters.','font',count=8)
statement(611,r'\textbf{Lemme 4.2.}','\n\nEn effet','Lemma4.2 statement',exceptions=('4.1',))
CHECKED.append(611)

# Page612 read in both main strips; witness623 confirms the opening f*L.
f(6,'Isom underlined in the definition of Rec','first paragraph612','Main and witness623 both show a short operator rule. The arguments are outside it. The applied form matches.',batch='611_615')
f(7,'Isom underlined in the displayed monomorphism','first display612','The rule covers Isom only. The applied form matches.',batch='611_615')
f(8,'Isom underlined after restreindre','second paragraph612','The third operator again has its own rule. The applied form matches.',batch='611_615')
f(9,'ou without grave accent','Lemma4.3(3)','The main lower strip prints ou, unlike the accented où in the first paragraph. This parenthesis specifies which isomorphism is meant, requiring the relative adverb où, not the disjunction ou. Add the grave in current only.','not applied and now applied','(où le dernier',batch='611_615')
patch(612,'current','(ou le dernier','(où le dernier','fixes/MISPRINTS_6.json#582','Restore the relative adverb in the explanatory parenthesis.','misprint')
sid=own(612,'opening description of Rec','données de recollement sur f*L',r'données de recollement sur \(f^*L\)',r'données de recollement sur \(L\)','mathematical_source_correction','Main and witness623 both print f*L. The preceding611 paragraph fixes L as a line bundle on X, while f:X→Y. The next sentence defines Rec(T) as Isom_{X_T×_{Y_T}X_T}(p_1^*L_T,p_2^*L_T), where p_i:X_T×_{Y_T}X_T→X_T. These are precisely the gluing data on L_T. The effective subfunctor assigns the data induced by a line bundle M on Y_T and an isomorphism f_T^*M≃L_T; such an M is the object still being sought. Thus the opening object is L, not an additional pullback f*L. Removing f* makes the sentence agree with its explicit functor definition without assuming effectivity.');patch(612,'current',r'données de recollement sur \(f^*L\)',r'données de recollement sur \(L\)',sid,'Use the line bundle on X named in the explicit Rec definition.','misprint')
statement(612,r'\textbf{Lemme 4.3.}',None,'Lemma4.3 statement and five conditions',exceptions=('4.1',))
CHECKED.append(612)

# Page613 read in both main strips and witness624.
f(10,'restreindre','proof4.3, first paragraph613','Both scans print the infinitive. The participle modifies la donnée de descente, so retain the existing current restreinte.',batch='611_615')
f(11,'R^i, dotted i','Lemma4.4, précisément parenthesis','Witness624 shows the separate dot and stem of i, unlike the digit1 in f^{-1}(V). The two attached layers already read i. The coordinator owns replay19; no duplicate patch is issued.',batch='611_615')
sid=own(613,'Lemma4.4, exactness clause','qui rend exact les foncteurs','same in both layers','qui rend exacts les foncteurs','misprint_in_print','Both scans omit the plural s. The adjective is the attribute of les foncteurs, explicitly plural; add s in current only.');patch(613,'current','qui rend exact les foncteurs','qui rend exacts les foncteurs',sid,'Agree exacts with the plural les foncteurs.','misprint')
sid=own(613,'four structure-sheaf letters','plain O_Y, O_X twice, and O_V','four occurrences of \\mathcal O','Use plain O with the printed subscripts and baseline restriction.','font','All four O letters are unlined typed letters in main and witness624.');patch(613,'both',r'\mathcal O','{O}',sid,'Restore the four locally observed plain structure-sheaf letters.','font',count=4)
sid=own(613,'Lemma4.4 display, word pour','pour underlined independently of the formula',r'\text{pour }',r'\text{\uline{pour} }','underline','Both scans draw a short rule under the word pour inside the displayed functor formula; the neighbouring inequality is unlined.');patch(613,'both',r'\text{pour }',r'\text{\uline{pour} }',sid,'Retain the single prose underline inside the otherwise unlined display.','underline')
statement(613,r'\textbf{Lemme 4.4.}','\n\nEn effet','Lemma4.4 statement',once_exceptions=('plat',))
own(613,'proof4.3, repeated open-set name','V=f^{-1}(V), followed by O_X|V','same in both layers','Retain the local reuse of V for its inverse image.','notation','The first V is an open of Y; its inverse image is the open X×_YV in X under the first projection, and f restricts to f_V:X×_YV→V. Pulling back a trivialization M|V≃O_Y|V gives L|f^{-1}(V)≃O_X|f^{-1}(V), with the induced trivial gluing datum. The source reuses V for this inverse-image open in the displayed equality and the next restriction. This explicit base-change identification recovers the stated restriction without introducing a new letter.','retained author shorthand')
CHECKED.append(613)

# Page614 read in both main strips and witness625.
f(12,'614 begins en procédant par récurrence décroissante','boundary613/614','Both scans place the entire clause pour n>r; on613 and en procédant at the top of614. The attached marker matches.',batch='611_615')
f(13,'R^n in the induction hypothesis','first paragraph614','Both scans show n, without a dot. The preceding replacement by S_{n+1} gives flatness of R^if_*F for every i≥n+1; the next R^n is the degree now being treated. Retain current i in the first occurrence and n in the next.',batch='611_615')
f(14,'Representation of unramified functors plain','Murre citation614','The title has no underline or quotation marks in either scan. The applied removal of emphasis matches.',batch='611_615')
f(15,'O_Y-Modules','Lemma4.6','Both scans print Y. The lemma defines λ:X→S and a morphism of sheaves on X; the source and target therefore carry the O_X-module structures used in its kernel and cokernel proof. Retain the existing current O_X.',batch='611_615')
sid=own(614,'single structure-sheaf letter in Lemma4.6','plain O_Y','one occurrence of \\mathcal O','Use plain O, retaining the diplomatic Y/current X variant.','font','The O is an unlined typed letter in both scans; the following Modules word alone is underlined.');patch(614,'both',r'\mathcal O','{O}',sid,'Preserve the plain letter independently of the corrected subscript.','font')
statement(614,r'\textbf{Lemme 4.5.}','\n\nPour représenter','Lemma4.5 statement')
statement(614,r'\textbf{Lemme 4.6.}','\n\nOn se ramène','Lemma4.6 statement')
f(1,'word-group underlines throughout Lemmas4.2–4.6','statements611–614','All four full pages have now been inspected and explicit prose underline patches supplied for the five lemmas, with per-layer counts. The first plat in4.4 remains plain as printed; pour in its display receives its own rule. Formulas, local operator marks and numerical references remain independently styled.','not applied and now applied','Apply the exact word-group patches and the single displayed pour rule recorded in ASTRA-XII findings.',batch='611_615')
CHECKED.append(614)

# Page615 read completely, including the blank lower portion.
f(16,'615 begins i.e. qui rend Coker u nul','boundary614/615','614 ends un épimorphisme,;615 starts i.e. qui. The attached marker matches the full-page scan.',batch='611_615')
f(17,'diagram-me split across the first line break','first paragraph615','The joined printed word is diagramme. The asserted operation is base change: for a ring map A→B, right exactness gives Coker(u)⊗_A B≃Coker(u⊗_A B). The paragraph then uses that fact to identify the vanishing locus. Retain current changement, while keeping diagramme diplomatically.',batch='611_615')
CHECKED.append(615)

# ADD NEXT EXPLICIT BATCH HERE
# These two amended corrections remain genuine source misprints: the amended
# verdict concerns the chosen current index, not the existence of a misprint.
for q in D:
 if q['source_id'] in ['check/findings/findings_596_600.json#14','check/findings/findings_596_600.json#16']:q['misprint']=True
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
# ADD AUDIT HERE
# Historical records are linked only to the independently completed image
# decisions above. The exact HOLD differences were separately read in full.
B={q['source_id']:q for q in D+OWN}
def ck(batch,n):return f'check/findings/findings_{batch}.json#{n}'
def copy_decision(sid,typ,ref,verdict=None,change=None,extra=''):
 q=B[ref];z={**q,'record_type':typ,'source_id':sid,'related_record':ref}
 if verdict is not None:z['verdict']=verdict
 if change is not None:z['change']=change
 if extra:z['reason']=q['reason']+' '+extra
 D.append(z);B[sid]=z;return z
def direct_decision(sid,typ,page,printed,region,reason,verdict,change):
 z=dict(record_type=typ,page=page,source_id=sid,verdict=verdict,printed_reading=printed,image=f'scan/SGA6_scan_360dpi.pdf#page={page+14}',region=region,reason=reason,change=change,forms='French forms; English where content changes')
 D.append(z);B[sid]=z;return z

fixmap={513:ck('596_600',15),514:ck('596_600',21),515:ck('596_600',29),516:ck('596_600',48),
517:ck('601_605',9),518:ck('601_605',10),519:ck('601_605',27),520:ck('601_605',29),521:ck('601_605',30),522:ck('601_605',31),523:ck('601_605',43),
524:ck('606_610',3),525:ck('606_610',4),526:ck('606_610',5),527:ck('606_610',6),528:ck('606_610',7),
529:ck('611_615',3),530:ck('611_615',4),531:ck('611_615',10),532:ck('611_615',11),533:ck('611_615',13),534:ck('611_615',15),535:ck('611_615',17)}
for n,ref in fixmap.items():
 z=copy_decision(f'fixes/FIXLOG_6_CURRENT.jsonl#{n}','fixlog',ref)
 if n==516:z['reason']+=' The separate extra coproduct index is removed by coordinator replay18; the removal of the prime is retained.'
 if n==532:
  z['verdict']='amended';z['kind']='transcription';z['change']='Retain the already present R^i in both layers; classify the former R^1 as a transcription error.';z['reason']+=' The directly observed source has i. This is not a correction to the printed mathematics, and replay19 is separately owned by the coordinator.'
 if n==535:
  z['verdict']='amended';z['kind']='misprint_in_print';z['change']='Retain current changement; classify it as a source correction, with diplomatic diagramme.';z['reason']+=' The historical transcription classification contradicts the visible split word diagram-me.'
copy_decision('fixes/FIXLOG_6.jsonl#384','fixlog',ck('611_615',17),'reverted','Retain diplomatic diagramme and current changement.','The former diplomatic replacement by changement was unsupported: both the source word and its line-break hyphen are visible. The supplied diplomatic layer has already restored diagramme.')

C=json.loads((R/'fixes/RECONCILE_CODEX_6.json').read_text())['entries']
def codex(n,ref,verdict=None,change=None,extra=''):
 z=copy_decision(f'fixes/RECONCILE_CODEX_6.json#{n}','codex',ref,verdict,change,extra);z['codex_id']=C[n-1]['id'];z['prior_status']=C[n-1]['status'];return z
def codex_direct(n,page,printed,region,reason,verdict,change):
 z=direct_decision(f'fixes/RECONCILE_CODEX_6.json#{n}','codex',page,printed,region,reason,verdict,change);z['codex_id']=C[n-1]['id'];z['prior_status']=C[n-1]['status'];return z

codex(6,ck('601_605',43))
codex(7,ck('606_610',3))
z=codex(8,ck('606_610',4),change='Retain current v(h_β) and nilrad Γ(X,O_{X′}).',extra=B[ck('606_610',5)]['reason'])
z['printed_reading']='v(h)+n_β; nilrad Γ(X,O_X)';z['related_records']=[ck('606_610',4),ck('606_610',5)]
codex(9,ck('606_610',6));codex(10,ck('606_610',7))
codex(11,'ASTRA-XII-0036','confirmed rejection')
codex(12,ck('611_615',3))
codex(13,'fixes/FIXLOG_6_CURRENT.jsonl#532')
codex(14,ck('611_615',13));codex(15,ck('611_615',15));codex(16,ck('611_615',4));codex(17,ck('611_615',10))
codex(18,'fixes/FIXLOG_6_CURRENT.jsonl#535','amended','Retain current changement and diplomatic diagramme; withdraw the claimed diplomatic correction.','The old note claimed a printed changement from an OCR layer. Direct image comparison shows diagram-me and overrides that claim.')
codex(48,ck('596_600',15))
z=codex(49,ck('596_600',14),'not applied and now applied','Use X_{S_2} and sur S_2 in current; retain printed i diplomatically.','The second occurrence was independently read and adjudicated in '+ck('596_600',16)+'. The old rejection is superseded by the explicit restriction S′⊂S_2 and its base-change map.')
z['related_records']=[ck('596_600',14),ck('596_600',16)];z['printed_reading']='X_{S_i} and sur S_i, dotted i in both scans'
codex(50,'ASTRA-XII-0001')
codex(51,ck('596_600',21));codex(52,ck('596_600',29));codex(53,ck('596_600',48));codex(54,ck('601_605',9));codex(55,ck('601_605',10))
codex_direct(56,602,'u:α*L→O_S','rigidification in the proof of Proposition2.3','Both main and witness613 print α. Put Z=Y_1∩Y_2 and let j:Z→Y be the common inclusion. The source defines α:S→Z and β=j∘α:S→Y. Pullback composition gives the canonical isomorphism α*(j*L)≃(j∘α)*L=β*L, explicitly induced by the associativity map on the tensor products defining inverse-image sheaves. Thus the source α*L is read with L restricted to Z; it specifies the same rigidification as β*L under this canonical identification. Retain the printed shorthand in both layers.','confirmed rejection','Retain α*L; do not replace it by β*L.')
codex_direct(57,602,'(f_1)_*L_1⊕(f_2)_*L_2→(f|Y_1∩Y_2)_*L_2','gluing-kernel formula at the end of the proof of Proposition2.3','The full cluster was read in main and witness613. With Z=Y_1∩Y_2 and j=f_1|Z=f_2|Z:Z→Y, the indicated target is j_*(L_2|Z). The map on sections is (s_1,s_2)↦φ(s_1|Z)−s_2|Z. Its kernel consists exactly of pairs of local sections agreeing through φ and therefore is the invertible sheaf glued from L_1 and L_2. The common restriction j supplies the displayed f|Z and the implicit restriction of L_2. This exact sheaf map recovers the printed construction; the old record supplied no further specific correction.','confirmed rejection','Retain the printed common-restriction notation and kernel formula.')
codex(58,ck('601_605',27))
codex_direct(59,603,'F≃I','proof of Lemma2.4(i)','Main and witness614 print the single capital I. For every S-scheme T, the displayed closed scheme F has T-points (u,v) with u:L_T→M_T, v:M_T→L_T, u∘v=id and v∘u=id. The maps (u,v)↦u and u↦(u,u^{-1}) are inverse bijections with Isom(L_T,M_T), and commute with every base change T′→T. Hence they give the natural isomorphism represented by F≃I, with I denoting the isomorphism functor under discussion. Retain this recoverable abbreviation; expansion to Isom(L,M) changes no mathematical content and is unnecessary.','confirmed rejection','Retain F≃I in both layers.')
z=codex(60,ck('601_605',29),change='Retain current f_*O_X and both X×_Y X bases.',extra=B[ck('601_605',30)]['reason']+' '+B[ck('601_605',31)]['reason'])
z['printed_reading']='f_*O_Y; X×_yX twice';z['related_records']=[ck('601_605',29),ck('601_605',30),ck('601_605',31)]
codex(61,'ASTRA-XII-0019')
# Every tagged duplicate has been read; these eight name the same loci above.
for n,refn in [(347,49),(348,50),(349,53),(350,54),(351,56),(352,59),(353,61),(354,11)]:
 codex(n,f'fixes/RECONCILE_CODEX_6.json#{refn}',extra='This tagged-tree record concerns exactly the same independently inspected locus; its historical status is superseded by that image decision.')

H=json.loads((R/'fr/codex/HOLD_VS_CORR.json').read_text())
def hold(n,ref,extra=''):
 z=copy_decision(f'fr/codex/HOLD_VS_CORR.json#{n}','hold_difference',ref,extra=extra)
 z['corr_lines']=H[n-1]['corr_lines'];z['hold_lines']=H[n-1]['hold_lines'];return z
hold(77,'fixes/RECONCILE_CODEX_6.json#49','The HOLD hunk changes both S_1 indices to S_2. The image instead prints i; the accepted S_2 is a current-only mathematical correction. The adjacent muni correction is independently recorded.')
hold(78,'fixes/RECONCILE_CODEX_6.json#50')
hold(79,'fixes/RECONCILE_CODEX_6.json#53','The prime removal is current-only. The unprinted coproduct index still present in both older hunk strings is separately removed by coordinator replay18.')
hold(80,'fixes/RECONCILE_CODEX_6.json#54','The hunk crosses the600/601 boundary; the changed codomain is on601.')
z=hold(81,'fixes/RECONCILE_CODEX_6.json#56',B['fixes/RECONCILE_CODEX_6.json#57']['reason'])
z['printed_reading']='α*L and (f|Y_1∩Y_2)_*L_2';z['change']='Retain both printed shorthands; reject the HOLD substitutions β*L and f_2|Y_1∩Y_2.';z['related_records']=['fixes/RECONCILE_CODEX_6.json#56','fixes/RECONCILE_CODEX_6.json#57']
hold(82,'fixes/RECONCILE_CODEX_6.json#58')
hold(83,'fixes/RECONCILE_CODEX_6.json#59')
z=hold(84,ck('601_605',29),B[ck('601_605',30)]['reason']);z['printed_reading']='f_*O_Y and O_{X×_yX}';z['change']='Retain current f_*O_X and O_{X×_Y X}.';z['related_records']=[ck('601_605',29),ck('601_605',30)]
hold(85,ck('601_605',31))
hold(86,'ASTRA-XII-0019','The hunk has the same five replacements proved here. Its old scan-inconclusive comment is superseded: the main image clearly establishes the printed A_i/B cluster, which is retained diplomatically.')
hold(87,'ASTRA-XII-0036','The HOLD change is the added phrase avec les notations de3.1 and its adjoining punctuation. Reject that prose insertion after the explicit identification of the notation. The filtration and immersion reversals shared by both historical hunk strings are genuine independent source errors, corrected in ASTRA-XII-0032; they are not the subject of this HOLD difference.')

for page in CHECKED:
 STATUS.append(dict(page=page,pdf_page=page+14,checked_against_scan=True,scan='scan/SGA6_scan_360dpi.pdf',regions='two overlapping full-width strips covering all body text, diagrams and footnotes,252dpi',findings=sum(q['page']==page for q in OWN),note='Entire page compared; witness consulted where recorded; statement-underlining convention separately recorded.'))
for name,rows in [('decisions.jsonl',D),('patches.jsonl',P),('own_findings.jsonl',OWN),('page_status.jsonl',STATUS)]:
 (O/name).write_text(''.join(json.dumps(x,ensure_ascii=False)+'\n' for x in rows))
print('decisions',len(D),'patches',len(P),'own',len(OWN),'pages',len(STATUS))
