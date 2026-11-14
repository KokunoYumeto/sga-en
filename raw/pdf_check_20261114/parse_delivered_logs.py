"""PDF check, step 1 (AGENTS.md, PDF CHECK BEFORE PUBLICATION): overfull boxes in the delivered final build logs of the
SGA 7, SGA 5 and SGA 4 1/2 readers (GPT-6 Astra, ChatGPT Pro mode), with the output page each lands on.
GitHub housekeeper (Claude Opus 5.5 at effort high), 14 Nov 2026. Usage: python -I -B parse_delivered_logs.py"""
import json, pathlib, re, sys
sys.stdout.reconfigure(encoding="utf-8")
R = pathlib.Path("C:/Users/user/Documents/pro_admin_readers_20261112")
OUT = pathlib.Path(__file__).resolve().parent
LOGS = {}
for f in sorted((R / "01_SGA7_READERS_work/returns_20261112/SGA7_READERS_RECORDS_unzipped/compile").glob("*.log")):
    LOGS[f.stem] = f
for f in sorted((R / "04_SGA5_READERS_work/returns_20261113/SGA5_READERS_RECORDS_unzipped/build_outputs").glob("*.log")):
    LOGS[f.stem] = f
for f in sorted((R / "05_SGA4HALF_READERS_work/returns_20261113/SGA4HALF_READERS_RECORDS_unzipped/work/build").glob("*.pass3.log.txt")):
    LOGS[f.name.split(".")[0]] = f
for f in sorted((R / "09_ESQUISSE_READERS_work/returns_20261114/ESQUISSE_READERS_FINAL_20261114T2138Z_unzipped/build_logs").glob("ESQUISSE_*.log")):
    LOGS[f.stem] = f


def parse(log):
    txt = log.read_text(encoding="latin-1")
    rows, page = [], 0
    for m in re.finditer(r"\[(\d+)(?=[\s\]{<])|(Overfull [\\][hv]box \(([\d.]+)pt too (?:wide|high)\)[^\n]*)", txt):
        if m.group(1):
            page = max(page, int(m.group(1)))
        else:
            rows.append((float(m.group(3)), page + 1, m.group(2)[:160]))
    pages = re.search(r"Output written on .*?\((\d+) pages", txt, re.S)
    return rows, int(pages.group(1)) if pages else None


summary = {}
with open(OUT / "DELIVERED_OVERFULL_ALL.tsv", "w", encoding="utf-8") as f:
    f.write("reader\tpt\tpage\twarning\n")
    for k, log in LOGS.items():
        rows, pages = parse(log)
        for pt, pg, w in rows:
            f.write(f"{k}\t{pt}\t{pg}\t{w}\n")
        summary[k] = dict(pages=pages, overfull=len(rows), over_2pt=sum(pt > 2 for pt, _, _ in rows),
                          over_10pt=sum(pt > 10 for pt, _, _ in rows), max_pt=max([pt for pt, _, _ in rows], default=0),
                          pages_over_2pt=sorted({pg for pt, pg, _ in rows if pt > 2}))
json.dump(summary, open(OUT / "DELIVERED_OVERFULL_SUMMARY.json", "w", encoding="utf-8"), indent=1)
for k, v in summary.items():
    print(k, v)
