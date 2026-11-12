"""Final French PDF identity, page-boundary and documentary-layout checks."""
from pathlib import Path
import hashlib,json,re,sys
import fitz

ROOT=Path(__file__).resolve().parents[1]
READERS=['SGA4_FR_diplomatique','SGA4_FR_corrige_apparat','SGA4_FR_texte_de_lecture']

def digest(path):return hashlib.sha256(path.read_bytes()).hexdigest()

def audit(name):
    source=ROOT/'output/fr'/f'{name}.tex';pdfpath=source.with_suffix('.pdf')
    status=json.loads((ROOT/'output/records/compile'/f'{name}.json').read_text())
    assert status['source_sha256']==digest(source),(name,'compiled source is not current')
    assert status['pdf_sha256']==digest(pdfpath),(name,'compiled PDF hash differs')
    assert not status['errors'] and not status['missing_characters']
    assert all(r['returncode']==0 for r in status['passes'])
    doc=fitz.open(pdfpath);outside=[];samples={'title':0,'credits':1};credits_text=doc[1].get_text()
    needles={
        'contents':'Table des matières',
        'editorial_references':'Références éditoriales de Fabrice Orgogozo',
        'human_dossier':'Dossiers de Fabrice Orgogozo',
        'original_pairs':'Complément documentaire : dossier original de Fabrice Orgogozo',
        'original_notes':'Notes éditoriales originales : conservation documentaire',
    }
    margin_samples={'I34':(1,34),'Vbis138':(2,138),'XIV151':(3,151),'XIX603':(3,603)}
    for number,page in enumerate(doc):
        data=page.get_text('dict',clip=fitz.INFINITE_RECT());spans=[s for b in data['blocks'] if b['type']==0 for line in b['lines'] for s in line['spans']]
        text='\n'.join(s['text'] for s in spans)
        for key,title in needles.items():
            # A chapter heading is a large-font span; ignore ToC and running heads.
            if key not in samples and any(s['size']>=14 and title[:25] in s['text'] for s in spans):samples[key]=number
        for key,(tome,folio) in margin_samples.items():
            if key not in samples and re.search(r'\b'+str(tome)+r'\s*:\s*'+str(folio)+r'\b',text):samples[key]=number
        w,h=page.rect.width,page.rect.height
        for s in spans:
            x0,y0,x1,y1=s['bbox']
            if s['text'].strip() and (x0<-.2 or y0<-.2 or x1>w+.2 or y1>h+.2):
                outside.append({'pdf_page':number+1,'text':s['text'],'bbox':list(s['bbox']),'page_box':[w,h]})
    toc=doc.get_toc();duplicates=[]
    for i in range(1,len(toc)):
        if toc[i]==toc[i-1]:duplicates.append({'entry':toc[i],'index':i})
    dest=ROOT/'output/records/pdf_qa/FR'/name;dest.mkdir(parents=True,exist_ok=True)
    rendered={}
    for label,number in samples.items():
        path=dest/f'{label}.png';doc[number].get_pixmap(matrix=fitz.Matrix(1.35,1.35),alpha=False).save(path)
        rendered[label]={'pdf_page':number+1,'image':path.relative_to(ROOT/'output/records').as_posix()}
    unresolved=[w for w in status['warnings'] if not w.startswith('LaTeX Font Warning:') and re.search(r'(?:Citation|Reference).*undefined|There were undefined references',w,re.I)]
    result={'reader':name,'source_sha256':digest(source),'pdf_sha256':digest(pdfpath),'pdf_pages':len(doc),
            'zero_compile_errors':not status['errors'],'zero_missing_glyphs':not status['missing_characters'],
            'unresolved_reference_warnings':unresolved,'text_spans_outside_physical_page':outside,
            'consecutive_identical_pdf_contents_entries':duplicates,
            'credit_urls_on_credit_page':all(u in credits_text for u in ['https://github.com/KokunoYumeto/sga-en/issues','https://creativecommons.org/publicdomain/zero/1.0/']),
            'samples':rendered}
    target=ROOT/'output/records'/f'{name}_PDF_QA.json';target.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({'reader':name,'pages':len(doc),'unresolved_references':len(unresolved),'outside_page_spans':len(outside),
                      'duplicate_contents_entries':len(duplicates),'credits_fit':result['credit_urls_on_credit_page'],'rendered_samples':len(rendered)},indent=2),flush=True)
    return result

if __name__=='__main__':
    for name in sys.argv[1:] or READERS:audit(name)
