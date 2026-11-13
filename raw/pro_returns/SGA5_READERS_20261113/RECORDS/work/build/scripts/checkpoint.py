from __future__ import annotations
import argparse,json,zipfile
from pathlib import Path

def main():
    ap=argparse.ArgumentParser();ap.add_argument('number',type=int);ap.add_argument('--finished',nargs='+',required=True);a=ap.parse_args()
    target=Path('deliverables')/f'SGA5_READERS_checkpoint_{a.number}.zip'
    files=[]
    for root,base in [(Path('deliverables'),'deliverables'),(Path('work/build/scripts'),'scripts'),(Path('work/build/prepared'),'prepared'),(Path('work/contributions'),'contributions')]:
        if not root.exists():continue
        for p in sorted(root.rglob('*')):
            # The same generated work tree is added below under scripts,
            # prepared and contributions; omit the final-package staging copy.
            if root==Path('deliverables') and 'records/work/' in p.as_posix():continue
            if not p.is_file() or p.suffix in ['.zip','.pyc','.stdout'] or any(v in p.parts for v in ['__pycache__','compile_tmp','runtime_check','flat_compile_check','compile_check']) or any(v.startswith(('portable-check-','patch-check-')) for v in p.parts):continue
            if p.suffix not in ['.tex','.pdf','.py','.json','.jsonl','.tsv','.md','.txt','.log','.png','.diff','.patch']:continue
            files.append((p,str(Path(base)/p.relative_to(root))))
    with zipfile.ZipFile(target,'w',zipfile.ZIP_DEFLATED,compresslevel=9) as z:
        z.writestr('CHECKPOINT_STATUS.md','# SGA 5 checkpoint '+str(a.number)+'\n\nCompleted readers at this checkpoint:\n\n'+'\n'.join('- '+v for v in a.finished)+'\n\nOther readers and records in this checkpoint are work in progress. Rebuild from the three original attached source archives and the included scripts. The final deliverables supersede all checkpoints.\n')
        for p,name in files:z.write(p,name)
    print(json.dumps({'file':target.name,'bytes':target.stat().st_size,'files':len(files),'completed_readers':a.finished}))

if __name__=='__main__':main()
