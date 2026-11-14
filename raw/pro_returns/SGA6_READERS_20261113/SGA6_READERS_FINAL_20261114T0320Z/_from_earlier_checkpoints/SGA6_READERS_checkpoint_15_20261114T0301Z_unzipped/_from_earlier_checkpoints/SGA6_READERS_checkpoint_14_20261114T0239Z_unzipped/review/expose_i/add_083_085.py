#!/usr/bin/env python3
import re
from review_helpers import Review,ROOT
r=Review()
r.finding('081_085',6,'p^{-1}(underlined O_S)). Le théorème central',
    'Le follows on the same printed line as the closing parentheses, so the supplied joined paragraph is retained.', 'First three lines')
r.finding('081_085',7,'Double-stem R in Rf_*',
    'The R has an added vertical stem, without lower rules. The supplied mathbb R represents this observed doubled glyph.', 'First paragraph, le foncteur Rf_*')
r.finding('081_085',8,'a) S est localement noethérien / b) f est projectif;',
    'No punctuation follows noethérien at the right end of its printed line. A semicolon follows projectif on the next line. Keep that exact punctuation.', 'First paragraph, two cases')
r.finding('081_085',9,'abelienne plate, with no accent in abe-/lienne',
    'Both scans leave the first e unaccented at the broken word, while the preceding abélienne has its acute. Retain abelienne diplomatically and the standard accented form in current.',
    '1.1.1 last sentence; main216dpi and witness300dpi',witness=95)
r.finding('081_085',10,'SGA1 VI7,1',
    'The separator has a visible descending tail in the witness; the earlier reference6.1 has a baseline point. Retain the printed comma diplomatically and use the reference separator7.1 in current.',
    '1.1.2 clivage reference; main216dpi and witness300dpi',witness=95)
r.finding('081_085',11,'S-foncteur additif (resp. exact), with exact alone underlined in the parenthesis',
    'The witness clearly leaves resp. unlined and places a rule under exact. The source has the correct span; its italic command is replaced by an underline in the local convention patch.',
    '1.1.3 final definition; main216dpi and witness300dpi',witness=95)
r.finding('081_085',12,'Underlined base-category S throughout84 and85',
    'Every observed category/site S in these two pages has its own rule. The explicit mapping preserves S as the same base-category symbol and adds its printed underline at14 occurrences on84 and20 on85, without changing S used for schemes on83.',
    'Definitions1.1.1–1.2, all category/site S occurrences',verdict='not applied and now applied',
    change='Add explicit underlines to the14+20 observed S letters in84–85.')
r.finding('081_085',13,'Fl D(C_Y), with a narrow slanted l',
    'The native witness shows a short slanted stroke with a small foot immediately after F, squeezed before D. Retain Fl for this handwritten letter. The parallel notation u∈Fl(S) is directly visible in Remark6.6(a), mainPDF156(p142), where the text names u as a flèche. Only that reference region on142 was consulted here.',
    'Footnote(2); main216dpi, witness300dpi and p142 Remark6.6(a)',witness=96)
r.finding('081_085',14,'C_{0U}, without an interposed comma',
    'The two subscripts are adjacent in the last paragraph; there is no comma between the typed zero and U. The attached layers already agree.', 'Last paragraph, avec E∈ob C_{0U}')

for p,count in[(83,2)]:
    id=f'ASTRA-I-O-{p:03d}';reason='Both structure-sheaf O letters on83 have a single rule and a plain typed outline.'
    r.own_finding(id,p,'underlined O_S and O_X',r'\mathcal O',r'\underline{O}',reason,'First and final main paragraphs')
    r.patch(p,'both',r'\mathcal O',r'\underline{O}',id,reason,count)
id='ASTRA-I-TERMS-083';reason='théorème de finitude, propre and formule de projection are upright and underlined in the scan.'
r.own_finding(id,83,'Three underlined word groups',r'\emph{...}',r'\uline{...}',reason,'First paragraph')
r.patch(83,'both',r'\emph{',r'\uline{',id,reason,3)

for p,c_count,s_count,e_count in[(84,17,14,6),(85,33,20,3)]:
    id=f'ASTRA-I-C-{p:03d}';reason='All category C letters on this inspected page are plain capitals with one underline; primes and indices remain outside the rule. Preserve this literal form without altering the later macro definitions.'
    r.own_finding(id,p,'underlined typed C, with primes/indices outside the rule',r'\mathcal C',r'\underline{C}',reason,'All body category C occurrences')
    for layer in['diplomatic','current']:
        original=(ROOT/f'build/page_packets/{p}/{layer}.tex').read_text()
        body=original.split('% Additional macro definitions')[0]
        assert body.count(r'\mathcal C')==c_count
        new=body.replace(r'\mathcal C',r'\underline{C}')
        r.patch(p,layer,body,new,id,reason)
        # Scope the next transformation to that same previously patched body.
        new_s,n=re.subn(r'(?<![A-Za-z\\])S(?![A-Za-z])',lambda m:r'\underline{S}',new)
        assert n==s_count
        r.patch(p,layer,new,new_s,'check/findings/findings_081_085.json#12','Preserve the printed base-category underline at every inspected S occurrence.')
        assert new_s.count(r'\emph{')==e_count
        changed=new_s.replace(r'\emph{',r'\uline{')
        r.patch(p,layer,new_s,changed,f'ASTRA-I-TERMS-{p:03d}','Preserve upright underlining of the exact defined-word groups visible in the source.')
    r.own_finding(f'ASTRA-I-TERMS-{p:03d}',p,'Underlined defined words at the exact recorded spans',r'\emph{...}',r'\uline{...}',
        'The source uses upright underlining for these definitions; the current italic wrappers have the correct spans after the resp. exact repair. Retain the spans with underlines.', 'Definition word groups')

id='ASTRA-I-NOTES-085';reason='Both main and witness print two notes, numbered1 and2, as raised digits inside baseline parentheses; explicit labels prevent the typeset running counter from changing their identities.'
r.own_finding(id,85,'(raised1) after complexes; (raised2) after quotient',r'Unlabeled \footnote calls',r'\SGAAuthorFootnote{1} and {2}',reason,'1.1.5 and two footnotes',kind='footnote',witness=96)
r.patch(85,'both',r'\footnote{à différentielle',r'\SGAAuthorFootnote{1}{à différentielle',id,reason)
r.patch(85,'both',r'\footnote{si \(a\in\Ob',r'\SGAAuthorFootnote{2}{si \(a\in\Ob',id,reason)

for p,b,e,w in[(83,'équivaut à dire que F','Il y a aussi des variances inhabituelles,',None),(84,'covariance de K^•','sur chaque fibre.',95),(85,'Si C et C′','confusion à redouter).',96)]:
    r.page(p,b,e,'Page85 footnotes included in the full comparison. p142 consulted only for the Fl reference.' if p==85 else '',witness=w)
r.commit()
