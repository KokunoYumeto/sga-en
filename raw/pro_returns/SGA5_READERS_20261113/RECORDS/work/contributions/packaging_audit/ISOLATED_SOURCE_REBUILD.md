# Isolated SGA 5 source rebuild

**Passed.** The source pipeline ran in an empty separate project through complete reader change-log reconstruction. PDF compilation was outside this isolated source-only run; the final delivery retains its separately verified compiler outputs.

## Inputs and executed scope

- All three original archives and all 270 manifest members were checked by bytes and SHA-256.
- Only Python implementations, the declared reviewed inputs and original archives seeded the project. No prepared bodies, reader TeX, glossary outputs, previous audit reports or compiler transcripts were copied.
- The run regenerated scan decisions, French and English branches, exact source metadata, wrappers, glossary evidence, independent audits and all five source-to-final-reader reconstruction chains.
- The folio 248 INITEX probe was executed again and all ten token observations passed.
- The source pipeline stopped after `complete_reader_changes`; it did not run the later eight PDF compilations or package the final archives.

## Exact comparisons

| Artifact | Bytes | Exact match |
|---|---:|---|
| `deliverables/FR/SGA5_FR_diplomatique.tex` | 1535298 | yes |
| `deliverables/FR/SGA5_FR_corrige_apparat.tex` | 1535298 | yes |
| `deliverables/FR/SGA5_FR_texte_de_lecture.tex` | 1535298 | yes |
| `deliverables/FR/SGA5_FR_master_annotated.tex` | 1535306 | yes |
| `deliverables/EN/SGA5_EN_diplomatic.tex` | 1397345 | yes |
| `deliverables/EN/SGA5_EN_corrected_apparatus.tex` | 1397345 | yes |
| `deliverables/EN/SGA5_EN_reading.tex` | 1397345 | yes |
| `deliverables/EN/SGA5_EN_master_annotated.tex` | 1397353 | yes |
| `work/contributions/english/EN_corrected_flat.tex` | 815614 | yes |
| `work/contributions/english/EN_diplomatic_flat.tex` | 818879 | yes |
| `work/build/prepared/FR_current_source.tex` | 883484 | yes |
| `work/build/prepared/FR_diplomatic_source.tex` | 883893 | yes |
| `work/build/prepared/FR_corrected_body.tex` | 884314 | yes |
| `work/build/prepared/FR_diplomatic_body.tex` | 884705 | yes |
| `work/contributions/english/GLOSSARY_SGA5_FR_EN.tsv` | 109688 | yes |
| `work/contributions/english/GLOSSARY_INCONSISTENCIES.md` | 30038 | yes |
| `work/contributions/english/GLOSSARY_FAMILIES.json` | 72514 | yes |
| `work/contributions/english/GLOSSARY_OCCURRENCES.json` | 158644 | yes |
| `work/contributions/english/GLOSSARY_SUMMARY.json` | 194 | yes |
| `work/contributions/english/GLOSSARY_ADDITIONS.json` | 17881 | yes |
| `work/contributions/english/GLOSSARY_COORDINATED_CATEGORY_EVIDENCE.json` | 1637 | yes |
| `work/contributions/decisions/index_glossary_pairs.tsv` | 22334 | yes |
| `work/contributions/decisions/body_terminology_inventory.tsv` | 27687 | yes |

The JSON contains both SHA-256 values for every comparison, the full seed inventory, stage commands and exit statuses, and the verified dependency preflight.

The final glossary has 320 rows, with 212 observed body forms in 131 French term families and all 108 paired index entries; 65 body families have multiple observed forms. All five final reader chains reconstruct their targets exactly.

## Ancillary inventory refresh

The first comparison matched all eight reader/master sources, all frozen language bodies and the final glossary. It identified two stale supporting inventories: the 108 English index offsets still pointed to an earlier source snapshot, and two terminology rows retained pre-repair spellings/counts. Their generators were rerun against the frozen final English source. `INVENTORY_FINAL_SOURCE_REFRESH.json` preserves every prior/final hash, changed field and exact reconstructable line operation; its six patches retain the byte differences.

The isolated outputs were left untouched. The final comparison against the refreshed current inventories passes for all 23 artifacts. No reader wording, formula, prepared body or final glossary value changed in that refresh.

## Unused temporary implementation copies

The initial seed inventory captured three implementation copies from a concurrently running compact-layout check. None appears in a stage command or required module input. Their exact hashes remain in the initial seed record; the unused isolated copies were removed after verification. The verifier now excludes both `portable-check-` and `patch-check-` directory prefixes at seed collection. All executed inputs and all 23 compared outputs retained their verified hashes.

## Reproduction commands

```sh
python work/contributions/packaging_audit/verify_source_rebuild.py
python work/contributions/packaging_audit/verify_portable_changes.py
```

The source verifier requires a fresh target directory. Its optional `--compare-existing` mode rechecks a completed, hash-verified isolated run and preserves initial comparison findings. The compact-layout utilities separately reproduce all eleven change artifacts per language byte for byte.
