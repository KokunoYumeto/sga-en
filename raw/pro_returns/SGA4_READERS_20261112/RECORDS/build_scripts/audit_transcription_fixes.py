"""Account for every agreed scan-transcription fix in source and final layers.

AF identifiers are the one-based line numbers of fixes/FIXLOG_4.jsonl.
The source record itself is checked before editorial alternatives are selected.
The final-layer checks use only literal characters, TeX whitespace/comment
offset maps, and the explicitly recorded adaptations below.
"""
import collections,csv,json,re
from pathlib import Path
from fr_core import ROOT,SRC,FILES,EXP,body,explicit_pages,find_exact,group,replace_sisi
from build_fr import restore_commented

ADAPTATIONS={
 ('AF0030','corr'):(r'(i_\alpha)_{\alpha\in J}','MP0083','The accepted misprint corrects the index set after the scan transcription has been restored.'),
 ('AF0043','dip'):(r'$\pi_\circ=\aleph_\circ$','FR-ED93-PI','The exact capital-Pi token maps to the recorded printed cardinal glyph.'),
 ('AF0043','corr'):(r'$\pi_\circ=\aleph_\circ$','FR-ED93-PI','The exact capital-Pi token maps to the recorded printed cardinal glyph.'),
 ('AF0045','dip'):(r'\Filt^{\pi^{\pi_1}}(F)','FR-ED93-PI','The exact capital-Pi tokens map to the recorded printed cardinal glyph.'),
 ('AF0045','corr'):(r'\Filt^{\pi^{\pi_1}}(F)','FR-ED93-PI','The exact capital-Pi tokens map to the recorded printed cardinal glyph.'),
 ('AF0046','dip'):(r'\pi^{\pi_1}','FR-ED93-PI','The exact capital-Pi tokens map to the recorded printed cardinal glyph.'),
 ('AF0046','corr'):(r'\pi^{\pi_1}','FR-ED93-PI','The exact capital-Pi tokens map to the recorded printed cardinal glyph.'),
 ('AF0049','dip'):(r"$A$ est grand devant $\pi'_{\circ}$).",'FR-ED93-PI','The exact capital-Pi token maps to the recorded printed cardinal glyph.'),
 ('AF0049','corr'):(r"$A$ est grand devant $\pi'_{\circ}$).",'FR-ED93-PI','The exact capital-Pi token maps to the recorded printed cardinal glyph.'),
 ('AF0203','corr'):(r'$\Top(X)_{/p^*(U)}','H17','The source uses the literal asterisk token for the same superscript; the slice denominator is present.'),
 ('AF0262','corr'):(r"$u_\ast : E \to E'$",'MP0329','The accepted misprint changes the sign before E from equals to colon.'),
 ('AF0290','corr'):(r'dont tous les objets sont','OM-SOL-0390','The agreed transcription inserts les; the accepted grammatical repair then changes tout to tous in the same clause.'),
 ('AF0328','corr'):(r'dans $\Ss/U$','MP0355; DEC-C293','The site-symbol repair remains; the independently agreed denominator correction gives U.'),
 ('AF0703','corr'):('premier résultats','H83','The by-hand replay is on a disputed page and remains deferred; the corrected source title is retained.'),
 ('AF0711','dip'):(r"H^{i}(\bar{X}'_{\bar{s}'},,\bar{F}')",'OM-OPUS-0173','The corrected geometric-point subscript remains; the accepted printed double-comma misprint is restored in the diplomatic form.'),
 ('AF0714','corr'):(r"${T'}^{i}(F)=H^{i}(Y,h^{\ast}(F))$",'MP0625','The accepted misprint changes g to h while preserving the transcribed cohomological expression.'),
 ('AF0715','corr'):(r"comme l'image $\eta$ de $\xi$ dans",'OM-SOL-0760','The accepted one-model language repair removes the extra de before eta.'),
 ('AF0754','corr'):(r'(R^{q}h_{\cl\ast})\varepsilon^{\ast}','H88; MP0710','The page-held replay is not newly applied. The existing corrected expression and its h correction remain, with the source epsilon macro.'),
 ('AF0823','corr'):(r'(K^{\bigdot})))  \ar[r] &','H90','The arrow replay remains deferred on the disputed page; the existing corrected-source arrow remains.'),
 ('AF0832','corr'):(r'ℋ^{1}(f^{\ast}L\otimes I))$','H93','The parenthesis replay remains deferred on the disputed page; the existing corrected source is retained.'),
 ('AF0865','corr'):(r'\Hom(k^{\ast}_XK, Rf^{!}_Vk^{\ast}L)','H101','The stray comma is absent; the existing independent correction removing the subscript X from the second pullback remains.'),
 ('AF0881','corr'):(r'(R^{2}i^{!})','H112','The functor i shriek is in the required position; the existing cohomological degree 2 is retained.'),
 ('AF0884','corr'):(r'(R^{2a}u^{!})(𝛍_{n}{}^{\otimes a})','H113','The by-hand replay remains deferred on a disputed page; the existing corrected grouping is retained.'),
 ('AF0886','corr'):(r'(\varphi(Y,X) \otimes 𝛍_{n}^{\otimes b})','H115; MP0918','The by-hand replay remains deferred. The existing tensor notation and the independently agreed missing-varphi repair remain.'),
}

def search(text,needle,page):
    return find_exact(text,needle,page) or find_exact(text,needle)

def main():
    records=[json.loads(x) for x in (SRC/'fixes/FIXLOG_4.jsonl').read_text().splitlines() if x.strip()]
    final=json.loads((ROOT/'work_fr/corrected_layers.json').read_text())
    raw={f:restore_commented(body(explicit_pages((SRC/'fr/D_diplomatic_after_scan_check'/f/(f+'.tex')).read_text(),f)),f,True) for f in FILES}
    ranges={}
    for f,text in raw.items():
        spans=[];end=0
        for m in re.finditer(r'\\sisi\s*\{',text):
            if m.start()<end:continue
            try:
                _,j=group(text,text.find('{',m.start()));_,end=group(text,j)
            except ValueError:continue
            spans.append((m.start(),end))
        ranges[f]=spans
    out=[];fail=[]
    for i,r in enumerate(records,1):
        ident=f'AF{i:04d}';f=r['file'].split('/')[0];p=r['page'];text=raw[f]
        row=dict(id=ident,tome=r['tome'],expose=EXP[f],page=p,source='fixes/FIXLOG_4.jsonl#'+ident,
                 before=r['old'],after=r['new'],raw_D_matches=0)
        if not r['new']:
            absent=not search(text,r['old'],p)
            row['source_status']='recorded deletion verified' if absent else 'unresolved deletion'
            for side in ['dip','corr']:
                absent=not search(final[side][f],r['old'],p)
                row[side+'_status']='recorded deleted span remains absent' if absent else 'unresolved deletion'
                row[side+'_matches']=0;row[side+'_reading']='';row[side+'_authority']=ident
                if not absent:fail.append((ident,side))
        else:
            matches=search(text,r['new'],p);row['raw_D_matches']=len(matches)
            row['source_status']='recorded new reading verified' if matches else 'unresolved source'
            if not matches:fail.append((ident,'source'));out.append(row);continue
            a,b=matches[0]
            for l,u in ranges[f]:
                if a<u and l<b:a=min(a,l);b=max(b,u)
            context=text[a:b];row['source_context']=context
            for side,branch in [('dip',0),('corr',1)]:
                expected=replace_sisi(context,branch)
                hits=search(final[side][f],expected,p) if expected.strip() else []
                row[side+'_reading']=expected;row[side+'_authority']=ident
                row[side+'_status']='recorded reading present' if hits else 'unresolved final reading'
                if not hits and (ident,side) in ADAPTATIONS:
                    expected,authority,reason=ADAPTATIONS[(ident,side)]
                    hits=search(final[side][f],expected,p)
                    row[side+'_reading']=expected;row[side+'_authority']=authority;row[side+'_reason']=reason
                    row[side+'_status']='reviewed source adaptation present' if hits else 'unresolved adaptation'
                row[side+'_matches']=len(hits)
                if not hits:fail.append((ident,side))
        out.append(row)
    target=ROOT/'output/records/AGREED_TRANSCRIPTION_FIXES_AUDIT.json'
    target.write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
    fields=['id','tome','expose','page','before','after','source','source_status','raw_D_matches',
            'dip_status','dip_matches','dip_reading','dip_authority','dip_reason',
            'corr_status','corr_matches','corr_reading','corr_authority','corr_reason']
    with target.with_suffix('.tsv').open('w',newline='') as stream:
        writer=csv.DictWriter(stream,fieldnames=fields,delimiter='\t',extrasaction='ignore');writer.writeheader();writer.writerows(out)
    print('records',len(out),'source',dict(collections.Counter(r['source_status'] for r in out)))
    print('final diplomatic',dict(collections.Counter(r.get('dip_status') for r in out)))
    print('final corrected',dict(collections.Counter(r.get('corr_status') for r in out)))
    print('unresolved',fail)
    return not fail

if __name__=='__main__':
    raise SystemExit(0 if main() else 1)
