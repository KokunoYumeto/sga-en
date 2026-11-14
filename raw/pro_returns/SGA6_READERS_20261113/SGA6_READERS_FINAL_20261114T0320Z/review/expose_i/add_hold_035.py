#!/usr/bin/env python3
from review_helpers import Review
r=Review()
r.source('fr/codex/HOLD_VS_CORR.json#35','a∈ob D(C_Y) (resp. Fl D(C_Y))',
    'The nominal page75 attached to this HOLD difference is incorrect: the passage is Exposé I1.1.5, printed85. The main and witness both print ob D(C_Y) followed by the narrow slanted l of Fl D(C_Y). The HOLD reconstruction replaces the two cases by ob K(C_Y) and ob D(C_Y), which changes the printed object/arrow alternatives. The actual functor f*:D(C_Y)→D(C_X) acts on both objects and arrows, so a_X abbreviates f*(a) in both printed cases; the K/D substitution is unsupported by the scan. Retain the actual printed readings already restored in the attached layers, with the observed category underlines and explicit note label2. The independently observed notation Fl(S) in I6.6(a), p142, supports the reading of the narrow letter.',
    'Printed85, author footnote2; mainPDF99 and witness96',verdict='amended',
    change='Confirm rejection of HOLD reconstruction; retain ob D(C_Y) and Fl D(C_Y), not the K/D replacement.',witness=96,page=85)
r.commit()
