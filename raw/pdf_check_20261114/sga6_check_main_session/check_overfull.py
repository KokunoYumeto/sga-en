"""PDF check of the SGA 6 readers final (AGENTS.md, PDF CHECK BEFORE PUBLICATION): compile a copy of each of the eight
delivered TeX files twice with pdflatex (MiKTeX), with the preamble's \\hfuzz=20pt lowered to 0.5pt so that every
overfull box is reported (\\hfuzz changes only the warnings, not the layout), then list every overfull box with its
amount and the output page it lands on. Written by the main session (Claude Opus 5.5 at effort max), 14 Nov 2026.
Our own command; Pro's scripts/compile_readers.py is not run. Usage: python -I -B check_overfull.py [--compile]"""
import concurrent.futures, json, pathlib, re, shutil, subprocess, sys
sys.stdout.reconfigure(encoding="utf-8")
FIN = pathlib.Path("C:/Users/user/Documents/pro_admin_readers_20261112/07_SGA6_READERS/returns_20261113/"
                   "SGA6_READERS_FINAL_20261114T0320Z_unzipped")
OUT = pathlib.Path(__file__).resolve().parent
SRC = [FIN / "readers/fr/final" / f"SGA6_FR_{n}.tex" for n in ("diplomatique", "corrige_apparat", "texte_de_lecture", "master_annote")] + \
      [FIN / "review/english/final" / f"SGA6_EN_{n}.tex" for n in ("diplomatic", "corrected_apparatus", "reading", "annotated_master")]


def build(src):
    d = OUT / src.stem; d.mkdir(exist_ok=True)
    t = src.read_text(encoding="utf-8")
    n = t.count("\\hfuzz=20pt")
    t = t.replace("\\hfuzz=20pt", "\\hfuzz=0.5pt")
    (d / src.name).write_text(t, encoding="utf-8")
    for _ in range(2):
        subprocess.run(["pdflatex", "-interaction=nonstopmode", "-halt-on-error", src.name], cwd=d,
                       capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=3600)
    return src.stem, n


def parse(log):
    """overfull boxes with the output page they land on (the page after the last page shipped before the warning)"""
    txt = log.read_text(encoding="latin-1")
    rows, page = [], 0
    for m in re.finditer(r"\[(\d+)(?=[\s\]{<])|(Overfull \\[hv]box \(([\d.]+)pt too (?:wide|high)\)[^\n]*)", txt):
        if m.group(1):
            page = max(page, int(m.group(1)))
        else:
            rows.append((float(m.group(3)), page + 1, m.group(2)[:160]))
    pages = re.search(r"Output written on .*?\((\d+) pages", txt)
    return rows, int(pages.group(1)) if pages else None


if "--compile" in sys.argv:
    with concurrent.futures.ThreadPoolExecutor(4) as ex:
        for stem, n in ex.map(build, SRC):
            print("built", stem, "(hfuzz lines replaced:", n, ")", flush=True)
summary = {}
with open(OUT / "OVERFULL_ALL.tsv", "w", encoding="utf-8") as f:
    f.write("reader\tpt\tpage\twarning\n")
    for src in SRC:
        log = OUT / src.stem / (src.stem + ".log")
        if not log.exists():
            summary[src.stem] = "no log"; continue
        rows, pages = parse(log)
        for pt, pg, w in rows:
            f.write(f"{src.stem}\t{pt}\t{pg}\t{w}\n")
        big = sorted({pg for pt, pg, _ in rows if pt > 10})
        summary[src.stem] = dict(pages=pages, overfull=len(rows), over_2pt=sum(pt > 2 for pt, _, _ in rows),
                                 over_10pt=sum(pt > 10 for pt, _, _ in rows), max_pt=max([pt for pt, _, _ in rows], default=0),
                                 pages_over_10pt=big)
json.dump(summary, open(OUT / "OVERFULL_SUMMARY.json", "w", encoding="utf-8"), indent=1)
for k, v in summary.items():
    print(k, v if isinstance(v, str) else {x: (v[x] if x != "pages_over_10pt" else len(v[x])) for x in v})
