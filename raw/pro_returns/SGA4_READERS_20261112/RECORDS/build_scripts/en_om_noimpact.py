"""Language-neutral one-model changes, with individually read English evidence."""
from pathlib import Path
import json,re
from en_extra import page_window,find_matches
ROOT=Path(__file__).resolve().parents[1]
CHOICES={
'OPUS':{1:3,7:4,8:3,14:3,17:0,36:1,42:0,43:1,55:3,77:0,116:2,123:3,125:1,137:1,172:1,178:0,198:0,212:1,252:3,255:0,257:1},
'SOL':{13:1,30:1,62:1,75:2,78:1,113:4,119:2,150:1,162:4,172:1,185:2,196:1,197:0,243:3,279:1,300:4,383:4,424:2,487:4,488:2,501:1,503:5,531:1,691:4,693:3,698:1,703:1,729:1,763:1,788:1,906:2,924:2,944:1,945:1,974:3,1028:4,1057:1,1268:1,1330:1}
}
CH={f'OM-{m}-{n:04d}':i for m,rs in CHOICES.items() for n,i in rs.items()}
DIRECT={
'OM-OPUS-0051':r'One sees at once that this gives a functor',
'OM-OPUS-0093':r'hypercovering of type $p$ of $X$) means a hypercovering',
'OM-OPUS-0209':r'to be the $0$\textsuperscript{th} left derived functor',
'OM-SOL-0046':r'and shall merely point out that',
'OM-SOL-0076':r'are left exact, \ie commute with finite projective limits',
'OM-SOL-0146':r'carries equivalence relations on $C$ to equivalence relations on $\Phi(C)$.',
'OM-SOL-0157':r'Let $C$ be a site whose underlying category',
'OM-SOL-0391':r'Let $C$ be a site in which fiber products are representable',
'OM-SOL-0475':r'Let $E \xrightarrow{\pi} B$ be a functor',
'OM-SOL-0489':r'Let $E$ be a topos, and let $C$ be a strictly full subcategory',
'OM-SOL-0516':r'for every quasi-compact arrow $u$ of $E$',
'OM-SOL-0522':r'its image under $i^{\ast}$ is quasi-compact',
'OM-SOL-0554':r'\item[L2)] For every pair of morphisms',
'OM-SOL-0624':r'In what follows, unless expressly stated otherwise',
}
SPECIAL={
'OM-SOL-0046':'The released rendering is “shall merely point out”; the missing French reflexive pronoun has no separate word in this English construction.',
'OM-SOL-0062':'English already uses “restrict ourselves”; the French reflexive-pronoun repair leaves that same construction and its object unchanged.',
'OM-SOL-0063':'The released English takes “Formula ... together with ...” as its subject and uses “gives”; French plural verb agreement introduces no different English assertion.',
'OM-SOL-0085':'The released English reads “This, together with the argument of c), shows”; the French coordination agreement leaves this English construction unchanged.',
'OM-SOL-0090':'Both readings of the French fixed expression are rendered “as the need arises”; its missing French preposition has no additional English counterpart.',
'OM-SOL-0146':'The sentence already speaks of carrying equivalence relations; its English repeats that plural at the target. The French singular ending is an agreement slip within the same assertion.',
'OM-SOL-0150':'The released English explicitly names the two sequences and says “respectively”; changing the French anaphoric agreement leaves this wording unchanged.',
'OM-SOL-0162':'Both sets are named in the unchanged subject. English uses “are small” for that coordinated subject; the French agreement repair changes neither set nor property.',
'OM-SOL-0229':'The unchanged subject is a covering family. The released English renders its property as “is epimorphic”; repairing the French noun/adjective form leaves that predicate unchanged.',
'OM-SOL-0240':'The reference is rendered “in Exercise” followed by its number; French alone requires the added definite article.',
'OM-SOL-0251':'The repeated French preposition belongs to the fixed term “adjoint à droite”; both readings render the unchanged term “right adjoint”.',
'OM-SOL-0279':'The singular functorial morphism is explicitly named in both readings; correcting the French article agreement leaves “the functorial morphism” unchanged.',
'OM-SOL-0285':'The released English uses the compound “gluing functor”; the inserted French linking preposition adds no English word or mathematical data.',
'OM-SOL-0481':'The released phrase is “confined ourselves ... to proving”; the French preposition repair leaves this same infinitival construction unchanged.',
'OM-SOL-0501':'English uses the gender-neutral pronoun “it” for the category; the French masculine/feminine correction has no English counterpart.',
'OM-SOL-0537':'The invariant English adverb is “even”; removing an erroneous French plural ending leaves the expression unchanged.',
'OM-SOL-0693':'The released expression is “a constructible sheaf of sets”; English does not inflect “constructible” for the French number agreement.',
'OM-SOL-0819':'The released expression is “a constructible sheaf of groups”; English does not inflect “constructible” for the French number agreement.',
'OM-SOL-0857':'The object is explicitly the fraction field K of A in the unchanged context; the released English definite phrase remains the same after the French contraction repair.',
'OM-SOL-0870':'The released phrase is “clopen subsets of Y-prime”; the extra French article contracted in des adds no mathematical object or separate English word.',
'OM-SOL-0945':'The released English uses the singular attributive compound “direct-image functors”; correcting the French adjective agreement leaves the compound unchanged.',
'OM-SOL-1152':'The released English renders the fixed expression by “determinants over”; removing the spurious French plural from rapport adds no English change.',
}

def main():
    q=json.loads((ROOT/'work_fr/en_om_review_queue.json').read_text());s=(ROOT/'work_fr/en_om_corrected_snapshot.tex').read_text();out=[]
    for r in q:
        if r['assessment']!='no English impact':continue
        ident=r['id'];ev=r['english_contexts'][CH.get(ident,0)]['text']
        if ident in DIRECT:
            a,b=page_window(s,r['expose'],r['page'],1);hits=find_matches(DIRECT[ident],s[a:b])
            if len(hits)!=1:print('DIRECT NEEDS REVIEW',ident,len(hits));continue
            x,y=hits[0];ev=s[max(a,a+x-100):min(b,a+y+100)]
        reason=SPECIAL.get(ident,'The inspected English context retains the same expression after this French spelling or grammatical-agreement correction; the changed French letters have no counterpart in the English mathematical notation or wording.')
        out.append({'id':ident,'expose':r['expose'],'page':r['page'],'place':r['place'],'assessment':'no English impact','reason':reason,'french_pairs':r['french_pairs'],'english_evidence':ev,'evidence_reviewed':True,'english_deltas':[]})
    (ROOT/'output/shared/EN_ONE_MODEL_NO_IMPACT_PARTIAL.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
    print('Verified no-impact records',len(out))
if __name__=='__main__':main()
