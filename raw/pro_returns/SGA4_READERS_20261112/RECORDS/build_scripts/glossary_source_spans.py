"""Enumerate the emphasized vocabulary in all 271 aligned source fragments.

The source line intervals come from the supplied translation filenames. Equal
emphasis sequences are paired in their retained order; the 23 unequal sequences
have explicit index maps below. Raw spans and the complete projection into a
lexical search phrase are retained in the output, including every exclusion.
"""
from en_common import *
import collections

# Zero-based source span maps, read against the complete two local lists.
MAPS={
 ('01',825):[(i,i+1) for i in range(6)],
 ('01',8706):[(0,0),(1,1),(2,3),(3,4)],
 ('04',31):[(0,0),((1,2),1)]+[(i,i-1) for i in range(3,10)],
 ('04',8026):[(i,i) for i in range(5)]+[(i,i-2) for i in range(7,15)],
 ('05',2301):[((0,1),0),(2,1),(4,2),(5,3),(6,4),(7,5)],
 ('05',3431):[(0,0),(1,1)]+[(i,i-1) for i in range(3,8)],
 ('06',2937):[(i,i) for i in range(9)]+[(i,i-1) for i in range(10,17)],
 ('06',3414):[(i,i) for i in range(12)]+[((12,13),12)]+[(i,i-1) for i in range(14,17)],
 ('07',43):[(i,i) for i in range(13)]+[((13,14),13)]+[(i,i-1) for i in range(15,23)],
 ('08',43):[(i,i) for i in range(16)]+[(i,i+1) for i in range(16,22)],
 ('09',279):[(i,i) for i in range(12)],
 ('09',1137):[(0,0),(1,2)],
 ('09',1340):[(0,1)],
 ('09',1460):[],
 ('12',43):[(0,0)],
 ('12',383):[(0,0)]+[(i,i+1) for i in range(1,5)],
 ('12',1601):[(i,i) for i in range(6)]+[(6,7),(7,8)],
 ('12',1925):[(0,0),(1,1),(2,2)],
 ('13',317):[(0,0),(1,1),(2,2),(4,3),(5,4)],
 ('15',1137):[(0,0),(1,1)]+[(i,i-1) for i in range(3,9)],
 ('16',1427):[(0,0),(1,1),(3,2)],
 ('17',261):[(i,i) for i in range(6)]+[((6,7),6),(8,7),((9,10),8)]+[(i,i-2) for i in range(11,18)],
 ('17',8601):[(i,i+1) for i in range(14)],
}

def spans(s):
    out=[]
    for m in active_matches(r'\\(?:emph|textit)\b',s):
        try:value,a,b,_=group(s,m.end())
        except ValueError:continue
        out.append(dict(start=m.start(),end=b,raw=value))
    return out

def phrase(raw):
    """Only explicit prose typography is projected; math stays in raw evidence."""
    value=uncomment(raw)
    # Every removed character is recoverable from the recorded raw value.
    if '$' in value or re.search(r'\\(?!emph\b|textit\b|textbf\b|textsc\b)',value):
        return '', 'mathematics or a semantic TeX command retained in the raw inventory'
    value=re.sub(r'\\(?:emph|textit|textbf|textsc)\s*','',value)
    value=value.replace('{','').replace('}','')
    value=re.sub(r'\s+',' ',value).strip()
    value=value.strip(' .,:;!?()[]«»`\"')
    if not value or not any(c.isalpha() for c in value):return '', 'no lexical term'
    if len(value.split())>8:return '', 'long emphasized statement retained in the raw inventory'
    return value, 'explicit typography projection; raw span retained'

def main():
    rows=[];terms=collections.defaultdict(set);census=[]
    for f in fragment_blocks(RELEASE.read_text()):
        text=(FRROOT/f['file']/(f['file']+'.tex')).read_text()
        lines=text.splitlines(True);offset=sum(map(len,lines[:f['a']-1]))
        ft=''.join(lines[f['a']-1:f['b']]);a=spans(ft);b=spans(f['text'])
        _,markers=french_marker_map(f['file'])
        key=(f['file'],f['a'])
        mapping=MAPS.get(key,[(i,i) for i in range(len(a))] if len(a)==len(b) else None)
        assert mapping is not None,(key,len(a),len(b))
        covered=set()
        for ai,bi in mapping:
            aa=ai if isinstance(ai,tuple) else (ai,)
            assert max(aa)<len(a) and bi<len(b),(key,aa,bi,len(a),len(b))
            covered.update(aa)
            frraw=' '.join(a[i]['raw'] for i in aa);enraw=b[bi]['raw']
            fr,frwhy=phrase(frraw);en,enwhy=phrase(enraw)
            pos=offset+a[aa[0]]['start']
            folio=next((p['folio'] for at,ln,p in reversed(markers) if at<=pos),'before first marker')
            row=dict(id='GE%04d'%(len(rows)+1),fragment=f['name'],expose=EXPOSE[f['file']],
                     page=folio,french_indices=','.join(map(str,aa)),english_index=bi,
                     french_raw=frraw,english_raw=enraw,french_term=fr,english_rendering=en,
                     alignment='reviewed explicit span map' if key in MAPS else 'equal ordered emphasis sequence',
                     projection=frwhy+'; '+enwhy,
                     status='lexical pair' if fr and en else 'raw source span retained')
            rows.append(row)
            if fr and en:terms[fr].add(en)
        for i,r in enumerate(a):
            census.append(dict(fragment=f['name'],french_index=i,raw=r['raw'],
                               disposition='paired' if i in covered else 'English emphasis boundary differs; raw source retained'))
    out=ROOT/'output/records'
    (out/'GLOSSARY_SOURCE_SPANS.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2)+'\n')
    write_tsv(out/'GLOSSARY_SOURCE_SPANS.tsv',rows,['id','fragment','expose','page','french_indices','english_index',
              'french_raw','english_raw','french_term','english_rendering','alignment','projection','status'])
    (out/'GLOSSARY_SOURCE_CENSUS.json').write_text(json.dumps(census,ensure_ascii=False,indent=2)+'\n')
    (ROOT/'output/shared/GLOSSARY_OBSERVED_TERMS.json').write_text(json.dumps(
        {k:sorted(v) for k,v in sorted(terms.items())},ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({'source_emphasis_spans':len(census),'paired_records':len(rows),
                      'lexical_pairs':sum(r['status']=='lexical pair' for r in rows),
                      'lexical_terms':len(terms),'explicit_maps':len(MAPS)}))
    return terms

if __name__=='__main__':main()
