# Apparatus counts

## Counting rule

An **entry** is one unique identifier in `FR_APPARATUS.json` or `EN_APPARATUS.json`, with its individual printed and corrected readings. A **variant block** is one distinct `group_id` in that register; one marked passage can contain several entries. Counts of source-log records, alignment operations, or source issues are different quantities and are not substituted for entry counts.

The classification below reproduces the recorded `kind` field. Some kinds describe the origin of a correction (for example `misprint_pass`) rather than its linguistic or mathematical content; this report does not silently reclassify them.

## Totals by language and reader form

| Language | Reader form | Variant entries | Marked blocks | Inherited editorial notes | Retained/unresolved notes |
| --- | --- | --- | --- | --- | --- |
| FR | Diplomatic | 0 | 0 | 0 | 0 |
| FR | Corrected with apparatus | 2824 | 1112 | 0 | 17 |
| FR | Plain reading | 0 | 0 | 0 | 0 |
| EN | Diplomatic | 0 | 0 | 0 | 0 |
| EN | Corrected with apparatus | 1811 | 702 | 212 | 17 |
| EN | Plain reading | 0 | 0 | 0 | 0 |

Zero means no visible critical-apparatus entry or editorial note in that form. The single-file TeX necessarily retains the inactive alternatives. The report checks that every numbered apparatus target and editorial note lies in a corrected-form-only conditional, that each reader selects the stated form, and that each file is exactly the corresponding master with that selector changed. This is a source-level visibility audit; PDF compilation and page-level inspection are recorded separately.

## Counts by exposé

The two zero columns are included explicitly. The final two note columns are separate from the variant entries and are visible only in the corrected-apparatus form.

### FR

| Volume / exposé | Diplomatic | Corrected | Reading | Blocks | Inherited notes | Unresolved notes |
| --- | --- | --- | --- | --- | --- | --- |
| 7I / Introduction | 0 | 5 | 0 | 4 | 0 | 0 |
| 7I / I | 0 | 59 | 0 | 34 | 0 | 0 |
| 7I / II | 0 | 21 | 0 | 8 | 0 | 0 |
| 7I / VI | 0 | 390 | 0 | 135 | 0 | 2 |
| 7I / VII | 0 | 212 | 0 | 77 | 0 | 5 |
| 7I / VIII | 0 | 162 | 0 | 77 | 0 | 0 |
| 7I / IX | 0 | 391 | 0 | 207 | 0 | 0 |
| 7I / Catalogue | 0 | 10 | 0 | 8 | 0 | 0 |
| 7II / X | 0 | 111 | 0 | 46 | 0 | 0 |
| 7II / XI | 0 | 54 | 0 | 25 | 0 | 0 |
| 7II / XII | 0 | 58 | 0 | 22 | 0 | 0 |
| 7II / XIII | 0 | 50 | 0 | 32 | 0 | 0 |
| 7II / XIV | 0 | 90 | 0 | 57 | 0 | 0 |
| 7II / XV | 0 | 66 | 0 | 35 | 0 | 0 |
| 7II / XVI | 0 | 18 | 0 | 10 | 0 | 1 |
| 7II / XVII | 0 | 171 | 0 | 47 | 0 | 2 |
| 7II / XVIII | 0 | 459 | 0 | 107 | 0 | 0 |
| 7II / XIX | 0 | 71 | 0 | 18 | 0 | 1 |
| 7II / XX | 0 | 155 | 0 | 40 | 0 | 0 |
| 7II / XXI | 0 | 122 | 0 | 48 | 0 | 0 |
| 7II / XXII | 0 | 149 | 0 | 75 | 0 | 6 |

### EN

| Volume / exposé | Diplomatic | Corrected | Reading | Blocks | Inherited notes | Unresolved notes |
| --- | --- | --- | --- | --- | --- | --- |
| 7I / Introduction | 0 | 1 | 0 | 1 | 0 | 0 |
| 7I / I | 0 | 43 | 0 | 25 | 0 | 0 |
| 7I / II | 0 | 18 | 0 | 7 | 0 | 0 |
| 7I / VI | 0 | 390 | 0 | 135 | 0 | 2 |
| 7I / VII | 0 | 160 | 0 | 36 | 0 | 5 |
| 7I / VIII | 0 | 90 | 0 | 44 | 0 | 0 |
| 7I / IX | 0 | 236 | 0 | 134 | 59 | 0 |
| 7I / Catalogue | 0 | 10 | 0 | 8 | 0 | 0 |
| 7II / X | 0 | 67 | 0 | 35 | 0 | 0 |
| 7II / XI | 0 | 47 | 0 | 23 | 1 | 0 |
| 7II / XII | 0 | 44 | 0 | 19 | 14 | 0 |
| 7II / XIII | 0 | 34 | 0 | 17 | 13 | 0 |
| 7II / XIV | 0 | 48 | 0 | 25 | 8 | 0 |
| 7II / XV | 0 | 44 | 0 | 22 | 14 | 0 |
| 7II / XVI | 0 | 12 | 0 | 8 | 3 | 1 |
| 7II / XVII | 0 | 79 | 0 | 22 | 13 | 2 |
| 7II / XVIII | 0 | 224 | 0 | 41 | 29 | 0 |
| 7II / XIX | 0 | 23 | 0 | 11 | 10 | 1 |
| 7II / XX | 0 | 71 | 0 | 16 | 22 | 0 |
| 7II / XXI | 0 | 71 | 0 | 20 | 15 | 0 |
| 7II / XXII | 0 | 99 | 0 | 53 | 11 | 6 |

Exposé XIII is assigned to XIII, including its single source folio 82, even though that text is stored in the Exposé XII source file. Publisher-catalogue variants on folios 525–527 of volume I are assigned to Catalogue in both languages, including those stored under IX in the French source register. Exposés III–V have no separately written text in these sources and therefore are not invented as empty source components. A zero for a supplied component means it has no registered variant, not that its text is missing.

## Recorded kinds by exposé and form

Only nonzero corrected-form kind combinations are listed; the diplomatic and reading counts remain explicitly zero. The complete machine-readable table is `APPARATUS_COUNTS.tsv`.

### FR

| Volume / exposé | Recorded kind | Diplomatic | Corrected | Reading |
| --- | --- | --- | --- | --- |
| 7I / Introduction | inherited corrected-layer difference | 0 | 5 | 0 |
| 7I / I | designated-witness attribution | 0 | 8 | 0 |
| 7I / I | inherited corrected-layer difference | 0 | 10 | 0 |
| 7I / I | misprint_in_print | 0 | 2 | 0 |
| 7I / I | misprint_pass | 0 | 15 | 0 |
| 7I / I | printed misprint | 0 | 24 | 0 |
| 7I / II | designated-witness attribution | 0 | 4 | 0 |
| 7I / II | inherited corrected-layer difference | 0 | 4 | 0 |
| 7I / II | misprint_pass | 0 | 1 | 0 |
| 7I / II | printed misprint | 0 | 12 | 0 |
| 7I / VI | designated-witness attribution | 0 | 56 | 0 |
| 7I / VI | inherited corrected-layer difference | 0 | 107 | 0 |
| 7I / VI | misprint_in_print | 0 | 32 | 0 |
| 7I / VI | misprint_pass | 0 | 125 | 0 |
| 7I / VI | printed misprint | 0 | 70 | 0 |
| 7I / VII | designated-witness attribution | 0 | 42 | 0 |
| 7I / VII | editorial decision | 0 | 1 | 0 |
| 7I / VII | inherited corrected-layer difference | 0 | 29 | 0 |
| 7I / VII | misprint_in_print | 0 | 6 | 0 |
| 7I / VII | misprint_pass | 0 | 62 | 0 |
| 7I / VII | printed misprint | 0 | 72 | 0 |
| 7I / VIII | designated-witness attribution | 0 | 16 | 0 |
| 7I / VIII | inherited corrected-layer difference | 0 | 24 | 0 |
| 7I / VIII | misprint_in_print | 0 | 2 | 0 |
| 7I / VIII | misprint_pass | 0 | 49 | 0 |
| 7I / VIII | printed misprint | 0 | 71 | 0 |
| 7I / IX | designated-witness attribution | 0 | 40 | 0 |
| 7I / IX | inherited corrected-layer difference | 0 | 18 | 0 |
| 7I / IX | misprint_in_print | 0 | 20 | 0 |
| 7I / IX | misprint_pass | 0 | 202 | 0 |
| 7I / IX | printed misprint | 0 | 109 | 0 |
| 7I / IX | punctuation | 0 | 2 | 0 |
| 7I / Catalogue | misprint_pass | 0 | 10 | 0 |
| 7II / X | designated-witness attribution | 0 | 27 | 0 |
| 7II / X | inherited corrected-layer difference | 0 | 28 | 0 |
| 7II / X | misprint_in_print | 0 | 12 | 0 |
| 7II / X | misprint_pass | 0 | 4 | 0 |
| 7II / X | printed misprint | 0 | 40 | 0 |
| 7II / XI | designated-witness attribution | 0 | 4 | 0 |
| 7II / XI | inherited corrected-layer difference | 0 | 6 | 0 |
| 7II / XI | misprint_in_print | 0 | 2 | 0 |
| 7II / XI | misprint_pass | 0 | 34 | 0 |
| 7II / XI | printed misprint | 0 | 8 | 0 |
| 7II / XII | designated-witness attribution | 0 | 4 | 0 |
| 7II / XII | inherited corrected-layer difference | 0 | 2 | 0 |
| 7II / XII | misprint_in_print | 0 | 3 | 0 |
| 7II / XII | misprint_pass | 0 | 21 | 0 |
| 7II / XII | printed misprint | 0 | 28 | 0 |
| 7II / XIII | designated-witness attribution | 0 | 2 | 0 |
| 7II / XIII | inherited corrected-layer difference | 0 | 3 | 0 |
| 7II / XIII | misprint_in_print | 0 | 1 | 0 |
| 7II / XIII | misprint_pass | 0 | 28 | 0 |
| 7II / XIII | printed misprint | 0 | 16 | 0 |
| 7II / XIV | inherited corrected-layer difference | 0 | 4 | 0 |
| 7II / XIV | misprint_in_print | 0 | 3 | 0 |
| 7II / XIV | misprint_pass | 0 | 70 | 0 |
| 7II / XIV | printed misprint | 0 | 13 | 0 |
| 7II / XV | designated-witness attribution | 0 | 7 | 0 |
| 7II / XV | inherited corrected-layer difference | 0 | 17 | 0 |
| 7II / XV | misprint_in_print | 0 | 4 | 0 |
| 7II / XV | misprint_pass | 0 | 26 | 0 |
| 7II / XV | printed misprint | 0 | 12 | 0 |
| 7II / XVI | designated-witness attribution | 0 | 1 | 0 |
| 7II / XVI | inherited corrected-layer difference | 0 | 2 | 0 |
| 7II / XVI | misprint_in_print | 0 | 2 | 0 |
| 7II / XVI | misprint_pass | 0 | 6 | 0 |
| 7II / XVI | printed misprint | 0 | 7 | 0 |
| 7II / XVII | designated-witness attribution | 0 | 66 | 0 |
| 7II / XVII | inherited corrected-layer difference | 0 | 5 | 0 |
| 7II / XVII | misprint_in_print | 0 | 3 | 0 |
| 7II / XVII | misprint_pass | 0 | 60 | 0 |
| 7II / XVII | printed misprint | 0 | 37 | 0 |
| 7II / XVIII | designated-witness attribution | 0 | 135 | 0 |
| 7II / XVIII | inherited corrected-layer difference | 0 | 145 | 0 |
| 7II / XVIII | misprint_in_print | 0 | 4 | 0 |
| 7II / XVIII | misprint_pass | 0 | 28 | 0 |
| 7II / XVIII | printed misprint | 0 | 147 | 0 |
| 7II / XIX | designated-witness attribution | 0 | 6 | 0 |
| 7II / XIX | inherited corrected-layer difference | 0 | 37 | 0 |
| 7II / XIX | misprint_in_print | 0 | 1 | 0 |
| 7II / XIX | misprint_pass | 0 | 5 | 0 |
| 7II / XIX | printed misprint | 0 | 22 | 0 |
| 7II / XX | designated-witness attribution | 0 | 48 | 0 |
| 7II / XX | font | 0 | 2 | 0 |
| 7II / XX | inherited corrected-layer difference | 0 | 39 | 0 |
| 7II / XX | misprint_in_print | 0 | 1 | 0 |
| 7II / XX | misprint_pass | 0 | 1 | 0 |
| 7II / XX | printed misprint | 0 | 64 | 0 |
| 7II / XXI | designated-witness attribution | 0 | 29 | 0 |
| 7II / XXI | inherited corrected-layer difference | 0 | 33 | 0 |
| 7II / XXI | misprint_corrected | 0 | 2 | 0 |
| 7II / XXI | misprint_in_print | 0 | 9 | 0 |
| 7II / XXI | misprint_pass | 0 | 12 | 0 |
| 7II / XXI | printed misprint | 0 | 37 | 0 |
| 7II / XXII | designated-witness attribution | 0 | 34 | 0 |
| 7II / XXII | extra | 0 | 1 | 0 |
| 7II / XXII | formula | 0 | 2 | 0 |
| 7II / XXII | inherited corrected-layer difference | 0 | 13 | 0 |
| 7II / XXII | misprint_in_print | 0 | 37 | 0 |
| 7II / XXII | misprint_pass | 0 | 8 | 0 |
| 7II / XXII | printed misprint | 0 | 54 | 0 |

### EN

| Volume / exposé | Recorded kind | Diplomatic | Corrected | Reading |
| --- | --- | --- | --- | --- |
| 7I / Introduction | verified English correction | 0 | 1 | 0 |
| 7I / I | mathematical reading | 0 | 29 | 0 |
| 7I / I | misprint_pass | 0 | 2 | 0 |
| 7I / I | prose, reference or bibliography reconstruction | 0 | 7 | 0 |
| 7I / I | reviewed formula or formula-context reconstruction | 0 | 5 | 0 |
| 7I / II | explicit editorial body or reading decision | 0 | 4 | 0 |
| 7I / II | mathematical reading | 0 | 7 | 0 |
| 7I / II | prose, reference or bibliography reconstruction | 0 | 6 | 0 |
| 7I / II | reviewed formula or formula-context reconstruction | 0 | 1 | 0 |
| 7I / VI | designated-witness attribution | 0 | 56 | 0 |
| 7I / VI | inherited corrected-layer difference | 0 | 107 | 0 |
| 7I / VI | misprint_in_print | 0 | 32 | 0 |
| 7I / VI | misprint_pass | 0 | 125 | 0 |
| 7I / VI | printed misprint | 0 | 70 | 0 |
| 7I / VII | explicit editorial body or reading decision | 0 | 2 | 0 |
| 7I / VII | mathematical reading | 0 | 69 | 0 |
| 7I / VII | misprint_pass | 0 | 10 | 0 |
| 7I / VII | prose, reference or bibliography reconstruction | 0 | 19 | 0 |
| 7I / VII | reviewed formula or formula-context reconstruction | 0 | 58 | 0 |
| 7I / VII | reviewed formula or formula-context reconstruction; explicit editorial body or reading decision | 0 | 1 | 0 |
| 7I / VII | verified final printed witness | 0 | 1 | 0 |
| 7I / VIII | explicit editorial body or reading decision | 0 | 3 | 0 |
| 7I / VIII | font, accent, scope or equation-tag reconstruction | 0 | 3 | 0 |
| 7I / VIII | mathematical reading | 0 | 48 | 0 |
| 7I / VIII | misprint_pass | 0 | 3 | 0 |
| 7I / VIII | prose, reference or bibliography reconstruction | 0 | 14 | 0 |
| 7I / VIII | reviewed formula or formula-context reconstruction | 0 | 19 | 0 |
| 7I / IX | explicit editorial body or reading decision | 0 | 3 | 0 |
| 7I / IX | font, accent, scope or equation-tag reconstruction | 0 | 8 | 0 |
| 7I / IX | mathematical reading | 0 | 123 | 0 |
| 7I / IX | mathematical reading; explicit editorial body or reading decision | 0 | 1 | 0 |
| 7I / IX | misprint_pass | 0 | 25 | 0 |
| 7I / IX | prose, reference or bibliography reconstruction | 0 | 41 | 0 |
| 7I / IX | reviewed formula or formula-context reconstruction | 0 | 28 | 0 |
| 7I / IX | verified English correction | 0 | 1 | 0 |
| 7I / IX | verified final printed witness | 0 | 6 | 0 |
| 7I / Catalogue | misprint_pass | 0 | 10 | 0 |
| 7II / X | explicit editorial body or reading decision | 0 | 3 | 0 |
| 7II / X | font, accent, scope or equation-tag reconstruction | 0 | 3 | 0 |
| 7II / X | mathematical reading | 0 | 36 | 0 |
| 7II / X | mathematical reading; explicit editorial body or reading decision | 0 | 1 | 0 |
| 7II / X | prose, reference or bibliography reconstruction | 0 | 3 | 0 |
| 7II / X | reviewed formula or formula-context reconstruction | 0 | 21 | 0 |
| 7II / XI | font, accent, scope or equation-tag reconstruction | 0 | 3 | 0 |
| 7II / XI | mathematical reading | 0 | 25 | 0 |
| 7II / XI | misprint_pass | 0 | 9 | 0 |
| 7II / XI | reviewed formula or formula-context reconstruction | 0 | 10 | 0 |
| 7II / XII | font, accent, scope or equation-tag reconstruction | 0 | 1 | 0 |
| 7II / XII | mathematical reading | 0 | 27 | 0 |
| 7II / XII | misprint_pass | 0 | 3 | 0 |
| 7II / XII | prose, reference or bibliography reconstruction | 0 | 4 | 0 |
| 7II / XII | reviewed formula or formula-context reconstruction | 0 | 9 | 0 |
| 7II / XIII | mathematical reading | 0 | 14 | 0 |
| 7II / XIII | misprint_pass | 0 | 6 | 0 |
| 7II / XIII | prose, reference or bibliography reconstruction | 0 | 8 | 0 |
| 7II / XIII | reviewed formula or formula-context reconstruction | 0 | 4 | 0 |
| 7II / XIII | verified final printed witness | 0 | 2 | 0 |
| 7II / XIV | font, accent, scope or equation-tag reconstruction | 0 | 1 | 0 |
| 7II / XIV | mathematical reading | 0 | 22 | 0 |
| 7II / XIV | misprint_pass | 0 | 9 | 0 |
| 7II / XIV | prose, reference or bibliography reconstruction | 0 | 4 | 0 |
| 7II / XIV | reviewed formula or formula-context reconstruction | 0 | 12 | 0 |
| 7II / XV | font, accent, scope or equation-tag reconstruction | 0 | 1 | 0 |
| 7II / XV | mathematical reading | 0 | 18 | 0 |
| 7II / XV | misprint_pass | 0 | 3 | 0 |
| 7II / XV | prose, reference or bibliography reconstruction | 0 | 3 | 0 |
| 7II / XV | reviewed formula or formula-context reconstruction | 0 | 19 | 0 |
| 7II / XVI | font, accent, scope or equation-tag reconstruction | 0 | 1 | 0 |
| 7II / XVI | mathematical reading | 0 | 10 | 0 |
| 7II / XVI | reviewed formula or formula-context reconstruction | 0 | 1 | 0 |
| 7II / XVII | font, accent, scope or equation-tag reconstruction | 0 | 5 | 0 |
| 7II / XVII | mathematical reading | 0 | 36 | 0 |
| 7II / XVII | misprint_pass | 0 | 3 | 0 |
| 7II / XVII | prose, reference or bibliography reconstruction | 0 | 2 | 0 |
| 7II / XVII | reviewed formula or formula-context reconstruction | 0 | 33 | 0 |
| 7II / XVIII | font, accent, scope or equation-tag reconstruction | 0 | 14 | 0 |
| 7II / XVIII | mathematical reading | 0 | 107 | 0 |
| 7II / XVIII | misprint_pass | 0 | 3 | 0 |
| 7II / XVIII | prose, reference or bibliography reconstruction | 0 | 11 | 0 |
| 7II / XVIII | reviewed formula or formula-context reconstruction | 0 | 84 | 0 |
| 7II / XVIII | verified final printed witness | 0 | 5 | 0 |
| 7II / XIX | font, accent, scope or equation-tag reconstruction | 0 | 2 | 0 |
| 7II / XIX | mathematical reading | 0 | 7 | 0 |
| 7II / XIX | misprint_pass | 0 | 1 | 0 |
| 7II / XIX | prose, reference or bibliography reconstruction | 0 | 10 | 0 |
| 7II / XIX | reviewed formula or formula-context reconstruction | 0 | 3 | 0 |
| 7II / XX | explicit editorial body or reading decision | 0 | 2 | 0 |
| 7II / XX | font, accent, scope or equation-tag reconstruction | 0 | 3 | 0 |
| 7II / XX | mathematical reading | 0 | 49 | 0 |
| 7II / XX | prose, reference or bibliography reconstruction | 0 | 4 | 0 |
| 7II / XX | reviewed formula or formula-context reconstruction | 0 | 13 | 0 |
| 7II / XXI | mathematical reading | 0 | 36 | 0 |
| 7II / XXI | misprint_pass | 0 | 3 | 0 |
| 7II / XXI | prose, reference or bibliography reconstruction | 0 | 6 | 0 |
| 7II / XXI | reviewed formula or formula-context reconstruction | 0 | 26 | 0 |
| 7II / XXII | font, accent, scope or equation-tag reconstruction | 0 | 12 | 0 |
| 7II / XXII | mathematical reading | 0 | 54 | 0 |
| 7II / XXII | misprint_pass | 0 | 3 | 0 |
| 7II / XXII | prose, reference or bibliography reconstruction | 0 | 11 | 0 |
| 7II / XXII | reviewed formula or formula-context reconstruction | 0 | 14 | 0 |
| 7II / XXII | verified final printed witness | 0 | 5 | 0 |

## Separate editorial notes

Inherited English editorial notes preserve the release’s existing editorial explanations. They are not authorial footnotes and are not additional before/after variants. The retained or unresolved notes are the explicitly selected questions in `editorial_decisions.json`; each is counted once in each language, even when its stated scope includes several folios. Its first explicit folio determines the exposé subtotal.

| Identifier | Volume / exposé | Source folio / scope | Recorded status |
| --- | --- | --- | --- |
| ED-G27-x-hat | 7I / VI | 7I:123 | needs the scan |
| ED-G27-missing-reference | 7I / VI | 7I:128 | retained; authorial reference unresolved |
| ED-G32-run-in-headings | 7I / VII | 7I:163,165 (and analogous numbered headings) | needs the scan |
| ED-G36-E-or-X | 7I / VII | 7I:180 | retained; no determinate emendation |
| ED-G36-psi-footnote | 7I / VII | 7I:180 | needs the scan |
| ED-G37-duplicate-number | 7I / VII | 7I:183 | retained; intended numbering unresolved |
| ED-G38-speck | 7II / XVI | 7II:202 | needs the scan |
| ED-G41-exton-sion | 7I / VII | 7I:195 | needs the scan |
| ED-G45-mathematical-repair | 7II / XVII | 7II:237 | retained; proposed mathematical replacement unavailable |
| ED-G48-inner-underlines | 7II / XVII | 7II:248 and other internal commas | needs the scan |
| ED-G58-comma | 7II / XIX | 7II:332 | needs the scan |
| ED-G63-miracle | 7II / XXII | 7II:416 | needs the scan |
| ED-G64-quotient | 7II / XXII | 7II:423 | needs the scan |
| ED-G64-subset-stroke | 7II / XXII | 7II:424 | needs the scan |
| ED-G64-Delta-Lambda | 7II / XXII | 7II:424–429 | needs the scan |
| ED-G67-Dwork-psi | 7II / XXII | 7II:436–438 | needs the scan |
| ED-G73-statement-underlines | 7II / XXII | 7II:403,405 and similar statements | needs the scan |

Authorial notes, references, bibliography entries, and the publisher catalogue are not critical-apparatus entries and are outside these counts.

## Reproduction and validation

Run `python build/edition_report.py` after rebuilding both language editions. The script reads the final registers, masters, reader selectors, page-marker table, and editorial-note registers. It verifies unique entry identifiers, nonidentical readings, one master target per entry, corrected-only guards, exact master-to-reader projections, and a stable input snapshot. `APPARATUS_COUNTS.json` records every subtotal, these validation results, and SHA-256 hashes of the exact inputs used. The report must be rerun if a source register or reader is rebuilt.
