#!/usr/bin/env python3
import json,re
from review_helpers import Review,ROOT,base_text,underline_words
r=Review();batch='251_255'
obs={
1:('Page251 begins d’une immersion régulière','The complete native and primary pages start with d’une;250 ends composé. Retain the attached boundary.','Boundary250/251',262),
3:('Three baseline full stops','The finite complex in the proof has low dots after the arrow from E^{a+1}. No extra arrow is introduced before E^b.','Proof4.3 truncated complex',262),
4:('Headless tilde over a line','Both scans show a wavy upper stroke and a straight lower stroke without an arrowhead.','First g-alpha pullback comparison',263),
5:('Headless tilde over a line','The second comparison has the same headless sign. The already-adjudicated replay patch supplies this sign in current after the independent F-alpha argument repair.','Second g-alpha pullback comparison',263),
7:('Comma after the three-arrow triangle','The comma is visibly placed to the right of S. The horizontal i arrow has its curved hook, and the other two arrows end at S.','Proposition4.4 diagram',263),
9:('Conjuguer(1.11)et(3.4).','The native page shows the second1 tight against the closing parenthesis. Proposition1.11 is the earlier triangular-morphism tensor comparison; retain both printed digits.','Proof4.5 reference',264),
11:('Page255 begins qui achève la preuve','Both pages were read:254 ends ce, and255 begins qui achève la preuve de(ii)⇒(i). Retain the exact attached boundary.','Boundary254/255',266),
12:('Page255 ends after(I5.1.1),','The complete primary and native pages end with that comma. The following que E^a/B^a est h-plat belongs to256 and is not included in this page’s full-coverage claim.','End of255',266),
13:('Literal label t), without an opening parenthesis','Both scans show t) at the left of the first truncation arrow. Preserve this author label exactly; the later reference(t) names its symbol t.','First truncation label',266),
14:('Three low full stops','The first truncated complex has baseline dots between its two arrows.','First truncation complex',266),
16:('Headless tilde over a line','The fibre comparison has no arrowhead in either scan. Its ordinary i* is the termwise pullback of the previously chosen complex of locally free modules, so no additional derived L is transcribed.','Fibre comparison display',266),
19:('Literal i*(t) label, without outer parentheses','The second truncation label consists exactly of i*(t); the parentheses belong to t and no second pair surrounds the entire label.','Second truncation label',266),
20:('Three low full stops','The second truncated complex independently has baseline dots before the final displayed term i*(E^b).','Second truncation complex',266),
21:('toramp followed directly by i*(E)_x','The native page clearly places no parentheses around this argument. Preserve the author’s juxtaposition; keep the parentheses internal to i*(E).','Fibre-amplitude hypothesis after second truncation',266),
}
for k,(reading,why,region,wit) in obs.items():r.finding(batch,k,reading,why,region,witness=wit)
r.finding(batch,2,'No final stop after est un morphisme parfait','Both complete scans leave the completed sentence without a final stop, before the separate Notation4.2 paragraph. Retain that absence diplomatically and the current terminal stop.','Opening sentence',witness=262,change='Retain the existing diplomatic/current terminal-stop variant.')
why=('Both scans print g_alpha*(F) in the second comparison. The preceding definition binds F_alpha on X_alpha and the first comparison identifies g_alpha*F_alpha with F on X. '
     'On the affine charts Y_alpha=SpecA_alpha, Y=SpecA, write B_alpha=A_alpha[t1,…,tr] and B=A[t1,…,tr]=B_alpha tensor_Aalpha A. '
     'For the module N representing F_alpha, the pullback is B tensor_Balpha N. The explicit map (b tensor a) tensor n↦a tensor bn identifies it with A tensor_Aalpha N, with inverse a tensor n↦(1 tensor a) tensor n. '
     'The given A_alpha-flatness of N identifies the ordinary tensor with its derived tensor. Thus both sides of the printed comparison identify g_alpha*F_alpha, already identified with F, and the corrected argument is F_alpha. '
     'Keep the printed F diplomatically and retain the headless comparison sign in both layers.')
r.finding(batch,6,'g_alpha*(F) in the second comparison',why,'Proof4.3 second pullback argument',verdict='amended',change='Retain current F_alpha and diplomatic F; both signs remain headless.',witness=263)
r.source('fixes/FIXLOG_6_CURRENT.jsonl#381','g_alpha*(F)',why,'Proof4.3 second pullback argument',change='Retain the argument repair F_alpha, together with the separately resolved headless comparison.',witness=263)
why='Both scans have two opening parentheses in parfamp(i_*(E) but only the inner closing parenthesis. The outer argument is i_*(E), exactly as the second implication on the same page writes it. Retain the one-close print diplomatically and the two-close expression in current.'
r.finding(batch,8,'parfamp(i_*(E) with one closing parenthesis',why,'Proposition4.4(i)',change='Retain current second closing parenthesis.',witness=264)
r.source('fixes/FIXLOG_6_CURRENT.jsonl#382','parfamp(i_*(E) with one closing parenthesis',why,'Proposition4.4(i)',change='Retain current second closing parenthesis.',witness=264)
why='The primary and native254 pages show a stop after aussi, a lower-case d in d’après, and a closing parenthesis after4.3 with no opening parenthesis. The parenthetical citation concerns Proposition4.3’s displayed stalk-amplitude condition. Replace the stray stop by the missing opening parenthesis in current, preserving the existing close and comma; diplomatic retains the exact printed marks.'
r.finding(batch,10,'Elle entraîne aussi. d’après4.3),',why,'Proof4.6 first implication',verdict='amended',change='Current: Elle entraîne aussi(d’après4.3), with ordinary word spacing.',witness=265)
r.patch(254,'current',"Elle entraîne aussi. d'après 4.3),","Elle entraîne aussi (d'après 4.3),",f'check/findings/findings_{batch}.json#10',why)
why=('Both scans print s. The already defined map h sends x∈X to s∈S; E and the truncation morphism t are complexes on X. '
     'Condition4.6(i) is stated on an open neighbourhood U of x, and the reduction explicitly restricts along its open immersion j:U→X. '
     'The restriction j*E→τ_[a,b](j*E) is the truncation used in the proof: its stalks on U are the same truncations of E, and its being a quasi-isomorphism follows from the vanishing specified on U. '
     'This identifies the recalled neighbourhood as the neighbourhood of x from(i). Retain current x and diplomatic s; neither h nor any fibre point is renamed.')
r.finding(batch,15,'au voisinage de s',why,'Parenthetical explanation of truncation t',change='Retain current x, diplomatic s.',witness=266)
r.source('fixes/FIXLOG_6_CURRENT.jsonl#383','au voisinage de s',why,'Parenthetical explanation of truncation t',change='Retain current x, diplomatic s.',witness=266)
why=('The fibre comparison is visibly unlabelled in both scans; later the print says la flèche(*). The map used in that final paragraph is the original truncation t:E→T on X, '
     'where T^a=E^a/B^a, T^j=E^j for a<j≤b, and T is zero elsewhere. Its component in degree a is the quotient map, its higher components are identities, and its lower components are zero. '
     'The preceding assertion makes t a quasi-isomorphism. Tensoring t with an arbitrary h^{-1}O_S-module therefore identifies the cohomology used to test toramp_h(E) with that of T. '
     'The terms T^j for j>a are h-flat because they are locally free over O_X and h is flat. LemmaI5.1.1, with m=a,n=b,F=T and base h^{-1}O_S, then gives precisely the h-flatness of T^a claimed at the start of256. '
     'The intervening fibre comparison has objects over the residue fibre and supplies no such map E→T on X. Therefore repair the later reference(*) to(t), and remove the previously inserted(*) label from the headless fibre comparison. '
     'The printed t) and i*(t) labels themselves remain unchanged.')
r.finding(batch,17,'Unlabelled fibre comparison; later reference la flèche(*)',why,'Fibre comparison and final paragraph of255',verdict='amended',change='Current: remove the added(*) display label and change the final reference(*)→(t). Diplomatic retains the print.',witness=266)
r.patch(255,'current',r'i^*(E)_x.\tag{$*$}',r'i^*(E)_x.\notag',f'check/findings/findings_{batch}.json#17',why)
r.patch(255,'current',r"D'autre part, la flèche \((*)\)",r"D'autre part, la flèche \((t)\)",f'check/findings/findings_{batch}.json#17',why)
(ROOT/'review/expose_iii/truncation_reference_255.json').write_text(json.dumps(dict(source='check/findings/findings_251_255.json#17',print='Unlabelled fibre comparison; later(*)',current='Unlabelled fibre comparison; later(t)',identification=why,source_lemma='I5.1.1, folio131',next_conclusion='Folio256 opening: E^a/B^a est h-plat'),ensure_ascii=False,indent=2)+'\n')
r.finding(batch,18,'localiser,. with both comma and full stop','Both scans show the comma followed by a second typed stop. The continuation on peut supposer belongs to the same sentence. Retain the pair diplomatically and the current single comma. The partial overstruck fragments above this line are not transcribed as a new expression.','Sentence before second truncation',change='Retain the existing single comma in current.',witness=266)
mis={2,6,8,10,15,17,18}
for x in r.decisions:
 ids={x['source_id'],x.get('related_finding')}
 if any(f'check/findings/findings_{batch}.json#{k}' in ids for k in mis) or x['source_id'] in ['fixes/FIXLOG_6_CURRENT.jsonl#381','fixes/FIXLOG_6_CURRENT.jsonl#382','fixes/FIXLOG_6_CURRENT.jsonl#383']:x['is_misprint']=True
for page,count in [(251,2),(252,4),(254,7),(255,4)]:
 id=f'ASTRA-III-STRUCTURE-{page}';why='Each structure sheaf on both fully viewed scans has an ordinary typed O with its own lower rule. Restore these counted exact occurrences and keep their independently read indices.'
 r.own_finding(id,page,'Ruled ordinary O',r'\mathcal O',r'\underline{O}',why,'All structure sheaves',kind='font',witness=page+11)
 r.patch(page,'both',r'\mathcal O',r'\underline{O}',id,why,count=count)
id='ASTRA-III-AUTHOR-NOTE-254';why='Both scans have one raised parenthesized author call1 after the criterion title. The complete note invokes the fibrewise flatness criterion EGAIV11.3.10. Retain its wording and restore its original call number.'
r.own_finding(id,254,'Original author note1',r'\footnote with reader numbering',r'\SGAAuthorFootnote{1}',why,'Proposition4.6 title',kind='symbol',witness=265)
r.patch(254,'both',r'\footnote{',r'\SGAAuthorFootnote{1}{',id,why)

def current(page,layer):
 t=base_text(page,layer)
 for p in r.patches:
  if p['page']==page and p['layer'] in ['both',layer]:
   assert t.count(p['old'])==p['expected_count'],(page,layer,p['source_id']);t=t.replace(p['old'],p['new'])
 return t
def rules(text,phrases):
 pats=[re.escape(s).replace(r'\ ',r'\s+') for s in sorted(phrases,key=len,reverse=True)]
 pat='(?<![A-Za-zÀ-ÿ])('+'|'.join(pats)+')(?![A-Za-zÀ-ÿ])'
 return re.sub(pat,lambda m:r'\uline{'+m[0]+'}',text)
for page in range(251,255):
 id=f'ASTRA-III-WORD-RULES-{page}';why='All word-group rules were read on both complete scans. Only statement/proof-label spans are restored. The separately unruled plat in254 remains plain, and the notation paragraph251 remains plain apart from its already explicit mathematical parf rules.'
 r.own_finding(id,page,'Observed upright statement word rules','Plain statement prose and italic proof labels','Restore the inspected rules',why,'Statements and proof labels',witness=page+11)
 for layer in ['diplomatic','current']:
  old=current(page,layer);new=old
  if page==251:
   a=new.index(r'\textbf{Proposition 4.3}')+len(r'\textbf{Proposition 4.3}');b=new.index(r'\emph{Preuve.}',a)
   part=rules(new[a:b],['Soient','un morphisme localement de type fini de schémas','un intervalle de','un point de','Les conditions suivantes sont équivalentes','au voisinage de','est','pseudo-cohérent rel.','à','et acyclique en dehors de',"et l'on a"])
   new=new[:a]+part+new[b:]
  elif page==252:
   for heading in [r'\textbf{Corollaire 4.3.1.}',r'\textbf{Corollaire 4.3.2.}']:
    a=new.index(heading)+len(heading);b=new.index(r'\emph{Preuve.}',a)
    part=rules(new[a:b],['Soient','un morphisme localement de type fini','et','un','Module',"Pour qu'on ait",'il faut et il suffit que','soit','rel.','à','plat et de présentation finie','En particulier','pour que','soit de dimension parfaite nulle','soit plat et localement de présentation finie','un complexe de','Modules plats et de présentation finie','un intervalle de','Si','pour','on a','est à degrés bornés supérieurement','est pseudo-cohérent rel.'])
    new=new[:a]+part+new[b:]
   new=new.replace('Soit un triangle commutatif de schémas',r'\uline{Soit un triangle commutatif de schémas}',1)
  elif page==253:
   b=new.index(r'\emph{Preuve.}')
   part=rules(new[:b],['où','est une immersion fermée et','un morphisme lisse','et soit','Pour que','soit parfait rel.','à','il faut et il suffit que','soit parfait','au sens absolu','Plus précisément','supposons','de dimension relative','un intervalle de','On a alors'])
   new=part+new[b:]
   a=new.index(r'\textbf{Proposition 4.5.}')+len(r'\textbf{Proposition 4.5.}');b=new.index(r'\emph{Preuve.}',a)
   part=rules(new[a:b],['Soit','un triangle commutatif de morphismes localement de type fini de schémas','et soient','des intervalles de','On a alors','Par suite','si','est parfait rel.','à','et','parfait rel.'])
   # The et between the two displayed amplitude hypotheses has no rule.
   part=part.replace(r'\text{ \uline{et} }',r'\text{ et }')
   new=new[:a]+part+new[b:]
   a=new.index(r'\textbf{Corollaire 4.5.1.}')+len(r'\textbf{Corollaire 4.5.1.}')
   new=new[:a]+rules(new[a:],['Sous les hypothèses de','si','est de dimension parfaite','on a','par suite','est parfait','parfait rel.','à','implique'])
  elif page==254:
   b=new.index(r'\textbf{Remarque 4.5.2.}')
   new=rules(new[:b],['par suite','si','est parfait','parfait rel.','à','implique'])+new[b:]
   a=new.index(r'\textbf{Proposition 4.6}')+len(r'\textbf{Proposition 4.6}');b=new.index(r'\emph{Preuve.}',a)
   part=new[a:b];note=r'\SGAAuthorFootnote{1}{Analogue du «~critère de platitude par fibres~» (EGA IV 11.3.10).}'
   assert part.count(note)==1;part=part.replace(note,'@@AUTHORNOTE@@')
   part=rules(part,['critère de perfection par fibres','Soit','un triangle commutatif de morphismes de schémas','On suppose','localement de type fini','et','localement de présentation finie et','Soient','Enfin','soit','et soit','un intervalle de','On note','la fibre de','en','i.e.','le morphisme déduit de','par le changement de base','Alors les conditions suivantes sont équivalentes','au voisinage de'])
   part=part.replace('@@AUTHORNOTE@@',note);new=new[:a]+part+new[b:]
  new=new.replace(r'\emph{Preuve.}',r'\uline{Preuve}.');new,_=underline_words(new)
  assert new!=old,page;r.patch(page,layer,old,new,id,why)
r.page(251,'d’une immersion régulière','Quitte à plonger X dans un espace affine type sur Y,on peut',notes='Both scans read: five mathematical parf rules, otherwise plain notation paragraph, missing initial sentence stop, two ruled O letters, exact truncated-complex arrows and the explicit(a−1) bounds.',witness=262)
r.page(252,'supposer que X=Y[t1,…,tr]','Three-arrow triangle ending with comma',notes='Both headless comparisons, independent F/F-alpha reading, four ruled O letters, one plain L, both corollaries, all reference numbers and the hooked triangle were read. Existing replay7 remains linked to the second comparison.',witness=263)
r.page(253,'où i est une immersion fermée','parfamp_h(Lf*(F)) contained in[c−m,d];',notes='Missing outer parenthesis in4.4(i), plain et in4.5’s display, three ordinary derived L letters, all triangle arrows and the tightly typed reference1.11 compared.',witness=264)
r.page(254,'par suite,si f est parfait','Final derived tensor condition,ce; author note1 complete',notes='Both scans show plat without a word rule; all seven O letters have individual rules. Criterion title, full author note, triangular diagram, both conditions and the malformed citation punctuation read.',witness=265)
r.page(255,'qui achève la preuve de(ii)⇒(i).','implique,toujours d’après(I5.1.1),',notes='Both complete pages read: ordinary i* of the chosen locally free complex, four O rules, t)/i*(t) labels, baseline dots, original s, comma-stop pair, unlabelled headless comparison and the final mistaken(*) reference. The current reference is tied to the explicit original truncation map t.',witness=266)
r.commit()
