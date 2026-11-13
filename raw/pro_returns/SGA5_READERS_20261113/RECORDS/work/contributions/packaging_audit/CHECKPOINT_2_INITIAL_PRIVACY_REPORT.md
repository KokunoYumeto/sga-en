# Checkpoint privacy and execution-artifact audit

| Archive | Members | Members with private values | Private matches | Raw compile artifacts |
|---|---:|---:|---:|---:|
| `SGA5_READERS_checkpoint_2.zip` | 182 | 10 | 378 | 3 |

The JSON report records archive SHA-256 values, member hashes, finding categories, and line numbers. It deliberately omits matched private values.

## Required exclusions

Exclude `compile_check/`, `runtime_check/`, `flat_compile_check/`, `compile_tmp/`, raw LaTeX build directories, `.stdout`, `.aux`, `.out`, `.toc`, `.fls`, `.fdb_latexmk`, and `__pycache__/`. Keep the screened `deliverables/records/build_outputs/` logs and summaries after testing their complete contents.

## Mathematical expressions and path detection

A broad drive-prefix pattern such as a single letter followed by colon and backslash also matches mathematical expressions. The regression cases preserve `f:\mathcal{C}\to\mathcal{D}`, `A:\cC\longrightarrow\cD`, and corresponding trace/vector examples. A Windows-path finding requires a known filesystem directory immediately after the drive prefix. Unix paths require an explicit absolute filesystem root; relative archive/build references remain intact.

The current `compile_readers.py` adds a broad drive-path substitution after its more precise redactor. That second substitution can erase mathematical text in diagnostics. Replace it with the known-directory pattern or use the shared precise redactor. Sanitization must never be used to rewrite the actual mathematical reader source.

## Raw artifacts in SGA5_READERS_checkpoint_2.zip

- `contributions/english/compile_check/EN_diplomatic_flat.log`
- `contributions/english/compile_check/EN_diplomatic_flat.pdf`
- `contributions/english/compile_check/console_second.txt`
