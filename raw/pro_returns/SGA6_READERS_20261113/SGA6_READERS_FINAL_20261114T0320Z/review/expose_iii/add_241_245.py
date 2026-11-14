#!/usr/bin/env python3
import json,re,hashlib
from review_helpers import Review,ROOT,base_text,underline_words
r=Review();batch='241_245'
obs={
1:('oeuvre with separate o and e','The complete primary and native pages show the two typed letters in mettre en oeuvre. Retain this exact spelling.','Scholie2.6',252),
3:('pour tout point, lower-case p','The printed second item starts with a small p.','Proposition3.3(ii)',253),
4:('pour tout objet, lower-case p','The third item independently starts with a small p.','Proposition3.3(iii)',253),
5:('même condition, lower-case m','The fourth item starts with the small m visible in both scans.','Proposition3.3(iv)',253),
6:('E|f^{-1}(V), restriction on the baseline','The restriction target follows the vertical bar on the same line; only the exponent −1 is raised.','First cohomology display',253),
7:('Tensor indexed by V','The lower index is V, not an expanded structure-sheaf expression. The independent upper L is plain.','First cohomology display tensor',253),
8:('E|f^{-1}(V), restriction on the baseline','The first restriction in the explanation repeats the same baseline notation.','Explanation after first display',253),
9:('First tensor indexed by V','The first tensor in the explanation has V below it, agreeing with the preceding display.','Explanation first tensor',253),
10:('Second restriction on the baseline; second tensor has no lower index','Both scans show E|f^{-1}(V), followed by a tensor with L above and no lower index, before Lf*(M).','Explanation second tensor',253),
11:('E|f^{-1}(V), restriction on the baseline','The lower comparison repeats this baseline restriction before the tensor.','Last displayed comparison',253),
12:('Tensor indexed by V','The lower comparison has V beneath its first tensor; the right-hand tensor has the separately printed structure-sheaf index.','Last displayed comparison tensor',253),
14:('Restriction target h^{-1}(Z-prime) on the baseline','The complete page shows the target after the vertical bar on the ordinary baseline. Both surrounding parentheses and the inverse-image exponent are retained.','Proof3.4 first cohomology display',None),
15:('Restriction target X-prime on the baseline','The first restriction in the associative comparison has X-prime on the baseline.','Proof3.4 comparison left member',None),
16:('E|X-prime on the baseline','The restriction after E has no lowered target.','Proof3.4 comparison middle factor',None),
17:('F|Y-prime on the baseline','The final restriction similarly keeps Y-prime on the baseline.','Proof3.4 comparison right factor',None),
18:('tor-dimension as one hyphenated word','The primary and native page show the ordinary internal hyphen, with no space after it.','Opening continuation of3.4.1(b)',255),
19:('Page245 begins catégorie dérivée','The last line of244 ends dans la; the complete native245 starts catégorie dérivée D(B) des B-modules. The attached marker already has the correct boundary.','Boundary244/245',256),
20:('Small ob in the six memberships on241–245','All six occurrences on these personally inspected pages have a small o. The scoped macro block now defines operatorname{ob}; retain that definition. The verdict concerns this macro and these read glyphs; later page records independently establish later usages, without an OCR-based page-coverage claim.','Scoped Ob definition after245',256),
}
for k,(printed,why,region,wit) in obs.items():r.finding(batch,k,printed,why,region,witness=wit)
r.finding(batch,13,'31 ordinary typed L letters across242–245','The complete primary pages and the native242,244,245 pages were inspected. The counts are7,7,8,9 respectively. Each L has the single typed stem and foot, with no lower rule or doubled contour. Retain all31 ordinary roman L letters.','Derived tensors and derived pullback symbols',witness=253)
r.finding(batch,2,'Individually ruled statement word groups, with unruled newly defined predicates in3.1','The exact spans on all five complete pages were read. Restore the observed upright word rules; leave the first d’amplitude plate relativement à f predicate, tor-dimension, and d’amplitude plate finie rel. à f unruled in3.1. Mathematical formulas and item labels retain their own glyph treatment.','Definitions, propositions and corollaries241–245',verdict='amended',change='Apply the five explicit page patches recorded as ASTRA-III-WORD-RULES-241 through245.',witness=252)
why=('The printed proof of2.5 cites2.5 itself. Corollary2.4 supplies the bounded derived functor under precisely the proper/projective or noetherian alternatives used here. '
     'Take the base S=Y locally on Y: the structure map of Y is id_Y, and f is pseudo-coherent. By1.12 the absolute pseudo-coherence of E is its relative pseudo-coherence over Y; '
     '2.2 transports that property through Rf_*, and2.4 gives the bounded restriction when Y is quasi-compact. On Y, relative pseudo-coherence over id_Y is the absolute property by the identity inverse-image map. '
     'Thus the middle citation is2.4, while2.2 and1.12 remain unchanged. Diplomatic retains the printed2.5.')
r.source('fixes/FIXLOG_6_CURRENT.jsonl#379','Conséquence de (2.2), (2.5) et (1.12).',why,'Proof of Corollary2.5',change='Retain current middle reference(2.4).',witness=252)
r.decisions[-1]['is_misprint']=True
why=('Both SGA6 scans print SGA4 XVII IV6.4. The personally viewed SGA4 tome1 re-edition page230, PDF236, has the ExposéIV header and Definition6.4.1: '
     'a conservative family of point fibre functors defines having enough points. This is the exact definition cited in3.3. '
     'For a module complex, the fibre functor sends H^i(E) to H^i(E_x), because the inverse-image fibre functor is exact; '
     'conservativity tests the isomorphism0→H^i(E) on these fibres. This identifies the cited criterion without changing any hypothesis or mathematical symbol. '
     'Retain IV6.4 in current and the full XVII IV6.4 diplomatically; source record external_sga4_242.json records the checked reference.')
r.source('fixes/FIXLOG_6_CURRENT.jsonl#380','SGA4 XVII IV6.4',why,'Proposition3.3 reference',change='Retain current SGA4 IV6.4.',witness=253)
r.decisions[-1]['is_misprint']=True
r.source('fr/codex/HOLD_VS_CORR.json#36','SGA4 XVII IV6.4',why,'Proposition3.3 reference; nominal HOLD page225, actual242',change='Accept the HOLD locator IV6.4 in current; retain the printed double chapter diplomatically.',witness=253,page=242)
r.decisions[-1]['is_misprint']=True

external=dict(source_url='https://www.cmls.polytechnique.fr/perso/laszlo/sga4/SGA4-1/sga41.pdf',
 source_file='build/external/sga4_tome1_laszlo.pdf',source_sha256=hashlib.sha256((ROOT/'build/external/sga4_tome1_laszlo.pdf').read_bytes()).hexdigest(),
 chapter='IV',section='6.4, especially Definition6.4.1',pdf_page=236,reprint_folio=230,original_margin_folio=389,
 personally_viewed_image='review/expose_iii/images/sga4_IV_6_4.png',observed='ExposéIV header;6.4.0 conservative families;6.4.1 definition of enough points by conservative fibre functors.',
 identification=why)
(ROOT/'review/expose_iii/external_sga4_242.json').write_text(json.dumps(external,ensure_ascii=False,indent=2)+'\n')

for page,count in [(241,4),(242,12),(243,1),(244,5)]:
 id=f'ASTRA-III-STRUCTURE-{page}';why='The complete page shows each structure sheaf as an ordinary typed O with an individual lower rule. Restore precisely these counted occurrences and retain their independent indices.'
 r.own_finding(id,page,'Ruled ordinary O',r'\mathcal O',r'\underline{O}',why,'All structure-sheaf symbols',kind='font',witness=page+11 if page!=243 else None)
 r.patch(page,'both',r'\mathcal O',r'\underline{O}',id,why,count=count)
id='ASTRA-III-AUTHOR-NOTE-241';why='The complete primary and native pages show one author note called by a raised parenthesized1. Preserve its full wording, including the literal theorem number1 and the Avril1971 addition, with that original call number.'
r.own_finding(id,241,'Raised parenthesized author call1 and complete note',r'\footnote with continuous reader numbering',r'\SGAAuthorFootnote{1}',why,'Scholie2.6 author footnote',kind='symbol',witness=252)
r.patch(241,'both',r'\footnote{',r'\SGAAuthorFootnote{1}{',id,why)

audit=json.loads((ROOT/'review/english/EN_INDEPENDENT_III_3_5_AUDIT_244_245.json').read_text())
audit['coordinator_scan_status']='Primary244–245 and native witness255–256 personally read in full; the printed assumptions, conclusion, stalk equations and proof agree with the tested passages.'
audit['editorial_handling']='Preserve the printed statement, proof and stalk equations in both French layers and both English branches. Record the demonstrated failures and exact comparison maps. The calculations supply no unique source-supported replacement text, so no new hypothesis or repaired theorem is inserted.'
(ROOT/'review/expose_iii/author_claim_244_245.json').write_text(json.dumps(audit,ensure_ascii=False,indent=2)+'\n')
why=('The printed3.5(a) uses relative amplitude for f1 and only cohomological concentration for E2. '
     'For S=SpecZ, X1=Y1=SpecFp, X2=Y2=S, identity f1,f2, E1=Fp and E2=Z/p in degree0, both Tor-independence pairs hold because their second member is S. '
     'The relative f1 amplitude of E1 is[0,0], and E2 is concentrated in[0,0]. Definition1.6 identifies the external tensor, via pr1=id and the unit multiplication, with Lpr2*(Z/p). '
     'The free resolution[Z --p→ Z] in degrees−1,0 pulls back to[Fp --0→ Fp], with H−1=Fp. This contradicts the printed conclusion for[0,0]. '
     'The same term appears in245’s proof as B tensor^L_B2 M2. Preserve the author’s statement and proof: this explicit calculation does not determine a unique printed-text correction. '
     'Full maps and the independent audit are in author_claim_244_245.json; no replacement hypothesis is added.')
r.own_finding('ASTRA-III-AUTHOR-CLAIM-244',244,'Proposition3.5(a) and its proof as printed','Same proposition and proof','Retain both layers; record explicit counterexample separately.',why,'Proposition3.5(a) and final proof sentence on245',kind='author_claim',verdict='confirmed',witness=255)
r.own[-1].update(is_misprint=False,correction_status='No unique source-supported replacement',supplemental_images=['scan/SGA6_scan_360dpi.pdf#page=259','scan/SGA6_witness_300dpi.djvu#page=256'])
why=('At a product point x the exact stalk map is R=A1 tensor_C A2→R_q=O_X,x, where q is the inverse image of the maximal ideal of O_X,x. '
     'On affine charts, localize the tensor ring first at the nonzero denominators from each projected local ring and then at q; localization transitivity gives that precise map. '
     'For k=Q, X1=X2=A1_k and x the generic point u=t, R=Q(t) tensor_Q Q(u) has distinct maximal ideals(u−t) and(u−t−1), since evaluation u=t and u=t+1 each gives Q(t). '
     'The element u−t−1 is a nonunit in R and becomes a unit in R_(u−t), proving that the displayed unlocalized equality for A fails. Identity f_i give the same example for B. '
     'For structural f_i to SpecQ, B1=B2=B=Q and the next displayed derived expression is R in degree0, while A is R_(u−t); it also lacks this localization. '
     'Preserve these printed formulas with their proof; changing only one equality would leave this second explicit mismatch. Exact maps and calculations are recorded in author_claim_244_245.json, without an invented repaired argument.')
r.own_finding('ASTRA-III-STALK-CLAIM-244',244,'A=A1 tensor_C A2; B=B1 tensor_C B2; ensuing derived equality','Same equalities','Retain both layers; record exact localizations and counterexample separately.',why,'Stalk definitions and final derived comparison',kind='author_claim',verdict='confirmed',witness=255)
r.own[-1].update(is_misprint=False,correction_status='No unique source-supported replacement')

def current(page,layer):
 t=base_text(page,layer)
 for p in r.patches:
  if p['page']==page and p['layer'] in ['both',layer]:
   assert t.count(p['old'])==p['expected_count'],(page,layer,p['source_id']);t=t.replace(p['old'],p['new'])
 return t
def rules(text,phrases):
 pat='(?<![A-Za-zÀ-ÿ])('+'|'.join(map(re.escape,sorted(phrases,key=len,reverse=True)))+')(?![A-Za-zÀ-ÿ])'
 return re.sub(pat,lambda m:r'\uline{'+m[0]+'}',text)
for page in range(241,246):
 id=f'ASTRA-III-WORD-RULES-{page}'
 why='Each word-group rule is entered from the complete printed page. Formula glyphs, plain case labels and the expressly unruled new predicates in3.1 remain independently typed. Proof labels become upright and ruled.'
 r.own_finding(id,page,'Observed upright word-group rules','Plain statement prose and italic proof labels','Restore the inspected rules',why,'Statements and proof labels',witness=page+11 if page!=243 else None)
 for layer in ['diplomatic','current']:
  old=current(page,layer);new=old
  if page==241:
   a=new.index(r'\textbf{Définition 3.1.}')+len(r'\textbf{Définition 3.1.}');b=new.index(r'\textbf{Notation 3.2.}',a)
   s=new[a:b]
   # The initial definition's new predicate remains plain. The explanatory
   # repetitions have independently observed rules.
   c=s.index('\nsi ')
   first=rules(s[:c],['Soient','un morphisme de topos annelés','un intervalle de',"On dit que",'est',"et l'on écrit"])
   rest=s[c:]
   d=rest.index("On dit que \\(E\\) est d'amplitude plate finie")
   mid=rules(rest[:d],['si','considéré comme complexe de','Modules',"est d'amplitude plate contenue",'dans',"On dit que",'ou de',"est d'amplitude plate",'rel.','à','contenue dans'])
   last=rules(rest[d:],["On dit que",'est',"s'il existe un intervalle","tel que l'on ait"])
   new=new[:a]+first+mid+last+new[b:]
  elif page==242:
   a=new.index(r'\textbf{Proposition 3.3.}')+len(r'\textbf{Proposition 3.3.}');b=new.index(r'\emph{Preuve.}',a)
   s=rules(new[a:b],['Les données étant celles de','supposons que','ait assez de points','Les conditions suivantes sont alors équivalentes','pour tout point','de','on a','où','est le point image de','par','annelé par','pour tout objet','et tout','Module','pour','même condition que','mais avec',"conoyau d'un homomorphisme"])
   new=new[:a]+s+new[b:]
  elif page==243:
   a=new.index(r'\textbf{Corollaire 3.4.}')+len(r'\textbf{Corollaire 3.4.}');b=new.index(r'\emph{Preuve.}',a)
   s=rules(new[a:b],['Soit','un triangle commutatif de topos annelés',"où l'on suppose que",'a assez de points','et soient','des intervalles de','On a alors'])
   new=new[:a]+s+new[b:]
   a=new.index(r'\textbf{Corollaire 3.4.1.}')+len(r'\textbf{Corollaire 3.4.1.}')
   new=new[:a]+rules(new[a:],['Sous les hypothèses de','si','est de tor-dimension','on a'])
  elif page==244:
   b=new.index(r'\textbf{Remarque 3.4.2.}')
   new=rules(new[:b],['si','est de tor-dimension','on a'])+new[b:]
   a=new.index(r'\textbf{Proposition 3.5.}')+len(r'\textbf{Proposition 3.5.}');b=new.index(r'\emph{Preuve.}',a)
   s=rules(new[a:b],['Soient','un schéma','et','pour','un','morphisme','un intervalle de','Supposons','ainsi que','tor-indépendants sur','Posons','Alors',"Si l'on a",'et si','est acyclique en dehors de','cf.','on a'])
   new=new[:a]+s+new[b:]
  elif page==245:
   a=new.index(r'\textbf{Corollaire 3.5.1.}')+len(r'\textbf{Corollaire 3.5.1.}');b=new.index('% Additions for Exposé III',a)
   s=rules(new[a:b],['Sous les hypothèses de','si','et','sont de tor-dimension finie','il en est de même de','Soit','un carré cartésien de schémas','où','sont supposés tor-indépendants sur','et soit','Alors on a','et par suite le foncteur','induit un foncteur'])
   new=new[:a]+s+new[b:]
  new=new.replace(r'\emph{Preuve.}',r'\uline{Preuve}.');new,_=underline_words(new)
  assert new!=old,page;r.patch(page,layer,old,new,id,why)
r.page(241,'Preuve. Conséquence de(2.2),(2.5)et(1.12).','c’est une sous-catégorie triangulée de D^b(X).',notes='Full author footnote with original1, four ruled O letters, small ob, all definition exceptions and the exact2.4 current reference identified.',witness=252)
r.page(242,'Proposition3.3','E_x tensor^L_{O_Y,y} M,',notes='All four items, twelve ruled O letters, seven plain derived L symbols, baseline restrictions and exact tensor indices read. The SGA4 locator was independently identified in IV6.4.1.',witness=253)
r.page(243,'d’après la commutation du produit tensoriel au passage aux fibres','toramp_h(E) contained in[a−n,b];',notes='Three-arrow triangle, both unbounded D memberships, all restrictions and seven plain L letters read. The display’s et is plain; the surrounding statement rules were individually checked.')
r.page(244,'b)si f est de tor-dimension≤m,on a','Par suite, le second membre de(*)est canoniquement isomorphe,dans la',notes='Five ruled O letters, eight plain L letters and every formula read in both scans. Proposition3.5(a) and the unlocalized stalk equalities are retained with exact counterexamples and comparison maps in the author-claim record.',witness=255)
r.page(245,'catégorie dérivée D(B)des B-modules','Lg*:D(f)_torf→D(f-prime)_torf.',notes='Full proof continuation, nine plain L letters, small ob, four arrows of the cartesian square, and both corollaries compared. No unprinted hypothesis or replacement proof inserted.',witness=256)
r.commit()
