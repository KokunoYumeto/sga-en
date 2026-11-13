"""Language-specific credit, rights and form notices for the flattened readers."""

RIGHTS_EN = """The rights in the original work belong to its author or the author's representatives or heirs.
Where we hold rights, in the AI-produced transcription, translation, corrections and typesetting, they are
dedicated to the public domain under CC0 1.0. This edition is published for educational, non-profit purposes,
and we claim no rights we do not hold. If you hold rights in this work and object to its publication here,
please open a GitHub issue and we will take it down."""

RIGHTS_FR = """Les droits sur l'œuvre originale appartiennent à son auteur, à ses représentants ou à ses ayants
droit. Dans la mesure où nous détenons des droits sur la transcription, la traduction, les corrections et la
composition produites par l'IA, nous les consacrons au domaine public sous CC0 1.0. Cette édition est publiée
à des fins éducatives et non lucratives, et nous ne revendiquons aucun droit que nous ne détenons pas. Si vous
détenez des droits sur cette œuvre et vous opposez à sa publication ici, veuillez ouvrir une issue GitHub et
nous la retirerons."""

def frontmatter(lang, mode, master=False):
    fr=lang=='fr'
    names={
      'fr':{0:'Texte diplomatique',1:'Texte corrigé avec apparat',2:'Texte de lecture'},
      'en':{0:'Diplomatic text',1:'Corrected text with apparatus',2:'Reading text'}}
    form=r'\ifnum\EditionIsMaster=1\relax '+('Master annoté' if fr else 'Annotated master')+r'\else '+names[lang][mode]+r'\fi'
    heading='Cohomologie étale' if fr else 'Étale cohomology'
    authorcredit=('avec la collaboration de' if fr else 'with the collaboration of')
    text=rf"""
\begin{{titlepage}}
\centering
\vspace*{{2cm}}
{{\Large Séminaire de Géométrie Algébrique du Bois-Marie\par}}
\vspace{{0.7cm}}
{{\Huge\bfseries SGA 4\textonehalf\par}}
\vspace{{0.8cm}}
{{\huge {heading}\par}}
\vspace{{1cm}}
{{\Large Pierre Deligne\par}}
\vspace{{0.5cm}}
{authorcredit}\\[0.3em]
J.-F. Boutot, A. Grothendieck, L. Illusie et J.-L. Verdier
\vfill
{{\Large {form}\par}}
\vspace{{0.7cm}}
Lecture Notes in Mathematics 569, Springer, 1977\\[0.4em]
{'Édition vérifiée sur l’imprimé' if fr else 'Edition checked against the printed volume'}\\
{'13 novembre 2026' if fr else '13 November 2026'}
\end{{titlepage}}
"""
    if fr:
        text+=r"""
\chapter*{Sources, crédits et droits}
Pierre Deligne, \emph{Cohomologie étale}, Séminaire de Géométrie Algébrique
du Bois-Marie SGA 4\textonehalf, avec la collaboration de J.-F. Boutot,
A. Grothendieck, L. Illusie et J.-L. Verdier, Lecture Notes in Mathematics
569, Springer, 1977. Les auteurs et rédacteurs de chaque exposé restent
indiqués à leur place.

\medskip
La composition en \LaTeX\ de Daniel Miller est la base de toutes les couches
de cette édition. Ce travail humain ne doit pas être attribué à l’IA.
Son dépôt \url{https://github.com/dkmiller/sga4.5} n’est plus en ligne.
Une copie subsiste à \url{https://github.com/NomiL/sga4.5}, commit
\texttt{d5266b27}; le projet \texttt{sga-fr} la publie inchangée.
Les crédits de \texttt{sga-en} attribuent également à Daniel Miller cette
composition et sa note de compositeur.

\medskip
L’anglais de \texttt{sga-en} est \emph{AI-translated} à partir de cette
composition française. Les crédits généraux du projet anglais enregistrent
OpenAI Codex (GPT-5.6 Sol : traduction; GPT-6 Astra : corrections et
assemblage, septembre--octobre 2026) et Claude Opus 5.5 (Anthropic : sources
SGA 2 et SGA 3 du 26 octobre 2026 et traduction de SGA 3 revue sur
l’impression de 1970 en novembre 2026). Ces mentions générales ne
réattribuent pas à ces modèles le travail humain de Miller.

\medskip
Les corrections de Codex (août 2026), les propositions du contrôle du scan
par GPT-6.1 Sol (API OpenAI, effort de raisonnement maximal, 12 novembre
2026) et les corrections de la présente édition sont des
\emph{AI-produced corrections}. Les passages français restitués ici à
partir de l’imprimé sont \emph{AI-transcribed}; leurs traductions nouvelles
sont \emph{AI-translated}. La seconde vérification, les décisions, la
restitution, l’alignement bilingue et cet assemblage sont dus à GPT-6 Astra
(OpenAI, ChatGPT Pro mode). Les crédits humains et notices de tiers
applicables restent en vigueur; l’attribution ne vaut ni autorisation ni
approbation.

\medskip
"""+RIGHTS_FR+'\n'
        text+=r"""
\chapter*{Préface à cette forme}
"""
        if mode==0:
            text+=r"""Ce texte suit l’imprimé, y compris ses coquilles, dans la forme
typographique de Miller. Les erreurs de transcription ont été réparées.
Les marques de page donnent la pagination de l’original. La note de Miller
est reproduite sous son nom, sans son adresse électronique.
"""
        elif mode==1:
            text+=r"""Les coquilles vérifiées de l’imprimé sont corrigées. Chaque lieu
ainsi modifié porte un appel à l’apparat, qui donne la lecture imprimée,
la correction et sa source. Les réparations de transcription sont communes
aux trois formes et n’entrent pas dans l’apparat. La note de Miller est
reproduite sous son nom, sans son adresse électronique. Les marques de
page donnent la pagination de l’original.
"""
        else:
            text+=r"""Ce texte donne les lectures corrigées sans apparat ni notes des
éditeurs de la présente édition. La note du compositeur Daniel Miller est
omise de cette forme; les notes des auteurs, les sommaires et les
bibliographies originaux sont conservés. Les numéros de page de l’imprimé
figurent seulement dans la marge.
"""
        text+=r"""
Les pages de titre et de copyright photographiées ne sont pas reproduites;
les données bibliographiques et la présente notice les remplacent. La
table générale originale, non paginée, est conservée. Les détails de la
vérification, les variantes et les différences de sources figurent dans
les fichiers de contrôle livrés avec cette édition.
"""
    else:
        text+=r"""
\chapter*{Sources, credits and rights}
Pierre Deligne, \emph{Cohomologie étale}, Séminaire de Géométrie Algébrique
du Bois-Marie SGA 4\textonehalf, with the collaboration of J.-F. Boutot,
A. Grothendieck, L. Illusie and J.-L. Verdier, Lecture Notes in Mathematics
569, Springer, 1977. The authors and writers of the individual exposés
retain their credits in place.

\medskip
SGA 4\textonehalf\ preserves Daniel Miller’s \LaTeX\ typesetting and its
original typesetter’s note. It is not attributed to AI. His repository
(\url{https://github.com/dkmiller/sga4.5}) is no longer online; the French
text is in \texttt{sga-fr}, and a copy survives at
\url{https://github.com/NomiL/sga4.5}, commit \texttt{d5266b27}.
Every layer of this edition rests on his typesetting.

\medskip
The English text is AI-translated from Miller’s French typesetting.
The English project’s general credits record OpenAI Codex (GPT-5.6 Sol:
translation; GPT-6 Astra: corrections and assembly, September--October
2026) and Claude Opus 5.5 (Anthropic: the SGA 2 and SGA 3 sources of
26 October 2026, and the translation of SGA 3 revised against the 1970
printing in November 2026). These collection-wide credits do not attribute
Miller’s human contribution to AI.

\medskip
Codex’s corrections (August 2026), the scan-check proposals by GPT-6.1 Sol
(OpenAI API, maximum reasoning effort, 12 November 2026), and this edition’s
corrections are AI-produced corrections. Restored French passages are
AI-transcribed, and their new English translations are AI-translated.
The second scan check, adjudication, restoration, bilingual alignment and
this build are by GPT-6 Astra (OpenAI, ChatGPT Pro mode).
Additional English translation is AI-translated; subsequent corrections,
editing, reconstruction and typesetting are AI-produced. The
source-specific human credits and genuine third-party notices remain
applicable; attribution does not establish permission or endorsement.

\medskip
"""+RIGHTS_EN+'\n'
        text+=r"""
\chapter*{Preface to this form}
"""
        if mode==0:
            text+=r"""This English text follows the printed work, retaining misprints
where they change the English reading. Transcription errors have been
repaired. Page markers identify the original pagination. Miller’s
typesetter’s note is reproduced under his name, with its email address
omitted.
"""
        elif mode==1:
            text+=r"""Verified misprints of the printed work are corrected. Every
such change is marked and has an apparatus entry giving the printed
reading, correction and source. Transcription repairs are shared by all
three forms and do not receive apparatus entries. Miller’s typesetter’s
note is reproduced under his name, with its email address omitted.
Page markers identify the original pagination.
"""
        else:
            text+=r"""This form gives the corrected text without an apparatus or notes
by the editors of this edition. Daniel Miller’s typesetter’s note is
omitted; the authors’ notes, original summaries and bibliographies are
retained. Original page numbers appear only in the margin.
"""
        text+=r"""
The photographed title and copyright pages are not reproduced; their
bibliographic information is supplied above with the present rights
notice. The original unnumbered general contents are retained. The
accompanying audit records document the scan check, variants and source
differences.
"""
    text+='\n\\ifnum\\EditionIsMaster=1\\relax\n'+('Ce master contient les deux lectures de chaque variante; son PDF montre la forme corrigée avec apparat.\n' if fr else 'This master contains both readings of every variant; its PDF displays the corrected form with apparatus.\n')+'\\fi\n'
    return text+'\n\\clearpage\n'
