"""Folio166: continued lemma, direct letter forms and proof sequence."""
from review_helpers import Review,ROOT
from source_emphasis import underline_words
r=Review()
obs={
1:('The words after the first display are underlined; their math and the final x are independently typed','The exact attached emphasis boundary ends after qui efface. All lexical groups within it have printed rules. The final x and its stop are outside the group.','Condition a)(ii), opening continuation'),
2:('Les conditions suivantes sont équivalentes is underlined; the colon is outside','Both the group boundary and the excluded colon match the existing emphasis span.','Part b) heading'),
3:('pour tous, et tout, la flèche canonique are underlined','The variables and their memberships remain independently typed. The attached emphasis grouping contains the same word groups.','Part b)(i)'),
4:('est un isomorphisme is underlined; its semicolon is outside','The existing emphasis span stops before the semicolon, matching the scan.','After the second Ext display'),
5:('le foncteur canonique and induit par are separately underlined','The parentheses and the functor glyph stay outside the two spans. The attached grouping matches.','Part b)(ii) introduction'),
6:('The lexical groups following the derived-category display are underlined','D^b(B), F, H^i(F), phi and the final i are outside the lexical rules. The attached emphasis boundary and math separation preserve those exact locations.','Final assertion of the lemma'),
7:('Three baseline ellipsis dots in the Yoneda sequence','The three typed stops lie below arrow height, and the attached ldots form matches.','Proof, exact sequence'),
8:('A baseline full stop is the empty argument of Ext_A^n(.,M)','The printed dot is visibly low. Both attached layers already have the literal full stop.','Definitions of F^n and G^n'),
9:('The empty argument in phi(.) is a baseline full stop','The dot is low, matching the adjacent placeholder. Both attached layers preserve it.','Definition of G^n')}
for n,(printed,reason,region) in obs.items():r.finding('166_170',n,printed,reason,region)
sid=r.finding('166_170',10,'Nine plain A and six plain B category letters on folio166',
    'Every A and B category letter on this complete page has ordinary type, including the Hom/Ext indices and the derived-category arguments. Replace the script forms on this inspected folio only. The remaining pages named by the inherited scope receive their own direct decisions.',
    'All category A,B occurrences on folio166',verdict='not applied and now applied',change='Folio166: mathcal A→A (9), mathcal B→B (6).')
r.patch(166,'both',r'\mathcal A','A',sid,'Preserve the nine inspected plain category A letters.',9)
r.patch(166,'both',r'\mathcal B','B',sid,'Preserve the six inspected plain category B letters.',6)
sid='ASTRA-II-PHI-166';reason='The ten functor glyphs on this page are closed loops crossed by a stroke, including all four Hom/Ext arguments at the top, the two textual occurrences, and the displayed definition of G^n. This is the same inspected form as phi in the preceding folio. Preserve it with phi in both layers.'
r.own_finding(sid,166,'Ten closed-loop phi glyphs',r'\varphi',r'\phi',reason,'All functor phi occurrences',kind='symbol')
r.patch(166,'both',r'\varphi',r'\phi',sid,reason,10)
sid='ASTRA-II-UNDERLINE-166';reason='All eight existing emphasis spans, including the proof heading, correspond to directly observed lexical underlines. The formatter preserves every mathematical unit and each span boundary, including the final x, final i and the parentheses outside the rules.'
r.own_finding(sid,166,'Eight inspected emphasis groups rendered as upright underlined words',r'\emph groups',r'\uline word groups with math unchanged',reason,'Statement continuation and proof heading',kind='underline')
old=(ROOT/'build/page_packets/166/diplomatic.tex').read_text()
for p in r.patches:old=old.replace(p['old'],p['new'])
new,stats=underline_words(old)
assert stats['inspected_emphasis_groups']==8
r.patch(166,'both',old,new,sid,reason)
r.page(166,'Hom_A(L,M)→Hom_B(phi(L),phi(M))','la limite inductive étant prise suivant l’ensemble des suites exactes',
    'Complete statement, proof, Yoneda sequence and the two functor displays directly compared. Every category A,B and closed-phi occurrence was inspected.')
sid='ASTRA-II-TEX-DELIMITER-166';reason='Replacing the script-category token by the inspected plain A joined the adjacent TeX control word into ObA. A separating source space restores the intended control word Ob followed by the same plain A. TeX consumes this delimiter, so the printed ob and A glyphs and the three memberships are unchanged.'
r.own_finding(sid,166,'Three memberships have the printed sequence ob A',r'\ObA',r'\Ob A',reason,'The three object-membership expressions on166',kind='tex_syntax')
r.patch(166,'both',r'\ObA',r'\Ob A',sid,reason,3)
r.commit()
