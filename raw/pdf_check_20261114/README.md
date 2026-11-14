# PDF check of the SGA readers, 14 November 2026

The check made before the releases `v2026-11-14-livres-de-lecture` (sga-fr) and `v2026-11-14-english-edition`
(sga-en), as AGENTS.md asks for every PDF: the overfull boxes counted in every build log, every page scanned for text
at the edge of the sheet, sample pages and every page with an overflow rendered and looked at. By the GitHub
housekeeper, Claude Opus 5.5 at effort high; the SGA 6 check (`sga6_check_main_session/`) by the main session,
Claude Opus 5.5 at effort max.

- `parse_delivered_logs.py` -> `DELIVERED_OVERFULL_ALL.tsv`, `DELIVERED_OVERFULL_SUMMARY.json`: every overfull box in
  the delivered build logs (GPT-6 Astra, ChatGPT Pro mode) of SGA 7, SGA 5, SGA 4 1/2 and the Esquisse readers, with
  the output page it lands on.
- `fix_overflows.py` -> `FIXED_OVERFULL_SUMMARY.json`, `fix_run2.log`: the build fix of the SGA 7 French, SGA 5 French
  and English and SGA 4 1/2 French readers (wide displays wrapped in `\adjustbox{max width=\displaywidth}`;
  `\emergencystretch=5em` and `\tolerance=2000` in the preamble), three pdfLaTeX passes (MiKTeX), and the overfull
  boxes left: none over 2pt.
- `render_check.py`: the page scan and the contact sheets.

Readers published as delivered: SGA 7, SGA 6 and SGA 4 1/2 in English (their logs show nothing over about 2pt).
Readers published from the fixed build: SGA 4 1/2, SGA 5, SGA 6 and SGA 7 in French, SGA 5 in English.
Not published: the SGA 4 reading texts of 12 November 2026 (English: 140 overfull boxes over 2pt, up to 70pt;
French: 16, up to 38pt).
