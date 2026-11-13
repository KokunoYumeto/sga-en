# Independent final verification

Run these commands after the final assembly, record export, glossary count, and completed PDF compilations:

```bash
python3 work/verification/verify_arcata_own.py
python3 work/verification/verify_final.py --strict
```

The first command verifies all 44 Arcata own findings in both languages. It checks actual variant occurrences and aliases, recorded operation targets, complete restored bibliography and contents, and the page-scoped literal witnesses in `arcata_own_witnesses.json`. It includes the additional witnesses on p. 55. It exits nonzero if any of its 88 checks is unresolved.

The second command independently parses the flattened readers and inspects the eight PDFs. It does not import the assembly's TeX parser or treat the assembly's asserted counts as verification. Its strict exit status is zero only when every check passes and no required input is pending.

Without `--strict`, the same script writes a preliminary report and exits zero even when the report contains failures or pending outputs. The preliminary mode is intended for use during an incomplete build. A PDF whose bytes or source do not agree with its last completed compilation record is marked pending rather than inspected as a final output.

## Checks

- The four TeX files in each language are identical after replacing only the literal values of `EditionMode` and `EditionIsMaster`.
- Every reader contains the complete prepared body and apparatus verbatim and has no external TeX input/include command.
- All 314 original-page markers occur once and in the required order, III–IV and 1–312. The page-table line numbers and marker contexts agree with the actual annotated masters.
- Variant occurrence identities are unique and sequential: 312 French and 218 English. Every occurrence has exactly one TeX apparatus entry, distinct printed/corrected readings, a valid decision, reasoned variant metadata, and matching preparation and component-inventory records.
- The French occurrences reconcile with all rows of the misprint register.
- The PDF name trees have exactly the 314 expected original-page destinations and exactly the apparatus destinations selected by the form: zero in diplomatic/reading PDFs, 312 in French corrected/master PDFs, and 218 in English corrected/master PDFs. Destinations resolve to existing pages, original-page destinations do not run backward, and internal links resolve.
- Current PDF/TeX hashes match the final compilation record. A timestamp fallback is documented if hashes are unavailable. Final logs have no errors, missing glyphs, unavailable fonts, undefined references, duplicate destinations, or outstanding cross-reference rerun notices.
- All 1,247 Sol decisions and all own findings have one coverage row per language. These rows preserve the independent allocation checks and distinguish actual repairs, existing correct English, rejected changes, and explicit language non-applicability. The combined table is an inventory of those checks, not a new claim to have repeated the entire visual scan audit.
- Arcata own-coverage and glossary input hashes remain current, and the prepared bodies postdate the component inputs.
- Distributable TeX, records, scripts, sanitized logs, PDF text, and PDF metadata are checked for recognized absolute local paths and email addresses. Raw runtime `.log`, `.aux`, and `.out` files are excluded. Potential private values are hashed and redacted in the audit output itself.

For an additional staging directory, append `--privacy-root` with its project-relative path. This option may be repeated. Staged PDFs identical to already inspected PDF hashes do not need to be extracted again.

Overfull/underfull box counts, font counts, text-extraction replacement characters, and nonblocking compile warnings are reported. They do not substitute for the separate rendered-page review. The informational bookmark alternative for the title's 4½ is permitted because it changes only PDF bookmark text.

## Outputs

| File | Contents |
|---|---|
| `FINAL_VERIFICATION.json` | Strict/preliminary result, reader hashes and PDF statistics, and every gate result |
| `FINAL_STRUCTURE_CHECKS.tsv` | One row per gate, with expected/actual values and a pass/fail/pending status |
| `FINAL_VARIANT_VALIDATION.tsv` | The 530 French/English variant occurrences and their decision/metadata checks |
| `FINAL_PAGE_MARKERS.tsv` | Each original-page marker's TeX line and PDF destination in each reader |
| `FINAL_FIX_COVERAGE.tsv` | Combined bilingual Sol and own-finding coverage with source evidence |
| `FINAL_PRIVACY_CHECK.tsv` | Any privacy hits, with locations, redacted contexts, and value hashes |
| `arcata_own_fix_coverage.json` / `.tsv` | Detailed results of all 88 Arcata own-finding language checks |
| `ARCATA_OWN_COVERAGE_STATUS.json` | Arcata coverage totals and checked component hashes |

The scripts are read-only with respect to the edition. They write only these verification records.
