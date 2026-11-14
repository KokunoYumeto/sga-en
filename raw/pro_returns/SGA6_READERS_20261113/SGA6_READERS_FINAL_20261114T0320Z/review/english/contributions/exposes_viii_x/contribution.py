#!/usr/bin/env python3
"""Build this contribution only, with literal reviewed French math placeholders."""
from pathlib import Path
import sys,re,json,hashlib,collections
ROOT=Path(__file__).resolve().parents[4]
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'review/english'))
from reviewed_french import load_reviewed_pages
from verify_reviewed_english import MATH,split

def sha(s): return hashlib.sha256(s.encode()).hexdigest()
def dump(path,data): path.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
def jsonl(path,rows): path.write_text(''.join(json.dumps(x,ensure_ascii=False)+'\n' for x in rows))
def marker(page): return f'%%%%%%%%%%  scan idx {page+13}  |  folio {page}  %%%%%%%%%%'

def prepare(first,last):
    for layer in ['current','diplomatic']:
        pages,record=load_reviewed_pages(last,layer,start=first)
        dump(HERE/f'reference_{first}_{last}_{layer}.json',record)
        for page,text in pages.items():
            dest=HERE/'source_packets'/str(page);dest.mkdir(parents=True,exist_ok=True)
            (dest/f'{layer}.tex').write_text(text)
            if layer=='current':
                units=[]
                def mask(m):
                    key=f'@@M{len(units)}@@';units.append(m.group());return key
                masked=MATH.sub(mask,text)
                (dest/'masked.tex').write_text(masked);dump(dest/'units.json',units)
                print(f'PAGE {page}\n{masked}')

def make_chunk(expose,first,last):
    out=[]
    for page in range(first,last+1):
        source=HERE/'source_packets'/str(page)
        units=json.loads((source/'units.json').read_text())
        pairs=json.loads((HERE/'lexical_math_pairs.json').read_text()) if (HERE/'lexical_math_pairs.json').exists() else []
        lex={p['French_literal_unit']:p['English_literal_unit'] for p in pairs if p['page']==page and p['layer'] in ('current','both')}
        units=[lex.get(u,u) for u in units]
        text=(HERE/'translations'/f'{page}.tex').read_text()
        seen=collections.Counter(int(n) for n in re.findall(r'@@M(\d+)@@',text))
        assert seen==collections.Counter(range(len(units))),(page,seen,range(len(units)))
        text=re.sub(r'@@M(\d+)@@',lambda m:units[int(m.group(1))],text)
        visible=f'\\SGAPrintPage{{{page}}}%\n'
        if '@@PAGE_MARK@@' in text:
            assert text.count('@@PAGE_MARK@@')==1,page
            text=text.replace('@@PAGE_MARK@@',visible)
        else:text=visible+text
        out.append(marker(page)+'\n'+text)
    result='\n'.join(out)
    path=HERE/f'EN_EXPOSE_{expose}_P{first}_{last}.tex';path.write_text(result)
    return result

def source_decision(source):
    for folder in ['expose_viii','expose_ix','expose_x','expose_x_amendments']:
        for name in ['decisions.jsonl','own_findings.jsonl']:
            path=ROOT/'review'/folder/name
            if not path.exists():continue
            for line in path.read_text().splitlines():
                record=json.loads(line)
                if record.get('source_id')==source:return record
    raise KeyError(source)

def build_records():
    native=(ROOT/'review/english/SGA6_EN_native_flattened_UNVERIFIED.tex').read_text()
    configs=json.loads((HERE/'batches.json').read_text())
    final_folio=max(c['last'] for c in configs)
    variants=[];ledger=[];spans=[]
    native_cursor=0
    for config in configs:
        first,last=config['first'],config['last'];expose=config['expose']
        chunk=make_chunk(expose,first,last)
        a=native.index(config['native_start'],native_cursor);b=native.index(config['native_end'],a)
        if native_cursor:assert a==native_cursor,(first,'noncontiguous native span',native_cursor,a)
        native_cursor=b
        old=native[a:b]
        targets=lambda t:re.findall(r'\\sgaStableTarget(?:Inline)?\{([^}]+)\}',t)
        assert targets(old)==targets(chunk),(first,'stable targets',targets(old),targets(chunk))
        spans.append(dict(id=f'EN-CONTRIB-{expose}-{first}-{last}',first_folio=first,last_folio=last,old=old,new=chunk,native_span_sha256=sha(old),first_stable_target=targets(old)[0] if targets(old) else None,last_stable_target=targets(old)[-1] if targets(old) else None,covered_folios=list(range(first,last+1)),status='manual complete prose and formula placement comparison against reviewed French; local two-branch check separately recorded',source=config['source'],reason=config['reason']))
        local=[]
        for entry in config.get('variants',[]):
            d=source_decision(entry['source'])
            assert d['page']==entry['page'],(entry['id'],'source decision page',d['page'],entry['page'])
            ds=[d]+[source_decision(s) for s in entry.get('related_sources',[])]
            assert all(x['page']==entry['page'] for x in ds)
            reason=' '.join(x['source_id']+': '+x['reason'] for x in ds) if len(ds)>1 else d['reason']
            v=dict(entry,corrected=entry['old'],scope_start=marker(entry['page']),scope_end=marker(entry['page']+1) if entry['page']<final_folio else '',scan_image=d['image'],scan_region=d['region'],reason=reason)
            local.append(v);variants.append(v)
            for atom in ds:
                ledger.append(dict(record_type='source_variant',page=v['page'],source_id=atom['source_id'],English_variant=v['id'],printed=v['printed'],corrected=v['corrected'],reason=atom['reason'],source_image_attribution=atom['image'],source_region=atom['region'],rendering_group=('complete display branch preserving all separately adjudicated local differences' if v['mode']=='display' else 'complete mathematical expression branch preserving all separately adjudicated local differences') if len(ds)>1 else 'single source difference'))
        for layer,key in [('current','corrected'),('diplomatic','printed')]:
            en_text=chunk
            for v in local:
                x=en_text.index(v['scope_start']);y=en_text.index(v['scope_end'],x) if v['scope_end'] and v['scope_end'] in en_text[x:] else len(en_text)
                part=en_text[x:y];assert part.count(v['old'])==1,(v['id'],part.count(v['old']))
                en_text=en_text[:x]+part.replace(v['old'],v[key],1)+en_text[y:]
            en=split(en_text)
            ref=json.loads((HERE/f'reference_{first}_{last}_{layer}.json').read_text())
            for page in range(first,last+1):
                fr=(HERE/'source_packets'/str(page)/f'{layer}.tex').read_text()
                units=[m.group() for m in MATH.finditer(fr)];enu=[m.group() for m in MATH.finditer(en[page])]
                cmds=lambda us:dict(sorted(collections.Counter(re.findall(r'\\(?:[A-Za-z]+|.)',''.join(us))).items()))
                ledger.append(dict(record_type='page_transfer_inventory',page=page,layer=layer,source=next(x for x in ref['bases'] if x['page']==page),reviewed_French_page_sha256=sha(fr),English_page_sha256=sha(en[page]),French_math_units=len(units),English_math_units=len(enu),French_math_command_inventory=cmds(units),English_math_command_inventory=cmds(enu),French_author_notes=re.findall(r'\\SGAAuthorFoot(?:note|Mark|Text)\{[^}]+\}',fr),English_author_notes=re.findall(r'\\SGAAuthorFoot(?:note|Mark|Text)\{[^}]+\}',en[page]),decision='Every paragraph, complete mathematical unit and its placement was compared with the reviewed French page. Exact literal branch verification is in literal_math_verification.json. Source image observations are attributed to the frozen French audit, not newly claimed by this translation check.'))
            for category in ['applied_patches','already_present_exact_patches','baseline_differences']:
                for p in ref.get(category,[]):
                    matched=[v['id'] for v in local if p.get('source_id') in [v['source']]+v.get('related_sources',[])]
                    ledger.append(dict(record_type='French_reference_'+category,reference_layer=layer,**p,English_variants=matched,decision='Exact patch-composed French reading transferred into the corresponding English branch; source-only spelling and agreement dispositions and all branch variants are explicitly recorded in the batch notes. Both-form glyphs and formula syntax remain literal.'))
        for note in config.get('notes',[]):ledger.append(dict(record_type='passage_disposition',**note))
        ledger.extend(config.get('extra_records',[]))
        for sid in config.get('retained_proof_audits',[]):
            d=source_decision(sid)
            ledger.append(dict(record_type='attributed_retained_author_argument',source_record=d,decision='The English author body retains the source wording in both branches. This independently checked mathematical scope/proof packet belongs to the French audit and is transferred separately without expanding the author body.'))
    jsonl(HERE/'variants.jsonl',variants);jsonl(HERE/'transfer.jsonl',ledger);jsonl(HERE/'translation_spans.jsonl',spans)
    print(json.dumps(dict(chunks=len(configs),pages=sum(c['last']-c['first']+1 for c in configs),variants=len(variants),transfer_records=len(ledger))))

if __name__=='__main__':
    if sys.argv[1]=='prepare':prepare(int(sys.argv[2]),int(sys.argv[3]))
    elif sys.argv[1]=='chunk':make_chunk(sys.argv[2],int(sys.argv[3]),int(sys.argv[4]))
    elif sys.argv[1]=='records':build_records()
