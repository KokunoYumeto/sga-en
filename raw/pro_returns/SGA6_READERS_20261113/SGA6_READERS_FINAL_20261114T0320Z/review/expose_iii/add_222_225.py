#!/usr/bin/env python3
"""Personal full-page comparison of III222–225; exact observed spans."""
import json
from review_helpers import Review,ROOT,BYID,base_text,underline_words
r=Review();batch='221_225'
observations={
4:('Single-rule EXPOSÉIII; double-rule full capital title','Both complete images show the two distinct title-rule counts. The accented capital follows NOTE6.','Exposé title',233),
5:('par L.ILLUSIE, all underlined','The complete author line and its capitals agree in both scans.','Author line',233),
7:('Lowercase ob in1.1(ii), first membership','The native witness contrasts this small ob with capital Ob in(i) and(iii).','Item(ii), first ob',233),
8:('Lowercase ob in1.1(ii), middle membership','The second membership has the same two small letters; its alpha and fi_alpha indices are intact.','Item(ii), middle ob',233),
9:('Lowercase ob in1.1(ii), final membership','The final membership uses small ob, as the attached explicit ob macro renders.','Item(ii), last ob',233),
11:('pour chaque alpha∈A','Both alpha and membership in A are printed in the proof before the factorisation.','Proof, factorisation lead-in',233),
12:('Lowercase ob D(Y_alpha) in the proof','The witness has small ob in the final membership of222.','Last membership on222',233),
13:('unicité underlined','The word has a visible lower rule; L’ remains outside that rule. Apply the upright-word convention.','Proof, first sentence',233),
14:('223 begins est bien déterminée','The complete222 image ends with donc D(f)_{n-coh}; the first word of223 is est.','Boundary222/223',234),
15:('Lowercase ob D(X) in1.1.1','The lemma’s membership has two small letters.','Lemma1.1.1',234),
16:('Triangle E-double-prime above E-prime→E, with a transverse tick','The tick crosses the oblique E-double-prime→E-prime edge. The other edges are E-prime→E and E→E-double-prime. The attached triangle has this exact incidence and marks that edge; the linear shifted presentation is withdrawn.','First distinguished triangle',234),
17:('The same triangle after applying i_*','The three vertices are i_*(E-double-prime),i_*(E-prime),i_*(E); the transverse tick remains on the upper-to-left edge. Applying i_* sends each vertex and edge of the first triangle to the displayed corresponding vertex and edge.','Second distinguished triangle',234),
18:('A full stop after the second diagram, then D’après','The witness separates the diagram from the capitalised next sentence; no et is printed.','After second triangle',234),
20:('Headless tilde-over-rule isomorphism sign','Both scans show a horizontal rule with a tilde above and no head. The earlier replay repair supplies this sign; the separate index decision now retains the source n.','Final proof paragraph, Comme H^n',234),
22:('immersion régulière underlined','The two words have their own rule; the following VII1.4 reference remains plain.','Remark1.1.2',235),
25:('225 begins with Lemme1.1.4','The blank space at the foot of224 follows the complete proof sentence. The next page begins with the lemma label and its statement.','Boundary224/225',236),
26:('Both horizontal immersions have hooks at X','The left edge is X→X-prime and the right edge X→X-double-prime, each with its hook at the central source X. The native witness resolves both hooks.','Lemma1.1.4 first diagram',236),
27:('Lowercase ob D(X)','The membership in the statement has small ob.','Lemma1.1.4 statement',236),
29:('Both i and j have hooks at X','The triangle has i:X→Y, j:X→Z and f:Y→Z. Both outgoing edges at X visibly begin with hooks.','Triangle(*)',236),
30:('Hook at Y on i-prime:Y→Z[T_1,…,T_r]','The native witness resolves the curved tail; the vertical f and oblique projection f-prime are ordinary headed arrows.','Factorisation diagram',236),
31:('Comma level with bottom Z','The comma follows the diagram at the level of its lower vertex. The same level convention is present in the two preceding diagrams.','Factorisation diagram end',236),
}
for k,(printed,reason,region,witness) in observations.items():r.finding(batch,k,printed,reason,region,witness=witness)

reason=('The printed raised calls are1 after D(X) and2 inside the equivalence display before its stop. '
        'Use the existing explicit author-label macros for those exact two numerals; the display call is enclosed in mbox so it is not evaluated in four math styles. Both note texts are retained verbatim.')
r.finding(batch,10,'Raised call2 inside the display, before its stop',reason,'Theorem1.1(iii) display and both author notes',verdict='amended',change='Use explicit author calls1/2 at the printed positions.',witness=233)
id='ASTRA-III-NOTES-222'
r.own_finding(id,222,'Raised author calls1 and2','Automatic counter-based calls','Explicit source labels1/2',reason,'Theorem1.1 and footnotes',kind='author_footnote',witness=233)
r.patch(222,'both',r'\footnote{',r'\SGAAuthorFootnote{1}{',id,reason)
r.patch(222,'both',r'\mbox{\footnotemark}',r'\mbox{\SGAAuthorFootMark{2}}',id,reason)
r.patch(222,'both',r'\footnotetext{',r'\SGAAuthorFootText{2}{',id,reason)

reason=('The printed paragraph writes n in the last step of the stated descending induction. '
        'The same local perfect approximation u:P→i_*E has H^q(u) an isomorphism for q>n and an epimorphism at n; '
        'for every r≥n it is therefore an r-quasi-isomorphism, with the identical map u. '
        'Starting at the locally bounded-above index M, the displayed cone construction is repeated at r=M−1,…,n. '
        'At each r its last cohomology map is H^r(i_*E_r-double-prime)≃i_*H^r(E_r-double-prime); '
        'the finite generators pass through the surjection O_Y→i_*O_X to the same generators on X. '
        'I2.10(b) and I2.6 complete that r step. The paragraph as printed is precisely its final r=n instance. '
        'Thus all printed n occurrences already close the argument; replacing them with m is an unnecessary editorial relabelling. '
        'Restore the printed n in current, while deciding the missing closing parenthesis and headless sign separately.')
id='ASTRA-III-DESCENT-223'
r.own_finding(id,223,'n throughout the displayed last descent step','Current changed n to m in five chunks','Restore the printed n in those five chunks',reason,'Lemma1.1.1 descent proof',kind='reverted_prior_correction',verdict='reverted',witness=234)
for number in range(367,372):
    sid=f'fixes/FIXLOG_6_CURRENT.jsonl#{number}';d=BYID[sid]['data']
    r.source(sid,d['old'],reason,'Lemma1.1.1 descent proof',verdict='reverted',change='Restore printed n; retain the independently verified headless isomorphism sign.',witness=234)
    old=d['new'].replace(r'\xrightarrow{\sim}',r'\simeq ')
    new=d['old'].replace(r'\xrightarrow{\sim}',r'\simeq ')
    r.patch(223,'current',old,new,id,reason)

reason=('The first H^n expression has one closing parenthesis in both scans; its i_*(E-double-prime) argument opens two. '
        'The immediately following expression prints the identical composite H^n∘i_* with both closings. '
        'Add only the second closing parenthesis in current; keep the first expression’s literal missing close diplomatically.')
r.finding(batch,19,r'H^n(i_*(E-double-prime) with one close',reason,'First H^n expression in final paragraph',verdict='not applied and now applied',change='Current: close both the i_* argument and H^n argument.',witness=234)
for row in r.decisions:
    if row['source_id']==f'check/findings/findings_{batch}.json#19' or row.get('related_finding')==f'check/findings/findings_{batch}.json#19':row['is_misprint']=True
r.patch(223,'current',r"\(H^n(i_*(E'')\)",r"\(H^n(i_*(E''))\)",f'check/findings/findings_{batch}.json#19',reason)

reason=('Both scans show a short extra bar above i in the final parenthesis. The lemma and the entire proof specify the single immersion i:X→Y. '
        'The conclusion about finite generators uses its ring surjection O_Y→i_*O_X: at x the stalk (i_*M)_{i(x)} is M_x, '
        'and generators over O_{Y,i(x)} remain generators over its quotient O_{X,x}. '
        'This is exactly the same i_* as in the hypothesis i_*O_X; retain the visible bar diplomatically and the unbarred i in current.')
r.finding(batch,21,'A short bar above i in the final i_*O_X',reason,'Last parenthesis on223',change='Retain diplomatic barred i and current unbarred i.',witness=234)

reason=('The scan spells Kozsul. The regular-sequence complex described here has terms exterior^j(O_Y^r) '
        'and differential d(epsilon_j)=f_j for generators f_j of the immersion ideal; this is the Koszul resolution used in VII1.4. '
        'Retain the literal transposed spelling diplomatically and the established name Koszul in current.')
r.finding(batch,23,'Kozsul',reason,'Remark1.1.2, complex name',change='Retain diplomatic Kozsul; current Koszul.',witness=235)
r.source('fixes/FIXLOG_6_CURRENT.jsonl#372','Kozsul',reason,'Remark1.1.2, complex name',change='Retain current Koszul.',witness=235)

reason=('Both complete scans leave the first assertion unlabelled and explicitly label the next one(ii). '
        'The first assertion is the displayed base-change isomorphism; the following(ii) gives the pseudo-coherence conclusions. '
        'The position map sends these two complete assertions to1 and2 respectively, so adding(i) only names the already identified first position. '
        'No displayed map, hypothesis or conclusion needs an inserted token. Preserve the observed numbering in both layers under the content-preservation rule.')
r.finding(batch,24,'No(i) before la flèche; the second assertion starts(ii)',reason,'Lemma1.1.3 enumeration',verdict='not a misprint',change='Retain the first assertion without an added label.',witness=235)
for row in r.decisions:
    if row['source_id']==f'check/findings/findings_{batch}.json#24' or row.get('related_finding')==f'check/findings/findings_{batch}.json#24':row['is_misprint']=False

reason=('The right side prints only i-double-prime_* followed by the finiteness predicate, whereas the left is i-prime_*(E). '
        'The proof sends that same E through the two closed-immersion direct-image functors and then the diagonal factorisation. '
        'The object tested on the right is therefore the value i-double-prime_*(E); restore its omitted argument in current alone.')
r.finding(batch,28,'i-double-prime_* without its(E) argument',reason,'Lemma1.1.4 equivalence',change='Retain omitted(E) diplomatically; current i-double-prime_*(E).',witness=236)
r.source('fixes/FIXLOG_6_CURRENT.jsonl#373','i-double-prime_* without(E)',reason,'Lemma1.1.4 equivalence',change='Retain restored(E) in current.',witness=236)

for page,count in [(222,1),(223,3),(224,4)]:
    id=f'ASTRA-III-STRUCTURE-{page}'
    reason='Each inspected structure-sheaf O is an ordinary typed O with its own lower rule; the X or Y index lies below and outside that rule. Preserve the occurrence map, with no change to the attached subscripts.'
    r.own_finding(id,page,'Underlined typed O',r'\mathcal O',r'\underline{O}',reason,'Every structure-sheaf O on the page',kind='font',witness=page+11)
    r.patch(page,'both',r'\mathcal O',r'\underline{O}',id,reason,count=count)

def current(page,layer):
    text=base_text(page,layer)
    for p in r.patches:
        if p['page']==page and p['layer'] in ['both',layer]:
            assert text.count(p['old'])==p.get('expected_count',1),(page,layer,p['source_id'],text.count(p['old']))
            text=text.replace(p['old'],p['new'])
    return text

spans={
222:[('Soit ','Soit '),('Pour chaque morphisme localement de type fini de schémas','Pour chaque morphisme localement de type fini de schémas'),
('il existe une et une seule sous-catégorie pleine','il existe une et une seule sous-catégorie pleine'),(' de \\(D(X)\\)',' de \\(D(X)\\)'),
('telle que les conditions ci-dessous soient satisfaites','telle que les conditions ci-dessous soient satisfaites'),
('Si','Si'),('alors','alors'),('pour tout ouvert','pour tout ouvert'),
("et s'il existe un recouvrement ouvert","et s'il existe un recouvrement ouvert"),('tel que','tel que'),('pour tout','pour tout'),
('est un triangle commutatif de morphismes localement de type fini','est un triangle commutatif de morphismes localement de type fini'),
('où','où'),('est une immersion fermée et','est une immersion fermée et'),('un morphisme lisse','un morphisme lisse'),('alors on a','alors on a')],
}

# Whole-page exact transformations below specify only personally read prose spans.
for page in (222,223,224,225):
    id=f'ASTRA-III-STATEMENT-RULES-{page}'
    reason=('The complete page and native witness show upright underlined word groups. Formulas remain independently styled. '
            'On223 the continuous rule under soit n-pseudo-cohérent includes n; on224/225 the separate rule starts at pseudo after the plain n-. '
            'On224 la before flèche is plain. Statement labels and section titles retain the accepted NOTE6 typesetting.')
    r.own_finding(id,page,'Exact statement word-group rules','Statements mostly plain, selected terms italic','Upright source word rules with the observed formula boundaries',reason,'Theorem/lemma statement and proof labels',witness=page+11)
    for layer in ('diplomatic','current'):
        old=current(page,layer);new=old
        if page==222:
            a=new.index(r'\textbf{Théorème 1.1.}')+len(r'\textbf{Théorème 1.1.}')
            b=new.index(r'\emph{Démonstration.}')
            s=new[a:b]
            phrases=['Soit','Pour chaque morphisme localement de type fini de schémas','il existe une et une seule sous-catégorie pleine','telle que les conditions ci-dessous soient satisfaites',
                     'Si','pour tout ouvert',"et s'il existe un recouvrement ouvert",'tel que','pour tout','est un triangle commutatif de morphismes localement de type fini','où','est une immersion fermée et','un morphisme lisse','alors on a','alors']
            # Split the author-note payloads out before applying prose rules.
            import re
            alternatives=sorted(phrases,key=len,reverse=True)
            pattern='(?<![A-Za-zÀ-ÿ])('+'|'.join(map(re.escape,alternatives))+')(?![A-Za-zÀ-ÿ])'
            s=re.sub(pattern,lambda m:r'\uline{'+m[0]+'}',s)
            s=s.replace(r'\) de \(D(X)\)',r'\) \uline{de} \(D(X)\)')
            new=new[:a]+s+new[b:]
        elif page==223:
            a=new.index(r'\textbf{Lemme 1.1.1.}')+len(r'\textbf{Lemme 1.1.1.}')
            b=new.index(r'\emph{Preuve.}')
            s=new[a:b]
            phrases=['Soit','une immersion fermée de schémas telle que','soit pseudo-cohérent','et soit','Pour que',r'soit \(n\)-pseudo-cohérent','il faut et il suffit que','le soit']
            import re
            pattern='(?<![A-Za-zÀ-ÿ])('+'|'.join(map(re.escape,sorted(phrases,key=len,reverse=True)))+')(?![A-Za-zÀ-ÿ])'
            s=re.sub(pattern,lambda m:r'\uline{'+m[0]+'}',s)
            new=new[:a]+s+new[b:]
        elif page==224:
            a=new.index(r'\textbf{Lemme 1.1.3.}')+len(r'\textbf{Lemme 1.1.3.}')
            b=new.index(r'\emph{Preuve.}')
            s=new[a:b]
            phrases=['Soit un carré cartésien de schémas','où','est une immersion fermée','et soit','un complexe de','Modules','Alors','flèche canonique de changement de base','est un isomorphisme','Posons','Si','est plat et','pseudo-cohérent','alors','Inversement','si','est fidèlement plat et','est']
            import re
            pattern='(?<![A-Za-zÀ-ÿ])('+'|'.join(map(re.escape,sorted(phrases,key=len,reverse=True)))+')(?![A-Za-zÀ-ÿ])'
            s=re.sub(pattern,lambda m:r'\uline{'+m[0]+'}',s)
            new=new[:a]+s+new[b:]
        elif page==225:
            a=new.index(r'\textbf{Lemme 1.1.4.}')+len(r'\textbf{Lemme 1.1.4.}')
            b=new.index(r'\emph{Preuve.}')
            s=new[a:b]
            phrases=['Soit un diagramme commutatif de schémas','où','resp.','est une immersion fermée','et soit','et','un morphisme lisse','On a alors']
            import re
            pattern='(?<![A-Za-zÀ-ÿ])('+'|'.join(map(re.escape,sorted(phrases,key=len,reverse=True)))+')(?![A-Za-zÀ-ÿ])'
            s=re.sub(pattern,lambda m:r'\uline{'+m[0]+'}',s)
            s=s.replace(r'n\text{-pseudo-cohérent}',r'n\text{-\uline{pseudo-cohérent}}')
            new=new[:a]+s+new[b:]
        new=new.replace(r'\emph{Démonstration.}',r'\uline{Démonstration}.').replace(r'\emph{Preuve.}',r'\uline{Preuve}.')
        new,_=underline_words(new)
        assert new!=old,page
        r.patch(page,layer,old,new,id,reason)
r.finding(batch,6,'Exact word-group statement rules on222–225','All four pages and their native witnesses have been read. The recorded per-page transformations preserve mathematical tokens, source-specific underlining of n, plain la on224, and unruled references.','Theorem1.1 and Lemmas1.1.1/1.1.3/1.1.4',verdict='not applied and now applied',change='Apply the four exact statement-rule maps in both layers.',witness=233)

id='ASTRA-III-EGA-224'
r.own_finding(id,224,'EGAIII1.4.15.4','Same reference','Retain the printed reference',
 'The original EGAIII page93 display1.4.15.4 was visually read. Under u=i,v=g,v-prime=f,u-prime=i-prime,q=0 it is exactly g*i_*E→i-prime_*f*E, degree by degree. On affine pieces A→A/I and A→B the map is b⊗m↦(b mod IB)⊗m from B⊗_A M to (B/IB)⊗_(A/I)M, with inverse induced by the same representatives. See external_ega_224.json.',
 'Lemma1.1.3 base-change reference',kind='reference_confirmation',verdict='confirmed',witness=235)

r.page(222,'EXPOSÉIII','donc D(f)_{n-coh}',notes='Both native author notes, every Ob/ob, the theorem triangle and the factorisation were inspected.',witness=233)
r.page(223,'est bien déterminée','indépendant de l’hypothèse sur barred-i_*O_X',notes='Both native triangles, transverse ticks, n indices, single missing parenthesis, headless sign and final bar were inspected. Unnecessary current n→m editorial changes are withdrawn.',witness=234)
r.page(224,'Remarque1.1.2','L’assertion se vérifie trivialement sur les fibres.',notes='Native word rules, plain la and n- prefixes, four structure O rules, square and exact EGA reference inspected. The unlabelled first assertion remains unlabelled.',witness=235)
r.page(225,'Lemme1.1.4','si et seulement si i-prime_*(F) l’est.',notes='All five hooks, diagram punctuation, native predicate-rule boundaries, missing right(E), star tag and complete proof were inspected. HOLD36 belongs to actual242 and remains for that page.',witness=236)
r.commit()

# Keep the earlier replay’s historical anchor and update its resulting reading.
p=ROOT/'review/middle/decisions.jsonl';rows=[json.loads(s) for s in p.read_text().splitlines()]
for row in rows:
    if row['source_id']=='fixes/REPLAY_MANUAL_6.json#6':
        row['change']='Current uses the printed headless sign; ExposéIII retains the printed exponent n.'
        row['reason']='The scan prints a tilde over a rule without a head. The replay first matched the inherited m exponent; the later independently justified ExposéIII descent decision restores printed n. These two exact patches compose in that order.'
p.write_text(''.join(json.dumps(x,ensure_ascii=False)+'\n' for x in rows))
