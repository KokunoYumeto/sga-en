"""Folio210: limits, function-space notation and the exact final boundary."""
from review_helpers import Review
r=Review()
r.finding('206_210',7,'The final words are d’image dense, et l’on a',
 'The complete last line contains no loc.cit. reference. The attached210 chunks end after a, leaving that reference beyond this page marker. The printed endpoint and attached endpoint agree.',
 'Last printed line',change='Retain the current boundary after et l’on a.')
sid='ASTRA-II-O-210';reason='Both O letters in the real and complex module structures of3.0.3 have one individual lower rule.'
r.own_finding(sid,210,'Two singly underlined O letters',r'\cO',r'\underline{O}',reason,'Paragraph3.0.3',kind='font',witness=221)
r.patch(210,'both',r'\cO',r'\underline{O}',sid,reason,2)
sid='ASTRA-II-FIELDS-210';reason='The coefficient C in3.0.3 and the integer Z in3.0.4 each have two distinct horizontal lower rules. The separate continuous-function sheaf C in3.0.1 has only one rule, already represented by underline C; the other function-space C letters and Banach-operator L are plain.'
r.own_finding(sid,210,'One coefficient C and one integer Z with double lower rules',r'\mathbb C and \Z',r'\underline{\underline{C}} and \underline{\underline{Z}}',reason,'Paragraphs3.0.3 and3.0.4',kind='font',witness=221)
r.patch(210,'both',r'\mathbb C',r'\underline{\underline{C}}',sid,reason)
r.patch(210,'both',r'\Z',r'\underline{\underline{Z}}',sid,reason)
sid='ASTRA-II-PARAGRAPHS-210';reason='The four paragraph identifiers3.0.1.,3.0.2.,3.0.3.,3.0.4. have plain typed numerals and final stops. The section-heading convention remains separate.'
r.own_finding(sid,210,'Four plain numerical paragraph identifiers','Bold3.0.1.–3.0.4.','Plain identifiers retaining all stops',reason,'Four definition paragraphs',kind='font',witness=221)
for num in ('3.0.1.','3.0.2.','3.0.3.','3.0.4.'):
 r.patch(210,'both',r'\textbf{'+num+'}',num,sid,reason)
r.page(210,'est un épimorphisme. D’autre part, on a(T.F.II3.3.1):','une application linéaire continue injective d’image dense, et l’on a',
 'Every word, the three-row opening Hom/section comparison, both lower-case lim operators with rightward arrows, all three headless isomorphism signs, the baseline restrictions and the four notation paragraphs were compared. The set-valued Hom words are plain, and their sheaf-Hom counterparts have individual rules. Native witness221 confirms the one-rule function sheaf C, double-rule coefficient C and integer Z, and the plain operator L. There is no lexical statement emphasis on this page.',witness=221)
r.commit()
