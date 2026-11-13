# Final packaging and reproducibility support

The final isolated source gate passed. All 23 compared artifacts match byte for byte: eight reader/master TeX files, two frozen English sources, both French source branches and their prepared bodies, the complete final glossary and its supporting tables. The empty-project run verified all 270 manifest members and executed 24 stages through the five complete source-to-reader reconstruction chains. Its 29 source-stage implementations still match the final script hashes. `ISOLATED_SOURCE_REBUILD.json` and `FINAL_SOURCE_REPRODUCTION.json` contain the same passing result; `ISOLATED_SOURCE_REBUILD.md` explains the scope.

## Exact reproduction evidence

- `FR_PORTABLE_REPRODUCTION.json` and `EN_PORTABLE_REPRODUCTION.json`, under their change-contribution directories, each verify all eleven compact-layout outputs byte for byte.
- The French source change proof was refreshed after the final preparation/resolution integration. The English corrected source and its 398 common operations remain unchanged.
- The isolated run reproduced the final glossary: 320 rows, 131 body phrase families, 212 observed body forms, 108 paired index entries and 65 families with multiple forms.
- The independent source, credits, glossary/notes and master audits passed. The folio 248 INITEX witness was replayed with all ten observations present.
- The initial source comparison exposed old English offsets in 108 paired-index records and two pre-repair terminology forms. Both inventory families were regenerated against the frozen English source. `INVENTORY_FINAL_SOURCE_REFRESH.json` gives every prior/final hash, exact changed field and reconstructable line operation, with six corresponding patches. Reader and formula bytes were unchanged.
- Three unused temporary implementation copies were captured while the compact-layout check was running. Their hashes and exclusion from executed stage/module inputs are explicit in the isolated report; the copies were removed. Source seeding and final packaging exclude temporary check-directory prefixes.

## Package inventory

`inventory_records.py` produces `FINAL_RECORD_INVENTORY.tsv` and `.json`, using the actual final packaging policy. It covers all eight standalone TeX/PDF pairs, all sixteen screened compiler logs/summaries, required root tables and citation aliases, prepared branches and variant catalogues, build and contribution scripts, scan evidence, complete change patches, the attached prompt and the rebuild entry points. It preserves the original `work/` layout so sibling imports and explicit source citations resolve.

The tiny `folio248_token_boundary_probe.log` is retained as a screened proof transcript. Ordinary compiler scratch directories, console dumps, compiler intermediates, caches, temporary check directories, downloaded runtime packages and machine-local environment files are excluded. The three original archives and extracted `work/sources/` tree remain external inputs; their original private manifest fields are not republished.

The final packager independently writes and verifies each ZIP's `MANIFEST.tsv`. These package manifests establish the final bytes after staging; the supporting inventory is a snapshot of the package inputs and omits only its own two self-referential hashes.

## Privacy checks

`audit_packages.py` screens full textual ZIP members, extracted PDF text and plain PDF metadata strings. It fails on detected private values, unsafe member names, prohibited original inputs, raw execution artifacts or failed PDF extraction. Findings contain category, member, line, count and hashes, without copying private values.

The scanner preserves mathematical expressions such as `f:\mathcal{C}\to\mathcal{D}`. Its only declared exceptions are exact standard interpreter shebangs and syntactically declared regular-expression literals. All four mathematical regression cases remain intact, and all three constructed private-value fixtures are detected.

The corrected checkpoint 2 and the later checkpoint 3–6 reports each show zero private matches and zero raw compiler artifacts. Current public compilation logs and summaries also have zero private matches, as recorded in `PUBLIC_LOG_PRIVACY_AUDIT.json`. Final ZIPs must be screened after the last staging operation; an earlier checkpoint scan does not establish a later archive's hash or contents.

## Rebuild requirements and limits

`rebuild.py` and `REBUILD.md` give a 35-stage complete build. Its source pipeline verifies original manifests, replays the reviewed inputs, prepares and resolves both languages, regenerates glossary additions, audits the exact source layers, reconstructs all final reader chains, compiles all eight documents, finalizes records, packages the outputs and runs final privacy checks. The French resolver is invoked once by French preparation. English preparation performs its own audit/apply/audit sequence.

The verified environment has Python, Pillow, GNU `patch`, Poppler `pdftotext` and `pdfinfo`, `pdftex`, `pdflatex`, `kpsewhich`, and all 24 explicitly checked TeX classes/packages. The active TeX environment may be loaded from a user-supplied local file; the published records require a normal complete TeX installation and contain no machine-specific bootstrap or downloaded runtime tree.

The isolated gate reproduced source bytes and reconstruction evidence. It stopped before PDF compilation. The eight final PDFs were compiled separately from those identical sources. Byte-identical PDF regeneration also depends on matching the TeX engine, package/font versions and fixed build date. The final privacy report is generated after packaging and records archive hashes; it cannot be inserted into the same hashed archive without changing that archive's hash.

The final original-source and final-reader hashes are explicit in the JSON proofs. Original CRLF bytes inside change-table cells are preserved; read TSV files with `newline=''`.
