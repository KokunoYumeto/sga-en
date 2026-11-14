#!/usr/bin/env python3
from review_helpers import Review,HERE
r=Review();p=335
r.finding('331_335',11,'335 starts with f-prime, evidemment unique.;334 ends et definit.',
 'Both complete335 scans resolve the first f-prime and its comma. The preceding334 end was separately fully compared. The attached marker now precedes f-prime and agrees with the printed boundary.',
 '334/335 boundary',witness=346)
r.finding('331_335',12,'The first product has only lower i=1; the two products in the following display each have upper n and lower i=1.',
 'Main349 and native346 place the subscript n of the preceding T_n] on the preceding text line; no upper bound belongs to the first product. The exact ring map K[X_1,...,X_n]→K[T_1,...,T_n], X_j↦e_j(T_1,...,T_n), sends1+sum_(j=1)^n X_j t^j to product_(i=1)^n(1+T_i t), by the coefficient definition of e_j. This identifies precisely the omitted upper bound n, also displayed on both next products. Preserve the missing upper bound diplomatically and restore n in the current layer.',
 'first factorization product before d ou',verdict='printed omission confirmed; current upper bound restored',change='Retain diplomatic product_(i=1); current product_(i=1)^n.',witness=346)
r.patch(p,'current',r'\prod_{i=1}(1+T_it)',r'\prod_{i=1}^{n}(1+T_it)','check/findings/findings_331_335.json#12','Restore the finite range fixed by the exact elementary-symmetric coefficient map.')
r.finding('331_335',13,'The first1 in each factor of the last displayed product is underlined; the1 inside1+T_i t is plain.',
 'Both main third strip and native lower crop resolve the short rule under the outer1 alone. The supplied underline and plain inner1 agree with the printed unit notation.',
 'last member of the displayed lambda_u equality',witness=346)
r.finding('331_335',14,'335 ends sur A; and336 begins on definit un lambda-homomorphisme:B→K.',
 'The complete335 bottom and the first-line/header region of336 were directly compared in both scans. The attached335 packet ends at the semicolon and the336 marker precedes on. No full336 comparison is claimed by this boundary observation.',
 '335/336 boundary',witness=346)
for row in r.decisions:
 if row['source_id']=='check/findings/findings_331_335.json#14':
  row['image']='scan/SGA6_scan_360dpi.pdf#page=349; scan/SGA6_witness_300dpi.djvu#page=346; scan/SGA6_scan_360dpi.pdf#page=350; scan/SGA6_witness_300dpi.djvu#page=347'
r.own_finding('ASTRA-V-STATEMENT-RULES-335',p,
 'The proposition underlines Soit; un entier; dans le; anneau libre engendre; sur; par une indeterminee; l ideal engendre par les; est; un; ideal. The corollary underlines Le; anneau engendre sur; par le generateur; soumis aux relations; pour; est isomorphe a.',
 'Use the sixteen exact lexical uline spans in the accompanying patches.',
 'Restore only the inspected statement word rules.',
 'Both native crops resolve every endpoint, with all lambda symbols, variables, index inequalities and displayed ring expressions outside the rules. The hyphens immediately after lambda also remain plain. Statement labels retain the accepted typesetting convention.',
 'Proposition4.8 and Corollary4.9',witness=346)
text=(HERE/'page_335_diplomatic.tex').read_text()
replacements={
 r'\textbf{Proposition 4.8.}':r'''\textbf{Proposition 4.8.} \uline{Soit} \(n\) \uline{un entier} \(\ge0\)~; \uline{dans le} \(\lambda\)-\uline{anneau libre engendré} \uline{sur} \(K\) \uline{par une indéterminée} \(X\), \uline{l'idéal engendré par les} \(\lambda^k X\), \(k>n\), \uline{est} \uline{un} \(\lambda\)-\uline{idéal}.''',
 r'\textbf{Corollaire 4.9.}':r'''\textbf{Corollaire 4.9.} \uline{Le} \(\lambda\)-\uline{anneau engendré sur} \(K\) \uline{par le générateur} \(X\) \uline{soumis aux relations} \(\lambda^k(X)=0\) \uline{pour} \(k>n\), \uline{est isomorphe à} \(K[X,\ldots,\lambda^n X]\).''',
}
for start,new in replacements.items():
 old=next(line for line in text.splitlines() if line.startswith(start))
 r.patch(p,'both',old,new,'ASTRA-V-STATEMENT-RULES-335','Restore the individually inspected statement word groups.')
r.own_finding('ASTRA-V-PARAGRAPHS-335',p,'Paragraph numbers4.9.1. and4.10. are plain typed numerals.',
 r'Remove textbf from4.9.1. and4.10.',
 'Preserve the two inspected paragraph-number forms.',
 'Both lower scans show the same ordinary weight as adjacent numerals and no underline.',
 'paragraph numbers4.9.1 and4.10',kind='font',witness=346)
for label in ['4.9.1.','4.10.']:
 r.patch(p,'both',r'\textbf{'+label+'}',label,'ASTRA-V-PARAGRAPHS-335','Preserve the inspected plain paragraph number.')
r.own_finding('ASTRA-V-PHI-335',p,
 'The three phi glyphs in the proof have an open upper-left curve and a descending central stroke.',
 r'Retain all three local \varphi occurrences.',
 'Keep the supplied variant after direct thin-stroke inspection.',
 'The native top crop shows the three forms in the series declaration, lambda^k(phi), and phi=1+X_1t+...; witness_335_phi_zoom.png resolves the upper-left opening in the first. This is a local glyph decision without changing the represented series.',
 'three phi occurrences in Proposition4.8 proof',kind='symbol',verdict='printed forms confirmed and retained',witness=346)
r.page(p,'f-prime, evidemment unique.','le lambda-anneau libre engendre par X sur A;',
 'All four main strips and native346 top/lower compared in full. Checked the first f-prime and comma; sixteen statement word rules; every k/n bound and polynomial-generator index; three headed arrows and lambda_t label; all three open phi forms; seven baseline ellipses; the first missing product upper bound against both following n bounds; the outer unit underline; every brace and final comma; complete corollary and4.9.1 with n_i>=2 and2<=k<=n_i;4.10 beginning and exact final semicolon.336 first-line region viewed only for the boundary. No author note.',
 witness='Native346 top/lower and phi crop: witness_335_top.png, witness_335_lower.png, witness_335_phi.png, witness_335_phi_zoom.png; boundary witness_336_header.png.')
r.commit()
