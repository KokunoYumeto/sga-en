#!/usr/bin/env python3
"""Write two reviewed English lexical corrections; do not edit the edition."""
from pathlib import Path
import hashlib, json, re
from lexical_inventory import pages

HERE=Path(__file__).resolve().parent
BASE=HERE/'input_snapshots'

def main():
    fr=pages((BASE/'build/FR_current_revised.tex').read_text())
    en=pages((BASE/'review/english/aggregate/SGA6_EN_raw_current.tex').read_text())
    rows=[]
    for page,old in [
        (648,r'\item every generalization of \(s\) remains in \(S_0\).'),
        (649,r'is ample for every generalization \(t\) of \(s\) (EGA III 4.7.1).'),
    ]:
        f,e=fr[str(page)]['text'],en[str(page)]['text']
        assert e.count(old)==1
        a=f.index(r"g\'en\'erisation")
        rows.append(dict(id=f'EN-TERM-GENERIZATION-{page}',record_type='English_translation_terminology_patch',page=page,layer='both',
            scope_start=f'%%%%%%%%%%  scan idx {page+13}  |  folio {page}  %%%%%%%%%%',
            scope_end=f'%%%%%%%%%%  scan idx {page+14}  |  folio {page+1}  %%%%%%%%%%',
            old=old,new=old.replace('generalization','generization'),expected_count=1,
            French_reading=r"g\'en\'erisation",French_context=f[max(0,a-100):a+150],
            reason='The passage quantifies over points t whose closure contains s, the source term générisation. The supplied SGA 4, 4½ and 7 glossaries render this term generization. In an affine neighbourhood Spec(A), t corresponds to a prime p_t contained in p_s, and the exact localization homomorphism A_{p_s} -> A_{p_t} induces Spec(A_{p_t}) -> Spec(A_{p_s}); its closed point maps to the generization t of s. The replacement names this same point relation, preserving the following specialization assertions, the ampleness condition, and every formula. Ordinary généralisation elsewhere retains generalization.',
            source_refs=['en/glossaries/GLOSSARY_SGA4_FR_EN.tsv#596','en/glossaries/GLOSSARY_SGA4HALF_FR_EN.tsv#440','en/glossaries/GLOSSARY_SGA7_FR_EN.tsv#435',f'build/FR_current_revised.tex#folio{page}'],
            input_English_page_sha256=hashlib.sha256(e.encode()).hexdigest(),input_French_page_sha256=hashlib.sha256(f.encode()).hexdigest(),
            mathematical_units_unchanged=True,source_forms='Apply to both English source forms as a translation correction; no French misprint variant.',shared_files_changed=False))
    (HERE/'EN_TERMINOLOGY_PATCHES.jsonl').write_text(''.join(json.dumps(r,ensure_ascii=False)+'\n' for r in rows))
    print('Saved two exact source-scoped patches.')

if __name__=='__main__':main()
