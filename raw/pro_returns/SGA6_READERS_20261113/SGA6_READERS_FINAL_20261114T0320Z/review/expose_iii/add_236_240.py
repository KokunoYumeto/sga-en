#!/usr/bin/env python3
import re,json
from review_helpers import Review,ROOT,base_text,underline_words
r=Review();batch='236_240'
obs={
1:('The first functor stays in the sentence','The complete236 page runs O_X tensor_Y^L dot=Lf* into the prose, before the separately displayed restricted functor. Retain the joined inline source.','Corollary1.13 opening functor',247),
2:('The inline functor closes before induit','The right endpoint D-minus(X) is followed by induit in the same sentence. The opening and closing transports are both retained.','Corollary1.13 inline close',247),
3:('A centered placeholder dot','Both scans place this dot above the baseline, at the tensor’s central height. Preserve cdot here; the baseline placeholder in235 is independently retained.','Corollary1.13 placeholder',247),
4:('Two indented roman-labelled cases','The words, two case labels, semicolon and final stop agree with the retained enumerate form. This is a layout transport, not an additional mathematical correction.','Theorem2.2 cases',247),
5:('Le théorème de finitude.','The heading ends with a stop after the title.','Section2 heading',247),
6:('Preuve dans le cas ruled; (i). plain','The lower rule ends after cas and leaves the parenthesized case number outside.','First proof label',None),
7:('Preuve dans le cas ruled; (ii). plain','The second label has the same separately inspected extent.','Second proof label',None),
8:('Ordinary typed P with r above and Y-prime below','The top vertex has one plain P, with independent superscript and subscript. No lower rule or doubled vertical is visible.','Top projective-space vertex',None),
9:('Ordinary typed P with r above and Y below','The left projective-space vertex uses the same ordinary P; its Y has no prime.','Left projective-space vertex',None),
10:('Inline j-prime_* Rf_*(E), ordinary R','Both scans keep the expression in the prose immediately before est pseudo-cohérent. Its R is the ordinary typed letter.','Opening reduction paragraph',249),
11:('Tilde over a headless horizontal stroke','Both complete scans show no arrowhead in the comparison j-prime_*Rf_*≃Rp-prime_*(ji)_*.','First displayed comparison',249),
12:('Ordinary typed P','The P in X=P_Y^r has the same plain contour as the projective-space labels on237.','Theorem2.2.2 first sentence',249),
14:('Three dots on the baseline','The dotted finite complex has three low dots between the two arrows. Preserve ldots and both terminal zeros.','Truncated complex E-prime',249),
16:('Pour cela continues the same paragraph','The line begins at the ordinary text margin, immediately below the full preceding line, with no paragraph indent or extra vertical separation.','Proof continuation after est parfait',250),
17:('Tilde over a headless horizontal stroke','The native witness clearly shows a separate wavy top and straight lower stroke, with no arrow tip, between the two complexes.','Displayed shifted higher direct image',250),
18:('Ordinary typed P','The printed projective-space P is ordinary, matching the P=P(F) glyph in the same corollary.','Corollary2.3 proof',251),
19:('No stop after the restricted Rf_* display','Both scans leave the display of Corollary2.4 without final punctuation; the final display of2.5 separately has a stop.','Corollary2.4 display end',251),
}
for k,(printed,reason,region,wit) in obs.items():r.finding(batch,k,printed,reason,region,witness=wit)
reason=('Both scans have R^qf_*(E)=0 with condition i>a+r. The preceding cohomological bound concerns the degree of that same higher direct image. '
        'In the displayed hypercohomology computation q is the total degree p+j; the source complex has j≤a and the r-dimensional projective-space cover gives p≤r, hence p+j≤a+r. '
        'The condition q>a+r selects exactly the vanishing total-degree terms. Current retains R^q and changes only the condition’s i to q; diplomatic retains the mismatched index.')
r.finding(batch,13,'R^qf_*(E)=0 pour i>a+r',reason,'Proof2.2.2 cohomological bound',verdict='amended',change='Retain current condition q>a+r, diplomatic i>a+r.',witness=249)
r.source('fixes/FIXLOG_6_CURRENT.jsonl#377','R^qf_*(E)=0 pour i>a+r',reason,'Proof2.2.2 cohomological bound',change='Retain current q>a+r.',witness=249)
reason=('The complete primary image has a faint short mark below the greater-than sign. The native witness251 and its enlarged proof crop show an ordinary > with only an isolated speck below; they do not show the complete horizontal rule in the nearby n≥N sign. '
        'Read > from the clearer witness and keep it in both layers. This agrees with the exact >a hypothesis repeated in2.3 and2.2.2; no alteration of a degree parameter is required. '
        'The earlier current reading is retained, but its classification as correction of a printed ≥ is withdrawn: the diplomatic transcription also becomes >.')
r.finding(batch,20,'Greater-than >; faint mark in the primary copy',reason,'Corollary2.3 proof degree bound',verdict='amended',change='Diplomatic ≥a→>a; current >a retained. Not a misprint of the printed mathematical text.',witness=251)
r.source('fixes/FIXLOG_6_CURRENT.jsonl#378','Greater-than > in the native witness',reason,'Corollary2.3 proof degree bound',verdict='amended',change='Retain the current reading; apply the same reading diplomatically.',witness=251)
r.patch(240,'diplomatic',r'\(\geq a\)',r'\(>a\)',f'check/findings/findings_{batch}.json#20',reason)
for row in r.decisions:
 if row.get('related_finding')==f'check/findings/findings_{batch}.json#20' or row['source_id'] in [f'check/findings/findings_{batch}.json#20','fixes/FIXLOG_6_CURRENT.jsonl#378']:row['is_misprint']=False
 if row.get('related_finding')==f'check/findings/findings_{batch}.json#13' or row['source_id'] in [f'check/findings/findings_{batch}.json#13','fixes/FIXLOG_6_CURRENT.jsonl#377']:row['is_misprint']=True
reason=('The restored triangle has the correct three vertices and arrows. Native witness250 shows a small curved tail immediately below the upper Rf_*(E-double-prime) vertex, not a transverse central bar. '
        'Replace the central marking by a curved hook at that arrow’s tail, preserving its E-double-prime→E-prime direction and the final stop. No [1] or degree interpretation is introduced.')
r.finding(batch,15,'Triangle with a curved tail at the upper vertex',reason,'Triangle(*) at top of239',verdict='amended',change='Retain triangle and final stop; use a hooked tail in place of the added central bar.',witness=250)
r.patch(239,'both',r'\arrow[dl,"|" marking]',r'\arrow[dl,hook]',f'check/findings/findings_{batch}.json#15',reason)
for page,count in [(236,1),(237,3),(238,2),(239,6),(240,4)]:
 id=f'ASTRA-III-STRUCTURE-{page}';why='Each structure sheaf on this personally inspected page is an ordinary typed O with an individual lower rule and an external index. The counted exact replacements reproduce those observed contours.'
 r.own_finding(id,page,'Ruled ordinary O',r'\mathcal O',r'\underline{O}',why,'All structure-sheaf occurrences',kind='font',witness=page+11 if page!=237 else None)
 r.patch(page,'both',r'\mathcal O',r'\underline{O}',id,why,count=count)
for page,count in [(238,2),(239,1)]:
 id=f'ASTRA-III-LCATEGORY-{page}';why=('The L, and only the L, in each named category L(X) has a visible lower rule in both scans. The references to II2.2.9 and II2.2.8 identify its objects as the finite direct sums used in the argument; the category itself and those object memberships are unchanged by restoring its printed rule.')
 r.own_finding(id,page,'Ruled L in L(X)','L(X)',r'\underline{L}(X)',why,'Category of finite sums of twists',witness=page+11)
 r.patch(page,'both','L(X)',r'\underline{L}(X)',id,why,count=count)

def current(page,layer):
 t=base_text(page,layer)
 for p in r.patches:
  if p['page']==page and p['layer'] in ['both',layer]:
   assert t.count(p['old'])==p.get('expected_count',1),(page,layer,p['source_id']);t=t.replace(p['old'],p['new'])
 return t

def rules(text,phrases):
 pat='(?<![A-Za-zÀ-ÿ])('+'|'.join(map(re.escape,sorted(phrases,key=len,reverse=True)))+')(?![A-Za-zÀ-ÿ])'
 return re.sub(pat,lambda m:r'\uline{'+m[0]+'}',text)
for page in [236,237,238,240]:
 id=f'ASTRA-III-WORD-RULES-{page}';why=('Every word rule was entered from the complete printed page; formulas, item labels and mathematical prefixes remain separate. '
       'In236’s Conjecture2.1, propre is visibly unruled between the ruled morphisme and de; that exception is retained. '
       'Proof labels are upright with the precise observed rule spans. These changes reproduce the author’s wording, including the original conjecture heading, without adding an assertion.')
 r.own_finding(id,page,'Observed upright statement word rules','Plain statements and italic proof labels','Restore the inspected word-group rules',why,'Statements and proof labels',witness=page+11 if page!=237 else None)
 for layer in ['diplomatic','current']:
  old=current(page,layer);new=old
  if page==236:
   b=new.index(r'\textbf{Remarque 1.14.1.}');s=rules(new[:b],['Dans la situation de','si','est pseudo-cohérent','on a','pour','en particulier','faisant','les notions de','pseudo-cohérence sur','au sens absolu','ou rel.','à','coïncident','le foncteur','induit','un foncteur','est','pseudo-cohérent','et','alors','Si'])
   new=s+new[b:]
   a=new.index(r'\textbf{Conjecture 2.1.}')+len(r'\textbf{Conjecture 2.1.}')
   s=rules(new[a:],['Soient','un schéma','un','morphisme','de schémas localement de type fini sur','Alors si','est pseudo-cohérent rel.','à','il en est de même de','La conjecture précédente est vraie dans les cas suivants','est localement noethérien','est projectif'])
   new=new[:a]+s
  elif page==237:
   a=new.index(r'\textbf{Théorème 2.2.1.}')+len(r'\textbf{Théorème 2.2.1.}');b=new.index(r'\emph{Preuve.}',a)
   s=rules(new[a:b],['Soit','un morphisme propre de schémas localement noethériens','et soit','Si les','sont cohérents','il en est de même des','Si en outre','est localement dans','il en est de même de'])
   new=new[:a]+s+new[b:]
  elif page==238:
   a=new.index(r'\textbf{Théorème 2.2.2.}')+len(r'\textbf{Théorème 2.2.2.}');b=new.index(r'\emph{Preuve.}',a)
   s=rules(new[a:b],['Soient','un schéma affine',"la projection d'un espace projectif type",'Alors','est pseudo-cohérent','En outre','si','est acyclique en degré','et il existe un entier','tel que','pour tout','où','soit acyclique en degré'])
   new=new[:a]+s+new[b:]
  elif page==240:
   for start,end in [(r'\textbf{Corollaire 2.3}',r'\emph{Preuve.}'),(r'\textbf{Corollaire 2.4.}',r'\emph{Preuve.}'),(r'\textbf{Corollaire 2.5.}',None)]:
    a=new.index(start)+len(start);b=new.index(end,a) if end else len(new)
    s=rules(new[a:b],['Soient','un schéma quasi-compact','et','un','morphisme projectif de schémas de type fini sur','le faisceau inversible défini par un plongement','où','est','Module quasi-cohérent de type fini','Pour','posons','Alors','si','est pseudo-cohérent rel.','à','acyclique en degré','il existe un entier','tel que','pour tout','vérifie les mêmes conditions','morphisme propre de schémas de type fini sur','Si','est noethérien ou si','est projectif','le foncteur','induit un foncteur','un morphisme propre et pseudo-cohérent','Supposons','localement noethérien ou','projectif','est pseudo-cohérent','au sens absolu','il en est de même de','est quasi-compact'])
    new=new[:a]+s+new[b:]
  new=new.replace(r'\emph{Preuve.}',r'\uline{Preuve}.');new,_=underline_words(new)
  assert new!=old,page;r.patch(page,layer,old,new,id,why)
r.page(236,'Corollaire1.12','(ii) f est projectif.',notes='All three corollaries, their bounded-degree signs, centered placeholder dot, original conjecture and the exact no-rule exception under propre were inspected; the active Ob macro expands to the observed small ob.',witness=247)
r.page(237,'Preuve dans le cas(i).','Commutative projective-space diagram, comma',notes='All three ruled structure sheaves, ordinary derived R symbols, the spectral sequence target R-star, r and N+r bounds, and all eight diagram edges including three hooks were compared.')
r.page(238,'où i,j,j-prime sont des immersions fermées','0→E-prime→E→E-double-prime→0,',notes='The first headless comparison, all three ob memberships, two ruled L category names, two ruled structure sheaves, q/i mismatch and low dots in the finite complex were directly inspected.',witness=249)
r.page(239,'où E-double-prime vérifie les mêmes conditions','pour références ultérieures :',notes='Full native page and enlarged triangle inspected: curved upper tail replaces the earlier central bar. All six ruled O letters, one ruled L category name, two bounds in t and the final shifted comparison were read.',witness=250)
r.page(240,'Corollaire2.3(EGAIII2.2.1)','Rf_*:D^b(X)_coh→D^b(Y)_coh.',notes='Full native page and enlarged proof compared: the uncertain primary inequality reads > in the witness, so both layers use >. Distinct final punctuation of2.4/2.5, every author reference and all four ruled O letters were checked.',witness=251)
r.commit()
