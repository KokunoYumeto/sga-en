"""Folio182: perfect-amplitude bound and the three derived-functor R forms."""
from review_helpers import Review,ROOT,underline_statement
r=Review()
for n,region in [(7,'Inline RΓ_S in item(c)'),(8,'Displayed RΓ_S in item(c)'),(9,'RΓ_S over the final arrow in proof(a)')]:
    r.finding('181_185',n,'The derived-functor R has a double underline',
        'The two lower strokes are visible at this occurrence. Both attached layers already use mathbb R. The earlier proof display has Γ_S alone, exactly as printed.',region)
reason='The print has membership i∈[m,n]. The proof on182 chooses E^i=0 for i>n; its directly inspected continuation on183 truncates to E^i=0 for i<m. The canonical map to the truncation preserves cohomology because perfect amplitude in[m,n] gives zero cohomology below m. Thus the displayed representative vanishes at every degree outside[m,n], which is the precise notin reading already present in current. Diplomatic retains the printed membership.'
r.finding('181_185',10,'F^i=0 pour i∈[m,n]',reason,'Proposition2.4.5(b)',change='Retain printed in diplomatically and the existing corrected notin.')
for source in ['fixes/RECONCILE_CODEX_6.json#248','fixes/FIXLOG_6_CURRENT.jsonl#356']:
    r.source(source,'F^i=0 pour i∈[m,n]',reason,'Proposition2.4.5(b)',page=182,change='Retain the existing corrected vanishing condition i∉[m,n].')
sid='ASTRA-II-UNDERLINE-182';reason='Every lexical group of the opening continuation and items(b),(c) has a rule, including both parenthetical essential-image descriptions. References, mathematical units and item controls remain independent. The proof body is plain except Preuve. These are the page182 occurrences of checker181–185#6.'
r.own_finding(sid,182,'Underlined statement continuation and both items','Plain statement prose',r'\uline on inspected lexical groups',reason,'Statement continuation through item(c), and proof heading',kind='underline')
for layer in ['diplomatic','current']:
    old=(ROOT/f'build/page_packets/182/{layer}.tex').read_text()
    start=old.index('\n')+1;end=old.index(r'\emph{Preuve.}')
    new=old[:start]+underline_statement(old[start:end],[r'\(I 4\.8\)'])+old[end:]
    new=new.replace(r'\emph{Preuve.}',r'\uline{Preuve.}')
    r.patch(182,layer,old,new,sid,reason)
r.page(182,'dont l’image essentielle est D^b(A)_coh','E^i∈ob Lib(S) pour i>m et E^i=0 pour i>n.',
    'All statement clauses, four displayed functor chains and the complete proof portion were compared. Native witness193 confirms the strict inequalities i>m and i>n on the last line. The first proof lines of183 were consulted to verify the explicit truncation underlying the already corrected amplitude condition.',witness=193)
r.commit()
