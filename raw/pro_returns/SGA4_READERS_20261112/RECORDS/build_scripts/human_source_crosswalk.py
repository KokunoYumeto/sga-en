"""Preserve original A arguments and map their D/English transmissions explicitly."""
from pathlib import Path
import bisect,collections,difflib,hashlib,json,re
from human_editorial_audit import calls,main_source
from en_common import fragment_blocks,sanitize
from fr_core import FILES,EXP,strip_comments
from build_fr import quote_tex
from build_en import literal_reading
ROOT=Path(__file__).resolve().parents[1]

def alignment_key(text):
    text=re.sub(r'\\SGApageno\{[^}]+\}\{[^}]+\}|\\SGApage\{[^}]+\}\{[^}]+\}\{[^}]+\}|\\pageoriginale\b','',text)
    return re.sub(r'\s+','',strip_comments(text))

def digest(text):return hashlib.sha256(text.encode()).hexdigest()

def main():
    inv=json.loads((ROOT/'work_fr/human_source_inventory.json').read_text())
    dossier=json.loads((ROOT/'work_fr/initial_layers.json').read_text())['org']
    pages=json.loads((ROOT/'sources/api_pass_20261111/PAGES.json').read_text())
    release=(ROOT/'sources/en/C_release_20261112/04_SGA4_EN_COMPLETE_READER.tex').read_text()
    fragments=fragment_blocks(release)
    original=[];notes=[];allraw={}
    for f in FILES:
        raw=(ROOT/f'sources/fr/A_orgogozo_snapshot_71766d9/{f}/{f}.tex').read_text();allraw[f]=raw
        pm=[m.start() for m in re.finditer(r'\\pageoriginale\b',raw)];pp=[p for p in pages if p['file']==f]
        assert len(pm)==len(pp),(f,len(pm),len(pp))
        source_rows=[r for r in inv['french_outer_pairs'] if r['file']==f]
        for r in source_rows:
            idx=max(0,bisect.bisect_right(pm,r['start'])-1)
            possible=[x for x in fragments if x['file']==f and x['a']<=r['line']<=x['b']]
            assert len(possible)==1,(f,r['line'],len(possible))
            original.append({'id':'A-'+r['id'],'file':f,'expose':EXP[f],'page':pp[idx]['folio'],
                             'source':r['source'],'source_line':r['line'],'printed':r['arguments'][0],
                             'corrected':r['arguments'][1],'raw_call':raw[r['start']:r['end']],
                             'argument_sha256':[digest(t) for t in r['arguments']],
                             'english_fragment':possible[0]['name'],'D_transmission_id':None,
                             'released_english_record_ids':[]})
        lo,hi=main_source(raw)
        nc=collections.Counter()
        for r in [r for r in calls(raw) if lo<=r['start']<hi and r['command'] in [r'\nde',r'\ndetext',r'\acorriger']]:
            kind='ACORRIGER' if r['command']==r'\acorriger' else 'NDE';nc[kind]+=1;n=nc[kind]
            enclosing=[s for s in source_rows if s['start']<r['start']<s['end']]
            parent='A-'+enclosing[0]['id'] if enclosing else None
            frag=next(z for z in fragments if z['file']==f and z['a']<=r['line']<=z['b'])
            notes.append({'id':f'A-{kind}-{f}-{n:03d}','file':f,'expose':EXP[f],
                          'page':pp[max(0,bisect.bisect_right(pm,r['start'])-1)]['folio'],
                          'source':f'fr/A_orgogozo_snapshot_71766d9/{f}/{f}.tex','source_line':r['line'],
                          'command':r['command'],'argument':r['arguments'][0],
                          'argument_sha256':digest(r['arguments'][0]),'enclosing_original_pair':parent,
                          'ancestors':r['ancestors'],'english_fragment':frag['name'],
                          'macro_expansion':r'\nde{#1}' if kind=='ACORRIGER' else None})
    # Exact-order alignment establishes correspondence; raw arguments determine
    # preservation. The alignment key is never used to assert byte equality.
    for f in FILES:
        aa=[r for r in original if r['file']==f];dd=[r for r in dossier if r['file']==f]
        ak=[(alignment_key(r['printed']),alignment_key(r['corrected'])) for r in aa]
        dk=[(alignment_key(r['printed']),alignment_key(r['corrected'])) for r in dd]
        for tag,a,b,c,d in difflib.SequenceMatcher(None,ak,dk,autojunk=False).get_opcodes():
            if tag=='delete':continue
            assert tag!='insert' and b-a==d-c,(f,tag,a,b,c,d)
            for ar,dr in zip(aa[a:b],dd[c:d]):
                ar['D_transmission_id']=dr['id']
                ar['D_arguments_exact']=[ar[k]==dr[k] for k in ['printed','corrected']]
                ar['D_argument_sha256']=[digest(dr[k]) for k in ['printed','corrected']]
                if not all(ar['D_arguments_exact']):
                    ar['D_transmitted_arguments']={k:dr[k] for k in ['printed','corrected']}
    # Only calls within translated source fragments are editorial body records.
    en=[];config=[]
    for r in inv['english_outer_pairs']:
        fs=[f for f in fragments if f['start']<=r['start']<f['end']]
        if not fs:config.append(r);continue
        assert len(fs)==1
        r=dict(r);r['id']=f'EN-ORG-{len(en)+1:04d}';r['fragment']=fs[0]['name'];r['file']=fs[0]['file'];en.append(r)
    assert len(en)==1171 and len(config)==20
    generated=json.loads((ROOT/'output/records/EN_HUMAN_RECORDS.json').read_text())
    for a,b in zip(en,generated):
        assert a['id']==b['id']
        assert tuple(map(alignment_key,a['arguments']))==(alignment_key(b['printed']),alignment_key(b['corrected'])),a['id']
        a['expose']=b['expose'];a['page']=b['page']
    for frag in fragments:
        aa=[r for r in original if r['english_fragment']==frag['name']]
        ee=[r for r in en if r['fragment']==frag['name']]
        ak=[(alignment_key(r['printed']),alignment_key(r['corrected'])) for r in aa]
        ek=[tuple(map(alignment_key,r['arguments'])) for r in ee]
        for tag,a,b,c,d in difflib.SequenceMatcher(None,ak,ek,autojunk=False).get_opcodes():
            if tag!='equal':continue
            for ar,er in zip(aa[a:b],ee[c:d]):
                ar['released_english_record_ids'].append(er['id'])
                ar['released_english_arguments_exact']=[ar[k]==v for k,v in zip(['printed','corrected'],er['arguments'])]
        ids=[r['id'] for r in ee]
        for r in aa:r['english_fragment_record_ids']=ids
    fr_extra=[r for r in original if not r['D_transmission_id'] or not all(r['D_arguments_exact'])]
    en_extra=[r for r in original if not r['released_english_record_ids'] or not all(r.get('released_english_arguments_exact',[]))]
    # The dedicated human rewrite is outside an active sisi command in A.
    raw=allraw['05bis'];a=raw.index('%Or pour toute flèche');b=raw.index('On peut supposer $p>n+1$',a);c=raw.index("Soit $[X'/X]^p$",b)
    rewrite={'id':'A-ORG-VBIS-REWRITE-138','expose':'Vbis','page':138,'source':'fr/A_orgogozo_snapshot_71766d9/05bis/05bis.tex',
             'source_line':raw.count('\n',0,a)+1,'printed_commented_source':raw[a:b].rstrip(),
             'editorial_rewrite_source':raw[b:c].rstrip(),
             'scope':'Original commented printed proof and the ensuing Changement Yves editorial replacement, through the sentence before Soit [X-prime/X]^p.',
             'english_fragment':'SGA4_VBIS_LINES_2586_2816_English.texfrag'}
    for lang,extra,quote,guard,title,intro in [
      ('FR',fr_extra,quote_tex,r'\ifnum\SGAForm=2\relax\else','Complément documentaire : dossier original de Fabrice Orgogozo',
       "Les arguments suivants sont reproduits depuis l’état original 71766d9. Ils complètent le dossier transmis par D : trois commandes ont été aplaties avant cette transmission, et d’autres arguments y ont été modifiés ou encodés différemment. Les identifiants A-ORG désignent l’original; ORG désigne la transmission D. Ce complément documentaire ne change aucune lecture du corps."),
      ('EN',en_extra,literal_reading,r'\ifSGAreading\else','Original French human editorial records: documentary supplement',
       "These exact original French arguments from snapshot 71766d9 supplement the released English rendering. The source-fragment crosswalk records every original pair. An original pair is reproduced here whenever its two raw arguments are not both present verbatim in a corresponding released English paired record. The French original and the released English rendering have separate source labels; this documentary supplement changes no body reading.")]:
        out=[guard,r'\chapter*{'+title+'}',r'\addcontentsline{toc}{chapter}{'+title+'}',intro+r'\par',
             ('Source complète et correspondances : ' if lang=='FR' else 'Complete source evidence and crosswalk: ')+r'\texttt{HUMAN\_ORIGINAL\_SOURCE\_RECORDS.json}.\par']
        for r in extra:
            out += [r'\par\medskip\noindent\textbf{'+r['id']+'}. '+('Exposé ')+r['expose']+', p. '+str(r['page'])+r'.\par',
                    r'\noindent '+('Source originale : ' if lang=='FR' else 'Original source: ')+quote(r['source'])+', '+('ligne ' if lang=='FR' else 'line ')+str(r['source_line'])+r'.\par']
            if lang=='FR':
                ref=r['D_transmission_id'] or 'aucune commande correspondante dans D'
                out.append(r'\noindent Transmission D : '+quote(ref)+r'.\par')
            else:
                out.append(r'\noindent Released English fragment: '+quote(r['english_fragment'])+r'.\par')
                out.append(r'\noindent Corresponding literal paired record: '+quote(', '.join(r['released_english_record_ids']) or 'no identical argument pair; original preserved here')+r'.\par')
            out += [r'\noindent '+('Premier argument original : ' if lang=='FR' else 'Original first argument: ')+quote(r['printed'])+r'\par',
                    r'\noindent '+('Second argument original : ' if lang=='FR' else 'Original second argument: ')+quote(r['corrected'])+r'\par']
        out += [r'\par\bigskip\noindent\textbf{'+rewrite['id']+r'}. Vbis, p.138.\par',
                ('Réécriture éditoriale humaine « Changement Yves », conservée depuis l’original.' if lang=='FR' else 'Human editorial rewrite labelled Changement Yves, retained from the original source.')+r'\par',
                r'\noindent '+('Ancien texte conservé en commentaires : ' if lang=='FR' else 'Printed text retained as source comments: ')+quote(rewrite['printed_commented_source'])+r'\par',
                r'\noindent '+('Réécriture éditoriale originale : ' if lang=='FR' else 'Original editorial rewrite: ')+quote(rewrite['editorial_rewrite_source'])+r'\par',r'\fi']
        (ROOT/f'output/shared/HUMAN_ORIGINAL_SUPPLEMENT_{lang}.tex').write_text(sanitize('\n'.join(out))+'\n')
    for lang,quote,guard,title in [
      ('FR',quote_tex,r'\ifnum\SGAForm=2\relax\else','Notes éditoriales originales : conservation documentaire'),
      ('EN',literal_reading,r'\ifSGAreading\else','Original human editorial notes: documentary preservation')]:
        intro=(r"Ce dossier conserve les 127 arguments N.D.E. directs et les deux arguments de la commande acorriger dans l’original 71766d9. Cette dernière commande est définie dans la source par acorriger[1] = nde\{\#1\}. Les notes propres aux lectures éditoriales et les notes transmises différemment restent ainsi disponibles dans les formes diplomatique et corrigée. Le corps garde ses notes et ses lectures propres."
               if lang=='FR' else
               "This dossier preserves all 127 direct N.D.E. arguments and the two arguments of acorriger in the original French snapshot 71766d9. The source defines acorriger with one argument by expanding exactly to nde with that same argument. Every original note remains available in the diplomatic and corrected forms, including notes attached only to an editorial reading and notes archived or rendered differently in the released English. The body keeps its own transmitted notes and readings.")
        nn=[guard,r'\chapter*{'+title+'}',r'\addcontentsline{toc}{chapter}{'+title+'}',intro+r'\par']
        for r in notes:
            nn += [r'\par\medskip\noindent\textbf{'+r['id']+'}. Exposé '+r['expose']+', p. '+str(r['page'])+r'.\par',
                   r'\noindent '+('Source originale : ' if lang=='FR' else 'Original source: ')+quote(r['source'])+', '+('ligne ' if lang=='FR' else 'line ')+str(r['source_line'])+r'.\par',
                   r'\noindent '+('Commande : ' if lang=='FR' else 'Command: ')+quote(r['command'])+r'.\par',
                   r'\noindent '+quote(r['argument'])+r'\par']
        nn.append(r'\fi')
        (ROOT/f'output/shared/HUMAN_ORIGINAL_NOTES_{lang}.tex').write_text(sanitize('\n'.join(nn))+'\n')
    payload={'original_active_sisi_records':1261,'D_transmitted_records':1258,'released_english_body_records':1171,
             'excluded_repeated_English_configuration_switches':20,
             'original_source_records':original,'original_NDE_records':notes,'dedicated_original_rewrite':rewrite,
             'supplement_FR_ids':[r['id'] for r in fr_extra],'supplement_EN_ids':[r['id'] for r in en_extra],
             'D_absent_original_ids':[r['id'] for r in original if not r['D_transmission_id']],
             'crosswalk_method':'Source-fragment line ranges give the English scope. Ordered exact-argument alignment links records; raw-byte equality is tested separately and every absent or changed original argument is explicitly reproduced in a supplement. No semantic equivalence is inferred from counts.',
             'source_byte_policy':'UTF-8 source arguments are retained without mathematical or lexical changes. Documentary TeX encodes literal metacharacters, glyphs, line breaks and line-break opportunities; the complete raw arguments and hashes remain in this record.'}
    (ROOT/'output/records/HUMAN_ORIGINAL_SOURCE_RECORDS.json').write_text(sanitize(json.dumps(payload,ensure_ascii=False,indent=2))+'\n')
    print('Original A',len(original),'FR supplement',len(fr_extra),'EN supplement',len(en_extra),'dedicated rewrite',1)
    print('D missing',payload['D_absent_original_ids'])
    print('A notes',len(notes),'inside pairs',sum(bool(r['enclosing_original_pair']) for r in notes))

if __name__=='__main__':main()
