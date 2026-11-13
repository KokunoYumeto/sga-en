"""Stable source and component identities. All stored paths are ZIP-relative."""
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OWNERS=['arcata','rapport_cycle','sommes','finitude_verdier']
COMPONENTS=[
 dict(key='introduction',name='Introduction',owner='arcata',fr='sga4.5-intro.tex',en='sga4half_intro_en.tex',pages=['III','IV']),
 dict(key='ariane',name='Un fil d’Ariane',owner='arcata',fr='ariane.tex',en='ariane_en.tex',pages=[str(x) for x in range(1,4)]),
 dict(key='1',name='Arcata',owner='arcata',fr='sga4.5-1.tex',en='sga4half_1_en.tex',pages=[str(x) for x in range(4,76)]),
 dict(key='2',name='Rapport',owner='rapport_cycle',fr='sga4.5-2.tex',en='sga4half_2_en.tex',pages=[str(x) for x in range(76,110)]),
 dict(key='3',name='Fonctions L',owner='rapport_cycle',fr='sga4.5-3.tex',en='sga4half_3_en.tex',pages=[str(x) for x in range(110,129)]),
 dict(key='4',name='Cycle',owner='rapport_cycle',fr='sga4.5-4.tex',en='sga4half_4_en.tex',pages=[str(x) for x in range(129,154)]),
 dict(key='5',name='Dualité',owner='rapport_cycle',fr='sga4.5-5.tex',en='sga4half_5_en.tex',pages=[str(x) for x in range(154,168)]),
 dict(key='6',name='Sommes trigonométriques',owner='sommes',fr='sga4.5-6.tex',en='sga4half_6_en.tex',pages=[str(x) for x in range(168,233)]),
 dict(key='7',name='Théorèmes de finitude',owner='finitude_verdier',fr='sga4.5-7.tex',en='sga4half_7_en.tex',pages=[str(x) for x in range(233,262)]),
 dict(key='8',name='Catégories dérivées',owner='finitude_verdier',fr='sga4.5-8.tex',en='sga4half_8_en.tex',pages=[str(x) for x in range(262,312)]),
 dict(key='erratum',name='Erratum pour SGA 4',owner='finitude_verdier',fr='sga4.5-erratum.tex',en='sga4half_erratum_en.tex',pages=['312']),
]
PAGE_ORDER=['III','IV']+[str(x) for x in range(1,313)]
PAGE_RANK={p:i for i,p in enumerate(PAGE_ORDER)}
PAGE_COMPONENT={p:c for c in COMPONENTS for p in c['pages']}
CITATIONS={
 '1':{'ar62':'[1]','gi64':'[5]','se94':'[14]','se59':'[15]','se55':'GAGA'},
 '2':{'de73':'[1]','gr95':'[2]','la83':'[3]','we48':'[4]'},
 '6':{'ca69-2':'[1]','de73':'[2]','dl76':'[3]','ka77':'[4]','se68':'[5]','sp76':'[6]','we74':'[7]','we52':'[8]','we74-2':'[9]'},
 '7':{'de71-1':'[1]','de71-2':'[2]','de74':'[3]','de80':'[4]'},
}

def component_path(c,lang):return ROOT/'work'/c['owner']/lang/c[lang]

def read_jsonl(path):
    import json
    return [json.loads(x) for x in path.read_text().splitlines() if x.strip()]

def all_rows(name):
    return [dict(x,record_owner=owner) for owner in OWNERS+(['glossary'] if name=='own_findings' else [])
            if (ROOT/'work'/owner/(name+'.jsonl')).exists()
            for x in read_jsonl(ROOT/'work'/owner/(name+'.jsonl'))]
