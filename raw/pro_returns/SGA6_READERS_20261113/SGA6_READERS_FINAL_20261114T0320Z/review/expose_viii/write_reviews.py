"""Direct scan collation of Exposé VIII. Explicitly reviewed findings only."""
from pathlib import Path
import json,re
R=Path(__file__).resolve().parents[2];O=R/'review/expose_viii';F={};D=[];P=[];OWN=[];STATUS=[]
for path in sorted((R/'check/findings').glob('*.json')):
 for i,x in enumerate(json.loads(path.read_text()),1):F[f'{path.name}#{i}']={**x,'source_id':str(path.relative_to(R))+f'#{i}'}
def f(n,printed,region,reason,verdict='confirmed',change=None,batch='466_470',page=None):
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
 sid=f'ASTRA-VIII-{len(OWN)+1:04d}';OWN.append(dict(record_type='own',page=page,source_id=sid,verdict=verdict,where=where,printed_reading=printed,tex=tex,change=change,kind=kind,reason=reason,image=f'scan/SGA6_scan_360dpi.pdf#page={page+14}',region=where,forms='French forms; English where content changes'));return sid
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
 reason='The directly inspected statement underlines its prose word groups; mathematical symbols retain their independently observed local underlines. Punctuation between adjacent prose groups stays outside the rules. Named statement headings follow NOTE_6. '
 if exceptions:reason+='Printed unlined terms retained: '+', '.join(exceptions)+'. '
 if plain_fragments:reason+='Unlined intervening fragments retained: '+', '.join(repr(t) for t in plain_fragments)+'. '
 if once_exceptions:reason+='Only the first occurrence of each of these terms is unlined: '+', '.join(once_exceptions)+'. '
 sid=own(page,where,'Prose word groups underlined, formulas independently styled','Roman statement prose','Insert explicit word-group \\uline commands in both layers.','underline',reason)
 totals={}
 for layer in ('diplomatic','current'):
  text=layer_text(page,layer);assert text.count(start)==1,(page,start)
  a=text.index(start)+len(start);b=text.index(end,a) if end else len(text)
  old=text[a:b]
  protect=r'(\$\$[\s\S]*?\$\$|\$[^$]*?\$|\\\([\s\S]*?\\\)|\\\[[\s\S]*?\\\]|\\begin\{equation\}[\s\S]*?\\end\{equation\}|\\begin\{enumerate\}(?:\[[^\]]*\])?|\\end\{enumerate\}|\\item\b)'
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
    m=re.fullmatch(r'([^A-Za-zÀ-ÿ]*)(.*?[A-Za-zÀ-ÿ0-9])([^A-Za-zÀ-ÿ0-9]*)',core,re.S)
    if m:prefix,core,suffix=m.groups()
    else:prefix=suffix=''
    fragments=re.split(r'([,.;:!?«»“”()])',core)
    for h in range(0,len(fragments),2):
     segment=fragments[h];body=segment.strip()
     if not re.search(r'[A-Za-zÀ-ÿ]',body):continue
     left=segment[:len(segment)-len(segment.lstrip())];right=segment[len(segment.rstrip()):]
     fragments[h]=left+r'\uline{'+body+'}'+right;count+=1
    ss[j]=lead+prefix+''.join(fragments)+suffix+tail
   pieces[k]=''.join(ss)
  new=''.join(pieces);assert new!=old
  patch(page,layer,old,new,sid,reason+f'Exact local count: {count} prose underline groups in this {layer} span.','underline')
  totals[layer]=count
 OWN[-1]['local_counts']=totals
 OWN[-1]['change']='Insert explicit word-group \\uline commands; '+', '.join(f'{k}: {v} groups' for k,v in totals.items())+'.'
CHECKED=[]
WITNESSES={}
PARTIAL={}

def symbols(page,pairs,where,reason):
 # Every replacement and its expected count is selected after direct page inspection.
 sid=own(page,where,'Printed letter forms recorded in exact local replacements','Plain or script letters differing from the scan','Restore the locally observed letter forms in both layers.','font',reason)
 totals={}
 for layer in ('diplomatic','current'):
  old=layer_text(page,layer);new=old;counts={}
  for pattern,replacement,count in pairs:
   n=len(re.findall(pattern,new));assert n==count,(page,layer,pattern,n,count)
   new=re.sub(pattern,lambda m:replacement,new);counts[pattern]=n
  assert old!=new
  # Root's marker repair can place an unprinted macro tail before this page.
  # Whole-page anchors begin at the marker, matching the merger's page scope.
  marker=re.search(r'^%%%%%%%%%%[^\n]*\|  folio '+str(page)+r'  %%%%%%%%%%',old,re.M)
  if marker and marker.start():
   prefix=old[:marker.start()];assert new.startswith(prefix),(page,layer,'pre-marker prefix changed')
   old=old[len(prefix):];new=new[len(prefix):]
  patch(page,layer,old,new,sid,reason+' Exact local counts: '+str(counts)+'.','font')
  totals[layer]=counts
 OWN[-1]['local_counts']=totals
 return sid

def local_symbols(page,start,end,pairs,where,reason):
 sid=own(page,where,'Locally printed sheaf-letter underlines','Plain letters in the attached layer','Restore the exact local rules in both layers.','font',reason);totals={}
 for layer in ('diplomatic','current'):
  text=layer_text(page,layer);assert text.count(start)==1
  a=text.index(start)+len(start);b=text.index(end,a) if end else len(text);old=text[a:b];new=old;counts={}
  for pattern,replacement,count in pairs:
   n=len(re.findall(pattern,new));assert n==count,(page,layer,pattern,n,count)
   new=re.sub(pattern,lambda m:replacement,new);counts[pattern]=n
  patch(page,layer,old,new,sid,reason+' Exact local counts: '+str(counts)+'.','font');totals[layer]=counts
 OWN[-1]['local_counts']=totals
 return sid
def letter(c):return r'(?<![A-Za-zÀ-ÖØ-öø-ÿ\\])'+c+r'(?![A-Za-zÀ-ÖØ-öø-ÿ])'
def marker(page):return re.search(r'^%%%%%%%%%%[^\n]*\|  folio '+str(page)+r'  %%%%%%%%%%\n',layer_text(page,'diplomatic'),re.M).group()


# PAGE_REVIEWS
# Directly inspected main pages466–470; witness480/481 for469/470.
CHECKED += list(range(466,471))
WITNESSES.update({469:[480],470:[481]})
for n,reading,region,reason in [
 (1,'EXPOSE VIII, one rule; LE THEOREME DE RIEMANN-ROCH, two rules','heading','The separate uppercase lines and rules are present. The attached accent restoration on typed capitals and joint-name dash follow NOTE_6; no new change.'),
 (2,'par Pierre BERTHELOT, whole line underlined','author line','The attached capital surname and whole-line rule match the observed line.'),
 (3,'se factorise en :','definition before triangle','The colon is printed and already present.'),
 (4,'Y with no terminal punctuation','definition triangle','No comma follows the centered lower vertex. The attached punctuation is correct; the independent geometry repair is recorded separately.'),
 (5,'A new indented paragraph begins Quitte','after definition','The attached blank paragraph reproduces the observed separation.'),
 (6,'V followed by a comma','Corollary1.3 diagram','The comma is clearly printed and already present.'),
 (8,"Or j′ begins a new indented paragraph",'after square','The observed paragraph break is already present.'),
 (9,"Soit i″ begins a new indented paragraph",'proofii','The observed paragraph break is already present.'),
 (10,'Page467 ends Posons V=Spec(A),;468 begins X=Spec(B)','467/468 boundary','Both adjoining main-image edges agree with the already relocated marker.'),
 (13,'Comma after the diagram','proofiv first triangle','The comma at the right of the lower row is present and already transcribed.'),
 (15,'Montrons maintenant1.2. and La propriété begin distinct paragraphs','proof of1.2','Both paragraph starts are printed; attached separation is correct.'),
 (16,'On en déduit begins a new indented paragraph','after diamond','The observed paragraph break is already present.'),
 (17,'Y with no terminal punctuation','proof1.4 triangle','No comma follows Y; the attached punctuation is correct.'),
 (18,'Par suite, les groupes','Koszul homology sentence','The comma is printed and present in both attached layers.'),
 (19,'Underlined Tor, subscript i and raised O_Y','homology expression','The main image and native witness crop review/expose_viii/images/w470_tor_native.png show the independent Tor rule. The attached Tor rule is correct; the O rule is restored in the separate local-symbol record.'),
 (20,'Underlined k in both k(y)','homology expression and residual-field clause','Both short k rules are clear in the main image and native witness crop; both are already encoded.'),
 (22,"470 ends par un idéal régulier,;471 begins c’est un anneau",'470/471 boundary','The end of main470 and the directly viewed start of main471 agree with the already relocated marker.')]:f(n,reading,region,reason)

# Independently observed diagram placement, preserving objects and composites.
sid=own(466,'Definition1.1 triangle','U and V on upper row, Y centered below','Y below V','Center Y and retain the two descending edges.','diagram','The image places Y beneath the midpoint of U and V. The displayed morphisms remain i:U→V, V→Y, and their composite U→Y; only the drawn incidence geometry changes.')
patch(466,'both',r'''\begin{tikzcd}[column sep=tiny]
U \arrow[r,"i"] \arrow[dr] & V \arrow[d]\\
& Y
\end{tikzcd}''',r'''\begin{tikzcd}[column sep=large,row sep=large]
U \arrow[rr,"i"] \arrow[dr] && V \arrow[dl]\\
& Y &
\end{tikzcd}''',sid,'Restore the printed centered lower vertex, without changing the three maps.','diagram')
sid=own(466,'Corollary1.3 lower arrow label','i above X→V','i below X→V','Place i above the arrow.','diagram','The main image places i above the horizontal lower edge; the map remains i:X→V.')
patch(466,'both',r'''X \arrow[ur,"j"] \arrow[r,"i"'] & V ,''',r'''X \arrow[ur,"j"] \arrow[r,"i"] & V ,''',sid,'Exact source-side placement of the label.','diagram')
sid=own(467,'proofi square lower arrow label','i above X→V','i below X→V','Place i above the arrow.','diagram','The main image puts i above the lower edge; the base-change square and section maps are unchanged.')
patch(467,'both',r'''X \arrow[r,"i"'] \arrow[ur,"j"]''',r'''X \arrow[r,"i"] \arrow[ur,"j"]''',sid,'Restore the observed label side.','diagram')
sid=own(468,'affine ring triangle','u above the leftward edge; v on the upper-left side of the diagonal','both labels on the opposite sides','Swap the two label sides.','diagram','The maps u:A→B and v:A[T_1,…,T_n]→B remain unchanged. Both printed labels lie on the upper sides of their respective arrows.')
patch(468,'both',r'''\arrow[dl,"v"]''',r'''\arrow[dl,"v"']''',sid,'Source-side label v.','diagram')
patch(468,'both',r'''\arrow[l,"u"]''',r'''\arrow[l,"u"']''',sid,'Source-side label u.','diagram')
sid=own(469,'last diagram vertical label','i″ left of the downward arrow','i″ right of it','Place i″ to the left.','diagram','The map is (i,i′):U→Z×_Y V. The scan places its label on the left of the vertical edge.')
patch(469,'both',r'''\arrow[d,"i''"]''',r'''\arrow[d,"i''"']''',sid,'Restore the printed label side.','diagram')
sid=own(470,'proof1.4 triangle','Y centered below U and V','Y below V','Center Y with two descending edges.','diagram','The three maps remain i:U→V, f:U→Y and g:V→Y with f=g∘i. The source triangle centers the lower vertex and keeps f outside the left edge, g outside the right edge.')
patch(470,'both',r'''U \arrow[r,"i"] \arrow[dr,"f"'] & V \arrow[d,"g"]\\
& Y''',r'''U \arrow[rr,"i"] \arrow[dr,"f"'] && V \arrow[dl,"g"]\\
& Y &''',sid,'Restore the printed triangle geometry and labels.','diagram')

# Local letter rules; ring J in the affine parenthesis is deliberately plain.
local_symbols(468,marker(468),'(du point de vue affine',[(letter('I'),r'\underline{I}',3),(letter('J'),r'\underline{J}',9),(letter('K'),r'\underline{K}',14)],'conormal ideal letters','Every I,J,K in the sheaf expressions has one short rule under the letter. The later affine ideal J is plain and lies outside this exact span. Subscripts, powers, pullbacks and quotient signs remain outside the rules.')
symbols(470,[(r'\\mathcal O',r'\underline{O}',7),(letter('E'),r'\underline{E}',2),(letter('K'),r'\underline{K}',4)],'proof1.4 structure sheaves, module and Koszul complex','Seven O letters, two E letters and four K letters have independent short rules. Native witness review/expose_viii/images/w470_tor_native.png confirms the raised O in the Tor superscript also has its own rule. The four Koszul degree bullets remain lower subscripts; no K-group notation is introduced.')
f(11,'468: I3,J9,K14 underlined; final affine J plain.470:E2,K4 underlined.','local sheaf letters on468 and470','The directly inspected rules are restored with exact local counts; the independently inspected seven O rules are also recorded. No rule is extended to an index, exponent, or a different letter.',change='Apply the local mathematical-letter patches in both layers.')

# Statement word groups and defined term follow the actual local print.
sid=own(466,'Definition1.1 defined phrase','morphisme d’intersection complète belongs to an underlined prose group','separate emph wrapper','Remove the emph wrapper before reproducing the printed continuous group.','underline','Unlike the later definition1.9, this definition does not exclude the defined phrase from its rule. Its source group runs through un morphisme d’intersection complète si pour tout point; the word-group patch supplies that rule.')
patch(466,'both',r"\emph{morphisme d'intersection complète}","morphisme d'intersection complète",sid,'Remove the unsupported italic transport; the exact underlined group is added next.','underline')
statement(466,r'\textbf{Définition 1.1.}',"\n\nQuitte",'Definition1.1 prose',exceptions=('VII 1.4',))
statement(466,r'\textbf{Proposition 1.2.}',"\n\nNous montrerons",'Proposition1.2 prose')
statement(466,r'\textbf{Corollaire 1.3.}',None,'Corollary1.3 opening')
statement(467,marker(467),'\n\ni) Supposons','Corollary1.3 continuation')
statement(470,r'\textbf{Proposition 1.4.}','\n\nSupposons','Proposition1.4 prose',exceptions=('1.1','EGA IV 19.3.6'))
f(7,'Each listed statement has prose word-group rules; formulas and references independently styled','466–470 statements','All four statements and the467 continuation were compared directly. The attached roman prose lacked the observed rules. The defined phrase in1.1 is inside the printed rule, so its prior emph wrapper is removed before adding the exact groups. Named headings follow NOTE_6.',change='Apply explicit statement word-group underline patches in both layers.')

f(12,'au at line end, then dessus without a hyphen','469 opening lines','Both main483 and witness480 visibly omit the compound hyphen. The ordinary compound is printed au-dessus on467; preserving the missing mark diplomatically and restoring it currently distinguishes this source omission from a retained line-end word division. Both attached layers already have the appropriate readings.',change='Diplomatic au dessus; current au-dessus (already present).')
f(14,'q∘i est régulière','469 proofiv','Main483 and witness480 both print i. Here j:X→W′, q:W′→W[T_1,…,T_n], p:W′→W, p₀:W[T_1,…,T_n]→W, and i=p∘j with p=p₀∘q. The preceding sentence establishes that q∘j is an immersion. Applying caseii to the étale q and regular j makes q∘j regular; caseiii applied to p₀ and q∘j then makes i=p₀∘q∘j regular. This supplies exactly the intermediate morphism used by the proof and fixes only its final argument letter.',change='Current q∘j; diplomatic retains q∘i.')
patch(469,'current',r'on en déduit que $q\circ i$ est régulière',r'on en déduit que $q\circ j$ est régulière','check/findings/findings_466_470.json#14','The explicitly displayed compositions and casesii–iii prove the corrected intermediate map.','misprint_in_print')
f(21,'anneau local de U_y en y','470 last sentence','Main484 and witness481 both print y. The preceding regular immersion i_y:U_y→V_y is regular at x, and its local homomorphism is the quotient O_{V_y,x}→O_{U_y,x}=O_{V_y,x}/I_x. This is the regular quotient invoked here;471 explicitly concludes that f is a complete intersection at x. The current x correction is already present.',change='Current en x (already present); diplomatic en y.')

own(467,'proofii, finite-presentation and quasi-compactness sentence','U′→V is asserted to be of finite presentation and quasi-compact','same printed sentence','Retain the author body; record the local descent justification and the limitation of the unrestricted wording.','mathematical_scope','The proof is explicitly local on the target. The chosen U′ can be replaced near a chosen lift by an affine W mapping to an affine neighborhood V₀ in V. The map W→V₀ is étale and affine, hence flat of finite presentation; its open image V₁ gives a faithfully flat quasi-compact map W→V₁. Pullback of i to W is the restriction of i″ and is regular, so the VII1.5 descent used in the text applies locally. An arbitrary U′ in the printed sentence need not be quasi-compact: take V=Spec k[t], X=V(t), V′=the disjoint union of copies V_n for n≥0, p the identity on each copy, and j:X→V₀ the origin. Then X′ is the union of the origins, j′(X) is its zeroth component, and U′=V₀ disjoint union of D(t) in every V_n for n≥1 has U′∩X′=j′(X). The map U′→V is étale and surjective, but the preimage of affine V is the non-quasi-compact infinite union U′. This diagnoses the unreduced wording while the specified affine restriction supplies the actual descent; no new hypothesis or explanatory sentence is inserted into the author body.','retained reading; scope recorded')
own(469,'proof1.2, immersion fermée i″','immersion fermée i″:U→Z×_Y V','same wording','Retain the printed closed-immersion description with its explicit local construction.','mathematical_scope','The paragraph begins by allowing localization on Z near i(x). Choose an affine neighborhood Y₀ of f(x), an affine neighborhood Z₀ of i(x) in Z×_Y Y₀, and then restrict U and choose affine V over Y₀ so that the regular immersion i′:U→V is closed (the local replacement allowed immediately after1.1). Now Z₀→Y₀ is separated. The graph U→Z₀×_{Y₀}U of i is closed, as the pullback of the closed diagonal of Z₀/Y₀; composing it with the closed immersion Z₀×_{Y₀}U→Z₀×_{Y₀}V induced by i′ gives exactly (i,i′). Thus the claimed closed map is available in the explicitly local proof, and no body emendation is warranted.','retained reading; local construction recorded')
own(470,'vanishing of Koszul homology','Comme f est un morphisme plat, ils sont nuls','same wording','Retain the printed sentence with its positive-degree scope recorded.','mathematical_scope','For the displayed resolution K_•(u), base change yields H_i(K_•(u)_y)=Tor_i^{O_Y}(O_U,k(y)). Flatness of O_U over Y makes these zero for i>0; H_0 is O_{U_y}, via the quotient map K_0(u)_y→O_{U_y}. The regularity criterion used for u_y is this vanishing of positive Koszul homology. The degree-zero quotient is already the sheaf used in the following local-ring argument. The prose uses the standard positive-degree vanishing in that criterion; no universal vanishing statement or additional body formula is inserted.','retained reading; degree scope recorded')

# Main471–475 fully compared; supplementary witness regions on472,474,475.
CHECKED += list(range(471,476))
WITNESSES.update({472:[483],474:[485],475:[486]})
for n,reading,region,reason in [
 (1,"471 opens c’est un anneau",'470/471 boundary','Both main-page edges confirm the marker already in place. This is the same boundary as466_470#22.'),
 (2,'carré commutatif :','last line471','The colon at the end of the page is printed and present.'),
 (4,'472 begins with the square','471/472 boundary','The final prose line of471 precedes the entire square on472; the marker is already outside the tikzcd options.'),
 (5,'j above the lower arrow','472 square','The observed upper-side label is already encoded; j:V→Z[T′] is unchanged.'),
 (6,'f′:X×_Y Y′→Y′ in the running line','Proposition1.6','Main and witness show an inline formula, as already restored.'),
 (7,'Pour la réciproque on conclut','proof1.6','There is no comma after réciproque; both attached layers preserve the absence.'),
 (11,'473 begins with the triangle, including its comma','472/473 boundary','The entire triangle follows the new folio. Its source comma is preserved. The separate centering patch changes only geometry.'),
 (12,'No punctuation after V','473 final diagram','The observed absence of a comma is already encoded.'),
 (13,'i above X→V','473 final diagram','The observed label side is already encoded.'),
 (15,'No punctuation after Y','474 first triangle','Both main and witness show no comma; both layers match.'),
 (17,'Soit X′ begins an indented paragraph','after1.8.1','The blank line already matches the paragraph break.'),
 (18,'En comparant begins an indented paragraph','after1.8.2','The blank line already matches the paragraph break.'),
 (20,'No terminal stop after (g)','Proposition1.10 display','Main and witness agree; both attached layers already omit the stop.'),
 (21,'Cela résulte starts an indented paragraph','475 first line','The blank line after the marker already preserves this paragraph.')]:f(n,reading,region,reason,batch='471_475')
f(8,'schéma lisse sur W','472 end of proof1.5','Main486 and witness483 print W. The actual upper-right scheme is Z[T′_1,…,T′_m,T_1,…,T_n], whose structural smooth projection π is to Z. The two displayed squares give π∘j′∘i=g∘f|_U: first the base-change square identifies projection to Z[T′] after j′ with j after projection to V, and the preceding factorization identifies those remaining composites with f and g. Thus the constructed regular immersion j′∘i factors g∘f through a smooth Z-scheme, which is exactly the claimed conclusion1.5. This fixes the base letter without changing the morphism or proof.',change='Current sur Z; diplomatic sur W.',batch='471_475')
patch(472,'current',"dans un schéma lisse sur $W$, d'où le résultat.","dans un schéma lisse sur $Z$, d'où le résultat.",'check/findings/findings_471_475.json#8','The structural projection and the two commutative diagrams explicitly factor g∘f over Z.','misprint_in_print')
f(9,'un morphisme g:Y′→Y un changement','Proposition1.6 opening','Both scans omit a conjunction or separator between the two declarations. The inherited current et joins the declaration of f to that of g; the following base-change construction uses exactly the same two maps. It adds no mathematical hypothesis. Both attached layer readings are appropriate.',change='Retain diplomatic omission and the already present current et.',batch='471_475')
f(10,'au cas ou','proof1.6','The main page has no grave accent. The context is the locative relative au cas où, and the current accent restoration is already present.',change='Diplomatic ou; current où (already present).',batch='471_475')
f(16,'p drawn V→V′','474 first triangle','Both main488 and witness485 show the arrow pointing right from V to V′. The immediately preceding diagram binds p:V′→V and i=p∘j. Its differential sequence is 0→p*Ω¹_{V/Y}→Ω¹_{V′/Y}→Ω¹_{V′/V}→0, locally split because the last term is locally free for the smooth p; at a point of V′ its rank equality is exactly1.8.1. The corrected triangle V′→V→Y supplies this same p and sequence. The existing current interchange of V and V′ is retained; the printed triangle is retained diplomatically.',change='Retain the already present current V′→V; preserve diplomatic V→V′.',batch='471_475')
f(19,'sà dimension','paragraph after Definition1.9','Main and witness show the grave above a. The possessive is sa, as also printed in the immediately preceding smooth case. The inherited current sa is retained.',change='Diplomatic sà; current sa (already present).',batch='471_475')
f(22,'complexe de chaines','475 lower paragraph','Main and witness show no circumflex. Restore the source-period French spelling chaînes in the current layer; preserve chaines diplomatically.',change='Current chaînes; diplomatic chaines.',batch='471_475')
patch(475,'current','complexe de chaines','complexe de chaînes','check/findings/findings_471_475.json#22','Restore the omitted circumflex in the current French text.','misprint_in_print')
f(23,'l’homomorphisme (1.5.1)','475 final line','Both main489 and witness486 print1.5.1. The displayed map immediately above is tagged2.1.1 and is d:J/J²→i*Ω¹_{V/Y}. The definitions L₁=J/J² and L₀=i*Ω¹_{V/Y} identify its domain and codomain exactly with the stated differential L₁→L₀. Hence2.1.1 is the specific required reference, already restored currently.',change='Current (2.1.1) already present; diplomatic (1.5.1).',batch='471_475')

# Exact mathematical symbol rules and source punctuation.
symbols(473,[(letter('J'),r'\underline{J}',3),(r'\\mathcal O',r'\underline{O}',1),(r'\\Omega',r'\underline{\Omega}',1)],'Proposition1.8 ideal and differential letters','All three J letters, the single O, and the single Ω have a short independent rule. Indices, degree1 and quotient exponents stay outside those rules.')
symbols(474,[(r'\\Omega',r'\underline{\Omega}',10),(letter('N'),r'\underline{N}',2)],'differential and conormal ranks','All ten Ω letters and both N letters have independent short rules. The order of the author’s conormal subscripts V′/X and V/X is retained exactly; the proof compares these conormal ranks through the composite j=i′∘j′ and the base-change identification for i′.')
symbols(475,[(letter('J'),r'\underline{J}',7),(r'\\mathcal O',r'\underline{O}',5),(r'\\Omega',r'\underline{\Omega}',5),(letter('L'),r'\underline{L}',6)],'2.1 cotangent-complex definitions','Every occurrence in this page is visibly underlined: J7,O5,Ω5,L6. The complex bullet and numerical chain degrees remain lower subscripts; superscript X/Y and all quotient exponents remain outside the letter rules.')
f(14,'473:J3,Ω1;474:Ω10,N2;475:J7,Ω5,L6 independently underlined','473–475 sheaf and complex letters','Direct comparison confirms every listed rule. The independent structure-sheaf rules O1 on473 and O5 on475 are restored too. All replacement counts are recorded locally, and the author’s indices are preserved.',change='Apply exact local letter-rule patches in both layers.',batch='471_475')
own(474,'ends of1.8.1 and1.8.2','A period after each rank equality','Both terminal periods are present','Retain both printed stops.','punctuation','Main488 and witness485 show a distinct stop after the final parenthesis of each rank equality, unlike the unpunctuated Proposition1.10 display below. Both attached layer stops already match.','confirmed; already present')

# Triangle geometry is independent of the474 mathematical direction repair.
sid=own(473,'the two downward triangles','Y centered below each U,V pair','Y below V','Center the lower vertex in each triangle.','diagram','Both main triangles are symmetric downward configurations. The first ends with a comma and the second does not. Each still displays the same f=g∘i.')
for punct in [',','']:
 old=r'''U \arrow[r,"i"] \arrow[dr,"f"'] & V \arrow[d,"g"]\\
& Y'''+punct+'\n'+r'\end{tikzcd}'
 new=r'''U \arrow[rr,"i"] \arrow[dr,"f"'] && V \arrow[dl,"g"]\\
& Y'''+punct+' &\n'+r'\end{tikzcd}'
 patch(473,'both',old,new,sid,'Restore one centered triangle, preserving its exact terminal punctuation.','diagram')
sid=own(474,'rank-comparison triangle','Y centered under V and V′','Y below right vertex','Center the lower vertex in each branch.','diagram','The geometric placement is independent of the source misprint in the direction of p. The diplomatic branch retains the printed V→V′; the current branch retains the already justified V′→V. Both receive only the printed centered lower vertex.')
for layer,left,right in [('diplomatic','V',"V'"),('current',"V'",'V')]:
 old=left+r''' \arrow[r,"p"] \arrow[dr] & '''+right+r''' \arrow[d]\\
& Y'''
 new=left+r''' \arrow[rr,"p"] \arrow[dr] && '''+right+r''' \arrow[dl]\\
& Y &'''
 patch(474,layer,old,new,sid,'Restore centered geometry without conflating the two directional readings.','diagram')
sid=own(475,'lissifiable factorization triangle','Y centered below X,V; final comma','Y below V','Center Y and retain the final comma.','diagram','The source has f outside the left sloping arrow, g outside the right, and i above X→V. The commutative factorization f=g∘i is unchanged.')
patch(475,'both',r'''X \arrow[r,"i"] \arrow[dr,"f"'] & V \arrow[d,"g"]\\
& Y,''',r'''X \arrow[rr,"i"] \arrow[dr,"f"'] && V \arrow[dl,"g"]\\
& Y, &''',sid,'Restore the source geometry and label positions.','diagram')

statement(471,r'\textbf{Proposition 1.5.}','\n\nSoit $x','Proposition1.5 prose')
statement(472,r'\textbf{Proposition 1.6.}','\n\nOn peut trouver','Proposition1.6 prose')
statement(472,r'\textbf{Proposition 1.7.}','\n\nLa propriété','Proposition1.7 prose')
statement(473,r'\textbf{Proposition 1.8.}','\n\nSupposons','Proposition1.8 prose')
sid=own(474,'Definition1.9 defined term','dimension relative virtuelle is plain and unlined','emph wrapper','Remove the italic wrapper; keep the term outside surrounding rules.','underline','Main and witness leave the defined term plain while underlining L’entier, de la proposition, s’appelle, de, sur, ou de, au point. This local exclusion differs from the printed continuous rule in Definition1.1 and is applied occurrence by occurrence.')
patch(474,'both',r'\emph{dimension relative virtuelle}','dimension relative virtuelle',sid,'Preserve the explicitly unlined defined phrase.','underline')
statement(474,r'\textbf{Définition 1.9.}','\n\nLa dimension','Definition1.9 prose',exceptions=('1.8','dimension relative virtuelle'))
statement(474,r'\textbf{Proposition 1.10.}',None,'Proposition1.10 prose')
f(3,'Prose word groups underlined in1.5–1.10; dimension relative virtuelle plain in1.9','471–474 statement typography','Every named statement was directly compared; six explicit spans reproduce the rules. Formula letters retain their independent styles. The number1.8 and the defined term of1.9 are excluded from prose rules, as visibly printed. The prior emph wrapper on that term is removed.',change='Apply explicit local statement rules and the1.9 term exclusion in both layers.',batch='471_475')

sid_module470=own(470,'proof1.4 module noun','O_V-Module','same capital M','Retain Module in both layers.','retained_typography','The main and witness visibly print capital Module after the structure-sheaf symbol. The page describes a sheaf of modules and consistently uses this author typography; changing the capital would replace an accurately transcribed source form. The only local changes concern independently observed symbol rules.','retained reading; rejected normalization')
own(471,'converse proof1.4, U′ plat sur Y','U′ plat sur Y','same true printed observation','Retain U′ and record the local ring maps supplying the proof.','mathematical_scope','U′ is the open affine neighborhood in Y chosen earlier, so U′→Y is an open immersion; its stalk maps are localizations, hence flat. Independently, the proposition already assumes f:X→Y flat, so O_{Y,y}→O_{U,x} is flat, while smoothness gives flat O_{Y,y}→O_{V,x}. The closed immersion gives O_{V,x}→O_{U,x}, and its fibre map is the quotient O_{V,x}⊗_{O_{Y,y}}k(y)→O_{U,x}⊗_{O_{Y,y}}k(y). These are precisely the maps involved in the transverse regularity argument. The printed claim about U′ is true and the needed flatness of U is already a stated hypothesis; no replacement of the prime or completion of the prose is justified.','retained reading; exact maps recorded')

CHECKED += list(range(476,481))
WITNESSES.update({476:[487],477:[488],478:[489]})
for n,reading,region,reason in [
 (3,'Par fonctorialité starts an indented paragraph','476 proof2.2','The blank line is already present and matches the source.'),
 (4,'Comme V et V′ starts an indented paragraph','476 after2.2.1','The observed break is present; the following Comme les Modules remains attached to its preceding display, as printed.'),
 (5,'i above X→V','476 comparison triangle','The main source label lies inside the triangle, above the lower arrow, as encoded.'),
 (7,'Par ailleurs starts an indented paragraph','477 first line','The blank line following the marker preserves the observed paragraph.'),
 (8,'i above X→V','477 square','The main and witness labels agree with the attached placement.'),
 (9,'j′ right of the curved upward section arrow','477 square','Both scans show the curve bulging to the right of p′ and its label on the outer right side. The attached swap option reproduces that placement.'),
 (10,'a) begins an indented paragraph after Nous allons montrer :','477 proof list','The paragraph break is already present.'),
 (11,'b) begins a separate indented paragraph','477 proof list','The paragraph break is already present.'),
 (14,'478 begins with the full affine ring diagram','477/478 boundary','Main477 ends On a le diagramme : with blank space below. Main478 starts with the whole diagram, as the relocated marker now records.'),
 (15,'L’homomorphisme begins an indented paragraph','478 after diagram','The existing blank line matches the source.'),
 (18,'(resp. T_f=cl(L_•)) is a separate centered display','479 second class display','The parenthesis and resp. belong inside the displayed line. The restored attached display matches the image; resp. on this displayed line is plain.'),
 (19,'Derived-functor L has two rules','480 distinguished triangle','The source-derived functor L has two rules, while each complex L has one. The existing mathbb L transport is retained occurrence-specifically, consistently with the author’s derived-functor notation; the three complex rules are restored separately.'),
 (20,'A full stop after L^{X/Z}_•','480 triangle','The terminal point is distinct in the source and already present.'),
 (21,'Soit V′ starts an indented paragraph','480 after triangle','The existing paragraph break matches the source.'),
 (22,'Alors l’immersion starts an indented paragraph','480 after factorization diagram','The existing paragraph break matches the source.'),
 (23,'Par ailleurs starts an indented paragraph','480 after2.6.1','The existing paragraph break matches the source.')]:f(n,reading,region,reason,batch='476_480')
f(6,'locally free over underlined O_V','476 differential sequence','Main490 and witness487 print the index V without a prime. Here p:V′→V and j:X→V′. The three terms are p*Ω¹_{V/Y}, Ω¹_{V′/Y}, Ω¹_{V′/V}; the pullback used is j*M=O_X⊗_{j⁻¹O_{V′}}j⁻¹M. Their local freeness over O_{V′} makes the sequence locally split and preserves its exactness under this tensor product, giving2.2.2. The existing current O_{V′} supplies the ring of this exact tensor map. There is no implicit replacement by p_*: for V=Y=Spec Z and V′=Spec Z[1/2][t], the sheaf Ω¹_{V′/Y}=O_{V′}dt is free over O_{V′}, while p_*Ω at the stalk(2) is Q[t]dt, which is not free over Z_(2), since multiplication by2 is surjective there and is not surjective on any nonzero free Z_(2)-module. The compatible X=Spec F_3 at t=0 gives the closed immersions required in the proof.',change='Retain current O_{V′} and diplomatic O_V, with each source O rule restored.',batch='476_480')
f(12,'entrainera without circumflex','477 assertionb','The main source spelling lacks the circumflex. The current entraînera restoration is already present and is retained.',change='Diplomatic entrainera; current entraînera (already present).',batch='476_480')
f(13,'Three-row ring diagram with Δ maps, labels(1),(2), and parallel j′/p′ arrows','478 upper diagram','The entire main478 diagram was compared vertex by vertex and arrow by arrow: B⊗_A B→B′⊗_A B′ above B→B′, Δ downward on each; B′⊗_B B′ lies to the right of B′ with Δ pointing left; i:B→C, j:B′→C, i′:B′→B′⊗_B C; the right vertical arrow lands in B′⊗_B C=B′/IB′. The upper parallel arrow j′ points left to C and lower p′ points right. The displayed(1),(2), label sides, and final stop are all present in the already repaired attached diagram.',change='Retain the inspected diagram repair; its true folio is478.',batch='476_480',page=478)
f(16,'First affine Ω has no superscript1, second has1','478 composite differential','The main image shows Ω_{B′/A} and Ω¹_{B′/B} exactly as attached. The unsuperscripted first module is the module representing A-derivations of B′; the same universal derivation b′↦db′ identifies it with the degree-one Kähler module. The second map is induced by A→B and sends db′ to the relative differential d_{B′/B}b′. No extra exponent is needed to describe this displayed map.',change='Retain the already restored absence of1 on the first Ω.',batch='476_480')
f(17,'peut-être défini','478 assertionb explanation','The main source and native witness crop print the hyphen. Here the phrase supplies the finite verb peut followed by the passive infinitive être défini; the current separation already restores that grammatical construction.',change='Diplomatic peut-être; current peut être (already present).',batch='476_480')

sid_regular477=own(477,'proof2.2, three regular immersions','les immersions i′,j,j′ sont régulières','same uncorrected assertion','Current l’immersion j′ est régulière; preserve all three printed immersions diplomatically.','substantive_mathematical_misprint','Main491 and native witness488 both print all three names. The governing assumption in2.1 and2.2 is only that f is lissifiable; complete-intersection hypotheses first appear in2.4. Take Y=Spec k, V=V′=Spec B with B=k[x,y], p=id, I=m² for m=(x,y), C=B/I and X=Spec C. Then i′=j=i is the closed immersion defined by m². At the unique point, I/I²=m²/m⁴ has k-dimension3+4=7 (degree2 and degree3 monomials), while C has length3. Thus I/I² cannot be a finite free C-module, whose length would be a multiple of3; a regular immersion would have a finite free conormal module, so these two immersions are not regular. The section j′ is id_X and is regular of codimension0. In general the actual j′ is a section of the smooth p′ and is regular, precisely the source fact used to identify its conormal with relative differentials on478. The short conormal sequence remains justified without regularity of i′ or j: in the affine notation B→B′, C=B/I and J=ker(B′→C), smoothness supplies a B-algebra lift ℓ:B′→B/I² of B′→C through the square-zero quotient B/I²→C. It sends J into I/I² and J² to0, inducing r:J/J²→I/I². For a∈I, r(p(a) mod J²)=a mod I², so r is a retraction of the natural map α:I/I²→J/J². The usual quotient J/J²→K/K², with K=J/IB′, has kernel the image of α; the retraction proves its injectivity, giving exactly2.2.3. Locally free relative differentials of the smooth p′ and the section identify K/K² with j*Ω¹_{V′/V}; the explicit inverse is described by the augmentation calculation on478. This repairs only the false two-immersion assertion and retains the author’s displayed sequences and proof.','confirmed source error; minimal current correction applied')
patch(477,'current',"et les immersions $i',j,j'$ sont régulières;","et l'immersion $j'$ est régulière;",sid_regular477,'Remove the two disproved regularity assertions; retain the regular section and the exact conormal proof.','misprint_in_print')

symbols(476,[(letter('I'),r'\underline{I}',4),(letter('J'),r'\underline{J}',4),(r'L\^\{X/Y\}',r'\underline{L}^{X/Y}',2),(r'\\Omega',r'\underline{\Omega}',10),(r'\\mathcal O',r'\underline{O}',1)],'2.2 sheaf and complex letters','The main image has independent rules under I4,J4,L2,Ω10,O1. The current O subscript prime is a separate mathematical correction and is not changed by this glyph patch.')
symbols(477,[(letter('I'),r'\underline{I}',7),(letter('J'),r'\underline{J}',3),(letter('K'),r'\underline{K}',5),(r'L\^\{X/Y\}',r'\underline{L}^{X/Y}',2),(r'\\Omega',r'\underline{\Omega}',1)],'2.2 conormal ideals and complexes','Every I,J,K and Ω in these sheaf formulas is independently underlined, as are the two complex L letters. Exact counts I7,J3,K5,L2,Ω1. The concluding affine-scheme names introduce no additional ideal-symbol occurrence.')
symbols(478,[(r'I/I\^2\\to J/J\^2',r'\underline{I}/\underline{I}^2\to\underline{J}/\underline{J}^2',1),(r'K/K\^2\\to j\^\*',r'\underline{K}/\underline{K}^2\to j^*',1),(r'\\Omega(?=\^1_\{V)',r'\underline{\Omega}',3),(r'L\^\{X/Y\}',r'\underline{L}^{X/Y}',2)],'478 sheaf formulas before affine calculations','The initial conormal I/I²→J/J², the initial K/K²→j*Ω, the three Ω with scheme subscripts V, and two cotangent L letters carry rules. The subsequent ring ideals I,J,K,H and their quotients, and all Ω with algebra subscripts B, are visibly plain. The exact patterns exclude all these plain occurrences and the two French initial L letters.')
symbols(479,[(letter('J'),r'\underline{J}',6),(r'\\mathcal O',r'\underline{O}',3),(r'\\Omega',r'\underline{\Omega}',2),(r'L\^\{X/Y\}',r'\underline{L}^{X/Y}',2)],'479 conormal, differential and complex letters','Short rules under J6,O3,Ω2,L2 are individually observed. The three K-group letters remain plain with their raised degree bullets; T_f remains plain. The initial L in L’élément is prose and is excluded by the exact complex pattern.')
symbols(480,[(letter('I'),r'\underline{I}',5),(letter('J'),r'\underline{J}',8),(letter('K'),r'\underline{K}',5),(letter('L'),r'\underline{L}',3),(r'\\Omega',r'\underline{\Omega}',3)],'480 conormal sequences and triangle complexes','The source has I5,J8,K5,three single-rule complex L letters and Ω3. Primes on J′ stay outside the short J rule. The derived-functor Lf has two rules and is excluded from the single-letter L pattern; its mathbb transport remains exactly as separately adjudicated.')
f(2,'Independent sheaf rules with the478 affine exceptions','476–480 mathematical letters','Every listed mathematical occurrence was directly compared. Exact local symbol patches record counts on each page. In particular478 preserves plain ring-level I,J,K,H and Ω while restoring only the initial sheaf formulas and the complex letters; no blind global alphabet replacement is used.',change='Apply occurrence-scoped mathematical-letter rules in both layers.',batch='476_480')

own(478,'first prose paragraph, coîncide','coîncide with a circumflex','coïncide in both attached layers','Retain the accepted ï transport in both layers; no variant.','convention','The main native crop review/expose_viii/images/p478_coincide_native.png and witness native crop review/expose_viii/images/w478_coincide_native.png show the pointed circumflex. NOTE_6 explicitly accepts the transcription’s ï for printed plain i or î in this word and says not to classify that transport as a source error. This records the inspected source form and the applicable convention without introducing a misprint variant.','confirmed convention; source observation only')

statement(476,r'\textbf{Proposition 2.2.}','\n\nSoient $V','Proposition2.2 prose')
statement(478,r'\textbf{Définition 2.3.}','\n\n\\textbf{Proposition 2.4.}','Definition2.3 prose',exceptions=('complexe cotangent relatif',))
statement(478,r'\textbf{Proposition 2.4.}',None,'Proposition2.4 opening',exceptions=('1.1',))
statement(479,marker(479),'\n\nSoit $f','Proposition2.4 continuation',exceptions=('2.1',))
statement(479,r'\textbf{Corollaire 2.5.}',"\n\nL'élément",'Corollary2.5 prose',exceptions=('1.9',))
statement(479,r'\textbf{Proposition 2.6.}',None,'Proposition2.6 opening')
statement(480,'(G)',"\n\nSoit $V'",'ConditionG and Proposition2.6 conclusion')
f(1,'Statements have prose word-group rules; complex cotangent relatif plain in2.3','476–480 statements','All statement spans and both continued page edges were inspected. The explicit rules preserve the unlined defined term of2.3, numerical references, formulas, labels(G) and their independent mathematical-letter rules. The displayed resp. line of2.5 remains plain exactly as printed.',change='Apply seven explicit statement spans in both layers.',batch='476_480')

sid_capitals479=own(479,'proof2.4, Idéal and Module','Idéal and O_X-Module with capitals','same capitals','Retain both source capitals.','retained_typography','The main source visibly uses capital Idéal and Module. The first names the ideal sheaf J and the second the locally free structure-sheaf Module J/J². The natural quotient map J→J/J² and its O_X action are unchanged; a capitalization change would only replace faithfully transcribed author typography.','retained reading; rejected normalization')
sid_respe479=own(479,'proof2.5, cas respé and cas non respé','respé and non respé','same abbreviations','Retain the printed abbreviations and their two explicitly introduced cases.','retained_reading','The parenthetical resp. in2.5 introduces the perfect-complex Grothendieck group. The later cas respé refers to that case and cas non respé to the vector-bundle group. The exact comparison sends a locally free Module E to its degree-zero perfect complex, [E]↦[E[0]]. For the actual two-term representatives, the Euler class is [L₀]−[L₁]; a quasi-isomorphism has bounded acyclic cone of locally free Modules, whose successive short exact sequences show its alternating class is0. Thus the maps in the proof of2.2 give the same Euler class already in the vector-bundle group, while their images are identified in the perfect-complex group by the quasi-isomorphism. This explicitly accounts for the two references without expanding or changing the author’s abbreviation.','retained reading; rejected expansion')

CHECKED += list(range(481,486))
WITNESSES.update({481:[492],482:[493],485:[496]})
for n,reading,region,reason in [
 (1,'f*(j*(Ω¹_{V′/Z}))','481 formula2.6.2','The nested parentheses are visible in main and witness and are already restored.'),
 (2,'Parentheses around Ω in each lower-row pullback','481 commutative diagram','All three lower nodes and their nested pullback parentheses match the source. The independent label-side repair is recorded separately.'),
 (3,'En combinant begins an indented paragraph','481 after2.6.2','The observed blank paragraph is already present.'),
 (4,'De la suite begins an indented paragraph','481 after diagram explanation','The observed blank paragraph is already present.'),
 (7,'482 starts est constante sur X','481/482 boundary','The adjacent main-page edges confirm the marker already moved before est.'),
 (9,'On obtient donc begins an indented paragraph','483 after Proposition3.2','The existing paragraph break matches the image.'),
 (10,'Pour toute begins an indented paragraph','483 after Ch(A) display','The existing paragraph break matches the image.'),
 (11,'Enfin, nous avons begins an indented paragraph','483 after completed Chern class','The existing paragraph break matches the image.'),
 (12,'Nous allons appliquer starts an indented paragraph','484 first line','The blank line after the marker matches the source.'),
 (14,'x followed by a wavy arrow to checked x','484 end of3.4','The main source visibly has a wavy arrow, already represented by rightsquigarrow.'),
 (15,'La relation begins an indented paragraph','484 after Proposition3.5','The existing paragraph break matches the image.'),
 (16,'485 begins Gr K^• (VI5.5), on','484/485 boundary','The final main484 line ends sur les, and485 begins with the graded group. The marker and the preceding Par additivité paragraph are already correct.'),
 (17,'c¹(x⁻¹)=−c¹(x) inline','485 proof3.5','The formula lies within the running sentence, as already restored.'),
 (19,'mod. Fil²K^•(X), with no parentheses','485 congruence','Main and witness show the plain abbreviation with its stop and final semicolon. The attached form matches.'),
 (20,'Théorème3.6. (Riemann-Roch).','485 heading','Both source stops are present in the attached label; bold label typesetting and the joint-name dash follow NOTE_6.'),
 (21,'No heading after est commutatif.','485/486 boundary','The lower main485 margin is blank after est commutatif. The directly inspected upper main486 begins La démonstration du théorème3.6 without an intervening heading. The unsupported heading is already absent.')]:f(n,reading,region,reason,batch='481_485')
f(13,'Underlined E and checked E for Modules; plain checked E for its class','484 paragraph3.4','The four underlined Module occurrences and two plain class occurrences match the source. The relation is explicit: dualization sends E to E∨=Hom_{O_X}(E,O_X), and the class map sends E∨ to [E∨] in K^•(X). The underline records the source’s two stages of this same construction, and all four attached rules are already present.',change='Retain the four Module rules and both plain class letters; restore the other local E rules separately.',batch='481_485')
f(18,'Gr^k K^•(X)','485 first Chern-class paragraph','Main499 and witness496 both print k. For the invertible sheaf under consideration, x has rank1, so x−1 lies in Fil¹. The first Chern class is its image under the quotient Fil¹→Fil¹/Fil²=Gr¹. The displayed identity gives x⁻¹−1−(1−x)=(x−1)(1−x⁻¹) in Fil², so applying precisely this quotient yields c¹(x⁻¹)=−c¹(x). The quotient degree is1 throughout this proof, which determines the corrected exponent independently of the unbound printed k.',change='Current Gr¹; diplomatic Gr^k.',batch='481_485')
patch(485,'current',r'Or $c^1(x)$ est la classe dans $\Gr^kK^{\bullet}(X)$',r'Or $c^1(x)$ est la classe dans $\Gr^1K^{\bullet}(X)$','check/findings/findings_481_485.json#18','The explicit quotient Fil¹/Fil² computing c¹ fixes the degree.','misprint_in_print')

# Double lower rules are reproduced literally in diplomatic; current transports are declared.
q=next(q for q in D if q['source_id']=='check/findings/findings_476_480.json#19')
q.update(verdict='amended',reason='Main480 visibly gives the derived-functor L two separate lower strokes, independently of the single rules on each complex L. Diplomatic now reproduces the literal two strokes; current retains mathbb L for the same derived pullback. For the displayed strictly perfect representative L^{Y/Z}, derived pullback is represented term by term by f*L^{Y/Z}; the identity on that representative is the exact comparison underlying this rendering choice.',change='Diplomatic literal doubly underlined L; current mathbb L retained.')
patch(480,'diplomatic',r'\mathbb L',r'\underline{\underline{L}}','check/findings/findings_476_480.json#19','Preserve the two directly observed lower rules on the derived functor; the three single complex rules stay separate.','font')
for pg,count in [(480,1),(482,2)]:
 sid=own(pg,'projective-space P glyphs','Typed P with two lower rules','mathbb P in both attached layers','Diplomatic literal two-rule P; current bold P.','font_convention','The directly inspected P letters each have two separate lower strokes. Diplomatic keeps these strokes literally; current uses the declared bold-P representation of the same projective-space construction Proj(O_Y[T₀,…,T_r]). The identity graded-algebra map induces the identity on every degree-zero localization chart D_+(T_i), and these chart identities glue to the identity of the projective Y-scheme. The plain abbreviation P elsewhere on482 is untouched.');OWN[-1]['local_counts']={'diplomatic':count,'current':count}
 patch(pg,'diplomatic',r'\mathbb P',r'\underline{\underline{P}}',sid,'Restore the literal double rule at each counted source occurrence.','font',count)
 patch(pg,'current',r'\mathbb P',r'\mathbf{P}',sid,'Use the declared bold-P transport for the identical Proj scheme.','font',count)
f(8,'Two doubly underlined P letters; plain abbreviation P remains plain','482 projective-space identification and triangle','The main source has two independent lower rules at exactly these two projective-space symbols. The local policy now preserves those strokes diplomatically and uses current bold P for the identical Proj(O_Y[T₀,…,T_r]) scheme, with the exact identity-chart comparison recorded. This resolves the checker’s pending font decision without altering the source’s ordinary abbreviation P.',verdict='amended',change='Diplomatic two-rule P; current bold P at these two occurrences.',batch='481_485')

symbols(481,[(r'\\Omega',r'\underline{\Omega}',11),(letter('I'),r'\underline{I}',2),(letter('J'),r'\underline{J}',2),(r'K/K\^2',r'\underline{K}/\underline{K}^2',1)],'481 differential and conormal symbols','All eleven Ω and the two letters of each ideal quotient I/I²,J/J²,K/K² carry independent short rules. The K-group letter in Corollary2.7 has its raised degree bullet and remains plain. The regular expression K is narrowed below to the ideal quotient.')
# The exact mathematical K pair above is scoped by the source count; the K-group command has an adjacent exponent and would otherwise also match.

sid=own(481,'two right-hand vertical d labels','d on the left of each arrow','d on the right','Put both d labels on the printed left sides.','diagram','The main diagram and witness492 show d to the left of the K/K² and I/I² vertical arrows. Their differential maps and the already left-placed f*(d) are unchanged.')
patch(481,'both',r'''\arrow[d,"d"]''',r'''\arrow[d,"d"']''',sid,'Exact local count2; label side only.','diagram',2)

sid=own(482,'projective factorization triangle','Y centered below X and projective space','Y below projective space','Center the lower vertex while retaining its stop.','diagram','The main image places f outside the left sloping arrow and g outside the right. The identity f=g∘i and the projective-space glyph choices remain unchanged.')
for layer,pp in [('diplomatic',r'\underline{\underline{P}}'),('current',r'\mathbf{P}')]:
 old=r'''X \arrow[r,"i"] \arrow[dr,"f"'] & '''+pp+r'''^r_Y \arrow[d,"g"]\\
& Y.'''
 new=r'''X \arrow[rr,"i"] \arrow[dr,"f"'] && '''+pp+r'''^r_Y \arrow[dl,"g"]\\
& Y. &'''
 patch(482,layer,old,new,sid,'Restore source placement independently of the P font rendering.','diagram')

symbols(484,[(r'\\mathcal O',r'\underline{O}',3),(r'\\mathbb Z',r'\underline{\mathbb Z}',2)],'484 structure sheaves and constant integer sheaves','Three structure-sheaf O letters carry one rule. Both integer sheaves in H⁰(X,Z),H⁰(Y,Z) have a double-struck Z with an independent short lower rule. The plain scheme Z later in the paragraph is untouched.')
local_symbols(484,'Par additivité,',None,[(letter('E'),r'\underline{E}',2)],'484 final proof paragraph','Both E occurrences in this proof are Module letters with a short rule. This local span excludes the already correct Module/class distinction in3.4.')
sid=own(485,'proof3.5 line bundle and dual','E, checked E, E⁻¹ each independently underlined','all three plain','Restore the three Module rules.','font','The main source and witness496 underline the E letter in all three occurrences. The check accent and inverse exponent remain attached to the same letter; the ensuing class x and checked x remain plain. Dualization identifies E∨ with E⁻¹ for this line bundle, and the class map gives checked x=x⁻¹ exactly as printed.')
patch(485,'both','que $E$ est un faisceau inversible',r'que $\underline{E}$ est un faisceau inversible',sid,'Restore the source Module rule.','font')
patch(485,'both',r'$\check E=E^{-1}$',r'$\underline{\check E}=\underline{E}^{-1}$',sid,'Restore both independent Module rules, retaining accent and inverse exponent.','font')
symbols(485,[(r'L\^\{X/Y\}',r'\underline{L}^{X/Y}',1)],'485 complex in theorem3.6','The complex L has a single short lower rule, with X/Y above and the chain bullet below. No rule is added to its K-class T_f.')
f(6,'Independent Ω, ideal, integer-sheaf, Module and complex rules','481–485 local mathematical typography','All relevant source occurrences were inspected directly. Local counts are Ω11,I2,J2,K2 on481; two underlined double-struck integer-sheaf Z letters and three O letters on484, where four Module rules already match and the final two E rules are restored; three E rules and one L rule on485. Plain K-group letters, class checked E, scheme Z, and T_f are explicitly excluded.',change='Apply occurrence-scoped rule patches; retain the already correct3.4 distinction.',batch='481_485')

sid=own(485,'lower horizontal label in Riemann-Roch square','ch∘c̃ above the lower arrow','label below','Place the lower Chern-character label above its arrow.','diagram','The main source places both horizontal labels above their arrows. The lower map remains ch∘c̃:K^•(Y)→Gr K^•(Y)_Q; no arrow or expression is changed.')
patch(485,'both',r'''K^{\bullet}(Y) \arrow[r,"\ch\circ\widetilde c"']''',r'''K^{\bullet}(Y) \arrow[r,"\ch\circ\widetilde c"]''',sid,'Restore the lower label side.','diagram')
statement(481,r'\textbf{Corollaire 2.7.}',"\n\n\\subsection*",'Corollary2.7 prose',exceptions=('2.6',))
statement(483,r'\textbf{Proposition 3.2.}','\n\nOn obtient','Proposition3.2 prose')
statement(484,r'\textbf{Proposition 3.5.}','\n\nLa relation','Proposition3.5 prose')
statement(485,r'\textbf{Théorème 3.6. (Riemann--Roch).}',"\n\nEn d'autres termes",'Theorem3.6 statement and continuation',exceptions=('1.1','1.9','3.3','2.5','2.3'))
f(5,'Statement prose word groups underlined; numerical references plain','481–485 statements','All four named statement spans were inspected. The theorem continuation underlines désignant…relatif and the conjunction et between2.5 and2.3; the formulas and source references stay independently styled. The named heading uses accepted NOTE_6 typesetting.',change='Apply four explicit statement underline spans in both layers.',batch='481_485')

CHECKED += list(range(486,491))
WITNESSES.update({487:[498],489:[500],490:[501]})
for n,reading,region,reason in [
 (2,'No heading between est commutatif. and La démonstration du théorème3.6','485/486 boundary','The two adjoining main-image edges were directly inspected. The lower485 margin is blank, and486 begins with the indented sentence. Both attached layers already omit the unsupported heading. This duplicates the independently decided481_485#21.'),
 (3,'Par additivité begins at the left margin immediately after the display','486 proof3.7 opening','The image gives no paragraph indentation here. The attached absence of a blank paragraph matches it.'),
 (4,'En combinant begins an indented paragraph','486 after3.8.2','The source indentation is visible and the attached blank paragraph is correct.'),
 (5,'En outre begins an indented paragraph','487 paragraph3.9','Main501 and witness498 show the separate indented paragraph after the first projective-space formula. The attached separation is correct.'),
 (7,'La première assertion begins an indented paragraph','489 proof4.2 opening','The source indentation after the display is visible, and the attached paragraph break matches.'),
 (8,'La deuxième relation begins another indented paragraph','489 proof4.2','The first assertion fills its own line; the following sentence begins independently with the same indentation. The attached separation is correct.'),
 (9,'v^gr∘u^gr=0 in the running sentence, with its final stop','489 proof4.3','The formula occupies the continuation at the left margin, at ordinary line spacing; both layers already keep it inline.'),
 (10,'First E underlined as a sheaf; second E plain as its class','489 Proposition4.4','Both main503 and witness500 show the independent short rule on the first E and no rule on the class E. The class map sends the locally free sheaf E to [E] in K^•(X); the two stages of that same map are exactly those written in the sentence. Both attached layers already preserve this distinction.'),
 (11,'E in fibré en drapeaux de E underlined; E in somme de classes plain','489 proof4.4','The short sheaf rule and the later plain class letter are visible. For the flag projection p, the pullback sheaf p*E has a filtration by invertible quotients L_j, and its class is Σ[L_j]; this is the exact sheaf-to-class relation invoked by the proof. Both attached rules already match.'),
 (12,'489 ends faisceau inversible. Soit;490 begins ξ la classe','489/490 boundary','Both adjoining main edges confirm the marker before ξ, as already placed in both layers. No paragraph break occurs in the sentence.'),
 (13,'Par ailleurs begins an indented paragraph','490 after the second display','The source indentation is visible and the attached paragraph break matches.')]:
 f(n,reading,region,reason,batch='486_490')

for pg,count in [(487,7),(488,1)]:
 sid=own(pg,'projective-space P glyphs','Typed P with two independent lower rules','mathbb P','Diplomatic literal double rule; current bold P.','font_convention','The main image shows both lower strokes at every counted occurrence; the487 native witness detail confirms all seven, including nested subscripts. The projective space is Proj(O_Y[T₀,…,T_r]); the identity graded-algebra map gives identity maps on degree-zero localizations at T_i, which glue to the identity projective scheme. The current bold P and diplomatic two-rule P therefore encode that exact same construction. No ordinary abbreviation is changed.');OWN[-1]['local_counts']={'diplomatic':count,'current':count}
 patch(pg,'diplomatic',r'\mathbb P',r'\underline{\underline{P}}',sid,'Literal local double rules at the independently counted source occurrences.','font',count)
 patch(pg,'current',r'\mathbb P',r'\mathbf{P}',sid,'Declared current bold-P transport for the identical Proj scheme.','font',count)
f(6,'Seven doubly underlined P letters on487 and one on488','487–488 projective-space formulas','All eight source occurrences were inspected. Diplomatic now preserves each pair of lower strokes literally; current uses the declared bold-P rendering with the explicit identity on Proj charts recorded in the occurrence-scoped findings.',verdict='amended',change='Diplomatic two-rule P; current bold P, at the stated counts only.',batch='486_490')

sid=own(487,'3.9, pronoun referring to le théorème de Riemann-Roch','de la démontrer','same feminine pronoun','Current de le démontrer; preserve la diplomatically.','misprint_in_print','Main501 and native witness498 both print la. The sentence explicitly names le théorème de Riemann-Roch as the object of démontrer and repeats that same verb and object through its pronoun. Restoring masculine le agrees with the explicitly written antecedent. This French grammatical repair changes no mathematical assertion or English object reference.')
patch(487,'current','de Riemann--Roch, de la démontrer','de Riemann--Roch, de le démontrer',sid,'The immediately stated masculine antecedent le théorème determines le.','misprint_in_print')

sid=own(488,'lower horizontal edge of the blow-up square','i above Y→X','i below the lower arrow','Place i above the arrow in both layers.','diagram','The main image places the lower i on the upper side of the horizontal edge. The maps i:Y→X, j:Y′→X′, g:Y′→Y and f:X′→X still satisfy f∘j=i∘g; all four objects, arrow directions and the terminal comma remain unchanged.')
patch(488,'both',r'''Y \arrow[r,"i"'] & X ,''',r'''Y \arrow[r,"i"] & X ,''',sid,'Restore the observed label side.','diagram')
own(488,'two RRR citations','RRR I1.5 and RRR without brackets','RRR macro defined as roman RRR','Retain both unbracketed citations.','confirmed_notation','The source writes plain RRR in the first parenthesis and at its ending. The attached main preamble defines RRR as roman RRR, without added square brackets or stops, so both citations already reproduce the printed content.','confirmed; already present')

sid_domain489=own(489,'Proposition4.3 quantified domain','y∈K^•(Y)_Q','same domain before graded operators','Current y∈Gr K^•(Y)_Q; preserve printed K diplomatically.','misprint_in_print','Main503 and native witness500, review/expose_viii/images/w489_domain_native.png, both omit Gr. The cited VII4.8 on folio460 explicitly defines u^gr:Gr^{k−d}K(Y)_Q→Gr^{k−1}K(Y′)_Q×Gr^kK(X)_Q by u^gr(y)=(g^gr(y)(−1)^{d−1}c^{d−1}(F),−i_gr(y)), and v^gr(a,b)=j_gr(a)+f^gr(b). Its zero composite gives f^gr i_gr(y)=j_gr(g^gr(y)(−1)^{d−1}c^{d−1}(F)). Proposition3.5 identifies the Chern factor with c^{d−1}(F∨), proving precisely the displayed4.3 for every degreewise y and hence for their finite sums in Gr K(Y)_Q. The ungraded group is explicitly related by θ_Z=ch∘c̃:K(Z)_Q→Gr K(Z)_Q from3.3–3.4, satisfying g^grθ_Y=θ_Y′g*; applying the graded identity to θ_Y(a) supplies a corresponding identity for any ungraded a. That transport does not change the directly cited graded operators or insert θ into the printed formula. The minimal Gr insertion restores exactly the domain written in VII4.8 and used on490 for y=ch(x)Todd(T_i∨).')
patch(489,'current',r'Pour tout \(y\in K^{\bullet}(Y)_{\mathbb Q}\)',r'Pour tout \(y\in \Gr K^{\bullet}(Y)_{\mathbb Q}\)',sid_domain489,'The explicit degreewise u^gr and v^gr of the cited VII4.8 determine this domain.','misprint_in_print')

sid_ref490=own(490,'4.5, equivalence before and after f^gr','D’après3.2','same locator','Current D’après4.2; preserve3.2 diplomatically.','misprint_in_print','Main504 and native witness501 both read3.2. Proposition4.2 immediately before gives f_gr∘f^gr=Id on Gr K(X)_Q. For A=ch(i*x) and B=i_gr(ch(x)Todd(T_i∨)), the equality A=B gives f^gr(A)=f^gr(B); applying the displayed left inverse f_gr to the latter recovers A=B exactly. Thus4.2 supplies the equivalence used in this sentence. Proposition3.2 provides the filtration compatibility from which f_gr is defined, and4.2 uses that compatibility together with VII3.6 to prove the split identity. Replacing only the locator cites that established split identity without changing the proof or adding a hypothesis.')
patch(490,'current',"D'après 3.2, la formule à démontrer","D'après 4.2, la formule à démontrer",sid_ref490,'The explicitly displayed left inverse in4.2 proves this equivalence.','misprint_in_print')
f(14,'ch(g*(y)) in the right member; g*(x) in the left member','490 final display','Main504 and native witness501 both read y on the right. The preceding right member is j_gr(g^gr(ch(x)Todd(T_i∨))c^{d−1}(F∨)). Naturality gives g^gr(ch(x))=ch(g*(x)) and g^gr(Todd(T_i∨))=Todd(g*(T_i∨)); multiplication by the same Chern factor gives exactly the displayed right member with x. The left member follows from VII3.4, f*i*(x)=j*(g*(x)λ_{−1}(F)), with the same input x. These two explicit maps determine x independently; the continuation on491 uses that identical x.',change='Current ch(g*(x)); diplomatic retains ch(g*(y)).',batch='486_490')
patch(490,'current',r'\ch(g^*(y))',r'\ch(g^*(x))','check/findings/findings_486_490.json#14','Apply the stated naturality of the Chern character to the preceding input x.','misprint_in_print')

statement(486,r'\textbf{Proposition 3.7.}','\nPar additivité','Proposition3.7 prose')
statement(486,r'\textbf{Lemme 3.8.}','\n\nPar hypothèse','Lemma3.8 prose',exceptions=('3.6',))
statement(489,r'\textbf{Proposition 4.2.}','\n\nLa première','Proposition4.2 prose')
statement(489,r'\textbf{Proposition 4.3.}','\n\nCette relation','Proposition4.3 prose')
statement(489,r'\textbf{Proposition 4.4.}','\n\nLes deux membres','Proposition4.4 prose')
f(1,'Five statements underline prose word groups; references and formulas independently styled','486 and489 statement spans','Each listed span was directly compared. The3.6 references in Lemma3.8 are plain. The sheaf E in4.4 retains its independent short rule, while its class and all displayed formulas remain independently styled. Named labels follow the accepted NOTE_6 treatment. Exact local group counts accompany every patch.',change='Apply five explicit statement spans in both layers.',batch='486_490')


CHECKED += list(range(491,496))
WITNESSES.update({491:[502],492:[503],493:[504],494:[505]})
for n,reading,region,reason in [
 (2,'Compte tenu de4.4 begins an indented paragraph','491 after the Todd identity','The main image visibly separates this paragraph; the attached blank paragraph matches.'),
 (3,'Posant z begins an indented paragraph','491 after the Riemann-Roch display','The source indentation is visible and the attached paragraph break matches.'),
 (4,'i*(1)=1−J, then d’où with a small d','491 final lines','The comma has a visible tail; the following connective has a lower-case initial and the sentence continues on492. Both attached layers already reproduce these marks.'),
 (6,'491 ends d’où;492 begins with the entire ch(i*(i*(y))) display','491/492 boundary','Both adjacent main edges were compared. The marker precedes the full display exactly as printed; it no longer divides the display from its connective incorrectly.'),
 (7,'Comme i*(1)=1−J begins an indented paragraph','492 middle','The source indentation is clear and the attached blank paragraph matches.'),
 (10,'On obtient donc finalement begins an indented paragraph','492 after the Todd fraction','The source starts a new paragraph here; the attached break is correct.'),
 (12,'Y followed by a full stop','493 first triangle','The visible stop follows the centered lower vertex. The attached triangle already has that punctuation and the correct centered geometry and label sides.'),
 (13,'Or cette suite exacte begins an indented paragraph','493 after5.2.1','The source indentation is visible and the attached break matches.'),
 (16,'493 ends supposées réduites;494 begins au degré0.','493/494 boundary','Both adjoining main edges confirm the marker before au degré0 and the separate indented paragraph beginning Le module below it.'),
 (17,'Ω¹_{B/O_P} en posant, with no comma','494 first paragraph','Main508 has no mark between the differential module and en posant. The attached removal of the comma is correct.'),
 (18,'En prenant les termes begins an indented paragraph','494 end of proof5.2','The main image and native witness505 show the separate paragraph. The attached blank paragraph matches.'),
 (19,'The isomorphism Ω¹_{P/Y}→F(−1) is in the running line','494 Remark5.2.1','The main image keeps this isomorphism between the words isomorphisme and d’après. Both attached layers already keep it inline; the independent sheaf-letter rules are restored separately.'),
 (21,'495 opens with the indented Comme E=…','494/495 boundary','The main494 display ends the preceding paragraph and main495 opens a new indented one. The attached blank line at the boundary is correct.'),
 (22,'D’après la définition de Todd begins an indented paragraph','495 before5.3.1','The observed indentation is reproduced by the attached blank paragraph.'),
 (23,'On voit donc begins an indented paragraph','495 after the projection-formula calculation','The source indentation is visible and the attached paragraph break matches.')]:
 f(n,reading,region,reason,batch='491_495')

f(5,'On est donc remané','491 reduction paragraph','Both main505 and native witness502, review/expose_viii/images/w491_remane_native.png, print remané. The construction se ramener is written in the preceding4.5 reduction, and this past participle is ramené. Restore that spelling currently and retain the printed transposition diplomatically.',change='Current ramené; diplomatic remané.',batch='491_495')
patch(491,'current','On est donc remané','On est donc ramené','check/findings/findings_491_495.json#5','Restore the spelled participle of the author’s se ramener construction.','misprint_in_print')
f(8,'−c(J), with no superscript','492 image of1−J in Gr¹','Main506 and native witness503, review/expose_viii/images/w492_chern_native.png, both omit1. For this line-bundle class J, the quotient q:Fil¹K(X)→Fil¹/Fil² gives c¹(J)=q(J−1), and therefore i_gr(1)=q(1−J)=−c¹(J). The completed Chern map instead writes c(J)=1+c¹(J), as the same page states in c̃(J)=(1,1+c¹(J)); the degree-one projection of that total class is precisely c¹(J). The displayed subsequent multiplication by Todd(−J∨)=(1−exp(c¹(J)))/(−c¹(J)) uses that degree-one element. For i a rational point in P¹, J=O(−1), with h=c¹(O(1)), the two readings are h and −1+h in the graded ring; the augmentation of the latter is −1, while i_gr(1) lies in degree1. The current exponent1 restores the quotient actually specified by the sentence.',change='Current −c¹(J); diplomatic −c(J).',batch='491_495')
patch(492,'current',r"donc c'est \(-c(J)\)",r"donc c'est \(-c^1(J)\)",'check/findings/findings_491_495.json#8','The explicit Fil¹/Fil² quotient identifies the first Chern class.','misprint_in_print')
sid=own(492,'projection-formula sentence','entrainent without circumflex','entrainent','Current entraînent; retain plain i diplomatically.','misprint_in_print','Both main506 and native witness503 show a plain i in entrainent. This is the omitted circumflex of entraîner, whose accented forms occur elsewhere in this exposé. NOTE_6’s special accepted ï transport concerns ambiguité/coîncide, not this verb; the diplomatic spelling is preserved.')
patch(492,'current','3.7 entrainent','3.7 entraînent',sid,'Restore the omitted circumflex in the current French spelling.','misprint_in_print')
f(15,'Underlined O_X at the lower vertex','493 symmetric-algebra triangle','Main507 and native witness504, review/expose_viii/images/w493_triangle_native.png, both print X. Here E=O_Y^{r+1} and A=S_{O_Y}(E). The two lower arrows are exactly the unit maps O_Y→A and O_Y→A[T,T⁻¹], a↦a·1 and a↦a·1·T⁰; the upper inclusion A→A[T,T⁻¹] has their composite equality. These are the structural maps of the Y-algebras used to form V and Z. The correction O_Y supplies precisely those two maps without changing the graded algebras, their degrees or the triangle.',change='Current O_Y; diplomatic O_X.',batch='491_495')
patch(493,'current',r'& \mathcal O_X \arrow[ul] \arrow[ur] &',r'& \mathcal O_Y \arrow[ul] \arrow[ur] &','check/findings/findings_491_495.json#15','The two unit maps of the specified O_Y-algebras determine the base sheaf.','misprint_in_print')
f(20,'g*(E)·ξ⁻¹−1','494 first display5.3','Main508 and native witness505, review/expose_viii/images/w494_Tf_native.png, both print g. The displayed Euler sequence5.2 on P is 0→Ω¹_{P/Y}→f*E⊗O_P(−1)→O_P→0; applying the class map gives T_f=f*[E]·ξ⁻¹−1 in K(P), exactly with f. The earlier triangle has h:Z→P and g=f∘h, so h*f*[E]=g*[E]; tensor associativity identifies O_Z⊗_{h⁻¹O_P}(h⁻¹O_P⊗_{g⁻¹O_Y}g⁻¹E) with O_Z⊗_{g⁻¹O_Y}g⁻¹E. Pulling back the Euler equality therefore gives the corresponding identity on Z. Moreover E=O_Y^{r+1} supplies canonical trivializations of both pullbacks: under the integer unit maps Z→K(P), Z→K(Z), both are the image of r+1. The following c̃(E) is consequently transported by f^gr as the same pair(r+1,1), and is retained. The minimal current f correction names the actual pullback in the cited sequence on P; it adds no new term or explanatory material.',change='Current f*(E); diplomatic g*(E).',batch='491_495')
patch(494,'current',r'=g^*(E)\cdot\xi^{-1}-1.',r'=f^*(E)\cdot\xi^{-1}-1.','check/findings/findings_491_495.json#20','Apply the K-class map to the explicitly cited Euler sequence on P, with its f pullback.','misprint_in_print')
own(494,'proof5.2, Ω¹_{V/Y} est égal à g*(E)','Ω¹_{V/Y}=g*(E)','same printed prose','Retain the author’s notation; record the structural extension and restriction maps.','mathematical_scope','Let ρ:V=Spec_Y S(E)→Y be the structural projection, and j:Z→V the stated open complement of the zero section. The diagram’s g is exactly ρ∘j. The universal derivation defines ρ*E→Ω¹_{V/Y} by1⊗e↦d(e); on a local basis e_0,…,e_r this sends the free basis to d(e_0),…,d(e_r), with inverse furnished by the coordinate derivations, so it is an isomorphism. Restricting by j gives j*Ω¹_{V/Y}=Ω¹_{Z/Y}≅g*E. Under h’s affine sheaf/module correspondence this is the B-module f*E⊗_{O_P}B used immediately afterward. Thus the paragraph’s g notation has the explicitly available structural extension ρ and its stated restriction; no new source correction is needed for this prose. This is separate from5.3’s formula on P, whose cited Euler sequence explicitly uses f.','retained reading; exact comparison recorded')

# Independent sheaf rules, with classes left plain.
symbols(491,[(r'\\mathcal O',r'\underline{O}',3)],'491 structure sheaves','All three O letters have independent short lower rules. Their scheme subscripts, the twist1 and the sequence maps stay outside the rules.')
sid=own(491,'491 ideals and the conormal exact sequence','J6,F1,N1 independently underlined','plain letters','Restore the eight exact sheaf rules.','font','Four J letters in the two conormal quotients and two J letters in the final ideal sequence/prose are sheaf letters. The F and N in the displayed short exact sequence also have rules. The class map sends that sequence to g*(N)=F+L, whose three class letters remain plain; the final class J in i*(1)=1−J remains plain as printed. Primes and powers lie outside the individual letter rules.')
for old,new in [(r'\cl(J/J^2)',r'\cl(\underline{J}/\underline{J}^2)'),(r"\cl(J'/J'^2)",r"\cl(\underline{J}'/\underline{J}'^2)"),(r'0\longrightarrow F\longrightarrow g^*(N)',r'0\longrightarrow \underline{F}\longrightarrow g^*(\underline{N})'),(r'0\longrightarrow J\longrightarrow',r'0\longrightarrow \underline{J}\longrightarrow'),(r'où \(J\) est ici inversible',r'où \(\underline{J}\) est ici inversible')]:
 patch(491,'both',old,new,sid,'Restore only the directly observed sheaf-letter rules.','font')
OWN[-1]['local_counts']={'J':6,'F':1,'N':1}
symbols(492,[(r'\\mathcal O',r'\underline{O}',2),(letter('E'),r'\underline{E}',1)],'492 final sheaf definitions','The two structure-sheaf O letters and E in the final definition have their own short rules. Both plain projective-space abbreviations and all K-classes remain independently styled.')
sid=own(492,'492 invertible ideal and its conormal quotient','Three J sheaf letters underlined; class J plain','all J letters plain','Restore the three sheaf J rules.','font','The initial Comme J est inversible refers to the ideal sheaf, and both letters in cl(J/J²) are sheaves. The quotient is J⊗O_Y and the class map gives cl(J/J²)=i*[J], so the later class occurrences are the expressly related K-classes and remain plain.')
patch(492,'both',r'Comme \(J\) est inversible',r'Comme \(\underline{J}\) est inversible',sid,'Initial invertible sheaf rule.','font')
patch(492,'both',r'\cl(J/J^2)',r'\cl(\underline{J}/\underline{J}^2)',sid,'Both conormal ideal letters carry separate rules.','font')
sid=own(492,'5.1 two projective-space symbols','P with two lower rules','mathbb P','Diplomatic literal double rule; current bold P.','font_convention','Both source symbols have two lower strokes. The ordinary abbreviation P remains plain. As for the preceding observed P occurrences, the identity graded map on O_Y[T₀,…,T_r] induces the identity on every projective chart, so the declared two renderings denote the same projective Y-scheme.');OWN[-1]['local_counts']={'diplomatic':2,'current':2}
patch(492,'diplomatic',r'\mathbb P',r'\underline{\underline{P}}',sid,'Literal double rule at the two inspected occurrences.','font',2)
patch(492,'current',r'\mathbb P',r'\mathbf{P}',sid,'Declared current rendering at the same two occurrences.','font',2)
f(9,'Two doubly underlined projective P letters; ordinary P plain','492 paragraph5.1','Main506 shows both pairs of lower rules. The exact identity on the projective charts is recorded in the local font finding; this completes the same occurrence-scoped policy already used on480,482,487,488.',verdict='amended',change='Diplomatic two-rule P; current bold P at these two symbols.',batch='491_495')

symbols(493,[(r'\\Omega',r'\underline{\Omega}',5),(letter('E'),r'\underline{E}',7),(letter('B'),r'\underline{B}',7),(letter('F'),r'\underline{F}',2),(r'\\mathcal O',r'\underline{O}',7)],'493 sheaves in the Euler-sequence proof','Every listed letter has an independent short rule: Ω5,E7,B7,F2,O7. The four E letters inside S(E) are included. The S letters have a separate double rule, handled next. The current base-subscript correction O_Y and printed O_X both retain the same O rule.')
symbols(494,[(r'\\Omega',r'\underline{\Omega}',10),(letter('B'),r'\underline{B}',5),(letter('F'),r'\underline{F}',1),(r'\\mathcal O',r'\underline{O}',6)],'494 differential sheaves and coefficient algebra','All ten Ω, five B, one F and six O letters have individual lower rules. Indices, powers, twists, tensor subscripts and pullback operators remain separate.')
local_symbols(494,marker(494),r'\textbf{5.3.}',[(letter('E'),r'\underline{E}',14)],'494 E sheaves before5.3','All fourteen E letters in the proof and its remark are sheaves, with short lower rules, including the eight E letters inside S(E). The two E letters after5.3 are K-classes and remain plain.')
for pg,count in [(493,4),(494,8)]:
 sid=own(pg,'symmetric-algebra S(E) glyphs','S with two lower rules; E with one','plain S; E rule restored separately','Diplomatic literal two-rule S; current bold S.','font_convention','The main image and native witness show the two S strokes independently of the single E rule. Both renderings denote the symmetric algebra ⊕_n E^{⊗n}/(permutation relations). The identity on E induces the identity on every tensor power, descends to each symmetric quotient, and yields mutually inverse identity graded-algebra maps. This occurrence-scoped VIII choice changes no generator, degree, algebra map or subscript; it does not propagate to earlier exposés.');OWN[-1]['local_counts']={'diplomatic':count,'current':count}
 patch(pg,'diplomatic',r'S(\underline{E})',r'\underline{\underline{S}}(\underline{E})',sid,'Preserve both directly observed lower S strokes literally.','font',count)
 patch(pg,'current',r'S(\underline{E})',r'\mathbf{S}(\underline{E})',sid,'Declared current bold-S representation of the identical symmetric algebra.','font',count)
f(14,'Four double-rule S letters on493; eight on494; each E singly underlined','493–494 symmetric algebras','Every occurrence was inspected on the main pages, with the native witness confirming the two-stroke form in the triangle and differential proof. The diplomatic and current renderings are separately declared and compared through the identity of the symmetric algebra, with exact per-page counts.',verdict='amended',change='Diplomatic double-rule S; current bold S, retaining each independent E rule.',batch='491_495')
symbols(495,[(r'\\mathcal O',r'\underline{O}',1)],'495 initial structure sheaf','The first-line O_Y has its own rule, with r+1 outside it.')
sid=own(495,'initial sheaf E and its class','First E underlined; the two following E class letters plain','all E letters plain','Underline only the first E.','font','The source gives E=O_Y^{r+1} with the sheaf rule, then E=r+1 and c̃(E) without it. The class map explicitly sends the trivial rank(r+1) sheaf to (r+1)[O_Y]; completed Chern class sends it to(r+1,1). These exact maps justify preserving all three printed forms.')
patch(495,'both',r'Comme \(E=(\underline{O}_Y)^{r+1}\)',r'Comme \(\underline{E}=(\underline{O}_Y)^{r+1}\)',sid,'Only the first sheaf E is underlined.','font')
f(1,'Independent sheaf rules throughout491–495; corresponding K-classes plain','491–495 local mathematical letters','The exact local counts are recorded in each patch:491 J6,F1,N1,O3;492 J3,E1,O2;493 Ω5,E7,B7,F2,O7;494 Ω10,B5,F1,O6,E14 before5.3;495 E1,O1. The unlined classes are linked to these sheaves by the stated class, pullback, tensor and completed Chern maps. No rule is added to a class solely for visual consistency.',change='Apply the explicit occurrence-scoped sheaf-letter patches in both layers.',batch='491_495')
statement(493,r'\textbf{Proposition 5.2.}','\n\nOn considère','Proposition5.2 prose')
f(11,'On a sur; la suite exacte; i and e separately; on a un isomorphisme underlined','493 Proposition5.2','The exact word-group rules were inspected. The dots in i.e. stay outside the two small rules; formulas retain their separately recorded sheaf-letter rules. The displayed où remains plain. Named label typesetting follows NOTE_6.',change='Apply the explicit statement-prose underline span in both layers.',batch='491_495')


CHECKED += [496,497]
WITNESSES.update({496:[507],497:[508]})
for n,reading,region,reason in [
 (1,'No punctuation after the final parenthesis of5.4.3','496 display5.4.3','The main image shows no terminal stop; the attached removal is correct. The following sentence begins independently as printed.'),
 (4,'A wide completion hat over Gr K^•(Y)_Q','496 coefficient ring','The main image and witness507 show the roof extending from Gr through the rational coefficient subscript. Both attached layers already include the full widehat around that ring.'),
 (5,'A semicolon after est0 in the first RR row','496 brace display','The main image and witness507 show the lower comma component of the semicolon. The attached semicolon is correct.'),
 (8,'BIBLIOGRAPHIE in capitals, with a rule','497 heading','The source capitals are already reproduced; section-heading typesetting without a literal rule is accepted by NOTE_6.'),
 (9,'Le théorème de Riemann-Roch in plain type','497 bibliography1','Both scans leave the article title unlined. The attached removal of emph matches the source; the joint-name dash follows NOTE_6.'),
 (10,'Techniques de construction et théorèmes d’existence en Géométrie Algébrique in plain type','497 bibliography2','Both scans leave this title unlined. The attached removal of emph matches the source, including the printed capitals.'),
 (11,'1960-61 with a short hyphen','497 bibliography2 date','Both scans show the ordinary typewriter hyphen. The attached single-hyphen rendering matches. This date range is independent of the accepted en dash in joint names.')]:
 f(n,reading,region,reason,batch='496_500')
f(2,'la serie, without accent','496 paragraph before RR','Main510 and witness507 both print a plain first e in serie, while écrire retains its accent in the same line. The current série restores the omitted accent; diplomatic keeps the visible reading.',change='Current série; diplomatic serie.',batch='496_500')
patch(496,'current',r'la serie \(\varphi_k=',r'la série \(\varphi_k=','check/findings/findings_496_500.json#2','Restore the omitted acute accent in the current French spelling.','misprint_in_print')
f(3,'No full stop after Gr K^•(Y) at the end of the independence sentence','496 before On peut alors écrire','The main image shows no stop after the closing parenthesis. The completed sentence is followed by a separate indented paragraph. The attached diplomatic absence and current terminal stop already preserve and correct this source omission respectively.',change='Retain the existing diplomatic absence/current full-stop variant.',batch='496_500')
f(6,'Three baseline multiplication stops on496 and one on497','VIII496–497 multiplication occurrences only','The two products defining φ and5.4.3 use the power-series multiplication map μ:Q[[u]]⊗Q[[u]]→Q[[u]], μ(a⊗b)=ab, evaluated at the displayed nilpotent x after cancellation through the unit (1−exp(−u))/u. The stops before dx and dy use the module action Q((u))⊗Q((u))du→Q((u))du, a⊗bdu↦abdu, and its y counterpart. The existing cdot renders exactly those multiplication operations; its vertical placement follows the retained typesetting convention and adds or removes no operator. This decision covers only the four directly inspected VIII occurrences. The nominal aggregate also lists IX examples, which were not inspected in this review and are covered by the coordinator’s occurrence supplement ASTRA-IX-PRODUCT-DOTS-499-502.',verdict='retained convention; VIII occurrences inspected',change='Keep cdot at the four VIII occurrences; see the separate IX occurrence supplement.',batch='496_500')
D[-1]['scope_pages']=[496,497]
D[-1]['related_record']='ASTRA-IX-PRODUCT-DOTS-499-502'
f(7,'A full stop after the residue fraction, followed by lower-case c’est-à-dire','497 first display and following line','Main511 and witness508 both show a compact full stop without a comma tail. The next lower-case clause restates the same residue as a coefficient, continuing the sentence introduced by résidu de. The attached diplomatic full stop/current comma already preserves this source punctuation and restores that continuation.',change='Retain the existing diplomatic stop/current comma variant.',batch='496_500')
own(496,'formal series and final change of parameter496–497','φ_k and the residue calculation as printed','same expressions','Retain the formulas with their exact formal-series interpretation recorded.','mathematical_scope','Use a formal variable u before evaluating the printed class x. The series U(u)=(1−exp(−u))/u has constant term1, hence a unique inverse in Q[[u]], and φ_k is exp(ku)U(u)^{−r−1}. Evaluation Q[[u]]→Q[x]/(x^{r+1}), u↦x, is the finite truncation modulo u^{r+1}; it gives the printed class without division by the nilpotent x. The coefficient of u^r equals Res_u exp(ku)du/(1−exp(−u))^{r+1}. The substitution y=1−exp(−u) has inverse u=−log(1−y), with du=dy/(1−y), so its exact image is (1−y)^{−k−1}dy/y^{r+1}, as printed on497. In the stated range −r≤k<0, the integer −k−1 runs from0 to r−1, so the numerator polynomial has no y^r term; for k=0 the numerator is Σ_{n≥0}y^n and that coefficient is1. This proves the two stated coefficient values, including r=0 where the negative-k range is empty, without changing the author’s formulas or adding a hypothesis.','retained reading; exact formal maps recorded')


# EXACT_HISTORICAL_LINKS
for path in ['fixes/FIXLOG_6.jsonl','fixes/FIXLOG_6_CURRENT.jsonl']:
 for i,line in enumerate((R/path).read_text().splitlines(),1):
  rec=json.loads(line)
  for q in list(D):
   if q['record_type']!='checker' or str(q.get('original_record_page',q['page']))!=str(rec.get('page')):continue
   x=F[q['source_id'].split('/')[-1]];fix=x.get('fix')
   if fix and fix.get('old')==rec.get('old') and fix.get('new')==rec.get('new'):
    D.append({**q,'record_type':'fixlog','source_id':path+f'#{i}','related_finding':q['source_id']});break
for i,x in enumerate(json.loads((R/'fixes/MISPRINTS_6.json').read_text()),1):
 for q in list(D):
  if q['record_type']=='checker' and q.get('original_record_page',q['page'])==x['page'] and q['where']==x['where']:
   D.append({**q,'record_type':'misprint','source_id':f'fixes/MISPRINTS_6.json#{i}','related_finding':q['source_id'],'misprint':q.get('misprint',True),'correction':q['change'] if q.get('misprint') is False or q['verdict']=='amended' else x['correct']});break
B={q['source_id']:q for q in D+OWN}
def ck(batch,n):return f'check/findings/findings_{batch}.json#{n}'
def copy_decision(sid,typ,ref,verdict=None,change=None,extra=''):
 q=B[ref];z={**q,'record_type':typ,'source_id':sid,'related_record':ref}
 if verdict is not None:z['verdict']=verdict
 if change is not None:z['change']=change
 if extra:z['reason']=q['reason']+' '+extra
 D.append(z);B[sid]=z;return z
C=json.loads((R/'fixes/RECONCILE_CODEX_6.json').read_text())['entries']
def codex(n,ref,verdict=None,change=None,extra=''):
 z=copy_decision(f'fixes/RECONCILE_CODEX_6.json#{n}','codex',ref,verdict,change,extra);z['codex_id']=C[n-1]['id'];z['prior_status']=C[n-1]['status'];return z
H=json.loads((R/'fr/codex/HOLD_VS_CORR.json').read_text())
def hold(n,ref,extra=''):
 z=copy_decision(f'fr/codex/HOLD_VS_CORR.json#{n}','hold_difference',ref,extra=extra);z['corr_lines']=H[n-1]['corr_lines'];z['hold_lines']=H[n-1]['hold_lines'];return z

# HISTORICAL_ALIASES
codex(200,ck('466_470',14),verdict='prior rejection reversed; current correction now applied')
codex(201,ck('466_470',21))
codex(202,ck('471_475',8),verdict='prior rejection reversed; current correction now applied')
codex(203,ck('471_475',16))
codex(204,sid_module470,verdict='rejection confirmed; source capital retained')
codex(205,ck('471_475',9))
codex(206,ck('471_475',10))
codex(207,ck('471_475',23))
hold(46,ck('471_475',8),extra='Nominal imported page association was wrong; this exact sentence is printed472. The HOLD Z reading is now independently confirmed.')
hold(47,ck('471_475',9),extra='Actual source472; the added SGA-SRC comment is editorial metadata, not printed text.')
hold(48,ck('471_475',10),extra='Actual source472. Both old variants retain an added comma after réciproque; checker471_475#7 independently removes that comma in both current layers. The substantive HOLD difference is solely the restored accent in où.')

codex(208,ck('476_480',6))
codex(209,sid_regular477,verdict='prior rejection reversed; minimal current correction now applied')
codex(210,ck('476_480',12))
codex(211,ck('476_480',17))
codex(212,sid_capitals479,verdict='rejection confirmed; source capitals retained')
codex(213,sid_respe479,verdict='rejection confirmed; printed abbreviation retained')
hold(49,sid_regular477,extra='The actual source is477. Its HOLD correction is independently established by the native source, counterexample and explicit conormal retraction; the added SGA-SRC comment is not printed text.')
hold(50,ck('476_480',12),extra='The actual source is477; only the source circumflex omission is restored in the current branch.')

codex(325,ck('471_475',9),extra='This tagged SGA-SRC-001509 entry repeats the queue record205. The native472 sentence and its missing conjunction were independently inspected; the tag adds no printed body text.')
codex(326,sid_regular477,verdict='prior rejection reversed; minimal current correction now applied',extra='This tagged SGA-SRC-001513 entry repeats queue209 and HOLD49. The directly observed477 assertion, explicit nonregular-immersion example and conormal retraction govern all three aliases.')
for line,ref in [
 (456,ck('466_470',21)),(457,ck('471_475',9)),(458,ck('471_475',10)),
 (459,ck('471_475',16)),(460,ck('471_475',23)),(461,ck('476_480',6)),
 (462,ck('476_480',12)),(463,ck('476_480',17))
]:
 copy_decision(f'fixes/FIXLOG_6_CURRENT.jsonl#{line}','fixlog',ref,extra='This exact historical current-layer application is linked to the independently inspected source reading and its stated local proof. The earlier application status supplies no scan evidence.')

# WRITE_OUTPUTS
for page in sorted(set(CHECKED)|set(PARTIAL)):
 for layer in ('diplomatic','current'):layer_text(page,layer)
 q=dict(page=page,pdf_page=page+14,checked_against_scan=page not in PARTIAL,scan='scan/SGA6_scan_360dpi.pdf',regions='two overlapping full-width strips covering all body text, diagrams and footnotes,252dpi',witness_pages=WITNESSES.get(page,[]),findings=sum(q['page']==page for q in OWN),note='Entire page compared word by word and symbol by symbol; explicit statement prose underlines and local mathematical forms recorded.')
 if page in PARTIAL:q.update(unresolved=PARTIAL[page],note='Visible source compared; specified unreadable regions remain unresolved and full-page certification is withheld.')
 STATUS.append(q)
for name,rows in [('decisions.jsonl',D),('patches.jsonl',P),('own_findings.jsonl',OWN),('page_status.jsonl',STATUS)]:
 (O/name).write_text(''.join(json.dumps(x,ensure_ascii=False)+'\n' for x in rows))
print('decisions',len(D),'patches',len(P),'own',len(OWN),'pages',len(STATUS))

