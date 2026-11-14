#!/usr/bin/env python3
"""IX511–515 complete source comparison, with exact quotient-index adjudication."""
import json,re,shutil
from pathlib import Path
from review_helpers import Review,base_text
r=Review();batch='511_515'
obs={
1:('Struck D alone in the first factor','Both complete511 images show D alone, without its E argument, in the first tensor line. Retain the attached abbreviation. The identification D=D(E) here is the identity on the complete-flag scheme named at the end of510.','First display, first D',511),
2:('Two more struck D abbreviations','Both complete511 images show D alone in the middle and final terms of the first display. Retain the abbreviations and their struck glyph, via the identity on the same flag scheme.','First display, last two D letters',511),
3:('Struck D alone in K(D) est libre','Both complete511 images show the abbreviated D. Retain it; this is the same complete-flag scheme and the same pullback on K groups.','After first display',511),
4:('Struck D(E), with singly ruled E','Both complete511 images show struck D and the ruled E argument in Soit donc. Retain mathbb D and restore the separately observed E rule. Identity on the flag functor gives the notation comparison.','Second proof paragraph',511),
5:('Comma after P(E)','Both complete511 images show the comma after the projective-bundle expression. Retain it.','Second proof paragraph',511),
6:('New indented Soit donc paragraph','Both complete511 images show the indentation after the preceding display. Retain that paragraph boundary.','Before Soit donc',511),
7:('réccurrence, with two c letters','Both complete511 images print réccurrence here, followed later on the same page by récurrence. Retain the doubled source letter diplomatically and the existing one-c current spelling. This lexical correction leaves the same induction on rank and its maps unchanged.','Soit donc paragraph',511),
8:('33 filled raised K dots:13 on511,7 on513,13 on514','All complete primary/native511–515 pairs were compared. The33 occurrence total is correct; the historical distribution8 on513 and12 on514 predates the514 marker repair and becomes7/13 at the true boundary. Restore the raised bullets at the individually read positions and retain all lower coherent-group dots. The comparison [E]↦[E] from locally free to coherent classes and the tensor action([E],[F])↦[E tensor F] are unchanged.','All raised K occurrences511–515',511),
9:('Occurrence-specific single rules on modules and sheaves','All complete511–515 primary/native pairs show the recorded lower rules:511 E6,F2,O3;512 E8,F5,O8, with the parenthetical contravariant en E plain;513 E13,F17,A1,O5;514 E11,F10,I4,O3, with xi subscripts E/F, the class I, plain J and the class E retained;515 E12,F2,L4,G5,B1,O2, including separately ruled G and B in the quotient G/B. Restore these precise letters with primes and indices outside. The class map E↦[E], ideal inclusions and identity on each module supply the exact comparisons.','All module/sheaf occurrences511–515',511),
10:('Individually ruled statement word groups','All complete511,513,514,515 primary/native images show separate word-group rules in Corollary3.2,Proposition3.4 and Proposition4.1. Restore the observed prose groups, leaving formula letters under their independent glyph decisions. NOTE_6 permits the existing bold statement labels and unruled subsection heading.','Statements3.2,3.4,4.1',511),
11:('512 begins On a alors','The complete511/512 image pairs put the full preceding sentence ending est projectif on511 and start512 at On a alors. Retain the attached marker at that boundary, within the same running argument.','Boundary511/512',512),
12:('Left exponent−1, right exponent−i','Both complete512 images show the digit1 on the left and dotted i on the right. The formula511 defines phi((x_i))=sum_i xi^(−i) f^*(x_i). Applying f_* termwise and the projection formula gives exactly sum_i x_i f_*(xi^(−i)); current therefore keeps its corrected exponent−i, while diplomatic keeps−1. For X=P^1_k,n=2,x_0=1,x_1=0, the printed left side is chi(O(−1))=0 but the displayed right side is1; the corrected left side is chi(O)=1.','First displayed projection formula',512),
13:('New En sens inverse paragraph','Both complete512 images show the indented paragraph after the V-action sentence. Retain the attached paragraph break.','Last paragraph',512),
14:('Two struck S letters in the tensor algebra','Both complete513 images show the vertical stroke through both symmetric-algebra S letters. Retain mathbb S, with identity on each homogeneous Sym^d summand.','First paragraph tensor expression',513),
15:('Two struck S letters in the quotient','Both complete513 images show struck S twice. Retain those glyphs for the same graded algebra, with identity on its homogeneous pieces.','First paragraph quotient',513),
16:('Struck S in the degree-zero localization','Both complete513 images show the struck S. Retain mathbb S. The map Sym(F)/(s−1)→Sym(F)_(s) sends a homogeneous a_d to a_d/s^d; its inverse sends that fraction to the class of a_d. These formulas preserve the source algebra identification.','First paragraph homogeneous fractions',513),
17:('Two struck S letters inside plain Proj','Both complete513 images show the two struck S letters and plain Proj without a lower rule. Retain those local glyphs. The quotient Sym(F)/(s)→Sym(E) is induced by u:F→E in3.3.1, and identifies their degree-zero charts.','Closed-complement formula',513),
18:('Three struck S letters','Both complete514 images show struck S in the three symmetric-algebra occurrences. Retain them. The graded map Sym(F)→Sym(E) is Sym(u), and its kernel is the homogeneous ideal generated by s(O_S).','Ideal description after projection formula',514),
19:('514 begins b in K-raised-dot(P(E)),on a','The complete513/514 pairs place a in K_bullet(S) et at the end of513 and the entire b clause at the start of514. Retain that marker.','Boundary513/514',514),
20:('Struck Gl, with lower-case l','Both complete514 images show the doubled G and small l in the section title. Retain the explicit bold Gl typesetting transport, keeping it distinct from the plain Gl encountered later in this exposé. It denotes the same functor R↦Aut_R(R^n), via identity on every invertible matrix. The subsection heading remains under the accepted NOTE_6 convention.','Section4 title',514),
21:('Struck Gl, with lower-case l','Both complete514 images show the same doubled Gl in4.1. Retain bold Gl as the declared transport for this local struck word. The identity natural transformation of R↦Aut_R(R^n) records its meaning.','Proposition4.1 group',514),
22:('The quotient homomorphism is inline','Both complete514 images put the homomorphism in running text with est donc un isomorphisme on the same line. Retain the attached inline opening.','Last proof paragraph',514),
23:('The same inline formula closes before est donc','Both complete514 images confirm that the formula continues directly into the prose. Retain its attached inline closing.','Last proof paragraph',514),
24:('515 begins par(E−n)','The complete514/515 pairs put le lambda-idéal engendré at the end of514 and par(E−n) at the beginning of515. Retain the attached marker.','Boundary514/515',515),
25:('One full stop after K_bullet(P)','Both complete515 images show one stop, with the headed isomorphism arrow and tilde. Retain the attached single punctuation mark.','Opening quotient display',515),
26:('Inline F_0 quotient formula with one full stop','Both complete515 images show the formula in the running paragraph and exactly one final stop. Retain the attached inline formula and paragraph break before Par ailleurs. The actual quotient map is separately used to adjudicate the later index.','End of first proof paragraph',515),
}
for k,(printed,why,region,p) in obs.items():
 r.finding(batch,k,printed,why,region,witness=p+11,actual_page=p,verdict='amended' if k==8 else 'not applied and now applied' if k in [9,10] else 'confirmed')
for k in range(27,35):
 r.finding(batch,k,'Juxtaposed source indices, without an inserted comma','Both complete515 images and the native detail show the juxtaposed0 and base-scheme indices. Retain the attached removal of the extra comma at this exact occurrence. The pullback to that same base scheme is unchanged.','The indexed occurrence identified in finding'+str(k),witness=526,actual_page=515)
r.source('fixes/FIXLOG_6_CURRENT.jsonl#466',obs[7][0],obs[7][1],obs[7][2],witness=522,page=511,change='Keep the printed spelling diplomatically and récurrence in current.')
for row in r.decisions:
 if row.get('kind')=='misprint_in_print' or row['type']=='misprint' or row['source_id']=='fixes/FIXLOG_6_CURRENT.jsonl#466':row.update(is_misprint=True,correction_status='accepted paired lexical/exponent correction')

id='ASTRA-IX-QUOTIENT-INDEX-515'
why='Both complete515 images and the native index detail show i+1 in the congruence. The same page defines F_0^(i)=G_0^(i−1)/G_0^(i), so the quotient q_i:G_0^(i−1)→F_0^(i) has kernel G_0^(i). Thus q_i(a)=q_i(b) exactly when a−b lies in G_0^(i). The comparison from G_0^(i−1)/G_0^(i+1) onto F_0^(i) has the extra kernel G_0^(i)/G_0^(i+1). In k² take G_0=k²,G_1=ke_1,G_2=0,i=1: e_2 and e_2+e_1 give the same basis class in F_1, and the upper unipotent matrix[[1,1],[0,1]] relates them, but their difference e_1 is not in G_2. Replace only i+1 by i in current, retaining the printed index diplomatically. The independent full-page/native audit agrees and is preserved in quotient_index_515.json.'
r.own_finding(id,515,'G_{0S-double-prime}^{(i+1)}','Same printed i+1','Current-only restoration of denominator index i.',why,'Representatives of the basis class',kind='misprint_in_print',witness=526)
r.own[-1].update(is_misprint=True,correction_status='accepted paired quotient-kernel correction',proof_file='review/expose_ix/quotient_index_515.json')
for source in ['fr/codex/HOLD_VS_CORR.json#51','fixes/RECONCILE_CODEX_6.json:entries#162','fixes/RECONCILE_CODEX_6.json:entries#327']:
 r.source(source,'Printed i+1; denominator definition i',why,'515 quotient definition and later congruence',verdict='not applied and now applied',change='Accept the earlier Codex i+1→i correction in current only.',witness=526,page=515);r.decisions[-1].update(is_misprint=True,correction_status='accepted paired quotient-kernel correction',related_finding=id)
r.patch(515,'current',"G_{0S''}^{(i+1)}","G_{0S''}^{(i)}",id,why)
shutil.copyfile(Path(__file__).parents[1]/'english/contributions/exposes_viii_x/IX515_independent_audit.json',Path(__file__).parent/'quotient_index_515.json')
id='ASTRA-IX-TORUS-WORDING-515'
why='Both complete515 images and the native torus detail print laissant les e_i invariants. Retain this author wording in both layers. The displayed maximal torus is described by the diagonal morphism d:(G_m)^n→GL_n,(t_i)↦diag(t_i); it sends e_i to t_i e_i and preserves the submodule Re_i. The pointwise stabilizer of every vector e_i is the identity subfunctor, because every t_i must equal1; its inclusion into the diagonal torus is(1,…,1). These explicit maps locate the wording issue, but the source supplies no isolated glyph replacement determining a unique revised phrase. This retained-author observation belongs in the decision records and creates no reader apparatus entry.'
r.own_finding(id,515,'T laissant les e_i invariants','Same wording','Retain the author phrase with exact action/stabilizer analysis in records.',why,'Maximal torus sentence',kind='mathematical_observation',verdict='confirmed',witness=526);r.own[-1].update(is_misprint=False,correction_status='retained author wording; no paired variant',proof_file='review/expose_ix/quotient_index_515.json')
id='ASTRA-IX-FINAL-STOP-512'
why='The complete512 primary page has a small blurred mark after(3.3.1). The complete native page and its full-resolution ending detail resolve a compact full stop with no comma tail. Restore that stop in both layers; the following513 paragraph begins independently at Soit donc. This repairs the transcription of the available witness and does not introduce a corrected-versus-diplomatic variant.'
r.own_finding(id,512,'A full stop after la suite(3.3.1)','A comma after(3.3.1)','Restore the native-confirmed full stop in both layers.',why,'Final punctuation',kind='punctuation',witness=523);r.own[-1]['is_misprint']=False
r.patch(512,'both','la suite (3.3.1),','la suite (3.3.1).',id,why)

def current(p,layer):
 t=base_text(p,layer)
 for x in r.patches:
  if x['page']==p and x['layer'] in ['both',layer]:
   assert t.count(x['old'])==x['expected_count'],(p,layer,x['source_id']);t=t.replace(x['old'],x['new'])
 return t
id='ASTRA-IX-RAISED-K-511-514';why=obs[8][1]
r.own_finding(id,511,obs[8][0],r'K^\circ','Restore the33 filled raised dots.',why,obs[8][2],kind='symbol',witness=522);r.own[-1].update(is_misprint=False,source_pages=[511,513,514],observed_occurrences={511:13,513:7,514:13})
for p,n in [(511,13),(513,7),(514,13)]:r.patch(p,'both',r'K^\circ',r'K^{\bullet}',id,why,count=n)

def select_rules(t,letter,ordinals,total):
 ms=list(re.finditer(r'(?<![A-Za-z\\])'+letter+r'(?![A-Za-z])',t));assert len(ms)==total,(letter,len(ms),total)
 for i,m in reversed(list(enumerate(ms,1))):
  if i in ordinals:t=t[:m.start()]+r'\underline{'+letter+'}'+t[m.end():]
 return t
counts={511:{'E':6,'F':2,'O':3},512:{'E':8,'F':5,'O':8},513:{'E':13,'F':17,'A':1,'O':5},514:{'E':11,'F':10,'I':4,'O':3},515:{'E':12,'F':2,'L':4,'G':5,'B':1,'O':2}}
for p in range(511,516):
 id=f'ASTRA-IX-GLYPHS-{p}';why=obs[9][1]
 r.own_finding(id,p,'Individually ruled module/sheaf letters','Plain letters and mathcal O','Restore only each observed single rule.',why,'Module/sheaf notation',kind='font',witness=p+11);r.own[-1].update(is_misprint=False,observed_rule_counts=counts[p])
 for layer in ['diplomatic','current']:
  old=current(p,layer);s=old;assert s.count(r'\mathcal O')==counts[p]['O'];s=s.replace(r'\mathcal O',r'\underline{O}')
  if p==511:
   s=select_rules(s,'E',set(range(1,7)),6);s=select_rules(s,'F',{1,2},2)
  elif p==512:
   s=select_rules(s,'E',{1,2,4,5,6,7,8,9},9);s=select_rules(s,'F',set(range(1,6)),5)
   assert s.count(r'\check \underline{E}')==2;s=s.replace(r'\check \underline{E}',r'\check{\underline{E}}')
  elif p==513:
   s=select_rules(s,'E',set(range(1,14)),13);s=select_rules(s,'F',set(range(1,18)),17);s=select_rules(s,'A',{1},1)
  elif p==514:
   s=select_rules(s,'E',{1,2,3,5,6,9,10,11,12,13,15},15);s=select_rules(s,'F',{1,2,4,5,9,10,11,12,13,16},16);s=select_rules(s,'I',{1,2,4,5},5)
  else:
   s=select_rules(s,'E',set(range(2,14)),13);s=select_rules(s,'F',{1,2},2);s=select_rules(s,'L',{1,2,3,4},4);s=select_rules(s,'G',{4,5,6,7,9},9)
   assert s.count('/B$')==1;s=s.replace('/B$',r'/\underline{B}$')
  assert s!=old;r.patch(p,layer,old,s,id,why)
id='ASTRA-IX-PARAGRAPH-NUMBER-512'
why='Both complete512 images show the plain paragraph number3.3. NOTE_6 treats paragraph-number bold as a separate pending convention. Remove only the added bold wrapper in both layers, preserving exactly3.3 and its stop.'
r.own_finding(id,512,'Plain3.3.',r'\textbf{3.3.}','Remove the added bold wrapper.',why,'Paragraph3.3',kind='font',witness=523);r.own[-1]['is_misprint']=False;r.patch(512,'both',r'\textbf{3.3.}','3.3.',id,why)

def rules(t,phrases):
 pat='(?<![A-Za-zÀ-ÿ])('+'|'.join(re.escape(x).replace(r'\ ',r'\s+') for x in sorted(phrases,key=len,reverse=True))+')(?![A-Za-zÀ-ÿ])'
 return re.sub(pat,lambda m:r'\uline{'+m[0]+'}',t)
blocks={
511:('Corollaire 3.2.','On a déjà vu',['Soient','un schéma noethérien','un','-Module localement libre de rang','le fibré projectif associé','le morphisme structural de','et','la classe dans','du faisceau',"Alors l'homomorphisme",'défini par','est un isomorphisme']),
513:('Proposition 3.4.','Avec les identifications',['Soient','un schéma noethérien','un','-Module localement libre de rang','le fibré vectoriel associé','un torseur sous','le morphisme structural de',"Alors l'homomorphisme canonique",'est un isomorphisme']),
514:('Proposition 4.1.',None,['Soient','un schéma noethérien','le','groupe','un torseur sous','et','-Module localement libre de rang','correspondant à','On note','la classe de','dans','idéal engendré']),
515:(None,r'Soient $\underline{E}_0',['par','Si','est le morphisme structural de','alors','défini car','est plat','est surjectif et définit un isomorphisme'])}
for p,(label,end,phrases) in blocks.items():
 id=f'ASTRA-IX-WORD-RULES-{p}';why=obs[10][1]
 r.own_finding(id,p,obs[10][0],'Plain statement prose','Restore the observed statement word groups.',why,'Statements3.2,3.4,4.1',witness=p+11);r.own[-1]['is_misprint']=False
 for layer in ['diplomatic','current']:
  old=current(p,layer);a=old.index(r'\textbf{'+label+'}')+len(r'\textbf{'+label+'}') if label else old.index('\n')+1;b=old.index(end,a) if end else len(old)
  s=old[:a]+rules(old[a:b],phrases)+old[b:];assert s!=old;r.patch(p,layer,old,s,id,why)
id='ASTRA-IX-LOCAL-NOTATION-511-515'
why='All complete511–515 primary/native pairs were compared.511 projective P and flag D,512 vector-bundle V,513–514 projective P and symmetric S are visibly struck and retain their attached mathbb forms;513 Proj remains plain.514 Gl retains its declared bold struck-word transport. The plain E in512 contravariant en E, the plain ideal J514 and all xi_E/xi_F subscripts remain literal.515 plain G/U and the separately ruled quotient G/B remain occurrence-specific: the source maps are the fpqc sheaf quotient maps G→G/U and G→G/B, and G/U→G/B is the canonical projection. Typed product dots513–515 retain their explicit cdot transport for ideal multiplication and the bilinear K action, without a factor or order change.'
r.own_finding(id,511,'Local struck,plain and quotient glyphs;typed products','Attached matching forms','Retain the individually observed forms.',why,'Local notation511–515',kind='font',verdict='confirmed',witness=522);r.own[-1].update(is_misprint=False,source_pages=list(range(511,516)))
for p,a,b in [(511,'homomorphisme se factorise en:','f_*,défini car f est projectif.'),(512,'On a alors,d’après IV(2.12.4):','d’où en passant aux duaux la suite(3.3.1).'),(513,'Soit donc P un torseur sous V','pour a∈K_bullet(S) et'),(514,'b∈K^bullet(P(E)),on a','et J le lambda-idéal engendré'),(515,'par(E−n).Si f est le morphisme structural','défini par l’algèbre:')]:
 r.page(p,a,b,notes='Complete primary/native pages personally compared.512 ending and515 torus/index also read in full-resolution native details. Finding516_520#1–4 belongs to actual516 and is intentionally closed with that page. HOLD51 is actual515 and is now resolved.',witness=p+11)
r.commit()
