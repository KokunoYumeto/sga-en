"""Folio221: final five bibliography entries and nonprinting macro transition."""
from review_helpers import Review
r=Review()
r.finding('221_225',1,'Entry[14], Lang, begins221 including its label',
 'Direct comparison of220 and221 confirms that the current marker is before the complete item14. Reapplying the historical move command would now move it to the wrong item, so the existing state is retained.',
 'Top boundary',change='Retain the already corrected marker location.',witness=232)
r.finding('221_225',2,'Łojasiewicz with an individually crossed initial Ł',
 'Both scans plainly show the short diagonal crossing the upright initial L. The attached L-with-stroke command reproduces that letter.',
 'Bibliography entry15',change=r'Retain \L{}ojasiewicz.',witness=232)
r.finding('221_225',3,'Princeton1963-64 with a typed hyphen',
 'The witness and main scan both have the short typed year-range hyphen; the attached single hyphen is correct.',
 'Bibliography entry16',change='Retain the existing single hyphen.',witness=232)
for sid in ['fixes/FIXLOG_6.jsonl#334','fixes/FIXLOG_6_CURRENT.jsonl#299']:
    r.source(sid,'No printed macro-definition text occurs on221; the page ends with bibliography entry18.',
      'This queue row concerns the nonprinting ExposéIII macro transition stored after the221 body. The queued old and new commands have the same replacement body and differ only by providecommand versus renewcommand: Ob is already defined earlier, so renewcommand installs the transition definition rather than leaving the previous definition untouched. The supplied transition already uses renewcommand and the lowercase ob body recorded by NOTE_6 forIII. Preserve it byte-for-byte. This decision validates that syntax/placement only and does not assert a scanned object-label reading on any uninspected III page.',
      'Nonprinting macro block after the complete bibliography',verdict='retained; syntax-only transition',change='Retain the existing nonprinting macro block; no content patch.',page=221)
r.page(221,'[14] Lang, S., Introduction to differentiable manifolds,','[18] Verdier, J.-L., Les catégories dérivées des catégories abéliennes, à paraître dans North Holl. Pub. Comp.',
 'All five bibliography entries14–18 and the blank lower half were directly inspected in all four strips and compared with both layer texts. Entry14 and entry17 really end with commas; entry15 prints serie without an accent; entry18 prints the distinct J.-L. initials with the stop after J. The lower half contains no further body text. The source’s following macro block produces no page text and is preserved unchanged. This printed folio is the final bibliography page of ExposéII, not the start ofIII.',witness=232)
r.commit()
