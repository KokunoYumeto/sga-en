#!/usr/bin/env python3
"""Make the two notes sections; unchanged readings are not counted variants."""
from pathlib import Path
import json, re
P=Path(__file__).parent
decisions={x['item']:x for x in json.loads((P/'decisions.json').read_text())}

def esc(s):
    return ''.join({'\\':r'\textbackslash{}','{':r'\{','}':r'\}','#':r'\#','$':r'\$','%':r'\%','&':r'\&','_':r'\_','^':r'\textasciicircum{}','~':r'\textasciitilde{}'}.get(c,c) for c in s)

# Literal mathematical alternatives use only ordinary amsmath symbols, not
# either reader's mutable source macros.  Each tuple has EN readings, FR
# readings, and the French reason.  English reasons are the decision record.
data={
'SOL-EN-010':(
 r'Retained: $f_{2*}(4)\circ(2)$. Proposed: $(f_{2*}(4)\circ(2))^{-1}$.',
 r'Lecture conservée : $f_{2*}(4)\circ(2)$. Proposition : $(f_{2*}(4)\circ(2))^{-1}$.',
 r'Les deux couches françaises fournies conservent le second chemin sans inverse dans le commentaire suivant 3.5. La traduction suit cette lecture. L’inverse proposé est une nouvelle correction mathématique ; la page imprimée et le diagramme complet doivent être revus avant de l’adopter.'),
'SOL-EN-017':(
 r'Retained: $(\{y\}\times Y,B)$. Proposed: $(\{x\}\times Y,B)$.',
 r'Lecture conservée : $(\{y\}\times Y,B)$. Proposition : $(\{x\}\times Y,B)$.',
 r'La source française conserve $y$ dans ce couple, et l’anglais le reproduit. La proposition portant $x$ reste signalée pour contrôle de la page imprimée.'),
'SOL-EN-026':(
 r'Retained: the strict localization at $\bar z$. Proposed: the strict localization at $\bar s$.',
 r'Lecture conservée : le localisé strict en $\bar z$. Proposition : le localisé strict en $\bar s$.',
 r'Les deux couches françaises conservent la localisation en $\bar z$ dans cette phrase. Le remplacement par $\bar s$ reste à vérifier sur la page imprimée.'),
'SOL-EN-028':(
 r'Retained: $R\Gamma(B\prime\cup D,i\prime_!(E\prime)|B\prime-(B\prime\cup D))$. Proposed: $R\Gamma(B\prime-D,i\prime_!(E\prime)|B\prime-D)$.',
 r'Lecture conservée : $R\Gamma(B\prime\cup D,i\prime_!(E\prime)|B\prime-(B\prime\cup D))$. Proposition : $R\Gamma(B\prime-D,i\prime_!(E\prime)|B\prime-D)$.',
 r'Les deux couches françaises conservent l’union et la différence emboîtée de cette formule. La lecture enregistrée reste dans le texte ; la proposition portant $B\prime-D$ attend le contrôle de la page.'),
'SOL-EN-029':(
 r'Retained: $\underline{\operatorname{Hom}}_A^\bullet(E,E)\to A$. Proposed target: $A_\natural$.',
 r'Lecture conservée : $\underline{\operatorname{Hom}}_A^\bullet(E,E)\to A$. But proposé : $A_\natural$.',
 r'La source française conserve $A$ dans cette phrase, tandis que les constructions voisines emploient $A_\natural$. La page imprimée est nécessaire avant d’adopter le changement proposé du but.'),
'SOL-EN-033':(
 r'Retained reference: 5.3.6. Proposed reference: 5.3.5.',
 r'Renvoi conservé : 5.3.6. Renvoi proposé : 5.3.5.',
 r'Les deux couches françaises donnent 5.3.6 après (5.9.1). Le renvoi imprimé enregistré est conservé ; 5.3.5 reste une proposition à contrôler sur la page.'),
'SOL-EN-046':(
 r'Retained: $E_2=KA_{X_1}$. Proposed: $F_1=KA_{X_1}$.',
 r'Lecture conservée : $E_2=KA_{X_1}$. Proposition : $F_1=KA_{X_1}$.',
 r'La couche française corrigée fournie porte elle aussi $E_2$. La proposition $F_1$ est enregistrée séparément, sans modifier cette lecture avant contrôle de l’imprimé.'),
'SOL-EN-050':(
 r'Retained: $D_c({}_AX)=D_c({}_{A[G]}X)$. Proposed left side: $D_c(G,{}_AX)$.',
 r'Lecture conservée : $D_c({}_AX)=D_c({}_{A[G]}X)$. Premier membre proposé : $D_c(G,{}_AX)$.',
 r'Les deux couches françaises conservent le premier membre sans argument $G$. La lecture de la source reste dans le corps du texte ; l’ajout proposé est soumis à la vérification de la page.'),
'SOL-EN-052':(
 r'Retained: $F^n\Lambda_X=0$ for $n\geq1$. Proposed bound: $n\geq2$.',
 r'Lecture conservée : $F^n\Lambda_X=0$ pour $n\geq1$. Borne proposée : $n\geq2$.',
 r'Les deux couches françaises conservent la borne $n\geq1$ à côté de la définition distincte de $F^1$. La lecture imprimée enregistrée est gardée et la borne proposée attend le scan.'),
'SOL-EN-053':(
 r'Retained target: $c_2^!(\Lambda_{X-U,X})$. Proposed target: $c_2^!(\Lambda_{U,X})$.',
 r'But conservé : $c_2^!(\Lambda_{X-U,X})$. But proposé : $c_2^!(\Lambda_{U,X})$.',
 r'Les deux couches françaises donnent le premier de ces buts dans la correspondance graduée de degré un. Ce but est conservé ; le second reste une lecture proposée à vérifier.'),
'SOL-EN-056':(
 r'Retained: every point $x$ of $G$. Proposed: every point $x$ of $C$.',
 r'Lecture conservée : tout point $x$ de $G$. Proposition : tout point $x$ de $C$.',
 r'Le français fourni porte lui aussi « pour tout point $x$ de $G$ ». Cette lecture reste dans les lecteurs ; $C$ est signalé comme alternative à vérifier sur l’imprimé.'),
'SOL-EN-057':(
 r'Retained: $f_*M$. Proposed: $f_*L$.',
 r'Lecture conservée : $f_*M$. Proposition : $f_*L$.',
 r'Les deux couches françaises conservent $f_*M$ dans la proposition 6.19. La proposition portant $L$ est maintenue dans cette note pour contrôle de la page.'),
'SOL-EN-062':(
 r'Retained: $\underline{\operatorname{Hom}}_A(M,\operatorname{Hom}_{C}(X,Y))$. Proposed outer symbol: $\operatorname{Hom}_A$.',
 r'Lecture conservée : $\underline{\operatorname{Hom}}_A(M,\operatorname{Hom}_{C}(X,Y))$. Symbole extérieur proposé : $\operatorname{Hom}_A$.',
 r'Le français fourni souligne le Hom extérieur à cet endroit, comme le fait l’anglais porté. Cette notation explicite de la source reste inchangée ; le Hom sans soulignement attend le contrôle de l’imprimé.'),
'SOL-EN-073':(
 r'Retained punctuation: ``cf. SGA 3 I 4.7.2).'' Proposed punctuation: ``cf. SGA 3 I 4.7.2.''',
 r'Ponctuation conservée : « cf. SGA 3 I 4.7.2). » Proposition : « cf. SGA 3 I 4.7.2. »',
 r'Les deux couches françaises contiennent cette parenthèse fermante sans parenthèse ouvrante correspondante. La ponctuation enregistrée est conservée jusqu’au contrôle de la page imprimée.'),
'SOL-EN-075':(
 r'Retained: Weil formula 6.1 and local invariants in no.~5. Proposed: formula 5.2 and local invariants in no.~6.',
 r'Lecture conservée : formule de Weil 6.1 et invariants locaux au n\textsuperscript{o}~5. Proposition : formule 5.2 et invariants locaux au n\textsuperscript{o}~6.',
 r'Les deux couches françaises conservent ces deux renvois. La renumérotation proposée reste dans les notes en attente de contrôle, sans changer les renvois du corps du texte.'),
'SOL-EN-076':(
 r'Retained: defined in 4.1. Proposed: defined in 3.4.',
 r'Lecture conservée : défini dans 4.1. Proposition : défini dans 3.4.',
 r'La proposition 3.6 française dit explicitement « défini dans 4.1 ». Le renvoi de la source est conservé ; 3.4 est enregistré comme alternative à vérifier.'),
'SOL-EN-077':(
 r'Retained reference: (4.3.1). Proposed reference: (3.7.1).',
 r'Renvoi conservé : (4.3.1). Renvoi proposé : (3.7.1).',
 r'Les deux couches françaises donnent (4.3.1) dans la phrase suivant (3.7.2). Le renvoi conservé et l’alternative sont présentés ensemble pour la vérification de la page.'),
'SOL-EN-086':(
 r'Retained: an endomorphism of $K\prime$. Proposed: an endomorphism of $K\prime_\nu$.',
 r'Lecture conservée : un endomorphisme de $K\prime$. Proposition : un endomorphisme de $K\prime_\nu$.',
 r'Le français fourni porte lui aussi $K\prime$ sans indice $\nu$ dans cette phrase. La lecture enregistrée reste dans le texte ; l’alternative indexée attend le scan.'),
'REVIEW-5-01':(
 r'Retained: ``faisceau normal'' (normal sheaf). Handwritten alternative: ``faisceau conormal'' (conormal sheaf).',
 r'Lecture conservée : « faisceau normal ». Insertion manuscrite proposée : « faisceau conormal ».',
 r'Le dossier classe le mince ajout « co » comme une annotation du lecteur et conserve « normal ». Le même énoncé donne explicitement $N=J/J^2$ et emploie son dual. La formule est donc transcrite sans changer le nom enregistré. L’image de la page 299 n’est pas fournie : la nature de l’ajout manuscrit reste à vérifier.'),
'GLOBAL-85-LABELS':(
 r'Retained: the source’s bold mixed-case statement labels. Recorded print alternative: DEFINITION 1.1.~- and the related capital labels.',
 r'Lecture conservée : les intitulés en gras et en casse mixte de la source. Alternative imprimée enregistrée : DEFINITION 1.1.~- et les intitulés en capitales correspondants.',
 r'Le dossier donne des exemples, sans fournir le relevé complet de chaque intitulé. Les scans correspondants manquent. Les formes de la source finale sont donc gardées ; aucun remplacement uniforme n’est déduit de ces seuls exemples.'),
'GLOBAL-85-ARROWS':(
 r'Retained: lower horizontal arrow labels below their arrows. Recorded print alternative: labels above those arrows.',
 r'Lecture conservée : étiquettes des flèches horizontales inférieures placées au-dessous. Alternative imprimée enregistrée : étiquettes placées au-dessus.',
 r'Cette observation de placement n’a pas été détaillée diagramme par diagramme. Les sources, buts et étiquettes des flèches sont conservés. Les déplacer par une règle générale exige les pages absentes et une vérification de chaque diagramme.'),
'GLOBAL-89a':(
 r'Retained: bold mixed-case labels. Recorded print alternatives: capital labels with ``.-'', a dash alone, or no stop or dash, according to the particular statement.',
 r'Lecture conservée : intitulés en gras et en casse mixte. Alternatives imprimées enregistrées : capitales avec « .- », un tiret seul, ou ni point ni tiret selon l’énoncé.',
 r'Le dossier signale plusieurs ponctuations, dont un intitulé sans point ni tiret. Il ne donne pas de relevé complet permettant un remplacement uniforme. Les intitulés restent ceux de la source finale jusqu’à l’examen des pages.'),
'GLOBAL-89b':(
 r'Retained: the source’s itemized readings at each occurrence. Remaining alternatives for unitemized sites: plain $R$ or double-struck $\mathbb{R}$; the record names exceptions in $Rp_*$, $R_!p$, $Rf_*$ in the proof of 1.2.',
 r'Lecture conservée : les choix détaillés de la source à chaque occurrence. Alternatives restantes aux endroits non détaillés : $R$ ordinaire ou $\mathbb{R}$ à double trait ; le dossier nomme des exceptions dans $Rp_*$, $R_!p$, $Rf_*$ dans la preuve de 1.2.',
 r'Les contrôles par page ont déjà appliqué des corrections de caractère et ont expressément nommé des exceptions. Ces lectures et leur portée locale sont conservées. Les occurrences encore non examinées ne sont pas déduites d’une définition globale de macro.'),
'GLOBAL-89c':(
 r'Retained: $\mathbb{P}$ and $\mathbb{E}$. Recorded print alternatives: typed $P$ and $E$ at 21 reported places.',
 r'Lecture conservée : $\mathbb{P}$ et $\mathbb{E}$. Alternatives imprimées enregistrées : $P$ et $E$ dactylographiés, en 21 endroits signalés.',
 r'La note globale n’individualise pas ces 21 occurrences. Les pages absentes sont nécessaires pour relier chaque constat au symbole précis. Les formes de la source finale sont conservées et les deux caractères restent signalés.'),
'GLOBAL-89e':(
 r'Retained: the capitalization checked at each occurrence. Pending alternatives at unitemized places: Module and module.',
 r'Lecture conservée : les capitales vérifiées à chaque occurrence. Alternatives restantes aux endroits non détaillés : Module et module.',
 r'Le dossier demande expressément un contrôle par occurrence, sans remplacement aveugle. Les formes finales déjà vérifiées sont conservées ; le constat général reste signalé sans modifier les passages non examinés.'),
'GLOBAL-89f':(
 r'Retained: the source’s $\mathcal{O}$ occurrences. Recorded print alternatives: typed plain $O$ and hand-drawn script $\mathcal{O}_C$.',
 r'Lecture conservée : les occurrences de $\mathcal{O}$ de la source. Alternatives imprimées enregistrées : $O$ dactylographié ordinaire et $\mathcal{O}_C$ manuscrit de forme cursive.',
 r'La note décrit plusieurs caractères sans donner de liste complète des occurrences. Un remplacement général effacerait cette variation enregistrée. Les caractères de la source finale restent en place ; les alternatives attendent les images.'),
'GLOBAL-VIII-CATEGORIES':(
 r'Retained: script $\mathcal{C},\mathcal{D},\mathcal{A},\mathcal{B}$. Recorded print alternatives: typed capitals $C,D,A,B$.',
 r'Lecture conservée : lettres cursives $\mathcal{C},\mathcal{D},\mathcal{A},\mathcal{B}$. Alternatives imprimées enregistrées : capitales dactylographiées $C,D,A,B$.',
 r'La note non numérotée pose une question de caractère, sans liste d’occurrences, et renvoie à la convention générale. Le texte final est conservé. Les quatre macros de catégories ne sont pas redéfinies globalement sur la seule base de cette note.'),
'GLOBAL-VIII-QUOTES':(
 r'Retained: each quotation mark in the final source. Recorded alternatives: straight typewriter quotes and guillemets; six pairs are mentioned.',
 r'Lecture conservée : les guillemets de chaque passage dans la source finale. Alternatives enregistrées : guillemets dactylographiés droits et guillemets français ; six paires sont signalées.',
 r'La note indique que les deux paires des pages 354--355 ont fait l’objet de corrections détaillées. Les formes finales sont conservées à ces endroits et ailleurs. Les images manquantes empêchent une nouvelle transcription uniforme des six paires.'),
'GLOBAL-VII-SET-DIFFERENCE':(
 r'Retained: the two itemized signs $X\mathbin{\dot{-}}Y$ and $X\prime\mathbin{\dot{-}}Y\prime$ on p.~301, and the existing signs elsewhere. Pending alternatives elsewhere: dotted minus and the existing ordinary set-difference sign.',
 r'Lecture conservée : les deux signes détaillés $X\mathbin{\dot{-}}Y$ et $X\prime\mathbin{\dot{-}}Y\prime$ à la page 301, ainsi que les signes existants ailleurs. Alternatives restantes ailleurs : moins pointé et signe ordinaire de différence ensembliste.',
 r'La source finale écrit explicitement le moins pointé dans les deux complémentaires de la page 301. Les autres occurrences n’ont pas été examinées dans la note fournie. Leurs signes restent donc inchangés jusqu’au contrôle des pages.'),
'GLOBAL-98b':(
 r'Retained in both branches: $\underline{\operatorname{\mathbb{F}r}}_{Y/S}:Y\longrightarrow Y^{(p/S)}$. Unresolved alternative: $\underline{\operatorname{Fr}}_{Y/S}:Y\longrightarrow Y^{(p/S)}$.',
 r'Lecture conservée dans les deux branches : $\underline{\operatorname{\mathbb{F}r}}_{Y/S}:Y\longrightarrow Y^{(p/S)}$. Alternative non résolue : $\underline{\operatorname{Fr}}_{Y/S}:Y\longrightarrow Y^{(p/S)}$.',
 r'Le point 98 laisse expressément cette occurrence ouverte face à la convention générale du point 78. L’entrée 572 du registre MISPRINTS\_5 décrit le F à double trait et son soulignement, tout en réservant son traitement à la décision sur les caractères du typographe. Le scan de la page 441 n’est pas fourni. La règle retenue pour les lectures non vérifiées impose donc de conserver la lecture imprimée enregistrée dans les six lecteurs ; l’alternative à F ordinaire reste ici en attente du scan. Le morphisme de Frobenius relatif $Y\to Y^{(p/S)}$ et les autres symboles de cette formule sont conservés.'),
}

inherited_english_only={'EN-INHERITED-0046-P43'}
expected={k for k,v in decisions.items() if 'needs the scan' in v['decision'] and k not in inherited_english_only}
assert set(data)==expected,(set(data)^expected)
for lang in ['EN','FR']:
    lines=[r'\section*{'+('Readings awaiting the scans' if lang=='EN' else 'Lectures en attente des scans')+'}',r'\begingroup\small']
    lines.append('These notes preserve unresolved alternatives without changing the retained reading. They are separate from the numbered apparatus of differences between the diplomatic and corrected texts. Each item needs the scan.' if lang=='EN' else 'Ces notes conservent les alternatives non résolues sans modifier la lecture retenue. Elles sont distinctes de l’apparat numéroté des différences entre textes diplomatique et corrigé. Chaque point nécessite le scan.')
    for key,(en,fr,reason_fr) in data.items():
        d=decisions[key]
        printed_place=d['page']
        if lang=='FR':
            printed_place=printed_place.replace('Exposé VII, including 295','Exposé VII, notamment 295').replace('301 and Exposé VII','301 et Exposé VII')
        lines.extend(['',r'\medskip\noindent\textbf{'+esc(key)+' (folio '+esc(printed_place)+r').}\par',en if lang=='EN' else fr])
        lines.append(esc(d['reason']) if lang=='EN' else reason_fr)
        source='port/SOL_NOTES_5.md' if key.startswith('SOL-') else ('fixes/REVIEW_5_OPEN.jsonl' if key.startswith('REVIEW') else 'conventions/GLOBAL_ISSUES_SGA.md')
        if key=='GLOBAL-98b':source+='; fixes/MISPRINTS_5.json, entry 572'
        lines.append(r'\par\noindent\textit{Source: }\texttt{'+esc(source)+'}. '+('Status: needs the scan.' if lang=='EN' else 'Statut : nécessite le scan.'))
    lines.extend([r'\endgroup',r'\clearpage',''])
    fragment='\n'.join(lines)
    # The records spell prime names explicitly; typeset them as superscripts.
    fragment=re.sub(r'([A-Za-z])\\prime',lambda m:m.group(1)+"'",fragment)
    (P/('unresolved_notes_'+lang+'.tex')).write_text(fragment)
(P/'unresolved_notes_inventory.json').write_text(json.dumps({'count':len(data),'included_ids':list(data),'excluded_existing_variant':[],'additional_inherited_English_only_note_ids':sorted(inherited_english_only),'rule':'Only unresolved notes with the same retained reading in both branches. GLOBAL-98b now retains the recorded print in both branches and is not a counted variant. The inherited English I 4.6 footnote is relocated separately by the English wrapper and is not added to these 30 shared notes.'},indent=2)+'\n')
print(json.dumps({'unresolved_notes_per_language':len(data)}))
