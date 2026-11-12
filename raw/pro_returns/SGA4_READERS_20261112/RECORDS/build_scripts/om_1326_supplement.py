"""Explicitly recorded scope extension to the repeated primed divisor formula."""
from pathlib import Path
import hashlib,json
from fr_core import find_exact
from marker_projection import carry_markers
ROOT=Path(__file__).resolve().parents[1]
DECISION='OM-DEC-1326-PRIMED-PRODUCT'
PRINTED=r"V(x'_{1},\ldots,x'_{r})"
CORRECTED=r"V(x'_{1}\cdots x'_{r})"
PROOF=("The local ring map O_{X,p} -> O_{X',p'} induced by g sends x_i to x'_i. "
       "For a prime q of the target, the inverse-image prime contains product_i x_i "
       "exactly when q contains product_i x'_i. Hence the inverse image of "
       "V(product_i x_i) is V(product_i x'_i). The ensuing localization "
       "B'[1/x'_1,...,1/x'_r] is isomorphic over B' to B'[1/(product_i x'_i)]: "
       "the first map sends 1/(product_i x'_i) to product_i (1/x'_i), and the "
       "inverse map sends 1/x'_i to (product_{j != i} x'_j)/(product_j x'_j). "
       "Both composites fix B' and the displayed generators, so they are identities.")

def main():
    p=ROOT/'work_fr/corrected_layers.json';data=json.loads(p.read_text())
    row={'id':'OM-SOL-1326','part':2,'file':'19','expose':'XIX','page':603,
         'place':'The repeated local equation for the primed divisor, immediately after the reported unprimed formula',
         'source':'api_pass_20261111/SOL_ONLY_MISPRINTS.json',
         'printed':PRINTED,'corrected':CORRECTED,'editorial_decision':DECISION,
         'scope_extension':True,'reason':PROOF,'on_disputed_page':False,
         'integration_stage':'after canonical and reviewed one-model changes; preserves the separate canonical Y-to-Y-prime change'}
    for layer,target in [('dip',PRINTED),('corr',CORRECTED)]:
        s=data[layer]['19'];hits=find_exact(s,PRINTED,603);state='printed'
        if not hits:hits=find_exact(s,CORRECTED,603);state='corrected'
        assert len(hits)==1,(layer,hits)
        a,b=hits[0];old=s[a:b];new=carry_markers(old,target)
        row[layer+'_hits']=1
        row[layer]={'old':old,'new':new,'at':a,'state':state,
                    'context_before':s[max(0,a-160):a],'context_after':s[b:b+160]}
    (ROOT/'output/shared/ONE_MODEL_FR_1326_SUPPLEMENT.json').write_text(json.dumps([row],ensure_ascii=False,indent=2)+'\n')
    decision={'id':DECISION,'source_id':'OM-SOL-1326','kind':'explicit editorial scope extension',
              'expose':'XIX','page':603,'original_scope':'unprimed local equation',
              'extended_scope':row['place'],'printed':PRINTED,'corrected':CORRECTED,'proof':PROOF,
              'source':'fr/E_corrected_after_scan_check/19/19.tex, XIX p.603',
              'baseline_sha256':hashlib.sha256(p.read_bytes()).hexdigest(),
              'unique_in_both_layers':True,'human_notes_changed':False}
    (ROOT/'output/records/OM_1326_SCOPE_DECISION.json').write_text(json.dumps(decision,ensure_ascii=False,indent=2)+'\n')
    print(DECISION+': part 2 uniquely located in both layers; no source/layer mutation.')

if __name__=='__main__':main()
