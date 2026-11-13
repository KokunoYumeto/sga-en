# English working record

## Status

This directory contains unfinished volume-wide work. The four reader sources are
generated from one annotated master. Exposé 0, including the appendix and
Grothendieck letter on printed pages 1–77, and Exposé I through printed 110 have
been freshly AI-translated from the French pages checked by the early reviewer
and coordinator. The English comparison follows the French paragraphs, formulas,
author notes and copyist interpolations. Beyond 110, the body retains the
supplied inherited English; no completed translation review is claimed there.

All four TeX sources are generated through 110, with 28 accepted exact-text
replacements and 92 source-linked variants. At the checkpoint03 handoff, their
PDFs still represent the successful through-95 build: corrected and annotated
387 pages, diplomatic and reading 376 pages, each completed in two passes.
The coordinator will compile the frozen through-110 source snapshot. The work
summary distinguishes generated, compared and compiled scope explicitly.

The p90 matrix spacing and display-variant wrapper repairs have been applied
and visually verified by compiling the exact generated fragments with the same
preamble. Their full-document rendering will be checked in the frozen-stage
build. Every reader retains its visible in-progress notice: the requested
volume-wide completion gate is unmet.

## Native source inventory

The supplied native master has fifteen active TeX files. Their recursive
expansion has 21,061 lines and 1,246,448 Unicode characters. Comparison with
the supplied released English has nineteen difference hunks, all from inclusion
comments and trailing `\relax\space` wrappers. The inactive input inside
`\SGAArchiveOnly` is consumed without expansion by that macro and is not an
active build dependency. `EN_SOURCE_MAP.tsv` retains the original native line
provenance; `EN_INPUT_GRAPH.json` records the active inclusion graph.

## Reviewed changes

The Introduction regains its omitted Hartshorne reference. Its statement that
the first proof has not appeared in the literature includes Borel–Serre and
the present seminar within that absence, as the French does. The contents gives
the printed starts I 78, III 222 and IV 274, retains the raised dot in the titles
of VI and VII, and restores plain K with its punctuation in IX. The Exposé III
start was independently viewed at main PDF 236, after the Exposé II bibliography.
These are specific front-matter decisions; the complete front-matter alignment
remains unfinished.

The renewed Exposé 0 restores full paragraphs, formulas and author commentary
that the inherited English shortened or altered. Restorations include the p. 8
paragraph and formula 3.2 on perfect complexes, the p. 15 cap-product note, source
cotangent and Euler-characteristic notation, the complete hat over A tensor Q,
underlined representation-ring notation, uppercase Chern C, script Todd T and
exterior-power symbols. The original mixed numbered/starred note labels and
repeated calls are explicit.

Later appendix passages restore lower-shriek Grothendieck-group direct images,
the omitted p. 53 filtration paragraph, the original intermediate class y-prime,
the source restriction notation and diagram orientation, both distinct lemmas
numbered 2.15, and the locally named C_j Grassmannian factors. The p. 65 Tor formula
retains its base ring, subscript, arguments and exterior-power exponent. The
Riemann–Roch passage restores G_p, C(T_X), varkappa_r, uppercase C_P/ch_P and
the omitted author note 69. The final proof restores the copyist note and all
inspected interpolation stars, checked bundles, the complete binomial formula
on 75, the leading y in the membership statement on 76, and the literal final
signature.

`EN_TRANSLATION_PATCHES.jsonl` retains every complete before/after passage.
`EN_VARIANTS.jsonl` gives the exact printed and corrected English readings,
source identifier, scan locator and reason. French spelling/agreement changes
whose English wording is unchanged have no artificial English variant. Retained
French and German publication titles and the observed KÜnneth name-case reading
are represented explicitly. `EN_EARLY_CURRENT_TRANSFER_001_077.tsv` individually
classifies all 61 current-only early-review patch rows as either an English
variant or an unchanged English rendering. This separate prose-reference check
caught and corrected the p. 8 citation of 2.1 in place of 2.2; it supplements the
mathematical-unit comparison.

## Mathematical comparison and typography

`verify_reviewed_english.py` compares 3,548 literal mathematical units across
printed 1–110 against the exact reviewed French current text. Exposé I uses the
coordinator's page packets plus their recorded patches, with page and patch
hashes preserved. Units are complete equation/align environments, bracketed displays,
parenthesized inline math and dollar-delimited inline math. Multisets permit
prose word-order changes; no whitespace or mathematical command is removed or
rewritten. The only nonidentical units are 27 paired occurrences, stored as 26
current-applicable complete exact pairs with explicit multiplicities: lexical formula translations
and the translated author note inside formula 2.10. There are zero unexpected
literal differences. This check supports the passage comparison and makes no
claim about the unreviewed remainder. `verify_expose_i_forms.py` separately
materializes every Exposé I printed and corrected reading, then compares both
against the corresponding reviewed French 78–110. Both branches have zero
unexplained mathematical-unit differences; their only differences are the nine
explicit lexical formula translations per branch. This verifies the source
branches, while the individual transfer ledgers also record prose, typography,
notes and references. It does not replace a prose comparison or PDF inspection.

The early reviewer confirmed the retained emphasis groups through77 as printed
underlining. `source_emphasis.py` renders their corresponding English words
upright and underlined, while preserving the mathematical symbols and keeping
explicit author notes and page markers independent. It records 167 inspected
emphasis groups and 509 resulting word spans. Four lexical groups inside formula
text receive explicit emph-to-uline wrapper changes; those exact pairs are listed
in `EN_FONT_RENDERING_RECORD.json`. The formatter compares every other byte of
the mathematical units. It does not impose a font convention on the unreviewed
English body. Exposé I uses the coordinator's explicitly inspected word-group
spans, including the independently underlined site/category symbols and the
defined terms that remain plain. These direct `uline` groups are preserved and
are not included in the formatter's inherited `emph` conversion count.

## Build and alignment evidence

`audit_build_english.py` produces the native flattening, provenance, source
graph, heading outline, release comparison, credit record and terminology
candidates. `build_english_candidates.py` applies accepted exact-text patches,
embeds credits and the requested rights wording, and generates the annotated
master plus all three forms. `compile_candidates.py` runs two passes and writes
path-free diagnostic summaries, source/PDF hashes, compiled print markers and
variant identifiers in `EN_CANDIDATE_BUILD_STATUS.json`. Its source hashes were
unchanged during all four final compilations.

The only final diagnostics are reading-form margin-marker movement on output
pages20/21/49. These have been visually checked: the markers are outside
the body and legible. Regional PDF checks, including title78, numbered notes85,
diagram variants86/92 and the composite94, are recorded in
`EN_PDF_VISUAL_QA.json`. No whole-volume visual inspection is claimed. Actual
encoding/layout failures and repairs are recorded in `EN_BUILD_REPAIRS.jsonl`.

`make_alignment_hints.py` maps all 77 reviewed printed-page start markers to
one-based supplied-French lines, generated-English-master lines, primary PDF
pages and witness pages. Its PDF column gives the reflowed pages containing
each start marker; it does not claim that all content of a printed page fits on
that output page. All 77 markers were found in the current corrected PDF. The
alignment status records exact source/PDF hashes.

## Terminology

The candidate inventory contains 1,116 French/English pairs from the supplied
SGA 4, 4½, 5 and 7 glossaries, filtered by literal French occurrence. There are 128
French expressions with multiple reference English renderings that also occur
in the inherited English corpus. The candidate inconsistency and cross-volume
files leave unpaired choices unresolved. Counts are exact, case-sensitive
literal matches with alphabetic boundaries in the TeX body, including headings,
comments and math operands. They refer to the supplied native English before
the renewed passages; they do not prove semantic inconsistency.

`GLOSSARY_SGA6_REVIEWED_001_077.tsv` separately contains 81 paired terms from the
reviewed Exposé 0 passage, counted only there. It remains a scoped terminology
record. The requested volume-wide glossary and cross-volume decisions are
unfinished.

## Credits and privacy

`CREDITS_REQUIRED.md` preserves the supplied human credit text and its attribution
scopes. `EN_NEW_EDITION_FRONTMATTER.tex` supplies reusable English front matter
with the named human contributors, original bibliographic data, AI-transcribed,
AI-translated and AI-produced-corrections wording, and the requested English
rights statement. The French coordinator handles its French counterpart.
No email address or private local path is included in the English text records
or derived documents. Raw TeX package-loading logs are replaced by diagnostic
summaries. Original English source files have not been modified.
