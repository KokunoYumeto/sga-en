#!/usr/bin/env python3
"""Rebuild all eight final TeX files from the exact planned archive union.

The new scratch tree receives copies, never hard links, of deliverable files.
Original supplied input trees are linked as unchanged external inputs.
"""
from pathlib import Path
import hashlib,json,shutil,subprocess,sys
from package_release import plan,FORM_NAMES

ROOT=Path(__file__).resolve().parents[1]

def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()

def main():
    n=1
    while (ROOT/f'build/release_reconstruction_{n:02d}').exists():n+=1
    target=ROOT/f'build/release_reconstruction_{n:02d}'
    target.mkdir(parents=True)
    archives,_=plan();files={}
    for value in archives.values():
        assert not (set(files)&set(value));files.update(value)
    for rel,src in files.items():
        dest=target/rel;dest.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(src,dest)
    for name in ['fr','en','fixes','conventions','check','scan']:
        assert (ROOT/name).is_dir() and not (target/name).exists()
        (target/name).symlink_to(ROOT/name,target_is_directory=True)
    (target/'build').mkdir(exist_ok=True)
    logs=ROOT/f'build/release_reconstruction_logs_{n:02d}';logs.mkdir()
    commands=[
      ['scripts/intake.py'],
      ['scripts/build_french.py','--final'],
      ['review/english/collect_english_aggregate.py'],
      ['review/english/build_english_aggregate.py','--final']]
    runs=[]
    for i,command in enumerate(commands,1):
        p=subprocess.run([sys.executable]+command,cwd=target,text=True,capture_output=True)
        (logs/f'command_{i:02d}.txt').write_text(p.stdout+p.stderr)
        runs.append(dict(command='python3 '+' '.join(command),exit_code=p.returncode))
        print(json.dumps(runs[-1]),flush=True)
        assert p.returncode==0,'Fresh reconstruction failed; see the scratch command transcript.'
    compared=[]
    for language,names in FORM_NAMES.items():
        directory='readers/fr/final' if language=='FR' else 'review/english/final'
        for name in names:
            rel=directory+'/'+name+'.tex'
            actual=sha(target/rel);expected=sha(ROOT/rel)
            assert actual==expected,rel
            compared.append(dict(path=rel,delivered_sha256=expected,reconstructed_sha256=actual,identical=True))
    old_catalog=json.loads((ROOT/'review/english/aggregate/INPUT_CATALOG.json').read_text())
    new_catalog=json.loads((target/'review/english/aggregate/INPUT_CATALOG.json').read_text())
    for before,after in zip(old_catalog['packets'],new_catalog['packets']):
        assert before['directory']==after['directory'] and before['manifest']==after['manifest']
    result=dict(passed=True,scope='Fresh source reconstruction from the exact planned union of the three release archives plus the originally supplied input trees.',
      planned_payload_files=len(files),commands=runs,source_files=compared,
      exact_English_packets_verified=len(new_catalog['packets']),
      exact_packet_members_verified=sum(r['manifest']['verified_files'] for r in new_catalog['packets']),
      packet_manifests_unchanged=True,final_TeX_reconstructed_byte_for_byte=8,
      PDF_scope='Delivered PDFs have their independent unchanged-source two-pass compile receipts; this fresh reconstruction verifies the identical TeX bytes and does not replace those PDFs.',
      private_runtime_transcripts='Kept only in reproducible scratch output; no local absolute path or raw runtime log is exported.')
    (ROOT/'records/RELEASE_RECONSTRUCTION.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(dict(passed=True,source_files=8,English_packets=result['exact_English_packets_verified'],packet_members=result['exact_packet_members_verified'])),flush=True)

if __name__=='__main__':main()
