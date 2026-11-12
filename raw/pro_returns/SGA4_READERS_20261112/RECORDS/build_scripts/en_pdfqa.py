"""Verify final English PDF hashes, diagnostics, text bounds, and sample pages."""
from pathlib import Path
import hashlib,json,re,subprocess,collections
import fitz
from en_common import ROOT,RECORDS

def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()

def main():
    output=[]
    for form in ['diplomatic','corrected_apparatus','reading']:
        name='SGA4_EN_'+form;src=ROOT/'output/en'/(name+'.tex');pdf=src.with_suffix('.pdf')
        previews=RECORDS/'pdf_qa/EN'/name;previews.mkdir(parents=True,exist_ok=True)
        meta=json.loads((RECORDS/'compile_logs'/(name+'.json')).read_text())
        assert meta['source_sha256']==sha(src) and meta['pdf_sha256']==sha(pdf),(name,'checksum mismatch')
        log=(RECORDS/'compile_logs'/(name+'.log')).read_text()
        errors=re.findall(r'^!.*$',log,re.M)
        missing=re.findall(r'^Missing character:.*$',log,re.M)
        unresolved=[b.strip() for b in log.split('\n\n') if re.search(r'LaTeX Warning:',b) and 'undefined' in b]
        unstable=bool(re.search(r'Label\(s\) may have changed|Rerun to get (?:cross-references|outlines) right',log))
        fonts=subprocess.check_output(['pdffonts',str(pdf)],text=True).splitlines()[2:]
        unembedded=[line.split()[0] for line in fonts if line.strip() and line.split()[-5]!='yes']
        doc=fitz.open(pdf);outside=[];selected={0:'title',1:'credits'}
        searches=[('contents','Contents'),('restored_diagram','5.13.2'),('original_Vbis_page138','2:138'),('XIV151','3:151'),('XIX603','3:603')]
        if form!='reading':
            searches += [('human_dossier','Orgogozo edition: human editorial records'),('original_human_pairs','Original French human editorial records'),('original_human_notes','Original human editorial notes')]
        if form=='corrected_apparatus':searches += [('critical_apparatus','Critical apparatus'),('XVII275_layout','3:275')]
        found={}
        for number,page in enumerate(doc):
            text=page.get_text();searchable=re.sub(r'\s+',' ',text)
            for tag,needle in searches:
                if tag in ['human_dossier','original_human_pairs','original_human_notes','critical_apparatus'] and number<800:continue
                if tag not in found and needle in searchable:found[tag]=number;selected.setdefault(number,tag)
            for block in page.get_text('dict',clip=fitz.INFINITE_RECT())['blocks']:
                for line in block.get('lines',[]):
                    for span in line['spans']:
                        x0,y0,x1,y1=span['bbox']
                        if span['text'].strip() and (x0<-.2 or y0<-.2 or x1>page.rect.width+.2 or y1>page.rect.height+.2):
                            outside.append(dict(page=number+1,text=span['text'],bbox=[round(x,2) for x in span['bbox']]))
        preview_rows=[]
        for number,tag in selected.items():
            path=previews/(tag+'.png')
            doc[number].get_pixmap(matrix=fitz.Matrix(1.4,1.4),alpha=False).save(path)
            preview_rows.append(dict(page=number+1,purpose=tag,preview=path.relative_to(RECORDS).as_posix()))
        widths=[float(x) for x in re.findall(r'Overfull \\hbox \(([0-9.]+)pt too wide\)',log)]
        toc=doc.get_toc();duplicates=[dict(entry=toc[i],index=i) for i in range(1,len(toc)) if toc[i]==toc[i-1]]
        row=dict(reader=name,source_sha256=sha(src),pdf_sha256=sha(pdf),pages=len(doc),passes=meta['passes'],tex_errors=errors,missing_glyphs=missing,undefined_references=unresolved,rerun_required=unstable,unembedded_fonts=unembedded,text_outside_page=outside,overfull_hboxes=len(widths),maximum_overfull_points=max(widths,default=0),font_warnings=[b.strip() for b in log.split('\n\n') if 'LaTeX Font Warning:' in b],rendered_samples=preview_rows)
        row.update(pdf_pages=len(doc),zero_compile_errors=not errors,zero_missing_glyphs=not missing,unresolved_reference_warnings=unresolved,text_spans_outside_physical_page=outside,consecutive_identical_pdf_contents_entries=duplicates,credit_urls_on_credit_page=all(u in doc[1].get_text() for u in ['https://github.com/KokunoYumeto/sga-en/issues','https://creativecommons.org/publicdomain/zero/1.0/']),samples={p['purpose']:dict(pdf_page=p['page'],image=p['preview']) for p in preview_rows},warning_counts=dict(latex=len(re.findall(r'^LaTeX Warning:',log,re.M)),font=len(re.findall(r'^LaTeX Font Warning:',log,re.M)),package=len(re.findall(r'^Package [^\n]+ Warning:',log,re.M)),overfull_hbox=len(widths),overfull_vbox=len(re.findall(r'Overfull \\vbox',log)),underfull_hbox=len(re.findall(r'Underfull \\hbox',log)),underfull_vbox=len(re.findall(r'Underfull \\vbox',log))))
        row['automated_checks_passed']=not(errors or missing or unresolved or unstable or unembedded or outside or duplicates)
        (RECORDS/(name+'_PDF_QA.json')).write_text(json.dumps(row,ensure_ascii=False,indent=2)+'\n')
        output.append(row)
        print(name,'pages',len(doc),'passed',row['automated_checks_passed'],'outside',len(outside),'missing',len(missing),'unresolved',len(unresolved),'max_overfull',row['maximum_overfull_points'])
    (RECORDS/'EN_PDF_VERIFICATION.json').write_text(json.dumps(output,ensure_ascii=False,indent=2)+'\n')

if __name__=='__main__':main()
