# SGA 4½: the check of every page against the print, and six readers, French and English, each in three forms

You are GPT-6 Astra in ChatGPT Pro mode, with a Python and LaTeX environment. Four ZIP files are attached:

- `SGA4HALF_FR.zip`
- `SGA4HALF_EN.zip`
- `SGA4HALF_SCANS.zip`
- `SGA4HALF_CHECK.zip`

Each has `MANIFEST.tsv` at its root (path in the zip, source, bytes, SHA-256, role). Read the manifests first.

## What this is for

SGA 4½ is P. Deligne, *Cohomologie étale* (Séminaire de Géométrie Algébrique du Bois-Marie SGA 4½, avec la
collaboration de J.-F. Boutot, A. Grothendieck, L. Illusie et J.-L. Verdier; Lecture Notes in Mathematics 569,
Springer, 1977).

**Daniel Miller's LaTeX rendition.** The book exists in LaTeX thanks to Daniel Miller. His typesetter's note calls
it "an essentially unmodified version of the original". His repository, github.com/dkmiller/sga4.5, is no longer
online. A copy survives at github.com/NomiL/sga4.5, commit d5266b27; our sga-fr publishes it unchanged.

**Earlier work on it:**
- In August 2026, Codex repaired the rendition against the scan in two trees, a diplomatic one and a corrected one,
  up to printed p. 65. It restored the essay *Un fil d'Ariane pour SGA 4, SGA 4½ et SGA 5* and the opening pages of
  Arcata, which Miller's text lacks.
- On 12 November 2026 every page of Miller's text was checked against the scan by GPT-6.1 Sol (reasoning effort max)
  over the API. The second half of that check, by a second model, was not run.
- Our English translation is sga-en's SGA4HALF, AI-translated from Miller's French.

**What you do:**
1. Do the second check of every page against the print.
2. Decide every finding of the Sol check.
3. Build the readers: finished books, one per form and language, that carry every fix and say exactly what was changed.

Work by script and diff. Look at the scan and the text wherever a decision needs them.

## The check against the print

**Pages.** Check every printed page that carries text against the scan, word by word and symbol by symbol, page by
page. That is:
- pp. III–IV (Introduction);
- pp. 1–312, including the pages Miller's text lacks: *Un fil d'Ariane* pp. 1–3, Arcata pp. 4–5, the printed
  summaries and tables of contents, and the bibliographies of the parts.

**Images.** `SGA4HALF_SCANS.zip` holds `scan/Number32.pdf` (300 dpi) and `scan/PAGE_INDEX.tsv`, which maps each
printed page to its PDF page:
- PDF page = printed page + 5 up to p. 109;
- PDF page = printed page + 39 from p. 110 on;
- the scan holds the Rapport twice, and its first copy is used.

It also holds the four strips of each page the Sol check saw (`strips/t1/pFFF_s1..4.png`, `strips/tfm/` for the
Introduction). For a stroke the strips do not show clearly, render the PDF page at higher resolution and crop it.

**What is Miller's form and what is an error** is set out in `check/NOTE_45.txt` (`SGA4HALF_CHECK.zip`). Follow it.

*Not errors (Miller's form):*
- layout, displays, `xymatrix` diagrams;
- numbering through `\label` names and `\tag`;
- emphasis and modern typography;
- his macros for the same sign;
- his stated conventions: script letters for sheaves, and `\Hom`/`\hom`, `\rHom`/`\rhom` for sheaf and ordinary
  functors.

*Errors (differences of content):*
- words and numbers;
- formulas, indices and exponents;
- symbols and letters;
- punctuation that changes the meaning;
- missing or extra text;
- wrong references;
- a convention of his that contradicts a distinction the print makes.

**The Sol findings.** `check/SOL_FINDINGS.tsv` holds every finding of the Sol check, 1,247 rows, each with an id
`S45-SOL-NNNN`. The rows give:
- the page and its PDF page;
- the TeX file and lines the model saw;
- the kind, the readings and the proposed fix (`fix_old` is a substring of that page's TeX in
  `check/batches/<batch>/page_FFF.tex`);
- the status: Sol only, not applied.

The 1,247 findings are:

| Kind | Count |
|---|---|
| word | 409 |
| misprint of the print | 273 |
| symbol | 159 |
| missing | 143 |
| formula | 129 |
| number | 44 |
| accent | 33 |
| extra | 24 |
| punctuation | 15 |
| font | 10 |
| other | 4 |
| page cut | 4 (pp. 105, 106, 262, 301) |

The longest proposed insertions say that Miller's text leaves out whole passages, among them:
- the Arcata foreword on p. 4;
- a paragraph with formula (4.14.2) on p. 203;
- Verdier's subtitle and historical note on p. 262;
- the adjunction identity on p. 155;
- the comparison-theorem paragraph on p. 41;
- §4.4 of Fonctions L on p. 126;
- the item b) on p. 19.

**Decide every row from the scan:** accept the fix as it stands, accept it with a corrected reading, or reject it, and
give each verdict a reason. Your own check finds what the Sol check missed. Record each of your findings the same way.

**Where the print itself is damaged** (a broken or faint stroke, an ink blot), decide the reading from the
neighbouring text and the mathematics, and say so in the reason.

**The page cut.** It was made automatically (`check/PAGES.json`, `check/README.md`), so a page's TeX can hold lines of
the next page. Settle every page break against the scan; the four cut reports are among the rows.

**Codex's records.** `fr/codex_records/dec.csv` holds 475 decisions; `qa.csv` and `STATUS.md` hold the visual checks
up to physical p. 70 (printed p. 65). Where a Sol finding falls on pp. 1–65, compare it with Codex's tree and
decision. Where they disagree, the scan decides.

## The six readers

Build one book per form and language. Each is a single LaTeX file that compiles with a standard TeX Live (the edition
uses `book` and its `sga-style.sty`):

| File | Language | Form |
|---|---|---|
| `SGA4HALF_FR_diplomatique.tex` | French | **Diplomatic**: the text as printed, misprints kept, in Miller's form, with the page of the print marked at every page break |
| `SGA4HALF_FR_corrige_apparat.tex` | French | **Corrected, with apparatus**: misprints corrected. Every place where it differs from the print is marked; the apparatus gives the printed reading, the correction and its source |
| `SGA4HALF_FR_texte_de_lecture.tex` | French | **Plain reading text**: the corrected text with no apparatus and no editors' notes; the printed page numbers in the margin only; a short preface says what was left out |
| `SGA4HALF_EN_diplomatic.tex` | English | **Diplomatic**: the English that follows the print. Where a misprint changes the English, its printed reading is kept. The print's page breaks are marked |
| `SGA4HALF_EN_corrected_apparatus.tex` | English | **Corrected, with apparatus**: as for the French |
| `SGA4HALF_EN_reading.tex` | English | **Plain reading text**: as for the French |

**Build all three forms of a language from one annotated master.** Mark every place where the print and the
corrected text differ, for instance with a macro `\var{printed reading}{corrected reading}{source id}`. Generate the
three forms from that master by switching the macro, so the forms cannot drift apart. A misprint that does not change
the English (a French spelling, for example) gets no variant in the English.

## Sources of record

**French** (`SGA4HALF_FR.zip`):
- **Base for pp. 1–65:** `fr/codex_dip/` (diplomatic) and `fr/codex_corr/` (corrected). These are Codex's two trees:
  - Miller's rendition repaired against the scan through printed p. 65;
  - the restored *Un fil d'Ariane* (`ariane.tex`);
  - Arcata pp. 4–5 (`opening.tex`, `toc-i.tex`);
  - the decisions of `fr/codex_records/dec.csv`.
- **Base for the rest:** Codex's trees also repair the Introduction, and change the main file, `sga-style.sty` and
  the bibliography file (see `dec.csv`). From p. 66 on, their text equals Miller's, except one `\mbox` in
  `sga4.5-7.tex` of the diplomatic tree.
- **Miller's text:** `fr/miller_src/` is his rendition as sga-fr publishes it. It is the "before" side of the French
  change log, and the text the Sol check saw.
- **The printed text no file has** (the summaries and tables of contents, the bibliographies of the parts, and any
  passage the check finds missing): transcribe it from the scan into the diplomatic and corrected masters.
- **Citations:** keep Miller's `\cite` keys in the running text, and give each part's printed bibliography as printed.

**English** (`SGA4HALF_EN.zip`):
- **Base:** `en/sources/` (sga-en `sources/native/SGA4HALF`; main file `SGA4half_English_Full_Workpass.tex`;
  components `components/sga4half_*_en.tex`).
- **Before side of the change log:** `en/release_v2026-11-12/` holds the English reader as released.
- **Alignment:** the English keeps Miller's `\label` names, so align it with the French by label, section and
  paragraph, and put the print's page breaks in the English at the same places.
- **Fixes:** carry every French fix that changes the English into the English.
- **New translation:** translate the French text the English lacks (*Un fil d'Ariane*, the Arcata foreword and
  contents, Verdier's note, and every restored passage). Mark each such passage in the English change log as
  AI-translated.

**Records** (`SGA4HALF_CHECK.zip`), all under `check/`:
- the README of the check, the page table `PAGES.json` and `PAGES_DIAG.json`;
- the page TeX, the Sol findings per batch (`sol/`) and their messages (`sol/*_coordinator.md`);
- the prompt the Sol check ran on (`PROMPT_OF_BATCH_t1_1_041_045.txt`) and the scripts.

## Rules

1. **Keep the author's notation and language** in every form.
   - Correct a misprint only where it is a misprint of the print, decided by you from the scan with a reason.
   - Never standardize notation silently.
   - Miller's macros and conventions stay, except where one contradicts the print.
2. **The English terms and notation** are those of sga-en's SGA4HALF, kept consistent with the SGA 4 and SGA 7
   readers: their glossaries and notation decisions are in `en/glossaries/`. Write `GLOSSARY_SGA4HALF_FR_EN.tsv`
   (French term or notation, English rendering, count, first place). List every French term rendered in more than
   one way in `GLOSSARY_INCONSISTENCIES.md`. Make the English consistent where the variation is plainly a slip, and
   record each change in the English change log.
3. **Misprints of the print.** Keep a register, `MISPRINTS_45.tsv`, with one row per misprint: page, place, the printed
   reading, the correction, the source (Sol id, your finding id) and the reason. A misprint is:
   - corrected in the corrected and plain forms;
   - kept in the diplomatic form;
   - given an apparatus entry.
4. **Miller's typesetter's note and Codex's editorial choices.**
   - Keep Miller's note, marked as his, in the diplomatic and corrected forms, with its e-mail address left out.
   - Leave the note out of the plain reading text, and say so in its preface.
   - Record Codex's corrections in the apparatus with their `SGA45-…` ids.
5. **Credit and rights.** Each reader's front matter carries:
   - the authors and the volume's bibliographic data;
   - **credit to Daniel Miller for the LaTeX rendition on which every layer rests**: his repository
     github.com/dkmiller/sga4.5, no longer online, and the surviving copy github.com/NomiL/sga4.5, commit d5266b27. His
     typesetting is not attributed to AI;
   - the other credits exactly as `en/repo_records/` (README, ATTRIBUTION, SOURCE_AUTHORITY) give them;
   - the wording "AI-transcribed", "AI-translated" and "AI-produced corrections", never "AI-assisted".
     - Codex's corrections (Aug 2026) and the scan check by GPT-6.1 Sol (12 Nov 2026) are AI-produced corrections.
     - The English is AI-translated.
     - Credit this build to GPT-6 Astra (OpenAI, ChatGPT Pro mode).
   - the rights statement, in the reader's language.
     - English: "The rights in the original work belong to its author or the author's representatives or heirs.
       Where we hold rights, in the AI-produced transcription, translation, corrections and typesetting, they are
       dedicated to the public domain under CC0 1.0. This edition is published for educational, non-profit purposes,
       and we claim no rights we do not hold. If you hold rights in this work and object to its publication here,
       please open a GitHub issue and we will take it down."
     - French: « Les droits sur l'œuvre originale appartiennent à son auteur, à ses représentants ou à ses ayants
       droit. Dans la mesure où nous détenons des droits sur la transcription, la traduction, les corrections et la
       composition produites par l'IA, nous les consacrons au domaine public sous CC0 1.0. Cette édition est publiée
       à des fins éducatives et non lucratives, et nous ne revendiquons aucun droit que nous ne détenons pas. Si vous
       détenez des droits sur cette œuvre et vous opposez à sa publication ici, veuillez ouvrir une issue GitHub et
       nous la retirerons. »
6. **Privacy.** Some records contain local file paths. Never copy a local path into a reader or a log; refer to files
   by their path inside the ZIP. Copy no e-mail address.

## What to deliver

Deliver three ZIPs: `SGA4HALF_READERS_FR.zip`, `SGA4HALF_READERS_EN.zip` and `SGA4HALF_READERS_RECORDS.zip`.
Together they hold:

- **Readers:** the six reader `.tex` files and the two annotated masters, with their PDFs. Leave a PDF out only if a
  ZIP would exceed about 100 MB, and say so.
- **`PAGES_CHECKED.tsv`:** one row per printed page (III–IV, 1–312). Columns: the PDF page, checked against the
  scan, the number of findings, and where the page begins in each master.
- **`SOL_FINDINGS_DECIDED.tsv`:** one row per `S45-SOL` id. Columns: your verdict (accepted, accepted with a
  corrected reading, rejected), the print's reading, the image and region you read it from, the change made, the
  forms affected, and the reason.
- **`CHECK_FINDINGS.tsv`:** every finding of your own check. Columns: id, page, place, the print's reading, the TeX's
  reading, the change, kind, and reason.
- **`MISPRINTS_45.tsv`.**
- **`CHANGES_FR.tsv`:** every difference between the corrected French reader and Miller's text, and between it and
  Codex's corrected tree. Columns: page, place, before, after, source (Sol id, your finding id, Codex decision id,
  misprint id).
- **`CHANGES_EN.tsv`:** every difference between the corrected English reader and the released English, the new
  translations included.
- **`DECISIONS.tsv`:** the page breaks you settled, the four cut reports, the conventions of Miller's that contradict
  the print, and the `\mbox` difference in `sga4.5-7.tex`.
- **Glossary:** `GLOSSARY_SGA4HALF_FR_EN.tsv` and `GLOSSARY_INCONSISTENCIES.md`.
- **`APPARATUS_COUNTS.md`:** per part and form, the number of apparatus entries by kind.
- **`README.md`:** what each file is, how each form was made, all the counts, the printed matter not reproduced and
  why (the title and copyright pages), and the compile status of each reader with its LaTeX errors and warnings.
- **Your build scripts,** with their outputs.

## When it is done

**Each item is done when:**
- **A page** has been compared with the scan, and its row in `PAGES_CHECKED.tsv` is filled.
- **A Sol finding** has a verdict read from the scan, and its reason.
- **A reader:**
  - compiles without errors;
  - carries every accepted fix and every finding of your own check, checked by script against your decision tables,
    with the counts reported;
  - has page markers that agree with `PAGES_CHECKED.tsv`.
- **The apparatus** has one entry for each difference between the diplomatic and the corrected forms, and none for
  anything else.

**Not acceptable:**
- a page left unchecked, or a Sol finding without a verdict;
- a verdict not read from the scan;
- a reader that drops, summarizes or paraphrases any part of the text;
- a fix applied in one form and missing from another;
- an apparatus entry without a source;
- Miller's or Codex's work presented as ours, or credited wrongly;
- a silent change of notation;
- a decision without a reason;
- local paths or e-mail addresses in any output.

**The task is finished** only when every page is checked, every Sol finding is decided, and all six readers and every
file listed above are in the three ZIPs. Keep working until then. Do not stop because:
- what remains is long;
- a part of the work looks presentable;
- much has already been done.

## Working method

- Start from the manifests, `PAGE_INDEX.tsv`, `SOL_FINDINGS.tsv` and Codex's `dec.csv`.
- Check the pages in order, part by part, with the strips and the PDF, and write the decision tables as you go.
- Build the annotated masters by script, generate the forms, compile, and check the counts.
- After each finished part and each finished reader, save a checkpoint ZIP of everything so far to the user's
  Library, or wherever files survive the loss of the execution environment. Name it
  `SGA4HALF_READERS_checkpoint_<n>.zip`. Save the final ZIPs there too.
- This task is long by design. Work through it completely; do not stop at an outline, a sample or a plan, and do not
  ask whether to continue. Ignore any clock.
- Write the files from the start and extend them as you go, so that an interruption loses little.

## If the execution environment fails

If the workspace disconnects or an attached ZIP cannot be opened, wait and retry for ten minutes. If it does not come
back, write the work out in the chat as text:
- the decision tables, the misprint register, the glossary, the README and the change logs so far, each in full in
  its own code block headed by its file name;
- your build scripts in full, so that the readers can be rebuilt from the attached sources;
- which pages were checked, which readers were finished, and where their checkpoints are.

Then continue the remaining work in the chat in the same form until every part is written. An answer that only
reports the failure or asks for the files again is not acceptable.

**Checkpoints.** Save a checkpoint ZIP to the Library after every finished Part, each under a new name, `<ID>_checkpoint_<NN>.zip` with `NN` counting up; never overwrite, rename or delete an earlier checkpoint. If the workspace comes back empty, restore it from the newest checkpoint and from this conversation before you continue. The final ZIP holds everything the checkpoints held: a file or passage left out of the final is listed in the report with the reason (superseded by which file, or wrong).
