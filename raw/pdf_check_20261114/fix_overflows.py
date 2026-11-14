"""PDF check, step 2: build fix of the SGA 7 FR, SGA 5 FR/EN and SGA 4 1/2 FR readers (GPT-6 Astra, ChatGPT Pro mode)
whose delivered logs show overfull boxes over 2pt (AGENTS.md: fix in the build, never in the text).
GitHub housekeeper (Claude Opus 5.5 at effort high), 14 Nov 2026, following the SGA 6 fix of the main session
(07_SGA6_READERS_work/pdfcheck_20261114/fix_wide_displays.py).

The fix, per reader:
  1. preamble: \\usepackage{adjustbox} if absent, \\emergencystretch=5em and \\tolerance=2000 (let TeX loosen a
     paragraph instead of letting a line run into the margin);
  2. each display reported "detected at line L" over 2pt in the delivered log (an equation, align* or \\[...\\]) is
     wrapped in \\adjustbox{max width=\\displaywidth}{$\\displaystyle ...$}, which shrinks it only when it is wider
     than the line; tags and labels stay outside. The wording and the mathematics are unchanged.
Then three pdflatex passes (MiKTeX) and every overfull box listed with its output page.
Usage: python -I -B fix_overflows.py [names...]"""
import concurrent.futures, csv, json, pathlib, re, subprocess, sys
sys.stdout.reconfigure(encoding="utf-8")
R = pathlib.Path("C:/Users/user/Documents/pro_admin_readers_20261112")
OUT = pathlib.Path(__file__).resolve().parent / "fixed"
SRC = {}
for n in ("corrige_apparat", "diplomatique", "texte_de_lecture"):
    SRC[f"SGA7_FR_{n}"] = R / f"01_SGA7_READERS_work/returns_20261112/SGA7_READERS_FR_unzipped/SGA7_FR_{n}.tex"
    SRC[f"SGA5_FR_{n}"] = R / f"04_SGA5_READERS_work/returns_20261113/SGA5_READERS_FR_unzipped/SGA5_FR_{n}.tex"
    SRC[f"SGA4HALF_FR_{n}"] = R / f"05_SGA4HALF_READERS_work/returns_20261113/SGA4HALF_READERS_FR_unzipped/deliverables/FR/SGA4HALF_FR_{n}.tex"
for n in ("corrected_apparatus", "diplomatic", "reading"):
    SRC[f"SGA5_EN_{n}"] = R / f"04_SGA5_READERS_work/returns_20261113/SGA5_READERS_EN_unzipped/SGA5_EN_{n}.tex"
WRAP_A = "\\adjustbox{max width=\\displaywidth}{$\\displaystyle "
WRAP_B = "$}"
TAGLAB = re.compile(r"^\s*((?:\\(?:tag|label)\{[^{}]*\}\s*)+)|((?:\\(?:tag|label)\{[^{}]*\}\s*)+)\s*$")

# display lines over 2pt, from the delivered logs (the three forms of a volume differ only in the form selector,
# so their line numbers agree)
DISPLAY_LINES = {}
for row in csv.DictReader(open(pathlib.Path(__file__).resolve().parent / "DELIVERED_OVERFULL_ALL.tsv", encoding="utf-8"), delimiter="\t"):
    m = re.search(r"detected at line (\d+)", row["warning"])
    if m and float(row["pt"]) > 2:
        vol = row["reader"].split("_")[0] + "_" + row["reader"].split("_")[1]
        DISPLAY_LINES.setdefault(vol, set()).add(int(m.group(1)))


def wrap_body(body):
    """move leading/trailing tags and labels out, wrap the rest"""
    pre = post = ""
    m = re.match(r"^\s*((?:\\(?:tag|label)\{[^{}]*\}\s*)+)", body)
    if m:
        pre, body = m.group(1), body[m.end():]
    m = re.search(r"((?:\\(?:tag|label)\{[^{}]*\}\s*)+)\s*$", body)
    if m:
        post, body = m.group(1), body[:m.start()]
    if re.search(r"\\(tag|label)\{", body):
        return None
    return pre + WRAP_A + body.strip("\n") + WRAP_B + "\n" + post


def fix(t, vol):
    lines = t.split("\n")
    report = []
    for L in sorted(DISPLAY_LINES.get(vol, ()), reverse=True):
        # the display's end may sit a few lines above the reported line (inside a variant argument)
        for back in range(6):
            if re.search(r"\\end\{(equation\*?|align\*)\}|\\\]", lines[L - 1 - back]):
                L -= back
                break
        pos = sum(len(x) + 1 for x in lines[:L - 1])          # start of line L
        end_line = lines[L - 1]
        txt = "\n".join(lines)
        done = False
        for env in ("equation", "equation*", "align*"):
            e = "\\end{" + env + "}"
            if e in end_line:
                ke = txt.index(e, pos)
                kb = txt.rindex("\\begin{" + env + "}", 0, ke)
                body = txt[kb + len(env) + 8:ke]
                if "\\begin{" + env + "}" in body:
                    break
                if env == "align*":
                    if "\\tag" in body or "\\label" in body:
                        break
                    new = "\\[\n" + WRAP_A + "\\begin{aligned}" + body + "\\end{aligned}" + WRAP_B + "\n\\]"
                    txt = txt[:kb] + new + txt[ke + len(e):]
                else:
                    w = wrap_body(body)
                    if w is None:
                        break
                    txt = txt[:kb + len(env) + 8] + "\n" + w + txt[ke:]
                done = True
                break
        if not done and "\\]" in end_line:
            ke = txt.index("\\]", pos)
            kb = txt.rindex("\\[", 0, ke)
            body = txt[kb + 2:ke]
            if "\\[" not in body:
                txt = txt[:kb + 2] + "\n" + WRAP_A + body.strip("\n") + WRAP_B + "\n" + txt[ke:]
                done = True
        report.append((L, "wrapped" if done else "NOT WRAPPED: " + end_line[:80]))
        lines = txt.split("\n")
    t = "\n".join(lines)
    pre = ""
    if not re.search(r"\\usepackage(\[[^]]*\])?\{[^}]*adjustbox", t):
        pre += "\\usepackage{adjustbox}\n"
    pre += "\\setlength{\\emergencystretch}{5em}\n\\tolerance=2000\n"
    k = t.index("\\begin{document}")
    return t[:k] + pre + t[k:], report


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


def build(name):
    vol = "_".join(name.split("_")[:2])
    d = OUT / name; d.mkdir(parents=True, exist_ok=True)
    t, rep = fix(SRC[name].read_text(encoding="utf-8"), vol)
    (d / (name + ".tex")).write_text(t, encoding="utf-8")
    for _ in range(3):
        subprocess.run(["pdflatex", "-interaction=nonstopmode", name + ".tex"], cwd=d,
                       capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=3600)
    rows, pages = parse(d / (name + ".log"))
    return name, rep, rows, pages


names = sys.argv[1:] or list(SRC)
summary = {}
with concurrent.futures.ThreadPoolExecutor(4) as ex:
    for name, rep, rows, pages in ex.map(build, names):
        summary[name] = dict(pages=pages, wraps=rep, overfull=len(rows), over_2pt=sum(p > 2 for p, _, _ in rows),
                             over_10pt=sum(p > 10 for p, _, _ in rows), max_pt=max([p for p, _, _ in rows], default=0),
                             rows=[r for r in rows if r[0] > 0.5])
        print(name, pages, "pages; wraps", rep, "; overfull", len(rows), "; >2pt", summary[name]["over_2pt"],
              "; max", summary[name]["max_pt"], flush=True)
        for r in rows:
            if r[0] > 2:
                print("   ", r, flush=True)
prev = {}
p = pathlib.Path(__file__).resolve().parent / "FIXED_OVERFULL_SUMMARY.json"
if p.exists():
    prev = json.load(open(p, encoding="utf-8"))
prev.update(summary)
json.dump(prev, open(p, "w", encoding="utf-8"), indent=1)
