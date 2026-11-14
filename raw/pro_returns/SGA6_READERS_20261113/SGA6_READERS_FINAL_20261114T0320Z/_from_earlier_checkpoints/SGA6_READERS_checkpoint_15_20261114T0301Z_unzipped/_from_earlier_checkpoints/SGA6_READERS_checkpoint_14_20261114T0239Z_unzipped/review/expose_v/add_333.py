#!/usr/bin/env python3
from review_helpers import Review,HERE
r=Review();p=333
r.finding('331_335',6,'The opening phrase is Le lambda-anneau A, without an inserted space after the hyphen.',
 'Both main347 and native344 first lines have the contiguous compound. The attached source already removes the line break which introduced an additional printed space.',
 'opening line',witness=344)
r.own_finding('ASTRA-V-STATEMENT-RULES-333',p,
 'Proposition4.2 has nine lexical rules; Definition4.4 has three; Definition4.5 has nine physical word-group rules. Mathematical symbols and the explicitly named defined terms remain plain.',
 'Use the exact word-only uline spans in the three accompanying patches.',
 'Restore all twenty-one inspected rules with their observed plain exceptions.',
 'The native top crop resolves Proposition4.2 rules on Pour toute; algebre; et toute famille; d elements de; il existe un; homomorphisme et un seul; de; dans; tel que pour tout. The lower crop resolves Definition4.4 rules on Le; anneau; sera appele le, leaving the whole defined name thereafter plain. Definition4.5 rules cover Soient; un; anneau; un ideal de; On dit que; est; un; si pour tout; et tout. All K, A, B, J, f, lambda, family notation and formulas remain outside the rules, along with the connecting hyphens and punctuation.',
 'Proposition4.2 and Definitions4.4–4.5',witness=344)
text=(HERE/'page_333_diplomatic.tex').read_text()
replacements={
 r'\textbf{Proposition 4.2.}':r'''\textbf{Proposition 4.2.} \uline{Pour toute} \(K\)-\(\lambda\)-\uline{algèbre} \(B\), \uline{et toute famille} \((b_i)_{i\in I}\) \uline{d'éléments de} \(B\), \uline{il existe un} \(K\)-\(\lambda\)-\uline{homomorphisme et un seul} \(f\) \uline{de} \(A\) \uline{dans} \(B\) \uline{tel que pour tout} \(i\in I\), \(f(X_i)=b_i\).''',
 r'\textbf{Définition 4.4.}':r'''\textbf{Définition 4.4.} \uline{Le} \(\lambda\)-\uline{anneau} \(A\) \uline{sera appelé le} \(\lambda\)-anneau libre engendré sur \(K\) par la famille de générateurs \((X_i)_{i\in I}\).''',
 r'\textbf{Définition 4.5.}':r'''\textbf{Définition 4.5.} \uline{Soient} \(A\) \uline{un} \(\lambda\)-\uline{anneau}, \(J\) \uline{un idéal de} \(A\). \uline{On dit que} \(J\) \uline{est} \uline{un} \(\lambda\)-idéal de \(A\) \uline{si pour tout} \(x\in J\), \uline{et tout} \(n\ge1\), \(\lambda^n(x)\in J\).'''
}
for start,new in replacements.items():
 old=next(line for line in text.splitlines() if line.startswith(start))
 r.patch(p,'both',old,new,'ASTRA-V-STATEMENT-RULES-333','Restore the individually inspected statement rules.')
r.own_finding('ASTRA-V-PARAGRAPH-333',p,'The paragraph number4.3. has plain typed weight.',
 r'4.3. replaces \textbf{4.3.}.','Preserve the inspected paragraph-number form.',
 'Both scans resolve the numeral group with no underline or added weight.',
 'paragraph number4.3',kind='font',witness=344)
r.patch(p,'both',r'\textbf{4.3.}','4.3.','ASTRA-V-PARAGRAPH-333','Preserve the plain paragraph number.')
r.own_finding('ASTRA-V-PRODUCT-DOT-333',p,
 'The multiplication dot between gamma^n X_i and t^n in4.3.1 lies on the baseline.',
 r'\gamma^n X_i\mathbin{.}t^n replaces \gamma^n X_i\cdot t^n.',
 'Preserve the observed low dot at this one product.',
 'The native344 top crop places the dot beside the foot of t, below the mid-height plus and equality strokes. Its two factors remain exactly gamma^n X_i and t^n; no coefficient or exponent is changed.',
 '4.3.1 first sum term',kind='symbol',witness=344)
r.patch(p,'both',r'\gamma^n X_i\cdot t^n',r'\gamma^n X_i\mathbin{.}t^n','ASTRA-V-PRODUCT-DOT-333','Set the one inspected product dot at baseline height.')
r.own_finding('ASTRA-V-INK-333',p,
 'The f after Si in the kernel paragraph has a broken vertical stem; its short bottom stroke is at the ordinary type baseline.',
 r'Retain plain f in Si \(f:A\to B\).','Record the broken glyph without adding a mathematical underline.',
 'The native row crop witness_333_frow_zoom.png compares both f characters in the same sentence. The intact f in le noyau de f has the same bottom serif position and width; the first f is missing intervening stem ink. A separate below-baseline underline is not observed. Main and native lower images agree on the broken form.',
 'kernel paragraph, first f',kind='physical_ink',verdict='physical damage recorded; plain f retained',witness=344)
r.own_finding('ASTRA-V-PRODUCT-GLYPH-333',p,
 'The product index on Ghat(A-prime) in4.3 is a closed downward triangle.',
 r'Retain the local \nabla index.','Preserve the directly inspected local product marker.',
 'The native top crop clearly resolves its top horizontal stroke and both descending sides. The paragraph references3.7.2, whose functor target was directly compared on329; the map used here is the prescribed A-prime→Ghat(A-prime)_nabla defined by4.3.1. This observation concerns this one actual333 glyph.',
 '4.3 homomorphism target',kind='symbol',verdict='printed form confirmed and retained',witness=344)
r.page(p,'Le lambda-anneau A est caracterise par la propriete universelle suivante :','A/J, qui se trouve ainsi muni',
 'Full comparison completed in all four main strips and native344 top/lower. Checked all twenty-one statement word rules and plain exceptions; all family subscripts and map equalities in4.2 proof; complete gamma polynomial algebra, triangle target, low product dot and gamma-prime superscript in4.3.1; every reference and prime in the canonical-isomorphism paragraph; both complete definitions; broken f and unbarred arrow in the kernel paragraph; both final headed arrows and their label; exact unfinished final phrase. No author note.',
 witness='Native344 top/lower plus f-row comparison: witness_333_top.png, witness_333_lower.png, witness_333_frow.png, witness_333_frow_zoom.png.')
r.commit()
