#!/usr/bin/env python3
from review_helpers import Review
r=Review();p=299
r.finding('296_300',18,'The first word-symbol is f_ψ; the preceding seul ends page 298.',
 'The complete first strip and native top crop begin f_ψ de K[Xi]… . The attached marker is already at that exact split.',
 'page start',witness=310)
r.finding('296_300',19,'ψ=1+a₁t+… with three baseline full stops.',
 'The main strip and witness top crop place the three stops on the writing baseline after the plus sign. The attached ldots preserves that level.',
 'definition of filtration in 1.3',witness=310)
r.finding('296_300',20,'Ab.fil. with independently underlined Ab and fil and a full stop after each.',
 'Both scans show a short rule beneath Ab, a separate rule beneath fil, and the two full stops outside those letter rules. The attached explicit form preserves this occurrence.',
 'first category name in 1.3',witness=310)
r.finding('296_300',21,'Ab fil with independently underlined Ab and fil, without either full stop.',
 'The native crop resolves separate rules and open whitespace between the names. This second occurrence has no dots; retain the occurrence-specific attached spelling.',
 'Soit H… category name',witness=310)
r.finding('296_300',22,'A tilde above a short rightward headed arrow between H(A^G) and H(A)^G.',
 'The native top crop clearly separates the wavy upper mark from the lower horizontal shaft and its right arrowhead. The attached headed arrow matches the printed restriction-to-invariants map.',
 'condition ii)',witness=310)
r.finding('296_300',23,'(l’exposant G désignant les invariants sous G) with no following punctuation.',
 'The main second strip and the upper edge of the native examples crop show a bare closing parenthesis, followed by the paragraph break. The attached text agrees.',
 'end of condition ii)',witness=310)
r.own_finding('ASTRA-V-PHI-299',p,'The argument of Ĝ(f_ψ) is the closed-oval phi with a central descending stroke.',
 r'\Ghat(f_\psi)(\phi)=\psi',
 'Use the observed closed phi form in this occurrence.',
 'The native top crop shows the closed oval crossed by a vertical stroke. This is the same universal series defined on 298, now used as the argument of the representing map. The replacement changes only its local glyph form; the map f_ψ and output ψ stay identical.',
 'first line',kind='font',witness=310)
r.patch(p,'both',r'\Ghat(f_\psi)(\varphi)',r'\Ghat(f_\psi)(\phi)','ASTRA-V-PHI-299','Preserve the observed closed-oval phi form.')
r.own_finding('ASTRA-V-FONT-299',p,'Plain paragraph numbers 1.3. and 1.4.; handwritten script C throughout; an underlined Exemples label; plain body words.',
 r'1.3.; 1.4.; \mathcal C; statement-label convention for Exemples.',
 'Remove bold weight from the two paragraph numbers; retain the other local forms.',
 'All five category letters have the same looping script form without separate lower rules. The two paragraph numbers have ordinary typewriter weight. Exemples has a rule beneath the word, covered by the accepted bold statement-label convention; none of the surrounding definition or example prose is underlined. All eleven hatted G occurrences, including the g and a subscripts, agree with the attached notation.',
 'paragraph numbers, category letters, and examples',kind='font',witness=310)
for n in ['1.3.','1.4.']:
 r.patch(p,'both',r'\textbf{'+n+'}',n,'ASTRA-V-FONT-299','Preserve the ordinary typed paragraph number.')
r.page(p,'f_ψ de K[Xi]…','Pour tout n… l’endomorphisme de K[X₁,…,X_n]',
 'All prose, both filtration bounds, all category names and operator capitals, the two invariant expressions and headed arrow, complete conditions i) and ii), and all three examples compared. The actual spacing before (avec is retained. No author footnote.',
 witness='Native witness310 top and examples crops; witness_299_top.png and witness_299_examples.png')
r.commit()
