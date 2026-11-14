"""Build fix for the four French SGA 6 readers (AGENTS.md, PDF CHECK: fix in the build, never in the text), 14 Nov
2026, main session (Claude Opus 5.5 at effort max). Two displays ran 10-13pt into the right margin, hidden in the
delivered logs by the preamble's \\hfuzz=20pt:
  1. the four maps i_*, j_*, f_*, g_* of 3.3 (folio 440-441; output page 244/245);
  2. both readings of the array i)/ii) of Proposition 2.6 (variant FRV0450, folio 386; output page 214/215).
Each is wrapped in \\adjustbox{max width=\\displaywidth}{$\\displaystyle ...$} (adjustbox is already loaded), which
shrinks a display only when it is wider than the line; the wording and the mathematics are unchanged. \\hfuzz=20pt is
set to 0.5pt so that a rebuild reports every overflow. Writes fixed/<name>/<name>.tex, compiles twice with pdflatex,
lists the remaining overfull boxes. Usage: python -I -B fix_wide_displays.py"""
import concurrent.futures, pathlib, re, subprocess, sys
sys.stdout.reconfigure(encoding="utf-8")
FIN = pathlib.Path("C:/Users/user/Documents/pro_admin_readers_20261112/07_SGA6_READERS/returns_20261113/"
                   "SGA6_READERS_FINAL_20261114T0320Z_unzipped/readers/fr/final")
OUT = pathlib.Path(__file__).resolve().parent / "fixed"
NAMES = ["SGA6_FR_diplomatique", "SGA6_FR_corrige_apparat", "SGA6_FR_texte_de_lecture", "SGA6_FR_master_annote"]
WRAP_A = "\\adjustbox{max width=\\displaywidth}{$\\displaystyle "
WRAP_B = "$}"


def fix(t):
    # 1. the four maps of 3.3
    key = "i_*:K^{\\bullet}(Y)\\to K^{\\bullet}(X);\\quad"
    assert t.count(key) == 1, ("maps", t.count(key))
    k = t.index(key)
    a = t.rindex("\\[", 0, k); b = t.index("\\]", k)
    inner = t[a + 2:b].strip("\n")
    assert "\\[" not in inner and len(inner) < 400, inner
    t = t[:a] + "\\[\n" + WRAP_A + inner + WRAP_B + "\n" + t[b:]
    # 2. the two readings of FRV0450
    end = t.index("}{FRV0450}")
    start = t.rindex("\\SGAvarDisplay{", 0, end)
    seg = t[start:end]
    n = seg.count("\\begin{array}{ll}")
    assert n == 2 and seg.count("\\end{array}") == 2, n
    seg = seg.replace("\\begin{array}{ll}", WRAP_A + "\\begin{array}{ll}").replace("\\end{array}", "\\end{array}" + WRAP_B)
    t = t[:start] + seg + t[end:]
    assert t.count("\\hfuzz=20pt") == 2
    return t.replace("\\hfuzz=20pt", "\\hfuzz=0.5pt")


def build(name):
    d = OUT / name; d.mkdir(parents=True, exist_ok=True)
    (d / (name + ".tex")).write_text(fix((FIN / (name + ".tex")).read_text(encoding="utf-8")), encoding="utf-8")
    for _ in range(2):
        subprocess.run(["pdflatex", "-interaction=nonstopmode", "-halt-on-error", name + ".tex"], cwd=d,
                       capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=3600)
    log = (d / (name + ".log")).read_text(encoding="latin-1")
    over = re.findall(r"Overfull \\[hv]box \(([\d.]+)pt too (?:wide|high)\)", log)
    pages = re.search(r"Output written on .*?\((\d+) pages", log)
    return name, (pages.group(1) if pages else "NO PDF"), [float(x) for x in over]


with concurrent.futures.ThreadPoolExecutor(4) as ex:
    for name, pages, over in ex.map(build, NAMES):
        print(f"{name}: {pages} pages; overfull boxes: {len(over)}; over 2pt: {sum(x > 2 for x in over)}; max {max(over, default=0)}pt")
