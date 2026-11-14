#!/usr/bin/env python3
"""Isolated disjoint VII rendering probe; never changes the aggregate candidates."""
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
    definitions,state=prepare_macro_states(source,variants)
    checks=[]
    for n,v in enumerate(variants,1):
        a=source.index(v['scope_start']);b=source.index(v['scope_end'],a) if v['scope_end'] else source.index(configs[-1]['native_end'],a)
        part=source[a:b];count=part.count(v['old']);assert count==1,(v['id'],count)
        if v['mode']=='display':
            replacement=('% VII probe display variant '+v['id']+'\n'
              +r'\SGACaptureAppState{'+v['id']+'}%\n'
              +r'\ifnum\SGAReaderForm=1\relax\SGAAppMark{'+v['id']+r'}\fi'+'\n'
              +r'\ifnum\SGAReaderForm=0\relax'+'\n'+v['printed']+'\n'
              +r'\else'+'\n'+v['corrected']+'\n'+r'\fi')
        else:replacement=r'\var{'+v['printed']+'}{'+v['corrected']+'}{'+v['id']+'}'
        source=source[:a]+part.replace(v['old'],replacement,1)+source[b:]
        definitions+='\\expandafter\\def\\csname SGAAppNumber@'+v['id']+'\\endcsname{VII '+str(n)+'}\n'
        checks.append(dict(id=v['id'],unique_anchor=True,mode=v['mode']))
    a=source.index(spans[0]['new'].splitlines()[0])
    b=source.index(configs[-1]['native_end'],a)
    rendered,font_stats=underline_words(source[a:b])
    source=source[:a]+rendered+source[b:]
    source=source.replace(r'\begin{document}',definitions+'\n'+r'\begin{document}',1)
    source=source.replace(r'\sgaStableTarget{sga6.e07.expose}',r'\par\noindent\textbf{Disjoint English VII rendering probe, printed416--'+str(last)+r'. This probe does not extend the assembled prefix beyond296.}\par'+'\n'+r'\sgaStableTarget{sga6.e07.expose}',1)
    app=['\\ifnum\\SGAReaderForm=1\n\\clearpage\n\\section*{VII contribution apparatus: rendering probe}\n']
    for n,v in enumerate(variants,1):
        app+=['\\noindent\\begin{minipage}{\\linewidth}\\raggedright\n','\\SGARestoreAppState{'+v['id']+'}%\n','\\paragraph{[VII '+str(n)+'] '+esc(v['id'])+'}\n']
        for label,key in [('Printed reading','printed'),('Corrected reading','corrected')]:
            value=v[key]
            if v['mode']=='math':value='\\('+value+'\\)'
            app.append(label+': '+value+'\\par\n')
        app.append('{\\raggedright Source: '+esc(v['source'])+'. '+esc(v['reason'])+'\\par}\n')
        app.append('\\end{minipage}\\par\\medskip\n')
    app.append('\\fi\n')
    source=source.replace(r'\end{document}',''.join(app)+r'\end{document}',1)
    status=dict(scope=f'disjoint English VII416–{last} probe over unchanged aggregate prefix1–296',source_claim='No aggregate extension, full-volume translation claim or new source-image reading.',base_annotated_master_sha256=sha(base),spans_sha256=sha(HERE/'translation_spans.jsonl'),variants_sha256=sha(HERE/'variants.jsonl'),sequential_anchor_checks=checks,forms={})
    (out/'macro_states.json').write_text(json.dumps(state,ensure_ascii=False,indent=2)+'\n')
    (out/'word_group_rendering.json').write_text(json.dumps(dict(scope=f'VII416–{last}',method='Shared observed-word underline helper; direct uline groups retained; literal raw mathematical units unchanged.',counts=font_stats),ensure_ascii=False,indent=2)+'\n')
    statuspath=out/'BUILD_STATUS.json'
    for form,mode in [('corrected_apparatus',1),('diplomatic',0)]:
        stem='PROBE_EN_VII_'+form;tex=out/(stem+'.tex');pdf=out/(stem+'.pdf')
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
