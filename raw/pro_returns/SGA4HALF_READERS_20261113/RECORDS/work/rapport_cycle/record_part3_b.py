from record import *
page(114,r"D'après \ref{III:1-5}",range(454,463),start_en=r'By \ref{III:1-5}, this is true')
variant('S45-SOL-0455',114,r'appliqué ou complexe $K$',r'appliqué ou complexe $K$',r'appliqué au complexe $K$','The print has ou; the syntactically required preposition is au.')
variant('S45-SOL-0458',114,r'=_{\text{(\ref{III:1-10})}}',r'=_{\text{(\ref{III:1-10})}}',r'=_{\text{(\ref{III:1-11})}}','The first equality uses the filtration lemma 1.10; the second uses the shifted one-term computation of 1.11.',english_applicability=True)
page(115,r'\begin{corollary_}\label{III:1-13}',[463,464],start_en=r'\begin{corollary_}\label{III:1-13}',overrides={464:dict(reason='The determinant-unit group in this particular displayed sentence is printed Lambda^*. The meaning is the same unit group, but the exact symbol is restored locally; no global normalization is inferred.')})
