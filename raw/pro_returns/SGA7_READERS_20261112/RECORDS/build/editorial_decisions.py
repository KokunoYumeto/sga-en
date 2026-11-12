#!/usr/bin/env python3
"""Reproduce the source-grounded editorial decisions and provenance fragments.

Inputs are read only from the supplied ZIP members, extracted under sources/.
No private source paths or e-mail addresses are copied into these outputs.
"""
from pathlib import Path
import csv
import json
import re

ROOT = Path(__file__).resolve().parents[1]
S = ROOT / 'sources'
R = ROOT / 'output' / 'records'
W = ROOT / 'work'


def tex(s):
    protected=[]
    def protect(m):
        protected.append(m[0]);return 'ZZPROTECTED'+str(len(protected)-1)+'ZZ'
    s=re.sub(r'https?://[^\s)]+|(?:en|fr|codex_french_corpus_aug2026)/[^\s,)]+|\b[A-Fa-f0-9]{40,64}\b',protect,s)
    s=''.join({'\\':r'\textbackslash{}','&':r'\&','%':r'\%','$':r'\$',
                    '#':r'\#','_':r'\_','{':r'\{','}':r'\}','~':r'\textasciitilde{}',
                    '^':r'\textasciicircum{}'}.get(c,c) for c in s)
    for i,p in enumerate(protected):
        s=s.replace('ZZPROTECTED'+str(i)+'ZZ',r'\url{'+p+'}')
    return s


def prose_to_tex(s):
    """Render textual source excerpts, retaining their wording and human credits."""
    s=re.sub(r'\[([^\]]+)\]\(([^)]+)\)',r'\1 (\2)',s)
    s=s.replace('**','').replace('*','').replace('`','')
    s=re.sub(r'(?m)^#+\s*','',s)
    paras=re.split(r'\n\s*\n',s.strip())
    return '\n\n'.join(tex(re.sub(r'\s+',' ',p)) for p in paras)+'\n'


def provenance():
    attr=(S/'en/repo/ATTRIBUTION.md').read_text()
    readme=(S/'en/repo/README.md').read_text()
    ai=readme[readme.index('Jacob C. Reinhold\'s English translation'):readme.index('\n## Status')].strip()
    src=(S/'en/repo/SOURCE_AUTHORITY.md').read_text()
    corpus_i=(S/'codex_french_corpus_aug2026/sga7i/README.md').read_text()
    corpus_ii=(S/'codex_french_corpus_aug2026/sga7ii/README.md').read_text()
    inherited_ref='en/evidence/supplemental_working_decisions/sga7i/INHERITED_ENGLISH_PROVENANCE_AND_ADVERSE_USE.md'
    inherited=(S/inherited_ref).read_text()
    inherited_auth=inherited[inherited.index('That service identity'):inherited.index('## Source-alignment findings')].strip()
    inherited_disposition=inherited[inherited.index('This witness is retained unchanged'):].strip()
    inherited_statement=(
        'The inherited witness documented in '+inherited_ref+' has 278,864 bytes and SHA-256 '
        'CFCB4C17081E16F963DCBC3FA04A43C4D4065477CB37BD931233840D287AA2E9. '
        'Its exact blob first appears in the public-mirror history at commit '
        'cb420190bbc6311cff96a08a5a11a4caf483fdff, dated 2026-05-29 12:24:48+02:00, '
        'under the generic identity “Manuscript Typesetting Project”; '
        'the Git blob is 2ac760f78b6107d2d71bd2e513e5baa4e3be418d. '
        'The local working paths and address are omitted for privacy.\n\n'+inherited_auth+'\n\n'+inherited_disposition)
    scope_en=(
        'Alexander Grothendieck, with M. Raynaud and D. S. Rim, Groupes de monodromie en géométrie '
        'algébrique I, Séminaire de géométrie algébrique du Bois-Marie 1967–1969 (SGA 7 I), '
        'Lecture Notes in Mathematics 288, Springer, 1972: Exposés I, II, VI–IX. '
        'Pierre Deligne and Nicholas Katz, Groupes de monodromie en géométrie algébrique II '
        '(SGA 7 II), Lecture Notes in Mathematics 340, Springer, 1973: Exposés X–XXII. '
        'The detailed authorship credits in the exposés are retained. '
        'The original-language Exposé VI by D. S. Rim is already English and remains English in both language readers.')
    scope_fr=(
        'Alexander Grothendieck, avec M. Raynaud et D. S. Rim, Groupes de monodromie en géométrie '
        'algébrique I, Séminaire de géométrie algébrique du Bois-Marie 1967–1969 (SGA 7 I), '
        'Lecture Notes in Mathematics 288, Springer, 1972 : exposés I, II, VI–IX. '
        'Pierre Deligne et Nicholas Katz, Groupes de monodromie en géométrie algébrique II '
        '(SGA 7 II), Lecture Notes in Mathematics 340, Springer, 1973 : exposés X–XXII. '
        'Les attributions détaillées des exposés sont conservées. '
        'L’exposé VI de D. S. Rim a été publié en anglais et reste en anglais dans les deux éditions linguistiques.')
    rights_en=("The rights in the original work belong to its author or the author's representatives or heirs. "
        'Where we hold rights, in the AI-produced transcription, translation, corrections and typesetting, '
        'they are dedicated to the public domain under CC0 1.0. This edition is published for educational, '
        'non-profit purposes, and we claim no rights we do not hold. If you hold rights in this work and '
        'object to its publication here, please open a GitHub issue and we will take it down.')
    rights_fr=(
        'Les droits sur l’œuvre originale appartiennent à son auteur ou aux représentants ou héritiers de celui-ci. '
        'Dans la mesure où nous détenons des droits sur la transcription, la traduction, les corrections et la '
        'composition produites par l’intelligence artificielle, nous les dédions au domaine public sous CC0 1.0. '
        'Cette édition est publiée à des fins éducatives et non lucratives, et nous ne revendiquons aucun droit '
        'que nous ne détenons pas. Si vous détenez des droits sur cette œuvre et vous opposez à sa publication '
        'ici, veuillez ouvrir un ticket GitHub et nous la retirerons.')
    provenance_intro_en=(
        'This build is credited to GPT-6 Astra (OpenAI, ChatGPT Pro mode). The French source is AI-transcribed; '
        'the English is AI-translated, except for Exposé VI, whose original English is retained. The edition '
        'contains AI-produced corrections. These descriptions do not transfer any human contribution to AI. '
        'The English authority is the supplied sga-en release v2026-11-12-english-edition, commit 4a4cbac; '
        'the French diplomatic and current layers, correction logs and decisions are the supplied November '
        '2026 records. The August French layer is used only as a change-log baseline. '
        'The following source excerpts preserve the recorded credits, including contributions to other '
        'volumes of the wider SGA project; those wider credits do not assert a contribution to SGA 7.')
    provenance_intro_fr=(
        'Cette construction est attribuée à GPT-6 Astra (OpenAI, ChatGPT Pro mode). La source française est '
        'AI-transcribed ; l’anglais est AI-translated, à l’exception de l’exposé VI dont l’anglais original '
        'est conservé. L’édition comporte des AI-produced corrections. Ces désignations n’attribuent à '
        'l’intelligence artificielle aucune contribution humaine. La source anglaise est la version fournie '
        'de sga-en, v2026-11-12-english-edition, commit 4a4cbac ; les couches françaises diplomatique et '
        'courante, journaux de corrections et décisions sont les enregistrements fournis de novembre 2026. '
        'La couche française d’août sert uniquement de référence au journal des changements. '
        'Les extraits anglais ci-dessous conservent les crédits des enregistrements, y compris ceux '
        'concernant les autres volumes du projet SGA ; ces derniers ne sont pas attribués à SGA 7.')
    numbering=src[src.index('SGA 7 I is complete'):src.index('\n- Published volume:')].strip()
    missing_en=(
        'The tables of contents in these readers are newly generated from the transcribed text. They do not '
        'purport to transcribe the printed tables. The SGA 7 II supplied layers begin with Exposé X; its '
        'preceding printed title, publication and contents pages are unavailable in these layers. '
        'SGA 7 I preserves its transcribed general introduction but has no separately transcribed printed '
        'contents table; no absent printed title or publication pages have been reconstructed. '
        'Exposés III–V are not missing transcriptions: the source-authority record explains their historical status.')
    missing_fr=(
        'Les tables des matières de ces lecteurs sont produites à partir du texte transcrit ; elles ne sont '
        'pas la transcription des tables imprimées. Les couches fournies de SGA 7 II commencent à l’exposé X : '
        'les pages de titre, de publication et de table des matières qui le précèdent ne figurent pas dans '
        'ces couches. SGA 7 I conserve son introduction générale transcrite mais ne comporte pas de table '
        'imprimée transcrite séparément ; aucune page de titre ou de publication absente n’a été reconstituée. '
        'Les exposés III–V ne sont pas des transcriptions manquantes : leur statut historique est expliqué '
        'dans l’enregistrement de l’autorité des sources reproduit ci-dessous.')
    for lang in ('en','fr'):
        chunks=[r'\section*{'+('Bibliographic identity' if lang=='en' else 'Identification bibliographique')+'}',
                tex(scope_en if lang=='en' else scope_fr),
                r'\section*{'+('Credits and provenance' if lang=='en' else 'Crédits et provenance')+'}',
                tex(provenance_intro_en if lang=='en' else provenance_intro_fr),
                r'\subsection*{'+('Recorded human contributions' if lang=='en' else 'Contributions humaines : enregistrement original')+'}',
                prose_to_tex(attr),
                r'\subsection*{'+('Recorded production history' if lang=='en' else 'Historique de production enregistré')+'}',
                prose_to_tex(ai),
                r'\subsection*{'+('SGA 7 I source authority' if lang=='en' else 'Autorité de la source de SGA 7 I')+'}',
                prose_to_tex(numbering),
                r'\subsection*{'+('Inherited English witness' if lang=='en' else 'Témoin anglais hérité')+'}',
                prose_to_tex(inherited_statement),
                r'\subsection*{'+('French corpus provenance' if lang=='en' else 'Provenance du corpus français')+'}',
                prose_to_tex(corpus_i),prose_to_tex(corpus_ii),
                r'\section*{'+('Printed front matter and contents' if lang=='en' else 'Pages liminaires imprimées et tables des matières')+'}',
                tex(missing_en if lang=='en' else missing_fr),
                r'\section*{'+('Rights' if lang=='en' else 'Droits')+'}',
                tex(rights_en if lang=='en' else rights_fr),
                r'\par\noindent\url{https://github.com/KokunoYumeto/sga-en/issues}',
                r'\par\noindent\url{https://creativecommons.org/publicdomain/zero/1.0/}',
                r'\clearpage']
        (W/f'frontmatter_{lang}.tex').write_text('\n\n'.join(chunks)+'\n')
    report='# Credits, rights and provenance\n\n'+scope_en+'\n\n'+provenance_intro_en+'\n\n'
    report+='## Source references\n\n'+('\n'.join('- `'+p+'`' for p in ['en/repo/README.md','en/repo/ATTRIBUTION.md','en/repo/SOURCE_AUTHORITY.md',inherited_ref,'codex_french_corpus_aug2026/sga7i/README.md','codex_french_corpus_aug2026/sga7ii/README.md']))+'\n\n'
    report+='## Recorded credits (verbatim wording; link markup simplified in the readers)\n\n'+attr+'\n\n'+ai+'\n\n'
    report+='## SGA 7 I source authority\n\n'+numbering+'\n\n## Inherited English\n\n'+inherited_statement+'\n\n'
    report+='## French binding records\n\n'+corpus_i+'\n\n'+corpus_ii+'\n\n## Missing printed front matter\n\n'+missing_en+'\n\n'
    report+='## Rights statement (English)\n\n'+rights_en+'\n\n## Déclaration de droits (français)\n\n'+rights_fr+'\n'
    (R/'PROVENANCE.md').write_text(report)


def page_text(volume,layer,filename,page):
    s=(S/'fr'/('sga7i' if volume=='7I' else 'sga7ii')/layer/filename).read_text()
    marks=list(re.finditer(r'%+\s*scan idx \d+\s*\|\s*folio (\d+)\s*%+',s))
    for i,m in enumerate(marks):
        if int(m[1])==page:
            return s[m.end():marks[i+1].start() if i+1<len(marks) else len(s)]
    raise ValueError((volume,filename,page))


def decisions():
    rows=[]
    patches=[]
    variants=[]
    notes=[]
    def row(item,page,readings,decision,reason,forms,source,status='decided'):
        rows.append(dict(item=item,page=page,readings=readings,decision=decision,reason=reason,
                         forms_affected=forms,source=source,status=status))
    def patch(item,language,volume,filename,page,old,new,reason,layer='current'):
        if language=='FR':
            text=page_text(volume,layer,filename,page)
            path='fr/'+('sga7i' if volume=='7I' else 'sga7ii')+'/'+layer+'/'+filename
        else:
            candidates=list((S/'en/sources/native'/('SGA7I' if volume=='7I' else 'SGA7II')).rglob(filename))
            assert len(candidates)==1,(filename,len(candidates))
            text=candidates[0].read_text();path=str(candidates[0].relative_to(S))
        assert text.count(old)==1,(item,filename,old,text.count(old))
        patches.append(dict(id=item,language=language,volume=volume,file=filename,source_path=path,page=page,
                            layer=layer,old=old,new=new,reason=reason,expected_count=1))
    forms_fr='FR corrected apparatus; FR plain reading'
    forms_all='FR and EN, all three forms'
    row('ED-MANUAL-7I-334','7I:334',r'IX\n\n<<CONT versus no running-head paragraph',
        'No further deletion; the requested removal is already reflected in both French layers.',
        'Both page-334 segments begin with the continuation “et de même le morphisme induit par”. '
        'Neither IX as a standalone body paragraph nor <<CONT remains. Global issues 57 and 59 record the '
        'continuation-tag pass and removal of the running head; replaying the stale string would be wrong.',
        forms_all,'fixes/MANUAL_7I_findings_331_335.json; conventions/GLOBAL_ISSUES_SGA.md:57,59','already resolved')
    row('ED-7I-356','7I:179',r'une catégorie cofibré $\underline{\Psi} versus une catégorie cofibrée $\underline{\Psi}',
        'Correct only the running sentence after (3.1.1), retaining the already-correct heading.',
        'The recorded old substring is also a prefix of “une catégorie cofibrée” in the heading; this explains '
        'the two substring matches. The exact suffix before the mathematical symbol isolates one grammatical '
        'error. Catégorie is feminine. English “cofibered category” has no corresponding gender variant.',
        forms_fr,'fixes/MISPRINTS_7I.json:356; fixes/misprint_pass/MISPRINT_PASS_LEFT_7I.json')
    patch('ED-7I-356','FR','7I','expose_VII_body.tex',179,
          r'Nous allons définir une catégorie cofibré $\underline{\Psi}',
          r'Nous allons définir une catégorie cofibrée $\underline{\Psi}',
          'Disambiguate the grammatical error from the already-correct heading by an exact context.')
    row('ED-7II-627','7II:353',"l'image ... n'est pas contenu versus n'est pas contenue",
        'Retain the corrected-layer contenue; no further body edit.',
        'Register identifiers are zero-based. Entry 627 is the feminine agreement error, already corrected '
        'in current. Its saved unclear decision discusses the different quotient omission at entries 626 '
        'and 1018; that mismatch is not evidence against the identifiable grammar correction.',
        forms_fr,'fixes/MISPRINTS_7II.json:627,1017; fixes/misprint_pass/decisions_misprints_7II_006.json','already correct')
    row('ED-7II-1018','7II:353',
        r'Printed: E^{n-1}=H^{n-1}(X_{\bar\eta},\mathbb Q_\ell(i))\quad H^{n-1}(X,Q_\ell(i)); current omits the equality; corrected: insert the recorded quotient slash and \mathbb Q.',
        'Restore the entire explanatory equality in corrected French and English, with the registered quotient reading.',
        'The equality is present in the supplied diplomatic page. The unclear-port claim of absence applies '
        'only to the already-abridged current layer. Entry 1018 identifies the missing quotient sign and '
        'coefficient typeface; the orthogonal complement/quotient interpretation is explained in its record. '
        'Restoring the recorded equality avoids dropping authorial text. No new denominator or proof is invented. '
        'The released English also omits the equality; the exact English body repair and its printed variant '
        'are recorded in EN_EDITORIAL_BODY_PATCH_1018.json as ED-7II-1018-EN.',
        'FR and EN corrected apparatus and plain reading; printed equality in both diplomatic forms',
        'fixes/MISPRINTS_7II.json:626,1018; fr/sga7ii/diplomatic/expose_XX_body.tex:353')
    patch('ED-7II-1018','FR','7II','expose_XX_body.tex',353,
          r"que son image dans $E^{n-1}(X_{\bar{\eta}},\mathbb{Q}_{\ell}(i))$ n'est pas nulle.",
          r"que son image dans $E^{n-1}(X_{\bar{\eta}},\mathbb{Q}_{\ell}(i)) = H^{n-1}(X_{\bar{\eta}},\mathbb{Q}_{\ell}(i)) / H^{n-1}(X,\mathbb{Q}_{\ell}(i))$ n'est pas nulle.",
          'Restore omitted printed equality, correcting only the recorded missing slash and coefficient typeface.')
    row('ED-VI-AUTHOR','7I:32–132','Original English Exposé VI in French source layers versus rewritten released English VI',
        'Use the original English source body, with the same diplomatic/current variants, in both language editions.',
        'Exposé VI was printed in English. The French source layers supply that original-language text; '
        'the released English component rewrites its sentences and mathematical presentation. Using the '
        'already-English authority preserves the author’s wording and every source folio. All release '
        'differences are recorded in CHANGES_EN.tsv.',forms_all,
        'fr/sga7i/diplomatic/expose_VI_body.tex; fr/sga7i/current/expose_VI_body.tex; en/repo/SOURCE_AUTHORITY.md')
    row('ED-en7I-C82','7I:102',r'Diagram label "\text{flat}"\prime versus "\text{flat}" (TikZ apostrophe changes label side)',
        'Use the source-layer corrected label placement in all forms; no print-misprint variant.',
        'C82 is zero-based FIXLOG_7I_CURRENT entry 82. The intended diagram is the pair-deformation diagram '
        'following Remark 4.6 on folio 102, not 4.1(d) on 97 as the unclear window note says. Both supplied '
        'French source layers already contain the corrected placement. ED-VI-AUTHOR carries it into English.',
        'EN all three forms','fixes/FIXLOG_7I_CURRENT.jsonl:C82; port/PORT_EN7I_LOG.jsonl:C82','resolved by source identity')
    row('ED-en7I-C713','7I:123','commute with base change versus commutes with base change',
        'Printed commute in diplomatic; corrected commutes in both corrected forms.',
        'The actual occurrence is Corollary 5.10(2), not Corollary 5.7(1) from the stale whole-file context. '
        'Its singular subject is J_S^p. Both readings are explicitly present in the paired original-English '
        'source pages and are included through ED-VI-AUTHOR.',
        'EN and FR all forms, variant by form','fixes/FIXLOG_7I_CURRENT.jsonl:C713; fixes/MISPRINTS_7I.json:254')
    row('ED-en7I-C874','7I:379',r'T_\ell(A\prime)/T_\ell(A\prime_K)^f versus T_\ell(A\prime_K)/T_\ell(A\prime_K)^f',
        'Corrected English already right at (5.5.8); restore the printed numerator only in diplomatic English.',
        'The folio-local intended occurrence is the second member of (5.5.8). The old window note '
        'mistakenly uses an earlier similar quotient in 5.2.6. Component 145 contains exactly the corrected '
        'generic-fibre numerator. The denominator is a Tate submodule of the generic fibre of A prime, making the restored '
        'subscript correction mathematically and textually determinate.',
        'EN diplomatic and apparatus variant','fixes/FIXLOG_7I_CURRENT.jsonl:C874; fixes/MISPRINTS_7I.json:609')
    variants.append(dict(id='ED-en7I-C874',volume='7I',file='145_expose_IX_sections_5_5_and_5_6.tex',page=379,
                         printed=r"T_\ell(A')/T_\ell(A'_K)^f",corrected=r"T_\ell(A'_K)/T_\ell(A'_K)^f"))
    old_c8=r'''We now prove (ii).  Since $D$ is regular, its strict transform $D'$ is
isomorphic to $D$ and meets $s^*$ with length one.  The assumption
$\operatorname{length}_{k(s)}(T\cap s^*)\leq n$ therefore implies
\[
\operatorname{length}_{k(s)}\bigl((D'\cup T)\cap s^*\bigr)\leq n+1,
\]
so that $D'\cup T$ satisfies the hypothesis of (i).'''
    new_c8=r'''Let $I_{D'\cap T}$ be the (principal) ideal of $\underline{O}_{D'}$
defining $D'\cap T$. Under the hypotheses (ii), the exact sequence
\begin{equation*}
0\longrightarrow I_{D'\cap T}\longrightarrow\underline{O}_{D'\cup T}
\longrightarrow O_T\longrightarrow0
\end{equation*}
shows that $D'\cup T$ satisfies hypothesis (i).'''
    dip_c8=new_c8.replace('(principal)','(principal').replace(r"\underline{O}_{D'\cup T}",r"\underline{O}_{D'\cap T}").replace("shows that $D'\\cup T$","shows that $D'\\cap T$")
    row('ED-en7II-C8','7II:24',r'0_T versus O_T; released replacement length argument versus omitted source exact sequence',
        'Restore a literal translation of the printed exact-sequence paragraph, with O_T in every form.',
        'The source sequence occurs in Lemma 2.14(ii) on p.24. It is absent from the released English, '
        'which substitutes a length argument. Both corrected and diplomatic French read O_T after the '
        'transcription repair, so zero-to-O is not an edition variant. The paragraph’s separate printed '
        'missing parenthesis and cap-for-cup misprints remain variants, as recorded on the same French page.',
        'EN all three forms','fixes/FIXLOG_7II_CURRENT.jsonl:C8; fr/sga7ii/diplomatic/expose_X_body.tex:24; fr/sga7ii/current/expose_X_body.tex:24')
    patch('ED-en7II-C8','EN','7II','005_expose_X_2_12_through_2_14.tex',24,old_c8,new_c8,
          'Restore source exact-sequence argument in place of the released substitute argument.','all')
    variants.append(dict(id='ED-en7II-C8-source',volume='7II',file='005_expose_X_2_12_through_2_14.tex',page=24,
                         printed=dip_c8,corrected=new_c8))
    row('ED-en7II-C17','7II:36',r'\widetilde\tau_0/\tau\overset\sim\longrightarrow versus \widetilde\tau_0/\tau\simeq',
        'Replace the arrow by the printed isomorphism relation in all English forms.',
        'The actual locus is the tangent-space identification after Lemma 2.33, not the Tor calculation '
        'in 1.6 cited by the stale whole-file context. The French diplomatic and current pages agree on '
        'simeq. The released English arrow is a transcription/presentation mismatch, not a printed misprint.',
        'EN all three forms','fixes/FIXLOG_7II_CURRENT.jsonl:C17; fr/sga7ii/diplomatic/expose_X_body.tex:36')
    patch('ED-en7II-C17','EN','7II','009_expose_X_2_31_through_bibliography.tex',36,
          r'\widetilde\tau_0/\tau\overset\sim\longrightarrow',r'\widetilde\tau_0/\tau\simeq',
          'The folio-local source has the isomorphism relation, not a labelled arrow.','all')
    row('ED-en7II-C138','7II:161',r'H^O versus H^0 in Lemma 4.18.5',
        'Retain the already-correct English H^0; no body edit or variant.',
        'The intended locus is the final degree-zero cohomology calculation in Lemma 4.18.5, not XIV 1.1.2 '
        'from the stale context. Component 062 has H^0 in all the pertinent factors. This is a transcription '
        'repair, also already in both French layers.',
        'EN all three forms','fixes/FIXLOG_7II_CURRENT.jsonl:C138; en/sources/native/SGA7II/components/062_expose_XIV_section_4_18.tex','already correct')
    row('ED-en7II-C475','7II:436',r'Final \right), in (6.2.8) versus \right)',
        'Remove the final comma in (6.2.8) in all English forms.',
        'The folio and formula tag identify this occurrence uniquely: the full component has the comma '
        'before end aligned, while both French layers omit it. The old unclear note incorrectly referred '
        'to (2.2.4.1), because its generic string had been found elsewhere in the exposé.',
        'EN all three forms','fixes/FIXLOG_7II_CURRENT.jsonl:C475; fr/sga7ii/diplomatic/expose_XXII_body.tex:436')
    patch('ED-en7II-C475','EN','7II','182_expose_XXII_cohomology_of_the_structure_sheaf.tex',436,
          '\\mathrel{\\Big|}W_S(1)\n\\right),\n\\end{aligned}',
          '\\mathrel{\\Big|}W_S(1)\n\\right)\n\\end{aligned}',
          'Remove the comma added by the transcription at the end of (6.2.8).','all')
    row('ED-en7II-C508','7II:14',r'n=\#[s^*,t] versus n=\#]s^*,t]; omitted in released English',
        'Restore the omitted parenthesis in English; retain the closed interval diplomatically and the half-open interval in corrected forms.',
        'The tree distance is the number of edges, not vertices. At t=s^*, n=0 but the closed interval '
        'has one element; excluding the root gives exactly n. This establishes the registered correction '
        'without needing a scan. The parenthetical is authorial text present in both French layers, so '
        'its absence from the release is repaired and logged.',
        'EN all forms; FR current retained','fixes/FIXLOG_7II_CURRENT.jsonl:C508; fixes/MISPRINTS_7II.json:12; conventions/GLOBAL_ISSUES_SGA.md:4')
    patch('ED-en7II-C508','EN','7II','003_expose_X_section_2_opening_through_2_9_statement.tex',14,
          '$t\\in S^*$ is the distance in the tree $S^*$ from $s^*$ to $t$.',
          '$t\\in S^*$ is the distance in the tree $S^*$ from $s^*$ to $t$ ($n = \\#]s^*,t]$).',
          'Restore the omitted source cardinality parenthesis.','all')
    variants.append(dict(id='ED-en7II-C508',volume='7II',file='003_expose_X_section_2_opening_through_2_9_statement.tex',page=14,
                         printed=r'($n = \#[s^*,t]$)',corrected=r'($n = \#]s^*,t]$)'))
    row('ED-XV-1.3.2-i','7II:175',r'English underlined $S$- versus French non-underlined $S$-',
        'Place $S$- outside the underline in all three English forms.',
        'Both French layers explicitly use $S$- followed by the underlined word schéma in clause (i). '
        'Clause (ii) of the English already uses the same boundary. This repairs source presentation '
        'without changing notation or creating a diplomatic/corrected variant.',
        'EN all three forms','fr/sga7ii/diplomatic/expose_XV_body.tex:175; en/sources/native/SGA7II/components/067_expose_XV_section_1_3.tex')
    patch('ED-XV-1.3.2-i','EN','7II','067_expose_XV_section_1_3.tex',175,
          r'such that the henselized $S$-scheme of $X$ at $x$ is isomorphic to',
          r'such that the henselized} $S$-\underline{scheme of $X$ at $x$ is isomorphic to',
          'Respect the source underline boundary, already followed by English clause (ii).','all')
    row('ED-G52-notée','7II:265',r'cohomologie à supports propres, notée H_c versus notées H_c',
        'Revert notées to the printed notée while retaining the separate mathematical correction to tilde Delta.',
        'H_c names the cohomologie, not the suites exactes. The source note explicitly identifies the '
        'pluralization as an erroneous part of correction SGA7II-FR-XVIII-011. The target remains '
        'notées in current, so a precise reversion is required.',forms_fr,
        'conventions/GLOBAL_ISSUES_SGA.md:52; fr/sga7ii/corrections.md:SGA7II-FR-XVIII-011')
    patch('ED-G52-notée','FR','7II','expose_XVIII_body.tex',265,
          r'« cohomologie à supports propres », notées $H^{\cdot}_{c}$',
          r'« cohomologie à supports propres », notée $H^{\cdot}_{c}$',
          'The notation H_c denotes cohomologie, a feminine singular noun.')

    def grow(n,suffix,page,printed,alternative,decision,reason,status='decided',note=False):
        ident='ED-G'+str(n).zfill(2)+(('-'+suffix) if suffix else '')
        row(ident,page,'Source-layer reading: '+printed+' | Proposed/other reading: '+alternative,
            decision,reason,forms_all,'conventions/GLOBAL_ISSUES_SGA.md:'+str(n),status)
        if note:
            notes.append(dict(id=ident,page=page,printed=printed,alternative=alternative,
                              decision=decision,reason=reason,status=status,
                              source='conventions/GLOBAL_ISSUES_SGA.md:'+str(n)))
    grow(4,'','7II:14',r'n=\#[s^*,t]',r'n=\#]s^*,t]',
         'Accept the current half-open interval; restore the omitted parenthesis in English under ED-en7II-C508.',
         'For t=s^* the order is zero, whereas the closed interval has one vertex. In general distance counts '
         'edges, so exclusion of the root gives exactly n. The proposed correction is determined by the '
         'definition and Proposition 2.3, without any glyph inference.')
    grow(18,'nearby-cycles','7II:100',r'R\Psi_\eta(K_s)',r'R\Psi_\eta(K_\eta); earlier corrected K_\eta alone',
         r'Accept the supplied current R\Psi_\eta(K_\eta).',
         'The triangle is on the special-fibre/nearby-cycle topos. The generic-fibre object must first pass '
         'through the nearby-cycle functor. The current page now contains that functor, so the earlier '
         r'defective K_\eta-only correction has already been repaired.')
    grow(19,'localization','7I:92',r'3.13(a)',r'3.13(c)',
         'Accept 3.13(c) in the corrected forms.',
         'The sentence constructs quasi-coherent sheaves by localization. Corollary 3.13(c) is the '
         'localization statement; 3.13(a) is the smoothness criterion. The referent is fixed by the text.')
    grow(19,'vanishing','7I:93',r'3.12(10)',r'3.13(b)',
         'Accept the current reference to complete-intersection vanishing, 3.13(b).',
         'Theorem 3.12 has only eight items. Corollary 3.13(b) states the required vanishing in degrees '
         'at least two for a relative complete intersection; the missing item 10 cannot be retained as '
         'a usable corrected reference.')
    grow(19,'conormal','7I:93',r'3.12(7)',r'3.12(8)',
         'Accept 3.12(8) in the corrected forms.',
         'Item 3.12(8) identifies degree-one cotangent cohomology with the conormal Hom quotient. '
         'Item 3.12(7) states finite generation and cannot justify the displayed Hom identification.')
    grow(19,'finiteness','7I:93',r'3.12(6) and (8)',r'current: 3.12(7) and smooth vanishing, cf.3.13(a); provisional issue: 3.12(6) and (7)',
         'Accept the more precise supplied-current references; reject the provisional 6-and-7 suggestion.',
         'Finite generation is 3.12(7). Support on the nonsmooth locus uses smooth vanishing '
         '(3.12(5), with the smoothness criterion in 3.13(a)); tensor compatibility in 3.12(6) alone '
         'does not supply that vanishing. The actual numbered statements settle the earlier low-confidence suggestion.')
    grow(25,'','7II:136–137',r'choix de t et s; B_{s,t}',r'choix de t et d; B_{t,d}',
         'Accept both supplied-current corrections together.',
         'Section 3.1.3 chooses d and t, defines B_{t,d}, and constructs (V,T) from them. The letter s '
         'is not one of these parameters, while the ensuing proof of 3.1.5 repeatedly uses B_{t_0,d_0}. '
         'Both replacements are fixed by the local definitions, not merely a preference of notation.')
    grow(27,'x-hat','7I:123',r'\mathfrak X_{(\hat x)} in the supplied source layers',r'earlier transcription \mathcal X_{(\mathfrak x)}',
         'Keep the supplied source-layer hat reading; do not invent a further glyph correction.',
         'The two current source pages both use the completion hat and the same completion-to-localization '
         'isomorphism. The earlier convention entry questioned the physical overstrike; without the scan '
         'that paleographic question cannot be independently resolved. The authoritative attached layers '
         'remain the printed-reading witness.',status='needs the scan',note=True)
    grow(27,'missing-reference','7I:128','is smooth by and therefore','is smooth by 4.13(a) and therefore',
         'Retain the printed blank reference in every body; record the suggested reference only as a note.',
         'The statement lacks a number in the recorded print. More than one preceding smoothness result '
         'could support the argument, and adding 4.13(a) would manufacture a citation. No supplied '
         'source establishes the omitted numeral.',status='retained; authorial reference unresolved',note=True)
    grow(28,'','7II:157',r'four occurrences muq',r'mqu',
         'Accept all four mqu corrections already in current.',
         'Corollary 4.11 defines K^{mqu} for finite quasi-unipotent determination. The same summand '
         'occurs in the third table row, the definition of Psi, and both members of 4.12(iii). '
         'The explicit definitions identify one notation, so the transposition is not a new standardization.')
    grow(31,'','7II:168,175',r'tags (4.2.1), (4.14.2)',r'tags (1.2.1.1), (1.3.2.1)',
         'Retain the coordinated local renumbering of the supplied current layer.',
         'The displays occur inside Definition 1.2.1 and Corollary 1.3.2, not any section 4. '
         'The corrected tags use the source’s established nested numbering and distinguish the two '
         'unrelated displays. Diplomatic keeps both old tags; the apparatus records both changes.')
    grow(32,'run-in-headings','7I:163,165 (and analogous numbered headings)',
         'Attached layers use separate paragraphs after numbered headings',
         'possible printed run-in headings with following prose on the same paragraph',
         'Keep the supplied paragraph boundaries; do not make an unchecked global reflow.',
         'The two specific changes were held at low confidence and the other headings were not '
         'verified. A text-only layer cannot establish a printed indentation or run-in break. '
         'This is a layout uncertainty, not grounds for altering any authorial wording.',
         status='needs the scan',note=True)
    grow(33,'agreement','7I:159',r'défini (twice)',r'définie (twice)',
         'Accept both feminine forms already present in current.',
         'Both participles describe the explicitly feminine structure d’extension. The relative '
         'positions and paired constructions make the grammatical referent unambiguous. English '
         'defined does not carry a corresponding gender variant.')
    grow(33,'diaeresis','7I:145,155,160',r'coîncident',r'coïncident',
         'Retain the edition’s established diaeresis convention and avoid a new glyph pass.',
         'NOTE_7I and global issue 78 expressly treat the typewriter circumflex as a substitute for '
         'diaeresis rather than an independent lexical reading. That convention is a source policy, '
         'not a new normalization decision by this build.')
    grow(36,'multiplicative-group','7I:177',r'G étant le groupe multiplicatif sur \underline G_m',
         r'G=\underline G_{m,S} étant le groupe multiplicatif sur S',
         'Accept the supplied-current clarification of the group over the stated base S.',
         'The paragraph concerns abelian schemes P_i on S and extensions by the multiplicative '
         'group. The current reading names that group and restores its base, while the literal '
         'printed sur G_m misidentifies the base. Keep the printed wording diplomatically and '
         'identify the entire correction in the apparatus, without treating it as a recovered glyph.')
    grow(36,'E-or-X','7I:180',r'd_1^*d_0^*(E)\simeq(d_0d_1)^*(E)',r'd_1^*d_0^*(X)\simeq(d_0d_1)^*(X)',
         'Retain E in all bodies; record the proposed X reading without adopting it.',
         'The preceding concrete extension is called X, but the transitivity isomorphism is valid '
         'for any extension E. Consequently the typography does not force a mathematical error. '
         'Both supplied layers retain E, and an authorial generic E remains possible.',
         status='retained; no determinate emendation',note=True)
    grow(36,'psi-footnote','7I:180',r'\psi_{L.}(A)',r'\underline\Psi_{L.}(A)',
         'Retain the source-layer lowercase psi in the body.',
         'The footnote names a category also denoted by underlined capital Psi in the main text, '
         'but the recorded low-confidence observation does not establish whether the glyph is a '
         'typist variant or an accidental change. No scan is supplied to adjudicate its shape.',
         status='needs the scan',note=True)
    grow(37,'duplicate-number','7I:183',r'two displays tagged (3.2.3)',r'second display (3.2.3\prime) or another new tag',
         'Retain both printed (3.2.3) tags; distinguish their locations by description in the records.',
         'The following source already uses (3.2.4); no unoccupied intended number is established. '
         'An editorial prime would be a new citation system, not recovery of the author’s number. '
         'The diagram and c(X,alpha) display remain distinguishable by their content.',
         status='retained; intended numbering unresolved',note=True)
    grow(37,'other-loci','7I:181–185',r'Psi_L(A); munie; peut-être; nous bornerons',
         r'Psi_{L.}(A); context-dependent agreement; peut être; nous nous bornerons',
         'Retain the supplied corrected-layer decisions; do not impose a blind grammar replacement.',
         'The missing complex dot in (3.1.6) is already restored in current. The printed munie '
         'on p.182 grammatically modifies l’extension triviale and must remain feminine there. '
         'Each other recorded correction is retained at its own source-linked locus; a global '
         'replacement would conflate unlike grammatical contexts.')
    grow(38,'speck','7II:202',r'(\mathrm{Sw}_{I\prime},s_{I/H}) without an extra lower dot',
         'a possible printed dot below the opening parenthesis',
         'Keep the supplied formula without an additional dot.',
         'No mathematical operation is defined by the possible mark. Its status as ink, damage '
         'or punctuation is a visual-source question; neither attached layer encodes it.',
         status='needs the scan',note=True)
    grow(38,'family','7II:202',r'supposer que X_s est le sous-schéma',r'supposer que X est le sous-schéma',
         'Accept current X.',
         'The ambient affine space is over S and the displayed equation includes the deformation '
         'parameter a in the maximal ideal. It defines the family X; its special fibre would '
         'set that parameter to zero. The local model determines the correction.')
    grow(41,'exton-sion','7I:195','extension (both attached layers)','exton-sion (held low-confidence visual reading)',
         'Retain the attached diplomatic reading extension, and list the alternative only in the note.',
         'The two source layers agree. The earlier candidate was explicitly held and supplies '
         'no established printed lexical error. The scan is needed to distinguish an actual o '
         'from a damaged e and a line-end hyphen.',status='needs the scan',note=True)
    grow(42,'projective-space','7II:215',r'P^r in 2.1 and \mathbf P^r in 2.2',r'\mathbb P^r in both places',
         'Preserve the supplied layer-specific typefaces; make no new global replacement.',
         'Both symbols are explicitly defined as projective space and no mathematical reading '
         'changes. The low-confidence proposal concerns typewriter shapes, which issue 78 '
         'distinguishes from textual misprints. The build is not authorized to standardize '
         'notation merely for visual uniformity.')
    grow(45,'mathematical-repair','7II:237',r'the printed pencil in (4.2.3)',
         'a proposed replacement pencil with an isolated ordinary quadratic singularity',
         'Preserve the supplied mathematical formula; do not construct a new proof or pencil.',
         'The global record explicitly calls the proposed replacement a repair of the mathematics '
         'rather than a recovered reading. The detailed proposed formula is not supplied in the '
         'attached findings file. The recorded concern (a singular plane for n=2k+1 at least 7) '
         'is disclosed, but no conjectural replacement is inserted.',
         status='retained; proposed mathematical replacement unavailable',note=True)
    grow(47,'duplicate-number','7II:244',r'two (5.2.6) labels',r'(5.2.6) followed by (5.2.6\prime)',
         'Accept the current editorial prime on the second display, retaining the first and all later tags.',
         'Unlike issue 37, this specific disambiguation is already adopted in the supplied '
         'corrected layer and does not change (5.2.7), (5.2.8), or their citations. It is '
         'recorded explicitly as an editorial label, not claimed as the printed reading.')
    grow(48,'inner-underlines','7II:248 and other internal commas',
         'source-layer continuous underlines through some inner commas',
         'stop and restart each underline around the comma',
         'Keep the source-layer markup pending visual evidence at each occurrence.',
         'The global record states that the typist sometimes underlined through commas and '
         'sometimes did not. Therefore a string-wide rule is not justified; each of the '
         'potential cases requires its scan. No authorial wording is changed.',
         status='needs the scan',note=True)
    grow(48,'equation-tag','7II:246',r'\tag*{5.3.7.}',r'\tag{5.3.7}',
         'Retain the printed unparenthesized 5.3.7. in all forms.',
         'The tag is a valid, unambiguous reference as printed. Adding parentheses would be '
         'notation standardization with no correction of mathematical content. Both supplied '
         'layers already agree on tag-star.')
    grow(52,'classification','7II:263,265',r'corrections XVIII-008 and XVIII-011 classified as transcription repairs',
         'misprints in the printed source, except erroneous notée-to-notées change',
         'Classify the mathematical differences as printed misprints; apply ED-G52-notée to undo the pluralization.',
         'The later convention record explicitly reports scan confirmation that pat and the '
         'missing Delta tilde belong to the print. It supersedes the earlier correction-ledger '
         'classification. The authorial singular cohomologie governs notée independently.')
    grow(58,'comma','7II:332',r'H_s,',r'H_{s,}',
         'Keep the comma as argument punctuation; do not move it into the subscript.',
         'The lower comma was a held visual observation, not a new index. The H_s followed by '
         'coefficient argument consistently denotes the fibre. Both layers retain ordinary '
         'argument punctuation; a physical baseline question requires the scan.',
         status='needs the scan',note=True)
    grow(59,'checked-readings','7I:338',r'(A_K ; A\prime_K) and \varphi_w',
         'earlier questioned readings of the subscripts or variable',
         'Retain the supplied readings; the low-confidence query was resolved by the recorded scan check.',
         'The final clause of global issue 59 explicitly states that both readings were checked '
         'on the scan and are as printed. It is positive closure evidence, so no new uncertainty '
         'or unrecorded normalization is introduced.',status='already resolved')
    grow(61,'glyphs','7II:362,384,389',r'plain Q or Fraktur-looking G in the typescript',
         r'\mathbb Q_\ell and \operatorname{Gal}',
         'Follow the later issue-78 disposition; do not introduce new glyph variants.',
         'Issue 78 expressly resolves the held question: typist glyph differences without a '
         'changed reading are not reproduced as independent diplomatic textual variants. '
         'The name Gal is an operator and Q_ell the same coefficient field; the user’s rule '
         'against silent notation changes precludes an additional unsourced pass.',status='superseded by issue 78')
    grow(63,'capital-accents','7II:403,409,412,415',
         'unaccented capitals of the typescript',
         'accented Évidemment, Écrivant, Écrivons in the supplied layers',
         'Keep the documented accented-capital convention.',
         'The convention record explicitly reverted four deaccenting edits and treats the '
         'unaccented capitals as a typewriter limitation. This is an already-decided glyph '
         'convention, not a fresh correction or a different French lexical reading.',status='already resolved')
    grow(63,'miracle','7II:416','oh miracle (both attached layers)','ô miracle (earlier held reading)',
         'Retain oh miracle as the attached diplomatic reading.',
         'The later supplied layers agree on oh. The earlier low-confidence record does not '
         'establish the visual reading independently; changing both layers back to ô would '
         'discard the current witness without evidence.',status='needs the scan',note=True)
    grow(63,'plain-Q','7II:416,418','plain Q glyph','double-struck Q',
         'Use the issue-78 interpretation of typist glyphs; preserve existing source-layer distinctions.',
         'The held observation is the same case as issue 61. No new coefficient field is '
         'introduced by the shape. Existing registered layer differences remain attributed '
         'to their records, but this build makes no additional global typeface change.',status='superseded by issue 78')
    grow(64,'psi-k','7II:421',r'\psi\circ G',r'\psi_k\circ G',
         'Retain the printed bare psi diplomatically and the supplied-current subscript k correction.',
         'The operator is explicitly defined as psi_k immediately before the stability sentence '
         'and in (4.5.11). Thus the intended indexed operator is textually identified, even '
         'though only a scan could determine whether the physical missing k was a print or '
         'scan defect. No unrelated psi is changed.')
    grow(64,'inclusion','7II:423',r'\bigoplus_{A\subseteq B}L^A',r'\bigoplus_{A\supset B}L^A',
         'Accept the supplied-current reversed inclusion.',
         'Formula (4.5.20) identifies the subspace by divisibility by the product over i in B, '
         'which requires supports containing B. The following quotient by strict supersets '
         'and definition of L^B confirm that containment direction. This is not an inference '
         'from a faint glyph alone.')
    grow(64,'quotient','7II:423','the displayed fraction in (4.5.21)','a slash presentation of the same quotient',
         'Keep the displayed fraction in both layers.',
         'Both attached layers encode the same numerator and denominator as a quotient. '
         'The proposed slash concerns the original graphic layout alone. No mathematical '
         'change follows, and without a scan the alternative typography cannot be established.',
         status='needs the scan',note=True)
    grow(64,'subset-stroke','7II:424',r'\subseteq in the supplied source',r'\subset without the lower stroke',
         'Keep the attached diplomatic subseteq reading.',
         'The issue reports a possible overstrike, not a verified symbol. Historical subset '
         'notation may also be non-strict, so semantics do not settle the physical stroke. '
         'No inequality is silently modernized.',status='needs the scan',note=True)
    grow(64,'Delta-Lambda','7II:424–429',r'\Delta_B throughout the defining discussion; \Lambda_B in printed (5.0.12)',
         r'change all seven \Delta_B to \Lambda_B, or retain current \Delta_B at (5.0.12)',
         'Keep the supplied diplomatic glyphs and the local current Delta correction; reject an unchecked all-seven replacement.',
         'The attached layers define Delta_B in (4.5.28) and use it in the intervening argument. '
         'Current (5.0.12) refers back to that same characteristic series. The earlier global '
         'all-seven proposal requires scans of all occurrences and cannot override the '
         'later source-layer distinction. The physical glyph family remains a scan question.',
         status='needs the scan',note=True)
    grow(65,'references','7I:397',r'two references 5.12 a)',r'5.13 b) or 5.14 a)',
         'Accept 5.13 b) in both occurrences, as already in current.',
         'Proposition 5.13(b) treats essentially good reduction, including ell=p in '
         'characteristic zero, exactly the case mentioned before 6.3.3. Proposition '
         '5.14(a) expressly assumes ell not equal to p and cannot supply the ell=p reduction '
         'in that sentence. This resolves the previously low-confidence alternatives by scope.')
    grow(67,'Dwork-psi','7II:436–438',r'\psi_q in the attached layers',r'\Psi_q suggested by the typewriter capital-form glyph',
         'Retain psi consistently with the attached source notation; do not recase the operator.',
         'Issue 78 excludes glyph-only substitutions from textual diplomatic variants. '
         'The operator is the same Dwork operator defined earlier in Exposé XXII; its '
         'cap-height typescript form does not introduce a second operator. No scan-backed '
         'case distinction is available.',status='needs the scan',note=True)
    grow(73,'statement-underlines','7II:403,405 and similar statements',
         'source underlines sometimes include mathematical symbols and final punctuation',
         'split each underline around symbols and punctuation according to the print',
         'Retain the supplied markup except for exact separately documented repairs, including ED-XV-1.3.2-i.',
         'The global record defers these cases to the individual visual review required '
         'by issue 48; the typist did not follow one mechanically inferable rule. A broad '
         'replacement would silently modify authorial presentation at unverified loci.',
         status='needs the scan',note=True)
    grow(77,'review-status','7I:276–350; 7II:291–395','earlier 34 API-only recheck batches outstanding',
         'issue 79: all 34 rechecked in-app and applied',
         'Treat that recheck queue as closed by issue 79; preserve actual source/fix counts.',
         'The later dated convention record explicitly closes all 34 batches. The task '
         'checks their supplied outcomes by diff and fix-log audit; it does not claim '
         'a new scan inspection in this build.',status='superseded by issue 79')
    # Keep a machine-readable selection audit so no explicitly low-confidence
    # SGA-7 convention disappears behind a grouped prose note.
    convention_text=(S/'conventions/GLOBAL_ISSUES_SGA.md').read_text()
    selected=[]
    for m in re.finditer(r'(?ms)^(\d+)\. (.*?)(?=^\d+\. |\Z)',convention_text):
        number=int(m[1])
        if number<=79 and number not in (75,76) and re.search(r'\blow\b|\breview\b|revert that part',m[2],re.I):
            selected.append(number)
    explicit_covered={int(re.match(r'ED-G(\d+)',r['item'])[1]) for r in rows if re.match(r'ED-G(\d+)',r['item'])}
    assert set(selected)<=explicit_covered,(selected,explicit_covered)
    (R/'GLOBAL_ISSUES_SELECTION_AUDIT.json').write_text(json.dumps(dict(
        scope='GLOBAL_ISSUES_SGA.md items 1–79; 75–76 concern other volumes',
        lexical_selection=selected,covered=sorted(explicit_covered),
        unresolved_note_ids=[n['id'] for n in notes],
        rule='Retained readings with no diplomatic/corrected difference appear in the separate editorial-notes section, never in variant counts.'
    ),ensure_ascii=False,indent=2)+'\n')
    with (R/'OPEN_ITEMS_DECIDED.tsv').open('w',newline='') as f:
        wr=csv.DictWriter(f,fieldnames=['item','page','readings','decision','reason','forms_affected','source','status'],delimiter='\t')
        wr.writeheader();wr.writerows(rows)
    result=dict(schema_version=1,decisions=rows,patches=patches,english_variants=variants,unresolved_notes=notes)
    (R/'editorial_decisions.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    unresolved_fragments(notes)
    print('Editorial decisions:',len(rows),'exact patches:',len(patches),'explicit English variants:',len(variants))


def unresolved_fragments(notes):
    french={
        'ED-G27-x-hat':'Conserver le chapeau des deux couches fournies. Le commentaire antérieur hésitait sur la forme physique du caractère surfrappé ; seul le scan permettrait de vérifier cette question paléographique.',
        'ED-G27-missing-reference':'Conserver la référence laissée vide dans le texte imprimé. Plusieurs résultats de lissité peuvent intervenir ; aucun témoin fourni ne donne le numéro manquant. La proposition 4.13(a) reste une suggestion éditoriale.',
        'ED-G32-run-in-headings':'Conserver les alinéas des couches fournies. Les corrections de mise en ligne ont été retenues à faible confiance et les autres occurrences n’ont pas été vérifiées. Le scan est nécessaire pour établir les retraits et les titres courants.',
        'ED-G36-E-or-X':'Conserver E. L’extension considérée juste avant est X, mais l’isomorphisme de transitivité est valable pour une extension quelconque E ; une notation générique de l’auteur reste possible.',
        'ED-G36-psi-footnote':'Conserver le psi minuscule de la couche diplomatique. Le texte principal emploie un Psi majuscule souligné, mais le dossier ne permet pas de distinguer une variante de glyphe d’une coquille. Le scan est nécessaire.',
        'ED-G37-duplicate-number':'Conserver les deux numéros (3.2.3). Le numéro (3.2.4) est déjà employé ensuite ; aucun numéro voulu par l’auteur ne peut être rétabli avec certitude. Le diagramme et le morphisme c(X,alpha) sont distingués par leur contenu.',
        'ED-G38-speck':'Ne pas ajouter de point sous la parenthèse. Aucune opération mathématique n’est définie par cette marque possible ; seul le scan peut distinguer ponctuation, encre et défaut matériel.',
        'ED-G41-exton-sion':'Conserver extension, lecture commune des deux couches fournies. La lecture exton-sion a été retenue à faible confiance ; le scan permettrait de distinguer un o d’un e endommagé et de vérifier le trait de coupure de fin de ligne.',
        'ED-G45-mathematical-repair':'Conserver le pinceau fourni dans (4.2.3). Le registre signale, pour n=2k+1 au moins 7, un plan singulier au lieu d’un point double ordinaire ; il distingue explicitement une réparation mathématique d’une lecture récupérée. La formule de remplacement détaillée n’est pas jointe et ne peut être inventée.',
        'ED-G48-inner-underlines':'Conserver le soulignement fourni à chaque occurrence. Le registre précise que le dactylographe passait parfois sous les virgules et parfois non ; aucune substitution globale n’est justifiée sans le scan de chaque lieu.',
        'ED-G58-comma':'Conserver la virgule comme séparation des arguments, après H_s. La position basse observée à faible confiance ne définit pas un nouvel indice. Le scan est nécessaire pour examiner la ligne de base physique.',
        'ED-G63-miracle':'Conserver oh miracle, lecture commune des deux couches fournies. L’observation antérieure ô miracle n’avait pas été établie ; seule la consultation du scan permettrait de trancher indépendamment.',
        'ED-G64-quotient':'Conserver la fraction de (4.5.21). Les deux couches donnent les mêmes numérateur et dénominateur ; la barre oblique proposée concerne uniquement la disposition graphique du quotient. Le scan est nécessaire pour établir cette disposition.',
        'ED-G64-subset-stroke':'Conserver le signe subseteq de la couche fournie. Le trait inférieur peut relever d’une surfrappe ; la convention historique de subset peut aussi être non stricte. Le sens seul ne décide donc pas de la forme physique.',
        'ED-G64-Delta-Lambda':'Conserver les glyphes de la couche diplomatique et la correction locale Delta de la couche courante. Delta_B est défini en (4.5.28) et la formule (5.0.12) renvoie à la même série caractéristique. Le remplacement global des sept occurrences demanderait leurs scans et n’est pas effectué.',
        'ED-G67-Dwork-psi':'Conserver psi pour l’opérateur de Dwork déjà défini dans l’exposé. La hauteur de capitale du glyphe dactylographié ne suffit pas à établir un second opérateur ni une distinction de casse. La convention 78 exclut les simples variantes de forme du texte diplomatique.',
        'ED-G73-statement-underlines':'Conserver le balisage fourni, sauf les réparations précises documentées séparément. Le registre renvoie ces soulignements à la vérification visuelle au cas par cas de la convention 48 ; aucune règle globale ne permet de retrouver le geste du dactylographe.'
    }
    for lang in ('en','fr'):
        chunks=[r'\clearpage',r'\section*{'+('Retained readings and unresolved editorial questions' if lang=='en' else 'Lectures conservées et questions éditoriales non tranchées')+'}']
        intro=('These notes record alternatives that have not been inserted as new corrections. They are separate '
               'from the numbered variant apparatus: a note without a diplomatic/corrected difference adds no '
               'apparatus entry. “Needs the scan” concerns a physical reading that this build cannot verify. '
               'The attached diplomatic layer remains the printed-reading witness.' if lang=='en' else
               'Ces notes présentent des alternatives qui ne sont pas insérées comme corrections nouvelles. '
               'Elles sont distinctes de l’apparat numéroté : une question sans différence entre les formes '
               'diplomatique et corrigée ne crée aucune entrée de variante. « Needs the scan » signifie que '
               'la lecture matérielle exige le scan, absent de cette construction. La couche diplomatique '
               'fournie reste le témoin de la lecture imprimée.')
        chunks.append(tex(intro))
        for n in notes:
            chunks.append(r'\subsection*{'+tex(n['id']+' — '+n['page'])+'}')
            chunks.append(tex(('Retained/source reading: ' if lang=='en' else 'Lecture de la source conservée : ')+n['printed']))
            chunks.append(tex(('Alternative: ' if lang=='en' else 'Alternative : ')+n['alternative']))
            chunks.append(tex((n['decision']+' '+n['reason']) if lang=='en' else french[n['id']]))
            chunks.append(tex(('Status: ' if lang=='en' else 'Statut : ')+n['status']+'. '
                              +('Source: ' if lang=='en' else 'Source : '))
                          +r'\nolinkurl{'+n['source']+'}')
        (W/f'unresolved_{lang}.tex').write_text('\n\n'.join(chunks)+'\n')


def frontmatter_inventory():
    items=[
        ('7I','General introduction','present','printed V–VII','fr/sga7i/diplomatic/general_introduction_body.tex',
         'Source comments identify scan pages 7–9 and printed V–VII; V is inferred from visible VI and VII. Signed P. DELIGNE, Bures sur Yvette, mai 1972.'),
        ('7I','Volume title, publication and volume-level printed contents leaves','not transcribed in supplied French layers',
         'outside the transcribed introduction V–VII; precise missing-leaf contents unverified without scans',
         'fr/sga7i/diplomatic/SGA7I_Fresh_Source_Transcription_Complete_Working.tex',
         'Master inputs the general introduction and then exposé bodies; no separately transcribed volume contents or title/publication leaf. Generated front matter is explicitly editorial.'),
        ('7I','Separate Exposés III–V','not separately written; not a transcription omission','historical exposé numbering',
         'en/repo/SOURCE_AUTHORITY.md','Written Exposé I summarizes the oral early exposés; complete published scope is I, II, VI–IX.'),
        ('7I','Exposé titles and local sommaires','present','within body folios 1–523',
         'fr/sga7i/diplomatic/expose_I_body.tex; fr/sga7i/diplomatic/expose_II_body.tex; fr/sga7i/diplomatic/expose_VI_body.tex; fr/sga7i/diplomatic/expose_VII_body.tex; fr/sga7i/diplomatic/expose_VIII_body.tex; fr/sga7i/diplomatic/expose_IX_body.tex',
         'All six exposé titles and their authors are present; preserve the local sommaires that are transcribed.'),
        ('7I','Publisher catalogue and terminal matter','present','folios 524–528, catalogue 525–528',
         'fr/sga7i/diplomatic/expose_IX_body.tex','These are source content and must not be silently omitted as modern front matter.'),
        ('7II','Printed volume front matter before Exposé X','not transcribed in supplied French layers','before folio 1 / source scan index 8',
         'fr/sga7ii/diplomatic/SGA7II_French_Source_Transcription_Working_X-XXI_Partial_20260731.tex',
         'The source master starts with expose_X_body. No preceding volume title, publication leaves or volume contents are supplied; their detailed contents cannot be reconstructed without the scans.'),
        ('7II','Exposé X title and authorship','present','folio 1',
         'fr/sga7ii/diplomatic/expose_X_body.tex','Full title INTERSECTIONS SUR LES SURFACES REGULIERES and par P. Deligne are present. There is no literal Exposé X line in that source segment; an editorial TOC label must not be represented as transcribed wording.'),
        ('7II','Exposé XIII title, authorship and local contents','present in the preceding component','folio 82 / source scan index 89',
         'fr/sga7ii/diplomatic/expose_XII_body.tex',
         'The tail of expose_XII_body contains Exposé XIII, Le formalisme des cycles évanescents, par P. Deligne, and its local contents. Exposé XIII starts at folio 82 even though expose_XIII_body begins with Introduction at folio 83.'),
        ('7II','Other exposé titles and authorship','present','Exposés XI–XII, XIV–XXII',
         'fr/sga7ii/diplomatic/','All headings are present in their respective bodies; no additional missing exposé title material was found in the boundary inventory.'),
    ]
    with (R/'FRONT_MATTER_INVENTORY.tsv').open('w',newline='') as f:
        w=csv.writer(f,delimiter='\t');w.writerow(['volume','item','status','place','source','evidence']);w.writerows(items)


def main():
    R.mkdir(parents=True,exist_ok=True)
    W.mkdir(parents=True,exist_ok=True)
    provenance()
    decisions()
    frontmatter_inventory()
    print('Provenance fragments and source records written.')


if __name__=='__main__':
    main()
