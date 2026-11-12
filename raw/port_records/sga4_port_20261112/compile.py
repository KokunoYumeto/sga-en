"""Compile a translation of SGA 4 into build/<target> (the sources are not touched): the English with XeLaTeX, three
passes, from the directory of its master, as the release of 10 Nov 2026 was built
(sga_release_20261110/en/tools/build_release_sga_en_20261110.py: SGA 4 864 pages, 0 errors). For use once the port
is approved; the pilot changes nothing, so it does not need a build.
usage: python -I -B compile.py [TARGET ...] [--passes=3] [--root=DIR (a copy of the source tree)] [--out=DIR]"""
import pathlib
import re
import subprocess
import sys

sys.stdout.reconfigure(encoding="utf-8")
HERE = pathlib.Path(__file__).parent
sys.path.insert(0, str(HERE))
import segment as S  # noqa: E402

ENGINE = {"en4": "xelatex"}
opts = dict(a[2:].split("=", 1) for a in sys.argv[1:] if a.startswith("--") and "=" in a)
passes = int(opts.get("passes", 3))
names = [a for a in sys.argv[1:] if not a.startswith("--")] or list(S.TARGETS)
for name in names:
    cfg = S.TARGETS[name]
    master = pathlib.Path(opts.get("root", cfg["root"])) / cfg["master"]
    out = pathlib.Path(opts["out"]) if "out" in opts else HERE / "build" / name
    out.mkdir(parents=True, exist_ok=True)
    job = master.stem
    ok = True
    for _ in range(passes):
        r = subprocess.run([ENGINE[name], "-interaction=nonstopmode", "-halt-on-error", "-file-line-error",
                            f"-output-directory={out}", master.name], cwd=master.parent, capture_output=True,
                           text=True, encoding="utf-8", errors="replace")
        if r.returncode != 0:
            ok = False
            break
    log = (out / f"{job}.log").read_text(encoding="utf-8", errors="replace") if (out / f"{job}.log").exists() else ""
    errs = re.findall(r"^(?:\S+:\d+: |! ).*$", log, re.M)
    pages = re.search(r"Output written on .*?\((\d+) pages", log.replace("\n", ""))
    undef = len(re.findall(r"LaTeX Warning: (?:Reference|Citation) .* undefined", log))
    print(f"{name}: {'OK' if ok else 'FAILED'}; pages {pages.group(1) if pages else '?'}; errors {len(errs)}; "
          f"undefined references {undef}", *(["   " + e[:200] for e in errs[:5]]), sep="\n")
