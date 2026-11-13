"""Read-only privacy, integrity and safe-name checks on a candidate archive."""
from pathlib import Path
import argparse,hashlib,importlib.util,json,zipfile

ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('final_privacy_patterns',ROOT/'work/verification/verify_final.py')
module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)

def check(path):
    hits=[];pdfs=[];files=[]
    with zipfile.ZipFile(path) as archive:
        names=archive.namelist()
        assert len(names)==len(set(names)),'Duplicate archive names'
        assert not archive.testzip(),'ZIP CRC failure'
        for name in names:
            assert not name.startswith('/') and '..' not in Path(name).parts, 'Unsafe archive name'
            data=archive.read(name);files.append(dict(path=name,bytes=len(data),sha256=hashlib.sha256(data).hexdigest()))
            suffix=Path(name).suffix.lower()
            if suffix=='.pdf':
                import fitz
                doc=fitz.open(stream=data,filetype='pdf')
                texts=[json.dumps(doc.metadata,ensure_ascii=False)]+[p.get_text() for p in doc]
                pdfs.append(dict(path=name,pages=len(doc)))
            elif suffix in {'.tex','.py','.sh','.md','.tsv','.csv','.json','.jsonl','.txt','.sty','.bib','.diff'}:
                texts=[data.decode('utf-8',errors='replace')]
            else:texts=[]
            for index,text in enumerate(texts):
                for kind,pattern in [('absolute local path',module.LOCAL_PATH),('email address',module.EMAIL)]:
                    for match in pattern.finditer(text):
                        hits.append(dict(file=name,kind=kind,text_block=index,line=text.count('\n',0,match.start())+1,value_sha256=hashlib.sha256(match.group().encode()).hexdigest()))
    return dict(archive=path.name,bytes=path.stat().st_size,sha256=hashlib.sha256(path.read_bytes()).hexdigest(),result='pass' if not hits else 'rejected',file_count=len(files),privacy_hits=hits,pdfs=pdfs)

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('archive');parser.add_argument('--report')
    args=parser.parse_args();path=ROOT/args.archive;result=check(path)
    if args.report:(ROOT/args.report).write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(result,ensure_ascii=False))
    raise SystemExit(0 if result['result']=='pass' else 1)
