# SGA 6 reader checkpoint

**Status: incomplete. This is a resumable checkpoint, not the requested final six-reader release.**

## Verification recorded at this checkpoint

87 of 714 primary front-matter/numbered pages have an independent full-page comparison recorded. 627 remain unchecked or incomplete.

| Record class | Total | Decided | Pending |
|---|---:|---:|---:|
| finding | 3751 | 478 | 3273 |
| fixlog | 5513 | 602 | 4911 |
| misprint | 724 | 157 | 567 |
| replay | 20 | 2 | 18 |
| manual | 7 | 0 | 7 |
| hold_difference | 119 | 39 | 80 |
| rejected_codex | 141 | 25 | 116 |

Own findings recorded: 165.

A row marked pending is an explicit absence of an independent verdict. No prior checker confidence, successful hash check, OCR extraction, diff, or LaTeX build is counted as a new scan review.

## Contents and construction

- `scripts/`: source integrity, exact patching, annotated French generation, record merging, compilation and checkpoint scripts.
- `readers/fr/`: three unfinished French forms and their common annotated master; PDFs are included only after successful compilation.
- `review/english/`: flattened native source, provenance map, page-aligned retranslation chunks, exact translation edits, individually sourced variants, candidate glossary material, four unfinished English TeX files and available PDFs.
- `review/front/`, `review/early/`, `review/late/`, `review/middle/`: explicit image-read decisions and exact-anchor patch files. Original supplied layers are not overwritten.
- `records/`: exhaustive decision queues with actual statuses, input hashes, page checks, literal changes, annotation data and compile diagnostics.

The French generator applies reviewed patches to the two supplied layers, verifies every exact anchor count, and computes page-local TeX-atom differences. Math spans and macro arguments stay intact. Both alternatives are stored in each `SGAvar` call. The three French forms differ only in the `SGAform` switch. The intermediate representation reconstructs each patched input text exactly before documented typesetting transports.

The French apparatus currently prints exact LaTeX alternatives for auditability. Many inherited differences still require scan-decision links. This apparatus is a working apparatus, not the final readable adjudicated apparatus.

The English generator uses its own common annotated master. Reviewed English replacements are logged passage by passage. French spelling corrections that have no effect on the English produce no English variant. Unchecked inherited English remains explicitly unverified.

## Front matter, boundaries and printed matter

The main scan has 720 PDF pages. Printed folio F is PDF page F+14. The witness has 711 DjVu pages; its folio F is physical page F+11, directly verified. Front-matter offsets differ: main PDF3 is witness1; main PDF11 is witness9; main PDF13 is witness10 because the blank main PDF12 is absent from the witness.

The source title/credits page, Preface, Introduction and contents have been compared. Front breaks include com-/plexe across VII/VIII and the beginning of IX at «d’un morphisme projectif d’espaces analytiques complexes». New transcription restores the cover, publisher title and colophon in French. The inside-cover publisher notice is partly hidden by an attached label and has no counterpart in the witness; its covered text remains unresolved and is visibly marked incomplete in the working transcription. Institutional stamps, barcodes, handwritten prices and attached labels are copy-specific marks and are not transcribed as the printed work. Publisher logos are non-textual decoration.

The publisher catalogue after folio700 (main PDF715–720) remains to be inspected/transcribed. The English transfer of the newly restored publisher matter also remains pending. No claim of complete printed-matter coverage is made.

## Notation and typesetting

The reviews use occurrence-specific glyph readings. Raised dots, lower dots, primes, asterisks, underlines, plain/script/double-struck letters and author footnote marks are retained where observed. No global replacement of a mathematical letter is inferred from its role. The exact notation convention decisions requested for the rest of the volume remain open.

Technical transports in the French generator: a TikZ-CD diagram scanned as a macro argument uses `ampersand replacement=\&`, with each original column delimiter mapped to `\&` and its count checked; heading underline boxes are preserved inside a maximum-width box to prevent clipping; footnote hyperlink generation is disabled to avoid inherited missing PDF destinations. These operations retain the displayed source text; they do not decide a reading.

## Compilation

| French file | Exit | PDF pages | Errors | Warnings |
|---|---:|---:|---:|---:|
| SGA6_FR_corrige_apparat_DRAFT.tex | 0 | 530 | 0 | 0 |
| SGA6_FR_diplomatique_DRAFT.tex | 0 | 378 | 0 | 0 |
| SGA6_FR_master_annote_DRAFT.tex | 0 | 530 | 0 | 0 |
| SGA6_FR_texte_de_lecture_DRAFT.tex | 0 | 379 | 0 | 0 |

Full path-free French diagnostics are the corresponding `records/COMPILE_*.json` files. English compile results:

```json
{
  "corrected_apparatus": {
    "runs": [
      {
        "run": 1,
        "exit_code": 0,
        "diagnostics": [
          "Underfull \\hbox (badness 8132) in paragraph at lines 21300--21301\n[]\\T1/lmr/m/n/10.95 (+20) Source: fix-es/MISPRINTS_6.json#18; check/findings/fi\nndings_026_030.json#6; re-",
          "LaTeX Warning: Temporary extra page added at the end. Rerun to get it removed."
        ],
        "output": "Output written on review/english/DRAFT_SGA6_EN_corrected_apparatus.pdf (382 pag"
      },
      {
        "run": 2,
        "exit_code": 0,
        "diagnostics": [
          "Underfull \\hbox (badness 8132) in paragraph at lines 21300--21301\n[]\\T1/lmr/m/n/10.95 (+20) Source: fix-es/MISPRINTS_6.json#18; check/findings/fi\nndings_026_030.json#6; re-"
        ],
        "output": "Output written on review/english/DRAFT_SGA6_EN_corrected_apparatus.pdf (381 pag"
      }
    ],
    "pdf_present": true,
    "scan_collation_complete": false
  },
  "diplomatic": {
    "runs": [
      {
        "run": 1,
        "exit_code": 0,
        "diagnostics": [],
        "output": "Output written on review/english/DRAFT_SGA6_EN_diplomatic.pdf (379 pages, 23803"
      },
      {
        "run": 2,
        "exit_code": 0,
        "diagnostics": [],
        "output": "Output written on review/english/DRAFT_SGA6_EN_diplomatic.pdf (379 pages, 23803"
      }
    ],
    "pdf_present": true,
    "scan_collation_complete": false
  },
  "reading": {
    "runs": [
      {
        "run": 1,
        "exit_code": 0,
        "diagnostics": [
          "LaTeX Warning: Marginpar on page 20 moved.",
          "LaTeX Warning: Marginpar on page 21 moved."
        ],
        "output": "Output written on review/english/DRAFT_SGA6_EN_reading.pdf (379 pages, 2380192 "
      },
      {
        "run": 2,
        "exit_code": 0,
        "diagnostics": [
          "LaTeX Warning: Marginpar on page 20 moved.",
          "LaTeX Warning: Marginpar on page 21 moved."
        ],
        "output": "Output written on review/english/DRAFT_SGA6_EN_reading.pdf (379 pages, 2380192 "
      }
    ],
    "pdf_present": true,
    "scan_collation_complete": false
  },
  "annotated_master": {
    "runs": [
      {
        "run": 1,
        "exit_code": 0,
        "diagnostics": [
          "Underfull \\hbox (badness 8132) in paragraph at lines 21300--21301\n[]\\T1/lmr/m/n/10.95 (+20) Source: fix-es/MISPRINTS_6.json#18; check/findings/fi\nndings_026_030.json#6; re-",
          "LaTeX Warning: Temporary extra page added at the end. Rerun to get it removed."
        ],
        "output": "Output written on review/english/DRAFT_SGA6_EN_annotated_master.pdf (382 pages,"
      },
      {
        "run": 2,
        "exit_code": 0,
        "diagnostics": [
          "Underfull \\hbox (badness 8132) in paragraph at lines 21300--21301\n[]\\T1/lmr/m/n/10.95 (+20) Source: fix-es/MISPRINTS_6.json#18; check/findings/fi\nndings_026_030.json#6; re-"
        ],
        "output": "Output written on review/english/DRAFT_SGA6_EN_annotated_master.pdf (381 pages,"
      }
    ],
    "pdf_present": true,
    "scan_collation_complete": false
  }
}
```

Compilation and selected visual layout checks do not establish the correctness of unchecked source pages.

## Restore and reproduce

1. Extract the four original archives into one working directory, preserving their internal paths; retain each root manifest under a distinct archive-derived name.
2. Extract this checkpoint over that directory. It contains no original archives and no nested checkpoints.
3. Run `python scripts/intake.py --archives <the four archive files>` from the working directory. This revalidates every manifest hash and recreates review packets.
4. Reproduce review outputs with the scripts in the corresponding review directories; these scripts encode actual recorded observations and do not perform new automatic verdicts.
5. Run `python scripts/build_french.py`, `python scripts/merge_records.py`, and the English audit/generation scripts. Compile with a complete standard TeX Live installation. The optional isolated-tree wrapper falls back to the installed TeX environment when its local package tree is absent.
6. Continue the pending scan collation, exact English alignment/translation review, rejected-Codex decisions, conventions and glossary. The final release gate must require zero pending page/finding decisions, complete English transfer, sourced apparatus entries and error-free compiled readers.

## Material omitted from this checkpoint

The four supplied source ZIPs and their extracted source trees are reproducible inputs and remain in the original attachments. Downloaded TeX/DjVu runtime packages, raw engine transcripts with runtime paths, caches, generated image strips and prior checkpoint ZIPs are omitted. Image evidence is specified by original archive-relative scan, page and region; review scripts reproduce crops. Previous checkpoint files are never replaced or nested.

No final release ZIPs have been designated complete.
