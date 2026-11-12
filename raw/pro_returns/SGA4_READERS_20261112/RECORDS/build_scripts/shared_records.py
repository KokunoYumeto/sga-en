"""Shared provenance, disputes, credits, and unresolved-source appendices.

Only ZIP-relative source references are published. Original manifests' machine
paths and contact addresses are deliberately excluded from generated records.
"""
from pathlib import Path
import csv, json, re, collections, unicodedata

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT/'sources'
OUT = ROOT/'output'
REC = OUT/'records'
SHARED = OUT/'shared'

def clean(value):
    text = str(value if value is not None else '')
    # Preserve mathematical map strings such as f:\Spec. Require an observed
    # operating-system directory after a Windows drive prefix.
    text = re.sub(r'(?i)(?<![\w/])[A-Z]:[\\/](?:Users|home|Documents and Settings|Documents|Temp|Windows|Program Files)[\\/][^\s`"<>]+', '[private path omitted]', text)
    text = re.sub(r'(?i)(?<![\w/])/(?:Users|home|root|workspace)/[^\s`"<>]+', '[private path omitted]', text)
    text = re.sub(r'[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}', '[contact omitted]', text)
    return text

def safe_tree(value):
    if isinstance(value, dict):
        return {k:safe_tree(v) for k,v in value.items() if k not in {'scan_path','source_path','raw_path'}}
    if isinstance(value,list): return [safe_tree(v) for v in value]
    return clean(value) if isinstance(value,str) else value

def write_tsv(path, rows, fields):
    path.parent.mkdir(parents=True,exist_ok=True)
    with path.open('w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=fields,delimiter='\t',lineterminator='\n',extrasaction='ignore')
        w.writeheader()
        for r in rows:w.writerow({k:clean(v) for k,v in r.items()})

MATH_CHARS = {'∅':r'\varnothing','∈':r'\in','∉':r'\notin','⊂':r'\subset','⊆':r'\subseteq',
    '⊃':r'\supset','⊇':r'\supseteq','≠':r'\ne','≤':r'\leq','≥':r'\geq','→':r'\to','←':r'\leftarrow',
    '↔':r'\leftrightarrow','⇄':r'\rightleftarrows','⇒':r'\Rightarrow','⇔':r'\Leftrightarrow',
    '∏':r'\prod','∐':r'\coprod','∑':r'\sum','∞':r'\infty','∘':r'\circ','⊗':r'\otimes',
    '⊕':r'\oplus','ℓ':r'\ell','ℤ':r'\mathbf{Z}','ℝ':r'\mathbf{R}','ℚ':r'\mathbf{Q}',
    'ℂ':r'\mathbf{C}','ℕ':r'\mathbf{N}','ℙ':r'\mathbf{P}','π':r'\pi','Π':r'\Pi',
    'φ':r'\phi','ϕ':r'\varphi','ψ':r'\psi','Ψ':r'\Psi','δ':r'\delta','Δ':r'\Delta',
    'α':r'\alpha','β':r'\beta','γ':r'\gamma','Γ':r'\Gamma','η':r'\eta','ε':r'\varepsilon',
    'κ':r'\kappa','λ':r'\lambda','μ':r'\mu','ν':r'\nu','ρ':r'\rho','σ':r'\sigma','Σ':r'\Sigma',
    'τ':r'\tau','ω':r'\omega','Ω':r'\Omega','θ':r'\theta','ζ':r'\zeta',
    '×':r'\times','⋅':r'\cdot','·':r'\cdot','•':r'\bullet','∗':r'\ast','⋆':r'\star',
    '∧':r'\wedge','∨':r'\vee','∪':r'\cup','∩':r'\cap','∼':r'\sim','≃':r'\simeq','≅':r'\cong',
    '∀':r'\forall','∃':r'\exists','⊥':r'\perp','ℋ':r'\mathcal{H}','ℱ':r'\mathcal{F}',
    'ℰ':r'\mathcal{E}','ℒ':r'\mathcal{L}','ℳ':r'\mathcal{M}','ℐ':r'\mathcal{I}',
    'ℛ':r'\mathcal{R}','ℬ':r'\mathcal{B}','ℜ':r'\mathfrak{R}','ℑ':r'\mathfrak{I}',
    '℘':r'\wp','〈':r'\langle','〉':r'\rangle','⟨':r'\langle','⟩':r'\rangle',
    '⟶':r'\longrightarrow','ℭ':r'\mathfrak{C}','⇉':r'\rightrightarrows',
    '⟹':r'\Longrightarrow','⥲':r'⥲',
    '∿':r'∿','⊠':r'\boxtimes','⩾':r'\geqslant','⟼':r'\longmapsto','⨿':r'\amalg',
    '\u2009':r'\,'}
ESC = {'\\':r'\textbackslash{}','{':r'\{','}':r'\}','$':r'\$','&':r'\&','#':r'\#',
       '_':r'\_','%':r'\%','~':r'\textasciitilde{}','^':r'\textasciicircum{}'}

COMBINING_MATH = {'\u0302':r'\hat','\u0303':r'\tilde','\u0304':r'\bar',
                  '\u0305':r'\overline','\u030c':r'\check','\u0332':r'\underline'}

def tex(text):
    out=[]
    value=clean(text); i=0
    while i<len(value):
        c=value[i]
        if i+1<len(value) and value[i+1] in COMBINING_MATH and (c.isalnum() or c in MATH_CHARS):
            base=MATH_CHARS.get(c,c); i+=1
            while i<len(value) and value[i] in COMBINING_MATH:
                base=COMBINING_MATH[value[i]]+'{'+base+'}'; i+=1
            out.append(r'\ensuremath{'+base+'}')
            continue
        if c=='=':out.append(r'=\allowbreak ')
        elif c in ESC:out.append(ESC[c])
        elif c in MATH_CHARS:out.append(r'\ensuremath{'+MATH_CHARS[c]+'}')
        elif ord(c)>=0x1D400 and ord(c)<=0x1D7FF:out.append(r'\ensuremath{'+c+'}')
        elif c in '\r\n\t':out.append(' ')
        elif c=='\u00a0':out.append('~')
        else:out.append(c)
        i+=1
    return ''.join(out)

def reading_text(value):
    if isinstance(value,str):return clean(value)
    pieces=[]
    for r in value or []:
        if not isinstance(r,dict):pieces.append(str(r));continue
        parts=[]
        for k,label in [('where','Place'),('scan','Reported print'),('tex','Source TeX'),('corrected','Proposed correction'),('note','Note')]:
            if r.get(k):parts.append(label+': '+clean(r[k]))
        f=r.get('fix') or {}
        if f:parts.append('Proposed edit: '+clean(f.get('old',''))+' => '+clean(f.get('new','')))
        pieces.append('; '.join(parts))
    return ' || '.join(pieces)

def make_disputes():
    pages=json.loads((SRC/'api_pass_20261111/PAGES_FOR_APP_CHECK.json').read_text())
    rows=[]; indexed=[]; held=[]
    for p in pages:
        for item in p['items']:
            rid=f'DP{len(rows)+1:04d}'
            readings=item.get('readings',{})
            places=[]
            for model,rs in readings.items():
                for r in rs if isinstance(rs,list) else []:
                    if r.get('where') and r['where'] not in places:places.append(r['where'])
            row={'id':rid,'tome':p['tome'],'expose':p['expose'],'page':p['page'],
                'place':' | '.join(places),'reading_1_model':'Claude Opus 5.5',
                'reading_1':reading_text(readings.get('opus','No reading supplied')),
                'reading_2_model':'GPT-6.1 Sol','reading_2':reading_text(readings.get('sol','No reading supplied')),
                'kind':item['category'],'status':'held for scan comparison; agreed text retained',
                'source':'api_pass_20261111/PAGES_FOR_APP_CHECK.json#'+rid,'reason':item.get('why','')}
            rows.append(row)
            indexed.append(safe_tree(dict(row,file=p['file'],batch=p.get('batch'),readings=readings)))
            if item['category']=='agreed_fix_held' and "editors' apparatus" in item.get('why',''):
                held.append({'id':f'DEC-HELD-{len(held)+1:02d}','item':rid,'tome':p['tome'],'expose':p['expose'],
                    'page':p['page'],'place':row['place'],'decision':'held; no change to Orgogozo apparatus',
                    'reason':item['why'],'source':row['source']})
    assert len(rows)==643 and len(pages)==443 and len(held)==18
    write_tsv(REC/'DISPUTED_PLACES.tsv',rows,list(rows[0]))
    (SHARED/'disputes_index.json').write_text(json.dumps(indexed,ensure_ascii=False,indent=2)+'\n')
    (SHARED/'held_apparatus_decisions.json').write_text(json.dumps(held,ensure_ascii=False,indent=2)+'\n')
    for lang in ['FR','EN']:
        title='Lieux en litige : vérification sur les scans réservée' if lang=='FR' else 'Disputed places: scan comparison reserved'
        lines=[r'\chapter*{'+title+'}',r'\addcontentsline{toc}{chapter}{'+title+'}',
            tex('643 items on 443 printed pages. The agreed source text is retained. These records reproduce the submitted readings and do not decide the disputes.' if lang=='EN' else '643 points sur 443 pages imprimées. Le texte de la source convenue est conservé. Ces notices reproduisent les lectures consignées sans trancher les litiges.'),
            r'\begingroup\small\raggedright\sloppy\setlength{\parskip}{4pt}']
        for r in rows:
            lines.extend([r'\par\noindent\hypertarget{'+r['id']+r'}{}\textbf{'+tex(f"{r['id']} -- {r['expose']}, p. {r['page']} ({r['kind']})")+r'}\par',
                tex(r['place'])+r'\par',r'\textbf{Claude Opus 5.5.} '+tex(r['reading_1'])+r'\par',
                r'\textbf{GPT-6.1 Sol.} '+tex(r['reading_2'])+r'\par',tex(r['reason'])+r'\par'])
        lines.append(r'\endgroup')
        (SHARED/f'disputes_{lang}.tex').write_text('\n'.join(lines)+'\n')
    return rows,held

RIGHTS_EN="The rights in the original work belong to its author or the author's representatives or heirs. Where we hold rights, in the AI-produced transcription, translation, corrections and typesetting, they are dedicated to the public domain under CC0 1.0. This edition is published for educational, non-profit purposes, and we claim no rights we do not hold. If you hold rights in this work and object to its publication here, please open a GitHub issue and we will take it down."
RIGHTS_FR="Les droits sur l'œuvre originale appartiennent à son auteur, à ses représentants ou à ses ayants droit. Dans la mesure où nous détenons des droits sur la transcription, la traduction, les corrections et la composition produites par l'IA, nous les consacrons au domaine public sous CC0 1.0. Cette édition est publiée à des fins éducatives et non lucratives, et nous ne revendiquons aucun droit que nous ne détenons pas. Si vous détenez des droits sur cette œuvre et vous opposez à sa publication ici, veuillez ouvrir une issue GitHub et nous la retirerons."

def make_frontmatter():
    bibliography=[
        'M. Artin, A. Grothendieck, J.-L. Verdier, Théorie des topos et cohomologie étale des schémas (SGA 4), Séminaire de géométrie algébrique du Bois Marie, 1963--1964.',
        'Tome 1 : Théorie des topos. Lecture Notes in Mathematics 269. Springer-Verlag, Berlin--Heidelberg--New York, 1972. Exposés I--IV.',
        'Tome 2 : Théorie des topos. Lecture Notes in Mathematics 270. Springer-Verlag, Berlin--Heidelberg--New York, 1972. Exposés V--VIII, dont V bis.',
        'Tome 3 : Théorie des topos et cohomologie étale des schémas. Lecture Notes in Mathematics 305. Springer-Verlag, Berlin--Heidelberg--New York, 1973. Exposés IX--XIX.',
        'Avec la participation de N. Bourbaki, P. Deligne et B. Saint-Donat.']
    project_names='Bas Edixhoven; Yves Laszlo; Michel Raynaud; L. Bayle; N. Borne; O. Brinon; J. Buresi; M. Chardin; F. Ducrot; P. Graftiaux; F. Han; P. Karwasz; L. Koelblen; D. Madore; S. Morel; D. Naie; B. Osserman; J. Riou; V. Sécherre; C. Sabbah; Jacob C. Reinhold; Philippe Gille; Patrick Polo; Daniel Miller; Société mathématique de France.'
    for lang in ['FR','EN']:
        if lang=='FR':
            credits=["L'édition LaTeX de Fabrice Orgogozo, état 71766d9, est la base de toutes les couches de ces livres. Ses corrections consignées par la commande sisi et ses notes N.D.E. sont un travail éditorial humain et lui restent attribuées.",
                "Les auteurs et collaborateurs du séminaire sont crédités dans les exposés. Les notices du projet mentionnent notamment Michael Artin, Alexander Grothendieck, Jean-Louis Verdier, Nicolas Bourbaki, Pierre Deligne, Bernard Saint-Donat, Michèle Raynaud, Michel Raynaud, Nicholas Katz, Michel Demazure et Luc Illusie.",
                "Les crédits des autres volumes de la collection, conservés ici dans leur portée propre, nomment : "+project_names,
                "Travail d'IA consigné : OpenAI Codex (GPT-5.6 Sol, traduction ; GPT-6 Astra, corrections et assemblage), Claude Opus 5.5 (Anthropic), GPT-6.1 Sol (OpenAI API). Le contrôle des scans du 11 novembre 2026 a été effectué par Claude Opus 5.5 et GPT-6.1 Sol. La transcription LaTeX humaine d'Orgogozo reste créditée comme telle ; les couches produites par IA portent les mentions AI-transcribed, AI-translated et AI-produced corrections.",
                "La présente construction est due à GPT-6 Astra (OpenAI, ChatGPT Pro mode), le 12 novembre 2026. La traduction anglaise suit le dépôt sga-en, état 4a4cbac, et son édition du 12 novembre 2026."]
            heading='Sources, crédits et droits'
        else:
            credits=["Fabrice Orgogozo's LaTeX edition, snapshot 71766d9, is the foundation of every layer of these books. His recorded sisi corrections and N.D.E. notes are human editorial work and retain that attribution.",
                "The seminar authors and contributors retain the credits printed within the exposés. The project records name Michael Artin, Alexander Grothendieck, Jean-Louis Verdier, Nicolas Bourbaki, Pierre Deligne, Bernard Saint-Donat, Michèle Raynaud, Michel Raynaud, Nicholas Katz, Michel Demazure and Luc Illusie.",
                "The credits for the wider SGA collection, retained with their original scope, also name: "+project_names,
                "Recorded AI work includes OpenAI Codex (GPT-5.6 Sol: translation; GPT-6 Astra: corrections and assembly), Claude Opus 5.5 (Anthropic), and GPT-6.1 Sol (OpenAI API). Claude Opus 5.5 and GPT-6.1 Sol performed the scan check of 11 November 2026. Orgogozo's human LaTeX transcription retains its own attribution; the AI-produced layers are described as AI-transcribed, AI-translated and AI-produced corrections.",
                "This build is credited to GPT-6 Astra (OpenAI, ChatGPT Pro mode), 12 November 2026. The English follows sga-en at commit 4a4cbac and the release of 12 November 2026."]
            heading='Sources, credits and rights'
        lines=[r'\chapter*{'+heading+'}',r'\addcontentsline{toc}{chapter}{'+heading+'}',r'\begingroup\small']
        bib=bibliography if lang=='FR' else [x.replace('Tome ','Volume ').replace('dont V bis','including V bis').replace('Avec la participation de','With contributions by').replace(' et B. Saint-Donat',' and B. Saint-Donat') for x in bibliography]
        lines += [tex(x)+r'\par\medskip' for x in bib+credits]
        lines += [tex(RIGHTS_FR if lang=='FR' else RIGHTS_EN)+r'\par',
            r'\medskip\noindent\url{https://github.com/KokunoYumeto/sga-en/issues}',
            r'\par\noindent\url{https://creativecommons.org/publicdomain/zero/1.0/}',r'\par\endgroup\clearpage']
        (SHARED/f'frontmatter_{lang}.tex').write_text('\n'.join(lines)+'\n')

def main():
    for p in [REC,SHARED]:p.mkdir(parents=True,exist_ok=True)
    rows,held=make_disputes();make_frontmatter()
    make_possible_appendices()
    (REC/'SHARED_RECORD_COUNTS.json').write_text(json.dumps({'disputed_items':len(rows),'disputed_pages':443,
        'kinds':dict(collections.Counter(r['kind'] for r in rows)),'held_human_apparatus_fixes':len(held)},indent=2)+'\n')
    print('Created 643 dispute records, 18 held-apparatus decisions, and bilingual shared front matter.')

def make_possible_appendices():
    path=REC/'ONE_MODEL_MISPRINTS_JUDGED.tsv'
    if not path.exists():return
    rows=list(csv.DictReader(path.open(encoding='utf-8'),delimiter='\t'))
    possible=[r for r in rows if r['verdict']=='possible-not-verified']
    for lang in ['FR','EN']:
        title='Coquilles possibles, non vérifiées' if lang=='FR' else 'Possible misprints, not verified'
        introduction=("Ces propositions restent ouvertes. Aucune correction n'est déduite de ces notices ; le texte convenu est conservé. Les lectures et les motifs sont reproduits dans la langue du dossier source."
             if lang=='FR' else 'These proposals remain open. No correction is made on the authority of these notices; the agreed text is retained. Readings and reasons are quoted in the language of the source records.')
        parts=[r'\chapter*{'+title+'}',r'\addcontentsline{toc}{chapter}{'+title+'}',tex(introduction),
               r'\begingroup\small\raggedright\sloppy\setlength{\parskip}{4pt}']
        for r in possible:
            parts.extend([r'\par\noindent\textbf{'+tex(r['id']+' -- '+r['page']+' -- '+r['model'])+r'}\par',
                tex(r['place'])+r'\par',r'\emph{'+('Lecture signalée' if lang=='FR' else 'Reported reading')+'}: '+tex(r['reading'])+r'\par',
                r'\emph{'+('Proposition' if lang=='FR' else 'Proposal')+'}: '+tex(r['corrected_reading'])+r'\par',tex(r['reason'])+r'\par'])
        parts.append(r'\endgroup')
        (SHARED/f'possible_misprints_{lang}.tex').write_text('\n'.join(parts)+'\n')
    print('Possible-misprint appendices:',len(possible),'records each')

if __name__=='__main__':main()
