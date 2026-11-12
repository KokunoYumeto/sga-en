#!/usr/bin/env python3
"""Verify the supplied manifests before extracting the three source archives.

Only ZIP-internal names are written to the audit; private source paths are omitted.
"""
import csv
import hashlib
import io
import json
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEST = ROOT / 'sources'
OUT = ROOT / 'output' / 'records'


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    results = []
    for archive in sorted((ROOT / 'upload').glob('SGA7_*.zip')):
        with zipfile.ZipFile(archive) as z:
            records = list(csv.DictReader(io.StringIO(z.read('MANIFEST.tsv').decode('utf-8-sig')), delimiter='\t'))
            checked = []
            for r in records:
                name = r['path_in_zip']
                path = Path(name)
                assert not path.is_absolute() and '..' not in path.parts, name
                data = z.read(name)
                digest = hashlib.sha256(data).hexdigest()
                assert len(data) == int(r['bytes']), name
                assert digest == r['sha256'], name
                checked.append({'path_in_zip': name, 'bytes': len(data), 'sha256': digest, 'role': r['role']})
            for r in checked:
                p = DEST / r['path_in_zip']
                p.parent.mkdir(parents=True, exist_ok=True)
                p.write_bytes(z.read(r['path_in_zip']))
            results.append({'archive': archive.name, 'sha256': hashlib.sha256(archive.read_bytes()).hexdigest(),
                            'manifest_entries': len(checked), 'verified': len(checked), 'files': checked})
    (OUT / 'INPUT_VERIFICATION.json').write_text(json.dumps(results, ensure_ascii=False, indent=2)+'\n')
    print(json.dumps([{k:v for k,v in r.items() if k != 'files'} for r in results], indent=2))


if __name__ == '__main__':
    main()
