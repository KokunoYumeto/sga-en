"""New rear matter and the physically covered inside-cover notice.

All six rear pages and the visible cover-verso text were read directly.
The covered notice remains unresolved; analogous notices do not supply it.
"""
from pathlib import Path
import hashlib,json,re,collections
R=Path(__file__).resolve().parents[2]
O=R/'review/backmatter'
D=[];P=[];S=[];N=[]
def own(suffix,page,pdf,printed,region,reason,change,kind='transcription',verdict='not applied and now applied'):
 q=dict(record_type='own',source_id=f'ASTRA-BACK-{suffix}',page=page,pdf_page=pdf,verdict=verdict,kind=kind,printed_reading=printed,image=f'scan/SGA6_scan_360dpi.pdf#page={pdf}',region=region,where=region,reason=reason,change=change,forms='Both French layers and corresponding English printed matter')
 D.append(q);return q['source_id']
def patch(page,old,new,sid,reason):
 P.append(dict(page=page,layer='both',old=old,new=new,source_id=sid,reason=reason,kind='transcription',expected_count=1))

text=(O/'printed_additions.tex').read_text()
pat=re.compile(r'(?m)^%+\s*scan idx\s+(\d+)\s*\|\s*folio\s+([^%\n]+?)\s*%+[^\n]*$')
markers=list(pat.finditer(text))
for k,m in enumerate(markers):
 key=m[2];pdf=int(m[1])+1;body=text[m.start():markers[k+1].start() if k+1<len(markers) else len(text)]
 N.append(dict(page=key,pdf_page=pdf,layer='both',source_file='review/backmatter/printed_additions.tex',text=body))

for pdf in [715,716]:
 own(str(pdf),f'rear-{pdf}',pdf,'No printed text','entire page','Both the full main-image render and an independent Poppler render show a blank grey page with only scanning/background marks. The OCR layer contains noise unsupported by any printed glyph.','Register the blank page and its source boundary.','blank_page','confirmed')
for pdf,first,last,split in [(717,38,110,74),(718,111,181,148),(719,182,225,217)]:
 own(str(pdf),f'rear-{pdf}',pdf,f'Catalogue entries Vol. {first} through Vol. {last}',f'both columns; left {first}–{split-1}, right {split}–{last}',
     'The whole page was read, then every entry manually transcribed against enlarged column images. Author names, titles, language, capitalization, numeral prefixes, page counts, years, prices and punctuation were compared. Discretionary line-end hyphens join their printed words; ordinary interword and initial spacing follows the established transcription convention. The upper heading and leaflet line on717 are included. Marginal handwriting and library stamps are not publisher text.',
     f'Insert the exact {last-first+1} entries and this page boundary from review/backmatter/printed_additions.tex.','missing_printed_matter')
own('720','rear-720',720,'ISBN 3-540-05647-5; ISBN 0-387-05647-5','bottom left, two lines; remainder of cover',
    'The entire outer back cover was inspected. These are the only two printed lines; the remainder has wear and background marks. Every digit and hyphen was compared with the image.',
    'Insert both ISBN lines and the back-cover page boundary.','missing_printed_matter')

own('717-MATH','rear-717',717,'(Γ₄=0) in Vol.53','left column, Vol.53; enlarged crop images/pdf717_v53.png',
    'The enlarged main-image crop resolves the initial capital Gamma, its small lower4, equality sign and final zero. The catalogue title is transcribed with that complete formula.',
    r'Use \((\Gamma_4=0)\).','symbol','confirmed')
own('717-PRICE','rear-717',717,'DM 6.80; DM 13.20; DM 10.–; DM14,','Vols.40,50,84 and71',
    'The decimal stops in40 and50 and the stop before the price dash in84 are visible. The enlarged71 crop ends with a comma after14 and contains no dash. These locally different printed forms are retained rather than made uniform.',
    'Retain each displayed price punctuation exactly.','punctuation','confirmed')
own('718-ACCENTS','rear-718',718,'Kähleriennes; Seminaire Bourbaki','Vols.154 and179, with enlarged crops',
    'The enlarged154 crop shows the umlaut on a and no acute on the following e. The179 crop prints Seminaire without an acute, while180 immediately below prints Séminaire. The source forms are separately preserved.',
    'Retain these observed diacritics and omissions in the transcription.','spelling','confirmed')

for pdf in range(715,721):
 S.append(dict(page=f'rear-{pdf}',pdf_page=pdf,witness_page=None,checked=True,checked_against_scan=True,status='blank page inspected' if pdf in [715,716] else 'fully compared',scan='scan/SGA6_scan_360dpi.pdf',image=f'scan/SGA6_scan_360dpi.pdf#page={pdf}',regions='whole page; enlarged columns and local crops for the catalogue',reason='Direct full-page inspection and comparison with the new transcription. The provided witness ends at printed700 and has no counterpart to these rear leaves.'))

sid=own('COVER-6','cover-verso',2,'V, 340 pages. 1970. DM 24,–','Lecture Notes in Physics, Vol.6; native-resolution enlarged crop',
    'The supplied front transcription reads VI,310. The enlarged main scan shows the single V followed immediately by a comma, and the three page-count digits340. The dark4 has its characteristic diagonal and crossbar despite the red library stamp. Correct the transcription in both layers; no bibliographic source correction is inferred.',
    'Replace VI,310 by V,340 in the printed Vol.6 advertisement.')
patch('cover-verso','VI, 310 pages. 1970. DM 24,--','V, 340 pages. 1970. DM 24,--',sid,'Restore the clearly visible roman prefix and page count from the enlarged primary image.')

sid=own('COVER-FRAGMENTS','cover-verso',2,'Visible left and right fragments of the publisher notice; Manuscripts heading','upper notice around the library label and the first sentence below its lower edge',
    'The label covers the centre of each upper line. The separate visible fragments were read directly at enlarged scale; the remaining cut letters and covered text are represented by explicit editorial masks. This adds visible material omitted from the previous partial transcription without supplying any obscured wording. The existing note that the page remains incomplete is retained.',
    'Insert review/backmatter/cover_notice_fragments.tex before the already transcribed Symbols paragraph.','partial_transcription')
old='Symbols not on the typewriter should be inserted by hand in indelible black ink.'
patch('cover-verso',old,(O/'cover_notice_fragments.tex').read_text().rstrip()+'\n\n'+old,sid,'Preserve the newly read visible fragments and heading, marking the physical lacuna explicitly.')

own('COVER-UNRESOLVED','cover-verso',2,'Central publisher notice obscured by an opaque library bookplate','upper half of inside front cover',
    'The supplied witness has no inside-cover counterpart. The official Springer front-matter PDF begins at the title page and contains9 imaged pages of the Roman-numbered front matter; the original MSRI/SLMath scan index likewise begins with a title-page image and then the preface. Neither supplies the obscured notice. A search also found analogous series notices, but their wording varies and they do not establish this exact covered text. The lookup record is review/backmatter/evidence/notice_lookup.json. No hidden wording is reconstructed by analogy.',
    'Keep this page explicitly partial and the masked text unresolved.','unresolved_obscuration','unresolved')
S.append(dict(page='cover-verso',pdf_page=2,witness_page=None,checked=False,checked_against_scan=False,status='visible text compared; central notice physically obscured',image='scan/SGA6_scan_360dpi.pdf#page=2',regions='whole page, with upper notice enlarged and lower advertisement enlarged',reason='Visible publisher text has been compared and corrected where established. Covered text remains unresolved after the exact-facsimile lookup; no full-page certification is made.',supersedes='review/front/page_status.jsonl:cover-verso'))

entries=[]
for page in N:
 pdf=page['pdf_page']
 for m in re.finditer(r'(?m)^Vol\. (\d+): (.*)$',page['text']):
  n=int(m[1]);split={717:74,718:148,719:217}[pdf]
  entries.append(dict(volume=n,page=page['page'],pdf_page=pdf,column='left' if n<split else 'right',reading=m[0],image=f'scan/SGA6_scan_360dpi.pdf#page={pdf}',source_file='review/backmatter/printed_additions.tex'))
assert [x['volume'] for x in entries]==list(range(38,226))
assert len(N)==6
front=(R/'review/front/printed_additions.tex').read_text()
for p in P:
 assert front.count(p['old'])==1,(p['source_id'],front.count(p['old']))
 front=front.replace(p['old'],p['new'])
assert len(D)==len({x['source_id'] for x in D})
for name,rows in [('own_findings.jsonl',D),('decisions.jsonl',[]),('patches.jsonl',P),('page_status.jsonl',S),('new_pages.jsonl',N),('catalogue_entries.jsonl',entries)]:
 payload=''.join(json.dumps(x,ensure_ascii=False)+'\n' for x in rows)
 assert not re.search(r'/workspace/|/mnt/|[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}',payload),name
 (O/name).write_text(payload)
(O/'cover_after_patches.tex').write_text(front[front.index('%%%%%%%%%%  scan idx 1 '):front.index('%%%%%%%%%%  scan idx 2 ')])
print('rear pages',len(N),'entries',len(entries),'own',len(D),'patches',len(P),'partial pages',sum(not x['checked'] for x in S))
