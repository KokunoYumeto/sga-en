#!/usr/bin/env python3
from review_helpers import Review, HERE
r=Review();p=315
r.finding('311_315',29,'The word is entrainera, with a dot over i and no circumflex.',
 'The main middle/lower strips and native overlapping crops resolve the plain i. The attached diplomatic entrainera and corrected entraînera preserve the intended paired spelling treatment.',
 'end of exampleb, before qu’elle se factorise',witness=326)
r.finding('311_315',30,'On prend pour begins a separate indented proof paragraph.',
 'The main lower strip and native lower crop show the indentation after the lemma’s first display. The attached break agrees; no additional content change is needed.',
 'beginning of lemma proof',verdict='formatting observed; no content error',witness=326)
r.finding('311_315',31,'There are eighteen underlined letters on315: five A occurrences and thirteen E occurrences. Their primes remain outside the rules.',
 'Every occurrence was read in both scans. Underlined A: (T,A), des A-Modules localement isomorphes, d’un A-Module libre, des A-Modules localement facteurs, and the lemma’s A-Modules. Underlined E: the example’s pour tout A-Module E and de E(qui); all three exact-sequence objects; all eight exterior-power arguments. Plain forms are the A after pour tout, E inside λ^i(E), E″ after telle que, and both tensor subscripts A. The rule under the lemma’s A is separate from the rule beginning at Modules, leaving the connecting hyphen plain. The316 continuation will be inspected separately.',
 'all eighteen specified letters on315',verdict='315 occurrences confirmed and applied;316 continuation separately scoped',change='Apply the exact local A/E replacements on315 only.',witness=326)
glyph_id='check/findings/findings_311_315.json#31'
for old,new,count in [
 (r'\((T,A)\)',r'\((T,\underline{A})\)',1),
 (r'des \(A\)-Modules',r'des \(\underline{A}\)-Modules',2),
 (r"d'un \(A\)-Module libre",r"d'un \(\underline{A}\)-Module libre",1),
 (r'pour tout \(A\)-Module \(E\)',r'pour tout \(A\)-Module \(\underline{E}\)',1),
 (r'de \(E\) (qui',r'de \(\underline{E}\) (qui',1),
 (r"0\longrightarrow E' \xrightarrow{u} E \xrightarrow{v} E''\longrightarrow0",r"0\longrightarrow \underline{E}' \xrightarrow{u} \underline{E} \xrightarrow{v} \underline{E}''\longrightarrow0",1),
 (r'une suite exacte de \(A\)-Modules',r'une suite exacte de \(\underline{A}\)-Modules',1),
 (r'\Lambda^n(E)',r'\Lambda^n(\underline{E})',4),
 (r"\Lambda^{n-p}(E')",r"\Lambda^{n-p}(\underline{E}')",2),
 (r"\Lambda^p(E'')",r"\Lambda^p(\underline{E}'')",1),
 (r'\Lambda^p(E)',r'\Lambda^p(\underline{E})',1),
]:r.patch(p,'both',old,new,glyph_id,'Preserve the individually inspected underline and plain prime/subscript boundaries.',count=count)
r.own_finding('ASTRA-V-UNDERLINE-315',p,'The lemma leaves Soit plain and underlines une suite exacte de; Modules qui est localement scindée; par exemple telle que; soit localement facteur direct d’un Module libre de type fini; Il existe sur; une filtration finie; et des isomorphismes.',
 r'\uline on these seven lexical groups, with the separately underlined A and E letters retained.',
 'Render the seven inspected word rules.',
 'The native lower crop resolves each endpoint: Soit, the sequence, parentheses, E″ in the parenthesis, and final punctuation are outside the lexical rules. The separate rule under A is already supplied by the letter-level patch; the following hyphen is plain. The words Module libre occur within the long underlined parenthetical clause. This is the315 portion of checker311_315#7.',
 'Lemme2.2.1 statement',witness=326)
modified=(HERE/'page_315_diplomatic.tex').read_text()
for patch in r.patches:
 assert modified.count(patch['old'])==patch['expected_count']
 modified=modified.replace(patch['old'],patch['new'])
old=modified.split(r'\textbf{Lemme 2.2.1.} ',1)[1].split('\n\\[',1)[0]
new=r"Soit \(0\longrightarrow \underline{E}' \xrightarrow{u} \underline{E} \xrightarrow{v} \underline{E}''\longrightarrow0\) \uline{une suite exacte de} \(\underline{A}\)-\uline{Modules qui est localement scindée} (\uline{par exemple telle que} \(E''\) \uline{soit localement facteur direct d'un Module libre de type fini}). \uline{Il existe sur} \(\Lambda^n(\underline{E})\) \uline{une filtration finie}, \uline{et des isomorphismes}~:"
r.patch(p,'both',old,new,'ASTRA-V-UNDERLINE-315','Preserve the seven observed lexical rules, the plain Soit, and separate mathematical-letter rules.')
r.finding('311_315',32,'All eight exterior-power signs on315 are small unadorned wedges at x-height.',
 'The native lower crop resolves the two straight sloping strokes in every occurrence, without capital-Lambda serifs and below the height of E. These occur in the statement, first display, proof phrase and second display. The exact operator is the exterior-power functor already described in exampleb: the notation identification takes each elementary exterior tensor e₁∧…∧e_d to itself in the same alternating quotient. The inspected glyph is restored at these eight usage points;316 remains separately scoped.',
 'all eight exterior-power signs on315',verdict='315 wedge forms confirmed and applied;316 separately scoped',change='Replace the eight315 Lambda commands with wedge.',witness=326)
r.patch(p,'both',r'\Lambda',r'\wedge','check/findings/findings_311_315.json#32','Preserve the eight observed small wedge signs.',count=8)
for id in ['fixes/FIXLOG_6.jsonl#1411','fixes/FIXLOG_6_CURRENT.jsonl#1533']:
 r.source(id,'Page315 ends with the canonical exterior-product map, pour0≤p≤n; si p≥n,;316 begins F^p∧^n(E)=∧^n(E).',
  'The complete315 lower strip and native lower crop were compared; the first main316 strip was read only for this boundary. Closing the gathered environment on315 keeps a valid page boundary and leaves the displayed mathematical token sequence and punctuation intact. This is a scoped TeX/layout implementation decision, not an additional content correction. The regional316 consultation does not mark that page fully checked.',
  '315/316 formula continuation',verdict='scoped implementation confirmed; no content error',change='Retain the attached environment closure.',witness=326,page=315)
r.finding('311_315',7,'The exact word rules on311,314 and315 have all been inspected: the theorem continuation, the definition, and the lemma;315 Soit remains plain.',
 'The three complete pages were compared independently in both scans. Their local patches preserve every inspected lexical span and its mathematical/punctuation exceptions. On314 the defined term pré-λ-anneau is plain; on315 the separate A/E letter rules are handled by checker#31 and Soit remains plain. No uniform whole-statement rule is inferred.',
 'the inspected statement spans on311,314,315',verdict='confirmed and applied at all listed inspected statements',change='Use the exact local word-rule patches for311,314 and315.',witness=326)
for row in r.decisions:
 if row['source_id']=='check/findings/findings_311_315.json#7':
  row['image']='; '.join(f'scan/SGA6_scan_360dpi.pdf#page={q+14}; scan/SGA6_witness_300dpi.djvu#page={q+11}' for q in [311,314,315])
r.page(p,'Exemples2.2. : a) On peut donner toutes les structures','pour0≤p≤n; si p≥n,',
 'Complete examplesa/b and their punctuation, integer-ring letter and λ_t(1), all eighteen individual A/E rules with the stated plain exceptions, historical entrainera, the lemma sequence and labels u/v, every word-rule endpoint including plain Soit, all eight small exterior wedges, the tilde-headed isomorphism, both plain tensor subscripts A, filtration exponents and final bounds/comma compared. No author note.',
 witness='Native witness326 top/lower crops; witness_315_top.png and witness_315_lower.png, plus the native/main Z detail crops')
r.commit()
