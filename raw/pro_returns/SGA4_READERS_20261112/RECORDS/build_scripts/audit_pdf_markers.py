"""Verify every original-page marginal label in the six rendered PDFs."""
import collections,csv,hashlib,json,re
from pathlib import Path
import fitz
from build_reports import READERS

ROOT=Path(__file__).resolve().parents[1];REC=ROOT/'output/records'

def main():
    original=json.loads((ROOT/'sources/api_pass_20261111/PAGES.json').read_text())
    expected=[(str(r['tome']),str(r['folio'])) for r in original]
    assert len(set(expected))==len(expected)
    page_lookup={(str(r['tome']),str(r['folio'])):r for r in original}
    want=collections.Counter(expected);audits=[];locations=[]
    for lang,form,name in READERS:
        pdf=ROOT/'output'/lang.lower()/(name+'.pdf')
        if not pdf.exists():
            audits.append(dict(reader=name,passed=False,reason='Current PDF absent'));continue
        found=[];document=fitz.open(pdf)
        for page_number,page in enumerate(document,1):
            for block in page.get_text('dict')['blocks']:
                for line in block.get('lines',[]):
                    text=''.join(span['text'] for span in line['spans'])
                    x0,y0,x1,y1=line['bbox']
                    # The supplied page-label macros place their bold labels
                    # in the outer 78-point bands, outside the body measure.
                    if not (x1<78 or x0>page.rect.width-78):continue
                    match=re.fullmatch(r'\s*([123])\s*:\s*(\d+)\s*',text)
                    if match:found.append((page_number,y0,x0,match.group(1),match.group(2)))
        found.sort();actual=[(t,p) for _,_,_,t,p in found];got=collections.Counter(actual)
        missing=list((want-got).elements());extra=list((got-want).elements())
        audit=dict(reader=name,language=lang,form=form,pdf_pages=len(document),
          pdf_sha256=hashlib.sha256(pdf.read_bytes()).hexdigest(),
          original_page_labels=len(actual),expected_labels=len(expected),
          missing=missing,extra=extra,sequence_matches=actual==expected,
          passed=not missing and not extra and actual==expected)
        audits.append(audit)
        for pdf_page,y,x,tome,folio in found:
            source=page_lookup.get((tome,folio),{})
            locations.append(dict(reader=name,pdf_page=pdf_page,tome=tome,
              expose=source.get('expose',''),original_page=folio,
              x_points=round(x,2),y_points=round(y,2)))
    (REC/'PDF_PAGE_MARKER_AUDIT.json').write_text(json.dumps(audits,ensure_ascii=False,indent=2)+'\n')
    with (REC/'PDF_ORIGINAL_PAGE_LOCATIONS.tsv').open('w',newline='') as stream:
        writer=csv.DictWriter(stream,fieldnames=['reader','pdf_page','tome','expose','original_page','x_points','y_points'],delimiter='\t',lineterminator='\n')
        writer.writeheader();writer.writerows(locations)
    for r in audits:print(r['reader'],r['passed'],r.get('original_page_labels'),r.get('missing',[])[:8],r.get('extra',[])[:8])
    return all(r['passed'] for r in audits)

if __name__=='__main__':raise SystemExit(0 if main() else 1)
