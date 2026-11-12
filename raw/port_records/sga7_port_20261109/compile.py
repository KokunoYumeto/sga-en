"""Compile the four translations of SGA 7 (both branches of the Spanish) with pdfLaTeX into build/<target>[_original],
one or more passes, and report errors. The sources are not touched.
usage: python -I compile.py [TARGET ...] [--passes=1]"""
import os
import pathlib
import re
import subprocess
import sys

sys.stdout.reconfigure(encoding="utf-8")
HERE = pathlib.Path(__file__).parent
sys.path.insert(0, str(HERE))
import segment as S  # noqa: E402

opts = dict(a[2:].split("=", 1) for a in sys.argv[1:] if a.startswith("--") and "=" in a)
passes = int(opts.get("passes", 1))
names = [a for a in sys.argv[1:] if not a.startswith("--")] or list(S.TARGETS)
ORIG = {"es7I": r"\def\SGAOriginalMode{1}", "es7II": r"\def\SGAOrigMode{1}"}
for name in names:
    cfg = S.TARGETS[name]
    jobs = [("", "")] + ([("_original", ORIG[name])] if name in ORIG else [])
    for suffix, pre in jobs:
        out = HERE / "build" / (name + suffix)
        out.mkdir(parents=True, exist_ok=True)
        job = pathlib.Path(cfg["master"]).stem
        ok = True
        for _ in range(passes):
            r = subprocess.run(["pdflatex", "-interaction=nonstopmode", "-halt-on-error", "-file-line-error",
                                f"-output-directory={out}", f"-jobname={job}", pre + r"\input{" + cfg["master"] + "}"],
                               cwd=cfg["root"], capture_output=True, text=True, encoding="utf-8", errors="replace")
            if r.returncode != 0:
                ok = False
                break
        log = (out / f"{job}.log").read_text(encoding="utf-8", errors="replace") if (out / f"{job}.log").exists() else ""
        errs = re.findall(r"^(?:\S+:\d+: |! ).*$", log, re.M)
        pages = re.search(r"Output written on .*?\((\d+) pages", log.replace("\n", ""))  # TeX wraps long log lines
        print(f"{name}{suffix}: {'OK' if ok else 'FAILED'}; pages {pages.group(1) if pages else '?'}; errors {len(errs)}",
              *(["   " + e[:200] for e in errs[:5]]), sep="\n")
