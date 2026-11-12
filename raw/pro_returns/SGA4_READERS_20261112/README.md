# SGA 4: English reading text, raw build of 12 November 2026

This folder holds the English reading text of SGA 4 (*Théorie des topos et cohomologie étale des schémas*, Tomes 1–3, Exposés I–XIX including V bis) and the records of the build that made it.

- `EN/SGA4_EN_reading.pdf` (863 pages): the plain reading text. It carries the corrected mathematical text without the critical apparatus, the dispute records, the possible-misprints appendix and the editorial notes of the LaTeX edition. The original tome and page numbers stand in the margin.
- `RECORDS/`: the build records that reproduce no editorial-note text: change decisions, misprint placements and judgments, apparatus counts, the French–English glossary, compile logs and diagnostics, PDF checks of the reading forms, verification results and the build scripts. Start with `RECORDS/README.md` (the build's own README).
- `RECORDS/FRONTMATTER_FIXES.json`: the front-matter corrections described below.

The French reading text of the same build is in the French repository: https://github.com/KokunoYumeto/sga-fr/tree/main/raw/pro_returns/SGA4_READERS_20261112

The same build also made diplomatic and corrected-with-apparatus readers in both languages and an annotated master per language. They are not published here, and neither are the TeX sources of any form, because they contain the full text of the LaTeX edition's editorial notes (N.D.E.). Our editions give an editor's notes in our own words, with credit; that version is not written yet. Thirty-five record files that quote those notes are held back for the same reason.

## Who made it

The build is by GPT-6 Astra (OpenAI, ChatGPT Pro mode), 12 November 2026. It was made from our scan-checked French text of SGA 4 and from the English edition in this repository (commit `4a4cbac`, release `v2026-11-12-english-edition`).

- **Seminar and printed edition.** *Séminaire de géométrie algébrique du Bois-Marie 1963–1964* (SGA 4), directed by M. Artin, A. Grothendieck and J.-L. Verdier, with the collaboration of N. Bourbaki, P. Deligne and B. Saint-Donat. M. Artin, A. Grothendieck and J.-L. Verdier edited the printed edition: Lecture Notes in Mathematics 269 and 270 (Springer, 1972) and 305 (Springer, 1973). The authors of each exposé are credited in the text.
- **French LaTeX edition.** The French text rests on the LaTeX edition of SGA 4, Tomes 1–3, made and distributed by Fabrice Orgogozo: https://www.normalesup.org/~forgogozo/SGA4/ (source snapshot at git commit `71766d9`). His corrections of the print are kept in the corrected text and credited to him.
- **Our layers.** The French was checked against the scans of the print by Claude Opus 5.5 and GPT-6.1 Sol (11 November 2026); the corrections from that check are AI-produced corrections. The English is AI-translated (OpenAI Codex, with GPT-6.1 Sol and Claude Opus 5.5 for the ports of corrections). The readers' assembly and typesetting are AI-produced (GPT-6 Astra).

The reader's front matter carries the full credits and the rights statement.

## The build's own validation (as reported)

- 81 of 81 verification checks passed (`RECORDS/VERIFICATION.json`).
- Six readers compiled with XeLaTeX and amsbook with 0 errors and 0 missing glyphs: French 1,050 / 1,684 / 877 pages, English 1,008 / 1,413 / 863 pages (diplomatic / corrected with apparatus / reading).
- 1,557 printed pages placed, with their marginal page numbers checked in every reader.
- 898 agreed transcription fixes and 930 agreed misprints of the print accounted for; 2,207 French and 1,956 English apparatus entries.
- 1,601 one-model misprint reports judged: 550 accepted, 1,043 left as possible misprints (an appendix of the corrected form), 8 rejected.
- 643 disputed readings on 443 pages are marked, not decided: they wait for a second check against the scans.
- 56 French corrections that had to be replayed by hand are placed or accounted for; 18 changes touching the LaTeX edition's apparatus are listed, not applied.

## Our check of this build (Claude Opus 5.5, 12 November 2026)

- **Completeness.** The three archives were unpacked and their files counted: French 9, English 9, records 248. Every PDF has the page count the build reports.
- **Compilation.** All six readers compiled again from their TeX, in a separate folder, with XeLaTeX three passes and shell escape off: 0 errors, 0 missing characters, 0 undefined references; page counts as above.
- **Privacy.** No personal names, local paths, e-mail addresses, keys or tokens in any published file, including the PDF text and metadata.
- **Front matter.** We corrected the front matter in our copy of the TeX of all eight files and recompiled the PDFs published here: the 1972–73 editors are now named as such, Orgogozo's page is linked, and the French readers' take-down link points to the French repository. The text is otherwise unchanged; the old and new lines are in `RECORDS/FRONTMATTER_FIXES.json`.
- **Reading text.** At three places (V bis p. 138, where the proof of Lemma 3.3.3.3 was rewritten in the LaTeX edition; XIV pp. 145–146, Theorem 1.1 and its notes; XVI 3.9–3.10) the reading text has no notes, variant marks or dispute marks, and its words match the corrected form once those are removed.
- **Pages not in the source.** The build had no text for the exposés' summary pages (V p. 1, V bis p. 83, VI pp. 163–164, VII p. 341, VIII p. 366, XVI p. 206, XVII pp. 250–251) or for the tomes' front matter and indexes. The scans we hold contain all of them; they are to be transcribed later.

## Status

This is the build as it came back, with the front-matter corrections above. The released English edition in `sources/` and in the releases is unchanged by this folder.

## Rights

The rights in the original work belong to its author or the author's representatives or heirs. Where we hold rights, in the AI-produced transcription, translation, corrections and typesetting, they are dedicated to the public domain under CC0 1.0. This edition is published for educational, non-profit purposes, and we claim no rights we do not hold. If you hold rights in this work and object to its publication here, please open a GitHub issue and we will take it down.
