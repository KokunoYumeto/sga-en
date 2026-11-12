"""Independent source-to-dossier and note-preservation audit for both masters."""
from pathlib import Path
import bisect,collections,hashlib,json,re
from en_common import group,fragment_blocks,sanitize
from fr_core import FILES,EXP,body
ROOT=Path(__file__).resolve().parents[1]

def commands(s):
    """Yield active TeX control words, treating escaped symbols and comments literally."""
    i=0;pattern=re.compile(r'\\[A-Za-z@]+|\\.',re.S)
    while i<len(s):
        if s[i]=='%':
            j=s.find('\n',i);i=len(s) if j<0 else j+1;continue
        if s[i]!='\\':i+=1;continue
        m=pattern.match(s,i)
        if not m:i+=1;continue
        end=i+len(m.group());yield m.group(),i,end;i=end

def calls(s):
    out=[]
    for name,start,end in commands(s):
        if name not in [r'\sisi',r'\nde',r'\ndetext',r'\ndemark',r'\acorriger']:continue
        prefix=s[s.rfind('\n',0,start)+1:start]
        if re.search(r'\\(?:def|newcommand|renewcommand|providecommand|DeclareMathOperator)\b',prefix):continue
        args=[];ranges=[];pos=end
        for _ in range(2 if name==r'\sisi' else 0 if name==r'\ndemark' else 1):
            text,a,b,braced=group(s,pos);args.append(text);ranges.append((a+int(braced),b-int(braced)));pos=b
        out.append({'command':name,'start':start,'end':pos,'arguments':args,'argument_ranges':ranges,
                    'line':s.count('\n',0,start)+1})
    for r in out:
        r['ancestors']=[{'command':p['command'],'start':p['start'],'argument':j+1} for p in out for j,(a,b) in enumerate(p['argument_ranges']) if a<=r['start']<b]
    return out

def main_source(raw):
    m=re.search(r'\\else\s*\n\\chapter',raw)
    a=m.end()-len(r'\chapter') if m else 0
    b=raw.rfind(r'\ifx\danslelivre\undefined')
    if b<a:b=len(raw)
    return a,b

def inventory():
    initial=json.loads((ROOT/'work_fr/initial_layers.json').read_text())
    byid={r['id']:r for r in initial['org']};allfr=[];diff=[];stats=[]
    for f in FILES:
        rel=f'fr/A_orgogozo_snapshot_71766d9/{f}/{f}.tex';raw=(ROOT/'sources'/rel).read_text()
        a,b=main_source(raw);cc=[x for x in calls(raw) if a<=x['start']<b]
        top=[x for x in cc if x['command']==r'\sisi' and not x['ancestors']]
        for n,r in enumerate(top,1):
            r={**r,'id':f'ORG-{f}-{n:04d}','file':f,'expose':EXP[f],'source':rel}
            old=byid.get(r['id']);r['same_as_d_source_record']=bool(old and r['arguments']==[old['printed'],old['corrected']])
            if not r['same_as_d_source_record']:diff.append({'id':r['id'],'A':r['arguments'],'D':[old['printed'],old['corrected']] if old else None})
            allfr.append(r)
        stats.append({'file':f,'expose':EXP[f],'outer_pairs':len(top),'all_sisi':sum(x['command']==r'\sisi' for x in cc),
                      'nde':sum(x['command']==r'\nde' for x in cc),'ndetext':sum(x['command']==r'\ndetext' for x in cc),
                      'ndemark':sum(x['command']==r'\ndemark' for x in cc)})
    released=(ROOT/'sources/en/C_release_20261112/04_SGA4_EN_COMPLETE_READER.tex').read_text()
    lo=released.index(r'\mainmatter');all_en=[x for x in calls(released) if x['start']>lo]
    top_en=[x for x in all_en if x['command']==r'\sisi' and not x['ancestors']]
    for n,r in enumerate(top_en,1):r['id']=f'EN-ORG-{n:04d}'
    result={'french_outer_pairs':allfr,'french_counts':stats,'french_A_D_differences':diff,'english_outer_pairs':top_en,
            'english_raw_note_calls':[x for x in all_en if x['command'] in [r'\nde',r'\ndetext',r'\ndemark']]}
    (ROOT/'work_fr/human_source_inventory.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    print('FR original outer pairs',len(allfr),'D dossier inventory',len(byid),'A/D differences',len(diff))
    print('FR per-expose',stats)
    print('EN released outer pairs',len(top_en),'all sisi',sum(x['command']==r'\sisi' for x in all_en),
          'notes',collections.Counter(x['command'] for x in all_en if x['command']!=r'\sisi'))
    print('FR A/D differing IDs',[r['id'] for r in diff])

if __name__=='__main__':inventory()
