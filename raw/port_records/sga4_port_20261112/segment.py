"""Page segments of the translations of SGA 4 by the printed pages (Springer folios) of the French, so that the French
scan-check fixes (sga_scan_check_20261105/FIXLOG_4_CURRENT.jsonl, through FINAL_4.json) can be located in them.

Target en4, the English SGA 4 (sga-en sources/native/SGA4/SGA4_English_current_buildable_source_20260906/source):
each exposé <NN>/<NN>_English.tex inputs fragments drafts/SGA4_<EXP>_LINES_<a>_<b>_English.texfrag, each the
translation of lines a..b of Orgogozo's French LaTeX at snapshot 71766d9 (the text the English was translated from),
and the fragments keep the edition's \\pageoriginale markers. For each fragment the markers of the English are paired
with the French markers in lines a..b of the snapshot, the j-th with the j-th, when their numbers agree; the k-th
French marker of an exposé is the k-th page of sga4_api_pass_20261111/PAGES.json (the page table of the scan check:
counter, Springer folio, lines). A page runs from the start of the line of its marker to the start of the line of the
next marker; the text of a fragment before its first marker belongs to the page before. Where the numbers disagree
(11 of the 271 fragments: the English has 1,545 of the 1,556 French markers, and in Exposé XVII one marker sits in the
neighbouring fragment), the fragment is "unaligned": every page it touches gets the whole fragment.

load(target) -> Target with .texts {path: text}, .segs {(dir, folio): [(path, start, end)]}, .unaligned (set of
fragment paths), .window(dir, folio) (the spans of folio-1..folio+1, merged, in reading order)."""
import pathlib
import re

BS = chr(92)
DOCS = pathlib.Path(r"C:\Users\user\Documents")
FR = DOCS / "sga_scan_check_20261105"
PASS = FR / "sga4_api_pass_20261111"
SNAP = DOCS / (r"interlanguage_parts\tmp\pdfs\sga4_orgogozo_71766d9_preflight_20260719T065631\archive_extract"
               r"\SGA4-HEAD-71766d9")
DIRS = ["01", "02", "03", "04", "05", "05bis"] + [f"{i:02d}" for i in range(6, 20)]
TARGETS = {
    "en4": dict(lang="English", root=DOCS / (r"rights_cc0_20261025\sga-en\sources\native\SGA4"
                                             r"\SGA4_English_current_buildable_source_20260906\source"),
                master="tomes/SGA4_English_translation_workpass.tex"),
}
MARK = re.compile(re.escape(BS) + r"pageoriginale(?![A-Za-z])")
COUNTER = MARK
FRMARK = re.compile(r"%%%%%%%%%%  scan idx (\d+)  \|  folio (\d+)  %%%%%%%%%%")   # not used in SGA 4; kept for apply.py
INP = re.compile(r"^[^%\n]*" + re.escape(BS) + r"input\{drafts/([^}]+)\}", re.M)
FRAG = re.compile(r"SGA4_([A-Za-z]+)_LINES_(\d+)_(\d+)_English")


def code(line):
    """The part of a line before an unescaped %."""
    m = re.search(r"(?<!\\)%", line)
    return line if m is None else line[:m.start()]


def marks_in_lines(lines):
    """Positions (line index, column) of the markers outside comments."""
    out = []
    for i, ln in enumerate(lines):
        for m in MARK.finditer(code(ln)):
            out.append((i, m.start()))
    return out


class Target:
    def __init__(self, name):
        import json
        cfg = TARGETS[name]
        self.name, self.root, self.lang = name, cfg["root"], cfg["lang"]
        pages = json.loads((PASS / "PAGES.json").read_text(encoding="utf-8"))
        self.files, self.texts, self.segs, self.unaligned, self.frag_range = [], {}, {}, set(), {}
        self.stats = {}
        for d in DIRS:
            # French pages of the exposé, in order, without a marker that stands in a commented-out line
            pr = (PASS / "pristine" / "diplomatic" / d / f"{d}.tex").read_text(encoding="utf-8").split("\n")
            fpages = [p for p in sorted((p for p in pages if p["file"] == d), key=lambda p: p["marker_line"])
                      if MARK.search(code(pr[p["marker_line"] - 1]))]
            snap = (SNAP / d / f"{d}.tex").read_text(encoding="utf-8", errors="replace").split("\n")
            smarks = marks_in_lines(snap)                       # [(line index, col)] in the snapshot
            assert len(smarks) == len(fpages), (d, len(smarks), len(fpages))
            wrapper = (self.root / d / f"{d}_English.tex").read_text(encoding="utf-8")
            frags = [self.root / d / "drafts" / (m.group(1) if m.group(1).endswith(".texfrag")
                                                 else m.group(1) + ".texfrag") for m in INP.finditer(wrapper)]
            prev_folio = None
            n_al = n_un = 0
            for p in frags:
                t = p.read_text(encoding="utf-8")
                self.files.append(p)
                self.texts[p] = t
                m = FRAG.search(p.name)
                a, b = int(m.group(2)), int(m.group(3))
                self.frag_range[p] = (d, a, b)
                fidx = [k for k, (li, _) in enumerate(smarks) if a - 1 <= li <= b - 1]   # French markers of a..b
                lines = t.split("\n")
                starts = [0]
                for ln in lines:
                    starts.append(starts[-1] + len(ln) + 1)
                emarks = marks_in_lines(lines)
                folios = [fpages[k]["folio"] for k in fidx]
                if len(emarks) == len(fidx):
                    n_al += 1
                    cuts = [starts[li] for li, _ in emarks]
                    bounds = [0] + cuts + [len(t)]
                    owners = [prev_folio] + folios
                    for j, owner in enumerate(owners):
                        s, e = bounds[j], bounds[j + 1]
                        if owner is not None and e > s:
                            self.segs.setdefault((d, owner), []).append((p, s, e))
                else:
                    n_un += 1
                    self.unaligned.add(p)
                    for owner in [prev_folio] + folios:
                        if owner is not None:
                            self.segs.setdefault((d, owner), []).append((p, 0, len(t)))
                if folios:
                    prev_folio = folios[-1]
            self.stats[d] = dict(fragments=len(frags), aligned=n_al, unaligned=n_un, french_pages=len(fpages))

    def window(self, d, folio, width=1):
        spans = []
        for g in range(folio - width, folio + width + 1):
            spans += self.segs.get((d, g), [])
        spans.sort(key=lambda s: (self.files.index(s[0]), s[1]))
        merged = []
        for p, s, e in spans:
            if merged and merged[-1][0] == p and s <= merged[-1][2]:
                merged[-1] = (p, merged[-1][1], max(e, merged[-1][2]))
            else:
                merged.append((p, s, e))
        return merged

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
        print(name, len(t.files), "fragments;", len(t.segs), "pages with text;", len(t.unaligned), "unaligned fragments")
        print(json.dumps(t.stats))
