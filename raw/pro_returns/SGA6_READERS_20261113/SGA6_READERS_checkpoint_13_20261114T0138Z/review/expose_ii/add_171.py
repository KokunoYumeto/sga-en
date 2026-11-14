"""Folio171: definitions, base-change complement and literal underlines."""
import re
from review_helpers import Review,ROOT,underline_statement
r=Review()
r.finding('171_175',1,'cohérent définissant S−U begins the page',
    'The preceding folio ends quasi- and this one begins cohérent. Both attached layers already preserve the split-word marker.',
    'First printed line',change='Retain the existing quasi-/cohérent page boundary.')
r.finding('171_175',2,'on obtient un diagramme cartésien :',
    'The colon appears immediately before the Cartesian diagram. Both attached layers already include it.',
    'Proof of Lemma2.2.6, diagram introduction')
r.finding('171_175',3,'M. BORELLI et S.L. KLEIMAN',
    'Both surnames are full typed capitals in the complete author note. The attached uppercase words preserve them.',
    'Author note to famille ample')
reason='The print has Y′=X′−U. The displayed Cartesian square gives U′=U×_X X′, with projection g:X′→X; hence U′=g^{-1}(U) and Y′=g^{-1}(X−U)=X′−U′. This exact inverse-image identity justifies the already present prime in current; diplomatic retains the printed U.'
r.finding('171_175',4,'où Y′=X′−U.',reason,'Sentence immediately below the Cartesian diagram',change='Retain printed U diplomatically and the existing U′ in current.')
for source in ['fixes/FIXLOG_6_CURRENT.jsonl#349','fixes/RECONCILE_CODEX_6.json#233']:
    r.source(source,'Y′=X′−U in print',reason,'Cartesian base-change proof',page=171,change='Retain the existing corrected U′ and diplomatic U.')
sid=r.finding('171_175',5,'Statement words are underlined; famille ample and divisoriel are plain',
    'Every lexical group of the three statements on this folio was inspected, with the native witness resolving thin rules in Definition2.2.4. The defined terms and numbered references remain plain. In the parenthetical dimension equation of Lemma2.2.6, ou is also plain; the earlier codimension ou has a rule. This decision certifies page171 only, with later folios adjudicated separately.',
    'Definitions2.2.4 and2.2.5; Lemma2.2.6',verdict='not applied and now applied',change='Underline the inspected statement words, leaving defined terms, references and the inner dimension-equation ou plain.',witness=182)
sid_o='ASTRA-II-O-171';reason_o='All seven structure-sheaf O letters have individual rules, in Definition2.2.5, the lemma, the local spectrum and the three local-cohomology expressions. Scheme subscripts remain outside the rules.'
r.own_finding(sid_o,171,'Seven individually underlined structure-sheaf O letters',r'\mathcal O',r'\underline{O}',reason_o,'All seven O occurrences',kind='font')
r.patch(171,'both',r'\mathcal O',r'\underline{O}',sid_o,reason_o,7)
sid_note='ASTRA-II-NOTE-171';reason_note='The author call after famille ample and the label before Cette notion both have a raised star within baseline parentheses. The note body was read in full.'
r.own_finding(sid_note,171,'Parenthesized raised star at call and note',r'\footnote',r'\SGAAuthorFootnote{raisedstar}',reason_note,'Definition2.2.4 and page foot',kind='other',witness=182)
r.patch(171,'both',r'\footnote{Cette notion',r'\SGAAuthorFootnote{raisedstar}{Cette notion',sid_note,reason_note)
for layer in ['diplomatic','current']:
    old=(ROOT/f'build/page_packets/171/{layer}.tex').read_text()
    for p in r.patches:
        if p['layer'] in ['both',layer]:old=old.replace(p['old'],p['new'])
    new=old.replace(r'\emph{famille ample}','famille ample').replace(r'\emph{divisoriel}','divisoriel')
    # Each exact statement interval was read; the explicit author note is plain.
    a=new.index(r'\SGAAuthorFootnote{raisedstar}')
    b=new.index(' si les conditions',a)
    note=new[a:b]
    intervals=[]
    for label,start_word,endmark in [
        (r'\textbf{Définition 2.2.4.}','Soit ',r'\textbf{Définition 2.2.5.}'),
        (r'\textbf{Définition 2.2.5.}',"On dit ",r'\textbf{Lemme 2.2.6.}'),
        (r'\textbf{Lemme 2.2.6.}','Soit ',r'\emph{Preuve.}')]:
        start=new.index(start_word,new.index(label));end=new.index(endmark,start)
        intervals.append((start,end))
    protected=[re.escape(note),r'famille ample(?=\\SGAAuthorFootnote)',r'divisoriel',r'\(2\.2\.[34]\)',r'\(EGA II 4\.5\.3\)',re.escape(r'$\dim(\underline{O}_{X,x})=0$ ou $1$')]
    for start,end in reversed(intervals):
        new=new[:start]+underline_statement(new[start:end],protected)+new[end:]
    # The default math token takes precedence in the helper's alternation.
    # Restore the separately inspected plain connector after that exact unit.
    new=new.replace(r'$\dim(\underline{O}_{X,x})=0$ \uline{ou} $1$',r'$\dim(\underline{O}_{X,x})=0$ ou $1$')
    new=new.replace(r'\emph{Preuve.}',r'\uline{Preuve.}')
    r.patch(171,layer,old,new,sid,'Restore precisely the inspected lexical rules and plain exceptions; all mathematical units and the complete author note remain unchanged.')
r.page(171,'cohérent définissant S−U.','H^{n−1}(U′,O_{U′})=0,; author note ends par le rédacteur.',
    'The complete proof continuation, both definitions, lemma, Cartesian diagram, local-cohomology formulas and author note were compared. Native witness182 resolved the thin statement rules and plain defined terms.',witness=182)
r.commit()
