"""Attach the corrected rendering selected by each annotated master's default."""
import hashlib,json,shutil
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
NAMES=[('FR','SGA4_FR_master_annote','SGA4_FR_corrige_apparat'),
       ('EN','SGA4_EN_annotated_master','SGA4_EN_corrected_apparatus')]

def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()

def main():
    status=json.loads((ROOT/'output/records/COMPILE_STATUS.json').read_text())
    completed={r['reader']:r for r in status if r['finished']}
    rows=[]
    for lang,master,form in NAMES:
        folder=ROOT/'output'/lang.lower();mp=folder/(master+'.tex');fp=folder/(form+'.tex')
        assert form in completed,form+' requires a current successful compile'
        assert sha(fp)==completed[form]['compiled_source_sha256']
        if lang=='FR':
            assert mp.read_bytes()==fp.read_bytes()
            evidence='The annotated master is byte-identical to the corrected reader; its default SGAForm selector is1.'
        else:
            text=mp.read_text();prefix='% Generated from SGA4_EN_annotated_master.tex.\n\\def\\SGAform{1}\n'
            assert fp.read_text()==prefix+text
            assert text.count(r'\providecommand{\SGAform}{1}')==1
            assert r'\jobname' not in text
            evidence='The generated corrected source prepends a comment and def SGAform{1}; the master supplies the same default by providecommand{SGAform}{1}. Both select the identical corrected rendering.'
        pdf=folder/(form+'.pdf');target=folder/(master+'.pdf')
        shutil.copyfile(pdf,target)
        rows.append(dict(language=lang,master=mp.name,master_sha256=sha(mp),
          compiled_reader=fp.name,compiled_reader_sha256=sha(fp),pdf=target.name,
          pdf_sha256=sha(target),pdf_bytes=target.stat().st_size,evidence=evidence))
    (ROOT/'output/records/MASTER_PDF_RENDERINGS.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2)+'\n')
    print('Master PDF renderings:',len(rows))

if __name__=='__main__':main()
