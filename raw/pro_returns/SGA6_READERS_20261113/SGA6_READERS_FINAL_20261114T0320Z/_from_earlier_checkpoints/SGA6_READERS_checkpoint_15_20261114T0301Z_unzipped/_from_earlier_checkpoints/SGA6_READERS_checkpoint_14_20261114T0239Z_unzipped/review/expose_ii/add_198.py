"""Folio198: duality chain, source shorthand, and protected continuation macros."""
from review_helpers import Review,ROOT
r=Review()
r.finding('196_200',14,'The page starts tie de(0.3).',
 'The preceding folio ends par- and the first line here completes partie. Both existing source markers preserve the exact split word.',
 'First printed line',change='Retain the existing split-word boundary.')
for i,n,region in [(15,3,'First duality display'),(16,2,'Second affine-comparison display'),(17,2,'Third derived-Hom display')]:
 r.finding('196_200',i,f'{n} R letters with two horizontal lower rules; Hom is plain',
 'The main scan and native witness show two separate rules beneath each indicated R. All Hom subscripts, pullback stars, sheaf tildes and headless relations were compared. Use the literal lower-rule construction at these occurrences.',
 region,verdict='amended',change=r'Use \underline{\underline{R}} for the inspected R letters; retain the other tokens.',witness=209)
reason='The middle affine-comparison term prints plain I. With X=Spec(A), let a:Mod(A)→Qcoh(X) be J↦tilde J and Γ_X its inverse. For F=j_1^*E, the adjunction with counit aΓ_XF≃F gives Hom_Qcoh(X)(F,a(I))≃Hom_A(Γ_XF,I). Both functors of this equivalence are exact, so the same identification holds for derived Hom. The module I is injective, hence a(I) is injective in Qcoh(X), and this derived Hom is the ordinary Hom written at the right of the chain. Thus the printed I denotes exactly a(I)=tilde I in that middle term. Retain this explicit shorthand and the preceding and following printed tildes; adding a tilde is an expansion, not a correction to the identified map.'
r.source('fixes/RECONCILE_CODEX_6.json#256','The middle RHom_Qcoh(j_1^*E,I) term has plain I',reason,
 'Second display on actual198',page=198,verdict='rejection confirmed with explicit identification',change='Retain the printed plain I in the middle term, with its exact associated-sheaf interpretation documented.',witness=209)
sid='ASTRA-II-R-198';reason='The first three displays contain five R letters immediately before Hom and two immediately before j_{1*}; each has two horizontal lower rules. The patches use those exact following tokens and therefore leave the appended continuation macro definitions, including the separate R macro, byte-identical.'
r.own_finding(sid,198,'Seven literal double-underlined R glyphs in the proof body',r'\mathbb R before Hom or j_{1*}',r'\underline{\underline{R}} at those exact seven occurrences',reason,'Three derived-Hom displays, before the continuation macro block',kind='font',witness=209)
r.patch(198,'both',r'\mathbb R\Hom',r'\underline{\underline{R}}\Hom',sid,reason,5)
r.patch(198,'both',r'\mathbb Rj_{1*}',r'\underline{\underline{R}}j_{1*}',sid,reason,2)
for layer in ('diplomatic','current'):
 before=(ROOT/f'build/page_packets/198/{layer}.tex').read_text();after=before
 for p in r.patches:after=after.replace(p['old'],p['new'])
 marker='% Additions for Expose II, Appendix II'
 assert before.split(marker,1)[1]==after.split(marker,1)[1]
r.page(198,'tie de(0.3).','pleinement fidèle, ce qui achève la démonstration de(0.3).',
 'Every proof word, all duality-chain arguments, the exact plain-I occurrence, every one of the five headless isomorphism signs, both Ext² expressions and the final nonzero element were compared. Witness209 confirms all seven literal double-underlined R glyphs and the middle plain I. The appended TeX continuation definitions are implementation material and remain byte-identical.',witness=209)
r.commit()
