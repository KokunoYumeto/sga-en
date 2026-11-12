# Exact visible-text projection used by the apparatus

The variant filter expands only definitions explicitly present in the source macro set. It makes no identifications between mathematical expressions. Unknown commands remain in the comparison.

| Macro | Visible replacement |
|---|---|
| `\\hyperref[label]{display}` | `display` |
| `\\eqhyperref[label]{display}` | `(display)` |
| `\\hyperrefext[X][label]{display}` | `X display` |
| `\\eqhyperrefext[X][label]{display}` | `X display`, exactly as defined in macros.tex |
| `\\neweqhyperrefext[X][label]{display}` | `X display`, exactly as defined in macros.tex |
| `\\pagehyperref[label]{display}` | `(page display)` |
| `\\etiquette[number]{label}` | no visible text (anchor and label only) |
| `\\label{label}`, `\\phantomsection`, `\\quoi` | no visible text |

Comments are removed. Runs of source whitespace become one source word space for this comparison. Only hunks whose two projected strings are equal are omitted from the correction apparatus. The unfiltered source changes remain in CHANGES_FR.tsv. Human editorial records remain in the separate Orgogozo dossier even when their two readings differ only in hyperlink metadata.
