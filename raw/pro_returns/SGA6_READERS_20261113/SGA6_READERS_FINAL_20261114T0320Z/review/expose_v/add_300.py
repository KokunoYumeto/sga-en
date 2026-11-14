#!/usr/bin/env python3
from review_helpers import Review
r=Review();p=300
reason='Both scans distinctly type permier in the first paragraph. The standard word premier is also printed correctly in the analogous identification sentence of 1.5 on this same page. Keep permier diplomatically and the already applied premier in current.'
r.finding('296_300',24,'le permier in the first paragraph; le premier in 1.5.',reason,'first paragraph and comparison in 1.5',witness=311,change='Retain the existing diplomatic/current permier/premier distinction.')
for sid in ['fixes/FIXLOG_6_CURRENT.jsonl#399','fixes/RECONCILE_CODEX_6.json#307']:
 r.source(sid,'le permier',reason,'first paragraph',witness=311,page=p,change='Retain the existing current spelling correction.')
r.finding('296_300',25,'The invariant-subgroup display ends at H(K[T₁,…,T_n]) with no following full stop.',
 'The main display strip and native top crop show the closing parenthesis without punctuation. The attached expression agrees. The first relation in this display has a tilde and a headless lower bar; the second has a tilde above a rightward headed arrow.',
 'display in 1.5',witness=311)
r.own_finding('ASTRA-V-FONT-300',p,'The paragraph number 1.5. is plain; the three symmetric-group symbols are hand-drawn Fraktur S with subscript n.',
 r'1.5.; \mathfrak S_n in all three occurrences.',
 'Remove bold weight from 1.5. and retain the three observed symmetric-group forms.',
 'The native top crop resolves the upper tail, inward central bend and rounded lower bowl in each S, without an underline. All prose on the page is plain. The lower native crop confirms both plain rightward map arrows, the sum from i=1 to n, both u indices, and the final period after the u_H^n display.',
 'paragraph number and displayed morphisms',kind='font',witness=311)
r.patch(p,'both',r'\textbf{1.5.}','1.5.','ASTRA-V-FONT-300','Preserve the ordinary typed paragraph number.')
r.page(p,'défini par f_n(X_i)=X_i si i<n…','qui par suite prend ses valeurs dans',
 'The complete factorization and both subgroup-identification paragraphs, augmentation sentence, invariant chain, all bracket and exponent placements, maps u_i^n and u_H^n, sum bounds and punctuation compared. All series-variable ellipses are baseline stops. No author note.',
 witness='Native witness311 top and maps crops; witness_300_top.png and witness_300_maps.png')
r.commit()
