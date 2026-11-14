#!/usr/bin/env python3
"""Record the personally completed primary/native comparisons391–395."""
import re
from review_helpers import Review,base_text
r=Review();batch='391_395'
obs={
1:('P has two lower rules; each F has one','Both full391 images show the two P rules and the separate single F rules. The existing P rendering is retained under the recorded projective-functor typesetting decision; the single F rules are restored below. The projective notation identifies the same functor of invertible quotients by the identity on each quotient.','Top recursive construction',391),
2:('New paragraph at On voit alors','Both full391 images indent On voit alors after the short line ending X_(k−1). Retain the attached paragraph break.','After the structural morphism',391),
3:('Wide hat over K^bullet(S)[[t]], with plus outside','Both full391 images show the wide handwritten hat over the entire indicated series expression, and the plus to its upper right. Retain the attached span of the hat.','Additivity paragraph',391),
4:('New paragraph at Comme S est un quasi-compact','Both complete images indent this sentence after the second polynomial-identity display. Retain that paragraph and the source word un; its deletion is adjudicated separately.','After V2.4.2 formulas',391),
5:('Eight explicit theorem word groups','Both complete391 images show the groups restored below. The variables, lambda signs and adjacent hyphens have their separately inspected styles; the O has its own rule.','Théorème3.2',391),
6:('Occurrence-specific sheaf, torsor and coefficient rules','Every mathematical occurrence on the five complete primary/native image pairs was read. The individually recorded patches restore those rules. Plain E,F in K-classes are retained: the exact class map sends a sheaf E to cl(E), and exterior powers induce lambda^i(cl(E))=cl(wedge^i E). The one plain A in3.3 is kept diplomatically and has a separate current-only correction.','All mathematical text391–395',391),
7:('Both flag D operators have two rules','Both full392 images show two rules under each D and one under its E or F argument. Diplomatic restores the literal double rules; current retains the existing bold D, identifying the same flag functor by identity on each quotient flag.','Opening sentence',392),
8:('Wide hat over K^bullet(S)[[t]], plus outside','Both complete392 images repeat the same wide hat and external plus seen on391. The S is also clear; retain it. The cited universal identities are polynomial identities transported by the induced lambda-homomorphism on K under pullback.','Conclusion of proof3.2',392),
9:('Théorème3.3 without a final stop','Both full images have no stop after3.3. Diplomatic keeps the omission; current retains the supplied label stop, paired against the source.','Theorem label',392),
10:('Eleven explicitly inspected statement word groups','Both full392 images show the groups restored below. The phrase de rang borné sur T, punctuation, class K and the lambda/hyphen signs remain plain; the first A in (T,A) is independently ruled.','Théorème3.3',392),
11:('First group-scheme Gl has two lower rules','Both complete393 images show the two lines beneath Gl in this representation-ring argument. Diplomatic restores the literal two rules; current retains the existing bold letters, with the exact functor-of-points identification recorded below.','First R_Z(Gl(n))',393),
12:('Gl of the representation target paragraph has two rules','Both full393 images show the pair of lower rules. Apply the same explicit glyph transport as for the first occurrence, preserving n and every argument.','rho de Gl(n)',393),
13:('Final Gl of first paragraph has two rules','Both full393 images show the pair of lower rules in R_Z(Gl(n)). Restore them diplomatically.','End of first paragraph',393),
14:('Both Gl operators have two lower rules','Both complete393 images show both pairs of rules in the product group scheme. Preserve both n,p arguments and the product.','First product representation ring',393),
15:('Both last product Gl operators have two rules','Both full393 images show the same two pairs of rules in the last product representation ring. Restore exactly these occurrences diplomatically.','End of second paragraph',393),
16:('New paragraph at On est donc ramené','Both full393 images indent On est donc ramené after the preceding representation-ring sentence. The attached paragraph break matches.','Final paragraph opening',393),
17:('Thirteen singly ruled Gl sheaf operators','Both complete393 images show one rule under each of the nine Gl(n,A) and four Gl(p,A) names. Each A has its own rule. Restore these thirteen names separately from the seven double-rule group-scheme occurrences. The natural evaluation map is Gl_n(A(U))=GL_n(A(U)), compatible with restriction; the associated-bundle map sends [p,v] to p(v).','All Gl(n,A),Gl(p,A) occurrences',393),
18:('Plain paragraph number4.1.','Both complete394 images show4.1 with its stop in ordinary weight. Retain the stop and additionally restore the plain paragraph-number style.','Section4 first paragraph',394),
19:('Three baseline stops in p_1+...+p_i','Both complete394 images show three low typed stops between the plus signs. Retain the attached ldots.','Ranks of successive quotients',394),
20:('New paragraph at Un tel foncteur','Both full394 images indent this sentence after the line ending p_i. The attached break matches.','Representability paragraph',394),
21:('réprésentable','Both complete394 images print the initial acute accent. Diplomatic preserves it; current retains the recorded spelling correction représentable.','Representability paragraph',394),
22:('D_pi has two rules','Both full394 images show the pair under D and the separate rule under E. Diplomatic restores the pair.','First representing flag scheme',394),
23:('No punctuation follows the final three dots','Both full394 images end this paragraph with the three baseline stops after p_2 and no added sentence stop. Retain the attached absence.','End of canonical-quotients paragraph',394),
24:('New paragraph at Si pi=(r,n−r)','Both full394 images indent the Grassmannian specialization after the projective specialization. Retain the attached break.','Two specializations',394),
25:('D and P both have two rules','Both full394 images show the two double-rule operators and separately ruled E arguments. D receives its literal diplomatic rule rendering; the already recorded P transport is retained at this stage. Both names represent the identical functor of rank-one quotients in this displayed specialization.','Projective specialization',394),
26:('Both D and G have two lower rules','Both complete394 images show both pairs. Diplomatic restores the literal D,G rules; current retains the existing bold operators. The displayed comparison sends a two-step flag to its rank-r quotient, with inverse adjoining the fixed endpoints0 and E.','Grassmannian specialization',394),
27:('grassmanienne with one n','Both complete394 images print one n. Diplomatic retains it; current retains grassmannienne, the recorded spelling correction.','Grassmannian specialization',394),
28:('New paragraph at Si tous les p_i','Both full394 images indent this full-flag specialization. Retain the attached paragraph.','Full-flag specialization',394),
29:('D(E) has two lower rules','Both full394 images show both D rules and the separate E rule. Restore D literally in diplomatic.','Name of the usual complete-flag scheme',394),
30:('Three baseline stops in p_1+...+p_k=n','Both full394 images show three baseline stops. Retain the attached ldots.','Lemme4.2 hypothesis',394),
31:('D_pi(E) has two lower rules','Both complete394 images show the D pair and E single rule. Restore the pair diplomatically.','Lemme4.2 canonical quotients',394),
32:('Explicit lemma word groups','Both complete394 images show the groups restored below. The S-hyphen of S-isomorphisme, formulas, index labels, punctuation and commas remain independently styled.','Lemme4.2',394),
33:('Two double-rule D operators and a headless isomorphism','The display stands at the top of395, personally read in both complete images. Each D has two rules, E,F each one, and the isomorphism has a straight lower bar with no arrowhead. Diplomatic restores the literal D rules, with the existing simeq retained.','Top display of395',395),
34:('395 begins with the isomorphism display','Both complete394/395 pairs put the ending colon of4.2 on394 and its display on395. The attached marker precedes that display and is correct.','Boundary394/395',395),
35:('New paragraph at La démonstration','Both full395 images indent La démonstration after the display. The attached blank-line separation is correct.','Proof of4.2',395),
36:('Explicit lemma word groups on395','Both complete395 images show the word groups restored below. All letters of the ring presentation are plain; the A-/B-hyphens, commas, indices, roman item labels and punctuation are not included in the prose rules. The396 continuation is reviewed with that page.','Lemme4.3 on395',395),
37:('Three baseline stops in the monomial product','Both full395 images and the native395_comma crop show three low typed stops. Retain the attached ldots.','Part i monomial display',395),
38:('A comma follows the last monomial','The main scan loses the thin descending tail. The complete native395 image and the native395_comma crop preserve its head and tail. Retain the attached comma, with this witness-based reading explicitly recorded.','Part i monomial display ending',395),
39:('Two consecutive colons after relation','Both full395 images show two distinct colon pairs. Diplomatic retains both; current removes only the duplicate colon.','Part ii introduction',395),
40:('No punctuation after the last closing parenthesis','Both complete395 images show no following comma. The personally read primary396 top continues with the parenthetical weight assignment. Retain the attached absence of terminal punctuation. The identity itself has a separate mathematical adjudication.','Final display and396 continuation',395),
}
amended={6,7,11,12,13,14,15,18,22,25,26,29,31,33}
new={5,10,17,32,36,39}
for k,(p,w,g,f) in obs.items():
 r.finding(batch,k,p,w,g,witness=f+11,actual_page=f,
   verdict='amended' if k in amended else 'not applied and now applied' if k in new else 'confirmed')
for row in r.decisions:
 if row.get('kind')=='misprint_in_print' or row['type']=='misprint':row.update(is_misprint=True,correction_status='accepted paired correction')
for n,source,why in [(421,'en somme de classe de',
 'Both complete392 images print singular classe in the decomposition into a sum of the classes of the successive invertible quotient sheaves. The class map on the full flag is [E]=sum_j[L_j/L_(j−1)], with the specified multiple summands. Retain current classes and diplomatic classe.'),
 (422,'réprésentable',obs[21][1]),(423,'grassmanienne',obs[27][1])]:
 r.source(f'fixes/FIXLOG_6_CURRENT.jsonl#{n}',source,why,'Previously applied spelling correction',witness=403 if n==421 else 405)
 r.decisions[-1].update(is_misprint=True,correction_status='accepted paired correction')
why='Both full391 images print Comme S est un quasi-compact. The preceding theorem has already introduced S as a scheme; this substantival use retains that referent. Deleting un is an editorial language change without a source-determined misprint. Retain the author phrase in both layers.'
r.source('fixes/FIXLOG_6_CURRENT.jsonl#420','Comme S est un quasi-compact',why,'Final paragraph opening',verdict='reverted',change='Restore un in current.',witness=402)
r.decisions[-1].update(is_misprint=False,correction_status='Author language retained')
r.patch(391,'current',r'Comme \(S\) est quasi-compact',r'Comme \(S\) est un quasi-compact','fixes/FIXLOG_6_CURRENT.jsonl#420',why)
r.patch(395,'current','relation~::','relation~:',f'check/findings/findings_{batch}.json#39',obs[39][1])

def current(p,layer):
 t=base_text(p,layer)
 for x in r.patches:
  if x['page']==p and x['layer'] in ['both',layer]:
   assert t.count(x['old'])==x['expected_count'],(p,layer,x['source_id']);t=t.replace(x['old'],x['new'])
 return t
math_pattern=re.compile(r'\\\(.*?\\\)|\\\[.*?\\\]|\\begin\{equation\}.*?\\end\{equation\}|(?<!\\)\$(?!\$).*?(?<!\\)\$',re.S)
def letters(t,alphabet):
 counts={}
 def one(m):
  s=m[0]
  for c in alphabet:
   s,n=re.subn(rf'(?<![A-Za-z\\]){c}(?![A-Za-z])',lambda _:r'\underline{'+c+'}',s);counts[c]=counts.get(c,0)+n
  return s
 return math_pattern.sub(one,t),counts
for p in range(391,396):
 id=f'ASTRA-VI-GLYPHS-{p}'
 why='Restore only the personally inspected single lower rules on these occurrences; indices, powers and accents stay outside the letter rule. The mathematical relation between sheaf and class notation is the explicitly recorded Grothendieck class map.'
 if p==391:why+=' The four F_i/F_(k−1)/F_k occurrences at the top and the E,F sheaf occurrences in the proof are ruled. All E,F in the polynomial identities and introduced as elements of K stay plain.'
 if p==392:why+=' The opening E,F flag arguments, A of (T,A), both A in the proof, and the two E et F pairs and last E,F sheaf pair are ruled. The A immediately after des in the theorem is plain in the source and protected for its separate paired decision.'
 if p==393:why+=' Every A and torsor P is ruled. Every E is ruled apart from the two lambda^i(E) class arguments; F is ruled at E,F de rangs and réciproquement pour F, and plain in lambda^j(F).'
 if p==394:why+=' Every E,L,F on this page is ruled, including all quotient indices. Ordinary O has its observed single rule.'
 if p==395:why+=' Only E,F in the top display carry these rules. The A,B,C,xi,c,sigma,alpha symbols of4.3 remain exactly plain as observed.'
 r.own_finding(id,p,'Individually observed single-rule mathematical letters','Plain sheaf letters and script O','Restore the observed occurrence rules.',why,'Complete mathematical text',kind='font',witness=p+11)
 for layer in ['diplomatic','current']:
  old=current(p,layer);s=old.replace(r'\mathcal O',r'\underline{O}')
  if p==391:
   replacements=[(r'\(F_i\)',r'\(\underline{F}_i\)'),(r'F_{k-1}',r'\underline{F}_{k-1}'),(r'F_k=',r'\underline{F}_k='),
    (r'\cl(E)',r'\cl(\underline{E})'),(r'où \(E\)',r'où \(\underline{E}\)'),
    (r'de type fini \(E,F\)',r'de type fini \(\underline{E},\underline{F}\)'),(r'\(E\) et \(F\)',r'\(\underline{E}\) et \(\underline{F}\)')]
   for a,b in replacements:assert a in s,(p,a);s=s.replace(a,b)
   counts={'F_top':4,'E_sheaf':5,'F_sheaf_below':3}
  elif p==392:
   replacements=[(r'\mathbf D(E)',r'\mathbf D(\underline{E})'),(r'\mathbf D(F)',r'\mathbf D(\underline{F})'),
    (r'\((T,A)\)',r'\((T,\underline{A})\)'),(r'classes de \(A\)-Modules',r'classes de \(\underline{A}\)-Modules'),
    (r'les rangs de \(E\) et \(F\)',r'les rangs de \(\underline{E}\) et \(\underline{F}\)'),
    (r'lesquels \(E\) et \(F\)',r'lesquels \(\underline{E}\) et \(\underline{F}\)'),
    (r'-Modules \(E,F\) localement',r'-Modules \(\underline{E},\underline{F}\) localement')]
   for a,b in replacements:assert a in s,(p,a);s=s.replace(a,b)
   counts={'A':3,'E':4,'F':4}
  elif p==393:
   s=s.replace(r'\lambda^i(E)',r'\lambda^i(\SGAKeepE)').replace(r'\lambda^j(F)',r'\lambda^j(\SGAKeepF)')
   s,counts=letters(s,'AEPF');s=s.replace(r'\SGAKeepE','E').replace(r'\SGAKeepF','F')
  elif p==394:s,counts=letters(s,'ELF')
  else:s,counts=letters(s,'EF')
  assert s!=old;r.patch(p,layer,old,s,id,why)
 r.own[-1]['observed_rule_counts']=dict(counts,ordinary_O=old.count(r'\mathcal O'))

for p,cts in [(392,{'D':2}),(394,{'D':5,'G':1}),(395,{'D':2})]:
 id=f'ASTRA-VI-FLAG-OPERATORS-{p}'
 why='Both complete images show two separate lower rules on each named operator counted here. Diplomatic restores those two rules, and current retains the existing bold operators. Each notation transport is identity on the represented flag or rank-r quotient functor, and on all its pullback maps; the representing scheme comparison is therefore the induced identity.'
 r.own_finding(id,p,'Two lower rules on the listed flag operators','Bold operator letters','Literal two-rule operators in diplomatic; existing bold in current.',why,'All flag-scheme operators on page',kind='font',witness=p+11)
 for c,n in cts.items():r.patch(p,'diplomatic',r'\mathbf '+c,r'\underline{\underline{'+c+'}}',id,why,count=n)

id='ASTRA-VI-GL-OPERATORS-393'
why='Both full images show seven double-rule group-scheme Gl names and thirteen single-rule Gl(n,A)/Gl(p,A) names. For each object U the group-scheme evaluation is Gl_n(A(U))=GL_n(A(U)), with identical matrix multiplication and restriction maps. A frame p and vector v map to p(v), giving the contracted-product comparison [p,v]↦p(v) used by the source. Diplomatic retains the observed one/two rules; current retains bold group-scheme Gl and singly ruled group-sheaf Gl. No object or action is replaced.'
r.own_finding(id,393,'Seven twice-ruled Gl and thirteen singly ruled Gl','Bold group-scheme Gl and plain sheaf Gl','Restore literal double rules in diplomatic and single rules in both.',why,'All Gl operators',kind='font',witness=404)
r.patch(393,'diplomatic',r'\mathbf{Gl}',r'\underline{\underline{\operatorname{Gl}}}',id,why,count=7)
r.patch(393,'both',r'\GL(',r'\underline{\GL}(',id,why,count=13)
id='ASTRA-VI-TOPOS-COEFFICIENT-RULE-392'
why='Both full source images leave A in des A-Modules plain, while the theorem introduces the ruled A in (T,A), and the two proof occurrences have the rule. These modules carry exactly the action of that same ring object: the comparison is id_A:A→A, with restriction of scalars along id_A equal to the identical module/action. Current restores this one omitted rule; diplomatic keeps the plain glyph.'
r.own_finding(id,392,'Plain A in des A-Modules',r'des \(A\)-Modules','Current adds the single A rule only.',why,'Theorem3.3 definition of K',kind='misprint_in_print',witness=403)
r.own[-1].update(is_misprint=True,correction_status='accepted paired notation correction')
r.patch(392,'current',r'des \(A\)-Modules',r'des \(\underline{A}\)-Modules',id,why)

def rules(t,phrases):
 pat='(?<![A-Za-zÀ-ÿ])('+'|'.join(re.escape(s).replace(r'\ ',r'\s+') for s in sorted(phrases,key=len,reverse=True))+')(?![A-Za-zÀ-ÿ])'
 return re.sub(pat,lambda m:r'\uline{'+m[0]+'}',t)
word_groups={
391:['Soit','un schéma quasi-compact','Le pré','anneau','défini à partir des','-Modules localement libres de type fini','est un'],
392:['Soit','un topos commutativement annelé','on désigne par','le groupe de Grothendieck des','Modules localement libres','Alors','muni de sa pré','structure canonique','est','un','anneau'],
394:['Soient','un schéma','un','-Module localement libre de rang','avec','soient','deux entiers','tels que','posons',"les quotients canoniques de l'image inverse de",'sur','et soit','le noyau de','Alors on a un','isomorphisme canonique'],
395:['Soient','un anneau commutatif avec unité','un entier',"une famille d'éléments de",'soit','la','algèbre engendrée par des générateurs','soumis aux relations','où les','désignent les fonctions symétriques élémentaires','des entiers','de somme','et pour','avec','Posons','et soit','la sous-algèbre de','engendrée par les','Alors','les éléments de la forme','où','forment une base de','considéré comme','module','les générateurs','de la','algèbre','satisfont aux','relations isobares déduites de la relation']}
for p,phrases in word_groups.items():
 id=f'ASTRA-VI-WORD-RULES-{p}';why=obs[{391:5,392:10,394:32,395:36}[p]][1]
 r.own_finding(id,p,'Individually inspected statement word groups','Plain statement prose','Restore the exact visible word rules.',why,'Theorem or lemma statement',witness=p+11)
 for layer in ['diplomatic','current']:
  old=current(p,layer);label={391:'Théorème 3.2.',392:'Théorème 3.3',394:'Lemme 4.2.',395:'Lemme 4.3.'}[p]
  a=old.index(r'\textbf{'+label);a=old.index('}',a)+1
  b=old.index('\n\n',a) if p in [391,392] else len(old)
  s=old[:a]+rules(old[a:b],phrases)+old[b:]
  assert s!=old;r.patch(p,layer,old,s,id,why)
id='ASTRA-VI-PARAGRAPH-NUMBER-394';why=obs[18][1]
r.own_finding(id,394,'4.1. in ordinary weight',r'\subsection*{4.1.}','4.1.',why,'Paragraph opening',kind='font',witness=405)
r.patch(394,'both',r'\subsection*{4.1.}','4.1.',id,why)

ends={391:('pour tout i un O_Xi-Module','E et F de rang constant sur S.'),392:('Soit alors X=D(E)×_S D(F).','E,F localement libres de rang constant.'),393:('Soit E un A-Module localement libre de rang fini n.','en utilisant1.14.'),394:('4.Calcul du K^bullet d’un fibré de drapeaux','Alors on a un S-isomorphisme canonique:'),395:('D_pi-prime(E)≃D_pi-double-prime(F).','sum_i c_i=product_j(sum_i c_i^(j))')}
for p,(a,b) in ends.items():
 r.page(p,a,b,notes='Complete primary and native pages personally compared word by word and symbol by symbol. The native395 comma crop preserves the faint tail. The primary396 top was additionally read for the sentence boundary; its full-page comparison is separate.',witness=p+11)
r.commit()
