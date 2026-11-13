#!/usr/bin/env python3
"""Compare literal mathematical units and make a scoped terminology inventory.

This verifies only the contiguous newly compared English chunk files present. Literal math-unit
multisets allow changes in prose word order, but no formula characters are
removed or canonicalized. Text inside a displayed formula remains present.
"""
from pathlib import Path
from collections import Counter
import csv
import json
import re
from reviewed_french import load_reviewed_pages

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
MARKER=re.compile(r'%%%%%%%%%%\s+scan idx\s+\d+\s*\|\s*folio\s+(\d+)\s+%%%%%%%%%%')
MATH=re.compile(r'\\begin\{(?:equation|align)\}.*?\\end\{(?:equation|align)\}|(?<!\\)\\\[.*?(?<!\\)\\\]|(?<!\\)\\\(.*?(?<!\\)\\\)|(?<!\\)\$(?:[^$]|\\\$)*?(?<!\\)\$',re.S)


def split(text):
    ms=list(MARKER.finditer(text))
    return {int(m.group(1)):text[m.end():ms[i+1].start() if i+1<len(ms) else len(text)] for i,m in enumerate(ms)}


def tsv(name,fields,rows):
    with (HERE/name).open('w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=fields,delimiter='\t',lineterminator='\n');w.writeheader();w.writerows(rows)


def main():
    chunks=[]
    for path in HERE.glob('EN_*_P*.tex'):
        match=re.fullmatch(r'EN_.*_P(\d{3})_(\d{3})\.tex',path.name)
        if match:chunks.append((int(match.group(1)),int(match.group(2)),path))
    chunks.sort()
    last=0
    for start,stop,path in chunks:
        assert start==last+1,(path.name,'noncontiguous or overlapping review scope')
        last=stop
    end=last
    fr,reference=load_reviewed_pages(end)
    en=split(''.join(path.read_text() for _,_,path in chunks))
    (HERE/'EN_FRENCH_REVIEW_REFERENCE.json').write_text(json.dumps(reference,ensure_ascii=False,indent=2)+'\n')
    approved_pairs=json.loads((HERE/'EN_APPROVED_LEXICAL_MATH_PAIRS.json').read_text())
    rows=[]; diffs=[]
    for page in range(1,end+1):
        a=Counter(m.group(0) for m in MATH.finditer(fr[page]));b=Counter(m.group(0) for m in MATH.finditer(en[page]))
        missing=list((a-b).elements());extra=list((b-a).elements())
        rows.append({'page':page,'French_math_units':sum(a.values()),'English_math_units':sum(b.values()),
                     'French_units_without_literal_match':len(missing),'English_units_without_literal_match':len(extra),
                     'method':'literal TeX mathematical-unit multiset; whitespace and commands retained'})
        approved_status={}
        ma=Counter(missing);eb=Counter(extra)
        for pair in approved_pairs:
            if pair['page'] != page or pair.get('layer','both') not in ('current','both'):
                continue
            fu=pair['French_literal_unit'];eu=pair['English_literal_unit'];n=pair['expected_multiplicity']
            if ma[fu]==n and eb[eu]==n:
                approved_status[('French',fu)]=pair['status']
                approved_status[('English',eu)]=pair['status']
        for item in missing:
            diffs.append({'page':page,'side':'French','literal_unit':item,'status':approved_status.get(('French',item),'unreviewed literal difference')})
        for item in extra:
            diffs.append({'page':page,'side':'English','literal_unit':item,'status':approved_status.get(('English',item),'unreviewed literal difference')})
    tsv(f'EN_REVIEWED_MATH_COUNTS_001_{end:03d}.tsv',list(rows[0]),rows)
    tsv(f'EN_REVIEWED_MATH_LITERAL_DIFFERENCES_001_{end:03d}.tsv',['page','side','literal_unit','status'],diffs)
    terms=[('faisceau cohérent','coherent sheaf'),('faisceaux cohérents','coherent sheaves'),
           ('Module localement libre','locally free Module'),('Modules localement libres','locally free Modules'),
           ('complexe parfait','perfect complex'),('complexes parfaits','perfect complexes'),
           ('catégorie dérivée','derived category'),('catégories dérivées','derived categories'),
           ('anneau de Chow','Chow ring'),('anneaux de Chow','Chow rings'),
           ('filtration topologique','topological filtration'),('fibré tangent relatif virtuel','virtual relative tangent bundle'),
           ('groupe de Picard','Picard group'),('foncteur de Picard','Picard functor'),
           ('classes de Chern','Chern classes'),('caractères de Chern','Chern characters'),
           ('immersion régulière','regular immersion'),('intersection complète','complete intersection'),
           ('morphisme propre','proper morphism'),('schémas noethériens','noetherian schemes'),
           ('faisceaux de cohomologie','cohomology sheaves'),('complexe cotangent relatif','relative cotangent complex'),
           ('dimension relative virtuelle','virtual relative dimension'),('foncteur déterminant','determinant functor'),
           ('représentations rationnelles irréductibles','irreducible rational representations'),
           ('groupe de Weyl','Weyl group'),('tore maximal','maximal torus'),
           ('caractères rationnels','rational characters'),('représentations fondamentales','fundamental representations'),
           ('groupe dérivé','derived group'),('anneau gradué','graded ring'),
           ('fonctions symétriques élémentaires','elementary symmetric functions'),
           ('polynômes universels','universal polynomials'),('automorphisme principal','principal automorphism'),
           ('homomorphisme de Chern','Chern homomorphism'),('série formelle','formal series'),
           ('partie alternée','alternating part'),('corps des quotients','field of fractions'),
           ('endomorphisme additif','additive endomorphism'),('composantes homogènes','homogeneous components'),
           ('équivalence rationnelle','rational equivalence'),('foncteur covariant','covariant functor'),
           ('foncteur contravariant','contravariant functor'),('non singulier','nonsingular'),
           ('application régulière','regular map'),('corps de base','base field'),
           ('catégorie abélienne','abelian category'),('résolution injective','injective resolution'),
           ('foncteurs dérivés','derived functors'),('foncteur cohomologique','cohomological functor'),
           ('dimension cohomologique','cohomological dimension'),('problème universel','universal problem'),
           ('quasi-cohérent','quasi-coherent'),('faisceaux quasi-cohérents','quasi-coherent sheaves'),
           ('théorème des syzygies','syzygy theorem'),('transport de structure','transport of structure'),
           ('application biadditive','biadditive map'),('sous-groupe de torsion','torsion subgroup'),
           ('espace fibré localement trivial','locally trivial fibre space'),('foncteurs composés','composite functors'),
           ('image directe','direct image'),('hypersurface','hypersurface'),
           ('linéairement équivalent','linearly equivalent'),('morphismes propres','proper morphisms'),
           ('sous-faisceau cohérent','coherent subsheaf'),('équivalence numérique','numerical equivalence'),
           ('variété de drapeaux','flag variety'),('fibré conormal','conormal bundle'),
           ('homomorphisme canonique','canonical homomorphism'),('faisceau des germes','sheaf of germs'),
           ('fibré normal','normal bundle'),('genre arithmétique','arithmetic genus'),
           ('hyperplan','hyperplane'),('sous-variété linéaire','linear subvariety'),
           ('formule sans dénominateur','formula without denominators'),('série formelle','formal series'),
           ('cycles de Schubert','Schubert cycles'),('puissance extérieure','exterior power'),
           ('fibré projectif','projective bundle'),('cohomologie des espaces projectifs','cohomology of projective spaces'),
           ('codimension des supports','codimension of supports'),('opération d\'image réciproque','inverse-image operation'),
           ('pseudo-cohérent','pseudo-coherent'),('pseudo-cohérence','pseudo-coherence'),('perfection','perfection'),
           ('présentation finie','finite presentation'),('type fini','finite type'),
           ('catégorie fibrée','fibered category'),('catégories fibrées','fibered categories'),
           ('sous-catégorie fibrée','fibered subcategory'),('catégorie scindée','split category'),
           ('catégorie triangulée','triangulated category'),('sous-catégorie triangulée','triangulated subcategory'),
           ('sous-catégorie strictement pleine','strictly full subcategory'),
           ('clivage','cleavage'),('foncteur cartésien','cartesian functor'),('foncteur exact','exact functor'),
           ('foncteur image réciproque','inverse-image functor'),('triangle distingué','distinguished triangle'),
           ('quasi-isomorphisme','quasi-isomorphism'),('épimorphisme','epimorphism'),('monomorphisme','monomorphism'),
           ('noyau','kernel'),('conoyau','cokernel'),('cône','cone'),('raffinement','refinement'),
           ('localement relevable','locally liftable'),('localement quasi-relevable','locally quasi-liftable'),
           ('site chaotique','chaotic site'),('site ponctuel','punctual site'),
           ('pleinement fidèle','fully faithful'),('image essentielle','essential image'),
           ('dimension tor finie','finite tor-dimension'),('borné supérieurement','bounded above'),
           ('complexes acycliques','acyclic complexes'),('sorites','sorites')]
    terms=list(dict.fromkeys(terms))
    termrows=[]
    for ft,et in terms:
        found=[]
        for page,text in en.items():
            matches=list(re.finditer(r'(?<![A-Za-z])'+re.escape(et)+r'(?![A-Za-z])',text))
            found.extend([page]*len(matches))
        termrows.append({'french_term_or_notation':ft,'english_rendering':et,'count':len(found),
                         'first_place':(('Exposé 0' if found[0]<78 else 'Exposé I')+', printed p.'+str(found[0])) if found else '',
                         'scope':f'newly compared English pp.1–{end} only; complete literal phrase with alphabetic boundaries; exact case',
                         'status':('literal phrase present; rendering paired during passage review; not a volume-wide glossary' if found else 'reference rendering retained; no complete literal occurrence in this raw TeX scope')})
    tsv(f'GLOSSARY_SGA6_REVIEWED_001_{end:03d}.tsv',list(termrows[0]),termrows)
    summary={'reviewed_pages':end,'mathematical_units':sum(r['English_math_units'] for r in rows),
             'literal_difference_units':len(diffs),
             'unexpected_difference_units':sum(d['status']=='unreviewed literal difference' for d in diffs),
             'French_patch_rows_applied':len(reference['applied_patches']),
             'French_reference_record':'EN_FRENCH_REVIEW_REFERENCE.json'}
    (HERE/f'EN_REVIEWED_VERIFICATION_001_{end:03d}.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(summary,ensure_ascii=False))
    for d in diffs:
        if d['status']=='unreviewed literal difference':print(json.dumps(d,ensure_ascii=False))
    if any(d['status']=='unreviewed literal difference' for d in diffs):raise SystemExit(2)


if __name__=='__main__':main()
