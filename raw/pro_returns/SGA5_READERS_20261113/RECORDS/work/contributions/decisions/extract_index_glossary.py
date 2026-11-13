#!/usr/bin/env python3
"""Extract exact bilingual index terms, preserving order and reference text."""
from pathlib import Path
import argparse,csv,hashlib,json,re
p=argparse.ArgumentParser()
p.add_argument('--fr',default='work/sources/SGA5_FR/fr/sga5/current/s5.tex')
p.add_argument('--en',default='work/contributions/english/EN_corrected_flat.tex')
p.add_argument('--out',default='work/contributions/decisions')
a=p.parse_args();F=Path(a.fr).read_text();E=Path(a.en).read_text();out=Path(a.out);out.mkdir(parents=True,exist_ok=True)

def arg(t,start):
    while t[start].isspace():start+=1
    assert t[start]=='{'
    depth=1;i=start+1
    while depth:
        assert i<len(t),'Unclosed index argument'
        if t[i]=='\\':i+=2;continue
        if t[i]=='{':depth+=1
        elif t[i]=='}':depth-=1
        i+=1
    return t[start+1:i-1],i

def extract(t,language):
    result=[]
    for m in re.finditer(r'^\\sgaindexentry(?=\{)',t,re.M):
        term,j=arg(t,m.end());ref,j=arg(t,j)
        before=t[:m.start()]
        notations=max(before.rfind('Index des notations'),before.rfind('Index of Notation'))
        terminology=max(before.rfind('Index terminologique'),before.rfind('Terminological Index'))
        category='notation' if notations>terminology else 'term'
        markers=list(re.finditer(r'folio\s+(\d+)\s+%',before))
        result.append({'term_tex':term,'references_tex':ref,'index_kind':category,'source_line':before.count('\n')+1,'source_char_offset':m.start(),'index_folio':int(markers[-1].group(1)) if markers else None})
    return result

def ref_compare(s):
    # This is a comparison key only: exact input references remain in outputs.
    return s.replace('déf','def').replace(r'n\textsuperscript{o}','no.').replace('~',' ')

fr=extract(F,'FR');en=extract(E,'EN');assert len(fr)==len(en),(len(fr),len(en))
rows=[];mismatches=[]
for i,(f,e) in enumerate(zip(fr,en),1):
    same=ref_compare(f['references_tex'])==ref_compare(e['references_tex'])
    assert f['index_kind']==e['index_kind'],i
    row={'id':f'INDEX-{i:03d}','kind':f['index_kind'],'French_term_or_notation':f['term_tex'],'English_rendering':e['term_tex'],'French_references':f['references_tex'],'English_references':e['references_tex'],'index_folio':f['index_folio'],'FR_source_line':f['source_line'],'EN_source_line':e['source_line'],'FR_char_offset':f['source_char_offset'],'EN_char_offset':e['source_char_offset'],'reference_match':same,'alignment':'same ordinal entry; reference text checked after translating def/no. labels only'}
    rows.append(row)
    if not same:mismatches.append(row['id'])
(out/'index_glossary_pairs.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2)+'\n')
with (out/'index_glossary_pairs.tsv').open('w',newline='') as f:
    w=csv.DictWriter(f,fieldnames=list(rows[0]),delimiter='\t');w.writeheader();w.writerows(rows)
summary={'entries':len(rows),'terminology_entries':sum(r['kind']=='term' for r in rows),'notation_entries':sum(r['kind']=='notation' for r in rows),'reference_mismatches':mismatches,'FR_source_archive_member':'fr/sga5/current/s5.tex','EN_basis':'generated corrected English before folio annotations','FR_source_sha256':hashlib.sha256(F.encode()).hexdigest(),'EN_source_sha256':hashlib.sha256(E.encode()).hexdigest(),'comparison_note':'The comparator changes only the language of reference labels for matching; exact TeX terms and references are preserved in both output columns.'}
(out/'index_glossary_summary.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(summary))
