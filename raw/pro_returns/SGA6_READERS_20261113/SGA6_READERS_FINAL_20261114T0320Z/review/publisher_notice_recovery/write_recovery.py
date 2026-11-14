"""Record the explicitly attributed restitution of the masked inside-cover notice.

This writes a separate amendment stream.  It never changes a frozen review or
the source masters.
"""
from pathlib import Path
import hashlib
import json

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / 'review/publisher_notice_recovery'

def dump(name, value):
    (OUT / name).write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n')

def jsonl(name, rows):
    (OUT / name).write_text(''.join(json.dumps(r, ensure_ascii=False) + '\n' for r in rows))

def sha(path):
    return hashlib.sha256((ROOT / path).read_bytes()).hexdigest()

source_id = 'ASTRA-FRONT-NOTICE-1971-RESTORATION'
template_pdf = 'review/publisher_notice_recovery/springer_lnm228_frontmatter.pdf'
template_image = 'review/publisher_notice_recovery/springer_lnm228_notice.png'
template_url = 'https://link.springer.com/content/pdf/bfm:978-3-540-36976-9/1'

lines = [
    ('This series aim[mask]arch and teaching – quickly, informally',
     'This series aims to report new developments in mathematical research and teaching – quickly, informally'),
    ('and at a high le[mask]ncludes:',
     'and at a high level. The type of material considered for publication includes:'),
    ('1. Preliminary d[mask]', '1. Preliminary drafts of original papers and monographs'),
    ('2. Lectures on a[mask]field', '2. Lectures on a new field, or presenting a new angle on a classical field'),
    ('3. Seminar work[mask]', '3. Seminar work-outs'),
    ('4. Reports of m[mask]', '4. Reports of meetings'),
    ('Texts which are[mask]red if they fall within these categories.',
     'Texts which are out of print but still in demand may also be considered if they fall within these categories.'),
    ('The timeliness o[mask]which may be unfinished or tentative.',
     'The timeliness of a manuscript is more important than its form, which may be unfinished or tentative.'),
    ('Thus, in some i[mask]ts presented which have been or will',
     'Thus, in some instances, proofs may be merely outlined and results presented which have been or will'),
    ('later be publishe[mask]', 'later be published elsewhere.'),
    ('Manuscripts shou[mask]', 'Manuscripts should comprise not less than 100 pages.'),
    ('Publication of L[mask]ational mathematical community, in',
     'Publication of Lecture Notes is intended as a service to the international mathematical community, in'),
    ('that a commercia[mask]tribution to documents which would',
     'that a commercial publisher, Springer-Verlag, can offer a wider distribution to documents which would'),
    ('otherwise have a[mask]ted, they can be documented in the',
     'otherwise have a restricted readership. Once published and copyrighted, they can be documented in the'),
    ('scientific literatur[mask]', 'scientific literature. –'),
    ('Manuscripts', 'Manuscripts'),
    ('Manuscripts are re[mask]herefore be typed with extreme care.',
     'Manuscripts are reproduced by a photographic process; they must therefore be typed with extreme care.'),
]

for visible, full in lines:
    bits = visible.split('[mask]')
    assert full.startswith(bits[0]), (visible, full)
    if len(bits) > 1 and bits[-1]:
        assert full.endswith(bits[-1]), (visible, full)

restored = r'''% The masked notice is restored from the contemporary primary template
% in Springer LNM 228 (1971), front-matter PDF page 1; see the separate
% ASTRA-FRONT-NOTICE-1971-RESTORATION evidence packet. No obscured stroke
% in the supplied SGA 6 image is claimed to have become directly readable.
This series aims to report new developments in mathematical research and teaching -- quickly, informally
and at a high level. The type of material considered for publication includes:
\begin{enumerate}
\item Preliminary drafts of original papers and monographs
\item Lectures on a new field, or presenting a new angle on a classical field
\item Seminar work-outs
\item Reports of meetings
\end{enumerate}
Texts which are out of print but still in demand may also be considered if they fall within these categories.

The timeliness of a manuscript is more important than its form, which may be unfinished or tentative.
Thus, in some instances, proofs may be merely outlined and results presented which have been or will
later be published elsewhere.

Manuscripts should comprise not less than 100 pages.

Publication of \textit{Lecture Notes} is intended as a service to the international mathematical community, in
that a commercial publisher, Springer-Verlag, can offer a wider distribution to documents which would
otherwise have a restricted readership. Once published and copyrighted, they can be documented in the
scientific literature. --

\subsection*{Manuscripts}
Manuscripts are reproduced by a photographic process; they must therefore be typed with extreme care.
'''
(OUT / 'notice_restored.tex').write_text(restored)

proof = {
    'source_id': source_id,
    'page': 'cover-verso', 'pdf_page': 2,
    'status': 'masked wording restored from a personally viewed contemporary primary template',
    'physical_strokes_recovered': False,
    'main_source': 'scan/SGA6_scan_360dpi.pdf#page=2',
    'main_image': 'build/publisher_recovery/sga6_front2.png',
    'main_image_sha256': sha('build/publisher_recovery/sga6_front2.png'),
    'template': {
        'title': 'Conference on Applications of Numerical Analysis',
        'editor': 'John Ll. Morris', 'series': 'Lecture Notes in Mathematics', 'volume': 228,
        'year': 1971, 'book_doi': '10.1007/BFb0069442',
        'book_url': 'https://link.springer.com/book/10.1007/BFb0069442',
        'pdf_url': template_url, 'file': template_pdf, 'sha256': sha(template_pdf),
        'notice_pdf_page': 1, 'printed_notice_page': 'N2', 'image': template_image,
        'date_evidence': 'The personally viewed title page (PDF 2) and copyright page (PDF 3) both print 1971.',
        'date_images': ['review/publisher_notice_recovery/springer_lnm228_p2.png',
                        'review/publisher_notice_recovery/springer_lnm228_p3.png'],
    },
    'direct_comparison': [
        {'line': i + 1, 'sga6_visible_fragment': visible,
         'template_reading': full,
         'visible_prefix_and_suffix_match': True,
         'masked_text_status': 'template-based restitution' if '[mask]' in visible else 'directly visible'}
        for i, (visible, full) in enumerate(lines)
    ],
    'layout_evidence': {
        'same_line_order': True,
        'same_observed_left_and_right_line_ends': True,
        'item4': 'The main image has one item-4 line followed by the Texts paragraph. The 1971 LNM 228 template has the same single line; the 1972 LNM 280 template has the additional provided-they-are line ending and two a/b lines. Those additions are excluded.',
        'main_pixel_frame': [1339, 2066],
        'main_left_visible_ink_bands': {'item2': [223, 245], 'item3': [265, 291], 'item4': [304, 339], 'Texts': [355, 383]},
        'measurement_method': 'Mean RGB below 90, x=25..204, row count above 4, grouping gaps no larger than four pixels; small isolated dirt bands omitted. These bounds supplement direct image inspection and do not measure hidden letters.',
        'manuscripts_minimum': 'The main image visibly begins Manuscripts shou and places this isolated sentence between later be publishe… and Publication of L…. LNM 228 has the exact sentence in that position, including the 100-page limit, with the same surrounding line wrapping.',
        'catalogue': 'The two notices continue with the same Lecture Notes in Physics catalogue, volumes 1–8; the 1972 UIC witness continues to 11. LNP 6 reads V, 340 pages in the 1971 template and in the directly inspected SGA 6 image.',
    },
    'other_primary_comparisons': [
        {'file': 'review/publisher_notice_recovery/gdz_hartshorne_00000002.jpg',
         'url': 'https://gdz.sub.uni-goettingen.de/id/PPN496067087', 'year': 1970,
         'personally_viewed': True,
         'finding': 'Single short item 4; no minimum-length sentence. The retyping-reimbursement sentence and address form differ, so this earlier template was not imported wholesale.'},
        {'file': 'review/publisher_notice_recovery/springer_lnm197_frontmatter.pdf',
         'url': 'https://link.springer.com/content/pdf/bfm:978-3-540-36653-9/1', 'year': 1971,
         'personally_viewed': True,
         'finding': 'The first notice is the earlier bilingual form, also lacking the minimum-length sentence. Its different wrapping and reimbursement clause are not imported.'},
        {'file': 'build/publisher_recovery/uic_lnm1972.pdf',
         'url': 'https://homepages.math.uic.edu/~bona/papers/misc/1972_Book_ConferenceOnTheTheoryOfOrdinar.pdf', 'year': 1972,
         'personally_viewed': True,
         'finding': 'Matching common body and 100-page sentence; item 4 has added a/b restrictions. These later restrictions are absent from the adopted 1971 template.'},
    ],
    'limits': [
        'The label on the supplied SGA 6 image remains in place and obscures the same letters.',
        'LNM 228 is a primary contemporary publisher template, not a second copy of SGA 6.',
        'All covered words are explicitly attributed restitution; no enhanced image or newly visible ink is asserted.',
        'The frozen partial transcription and unsuccessful lookup record remain unchanged as the historical observation.'
    ],
    'supersedes_reading': ['ASTRA-BACK-COVER-FRAGMENTS', 'ASTRA-BACK-COVER-UNRESOLVED'],
    'preserves_other_corrections': ['ASTRA-BACK-COVER-6', 'ASTRA-FRONT-CATALOGUE6-POSTFREEZE'],
}
dump('notice_restitution_1971.json', proof)

reason = (
    'Personally compared the complete supplied inside cover, its enlarged upper notice, '
    'and the complete official Springer LNM 228 (1971) notice. The latter preserves '
    'the same 17 line/heading sequence and every visible left/right fragment, including '
    'the one-line item 4 and the isolated Manuscripts shou… sentence. Its title and '
    'copyright pages independently print 1971; its LNP catalogue likewise stops at volume 8. '
    'Restore the masked wording from this exact contemporary template, including the '
    '100-page sentence. The 1972 a/b restrictions and the earlier reimbursement clause '
    'are excluded. This is attributed reconstruction, not physical recovery of the covered '
    'strokes. Full comparison and source hashes: review/publisher_notice_recovery/notice_restitution_1971.json.'
)
own = {
    'record_type': 'own', 'page': 'cover-verso', 'pdf_page': 2, 'source_id': source_id,
    'verdict': 'amended', 'kind': 'damaged_source_restitution',
    'printed_reading': 'Visible publisher fragments supplemented by the exact primary contemporary LNM 228 notice; item 4 is the short form; minimum length is 100 pages.',
    'image': 'scan/SGA6_scan_360dpi.pdf#page=2; ' + template_pdf + '#page=1',
    'region': 'Publisher notice above and immediately below the library label',
    'where': 'Publisher notice above and immediately below the library label',
    'reason': reason, 'change': 'Replace the masked fragment block with notice_restored.tex in both forms.',
    'forms': 'French and English, both source branches', 'is_misprint': False,
    'physical_strokes_recovered': False,
    'correction_status': 'Explicitly attributed contemporary-template restitution',
    'supersedes': ['ASTRA-BACK-COVER-FRAGMENTS', 'ASTRA-BACK-COVER-UNRESOLVED'],
}
jsonl('own_findings.jsonl', [own])
old = (ROOT / 'review/backmatter/cover_notice_fragments.tex').read_text().strip()
jsonl('patches.jsonl', [{
    'page': 'cover-verso', 'layer': 'both', 'old': old, 'new': restored.strip(),
    'source_id': source_id, 'reason': reason, 'kind': 'damaged_source_restitution',
    'expected_count': 1,
}])
jsonl('page_status.jsonl', [{
    'page': 'cover-verso', 'pdf_page': 2, 'witness_page': None,
    'checked': True, 'checked_against_scan': True, 'fully_checked': True,
    'status': 'fully compared; masked notice explicitly restored from the contemporary primary template',
    'image': 'scan/SGA6_scan_360dpi.pdf#page=2; ' + template_pdf + '#page=1',
    'regions': 'Complete visible inside cover and all 17 upper notice line/heading positions; masked portions compared through the primary 1971 template',
    'reason': reason,
    'physical_strokes_recovered': False, 'hidden_text_directly_read_in_sga6': False,
    'reconstruction_basis': 'Springer LNM 228, 1971, official front-matter PDF page 1',
    'source_id': source_id, 'supersedes': 'review/backmatter/page_status.jsonl:cover-verso',
}])

(OUT / 'HANDOFF.md').write_text('''# Publisher notice — contemporary primary restitution

The formerly masked notice on SGA 6 PDF page 2 can be restored from the official
Springer inside-cover notice of LNM 228 (1971). The downloaded primary PDF,
personally viewed notice, title and copyright pages are retained here. The
download SHA-256 is `5e3f9eb2caa60dde9b0b22165b03749bff292b33201c704f11c9fdefb21eeba8`.

`notice_restitution_1971.json` records all 17 visible-fragment comparisons, the
single-line item 4, the manuscript-length sentence, the 1–8 physics catalogue,
and the differences from the earlier 1970/1971 and later 1972 templates.
`notice_restored.tex` is the proposed complete upper notice. `patches.jsonl`
replaces exactly the existing frozen fragment block, in both branches, after
the earlier backmatter insertion has run. No source-misprint variant is created.

The SGA 6 label remains physically opaque. The masked words are an explicitly
attributed restitution from a primary contemporary template, not recovered
strokes. The page-status amendment states this limitation in separate fields.
The historical incomplete observations and all frozen files remain untouched.

Integration must select the new reading/status over
ASTRA-BACK-COVER-FRAGMENTS and ASTRA-BACK-COVER-UNRESOLVED, preserve both prior
LNP 6 count corrections, and remove any obsolete aggregate incompleteness note
whose sole basis was the masked notice. The coordinator owns those aggregate
changes and the English printed-matter transfer.
''')

check = {
    'visible_fragment_comparisons': len(lines), 'all_visible_fragments_match': True,
    'patches': 1, 'expected_applications': 2,
    'frozen_files_modified': False, 'masters_modified': False,
    'source_id': source_id, 'template_sha256': sha(template_pdf),
}
dump('validation.json', check)
print(json.dumps(check, ensure_ascii=False))
