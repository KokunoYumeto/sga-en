"""Independently inspect the 169 automatically represented one-model records.

The frozen baseline is read only. All resulting branch pairs have independently
read contexts; contextual overrides repair false already-present matches and
incomplete token reconstructions.
"""
from pathlib import Path
import json
from fr_core import find_exact
from review_t3 import locate
from marker_projection import carry_markers
ROOT=Path(__file__).resolve().parents[1]
OVERRIDES={
'OM-OPUS-0001':[(r"qu'on a définit ainsi un foncteur",r"qu'on a défini ainsi un foncteur")],
'OM-OPUS-0012':[(r'\check{C}=\Hhom(C,(\Ens)',r'\check{C}=\Hhom(C,(\Ens))')],
'OM-OPUS-0139':[(r'\cf la d scription des morphismes',r'\cf la description des morphismes')],
'OM-OPUS-0200':[(r'opérateurs de dégeneres-cence',r'opérateurs de dégénérescence')],
'OM-SOL-0032':[(r'De même $\varphi$ est conservative pour les monomorphismes',r'De même $\varphi$ est conservatif pour les monomorphismes')],
'OM-SOL-0113':[(r'« $\pi$-préaccessible »',r'« $\pi$-préaccessibles »')],
'OM-SOL-0146':[(r"en relation d'équivalence sur $\Phi (C)$.",r"en relations d'équivalence sur $\Phi (C)$.")],
'OM-SOL-0169':[(r'i_A a_A(\coim(i_A(u))',r'i_A a_A(\coim(i_A(u)))'),(r'i_A a_A (\coker(i_A (u))',r'i_A a_A (\coker(i_A (u)))')],
'OM-SOL-0172':[(r'provenant de famille couvrantes pour $T$',r'provenant de familles couvrantes pour $T$')],
'OM-SOL-0197':[(r'variétés ou espaces analytiques (réelles ou complexes, au choix)',r'variétés ou espaces analytiques (réels ou complexes, au choix)')],
'OM-SOL-0279':[(r'\id\longrightarrow j_\ast j^{\ast} $$ est isomorphe aux morphisme fonctoriel',r'\id\longrightarrow j_\ast j^{\ast} $$ est isomorphe au morphisme fonctoriel')],
'OM-SOL-0383':[(r'ce qui précède toute famille de support de $E$',r'ce qui précède toute famille de supports de $E$')],
'OM-SOL-0390':[(r'$K_∙$ est un objet semi-simplicial de $C^{\wedge}$ dont tout les objets sont semi-représentables',r'$K_∙$ est un objet semi-simplicial de $C^{\wedge}$ dont tous les objets sont semi-représentables')],
'OM-SOL-0424':[(r'$(F_{\lambda})$ un système inductif local de faisceau sur $\Tt_2$',r'$(F_{\lambda})$ un système inductif local de faisceaux sur $\Tt_2$')],
'OM-SOL-0522':[(r'son image par $i^{\ast}$ est quasi-compact',r'son image par $i^{\ast}$ est quasi-compacte')],
'OM-SOL-0554':[(r'\item [L2)] Pour tout couple de morphisme',r'\item [L2)] Pour tout couple de morphismes')],
'OM-SOL-0691':[(r"faisceaux d'ensembles localement constant sur $T$",r"faisceaux d'ensembles localement constants sur $T$")],
'OM-SOL-0693':[(r"Supposons que $F$ soit un faisceau d'ensembles constructibles.",r"Supposons que $F$ soit un faisceau d'ensembles constructible.")],
'OM-SOL-0819':[(r'Si $F$ est un faisceau de groupes constructibles',r'Si $F$ est un faisceau de groupes constructible')],
'OM-SOL-0871':[(r'normal ($\bar{S}\rightarrow S$ étant fini (\EGA IV 7.8.3 (iii) (vi)).',r'normal ($\bar{S}\rightarrow S$ étant fini (\EGA IV 7.8.3 (iii) (vi))).')],
'OM-SOL-1028':[(r'la composé des flèches \ding{195}',r'la composée des flèches \ding{195}')],
'OM-SOL-1047':[(r'Si $L$ est borné à composante de \ttor-dimension finie',r'Si $L$ est borné à composantes de \ttor-dimension finie')],
'OM-SOL-1118':[(r'formé des complexes de $\Oo_{X}$-modules',r'formée des complexes de $\Oo_{X}$-modules')],
'OM-SOL-1288':[(r'\emph{(\EGA IV 6.8.1 et 12.2.1 (vii)}',r'\emph{(\EGA IV 6.8.1 et 12.2.1 (vii))}')],
}
INTERMEDIATE={
('OM-OPUS-0012',1):r'\check{C}=Hom(C,(\Ens))',
('OM-OPUS-0139',1):r'\cf la scription des morphismes',
('OM-OPUS-0200',1):r'opérateurs de dégeneres',
('OM-SOL-0871',1):r'normal ($\bar{S}\rightarrow S$ étant fini (EGA IV 7.8.3 (iii) (vi)).',
('OM-SOL-1047',1):r'Si $L$ est borné à composante de tor-dimension finie',
('OM-SOL-1288',1):r'\emph{(EGA IV 6.8.1 et 12.2.1 (vii)}',
}
REPAIR_REASONS={
'OM-OPUS-0001':'The previous test matched unrelated occurrences of définit/défini; the specified clause still needed its diplomatic reading.',
'OM-OPUS-0012':'The previous token match changed Hom typography but did not restore the missing outer parenthesis. Both branches retain the source operator macro and differ only at the accepted delimiter.',
'OM-OPUS-0139':'The token projection had restored only scription. The complete reported printed reading is d scription.',
'OM-OPUS-0200':'The token projection had restored only dégeneres. The complete reported printed reading is dégeneres-cence.',
'OM-SOL-0032':'The previous test matched conservatif in a later diagram; the initial sentence still had conservative.',
'OM-SOL-0113':'The previous test matched a different plural préaccessibles; the pi-prefixed term still required its plural.',
'OM-SOL-0146':'The previous test matched relations earlier in the sentence; the final image of the equivalence relations remained singular.',
'OM-SOL-0172':'The previous test matched familles in other conditions; the specified footnote remained singular.',
'OM-SOL-0197':'The previous test matched réels in a later Lie-group example; the specified analytic-spaces phrase remained réelles.',
'OM-SOL-0383':'The previous test matched supports in other examples; the final sentence of item5 remained singular.',
'OM-SOL-0390':'The previous test matched the truncated-object clause; the subsequent untruncated-object clause retained tout.',
'OM-SOL-0424':'The previous test matched later systems of sheaves; proposition8.2.5 retained the singular faisceau.',
'OM-SOL-0522':'The previous test matched quasi-compacte in the j-star image clause; the i-star image at the page boundary remained masculine.',
'OM-SOL-0554':'The previous test matched the Fr3 condition; the requested L2 condition retained singular morphisme.',
'OM-SOL-0693':'The previous test matched constructible in other sentences; the opening set-valued case retained constructibles.',
'OM-SOL-0819':'The previous test matched constructible in adjacent module examples; the group-sheaf phrase retained constructibles.',
'OM-SOL-0871':'The previous token match changed EGA typography without repairing the outer delimiter; the source citation macro is restored and the complete parenthesis is represented.',
'OM-SOL-1047':'The accepted change is the plural composantes. Both branches preserve the source ttor macro; the automatic plain tor reconstruction is removed.',
'OM-SOL-1118':'The previous test matched formée in the following subcategory definition; the first definition retained formé.',
'OM-SOL-1288':'The delimiter reading was already represented; the automatic plain EGA reconstruction is removed so that both branches retain the source citation macro.',
}

def unique_spans(hits):
    spans={}
    for a,b,kind in hits:spans[a,b]=kind
    return [(a,b,k) for (a,b),k in spans.items()]

def main():
    data=json.loads((ROOT/'work_fr/om_auto_baseline.json').read_text())
    recs={r['id']:r for r in json.loads((ROOT/'work_fr/om_auto_scope.json').read_text())}
    inspected=json.loads((ROOT/'work_fr/om_auto_inspection.json').read_text())
    rows=[]
    for r in inspected:
        ident=r['id'];rec=recs[ident];f=rec['file'];page=rec['page']
        pairs=OVERRIDES.get(ident,[(p['printed'],p['corrected']) for p in r['pairs']])
        for j,(printed,corrected) in enumerate(pairs,1):
            assert printed!=corrected
            row={'id':ident,'part':j,'file':f,'page':page,'expose':rec['expose'],'place':rec['place'],'source':rec['source'],'printed':printed,'corrected':corrected,'reason':REPAIR_REASONS.get(ident,'The distinct printed and corrected readings occur in the independently inspected intended source context.'),'requires_repair':ident in REPAIR_REASONS}
            if ident=='OM-SOL-0021':row['represented_by']={'id':'OM-OPUS-0005','part':1}
            for layer,target in [('dip',printed),('corr',corrected)]:
                t=data[layer][f];hits=unique_spans(locate(t,printed,corrected,page))
                if not hits and (ident,j) in INTERMEDIATE:hits=[(a,b,'intermediate automatic reading') for a,b in find_exact(t,INTERMEDIATE[ident,j],page)]
                if not hits:hits=unique_spans(locate(t,printed,corrected,None))
                row[layer+'_hits']=len(hits)
                if len(hits)==1:
                    a,b,kind=hits[0];old=t[a:b];new=carry_markers(old,target)
                    row[layer]={'old':old,'new':new,'at':a,'state':kind,'context_before':t[max(0,a-90):a],'context_after':t[b:b+90]}
                    data[layer][f]=t[:a]+new+t[b:]
                else:row[layer]={'status':'needs-location-review'}
            rows.append(row)
    (ROOT/'output/shared/ONE_MODEL_FR_AUTO_AUDIT_PAIRS.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2)+'\n')
    repairs=[r for r in rows if r['requires_repair']]
    (ROOT/'output/shared/ONE_MODEL_FR_AUTO_REPAIRS.json').write_text(json.dumps(repairs,ensure_ascii=False,indent=2)+'\n')
    failed=[r for r in rows if r['dip_hits']!=1 or r['corr_hits']!=1]
    (ROOT/'work_fr/om_auto_unlocated.json').write_text(json.dumps(failed,ensure_ascii=False,indent=2)+'\n')
    print('Records',len(recs),'Parts',len(rows),'Repairs',len(repairs),'Unique both',len(rows)-len(failed),'Unlocated',len(failed))
    for r in failed:print(r['id'],r['part'],r['dip_hits'],r['corr_hits'])

if __name__=='__main__':main()
