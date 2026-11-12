# SGA 7 I and II: English readers, raw build of 12 November 2026

This folder holds the English readers build of SGA 7 (*Monodromy Groups in Algebraic Geometry*, Volumes I and II) in three forms, all made from one annotated master:

- `EN/SGA7_EN_diplomatic.tex` and `.pdf`: the diplomatic text;
- `EN/SGA7_EN_corrected_apparatus.tex` and `.pdf`: the corrected text with critical apparatus;
- `EN/SGA7_EN_reading.tex` and `.pdf`: the plain reading text;
- `EN/SGA7_EN_annotated_master.tex` and `.pdf`: the annotated master (byte-identical to the corrected form).

`RECORDS/` holds the build records: change logs, apparatus registers and counts, the French–English glossary and its attestations, editorial decisions, provenance, input verification, compilation logs and the build scripts. Start with `RECORDS/README.md`.

The same build also made the French readers (texte diplomatique, texte corrigé avec apparat, texte de lecture), in the French repository: https://github.com/KokunoYumeto/sga-fr/tree/main/raw/pro_returns/SGA7_READERS_20261112

## Who made it

The build is by GPT-6 Astra (OpenAI, ChatGPT Pro mode), 12 November 2026, from the checked layers it was given: the French diplomatic and current layers of SGA 7 (AI-transcribed, with AI-produced corrections from the scan check), their correction logs and decisions, and the English release `v2026-11-12-english-edition` of this repository (commit `4a4cbac`; AI-translated, with AI-produced corrections). Exposé VI by D. S. Rim was written in English and keeps its original English. The authors of SGA 7 are Alexander Grothendieck, with M. Raynaud and D. S. Rim (Volume I, Lecture Notes in Mathematics 288, Springer, 1972) and Pierre Deligne and Nicholas Katz (Volume II, Lecture Notes in Mathematics 340, Springer, 1973). Each reader's front matter carries the full credits and the rights statement.

## Status

This is the build as it came back; we have not reviewed it yet. The corrected reader marks 13 places as needing the scan; they are still open. The released English edition in `sources/` and in the releases is unchanged by this folder.
