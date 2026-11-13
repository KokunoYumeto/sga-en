"""Record immutable checkpoint hashes and returned persistent file identities."""
from pathlib import Path
import csv,hashlib,sys

ROOT=Path(__file__).resolve().parents[1]
TARGET=ROOT/'work/records/CHECKPOINT_INDEX.tsv'
INITIAL={
1:'libfile_fde3_f-7fcf224928c88191ae07ff0684fd5ca8_c6789dc4b4d481919ad633aabe6d84d0',
2:'libfile_fde3_f-8d44a2a41c2c8191b69349a58275e47d_c6789dc4b4d481919ad633aabe6d84d0',
3:'libfile_fde3_f-6d0da76d558c8191b13913383e70c69b_c6789dc4b4d481919ad633aabe6d84d0',
4:'libfile_fde3_f-3dd149ec8e648191a8f095b793b2f7cc_c6789dc4b4d481919ad633aabe6d84d0',
5:'libfile_fde3_f-79d1921c291c8191a013aa67154810e4_c6789dc4b4d481919ad633aabe6d84d0',
6:'libfile_fde3_f-ddab31f54ea08191bea1e78953b71f6a_c6789dc4b4d481919ad633aabe6d84d0',
}
def record(number=None,file_id='',milestone=''):
    prior={}
    if TARGET.exists():
        with TARGET.open(newline='') as f:prior={int(r['number']):r for r in csv.DictReader(f,delimiter='\t')}
    rows=[]
    for p in sorted((ROOT/'output').glob('SGA4HALF_READERS_checkpoint_*.zip')):
        n=int(p.stem.rsplit('_',1)[1]);old=prior.get(n,{})
        ident=file_id if n==number else old.get('library_file_id',INITIAL.get(n,''))
        status='uploaded' if ident else 'unpublished candidate'
        note=milestone if n==number else old.get('milestone','Completed part/progress checkpoint')
        if n in {7,8} and not ident:
            status='unpublished; rejected by privacy preflight'
            note='Superseded by sanitized checkpoint09 and final archives; candidate is never distributed, overwritten or deleted.'
        rows.append(dict(number=n,filename=p.name,bytes=p.stat().st_size,sha256=hashlib.sha256(p.read_bytes()).hexdigest(),status=status,library_file_id=ident,url=('https://chatgpt.com/library?file_id='+ident+'&account_id=personal') if ident else '',milestone=note,final_replacement='The three final SGA4HALF_READERS archives; see CHECKPOINT_RECONCILIATION.tsv.'))
    fields=['number','filename','bytes','sha256','status','library_file_id','url','milestone','final_replacement']
    with TARGET.open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=fields,delimiter='\t');w.writeheader();w.writerows(rows)
    return rows

if __name__=='__main__':
    rows=record(int(sys.argv[1]) if len(sys.argv)>1 else None,sys.argv[2] if len(sys.argv)>2 else '',sys.argv[3] if len(sys.argv)>3 else '')
    print('Checkpoint index rows:',len(rows))
