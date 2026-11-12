"""Verify the supplied manifests before extracting the three source archives."""
from pathlib import Path
import csv, hashlib, io, json, zipfile

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'sources'
RECORDS = ROOT / 'output' / 'records'
SOURCE.mkdir(exist_ok=True)
RECORDS.mkdir(parents=True, exist_ok=True)
inventory = []
for archive in sorted((ROOT / 'upload').glob('*.zip')):
    with zipfile.ZipFile(archive) as z:
        rows = list(csv.DictReader(io.StringIO(z.read('MANIFEST.tsv').decode('utf-8-sig')), delimiter='\t'))
        for row in rows:
            name = row['path_in_zip']
            assert not name.startswith('/') and '..' not in Path(name).parts, name
            data = z.read(name)
            assert len(data) == int(row['bytes']), name
            assert hashlib.sha256(data).hexdigest() == row['sha256'], name
            destination = SOURCE / name
            destination.parent.mkdir(parents=True, exist_ok=True)
            destination.write_bytes(data)
            inventory.append({'archive':archive.name,'path':name,'bytes':len(data),'sha256':row['sha256'],'role':row['role']})
        print(archive.name, len(rows), 'manifest entries verified and extracted')
(RECORDS/'SOURCE_MANIFEST.json').write_text(json.dumps(inventory,ensure_ascii=False,indent=2)+'\n')
print('Total verified:',len(inventory))
