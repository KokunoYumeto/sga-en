#!/usr/bin/env python3
"""Isolated disjoint XIII rendering probe; never changes the aggregate candidates."""
from pathlib import Path
import sys,json,hashlib,re,subprocess
HERE=Path(__file__).resolve().parent
EN=HERE.parents[1]
ROOT=EN.parents[1]
sys.path.insert(0,str(EN))
from build_english_candidates import esc
from apparatus_macro_state import prepare_macro_states
from compile_candidates import diagnostics
from source_emphasis import underline_words
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    spans=[json.loads(x) for x in (HERE/'translation_spans.jsonl').read_text().splitlines()]
    variants=[json.loads(x) for x in (HERE/'variants.jsonl').read_text().splitlines()]
    configs=json.loads((HERE/'batches.json').read_text())
    last=max(x['last_folio'] for x in spans)
    out=HERE/f'probe{last}';out.mkdir(exist_ok=True)
    base=EN/'DRAFT_SGA6_EN_annotated_master.tex'
    source=base.read_text()
    for span in spans:
        assert source.count(span['old'])==1,span['id']
        source=source.replace(span['old'],span['new'],1)
    boundary=json.loads((ROOT/'build/review_snapshots/english_xii_complete595_615/XII_boundary_macros.json').read_text())
    macro_block=boundary['reviewed_615_616_block']
    assert hashlib.sha256(macro_block.encode()).hexdigest()==boundary['reviewed_block_sha256']
    target=r'\sgaStableTarget{sga6.e13.expose}'
    assert source.count(target)==1
    source=source.replace(target,macro_block+'\n\n'+target,1)
    (out/'preceding_macro_packet.json').write_text(json.dumps(boundary,ensure_ascii=False,indent=2)+'\n')
    definitions,state=prepare_macro_states(source,variants)
    checks=[]
    for n,v in enumerate(variants,1):
        a=source.index(v['scope_start']);b=source.index(v['scope_end'],a) if v['scope_end'] else source.index(configs[-1]['native_end'],a)
        part=source[a:b];count=part.count(v['old']);assert count==1,(v['id'],count)
        if v['mode']=='display':
            replacement=('% XIII probe display variant '+v['id']+'\n'
              +r'\SGACaptureAppState{'+v['id']+'}%\n'
              +r'\ifnum\SGAReaderForm=1\relax\SGAAppMark{'+v['id']+r'}\fi'+'\n'
              +r'\ifnum\SGAReaderForm=0\relax'+'\n'+v['printed']+'\n'
              +r'\else'+'\n'+v['corrected']+'\n'+r'\fi')
        else:replacement=r'\var{'+v['printed']+'}{'+v['corrected']+'}{'+v['id']+'}'
        source=source[:a]+part.replace(v['old'],replacement,1)+source[b:]
        definitions+='\\expandafter\\def\\csname SGAAppNumber@'+v['id']+'\\endcsname{XIII '+str(n)+'}\n'
        checks.append(dict(id=v['id'],unique_anchor=True,mode=v['mode']))
    a=source.index(spans[0]['new'].splitlines()[0])
    b=source.index(configs[-1]['native_end'],a)
    rendered,font_stats=underline_words(source[a:b])
    source=source[:a]+rendered+source[b:]
    layout=[]
    repairfile=HERE/'rendering_repairs.jsonl'
    if repairfile.exists():
        for line in repairfile.read_text().splitlines():
            r=json.loads(line)
            if r['page']>last:continue
            a=source.index(r['scope_start']);b=source.index(r['scope_end'],a)
            part=source[a:b]
            assert part.count(r['old'])==1,(r['id'],part.count(r['old']))
            source=source[:a]+part.replace(r['old'],r['new'],1)+source[b:]
            layout.append(r)
    (out/'rendering_repair_applications.json').write_text(json.dumps(layout,ensure_ascii=False,indent=2)+'\n')
    source=source.replace(r'\begin{document}',definitions+'\n'+r'\begin{document}',1)
    source=source.replace(r'\sgaStableTarget{sga6.e13.expose}',r'\par\noindent\textbf{Disjoint English XIII rendering probe, printed616--'+str(last)+r'. This probe does not extend the assembled prefix beyond296.}\par'+'\n'+r'\sgaStableTarget{sga6.e13.expose}',1)
    app=['\\ifnum\\SGAReaderForm=1\n\\clearpage\n\\section*{XIII contribution apparatus: rendering probe}\n']
    for n,v in enumerate(variants,1):
        app+=['\\noindent\\begin{minipage}{\\linewidth}\\raggedright\n','\\SGARestoreAppState{'+v['id']+'}%\n','\\paragraph{[XIII '+str(n)+'] '+esc(v['id'])+'}\n']
        for label,key in [('Printed reading','printed'),('Corrected reading','corrected')]:
            value=v[key]
            if v['mode']=='math':value='\\('+value+'\\)'
            app.append(label+': '+value+'\\par\n')
        app.append('{\\raggedright Source: '+esc(v['source'])+'. '+esc(v['reason'])+'\\par}\n')
        app.append('\\end{minipage}\\par\\medskip\n')
    app.append('\\fi\n')
    source=source.replace(r'\end{document}',''.join(app)+r'\end{document}',1)
    status=dict(scope=f'disjoint English XIII616–{last} probe over unchanged aggregate prefix1–296',source_claim='No aggregate extension, full-volume translation claim or new source-image reading.',base_annotated_master_sha256=sha(base),spans_sha256=sha(HERE/'translation_spans.jsonl'),variants_sha256=sha(HERE/'variants.jsonl'),sequential_anchor_checks=checks,forms={})
    (out/'macro_states.json').write_text(json.dumps(state,ensure_ascii=False,indent=2)+'\n')
    (out/'word_group_rendering.json').write_text(json.dumps(dict(scope=f'XIII616–{last}',method='Shared word-group underline helper applied to the reference emphasis groups; direct uline groups retained; literal raw mathematical units unchanged.',counts=font_stats,limitation='ASTRA-XIII-0007 statement/defined-term convention remains under the separately assigned global source audit. This rendering pass is not a claim that every statement-word rule has completed that gate.'),ensure_ascii=False,indent=2)+'\n')
    statuspath=out/'BUILD_STATUS.json'
    for form,mode in [('corrected_apparatus',1),('diplomatic',0)]:
        stem='PROBE_EN_XIII_'+form;tex=out/(stem+'.tex');pdf=out/(stem+'.pdf')
        tex.write_text(source.replace(r'\providecommand{\SGAReaderForm}{1}',r'\providecommand{\SGAReaderForm}{'+str(mode)+'}',1));pdf.unlink(missing_ok=True)
        texhash=sha(tex);runs=[]
        for n in [1,2]:
            p=subprocess.run([sys.executable,str(ROOT/'scripts/tex_environment.py'),'pdflatex','-interaction=nonstopmode','-halt-on-error','-output-directory='+str(out.relative_to(ROOT)),str(tex.relative_to(ROOT))],cwd=ROOT,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
            ds=diagnostics(p.stdout);summary=next((x for x in p.stdout.splitlines() if x.startswith('Output written on ')),'')
            run=dict(run=n,exit_code=p.returncode,diagnostics=ds,output=summary);runs.append(run)
            (out/(stem+'.log')).write_text('Diagnostic-only report; TeX filesystem loading paths omitted.\n'+json.dumps(run,ensure_ascii=False,indent=2)+'\n')
            print(form,json.dumps(run,ensure_ascii=False),flush=True)
            if p.returncode:break
        record=dict(runs=runs,source_sha256=texhash,source_unchanged=sha(tex)==texhash,pdf_present=pdf.exists())
        if pdf.exists() and not runs[-1]['exit_code']:record['pdf_sha256']=sha(pdf)
        status['forms'][form]=record;statuspath.write_text(json.dumps(status,ensure_ascii=False,indent=2)+'\n')
        if runs[-1]['exit_code']:break
if __name__=='__main__':main()
