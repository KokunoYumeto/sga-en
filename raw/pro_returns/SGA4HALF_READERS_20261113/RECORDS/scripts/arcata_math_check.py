from pathlib import Path
import difflib,json
from tex_audit import math_fragments,canonical_math
ROOT=Path(__file__).resolve().parents[1]
W=ROOT/'work/arcata'
f=math_fragments((W/'fr/sga4.5-1.tex').read_text())
e=math_fragments((W/'en/sga4half_1_en.tex').read_text())
fa=[canonical_math(s) for _,s in f];ea=[canonical_math(s) for _,s in e]
out=[]
for op,a,b,c,d in difflib.SequenceMatcher(None,fa,ea,autojunk=False).get_opcodes():
    if op=='equal':continue
    out.append(dict(kind=op,fr=[s for _,s in f[a:b]],en=[s for _,s in e[c:d]],
                    fr_context=[s for _,s in f[max(0,a-1):a]],en_context=[s for _,s in e[max(0,c-1):c]]))
(W/'math_alignment_review.json').write_text(json.dumps(out,ensure_ascii=False,indent=2))
print('Math differences to inspect:',len(out))
for i,r in enumerate(out):
    print(i+1,r['kind'],'FR:',repr(r['fr'])[:500],'EN:',repr(r['en'])[:500])
