"""Six source-verified first-coordinate repairs in V 1.10.

Integration baseline: after canonical and reviewed one-model changes, including
OM-SOL-0353. The common Pi decision concerns expose I and does not affect these
six spans. Original source trees and layer files are read only.
"""
from pathlib import Path
import hashlib,json,re
from fr_core import find_exact
from marker_projection import carry_markers

ROOT=Path(__file__).resolve().parents[1]
REASON=("V 1.10 defines Delta_n=[0,...,n], and (1.10.3) has degree-zero "
        "term direct-sum_i A_{U_i}. The first coordinate must therefore be 0. "
        "The maps defined by projections indexed by g(i) include i=0.")

def main():
    baseline=ROOT/'work_fr/corrected_layers.json'
    data=json.loads(baseline.read_text())
    # Old spans retain all already represented canonical changes in each layer.
    specs=[
      (15,r'U_{f(1)} \times_{X} \ldots \times_{X} U_{f(n)}{\quoi},',None),
      (16,r'\mbox{$U_{f(1)} \times_{X}\ldots \times_X U_{f(n)}$}',None),
      (16,r'U_{f(g(1))} \times_X \ldots \times_X U_{f(g(m))} \hookrightarrow S_m(\Uu)',None),
      (16,r's_f(g) : U_{f(1)} \times_X \ldots \times_X U_{f(n)}',None),
      (16,r'\to U_{f(g(1))} \times_{X} \ldots \times_X U_{f(g(m))}',
          r'\to U_{f(g(1)} \times_{X} \ldots \times_X U_{f(g(m))}'),
      (16,r'U_{f(1)} \times_X \ldots \times_X U_{f(n)}{\quoi}',
          r'U_{f(1)} \times_X \ldots \times_X U_{f()}{\quoi}'),
    ]
    rows=[]
    for part,(page,c_old,d_old) in enumerate(specs,1):
        printed=c_old
        corrected=c_old.replace('f(1)','f(0)').replace('g(1)','g(0)')
        row={'id':'OM-SOL-0352','part':part,'file':'05','expose':'V','page':page,
             'place':['S_n definition','restriction of s(g)','canonical inclusion into S_m',
                      'source of s_f(g)','target of s_f(g)','formula (1.10.2)'][part-1],
             'source':'api_pass_20261111/SOL_ONLY_MISPRINTS.json',
             'printed':printed,'corrected':corrected,'reason':REASON,
             'integration_stage':'after canonical and reviewed one-model changes, including OM-SOL-0353',
             'on_disputed_page':False}
        if part==5:
            row['related_ids']=['OM-SOL-0353']
            row['joint_printed']=d_old
            row['joint_corrected']=corrected
            row['reason']+=' The same span also retains the separately accepted closing parenthesis of OM-SOL-0353.'
        for layer,needle,target in [('dip',d_old or c_old,d_old or c_old),('corr',c_old,corrected)]:
            text=data[layer]['05'];hits=find_exact(text,needle,page)
            assert len(hits)==1,(part,layer,hits)
            a,b=hits[0];old=text[a:b];new=carry_markers(old,target)
            assert re.findall(r'\\SGApageno\{[^}]*\}\{[^}]*\}',old)==re.findall(r'\\SGApageno\{[^}]*\}\{[^}]*\}',new)
            row[layer+'_hits']=1
            row[layer]={'old':old,'new':new,'at':a,'state':'printed first coordinate after prior changes',
                        'context_before':text[max(0,a-140):a],'context_after':text[b:b+140]}
            data[layer]['05']=text[:a]+new+text[b:]
        rows.append(row)
    out=ROOT/'output/shared/ONE_MODEL_FR_0352_SUPPLEMENT.json'
    out.write_text(json.dumps(rows,ensure_ascii=False,indent=2)+'\n')
    checks={'id':'OM-SOL-0352','records':1,'parts':6,'unique_in_both_layers':6,
            'baseline_sha256':hashlib.sha256(baseline.read_bytes()).hexdigest(),
            'baseline_stage':rows[0]['integration_stage'],
            'disputed_pages':[],'source_trees_and_layers_modified':False,
            'joint_source_part':{'part':5,'ids':['OM-SOL-0352','OM-SOL-0353']},
            'evidence':'fr/E_corrected_after_scan_check/05/05.tex, V 1.10, pp.15–16; formula (1.10.3) gives the degree-zero term.'}
    (ROOT/'output/shared/ONE_MODEL_FR_0352_CHECKS.json').write_text(json.dumps(checks,ensure_ascii=False,indent=2)+'\n')
    print('OM-SOL-0352: six parts, each uniquely located in both layers; no layer files modified.')

if __name__=='__main__':main()
