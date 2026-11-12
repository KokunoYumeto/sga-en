"""Record a successfully saved completed-reader checkpoint without private paths."""
import argparse,datetime,hashlib,json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
REC=ROOT/'output/records'

def main():
    p=argparse.ArgumentParser()
    p.add_argument('number',type=int)
    p.add_argument('library_file_id')
    p.add_argument('trigger_reader')
    args=p.parse_args()
    assert args.library_file_id.startswith('libfile_')
    archive=ROOT/'deliverables'/f'SGA4_READERS_checkpoint_{args.number}.zip'
    qa=json.loads((REC/(args.trigger_reader+'_PDF_QA.json')).read_text())
    assert not qa['text_spans_outside_physical_page']
    assert not qa['unresolved_reference_warnings']
    file=REC/'CHECKPOINTS.json'
    previous=json.loads(file.read_text()) if file.exists() else []
    completed=[]
    for row in previous:
        if row.get('trigger_reader') and row['trigger_reader'] not in completed:
            completed.append(row['trigger_reader'])
    if args.trigger_reader not in completed:completed.append(args.trigger_reader)
    row=dict(name=archive.name,checkpoint_number=args.number,
      trigger_reader=args.trigger_reader,finished_readers=len(completed),
      acknowledged_completed_readers=completed,
      status='Saved completion checkpoint; records for concurrent work reflect their state at packaging.',
      bytes=archive.stat().st_size,sha256=hashlib.sha256(archive.read_bytes()).hexdigest(),
      library_file_id=args.library_file_id,
      trigger_source_sha256=qa['source_sha256'],trigger_pdf_sha256=qa['pdf_sha256'],
      saved_at=datetime.datetime.now(datetime.timezone.utc).isoformat())
    assert not any(r.get('checkpoint_number')==args.number for r in previous)
    previous.append(row)
    file.write_text(json.dumps(previous,ensure_ascii=False,indent=2)+'\n')
    print(archive.name,'recorded; completed-reader acknowledgements',len(completed))

if __name__=='__main__':main()
