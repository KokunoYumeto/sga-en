"""Folio193: the noetherian-case composite and spectral-sequence bounds."""
from review_helpers import Review
r=Review()
r.finding('191_195',17,'The page begins with the complete display(*), including its tag',
 'The previous page ends on a and the next first printed mathematical line includes(*). The attached marker already precedes the equation environment and its tag.',
 'Page opening',change='Retain the marker before the complete(*) display.')
for i,printed,region in [(18,'Three double-underlined R letters and two headless isomorphism signs','Display(*)'),(19,'Rf_* has a double-underlined R','Inline inducing functor'),(20,'Three double-underlined R letters and one headless isomorphism sign','Display after Par suite')]:
 r.finding('191_195',i,printed,
 'The native witness and main scan show two distinct horizontal rules beneath every indicated R. The headless signs, functor compositions and arguments agree with the attached formulas. Preserve the lower rules literally.',
 region,verdict='amended',change=r'Replace the indicated mathbb R representations by \underline{\underline{R}}, retaining all other tokens.',witness=204)
r.finding('191_195',21,'The spectral sequence has R^qQf^*E without added parentheses around f^*E',
 'The direct token sequence Qf^*E is visible, with the three R letters in this spectral sequence plain and degree-indexed. The attached formula matches, including the abutment star.',
 'Spectral-sequence display',witness=204)
r.finding('191_195',22,'The intersections use three baseline dots between cap signs',
 'The three typed stops lie on the baseline. The multi-indices and surrounding sentence match the attached ldots expression.',
 'Definition of N″',witness=204)
sid='ASTRA-II-R-193';reason='The three R letters in(*), the inline inducing Rf_*, and the three R letters in the next display each have two horizontal lower rules. All seven were viewed in the native witness and main scan. The degree-indexed R letters in the spectral sequence and vanishing formulas are plain and remain so.'
r.own_finding(sid,193,'Seven literal double-underlined derived R letters',r'\mathbb R',r'\underline{\underline{R}}',reason,'First two displays and intervening inducing functor',kind='font',witness=204)
r.patch(193,'both',r'\mathbb R',r'\underline{\underline{R}}',sid,reason,7)
sid='ASTRA-II-BOUNDS-193';reason='The native witness lower region shows strict greater-than signs in p>N, n>N+N″ and n>N+N′+N″, including both occurrences of n>N+N″. The N′ and N″ symbols retain their respective one and two prime marks. The attached expressions already preserve every bound.'
r.own_finding(sid,193,'Strict lower vanishing bounds and distinct one/two prime marks','Attached strict inequalities and N′,N″','Retain the attached bounds and prime counts',reason,'Lower four vanishing displays and definition of N″',kind='symbol',verdict='confirmed',witness=204)
r.page(193,'(*) R(Qf_*)f^*E ≃ RQf_*f^*E ≃ R(f_*Q)f^*E.','R^nQ(E)=0 pour n>N+N′+N″,',
 'All prose, every functor composition, two derived isomorphism displays, the full spectral sequence, all five vanishing statements and every degree bound were compared. Native witness204 confirms the seven literal double-underlined R glyphs, all lower strict inequalities and both prime counts. No prose on this page carries statement underlining.',witness=204)
r.commit()
