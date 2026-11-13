# Rebuild support

Run commands from the unpacked project directory, or invoke a script by its path; the rebuild driver sets the working directory for its child commands. Python scripts are invoked with `python3`.

## Complete rebuild

Place the four supplied original ZIP files in `upload`, preserve the files listed in `scripts/rebuild_inputs.json`, then run:

```sh
python3 scripts/rebuild_all.py --dry-run
python3 scripts/rebuild_all.py
```

The default sequence verifies and extracts the original inputs, reconstructs all 22 annotated components, checks their source-operation coverage, regenerates the bilingual glossary, assembles the eight flattened TeX books, compiles each book three times, exports the registers and complete textual differences, then runs the independent strict verification. A nonzero exit stops the sequence. The final report is `work/reproducibility/REBUILD_RESULT.json`; individual command logs are sanitized before retention.

Use `--stage inputs`, `components`, `glossary`, `assemble`, `compile`, `export`, or `verify` to rerun one stage. A successful single stage is explicitly reported as a partial rebuild. `--passes 2` is permitted for the PDF stage; three passes are the default to settle references, bookmarks, and margin positions. Repeated `--privacy-root` arguments add staged package directories to the final privacy inspection.

The independent final gate is:

```sh
python3 work/verification/verify_arcata_own.py
python3 work/verification/verify_final.py --strict
```

## Verified input extraction

```sh
python3 scripts/unpack_inputs.py --verify-only
python3 scripts/unpack_inputs.py
```

The four whole-archive hashes are fixed in `scripts/unpack_inputs.py`. Extraction also checks the exact ZIP/manifest inventories, all 1,775 payload sizes and SHA-256 hashes, duplicate and case-colliding names, forbidden path forms, and nonregular or encrypted members. All payload verification finishes before installation. Existing identical files are preserved; a divergent destination stops extraction without overwriting it. Root manifests are replaced by privacy-safe copies in `source/manifests`; their original source-location column is excluded. Unrelated existing files are not removed.

The original payloads total 75,865,260 bytes. The archive verification report records only archive names, ZIP-relative paths, content roles, sizes, and hashes. Original archives and raw upstream metadata remain reference inputs; only the independently privacy-checked package is intended for distribution.

## Required software and runtime behavior

The recorded Python runtime is 3.12.14. The scripts require Python 3.10 or newer. All Python build modules use the standard library except the independent PDF inspection, which uses PyMuPDF 1.26.6, pinned in `requirements-rebuild.txt`. Rendering tools used during the historical visual audit are not needed to reconstruct the TeX sources.

PDF compilation requires the TeX commands `pdflatex`, `pdftex`, and `kpsewhich`, with the packages and fonts used by the inlined Miller style. A complete TeX Live installation uses its normal format and font maps. If no `pdflatex.fmt` is found, `scripts/compile_reader.py` initializes a local format in `work/tex_runtime`, uses the discoverable TeX distribution trees, and creates a local font map from the installed Latin Modern, Computer Modern, Euler, AMS symbols, Ralph Smith script, and Xy-pic map files. The helper does not download or install packages and does not modify the system TeX configuration.

The preamble preserves the normal `calligra` font when its `callig15.tfm` metric is available. If the metric is absent, its trailing operator letters use italics; the script H/E/T still distinguish sheaf Hom/Ext/Tor. The normal `stmaryrd` package is used when available; otherwise two close brackets form the double-bracket sign. These two documented typography fallbacks do not change mathematical tokens or the selected variant reading. Their focused compile and visual evidence is retained in `work/tex_infrastructure_test` and summarized in `work/common/font_fallbacks.json`.

Automatic PDF destinations use a global hyperref counter so repeated local equation numbers do not collide. Explicit original-page and apparatus destinations retain their named identifiers. The strict verifier checks duplicate destinations, unresolved references, every original-page marker, and every apparatus occurrence.

Source reconstruction is deterministic. PDF bytes can vary with the TeX distribution, installed fonts, engine metadata, and build time; the exact delivered PDFs are identified by the package manifests and compile reports.

## Frozen inputs, generated files, and excluded trials

`scripts/rebuild_inputs.json` lists all 54 frozen reviewed input files and the reusable code modules. Keep the decision/page/variant ledgers, exact patch data, English semantic witnesses, manually restored contents and bibliographies, original general contents, and the reviewed English Ariadne translation. The latter is `work/arcata/ariane_en_reviewed.tex`; it supplies material absent from the original English release. The four opening components rebuild through `scripts/rebuild_opening.py` without adding audit rows.

Do not rerun append-only `record_*` or `audit_*` scripts, nor the historical `finish_part*`, `close_part*`, or `close_citations_and_coverage.py` helpers. Their reviewed results are already materialized in the frozen inputs. The explicitly invoked `finalize_arcata_records.py` and `complete_alignment.py` are idempotent finalizers.

Retain the final TeX/PDF books; exported record tables and complete diffs; glossary tables and attestations; final independent verification; source-operation coverage; sanitized compile reports/logs; and focused formatter validation and visual evidence. Historical audit scripts and scan crops remain provenance evidence even when they are not rebuild dependencies. Local format caches, raw TeX logs, auxiliary files, bytecode caches, and temporary trial trees are operational artifacts. The final packaging and checkpoint-reconciliation maps give the specific disposition of each such file.

## Reproducibility checks already performed

```sh
python3 scripts/check_unpack_inputs.py
python3 scripts/check_rebuild_components.py
```

The extraction check passed all original payloads, a repeated extraction, conflict refusal, tamper detection, and the path/member defenses. Its report is `work/reproducibility/UNPACK_VALIDATION.json`.

Two isolated component replays copied only the declared code and frozen inputs, used the verified source payloads, and rebuilt every component. All 22 component hashes matched the reviewed originals on both passes, and all 54 frozen input hashes remained unchanged. The trial trees were removed. `work/reproducibility/COMPONENT_REPLAY_VALIDATION.json` retains the exact comparison hashes; the four opening-file replay hashes are also recorded separately. These tests establish reconstruction and idempotence; the recorded primary visual audit establishes fidelity to the scans.
