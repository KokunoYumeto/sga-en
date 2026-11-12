"""Page segments of the translations of SGA 7 by the printed pages (folios) of the French, so that the French
scan-check fixes (sga_scan_check_20261105/FIXLOG_7I*.jsonl, FIXLOG_7II*.jsonl) can be located in them.

Targets:
  en7I, en7II  English (sga-en): no page markers.
  es7I         Spanish SGA 7 I (sga-es/sources/SGA7I, copied from the August workpass): the French markers
               "%%%%%%%%%%  scan idx N  |  folio F  %%%%%%%%%%" on 403 of 528 folios.
  es7II        Spanish SGA 7 II (sga-es/sources/SGA7II): \\pageoriginale counters, the k-th one is folio k.
Where a target has no marker for a folio, its start is estimated by aligning the mathematics of the French corrected
edition with the target (difflib on normalized formula tokens, exposé by exposé), interpolated between anchors and
kept between the real markers on either side.

load(target) -> Target with .texts {path: text} and .segs {folio: [(path, start, end)]}; .window(folio) gives the
spans of folios folio-1..folio+1."""
import bisect
import difflib
import pathlib
import re

BS = chr(92)
DOCS = pathlib.Path(r"C:\Users\user\Documents")
FR = DOCS / "sga_scan_check_20261105"
FRMARK = re.compile(r"%%%%%%%%%%  scan idx (\d+)  \|  folio (\d+)  %%%%%%%%%%")
FRFILES = {
    "7I": ["general_introduction_body.tex", "expose_I_body.tex", "expose_II_body.tex", "expose_VI_body.tex",
           "expose_VII_body.tex", "expose_VIII_body.tex", "expose_IX_body.tex"],
    "7II": [f"expose_{r}_body.tex" for r in
            "X XI XII XIII XIV XV XVI XVII XVIII XIX XX XXI XXII".split()],
}
TARGETS = {
    "en7I": dict(vol="7I", root=DOCS / r"rights_cc0_20261025\sga-en\sources\native\SGA7I"
                 r"\SGA7I_English_current_buildable_source_20260823", master="SGA7_I_English_source_first_workpass.tex"),
    "en7II": dict(vol="7II", root=DOCS / r"rights_cc0_20261025\sga-en\sources\native\SGA7II",
                  master="SGA7_II_English_source_first_workpass.tex"),
    "es7I": dict(vol="7I", root=DOCS / r"rights_cc0_20261025\sga-es\sources\SGA7I", master="sga7_tome_i_es.tex"),
    "es7II": dict(vol="7II", root=DOCS / r"rights_cc0_20261025\sga-es\sources\SGA7II", master="sga72_es.tex"),
}
INPUT = re.compile(r"^[^%\n]*?" + re.escape(BS) + r"(?:input|include)\{([^}]+)\}", re.M)
COUNTER = re.compile(re.escape(BS) + r"pageoriginaled?(?![A-Za-z])")


def expose_of(name):
    """Exposé of a file, from its name: 'intro', 'front', or a roman numeral."""
    n = name.replace(BS, "/").rsplit("/", 1)[-1]
    low = n.lower()
    if "general_introduction" in low:
        return "intro"
    if "front_matter" in low or "terminal" in low or "blank_folio" in low or "notice" in low:
        return "front"
    m = re.search(r"expose_([ivxl]+)(?:_|\.|$)", low)
    if m:
        return m.group(1).upper()
    return None


def master_files(root, master):
    """The .tex files of a document in \\input order (recursively)."""
    out = []

    def walk(p):
        t = p.read_text(encoding="utf-8", errors="replace")
        out.append(p)
        for m in INPUT.finditer(t):
            name = m.group(1).strip()
            q = (root / name)
            if q.suffix != ".tex":
                q = q.with_name(q.name + ".tex")
            if q.exists() and q not in out:
                walk(q)

    walk(root / master)
    return [p for p in out if p.name != master]


# \[ and \( only when not the line break \\[1.5em] or \\(; $ only when not escaped
MATH = re.compile(r"(?<!\\)\$\$(.+?)(?<!\\)\$\$|(?<!\\)\$([^$]{1,600}?)(?<!\\)\$|(?<!\\)\\\[(.+?)\\\]|"
                  r"(?<!\\)\\\((.+?)\\\)|\\begin\{(equation|align|eqnarray|gather|multline|displaymath)(\*?)\}(.+?)"
                  r"\\end\{\5\6\}", re.S)
TAG = re.compile(re.escape(BS) + r"tag\*?\{(?:" + re.escape(BS) + r"SGARefTarget\{[^}]*\}\{)?([^{}]*)\}")
DROP = re.compile(re.escape(BS) + r"(?:[,;:! ]|quad|qquad|left|right|[bB]igg?[lr]?|displaystyle|textstyle|limits|"
                  r"nolimits|mathrm|mathbf|mathbb|mathcal|mathscr|mathfrak|boldsymbol|bm|bf|rm|it|operatorname\*?|"
                  r"text(?:rm|it|bf|up)?|mbox|hbox|mathop|SGARefTarget\{[^}]*\}|SGARefLink\{[^}]*\}|label\{[^}]*\}|"
                  r"tag\*?)(?![A-Za-z])")
SAME = [(BS + "varphi", BS + "phi"), (BS + "epsilon", BS + "varepsilon"), (BS + "leqslant", BS + "le"),
        (BS + "leq", BS + "le"), (BS + "geqslant", BS + "ge"), (BS + "geq", BS + "ge"),
        (BS + "longrightarrow", BS + "to"), (BS + "rightarrow", BS + "to"), (BS + "xrightarrow", BS + "to")]


def norm(s):
    s = DROP.sub("", s)
    for a, b in SAME:
        s = s.replace(a, b)
    return re.sub(r"[\s{}]", "", s)


def tokens(t):
    """(offset, normalized token) for the formulas and equation tags of t."""
    out = []
    for m in MATH.finditer(t):
        body = next(g for g in (m.group(1), m.group(2), m.group(3), m.group(4), m.group(7)) if g is not None)
        for tm in TAG.finditer(body):
            out.append((m.start(), "#" + tm.group(1).strip()))
        k = norm(TAG.sub("", body))
        if len(k) >= 2:
            out.append((m.start(), k))
    for tm in TAG.finditer(t):   # tags outside the math matched above are rare; the duplicates do no harm
        pass
    return out


class Target:
    def __init__(self, name):
        cfg = TARGETS[name]
        self.name, self.vol, self.root = name, cfg["vol"], cfg["root"]
        self.files = [p for p in master_files(cfg["root"], cfg["master"])]
        self.texts = {p: p.read_text(encoding="utf-8", errors="replace") for p in self.files}
        self.starts = {}     # folio -> (path, offset) where the folio starts
        self.real = set()    # folios with a real marker
        self._segment()

    # ---- French ----
    def _french(self):
        d = FR / ("sga7i" if self.vol == "7I" else "sga7ii") / "current"
        out = {}
        for fn in FRFILES[self.vol]:
            t = (d / fn).read_text(encoding="utf-8", errors="replace")
            out[expose_of(fn)] = (t, [(int(m.group(2)), m.start()) for m in FRMARK.finditer(t)])
        return out

    def _real_markers(self):
        res = {}
        if self.name == "es7I":
            for p in self.files:
                for m in FRMARK.finditer(self.texts[p]):
                    res.setdefault(int(m.group(2)), (p, m.start()))
        elif self.name == "es7II":
            k = 0
            for p in self.files:
                for m in COUNTER.finditer(self.texts[p]):
                    k += 1
                    res.setdefault(k, (p, m.start()))
        return res

    def _segment(self):
        fr = self._french()
        real = self._real_markers()
        by_exp = {}
        for p in self.files:
            by_exp.setdefault(expose_of(str(p.relative_to(self.root))), []).append(p)
        self.align_stats = {}
        for exp, (ft, fmarks) in fr.items():
            tfiles = by_exp.get(exp, [])
            if not fmarks or not tfiles:
                continue
            # one string for the exposé's target files, with a map back to (file, offset)
            pieces, base, cat = [], [], ""
            for p in tfiles:
                base.append(len(cat))
                pieces.append(p)
                cat += self.texts[p] + "\n\n"
            ftok, ttok = tokens(ft), tokens(cat)
            sm = difflib.SequenceMatcher(None, [k for _, k in ftok], [k for _, k in ttok], autojunk=False)
            anchors = []
            for a, b, n in sm.get_matching_blocks():
                for i in range(n):
                    anchors.append((ftok[a + i][0], ttok[b + i][0]))
            self.align_stats[exp] = (len(ftok), len(ttok), len(anchors))
            fo = [a for a, _ in anchors]

            def est(m):
                """Target offset (in cat) of French offset m, by interpolation between anchors."""
                if not anchors:
                    return int(m / max(1, len(ft)) * len(cat))
                i = bisect.bisect_left(fo, m)
                if i == 0:
                    return max(0, anchors[0][1] - (anchors[0][0] - m))
                if i >= len(anchors):
                    return min(len(cat), anchors[-1][1] + (m - anchors[-1][0]))
                (f0, t0), (f1, t1) = anchors[i - 1], anchors[i]
                return t0 + (t1 - t0) * (m - f0) // max(1, f1 - f0)

            def to_cat(p, off):
                return base[pieces.index(p)] + off

            def from_cat(x):
                j = bisect.bisect_right(base, x) - 1
                p = pieces[max(0, j)]
                return p, min(len(self.texts[p]), x - base[max(0, j)])

            prev = 0
            folios = [f for f, _ in fmarks]
            for idx, (f, m) in enumerate(fmarks):
                if f in real and real[f][0] in pieces:
                    x = to_cat(*real[f])
                    self.real.add(f)
                else:
                    x = est(m)
                    brk = cat.rfind("\n\n", max(prev, x - 600), x)
                    if brk > 0:
                        x = brk + 2
                    # keep it below the next real marker of this exposé
                    nxt = [to_cat(*real[g]) for g in folios[idx + 1:] if g in real and real[g][0] in pieces]
                    if nxt:
                        x = min(x, nxt[0])
                x = max(x, prev)
                prev = x
                if f not in self.starts:
                    self.starts[f] = from_cat(x)
        # segments: from a folio's start to the next start in the same file (or the file end)
        order = sorted(self.starts.items(), key=lambda kv: (self.files.index(kv[1][0]), kv[1][1]))
        self.segs = {}
        for i, (f, (p, s)) in enumerate(order):
            # the folio runs to the next start; if that is in a later file, through the files in between
            if i + 1 < len(order):
                q, e = order[i + 1][1]
            else:
                q, e = self.files[-1], len(self.texts[self.files[-1]])
            spans, pi, qi = [], self.files.index(p), self.files.index(q)
            if pi == qi:
                spans.append((p, s, e))
            else:
                spans.append((p, s, len(self.texts[p])))
                for r in self.files[pi + 1:qi]:
                    spans.append((r, 0, len(self.texts[r])))
                spans.append((q, 0, e))
            self.segs.setdefault(f, []).extend(sp for sp in spans if sp[2] > sp[1])

    def window(self, folio, width=1):
        out = []
        for g in range(folio - width, folio + width + 1):
            out += self.segs.get(g, [])
        return out

    def rel(self, p):
        return str(p.relative_to(self.root)).replace(BS, "/")


def load(name):
    return Target(name)


if __name__ == "__main__":
    import json
    import sys
    sys.stdout.reconfigure(encoding="utf-8")
    for name in sys.argv[1:] or list(TARGETS):
        t = load(name)
        print(name, len(t.files), "files;", len(t.segs), "folios;", len(t.real), "real markers;",
              json.dumps(t.align_stats))
