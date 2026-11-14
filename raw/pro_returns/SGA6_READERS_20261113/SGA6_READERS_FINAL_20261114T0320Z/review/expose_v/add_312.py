#!/usr/bin/env python3
from review_helpers import Review
r=Review();p=312
r.finding('311_315',8,'Page312 begins (1.7) que Φ est déterminé; page311 ends Nous avons vu.',
 'The full first strip and native top crop begin with the parenthesized reference, followed by que and capital Φ. The prior page was fully checked through Nous avons vu. The attached marker agrees.',
 'page start',witness=323)
r.finding('311_315',9,'The first index is j=1..k, with two baseline stops and no commas.',
 'The native top crop resolves both stops in the subscript below the tuple of universal elements. The attached literal two-stop range agrees.',
 'second printed line, first tuple',witness=323)
r.finding('311_315',10,'The first polynomial-ring index has i≥1 above j=1..k, without a comma between the two rows.',
 'The native top crop resolves the two stacked rows and the two stops in the lower row. The attached substack has the same index conditions and punctuation.',
 'second printed line, polynomial-ring index',witness=323)
r.finding('311_315',11,'The later polynomial-ring index is i≥1,j=1..k on one line, with one separating comma and two baseline stops.',
 'The native top crop resolves this unstacked index after coefficients dans. The attached text preserves its different geometry and exact punctuation.',
 'coefficient-ring expression',witness=323)
r.finding('311_315',12,'The completion hat covers Gr followed by its low placeholder dot.',
 'The native top crop resolves the full-stop-shaped dot immediately after Gr. The inherited restoration of that missing placeholder is confirmed; its cdot height is amended by the separately recorded baseline-dot patch.',
 'list of example functors',verdict='placeholder restoration confirmed; height treatment amended',witness=323)
r.finding('311_315',13,'The complete defined term n-ième polynôme universel de is underlined, including the initial n and hyphen; Φ remains outside.',
 'Both scans show one continuous rule beginning under n and ending under de. The inherited emph span identifies the right text; the exact inspected span now uses explicit underlining, including its initial mathematical letter.',
 'defined term after sera appelé',verdict='span confirmed; explicit underline applied',witness=323)
r.patch(p,'both',r'\emph{\(n\)-ième polynôme universel de}',r'\uline{\(n\)-ième polynôme universel de}','check/findings/findings_311_315.json#13','Preserve the complete observed rule, including n and its following hyphen.')
r.finding('311_315',14,'Both interior +…+ groups in the long Φ evaluation are three baseline dots.',
 'The native top crop resolves the first and last factor-series groups. The separate argument-separator ellipsis is also low. All three attached ldots forms agree.',
 'on calcule les éléments formula',witness=323)
r.finding('311_315',15,'The series after en décomposant has three baseline dots between its first and nth terms.',
 'The native top crop resolves the three dots, lower than the adjacent plus signs; the product below retains lower bound j=1 and upper bound n. The attached reading agrees.',
 'en décomposant formula',witness=323)
r.own_finding('ASTRA-V-PLACEHOLDER-312',p,'The sole completion-placeholder dot is on the baseline, directly after Gr under the hat.',
 r'\,\mathord{.}\, replaces \,\cdot\, at this occurrence.',
 'Restore the inspected low placeholder height.',
 'The native top crop resolves the low dot under the same completion hat as Gr. This remains the example functor 1+completed Gr(.)⁺, with the same unspecified argument; only the printed height is restored.',
 'example-functor list',kind='symbol',witness=323)
r.patch(p,'both',r'\,\cdot\,',r'\,\mathord{.}\,','ASTRA-V-PLACEHOLDER-312','Preserve the observed baseline dot.')
r.own_finding('ASTRA-V-FORMS-312',p,'The two lowercase universal-element φ glyphs have open upper-left outlines; every transformation letter is capital Φ; the examples are Ĝ, Ĝ_g and Ĝ_a.',
 r'Retain \varphi in the two tuple occurrences, \Phi throughout, and the three hatted-G forms.',
 'Retain these directly inspected forms and the two printed stops after the first parenthesized resp. clause and after etc.',
 'The native top crop resolves the open-left lowercase glyphs, the typed capitals, all three hats and the separate g/a indices. It also shows the unusual doubled final stops after the resp. clause and etc.; these remain exactly as printed. The lower crop confirms ψ, θ, the stated bounds n/mn and k/km, and the final full stop.',
 'Greek-letter and punctuation comparison throughout',kind='symbol',verdict='confirmed',witness=323)
# Page status is added only after the isolated lower-line ink point is adjudicated.
r.commit()
