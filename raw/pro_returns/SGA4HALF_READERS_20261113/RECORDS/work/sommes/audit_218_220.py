from audit_helpers import *
reasons={926:'The primitive character in the last paragraph is visibly a character of (Z/d)*; its conductor is d, not n.',927:'The final analogous sum also visibly runs over (Z/d)*, not (Z/n)*.',928:'The source says Le cas intéressant, with masculine article.',929:'The source begins Nos outils essentiels, not Nous outils.',930:'The print has the malformed phrase énoncés cohomologiques de reflet les identités suivantes. The intended grammatical relation is that the identities reflect the cohomological statements; correct to que reflètent.',931:'The first inner decomposition visibly has psi(x_1), matching its outer summation variable, not psi(x_i).',932:'The source says k une algèbre étale, with feminine article.',933:'The phrase is printed en terme de sommes. Correct the fixed expression to en termes de sommes.',934:'The comparison in print identifies the split n-variable sum with the field F_{q^n}; its defining algebra is instead the split product F_q^n. Correct the placement of the exponent.',935:'The source says F une clôture algébrique.'}
for n,reason in reasons.items():decide(n,reason)
page(218,r'Tant $X$ que $Y=',r'Both $X$ and $Y=')
page(219,r'\section{Sommes de Kloosterman généralisées}',r'\section{Generalized Kloosterman sums}')
page(220,'On a encore','We still have')
variant(219,'S45-SOL-0930','les énoncés cohomologiques de reflet les','les énoncés cohomologiques que reflètent les','Restore the grammatical relation between the statements and the identities reflecting them.',place='Before (7.1.4)')
variant(220,'S45-SOL-0933','en terme de sommes de Gauss','en termes de sommes de Gauss','Correct the fixed expression en termes de.',place='Fourier inversion paragraph')
variant(220,'S45-SOL-0934',r'\kloos_{\dF_{q^n},a}',r'\kloos_{\dF_q^n,a}','The original n-variable sum uses the split étale algebra F_q^n.',en_old=r'\kloos_{\dF_{q^n},a}',en_new=r'\kloos_{\dF_q^n,a}',place='Before (7.2.5)')
for n,p in [(38,218),(39,219),(40,220)]:
 own(n,p,'Unit-group notation',r'^\ast',r'^\times',r'^\ast','symbol','The unit-group signs in the scan are asterisks.')
 append('notation_units',{'page':str(p),'source':f'S45-ASTRA-S-{n:04}','replace':r'^\times','with':r'^\ast'})
