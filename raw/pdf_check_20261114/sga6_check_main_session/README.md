# SGA 6 readers, final of 14 November 2026: PDF check and build fix

The check of the eight PDFs of the SGA 6 readers delivered by GPT-6 Astra (OpenAI, ChatGPT Pro mode) on 14 November
2026, and the build fix of the four French readers. Check and fix by Claude Opus 5.5 (Anthropic, effort max), with its
own scripts; the run's own compile script was not used.

## What was checked

Each of the eight delivered LaTeX files was compiled twice with pdfLaTeX (MiKTeX 26.5). The French sources set
`\hfuzz=20pt`, which keeps TeX from reporting any line that sticks out by less than 20pt; for the check that value was
lowered to 0.5pt. `\hfuzz` changes only what the log reports, not the layout: the page counts of the check builds equal
those of the delivered PDFs (French 390, 553, 390, 553 pages; English 388, 561, 387, 561).

| Reader | Overfull boxes | Over 2pt | Over 10pt | Widest |
|---|---:|---:|---:|---:|
| SGA6_FR_diplomatique | 4 | 4 | 2 | 12.93pt |
| SGA6_FR_corrige_apparat | 2 | 2 | 1 | 12.93pt |
| SGA6_FR_texte_de_lecture | 4 | 4 | 1 | 12.93pt |
| SGA6_FR_master_annote | 2 | 2 | 1 | 12.93pt |
| SGA6_EN_diplomatic | 0 | 0 | 0 | |
| SGA6_EN_corrected_apparatus | 0 | 0 | 0 | |
| SGA6_EN_reading | 0 | 0 | 0 | |
| SGA6_EN_annotated_master | 0 | 0 | 0 | |

The French boxes are two displays that run into the right margin, in all four French readers:
- the four maps i_*, j_*, f_*, g_* of 3.3 (folios 440-441), 12.9pt, output page 244 (245 in the apparatus forms);
- both readings of the array i)/ii) of Proposition 2.6 (variant FRV0450, folio 386), 9.9-10.3pt, output page 214
  (215);

and, in the diplomatic and reading forms, one page 2.19pt too high (output page 346).

Pages looked at, rendered to images: 214, 244 and 346 of the French diplomatic reader, 215 and 245 of the French
apparatus reader, and nineteen pages spread over the French and English readers. Nothing is cut and nothing leaves the
sheet; the two displays end in the margin, near the original's page numbers.

## The fix (French readers only)

`fix_wide_displays.py` wraps each of the two displays in `\adjustbox{max width=\displaywidth}{$\displaystyle ...$}`
(adjustbox is already loaded by the readers). This shrinks a display only when it is wider than the line; the wording
and the mathematics are unchanged. It also sets `\hfuzz=0.5pt`, so that a rebuild reports every overflow.

After the fix: no overfull box in the apparatus reader and the annotated master; in the diplomatic and reading forms
only the page 2.19pt too high (346), which was looked at and shows nothing cut. Page counts are unchanged.

## Files

- `fixed/<reader>/<reader>.tex` and `.pdf`: the four French readers with the fix.
- `check_overfull.py`, `OVERFULL_ALL.tsv`, `OVERFULL_SUMMARY.json`: the check of the delivered sources.
- `fix_wide_displays.py`, `fix_run.log`: the fix and its result.

Seen in passing, to be checked against the scan of folio 440: the sentence "Ces morphismes étant projectifs, on peut
définir les homomorphismes additifs (IV" ends without its reference in the French diplomatic reader.
