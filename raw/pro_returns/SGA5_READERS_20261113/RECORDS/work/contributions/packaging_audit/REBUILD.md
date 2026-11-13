# Rebuilding the SGA 5 readers

The records package preserves the original project layout. Run commands from the directory containing `work/`; keep contribution modules beside their sibling scripts because several imports and reviewed data files use that relationship. The three original input archives remain external inputs and are excluded from the published records package because their original records can contain machine paths.

Place the original `SGA5_FR.zip`, `SGA5_EN.zip`, and `SGA5_SCANS.zip` in `upload/`. The attached prompt is retained at its recorded path under `upload/`; the independent credit audit checks the exact requested rights wording there.

## Read-only preflight

```sh
python work/contributions/packaging_audit/rebuild.py --mode plan
```

The default mode reads each original ZIP's manifest and verifies every listed member's byte length and SHA-256. It also checks existing extracted originals without changing them, inventories required scripts and reviewed inputs, and writes the ordered plan under `work/contributions/packaging_audit/rebuild_outputs/`. It does not run a builder or compiler. The source-manifest `source_path` fields are never copied into the public report.

ZIP extraction rejects duplicate names, absolute/traversing member names, and symbolic links. An existing original source that differs from its archive causes an error; the driver does not overwrite it.

## Complete rebuild

```sh
python work/contributions/packaging_audit/rebuild.py --mode build
```

The driver extracts missing originals under `work/sources/`, verifies dependencies, regenerates the readers and records, compiles all six readers and both annotated masters, invokes the final metadata and packaging scripts, and screens the resulting three archives. Each subprocess has a screened JSON step report. A failed command, audit result, occurrence count, or final privacy check stops the run.

`--checkpoints` creates a local checkpoint ZIP after each of the six ordinary readers compiles. Uploading checkpoints to a persistent destination is performed by the surrounding delivery workflow; this command does not claim to upload them. `--stop-after STAGE_ID` supports an explicitly partial run, and the report then records that the full rebuild was not completed.

## Dependencies

Use Python 3.10 or later, Pillow for scan-evidence crops, GNU `patch` for independent change-log replay, and Poppler `pdftotext` and `pdfinfo` for PDF privacy checks and authoritative page counts. The books compile with pdfLaTeX and standard TeX Live packages; `pdftex` also replays the minimal INITEX token witness. The preflight checks `article`, T1/UTF-8 support, English and French babel, Latin Modern, geometry, microtype, AMS packages, mathtools, mathrsfs, enumitem, amsthm, tikz-cd, graphicx, hyperref, ulem, xcolor, marginnote, fvextra, xparse, and needspace.

The build uses the active TeX environment. A regenerated local environment can be loaded explicitly:

```sh
python work/contributions/packaging_audit/rebuild.py --mode build --tex-env work/toolchain/env.sh
```

The example environment file is optional user-supplied local runtime state and is excluded from publication. A complete standard TeX Live installation can be used directly. The driver does not install software or download dependencies.

## Dependency order

1. Verify the three input archives and all manifest members.
2. Reproduce the source-record audit, open-item decisions, unresolved notes, and the 32 scan-decision outputs.
3. Prepare the French source branches and annotated master. French preparation owns its exact source resolver; the driver does not invoke that resolver a second time on its already resolved ledger.
4. Prepare the English candidates and final branches. This uses the French prepared bodies and the reviewed manual prose catalogue.
5. Extract bilingual index pairs and the terminology inventory, then generate English alignment, the reviewed glossary additions and coordinated-phrase evidence, the complete glossary, and the per-record port audit. Alignment needs the index pairs; the glossary needs both inventories and the regenerated additions.
6. Prepare the English annotated master. Its builder runs the independent audit, applies its exact source-resolution metadata, and audits again.
7. Assemble the French and English reader wrappers, including front matter, generated contents, folio display, apparatus, and recorded wrapper-only editorial extractions.
8. Run the complete glossary/unresolved-note audit, French fix inheritance, the minimal folio 248 INITEX token probe, and both independent master/credit audits.
9. Rebuild the complete French and English source change logs, then extend them through body extraction, representation, and final reader assembly.
10. Compile the six readers and both masters, with the compiler's fixed date environment. Produce final counts, README, build summary, package manifests, and the three final ZIPs.
11. Screen the final archives, including all text members and extracted PDF text, and fail on private values or raw execution artifacts.

## Reviewed inputs that must remain included

The reproducible program replays recorded editorial judgments; it does not recreate those judgments by inference. Include the two credited front-matter fragments, `manual_prose_variants.json` with its 43 reviewed pairs, both `EN_PROJECTION_REVIEW_DECIDED` files, and the attached task prompt. Include the scan-decision script and its exact occurrence coordinates, plus the decision catalogues and evidence reports.

`build_manual_prose.py` is a historical extraction helper that reads an existing English flat source. It is not run during this rebuild because replacing the reviewed manual catalogue with a fresh extraction would create a dependency cycle and could discard its reviewed decisions. The fixed catalogue is an explicit input.

Keep all build modules and their sibling helpers under their existing `work/build/scripts/` and `work/contributions/` paths. The original source archives and `work/sources/` tree are supplied separately and are never copied into a final reader/records ZIP. Include the `.patch` files; their omission would remove independent byte-replay artifacts referenced by the change-log reports.

Retain `validation_fr/folio248_token_boundary_probe.tex` and `folio248_probe_input.json` as reviewed proof inputs. The driver regenerates their tiny `.log` witness with `run_token_probe.py` before the independent French audit. That screened INITEX log is retained as evidence: it loads no package tree and records the ten explicit token observations. It does not belong to the excluded ordinary compiler scratch directories.

## Isolated source reproduction

The following additional gate starts an empty isolated project using only Python implementations, the declared reviewed inputs, and the three original archives:

```sh
python work/contributions/packaging_audit/verify_source_rebuild.py
```

It runs the source pipeline through complete reader change-log reconstruction, then compares all eight reader/master TeX files, both frozen English branches, the two French source branches and their prepared bodies, and the glossary tables/evidence against the frozen delivery outputs. The report records every seed input and compared artifact by bytes and SHA-256. No prepared source, reader, glossary output, previous audit report or compile transcript is seeded. A nonempty target is rejected; retain an earlier run and choose a new relative `--target` for another attempt.

`verify_portable_changes.py` separately runs both change-table utilities in their documented compact layouts and checks all eleven output artifacts for each language byte for byte. These gates reproduce source bytes and reconstruction evidence; the separate compilation stages produce the PDFs.

## Exactness and limits

The source change tables preserve complete UTF-8 before/after strings and every CRLF/LF difference. Read them with `csv.DictReader` on a file opened using `newline=''`; ordinary text newline conversion would alter the original bytes in quoted cells. The written tables and unified patches independently reconstruct their recorded targets.

The driver checks the substantive audit result fields even where an audit script reports a false result without returning a failing process status. The per-step records establish which stages actually ran. A saved plan or a successful preflight is not reported as a completed rebuild.

Source-byte reproduction and PDF reproduction are reported separately. Identical PDF bytes require the same TeX engine, packages, fonts, and fixed build date; a different standard TeX Live may produce different pagination or warning counts while compiling the same standalone reader source. The final package retains the actual build's compile summaries and screened complete logs.

The final post-package privacy report contains the finished archive hashes and is generated after packaging. It cannot be included inside the very archive whose hash it records without changing that hash. The scanner and earlier package/checkpoint audit evidence remain in the records, while the final archive audit accompanies the delivery verification.

## Privacy checks

```sh
python work/contributions/packaging_audit/audit_packages.py deliverables/SGA5_READERS_FR.zip deliverables/SGA5_READERS_EN.zip deliverables/SGA5_READERS_RECORDS.zip --report-stem FINAL_PACKAGE_PRIVACY
```

The scanner examines ZIP text members, PDF extracted text, and plain PDF metadata strings. It excludes only exact standard interpreter shebangs and explicitly declared regular-expression literals containing regex syntax. A bare letter-colon-backslash does not establish a Windows path: expressions such as `f:\mathcal C` are preserved. Matches are reported by member, category, line, count, and hash; private matched values are not copied into the report.

Exclude raw compile/check directories, console/stdout dumps, compiler intermediates, caches, temporary runtime checks, downloaded runtime packages, original source archives, and the extracted-originals tree. Retain screened public compile logs and structured summaries. The scanner exits unsuccessfully when privacy findings, unsafe member names, raw execution artifacts, or PDF extraction failures remain.
