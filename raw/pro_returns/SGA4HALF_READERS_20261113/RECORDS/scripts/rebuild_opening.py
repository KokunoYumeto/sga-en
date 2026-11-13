# Invoke this script with python3.
"""Rebuild the reviewed Introduction and Ariadne components without audit writes.

The three source transformations reproduce the reviewed opening components
byte for byte. English Ariadne was absent from the supplied English release;
its reviewed translation is a frozen, separately credited build input.
"""
from pathlib import Path
import hashlib
import json

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "source"
OUT = ROOT / "work/arcata"


def one(text, old, new):
    count = text.count(old)
    if count != 1:
        raise ValueError("An opening source anchor does not occur exactly once.")
    return text.replace(old, new, 1)


def rebuild():
    outputs = {}
    text = (SOURCE / "fr/codex_dip/sga4.5-intro.tex").read_text(encoding="utf-8")
    for old, new in [
        (r"\chapter*{Introduction}", "\\PrintPage{III}\n\\chapter*{Introduction}"),
        ("Je remercie enfin", "\\PrintPage{IV}\nJe remercie enfin"),
        ("étaien devenues", "étaient devenues"),
        ("série de digression,", r"série de \var{digression}{digressions}{SGA45-CORR-0001},"),
    ]:
        text = one(text, old, new)
    outputs["fr/sga4.5-intro.tex"] = text

    text = (SOURCE / "en/sources/components/sga4half_intro_en.tex").read_text(encoding="utf-8")
    for old, new in [
        (r"\chapter*{Introduction}", "\\PrintPage{III}\n\\chapter*{Introduction}"),
        ("Finally, I thank", "\\PrintPage{IV}\nFinally, I thank"),
        ("series of digressions,", r"series of \var{digression}{digressions}{SGA45-CORR-0001},"),
    ]:
        text = one(text, old, new)
    titles = {
        "II": "Report on the trace formula",
        "III": r"Functions $L$ modulo $\ell^n$ and modulo $p$",
        "IV": "The cohomology class associated with a cycle",
        "V": "Duality",
        "VI": "Applications of the trace formula to trigonometric sums",
        "VII": r"Finiteness theorems in $\ell$-adic cohomology",
        "VIII": "Derived categories (State 0)",
    }
    for label, title in titles.items():
        text = one(text, r"\nameref{" + label + "}", r"\hyperref[" + label + "]{" + title + "}")
    outputs["en/sga4half_intro_en.tex"] = text

    text = (SOURCE / "fr/codex_dip/ariane.tex").read_text(encoding="utf-8")
    for old, new in [
        (r"\markboth{}{}", "\\PrintPage{1}\n\\markboth{}{}"),
        ("cohomologiques,", r"\var{cohomologiques}{cohomologique}{SGA45-CORR-0002},"),
        ("\\newpage\n\nLes exposés XV", "\\PrintPage{2}\n\nLes exposés XV"),
        ("\\newpage\n\net XIII", "\\PrintPage{3}\n\net XIII"),
    ]:
        text = one(text, old, new)
    outputs["fr/ariane.tex"] = text
    outputs["en/ariane_en.tex"] = (OUT / "ariane_en_reviewed.tex").read_text(encoding="utf-8")

    rows = []
    for relative, text in outputs.items():
        path = OUT / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        data = text.encode("utf-8")
        path.write_bytes(data)
        rows.append(dict(file=path.relative_to(ROOT).as_posix(), bytes=len(data),
                         sha256=hashlib.sha256(data).hexdigest()))
    report = dict(files=rows, audit_records_modified=False,
                  translation_input="work/arcata/ariane_en_reviewed.tex")
    (OUT / "opening_rebuild.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False))
    return report


if __name__ == "__main__":
    rebuild()
