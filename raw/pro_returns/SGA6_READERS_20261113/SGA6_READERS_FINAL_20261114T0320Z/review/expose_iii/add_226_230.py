#!/usr/bin/env python3
import re
from review_helpers import Review,ROOT,base_text,underline_words
r=Review();batch='226_230'
observations={
1:('spécial has its own lower rule','Both scans underline just the defined word, leaving its surrounding parenthesis and pour abréger plain.','Definition of spécial',237),
2:('Preuve de and fin separately underlined','The number1.1 and the parentheses have no rule. Preserve the exact two spans in upright type.','Proof continuation label',237),
4:('Lowercase ob in(A)','The complete227 image shows small ob. The active ExposéIII macro also gives small ob for the later occurrences on228/229; the explicit operatorname form at227 is identical in output.','Statement(A) membership',None),
6:('Unprimed i_{2*}(E) in the final conclusion','Both scans show unprimed i_2 in that last sentence. Its domain X_2 and target Y_2 agree with(A); the intermediate i-prime_2 has target X-prime_2 and remains primed in the preceding steps.','Proof(A), final conclusion',239),
7:('On dira que f follows the preceding definition on the same line','The first line of229 contains the end of the previous sentence followed directly by On. Retain the attached continuous paragraph; this is an observed layout boundary.','Definition1.2 continuation',240),
8:('230 begins(-1)-pseudo-cohérent','The bottom of229 ends dire que f est. The complete next page begins with the entire parenthesized index and predicate. The marker is already in that position.','Boundary229/230',241),
9:('Triangle E→F→G→E, G above','The native witness shows three headed edges with no transverse tick and no written[1]. Keep the exact triangle incidence.','Proposition1.4 triangle',241),
10:('The corresponding triangle after applying f_*','Its upper vertex is f_*(G); the lower edge is f_*(E)→f_*(F). The other two edges are f_*(F)→f_*(G) and f_*(G)→f_*(E), again without a tick.','Proposition1.4 proof triangle',241),
11:('Comma level with f_*(F)','The comma stands at the lower-vertex level to the right of the triangle. Retain the attached comma.','Proof triangle end',241),
12:('One lower rule under displayed Tor','The native crop shows a rule under Tor, while i and S are independent indices. The source Tor macro is an ordinary operator; its one explicit wrapper supplies exactly this rule.','Definition1.5 Tor display',241),
13:('One lower rule under the second Tor','This rule is distinct from the word rules under les and étant les hyper-tor locaux définis dans. Preserve all three spans.','Definition1.5 final sentence',241),
15:('230 ends(EGAIII6.5).;231 begins C’est une','The complete230 image and the independently viewed top of231 fix the boundary exactly. The existing marker precedes C’est une.','Boundary230/231',241),
}
for k,(printed,reason,region,wit) in observations.items():r.finding(batch,k,printed,reason,region,witness=wit)
reason=('The top edge of(a-prime) visibly bears i-double-prime. The immediately following text specifies i-prime:X-prime→Y-prime and its functor i-prime_*p-prime*; the next page’s cube gives this same edge i-prime. '
        'The second diagram(a-double-prime) has a different edge X-double-prime→Y-double-prime named i-double-prime. '
        'The endpoint-preserving identification of the first edge with the first prose immersion therefore supplies i-prime. Retain i-double-prime diplomatically and the existing i-prime correction in current.')
r.finding(batch,3,'i-double-prime above X-prime→Y-prime',reason,'Diagram(a-prime)',change='Retain diplomatic double prime and current single prime.',witness=237)
r.source('fixes/FIXLOG_6_CURRENT.jsonl#374','i-double-prime',reason,'Diagram(a-prime), top edge',change='Retain current i-prime.',witness=237)

reason=('Both scans show ruled O_X and unruled O_Y. The next page explicitly identifies the affine rings of X,Y,S as B,C,A and the same tensor map B tensor^L_A C→B tensor_A C. '
        'Its two sheaf arguments are the structure sheaves with sections B and C; O_Y here is that same structure sheaf of Y, with no changed module or ring map. '
        'Keep the isolated missing rule in the diplomatic form and the established structure-sheaf rule in current.')
r.finding(batch,14,'Underlined O_X, plain O_Y',reason,'Definition1.5 Tor arguments',change='Diplomatic retains plain O_Y; current retains ruled O_Y.',witness=241)

for page,layer,count in [(229,'both',4),(230,'diplomatic',1),(230,'current',2)]:
    id=f'ASTRA-III-STRUCTURE-{page}'
    reason='The personally inspected structure-sheaf letters are ordinary typed O with their own rules and external indices. On230 only the diplomatic Y argument remains unruled, as separately adjudicated from both native scans.'
    if not any(x['source_id']==id for x in r.own):
        r.own_finding(id,page,'Exact underlined O occurrence map',r'\mathcal O',r'\underline{O}',reason,'All structure-sheaf occurrences',kind='font',witness=page+11)
    r.patch(page,layer,r'\mathcal O',r'\underline{O}',id,reason,count=count)

def current(page,layer):
    text=base_text(page,layer)
    for p in r.patches:
        if p['page']==page and p['layer'] in ['both',layer]:
            assert text.count(p['old'])==p.get('expected_count',1),(page,layer,p['source_id'])
            text=text.replace(p['old'],p['new'])
    return text

def rules(text,phrases):
    pats=[re.escape(s).replace(r'\ ',r'\s+') for s in sorted(phrases,key=len,reverse=True)]
    pat='(?<![A-Za-zÀ-ÿ])('+'|'.join(pats)+')(?![A-Za-zÀ-ÿ])'
    return re.sub(pat,lambda m:r'\uline{'+m[0]+'}',text)

for page in range(226,231):
    id=f'ASTRA-III-WORD-RULES-{page}'
    reason=('The rules are entered from the complete source page, with native crops for the definition boundaries. '
            'On228 the first two newly defined predicates and their relatively-to-f phrases remain plain; only the third pseudo-cohérent and its relativement à have rules. '
            'On229 the continuation’s observed word groups have rules, while mathematical letters, parentheses and quotation marks remain independent. '
            'On230 S and its following hyphen remain plain before ruled schémas; pour in the Tor display is independently ruled. '
            'The rule under un carré commutatif de schémas on227 spans a source line break after un; that whitespace is retained inside the exact rule span.')
    r.own_finding(id,page,'Observed upright word rules','Mostly plain statement prose or selected italic words','Apply only the inspected word-group rules',reason,'Statements, definitions and proof labels',witness=page+11 if page in [226,228,229,230] else None)
    for layer in ['diplomatic','current']:
        old=current(page,layer);new=old
        if page==227:
            a=new.index('(A) :');s=new[a:]
            s=rules(s,['un carré commutatif de schémas','où','est un morphisme spécial','un morphisme lisse','et','des immersions fermées','et soit','Alors','pour que','soit','pseudo-cohérent','il faut et il suffit que','le soit'])
            new=new[:a]+s
        elif page==228:
            a=new.index(r'\textbf{Définition 1.2.}')+len(r'\textbf{Définition 1.2.}');s=new[a:]
            s=rules(s,['Soient','un morphisme localement de type fini','On dira que','est','si','ou encore','pour tout','On notera','la sous-catégorie'])
            # Only the third occurrence is a ruled predicate in this definition.
            anchor=r'\(n\)-pseudo-cohérent relativement à \(f\) pour tout'
            # The earlier word-group pass has already ruled pour tout.
            anchor=anchor.replace('pour tout',r'\uline{pour tout}')
            assert s.count(anchor)==1
            s=s.replace(anchor,r'\(n\)-\uline{pseudo-cohérent relativement à} \(f\) \uline{pour tout}')
            new=new[:a]+s
        elif page==229:
            b=new.index(r'\textbf{Remarques 1.2.1.}');s=new[:b]
            s=rules(s,['pleine de','formée des objets pseudo-cohérents relativement à','On dira que','est','pseudo-cohérent','resp.','si','relativement à','On dira parfois','quand cela ne pourra prêter à confusion','au lieu de',"et l'on écrira aussi",'Enfin pour','on posera'])
            new=s+new[b:]
        elif page==230:
            a=new.index(r'\textbf{Proposition 1.4.}')+len(r'\textbf{Proposition 1.4.}');b=new.index(r'\emph{Preuve.}')
            s=rules(new[a:b],['Soit','un morphisme localement de type fini','et soit','un triangle distingué de','On a alors le tableau suivant','où','indique un degré de pseudo-cohérence par rapport à','et chaque ligne représente une implication dont le but est souligné','En particulier','est une sous-catégorie triangulée de'])
            new=new[:a]+s+new[b:]
            a=new.index(r'\textbf{Définition 1.5.}')+len(r'\textbf{Définition 1.5.}');s=new[a:]
            s=rules(s,['Soient','et','deux','schémas','Nous dirons que','sont tor-indépendants sur',"si l'on a",'les','étant les hyper-tor locaux définis dans'])
            s=s.replace(r'\text{pour }',r'\text{\uline{pour} }')
            new=new[:a]+s
        new=new.replace(r'\emph{Preuve.}',r'\uline{Preuve}.')
        new,_=underline_words(new)
        assert new!=old,page
        r.patch(page,layer,old,new,id,reason)
r.finding(batch,5,'Occurrence-specific statement word rules on227–230','The full pages and native228/229/230 definitions were compared. The five page transformations record the exact word groups, including plain newly defined predicates on228 and the different ruled occurrences that follow.','Statement(A), Definition1.2, Proposition1.4 and Definition1.5',verdict='not applied and now applied',change='Apply explicit word-group maps in both layers.',witness=239)

r.page(226,'On peut donc supposer que Y=Z[T_1,…,T_r]','Soit donc',notes='Every word and ring-map symbol compared; native i-double-prime in(a-prime), both bare coproducts, sigma/epsilon maps and proof-label rules inspected.',witness=237)
r.page(227,'Diagram(a-double-prime)','le soit.',notes='Both factorisation diagrams, all twelve cube edges and their three horizontal hooks, and the statement(A) square were compared with the printed endpoints, arrowheads and labels. Small ob and predicate rules confirmed.')
r.page(228,'Preuve de(A).','la sous-catégorie',notes='All three hooks and the curved unhooked i_2 arrow inspected; the final i_2 lacks a prime. Native definition crop fixes plain/ruled predicate occurrences.',witness=239)
r.page(229,'pleine de D(X)','En particulier, dire que f est',notes='Full native page inspected: four ruled O letters, both intersections and punctuation, continuation word rules, all three remarks and exact rel. abbreviations retained.',witness=240)
r.page(230,'(-1)-pseudo-cohérent équivaut','définis dans(EGAIII6.5).',notes='All nine table entries and exactly three ruled targets, both unmarked triangles, both Tor rules, plain diplomatic O_Y and the next-page boundary were inspected.',witness=241)
r.commit()
