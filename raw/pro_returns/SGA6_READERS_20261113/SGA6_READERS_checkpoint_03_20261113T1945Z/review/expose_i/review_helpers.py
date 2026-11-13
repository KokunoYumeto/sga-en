#!/usr/bin/env python3
"""Append explicit observations; never infer an image verdict from a diff."""
import json,re
from pathlib import Path

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
REGISTRY=json.loads((ROOT/'build/registry.json').read_text())
BYID={r['id']:r for r in REGISTRY}

def read(name):
    p=HERE/name
    return [json.loads(x) for x in p.read_text().splitlines() if x.strip()] if p.exists() else []

def underline_words(text,plain=()):
    """Typeset inspected emphasis spans upright, keeping formulas independently marked."""
    pos=0;pieces=[];count=0
    while True:
        start=text.find(r'\emph{',pos)
        if start<0:pieces.append(text[pos:]);break
        pieces.append(text[pos:start]);depth=1;j=start+6
        while depth:
            if text[j]=='{' and text[j-1]!='\\':depth+=1
            if text[j]=='}' and text[j-1]!='\\':depth-=1
            j+=1
        content=text[start+6:j-1]
        alternatives=[re.escape(x) for x in sorted(plain,key=len,reverse=True)]+[r'\\\(.*?\\\)']
        pattern='('+'|'.join(alternatives)+')'
        for span in re.split(pattern,content,flags=re.S):
            if not span:continue
            if span.startswith(r'\(') or span in plain:pieces.append(span)
            elif span.strip():
                lead=span[:len(span)-len(span.lstrip())];tail=span[len(span.rstrip()):]
                body=span.strip()
                slashes=len(body)-len(body.rstrip('\\'))
                if tail and slashes%2:
                    body+=tail[0];tail=tail[1:]
                pieces.append(lead+r'\uline{'+body+'}'+tail)
            else:pieces.append(span)
        count+=1;pos=j
    return ''.join(pieces),count

class Review:
    def __init__(self):self.decisions=[];self.patches=[];self.pages=[];self.own=[]

    def finding(self,batch,index,printed,reason,region,verdict='confirmed',change=None,witness=None,actual_page=None):
        id=f'check/findings/findings_{batch}.json#{index}';item=BYID[id];f=item['data'];nominal_page=item['page'];page=nominal_page if actual_page is None else actual_page
        row=dict(source_id=id,page=page,type='finding',kind=f['kind'],verdict=verdict,
          printed_reading=printed,image=f'scan/SGA6_scan_360dpi.pdf#page={page+14}'+
          (f'; scan/SGA6_witness_300dpi.djvu#page={witness}' if witness else ''),
          region=region,change=change if change is not None else f.get('fix',f.get('corrected','Retain attached reading')),
          forms='French diplomatic and corrected; corresponding English transfer',reason=reason)
        self.decisions.append(row)
        # Each exact FIXLOG duplicate refers to the same observed glyph/text.
        for candidate in REGISTRY:
            c=candidate['data']
            if candidate['page']!=nominal_page:continue
            samefix=(candidate['type']=='fixlog' and f.get('fix') and
                c.get('old')==f['fix'].get('old') and c.get('new')==f['fix'].get('new'))
            samemisprint=(candidate['type']=='misprint' and f['kind']=='misprint_in_print' and
                c.get('source')==f'findings_{batch}.json' and c.get('where')==f.get('where'))
            if samefix or samemisprint:
                r=row.copy();r.update(source_id=candidate['id'],type=candidate['type'],related_finding=id)
                self.decisions.append(r)
        return id

    def source(self,id,printed,reason,region,verdict='confirmed',change='',witness=None,page=None):
        item=BYID[id];page=item['page'] if page is None else page
        self.decisions.append(dict(source_id=id,page=page,type=item['type'],verdict=verdict,
          printed_reading=printed,image=f'scan/SGA6_scan_360dpi.pdf#page={page+14}'+
          (f'; scan/SGA6_witness_300dpi.djvu#page={witness}' if witness else ''),
          region=region,change=change,forms='French layers; corresponding English transfer',reason=reason))

    def own_finding(self,id,page,printed,tex,change,reason,region,kind='underline',verdict='not applied and now applied',witness=None):
        self.own.append(dict(source_id=id,page=page,kind=kind,verdict=verdict,
            printed_reading=printed,tex=tex,change=change,reason=reason,region=region,
            image=f'scan/SGA6_scan_360dpi.pdf#page={page+14}'+
            (f'; scan/SGA6_witness_300dpi.djvu#page={witness}' if witness else '')))

    def patch(self,page,layer,old,new,source_id,reason,count=1):
        self.patches.append(dict(page=page,layer=layer,old=old,new=new,source_id=source_id,reason=reason,expected_count=count))

    def page(self,page,begins,ends,notes='',witness=None):
        self.pages.append(dict(page=page,pdf_page=page+14,fully_checked=True,
          image=f'scan/SGA6_scan_360dpi.pdf#page={page+14}',region='Complete printed page at216dpi, compared with both layer texts',
          begins=begins,ends=ends,witness_viewed=witness,
          notes='Word and symbol comparison personally completed. '+notes))

    def commit(self):
        combined=read('patches.jsonl');ids={p['source_id'] for p in self.patches}
        combined=[p for p in combined if p['source_id'] not in ids]+self.patches
        chunks={}
        for p in combined:
            for layer in ['diplomatic','current'] if p['layer']=='both' else [p['layer']]:
                key=(p['page'],layer)
                t=chunks.setdefault(key,(ROOT/f'build/page_packets/{key[0]}/{layer}.tex').read_text())
                assert t.count(p['old'])==p['expected_count'],(key,p['source_id'],t.count(p['old']),p['expected_count'])
                chunks[key]=t.replace(p['old'],p['new'])
        for filename,rows,key in [('decisions.jsonl',self.decisions,'source_id'),('own_findings.jsonl',self.own,'source_id'),('page_status.jsonl',self.pages,'page'),('patches.jsonl',self.patches,'source_id')]:
            if not rows:continue
            ids={r[key] for r in rows}
            prior=[r for r in read(filename) if r[key] not in ids]
            out=prior+rows
            if filename!='patches.jsonl':assert len({r[key] for r in out})==len(out),filename
            (HERE/filename).write_text(''.join(json.dumps(r,ensure_ascii=False)+'\n' for r in out))
        print(json.dumps({'new_decisions':len(self.decisions),'new_own_findings':len(self.own),'new_patches':len(self.patches),'new_fully_checked_pages':len(self.pages)}))
