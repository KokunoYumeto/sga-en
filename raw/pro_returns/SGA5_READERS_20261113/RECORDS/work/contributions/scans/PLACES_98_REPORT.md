# Exposé XV: the 32 RΓ readings

All 32 requested occurrences show an ordinary upright/typescript R with **two short horizontal strokes beneath it**. Each occurrence was located and visually inspected in its original strip; the regions are recorded in `PLACES_98_DECIDED.tsv`. The accompanying native-resolution crops preserve those regions without retouching. The two contact sheets enlarge the crops for comparison.

| Printed folio | IDs | Double-underlined R |
|---|---|---:|
| 457 | R98-01–R98-07 | 7 |
| 458 | R98-08–R98-11 | 4 |
| 459 | R98-12 | 1 |
| 460 | R98-13–R98-22 | 10 |
| 461 | R98-23–R98-24 | 2 |
| 470 | R98-25–R98-26 | 2 |
| 472 | R98-27–R98-28 | 2 |
| 473 | R98-29–R98-30 | 2 |
| 474 | R98-31–R98-32 | 2 |
| **Total** | | **32** |

The evidence identifies the letter body, Gamma and two lower strokes separately. Its transcription is therefore `\underline{\underline{\mathrm{R}}}\Gamma` in the diplomatic forms. The corrected forms retain the existing upright-R derived-functor convention recorded in `conventions/GLOBAL_ISSUES_SGA.md`, item 98, using `\mathrm{R}\Gamma`. Every one of these 32 locations consequently contributes a typography variant to each language's corrected apparatus. No argument, Gamma, superscript or subscript is altered by this decision.

## Two points resolved by the images

1. **R98-18, p. 460.** Item 98 provisionally described the lower diagram label as plain. In `scans/page_460_s2.png`, region `[708,42,784,103]`, two separate horizontal strokes appear below R. The wider detail in `evidence/R98-18-detail.png` includes the full start of the label, establishing its identity as `RΓ(Fr*_{F⊗F'/X×X'})`. The diplomatic form therefore carries the double underline here too. This decision supersedes that provisional description.
2. **R98-25 and R98-26, p. 470.** Both R subscripts have two underlines in `scans/page_470_s3.png`. The short checker crop `checker_crops/c470_frRG.png` omits the lower edge of the first R; `checker_crops/c470_frRG2.png` and the full strip show both strokes. The second occurrence is independently clear in `checker_crops/c470_fRG.png`.

## Plain-R control on p. 461

The first RΓ on p. 461, in the sentence saying that the endomorphism is defined by the pair, has **no lower strokes**. It appears in `scans/page_461_s2.png`, region `[90,88,159,151]`, and in `checker_crops/p461_RGamma1.png`. The French layers already transcribe this occurrence explicitly with upright R; it is outside the requested 32. The ported English instead has `\RGamma` there. The English build must explicitly use `\mathrm{R}\Gamma` in all three forms at that location. This is a transcription repair shared by the English forms, with no diplomatic/corrected variant of its own.

The next two occurrences on the same strip are R98-23 and R98-24. Both have two lower strokes, corroborated by `checker_crops/p461_RGamma2.png` and `checker_crops/p461_RGamma3.png`.

## Alignment and reproducibility

`PLACES_98_PATCHES.json` gives the exact source token, source line, character interval and surrounding text in both French layers and the ported English. Character intervals refer to Python's UTF-8-decoded text with universal newlines; they are intended for use before later source edits. All file references are paths inside the supplied ZIPs.

In the English Exposé XV, the first 22 RΓ occurrences correspond to R98-01–R98-22. The 23rd is the plain-R control. The 24th and 25th correspond to R98-23 and R98-24. The remaining eight correspond to R98-25–R98-32 and are written as bare `R\Gamma` in the ported source. They need explicit glyph transcription in both branches.

The original `estimated_strip` values are estimates from TeX positions. Several point to adjacent strips that do not contain the complete glyph; the decided table uses the visually verified strips and coordinates instead. Coordinates have their origin at the upper left; `[x0,y0,x1,y1]` gives a Pillow-compatible rectangle in original strip pixels, with the right and lower edges excluded.

To reproduce the tables, source alignment, exact crops and contact sheets, run:

```bash
python decide_places98.py --sources extracted_archives --output scans_decisions
```

The source directory contains `SGA5_FR`, `SGA5_EN` and `SGA5_SCANS` extracted under those names. The script checks the identity, order and folio of all 32 French occurrences and checks the 33-occurrence English sequence including the control. It records a SHA-256 hash for every image used. Pillow is needed for evidence image generation; the TSV and JSON require Python's standard library only. The recorded visual judgments are inputs to the script; the script does not claim to infer glyph identity automatically.
