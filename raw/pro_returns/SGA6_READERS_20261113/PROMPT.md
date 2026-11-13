# SGA 6: the second check of every page against the print, every finding decided, and six readers, French and English, each in three forms

You are GPT-6 Astra in ChatGPT Pro mode, with a Python and LaTeX environment. Four ZIP files are attached:

- `SGA6_FR.zip`
- `SGA6_EN.zip`
- `SGA6_SCANS.zip`
- `SGA6_CHECK.zip`

Each has `MANIFEST.tsv` at its root (path in the zip, source, bytes, SHA-256, role). Read the manifests first.

## What this is for

SGA 6 is *Théorie des intersections et théorème de Riemann-Roch* (Séminaire de Géométrie Algébrique du Bois-Marie
1966–67, SGA 6), directed by P. Berthelot, A. Grothendieck and L. Illusie, with D. Ferrand, J.-P. Jouanolou,
O. Jussila, S. Kleiman, M. Raynaud and J.-P. Serre; Lecture Notes in Mathematics 225, Springer, 1971.

**Earlier work on it:**
- In August 2026 Codex built French layers from the print: a mixed tree it later put on hold (`fr/codex/ref_hold/`,
  its own `HOLD.md` says why) and a second tree (`fr/codex/sga6_fr_r1_fr.tex`) that holds an image-checked
  re-transcription of Exposé XIV pp. 672–689 and 234 accepted corrections.
- On 5 November 2026 two layers were made from Codex's corpus: a **diplomatic** layer (the text as printed, misprints
  kept) and a **corrected** layer.
- From 10 to 13 November 2026 every printed page, pp. 1–700, was checked against the scan by Claude Opus 5.5 at effort
  max, five pages at a time (140 batches), with a second scan of the same printing as the witness for thin strokes.
  The checkers' findings were applied to both layers by script; Codex's earlier corrections were reconciled with the
  result.
- Our English translation is sga-en's SGA 6, AI-translated. None of the French fixes of 10–13 November is in it yet.

**What you do:**
1. The second check of every page against the print.
2. Decide every finding: the checkers' fixes, the misprint register, the open items, Codex's corrections that the
   reconciliation rejected, the differences from Codex's tree, and the conventions left for the whole volume.
3. Build the readers: finished books, one per form and language, that carry every fix and say exactly what was
   changed, with every French fix carried into the English.

Work by script and diff. Look at the scan and the text wherever a decision needs them.

## The check against the print

**Pages.** Check every printed page that carries text against the scan, word by word and symbol by symbol, page by
page: pp. 1–700, and the front matter. The text before the folio-1 marker of the layers is the front matter (the
Introduction among it); match it to the scan pages before p. 1 and mark its printed page breaks. Printed matter that
no layer transcribes (title pages, tables of contents, and anything your check finds missing) is transcribed from the
scan into the diplomatic and corrected masters.

**Page markers.** Each printed page begins in both layers with a marker
`%%%%%%%%%%  scan idx N  |  folio F  %%%%%%%%%%`, with N = F + 13. There are 699 markers: **p. 690 has none.** Find where
p. 690 begins on the scan and add its marker in both layers. Settle every marker you find misplaced.

**Images.** `SGA6_SCANS.zip` holds:
- `scan/SGA6_scan_360dpi.pdf`, the scan the check was made against: PDF page = scan idx + 1 = folio + 14;
- `scan/SGA6_witness_300dpi.djvu`, a second scan of the same printing: its page is about folio + 11 (confirm the
  offset on the first page you use);
- `scan/PAGE_INDEX.tsv`, which gives both for every folio.

Render a page at a higher resolution and crop it wherever a stroke is unclear. Where the main scan is faint or broken,
read the witness before deciding.

**What is an error and what is not** is set out in `conventions/NOTE_6.txt` and `conventions/CHECKER_PROMPT_SGA.txt`
(`SGA6_FR.zip`). Follow them.
- *Errors* are differences of content: words and numbers; formulas, indices and exponents; symbols and letters;
  punctuation that changes the meaning; missing or extra text; wrong references; a typographic convention that
  erases a distinction the print makes (an underline, a raised dot, a script letter).
- *Not errors* are layout and the items NOTE_6 lists as handled globally (straight quotes, joint names, typed
  substitutes for symbols, and the others it names).

## The findings to decide

All of them are in `SGA6_FR.zip` (`fixes/`, `conventions/`, `fr/codex/`) and `SGA6_CHECK.zip` (`check/`).

1. **The checkers' findings.** `check/findings/findings_F_L.json`: 140 files, 3,751 findings, each with `page`,
   `where`, `scan` (the print's reading), `tex`, `kind`, `confidence`, `fix` and `note`. By kind: underline 758,
   misprint of the print 724, other 394, punctuation 392, symbol 382, font 342, marker 321, formula 213, word 107,
   extra 88, missing 18, accent 6. `check/pages/` holds the page TeX each batch saw, `check/prompts/` the prompt each
   batch ran on.
2. **The fixes applied.** `fixes/FIXLOG_6.jsonl` (2,776 fixes, diplomatic layer) and `fixes/FIXLOG_6_CURRENT.jsonl`
   (2,737, corrected layer; 222 of kind `misprint_correction`), each with `page`, `old`, `new`, `kind` and `source`.
   Decide every one from the scan: confirmed, amended (give the reading), or reverted.
3. **The misprint register.** `fixes/MISPRINTS_6.json`: 724 places the checkers judged misprints of the print
   (`page`, `where`, `print`, `correct`, `tex_did`, `note`, `source`). Decide each: a misprint, corrected in the
   corrected layer as given or with your correction; or not a misprint, the printed reading kept in both layers.
4. **The open items.** `fixes/REPLAY_MANUAL_6.json`: 20 fixes the script could not place; 4 are resolved, 16 are open
   (pp. 4, 45, 165, 181, 190, 223, 252, 341, 351, 600 twice, 603, 613, 619 twice, 688). Also the 7 findings in
   `fixes/MANUAL_6_findings/`, placed by hand.
5. **Codex's corrections.** `fixes/RECONCILE_CODEX_6.json` reconciles Codex's earlier corrections with the layers:
   of 313 queue entries, 203 applied, 7 present, 3 superseded, 100 rejected; of 72 tagged source records, 28 applied,
   2 present, 1 superseded, 41 rejected. Decide every rejected one from the scan: accept it, or confirm the rejection,
   with a reason. On pp. 672–689, compare the layers with `fr/codex/sga6_fr_r1_fr.tex` as a second reading.
6. **The differences from Codex's tree.** `fr/codex/HOLD_VS_CORR.md` (and `.json`) lists 119 places where Codex's
   HOLD tree and the corrected layer differ. Each is explained by a fix or a misprint record, or it is not: decide
   every unexplained one from the scan.
7. **The conventions of the volume.** The checkers left these for one decision per exposé or for the whole volume
   (`conventions/GLOBAL_ISSUES_SGA.md`, items 76, 81, 82, 84, 86, 87 and 88; `conventions/NOTE_6.txt`):
   - the raised dot (K^•, L^•, Gr^•) written as a prime, as ∘ or as a lower dot; the dot of Exposé XIV (L^• or L_•);
   - letters and functors the print underlines (Pic, Isom, Proj, Hom, the underlined A, E, L(S), C): underline kept in
     the diplomatic form, one notation in the corrected form;
   - statements the print underlines, and defined terms the TeX emphasizes where the print does not;
   - item letters and paragraph numbers set in bold where the typescript types them plain;
   - `\Ob` against `ob`; `\Abfil` against the underlined "Ab.fil."; `\cdots` for the typed baseline dots;
   - the exterior power (small wedge or Λ) and the forms of Gr with a hat;
   - the structure sheaf (script or plain O) in Exposés XIII–XIV; φ in Exposé XIV;
   - the double-struck letters and P (`\mathbb` or `\mathbf`); asterisks; n°; `\cl` against cℓ; `\Gro`.
   Decide each from the scan: the diplomatic layer follows the print; the corrected layer follows one notation per
   distinction the print makes, stated in the README.

**Your own check** finds what the checkers missed. Record each of your findings the same way.

**Where the print itself is damaged** (a broken or faint stroke, an ink blot), decide the reading from the witness,
the neighbouring text and the mathematics, and say so in the reason.

## The six readers

Build one book per form and language. Each is a single LaTeX file that compiles with a standard TeX Live:

| File | Language | Form |
|---|---|---|
| `SGA6_FR_diplomatique.tex` | French | **Diplomatic**: the text as printed, misprints kept, with the page of the print marked at every page break |
| `SGA6_FR_corrige_apparat.tex` | French | **Corrected, with apparatus**: misprints corrected. Every place where it differs from the print is marked; the apparatus gives the printed reading, the correction and its source |
| `SGA6_FR_texte_de_lecture.tex` | French | **Plain reading text**: the corrected text with no apparatus; the printed page numbers in the margin only; a short preface says what was left out |
| `SGA6_EN_diplomatic.tex` | English | **Diplomatic**: the English that follows the print. Where a misprint changes the English, its printed reading is kept. The print's page breaks are marked |
| `SGA6_EN_corrected_apparatus.tex` | English | **Corrected, with apparatus**: as for the French |
| `SGA6_EN_reading.tex` | English | **Plain reading text**: as for the French |

**Build all three forms of a language from one annotated master.** Mark every place where the print and the
corrected text differ, for instance with a macro `\var{printed reading}{corrected reading}{source id}`. Generate the
three forms from that master by switching the macro, so the forms cannot drift apart. A misprint that does not change
the English (a French spelling, for example) gets no variant in the English.

## Sources of record

**French** (`SGA6_FR.zip`):
- **Base:** `fr/sga6/diplomatic/main.tex` and `fr/sga6/current/main.tex`, the two layers after the check of 10–13
  November.
- **Before side of the French change log:** `fr/codex/ref_hold/main.tex`, Codex's tree of August 2026.

**English** (`SGA6_EN.zip`):
- **Base:** `en/sources/`, sga-en's `sources/native/SGA6`. The main file is
  `SGA6_English_current_buildable_source_20260823/02f_SGA6_English_Master.tex`; its fragments are named by the scan
  pages they cover. The fragment for source pages 1–525 is, by its own name, an inherited English that is only partly
  synchronized with the French; the later fragments are synchronized with it.
- **Before side of the English change log:** `en/release_v2026-11-12/07_SGA6_EN_CURRENT_LAYERED_READER.tex`, the
  English as released on 12 November 2026.
- **Alignment:** align the English with the French by exposé, section and paragraph number, and put the print's page
  breaks in the English at the same places.
- **Fixes:** carry every French fix that changes the English into the English.
- **Translation:** translate the French text the English lacks, and correct the English wherever it does not render
  the French (an omission, an addition, a wrong sense). Mark each such passage in the English change log; new text is
  AI-translated.

## Rules

1. **Keep the authors' notation and language** in every form.
   - Correct a misprint only where it is a misprint of the print, decided by you from the scan with a reason.
   - Never standardize notation silently.
2. **One English for the whole SGA.** All the SGA English readers will be merged into one book, so the English terms
   and notation of SGA 6 follow those already settled for SGA 4, SGA 4½, SGA 5 and SGA 7: their glossaries and
   notation decisions are in `en/glossaries/`. Write:
   - `GLOSSARY_SGA6_FR_EN.tsv` (French term or notation, English rendering, count, first place);
   - `GLOSSARY_INCONSISTENCIES.md` (every French term rendered in more than one way within SGA 6);
   - `CROSS_VOLUME_TERMS.tsv` (every term or notation where SGA 6's rendering differs from another volume's glossary:
     the term, each volume's rendering, your choice for SGA 6, and the reason).
   Make the English consistent where the variation is plainly a slip, and record each change in the English change log.
3. **Misprints of the print.** Decide the register as above and write `MISPRINTS_6_DECIDED.tsv`: page, place, the
   printed reading, the correction, the source (misprint record, finding id, your finding id) and the reason. A
   misprint is corrected in the corrected and plain forms, kept in the diplomatic form, and given an apparatus entry.
4. **The editors' text.** Keep the editors' notes and the Introduction as printed, marked as theirs, in the diplomatic
   and corrected forms. The plain reading text keeps the Introduction and leaves out only our apparatus.
5. **Credit and rights.** Each reader's front matter carries:
   - the authors and the volume's bibliographic data;
   - the other credits exactly as `en/repo_records/` (README, ATTRIBUTION, SOURCE_AUTHORITY) and
     `en/sources/SOURCES.md` give them; keep every human contribution they name;
   - the wording "AI-transcribed", "AI-translated" and "AI-produced corrections", never "AI-assisted":
     - Codex's layers and corrections (August 2026), the check of every page by Claude Opus 5.5 at effort max
       (10–13 November 2026) and this build are AI-produced corrections;
     - the English is AI-translated;
     - credit this build to GPT-6 Astra (OpenAI, ChatGPT Pro mode);
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

Deliver three ZIPs: `SGA6_READERS_FR.zip`, `SGA6_READERS_EN.zip` and `SGA6_READERS_RECORDS.zip`. Together they hold:

- **Readers:** the six reader `.tex` files and the two annotated masters, with their PDFs. Leave a PDF out only if a
  ZIP would exceed about 100 MB, and say so.
- **`PAGES_CHECKED.tsv`:** one row per printed page (the front matter and pp. 1–700). Columns: the PDF page, checked
  against the scan, the number of findings, and where the page begins in each master.
- **`FINDINGS_DECIDED.tsv`:** one row per checker finding and per FIXLOG row. Columns: the id (batch file and index,
  or log and line), your verdict (confirmed, amended, reverted, not applied and now applied), the print's reading, the
  image and region you read it from, the change made, the forms affected, and the reason.
- **`MISPRINTS_6_DECIDED.tsv`.**
- **`OPEN_ITEMS_DECIDED.tsv`:** the 16 open replay items and the 7 hand-placed findings.
- **`CODEX_DECIDED.tsv`:** the 141 rejected Codex corrections and the 119 differences from the HOLD tree.
- **`CHECK_FINDINGS.tsv`:** every finding of your own check. Columns: id, page, place, the print's reading, the TeX's
  reading, the change, kind, and reason.
- **`DECISIONS.tsv`:** the conventions of the volume, the marker of p. 690, the page breaks you settled, and every
  other decision, each with its reason.
- **`CHANGES_FR.tsv`:** every difference between the corrected French reader and Codex's tree, and between it and the
  corrected layer as attached. Columns: page, place, before, after, source.
- **`CHANGES_EN.tsv`:** every difference between the corrected English reader and the released English, the new and
  corrected translations included.
- **Glossary:** `GLOSSARY_SGA6_FR_EN.tsv`, `GLOSSARY_INCONSISTENCIES.md` and `CROSS_VOLUME_TERMS.tsv`.
- **`APPARATUS_COUNTS.md`:** per exposé and form, the number of apparatus entries by kind.
- **`README.md`:** what each file is, how each form was made, all the counts, the printed matter not reproduced and
  why, and the compile status of each reader with its LaTeX errors and warnings.
- **Your build scripts,** with their outputs.

## When it is done

**Each item is done when:**
- **A page** has been compared with the scan, and its row in `PAGES_CHECKED.tsv` is filled.
- **A finding** (checker finding, FIXLOG row, misprint record, open item, rejected Codex correction, HOLD difference,
  convention) has a verdict read from the scan, and its reason.
- **A reader:**
  - compiles without errors;
  - carries every accepted fix and every finding of your own check, checked by script against your decision tables,
    with the counts reported;
  - has page markers that agree with `PAGES_CHECKED.tsv`.
- **The apparatus** has one entry for each difference between the diplomatic and the corrected forms, and none for
  anything else.

**Not acceptable:**
- a page left unchecked, or a finding without a verdict;
- a verdict not read from the scan;
- a reader that drops, summarizes or paraphrases any part of the text;
- a fix applied in one form and missing from another;
- an apparatus entry without a source;
- someone's work presented as ours, or credited wrongly;
- a silent change of notation;
- a decision without a reason;
- local paths or e-mail addresses in any output.

**The task is finished** only when every page is checked, every finding is decided, and all six readers and every
file listed above are in the three ZIPs. Keep working until then. Do not stop because:
- what remains is long;
- a part of the work looks presentable;
- much has already been done.

## Working method

- Start from the manifests, `PAGE_INDEX.tsv`, the fix logs and the findings.
- Check the pages in order, exposé by exposé, with the scan and the witness, and write the decision tables as you go.
- Build the annotated masters by script, generate the forms, compile, and check the counts.
- After each finished exposé and each finished reader, save a checkpoint ZIP to the user's Library, or wherever files
  survive the loss of the execution environment. Name it `SGA6_READERS_checkpoint_<NN>.zip`, with `NN` counting up;
  never overwrite, rename or delete an earlier checkpoint, and never put an earlier checkpoint ZIP inside a new one.
  If the workspace comes back empty, restore it from the newest checkpoint and from this conversation before you
  continue. Save the final ZIPs there too; they hold everything the checkpoints held, and a file left out of the final
  is listed in the README with the reason.
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
