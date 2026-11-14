#!/usr/bin/env python3
"""Seal this assigned contribution while leaving the earlier V seal untouched."""
from pathlib import Path
import hashlib,json,re,shutil,sys
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[3]
sys.path.insert(0,str(HERE))
from audit_complete_contribution import main as audit
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def put(p,value):p.write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n')
checked=audit();counts=checked['counts']
handoff=dict(scope='Prepared English V297–364 and VI365–393; assigned range complete',counts=counts,first_native_target='sga6.e05.expose',VI_first_native_target='sga6.e06.expose',next_native_target='sga6.e06.sec.4',replacement='Consume all20 exact contiguous native replacement spans in translation_spans.jsonl. VI consists of six chunks365–369,370–374,375–379,380–384,385–389 and390–393.',source_reference='Both complete reviewed French forms are saved in source_packets with per-patch reference hashes. The closure audit confirms exact full-page text equality with the current ordered loader for all97 pages in both forms.',literal_checks='Current3077 and diplomatic3075 primary units,plus two starred align displays per branch,have zero unexpected units. VI contributes941 primary units in each branch. Thirty-five complete lexical unit pairs account for104 approved difference side-units.',manual_comparison='Every prose clause,formula placement,original author note,observed word-rule group and source alternative was manually compared in the registered batches;96 internal page joins are explicitly recorded.',macro_boundaries=checked['macro_boundaries'],original_author_note=checked['original_note'],legacy_target_mapping='On385,sga6.e06.eq.2-5-2 remains attached to the same derived beta map as in native English. Its actual source display number is2.5.3. The distinct source section map2.5.2 is also restored; the transfer ledger records this mapping.',source_claims='The source385 section-space equality and390 stopping-index passage are retained in both author bodies with their exact restriction/forgetful maps and counterexamples separately attributed. The earlier V author claims remain unchanged with their proof packets.',next_contribution='review/english/contributions/expose_vi_394_415 starts exactly at sga6.e06.sec.4 and owns the415/416 native/reviewed continuation blocks.',final_scope='The last local variant scope_end is empty because393 is this packet end. Bound it by the actual394 marker/section4 boundary during aggregate integration.',earlier_V_seal=checked['V_immutable_snapshot'],status='Prepared,fully manually compared,and locally exact-checked; not yet registered or compiled by this contributor.',limitations=checked['limitations'])
put(HERE/'HANDOFF_COMPLETE.json',handoff)
(HERE/'HANDOFF_COMPLETE.md').write_text('''# Prepared English V297–364 and VI365–393

The assigned contribution is complete through393. Its20 exact native replacement spans run continuously from `sga6.e05.expose` to immediately before `sga6.e06.sec.4`. All204 native stable targets are retained in order. V has68 folios in14 chunks; VI has29 folios in six chunks:365–369,370–374,375–379,380–384,385–389 and390–393. The separate late-VI contribution starts at the retained section4 target and owns394–415 and both415/416 continuation blocks.

Every prose clause,formula placement,original note,source word-rule group and explicit source alternative has been manually compared with both reviewed French forms. The final closure audit also compares the entire saved French text against the current exact ordered loader: all97 pages agree in both forms. There are117 provisional English variant groups,of which47 belong to VI,and1,247 transfer records. VI preserves its complete graded-Module proofs,the full arbitrary sheafification construction,the cone argument,and the full torsor/representation argument that native English had shortened.

The primary literal comparison covers3,077 current and3,075 diplomatic mathematical units; VI contributes941 in each branch. Two complete starred displays per branch are separately compared in exact order. Both checks have zero unexpected units. Thirty-five individually reviewed complete lexical unit pairs account for104 approved difference side-units. The32 text-mode variant arguments also have balanced inline and dollar delimiters in both readings. These checks do not certify prose or rendered typography;the manual passage comparison is separately recorded.

All96 internal source-folio joins are explicit:33 paragraph boundaries and63 continuations. The nine native commands between389 and390 remain before the source induction continuation,without importing a blank paragraph into the source `on / achève` sentence. Both native and reviewed macro blocks remain at323/324,346/347 and364/365. The sole original author note in this contribution is the observed baseline parenthesized star on374: “This proof is due to J.P. Jouanolou.” Its exact call position and source ID are in `author_notes.tsv`.

The source385 section-space equality remains in both author bodies. Its audit retains the precise restriction of degree-two homogeneous polynomials to the affine chart,the section outside that image,the truncation example,and the well-defined fraction map. The separately justified alpha-subscript change has its own English branch. The source390 flag stopping-index passage also remains,with the precise forgetful map from the complete flag of a three-dimensional vector space to its rank-one quotient space and its projective-line fiber documented separately. No replacement author theorem or source paragraph is inserted.

On385,the legacy stable target named `sga6.e06.eq.2-5-2` remains at the same derived natural transformation as in native English;the displayed source number there is2.5.3. The distinct section map2.5.2 is restored earlier. The transfer ledger records this exact target-to-map correspondence so links can be reviewed at assembly.

The earlier immutable V snapshot is unchanged,and all14 live V raw chunks still match it. This final packet includes24 attributed proof-audit copies and48 source-anchored terminology candidates. Shared registration,final variant numbers,glossary integration,macro expansion,compilation and PDF visual inspection remain with the English assembly owner. This contributor has not compiled or visually inspected an English PDF for this packet. The final local variant scope must stop at394 during integration.
''')
deps=[]
base=['review/english/EN_PARALLEL_TRANSFER_HANDOFF.md','review/english/SGA6_EN_native_flattened_UNVERIFIED.tex','review/english/reviewed_french.py','review/english/verify_reviewed_english.py','review/english/check_contribution.py','review/expose_v/FROZEN_HANDOFF.md','review/expose_vi/HANDOFF.md']
for folder in ['expose_v','expose_v_rendering','expose_vi','expose_vi_amendments','middle']:
    for name in ['decisions.jsonl','own_findings.jsonl','patches.jsonl','page_status.jsonl']:
        if (ROOT/'review'/folder/name).exists():base.append(f'review/{folder}/{name}')
for rel in base:
    p=ROOT/rel;deps.append(dict(path=rel,sha256=sha(p),bytes=p.stat().st_size))
put(HERE/'EXTERNAL_INPUT_HASHES_COMPLETE.json',deps)
snapshot=ROOT/'build/review_snapshots/english_v297_364_vi365_393_complete'
assert not snapshot.exists(),'Never overwrite a sealed snapshot'
snapshot.parent.mkdir(parents=True,exist_ok=True)
shutil.copytree(HERE,snapshot,ignore=lambda directory,names:[n for n in names if n=='__pycache__' or n.endswith(('.aux','.out'))])
files=[dict(path=p.relative_to(snapshot).as_posix(),sha256=sha(p),bytes=p.stat().st_size) for p in sorted(snapshot.rglob('*')) if p.is_file()]
put(snapshot/'MANIFEST.json',dict(scope=handoff['scope'],files=files,file_count=len(files),counts=counts,limitations=handoff['limitations']))
manifest_sha=sha(snapshot/'MANIFEST.json')
for p in snapshot.rglob('*'):p.chmod(0o555 if p.is_dir() else 0o444)
snapshot.chmod(0o555)
receipt=dict(snapshot=snapshot.relative_to(ROOT).as_posix(),manifest_sha256=manifest_sha,manifested_files=len(files),counts=counts,next_native_target='sga6.e06.sec.4')
put(HERE/'SEAL_COMPLETE_RECEIPT.json',receipt)
print(json.dumps(receipt,ensure_ascii=False,indent=2))
