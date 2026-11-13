# Checkpoint privacy and execution-artifact audit

| Archive | Members | Members with private values | Private matches | Raw compile artifacts |
|---|---:|---:|---:|---:|
| `SGA5_READERS_checkpoint_3.zip` | 264 | 0 | 0 | 0 |

The JSON report records archive SHA-256 values, member hashes, finding categories, and line numbers. It deliberately omits matched private values.

## Required exclusions

Exclude `compile_check/`, `runtime_check/`, `flat_compile_check/`, `compile_tmp/`, raw LaTeX build directories, `.stdout`, `.aux`, `.out`, `.toc`, `.fls`, `.fdb_latexmk`, and `__pycache__/`. Keep the screened `deliverables/records/build_outputs/` logs and summaries after testing their complete contents.

## Mathematical expressions and path detection

A broad drive-prefix pattern such as a single letter followed by colon and backslash also matches mathematical expressions. The regression cases preserve `f:\mathcal{C}\to\mathcal{D}`, `A:\cC\longrightarrow\cD`, and corresponding trace/vector examples. A Windows-path finding requires a known filesystem directory immediately after the drive prefix. Unix paths require an explicit absolute filesystem root; relative archive/build references remain intact.

Avoid any broad drive-path substitution after a more precise redactor: it can erase mathematical text in diagnostics. The scanner requires known-directory Windows-root context. Its only explicit path-like exceptions are exact standard interpreter shebangs and declared regular-expression literals that contain regex structure rather than an actual private file value. Every exception is listed by member, line, category, and hash. Sanitization must never rewrite mathematical reader content.
