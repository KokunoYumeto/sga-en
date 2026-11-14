#!/usr/bin/env python3
"""Capture the corrected macro-count metadata without overwriting its history."""
from pathlib import Path
import json,hashlib

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]

def main():
    rows=[]
    for relative in ['review/english/EN_MACRO_EXPANSION_DECISIONS.json','review/english/EN_AGGREGATE_MACRO_TRANSPORTS.jsonl']:
        source=ROOT/relative;data=source.read_bytes()
        target=HERE/'input_snapshots/macro_decisions_final'/relative
        target.parent.mkdir(parents=True,exist_ok=True)
        if target.exists():assert target.read_bytes()==data,('Refuse to overwrite captured final input',relative)
        else:target.write_bytes(data)
        previous=HERE/'input_snapshots'/relative
        rows.append(dict(source=relative,snapshot=str(target.relative_to(ROOT)),sha256=hashlib.sha256(data).hexdigest(),bytes=len(data),
                         earlier_snapshot=str(previous.relative_to(ROOT)),earlier_sha256=hashlib.sha256(previous.read_bytes()).hexdigest()))
    (HERE/'FINAL_MACRO_INPUT_MANIFEST.json').write_text(json.dumps(rows,indent=2)+'\n')
    (HERE/'MACRO_COUNT_CLARIFICATION.json').write_text(json.dumps(dict(source_id='EN-AGG-MACRO-RED-502',earlier_metadata_count=30,corrected_macro_invocation_count=20,
        reason='The English assembly owner confirmed that30 was an arithmetic error and corrected the shared metadata to20. The source-scoped census finds20 identical literal red-command invocations in FR and EN, excluding definitions/comments.',
        separate_literal_forms=[dict(page=545,French=r'\mathrm{red}',English=r'\mathrm{red}',count=3),dict(page=597,French=r'\text{réd}',English=r'\text{red}',count=1)],
        body_text_changed=False,earlier_snapshot_preserved=True),ensure_ascii=False,indent=2)+'\n')
    print('Captured final macro metadata with its preserved earlier snapshot.')

if __name__=='__main__':main()
