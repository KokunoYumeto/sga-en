"""English impact judgments and exact source anchors for accepted one-model reports."""
from pathlib import Path
import collections,json,re
from en_common import group,replace_spans,active_matches
from en_extra import page_window,find_matches,compact,transplant,key
ROOT=Path(__file__).resolve().parents[1]
OPUS_IMPACT=[3,5,12,28,31,60,63,65,73,82,83,90,92,101,110,115,117,127,152,154,157,167,173,228,238,244,247]
SOL_IMPACT=[3,7,8,11,21,33,60,86,112,118,124,136,169,173,174,180,201,252,277,303,336,348,352,353,359,373,374,375,378,379,382,385,386,393,437,441,472,473,493,494,495,497,498,499,500,506,536,543,550,582,585,594,605,611,612,613,614,617,631,639,643,646,667,681,682,731,742,744,748,749,760,765,766,767,774,775,784,786,811,823,871,889,935,989,1032,1035,1107,1108,1136,1267,1288,1309,1310,1319,1326,1332]
IMPACT={f'OM-OPUS-{x:04d}' for x in OPUS_IMPACT}|{f'OM-SOL-{x:04d}' for x in SOL_IMPACT}
# Each entry was read against its complete French change; these English words
# retrieve the actual released terminology for inspection, not replacement.
NOIMPACT_TERMS={
'OPUS':{1:'defin',7:'faithful',8:'inductive',9:'representable',13:'reconstit|reconstruct',14:'cardinal',15:'reader',17:'hypotheses',21:'passage|passing',26:'having|possess|admit',32:'immediate',35:'reconstit|reconstruct',36:'privileg|distinguished',37:'endow|equip',39:'call',40:'describ',41:'reconstit|reconstruct',42:'reconstit|reconstruct',43:'reconstit|reconstruct',44:'reconstit|reconstruct',50:'adjoint',51:'thus|therefore',53:'reconstit|reconstruct',54:'reconstit|reconstruct',55:'projective',56:'reconstit|reconstruct',57:'manifest|obvious',69:'isomorph',70:'intersection',71:'correspond',77:'homomorph',86:'represent',93:'hyper',98:'sheaf',100:'systems',116:'every|each',121:'exception',122:'suppos',123:'connected',124:'reconstit|reconstruct',125:'reconstit|reconstruct',137:'reduc',139:'description',145:'reconstit|reconstruct',153:'become',156:'only',165:'proof',168:'candidate',169:'call',172:'arbitrary|any',175:'consider|envisag',178:'respect',179:'embed',187:'axiom',192:'rid|remove',193:'comprehens|understand',194:'compos',197:'homomorph',198:'finite|family',199:'inductive',200:'degeneracy',202:'ordinary',209:'being',211:'specific',212:'follow',221:'flat',224:'functorial',246:'solv',248:'rational',252:'constant',253:'ring',255:'rational',256:'equidimensional',257:'prov'},
'SOL':{2:'such that',10:'kernel',13:'filter',20:'free',26:'double|parallel',27:'Let',30:'defined',32:'conservative',37:'such that',46:'ourselves|limit',51:'abuse',53:'obtained',54:'such as',61:'verification|details',62:'ourselves|restrict|limit',63:'immediate',66:'made',75:'representable',76:'left.exact|exact on the left',78:'left.exact|exact on the left',85:'argument',90:'as',111:'denot',113:'accessible',114:'variant',115:'epimorphism',119:'equal',123:'Let',134:'satisfied',135:'homomorphism',138:'inverse.image',146:'equivalence relation',147:'functorial morph|natural transform',150:'sequence',157:'Let',162:'small',172:'covering famil',182:'equipped|endowed',185:'Let',196:'consider',197:'real',200:'same',202:'impractic|unworkable',229:'epimorphic',236:'small',238:'same',240:'exercise',243:'equivalent',245:'induced',251:'right adjoint|right.adjoint',279:'functorial morph|natural transform',285:'gluing|glueing',298:'neighbo',300:'equivalence relation',345:'morphisms',356:'Modules|modules',383:'supports',384:'families',390:'all|every',391:'fiber|fibre',424:'sheaves',435:'terms',436:'preced',475:'Let',481:'prov',487:'quasi.separated',488:'quasi.separated',489:'Let',501:'contain',503:'perfect',509:'set of objects',516:'arrow',522:'quasi.compact',523:'quasi.compact',524:'also',525:'complement',526:'each',531:'pro.object',537:'even',541:'arbitrary',554:'pair',584:'continuous',624:'sequel|following',625:'two morphisms',632:'such that',670:'form',677:'sums',691:'locally constant',693:'constructible',698:'one of',703:'reduc',705:'biject',709:'Let',729:'dense',730:'open and dense',741:'replaced',763:'integral',788:'noetherian',794:'flat',799:'represented',800:'expressed',819:'constructible',850:'surjective',857:'field of fractions|fraction field',870:'open and closed',882:'sheaves of sets',894:'contravariant functors',895:'terms',899:'equipped|endowed',906:'distinguished triangles',924:'ringed sites',936:'commutative',939:'universal property',940:'invertible',944:'split',945:'direct.image',955:'terms',974:'compactifications',977:'recall',987:'first two columns',999:'sums',1028:'composite',1047:'dimension',1057:'soft sheaves',1100:'Let',1118:'consist|formed',1135:'decompositions',1137:'homology',1138:'simplicial',1139:'functorial',1146:'rings',1152:'respect to',1167:'reduc',1221:'pair',1262:'necessary',1268:'equipped|endowed',1300:'rings',1322:'developed',1323:'such as',1330:'appl',1337:'such that'}
}
TERMS={f'OM-{model}-{n:04d}':term for model,terms in NOIMPACT_TERMS.items() for n,term in terms.items()}
TERMS.update({'OM-OPUS-0036':'preferred','OM-OPUS-0124':'recovered','OM-OPUS-0125':'recovered','OM-OPUS-0178':'condition.*?holds|holds','OM-OPUS-0192':'dispense','OM-OPUS-0202':'usual','OM-SOL-0066':'included','OM-SOL-0135':'define a morphism','OM-SOL-0624':'follows','OM-SOL-0632':'such as','OM-SOL-0741':'replacing','OM-SOL-0870':'clopen','OM-SOL-0944':'adapted','OM-SOL-0977':'Bearing this in mind','OM-SOL-1146':'ring.theoretic','OM-SOL-1152':'determinants over','OM-SOL-1262':'needed'})

def selected(text,corrected):
    edits=[]
    for m in active_matches(r'\\SGA(?:quiet)?var\b(?=\s*\{)',text):
        if any(a<=m.start()<b for a,b,_ in edits):continue
        d,_,j,_=group(text,m.end());c,_,j,_=group(text,j);_,_,end,_=group(text,j)
        chosen=selected(c if corrected else d,corrected)
        if re.search(r'\\[A-Za-z]+$',chosen) and end<len(text) and text[end].isalpha():chosen+=' '
        edits.append((m.start(),end,chosen))
    return replace_spans(text,edits)

def initialize():
    rows=json.loads((ROOT/'output/shared/ONE_MODEL_FR_PATCHES.json').read_text())+json.loads((ROOT/'output/shared/ONE_MODEL_FR_AUTO_AUDIT_PAIRS.json').read_text())+json.loads((ROOT/'output/shared/ONE_MODEL_FR_0352_SUPPLEMENT.json').read_text())+json.loads((ROOT/'output/shared/ONE_MODEL_FR_1326_SUPPLEMENT.json').read_text())
    by=collections.defaultdict(list)
    for r in sorted(rows,key=lambda r:(r['id'],r['part'])):by[r['id']].append(r)
    assert len(by)==338
    assert not IMPACT&set(TERMS)
    assert IMPACT|set(TERMS)==set(by),(set(by)-IMPACT-set(TERMS),IMPACT-set(by),set(TERMS)-set(by))
    snapshot=ROOT/'work_fr/en_om_current_snapshot.tex'
    if not snapshot.exists():snapshot.write_text((ROOT/'output/en/SGA4_EN_annotated_master.tex').read_text())
    s=snapshot.read_text();dpath=ROOT/'work_fr/en_om_diplomatic_snapshot.tex';cpath=ROOT/'work_fr/en_om_corrected_snapshot.tex'
    d=dpath.read_text() if dpath.exists() else selected(s,False)
    c=cpath.read_text() if cpath.exists() else selected(s,True)
    (ROOT/'work_fr/en_om_diplomatic_snapshot.tex').write_text(d)
    (ROOT/'work_fr/en_om_corrected_snapshot.tex').write_text(c)
    review=[]
    for ident,rs in by.items():
        r=rs[0];exp=r['expose'];page=r['page'];w=page_window(c,exp,page,0);lo,hi=w or (0,0)
        text=c[lo:hi]
        item={'id':ident,'expose':exp,'page':page,'place':r['place'],'french_pairs':[{'part':x['part'],'printed':x['printed'],'corrected':x['corrected']} for x in rs],'assessment':'English-impact' if ident in IMPACT else 'no English impact'}
        if ident in TERMS:
            term=TERMS[ident];matches=list(re.finditer(term.replace(' ',r'\s+'),text,re.I))
            if not matches:
                lo,hi=page_window(c,exp,page,1);text=c[lo:hi];matches=list(re.finditer(term.replace(' ',r'\s+'),text,re.I))
            item['term_pattern']=term
            item['english_contexts']=[{'at':lo+m.start(),'text':text[max(0,m.start()-130):m.end()+170]} for m in matches[:6]]
        else:
            item['english_page']=text
        review.append(item)
    (ROOT/'work_fr/en_om_review_queue.json').write_text(json.dumps(review,ensure_ascii=False,indent=2)+'\n')
    print('Records',len(review),'Impact',len(IMPACT),'No impact',len(TERMS),'No term hit',[(r['id'],r.get('term_pattern')) for r in review if r['assessment']=='no English impact' and not r['english_contexts']])
if __name__=='__main__':initialize()
