# SGA — Current English Edition

[![Stable English DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.21925497.svg)](https://doi.org/10.5281/zenodo.21925497)
[![Exact release DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.21925498.svg)](https://doi.org/10.5281/zenodo.21925498)

A navigable English reading edition of the *Séminaires de Géométrie Algébrique* (SGA), presented as one cumulative linked reader and nine smaller component readers.

## Read the English edition

### [Open the complete 4,180-page linked reader (PDF, 34.6 MB)](https://github.com/KokunoYumeto/sga-en/releases/latest/download/00_SGA_EN_CUMULATIVE_LINKED_READER.pdf)

The cumulative reader has a cover followed by 4,179 admitted pages and preserves 39,941 named destinations. Its table of contents, statement references, bibliography links, and cross-volume references are live PDF links.

Prefer a smaller file? Choose a volume below.

| Volume | Main subject | Coverage in this release | Pages | English PDF |
|---|---|---:|---:|---|
| SGA 1 | Étale coverings and the fundamental group | Complete published scope; Exposé VII was never written | 260 | [Download](https://github.com/KokunoYumeto/sga-en/releases/latest/download/01_SGA1_EN_COMPLETE_PUBLISHED_SCOPE_READER.pdf) |
| SGA 2 | Local cohomology and Lefschetz theorems | Complete reader | 178 | [Download](https://github.com/KokunoYumeto/sga-en/releases/latest/download/02_SGA2_EN_COMPLETE_READER.pdf) |
| SGA 3 | Group schemes | Complete reader | 1,470 | [Download](https://github.com/KokunoYumeto/sga-en/releases/latest/download/03_SGA3_EN_COMPLETE_READER.pdf) |
| SGA 4 | Topos theory and étale cohomology | Complete reader | 864 | [Download](https://github.com/KokunoYumeto/sga-en/releases/latest/download/04_SGA4_EN_COMPLETE_READER.pdf) |
| SGA 4½ | Étale cohomology | Complete reader | 175 | [Download](https://github.com/KokunoYumeto/sga-en/releases/latest/download/05_SGA4HALF_EN_COMPLETE_READER.pdf) |
| SGA 5 | ℓ-adic cohomology and L-functions | Complete published content; all ten published exposés | 309 | [Download](https://github.com/KokunoYumeto/sga-en/releases/latest/download/06_SGA5_EN_COMPLETE_PUBLISHED_CONTENT_READER.pdf) |
| SGA 6 | Intersection theory and Riemann–Roch | Current layered reader; mixed source-alignment status | 376 | [Download](https://github.com/KokunoYumeto/sga-en/releases/latest/download/07_SGA6_EN_CURRENT_LAYERED_READER.pdf) |
| SGA 7 I | Monodromy groups in algebraic geometry, I | **Complete published volume:** Exposés I, II, VI–IX; no separately written/published Exposés III–V exist | 287 | [Download](https://github.com/KokunoYumeto/sga-en/releases/latest/download/08_SGA7I_EN_EXPOSES_I_II_VI_IX_READER.pdf) |
| SGA 7 II | Monodromy groups in algebraic geometry, II | Complete reader; Exposés X–XXII | 258 | [Download](https://github.com/KokunoYumeto/sga-en/releases/latest/download/09_SGA7II_EN_COMPLETE_READER.pdf) |

> **Why does SGA 7 I jump from II to VI?** This is the published structure, not a gap in the English edition. Grothendieck's oral Exposés I–V were not separately written; their substance was summarized in the written Exposé I. The published volume therefore contains I, II, VI, VII, VIII, and IX, all of which are included here. See [the source-authority note](SOURCE_AUTHORITY.md#sga-7-i-numbering).

The machine-readable coverage table is [`COMPONENT_COVERAGE.tsv`](COMPONENT_COVERAGE.tsv).

## How to navigate it

1. Open the cumulative reader in a PDF viewer with a bookmarks/sidebar panel.
2. Use the linked table of contents to move among volumes, exposés, sections, and statements.
3. Click numbered references in the text to follow internal and cross-volume links.
4. Use the standalone volume PDFs when you want a faster download or a narrower search space.
5. Return to the cumulative reader when following a reference into another SGA volume.

## What this edition is

This repository is the discoverable reading surface for one evolving English SGA DOI lineage. It gathers material that is otherwise difficult to approach as a coherent whole and makes its internal reference graph usable.

It is an auditable working mathematical edition—not peer review and not a claim that no error remains. Coverage and source alignment are stated rather than implied. In particular:

- SGA 7 I is complete as the published volume stands; its historical numbering jump is explained above and in `SOURCE_AUTHORITY.md`.
- SGA 6 contains layers with different source-alignment status.
- No separate DOI is minted for each volume or exposé.
- Rights in underlying French works, editions, typography, and third-party material remain with their respective rightsholders.

See [`SOURCE_AUTHORITY.md`](SOURCE_AUTHORITY.md) and [`LICENSE_AND_RIGHTS.md`](LICENSE_AND_RIGHTS.md).

## Editable sources and audit trail

- [Editable English sources (ZIP)](https://github.com/KokunoYumeto/sga-en/releases/latest/download/10_SGA_EN_EDITABLE_SOURCES.zip)
- [Evidence and provenance archive (ZIP)](https://github.com/KokunoYumeto/sga-en/releases/latest/download/11_SGA_EN_EVIDENCE_AND_PROVENANCE.zip)
- [SHA-256 manifest](https://github.com/KokunoYumeto/sga-en/releases/latest/download/12_SGA_EN_SHA256_MANIFEST.txt)
- [`RELEASE_MANIFEST.json`](RELEASE_MANIFEST.json): exact files, byte sizes, hashes, and validation identities
- [`DATACITE_RELATIONS.json`](DATACITE_RELATIONS.json): DOI relationships
- [Latest GitHub release](https://github.com/KokunoYumeto/sga-en/releases/latest)

## Citation and stable links

- Stable English-edition DOI: [10.5281/zenodo.21925497](https://doi.org/10.5281/zenodo.21925497)
- Exact 2026-08-14 release DOI: [10.5281/zenodo.21925498](https://doi.org/10.5281/zenodo.21925498)
- Global SGA hub DOI: [10.5281/zenodo.20410947](https://doi.org/10.5281/zenodo.20410947)
- Citation metadata: [`CITATION.cff`](CITATION.cff)

For scholarly citation, use the stable English DOI when referring to the evolving edition and the exact release DOI when page-level reproducibility matters.