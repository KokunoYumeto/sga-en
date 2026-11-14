"""Folio197: doubled affine scheme, precise sheaf shorthand and derived glyphs."""
from review_helpers import Review
r=Review()
sid=r.finding('196_200',13,'The R before Q and the R before j_{1*} each have two horizontal lower rules',
 'Both pairs of lower strokes are visible in the composite display. Preserve them literally. The degree-indexed R^1 and R^2 elsewhere are plain, and the displayed relation is a wave over a headless bar.',
 'Composite derived-coherer/direct-image display',verdict='amended',change=r'Replace these two mathbb R forms by \underline{\underline{R}}.')
r.patch(197,'both',r'\mathbb R',r'\underline{\underline{R}}',sid,'Preserve the two directly observed double lower rules in this exact composite.',2)
reason='The first cohomology display prints plain I in both arguments, while its surrounding definition names the associated sheaf. Let a:Mod(A)→Qcoh(X) be J↦tilde J and i:U→X the displayed open immersion. The two arguments mean a(I) and i^*a(I). For this affine X and quasi-coherent a(I), H^1(X,a(I))=H^2(X,a(I))=0; the localization boundary δ:H^1(U,i^*a(I))→H^2_Y(X,a(I)) is therefore an isomorphism. The printed relation H^2_Y(X,I)≃H^1(U,I) expresses δ^{-1} with precisely those associations. Retain the printed shorthand in both layers and document this exact interpretation, rather than insert two extra tildes.'
r.source('fixes/RECONCILE_CODEX_6.json#255','H^2_Y(X,I) ≃ H^1(U,I) has two plain I arguments',reason,
 'First cohomology display on actual197',page=197,verdict='rejection confirmed with explicit identification',change='Retain both printed plain I arguments; identify their associated sheaf and restriction explicitly in the decision.')
sid='ASTRA-II-BOUNDARY-197';reason='The final source word is split par- at the end of197 and continues tie on198. The attached marker follows par% and therefore preserves this exact word boundary without inserting or dropping a letter.'
r.own_finding(sid,197,'The page ends première par-','Attached ending première / par%','Retain the exact existing page split',reason,'Final printed line',kind='marker',verdict='confirmed')
r.page(197,'donc que l’espace sous-jacent à X est noethérien de dimension2.','Le faisceau j_{1*}tilde I étant injectif dans Qcoh(Z), on a prouvé la première par-',
 'Every proof clause, the complete cartesian square with its four labels, all restrictions, all five headless isomorphism signs, the two literal double-underlined R letters, and the exact final split word were compared. The rejected Codex sheaf-tilde proposal was resolved at its actual197 locus with the associated-sheaf and localization maps made explicit.')
r.commit()
