"""Folio183: separate the two printed functor clauses by their exact maps."""
from review_helpers import Review,ROOT,underline_statement
r=Review()
reason11='The printed Loclib(S)) has one closer beyond the completed category expression. Current already removes that unmatched closer; diplomatic retains it.'
r.finding('181_185',11,'E^m∈ob Loclib(S))',reason11,'First proof sentence',change='Retain the printed excess diplomatically and its existing current removal.')
for source in ['fixes/RECONCILE_CODEX_6.json#249','fixes/FIXLOG_6_CURRENT.jsonl#357']:
    r.source(source,'E^m∈ob Loclib(S))',reason11,'First proof sentence',page=183,change='Retain the existing corrected removal of the unmatched closer.')
reason12='The first displayed functor j:K^b(Loclib(S))→D(S) and its image D(S)_parf remain unchanged. The later sentence expressly uses Γ_S. Degreewise sections define T:K^b(Loclib(S))→K^b(Mod(A))→D(A). The theorem-B acyclicity of the locally free coherent terms gives the canonical comparison T≃RΓ_S∘j. Thus the named second functor has the A-module target used in the directly inspected statement2.4.5(c), and current restores A only in this second clause.'
sid=r.finding('181_185',12,'The second functor is printed K^b(Loclib(S))→D(S), induit par Γ_S',reason12,
    'Second functor clause of proof(c)',verdict='not applied and now applied',change='Current changes this second target to D(A); retain the earlier D(S) target and all diplomatic readings.')
r.patch(183,'current',r'le foncteur $\mathrm K^b(\Loclib(S))\to\mathrm D(S)$ induit',r'le foncteur $\mathrm K^b(\Loclib(S))\to\mathrm D(A)$ induit',sid,'Use the explicit target of the degreewise-global-sections composite T, preserving the preceding sheaf-derived target.')
reason13='The essential-image phrase belongs to the same second functor T=Γ_S on bounded locally free complexes. Under the comparison T≃RΓ_S∘j, the proposition2.4.5(c) on182 identifies its image as D(A)_parf. The earlier image D(S)_parf belongs to j and stays unchanged. Current restores A only in the last image phrase.'
sid=r.finding('181_185',13,'The second essential image is printed D(S)_parf',reason13,
    'Last essential-image clause of proof(c)',verdict='not applied and now applied',change='Current changes only the last image phrase to D(A)_parf; diplomatic preserves S.')
r.patch(183,'current',r"a pour image essentielle $\mathrm D(S)_{\parf}$, et l'on achève",r"a pour image essentielle $\mathrm D(A)_{\parf}$, et l'on achève",sid,'Match the image of T with the A-module perfect category named in the proposition, leaving the preceding image of j unchanged.')
r.source('fixes/RECONCILE_CODEX_6.json#250','The first and second clauses both print D(S) and D(S)_parf',
    reason12+' '+reason13+' The prior rejection correctly protected the first pair but left the second pair unresolved. The exact functor comparison now resolves the latter.',
    'Both adjacent functor clauses in proof(c)',page=183,verdict='amended',change='Retain the first target/image pair; apply both current-only A substitutions in the second sentence.')
r.finding('181_185',14,'The structural-sheaf sentence and the Stein sentence are separate paragraphs',
    'Both paragraphs have their own indentation. The attached layers already preserve the break.',
    'Two paragraphs following Definition2.4.7')
r.finding('181_185',15,'The object abbreviation is ob, with lowercase o',
    'The two object-membership occurrences on this folio and the directly read preceding pages use lowercase ob. The attached continuation macro already defines operatorname{ob}. This record confirms that definition against the inspected scope; later claimed occurrences in the inherited note are checked on their own pages.',
    'The two printed ob occurrences and attached continuation macro',change='Retain the existing lowercase ob macro; no future-page scan verdict is inferred.')
sid='ASTRA-II-C-183';reason='All four category C letters in the opening proof continuation have individual rules; the zero and S indices remain outside.'
r.own_finding(sid,183,'Four individually underlined category C letters',r'\mathcal C',r'\underline{C}',reason,'Applications of I4.16 and1.1',kind='font')
r.patch(183,'both',r'\mathcal C',r'\underline{C}',sid,reason,4)
sid='ASTRA-II-O-183';reason='The structure-sheaf O in the model(Y,O_X|Y) has an individual rule. Its X index and baseline restriction Y remain outside the rule and retain their positions.'
r.own_finding(sid,183,'One underlined structure-sheaf O in a baseline restriction',r'\mathcal O',r'\underline{O}',reason,'Definition2.4.7',kind='font')
r.patch(183,'both',r'\mathcal O',r'\underline{O}',sid,reason)
sid='ASTRA-II-UNDERLINE-183';reason='Definition2.4.7 and both following sentences have word-group rules. The complete defined term espace pseudo-analytique complexe is underlined here, together with the other statement words; the later phrase de Stein is plain. All formulas and reference(2.4.1) remain independent. Proof, remark, transition and continuation macros remain unchanged. This is the actual page183 scope of checker181–185#6.'
r.own_finding(sid,183,'Underlined definition and following sentences, with plain de Stein','Only the defined term emphasized',r'\uline on the inspected lexical groups',reason,'Definition2.4.7 and its two following paragraphs',kind='underline')
for layer in ['diplomatic','current']:
    old=(ROOT/f'build/page_packets/183/{layer}.tex').read_text()
    for p in r.patches:
        if p['layer'] in ['both',layer]:old=old.replace(p['old'],p['new'])
    new=old.replace(r'\emph{espace pseudo-analytique complexe}','espace pseudo-analytique complexe')
    start=new.index('On appelle ',new.index(r'\textbf{Définition 2.4.7.}'));end=new.index('% Exposé II continuation macros',start)
    new=new[:start]+underline_statement(new[start:end],[r'de Stein',r'\(2\.4\.1\)'])+new[end:]
    r.patch(183,layer,old,new,sid,reason)
r.page(183,'Quitte à tronquer','le topos correspondant l’est(2.4.1).',
    'The full proof continuation and its two separate functor clauses, remark, transition, definition and both subsequent statements were compared. The attached macro block has no printed body counterpart and was left byte-identical in the typography patch.')
r.commit()
