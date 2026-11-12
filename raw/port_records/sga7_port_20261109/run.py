"""Carry the French SGA 7 scan-check fixes into one translation with OpenAI GPT-6.1 Sol (effort high, Flex tier), batch
by batch, at most CONCURRENCY at a time; answers in answer_<batch>.md and decisions_<batch>.json; each decisions file
is dry-run with apply.py. The prompt follows the EGA ports of 9 Nov (ega_scan_check_20261101/sol_port_es_20261109).
usage: python -I run.py TARGET [CONCURRENCY=3] [--only=BATCH,BATCH] [--tag=NAME]
The API key is read from the user's note at run time by enr_pilot (never printed or stored)."""
import json
import os
import re
import subprocess
import sys
import time

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, r"C:\Users\user\Documents\enriques_api_pilot_20261106")
import enr_pilot as P  # noqa: E402

COMMON = r"""
The French SGA 7 (Groupes de monodromie en géométrie algébrique, SGA 7 I = Lecture Notes in Mathematics 288, 1972;
SGA 7 II = LNM 340, 1973; offset reproductions of typescripts) is our LaTeX transcription. It was checked page by page
against the printed original, and every correction is an exact edit OLD -> NEW of the French LaTeX. The {LANG} edition
is a translation of the French, made before these corrections. Exposé VI of SGA 7 I is printed in English: there the
"French" text is the English original{VI}.

Your batch is below, between BEGIN BATCH and END BATCH. It has one block per printed page: "=== PAGE <page> ===", then
the {LANG} text of that page and of its neighbours ("----- {LANG}, file <file>, page <p> -----"){WHERE}, then the
French corrections of that page: "[id X]" with the kind of the correction, OLD, NEW and, where found, FRENCH CONTEXT
(the French around the corrected place).

For each id decide:
- "apply": the {LANG} has the error that the French fix corrects. Give an exact {LANG} edit: "tr_file" (as named in
  the block), "tr_old" (an exact substring of that {LANG} text, long enough to occur only once in the {LANG} pages of
  the block) and "tr_new" (the corrected {LANG}). Carry over the meaning of the fix: a corrected formula, index, sign,
  reference, number or letter; a missing or wrong word or phrase (translated, never pasted in French); an underline
  (the typescript's emphasis; the edition writes it as \underline{...} or with its own underline macro) added, removed
  or moved: put it on the {LANG} words that translate the French ones; a missing or wrong parenthesis, bracket or
  punctuation mark that belongs to the mathematics or the meaning.
- "already": the {LANG} already says what the corrected French says.
- "not_applicable": the fix concerns only the French: spelling, accents, French punctuation or spacing (spaces before
  ; : ! ?, guillemets), grammar, a line or page break, blank lines, or another layout choice of the French print that
  the {LANG} does not follow.
- "unclear": you cannot find the passage or are not sure; say why in "note".

Rules:
- Mathematics must end up identical to the corrected French: same symbols, letters, indices, references and numbering.
- Keep the {LANG} edition's conventions, macros, spelling and typography.
- Never change page markers (comment lines "%%%%%%%%%%  scan idx N  |  folio F  %%%%%%%%%%", \pageoriginale),
  \label, \SGARefTarget, \SGARefLink, \hyperref or \ref keys, or file structure.
- If one {LANG} edit covers several ids, put it in the first and give the others "already" with note "covered by <id>".
  No two "apply" edits may overlap.
- Use LF line breaks (\n) in tr_old and tr_new, exactly as in the {LANG} text shown.{BRANCHES}

Answer with one fenced block ```json containing one JSON list, one object per id, in the batch's order:
  {"id": "X", "decision": "apply"|"already"|"not_applicable"|"unclear", "tr_file": ..., "tr_old": ..., "tr_new": ...,
   "note": "..."}
("tr_file" and "tr_old" for "apply" and "already", "tr_new" only for "apply"; "note" short, and only where useful).
Every id of the batch gets exactly one object. For "already", "tr_old" is the exact {LANG} text (occurring once in the
{LANG} pages of the block) that already says what the corrected French says, so that the decision can be checked.
After the block, one line each: any place where the {LANG} translation itself is wrong in a way the French fix does
not cover (do not fix those). Nothing else.
"""
EN = dict(LANG="English", VI=" and the English edition reproduces it, so its fixes carry over as they stand wherever the "
          "English edition has the same text",
          WHERE=(": the English edition has no page markers, so these pages were found by aligning its formulas with "
                 "the French, and the passage can sit a little before or after the page named"),
          BRANCHES="")
ES = dict(LANG="Spanish", VI=", from which the Spanish of Exposé VI was translated",
          WHERE=(": the Spanish page breaks fall a few lines differently from the French, and some pages have no "
                 "marker, so the passage can sit on the page before or after"),
          BRANCHES=r"""
- Two branches. The Spanish edition is one source for two editions: \sisi{A}{B} prints A in the diplomatic edition
  (the printed reading, "original") and B in the corrected edition; text outside \sisi is in both. Each id says its
  BRANCH:
  "both": the French fix was made in the diplomatic and in the corrected French alike: edit the shared Spanish text
  (inside an existing \sisi, edit both arguments).
  "corrected only": only the corrected edition changes: write \sisi{<Spanish as it is>}{<corrected Spanish>}, or edit
  the second argument of an existing \sisi.
  "diplomatic only": only the diplomatic edition changes: write \sisi{<Spanish of the printed reading>}{<Spanish as
  it is>}, or edit the first argument of an existing \sisi. These fixes mostly restore in the diplomatic French a
  misprint of the print (kind misprint_in_print). The diplomatic Spanish reproduces a printed misprint where it is
  mathematics (a formula, index, sign, letter, number, reference) or a name; a French spelling or grammar slip of the
  print has no Spanish counterpart ("not_applicable"). If the Spanish already has \sisi with the printed reading in
  its first argument, the decision is "already".
- Keep each \sisi{...}{...} small (the formula or the few words that differ) and its braces balanced.""")
PROMPTS = {"en": "You carry corrections from the French SGA 7 into the English SGA 7.\n" + COMMON,
           "es": "You carry corrections from the French SGA 7 into the Spanish SGA 7.\n" + COMMON}


def prompt(target):
    lang = "en" if target.startswith("en") else "es"
    p = PROMPTS[lang]
    for k, v in (EN if lang == "en" else ES).items():
        p = p.replace("{" + k + "}", v)
    return p


def submit(target, tag, name, effort="high"):
    text = open(os.path.join(HERE, f"batches_{tag}", name + ".txt"), encoding="utf-8").read()
    body = {"model": "gpt-6.1-sol", "input": prompt(target) + "\nBEGIN BATCH\n" + text + "\nEND BATCH\n",
            "reasoning": {"effort": effort}, "max_output_tokens": 128000, "background": True, "service_tier": "flex"}
    code, r = P.call("POST", P.API, body)
    return code, r.get("id"), r.get("error")


def finish(target, name, r):
    text = "".join(c.get("text", "") for o in r.get("output", []) if o.get("type") == "message"
                   for c in o.get("content", []))
    open(os.path.join(HERE, f"answer_{name}.md"), "w", encoding="utf-8").write(text)
    m = re.search(r"```json\s*\n(.*?)```", text, re.S)
    ok = False
    if m:
        try:
            lst = json.loads(m.group(1))
            json.dump(lst, open(os.path.join(HERE, f"decisions_{name}.json"), "w", encoding="utf-8"), ensure_ascii=False,
                      indent=1)
            ok = True
        except ValueError as e:
            print(name, "JSON error", e, flush=True)
    u = r.get("usage") or {}
    usd = (u.get("input_tokens", 0) * 2 + u.get("output_tokens", 0) * 10) / 1e6 / 2
    dry = ""
    if ok:
        res = subprocess.run([sys.executable, "-I", "-B", os.path.join(HERE, "apply.py"), target,
                              os.path.join(HERE, f"decisions_{name}.json"), "--dry"], capture_output=True, text=True,
                             encoding="utf-8")
        dry = (res.stdout.strip().splitlines() or [res.stderr.strip()[-300:]])[-1]
    return ok, round(usd, 4), dry, u


def run(target, conc, tag, only=None, effort="high"):
    sp = os.path.join(HERE, f"state_{tag}.json")
    st = json.load(open(sp, encoding="utf-8")) if os.path.exists(sp) else {}
    index = json.load(open(os.path.join(HERE, f"batches_{tag}", "BATCHES.json"), encoding="utf-8"))
    todo = [b["batch"] for b in index if not os.path.exists(os.path.join(HERE, f"decisions_{b['batch']}.json"))
            and (only is None or b["batch"] in only)]
    flying = {n: v["id"] for n, v in st.items() if v.get("status") == "submitted" and n in todo}
    queue = [n for n in todo if n not in flying]
    while queue or flying:
        while queue and len(flying) < conc:
            n = queue.pop(0)
            code, rid, err = submit(target, tag, n, effort)
            if code >= 300 or not rid:
                print(n, "submit failed", code, json.dumps(err)[:200], flush=True)
                time.sleep(30)
                queue.append(n)
                continue
            flying[n] = rid
            st[n] = {"status": "submitted", "id": rid, "t": time.time(), "tries": st.get(n, {}).get("tries", 0) + 1}
            json.dump(st, open(sp, "w", encoding="utf-8"), indent=1)
        time.sleep(45)
        for n, rid in list(flying.items()):
            code, r = P.call("GET", f"{P.API}/{rid}")
            s = r.get("status")
            if s in ("queued", "in_progress"):
                continue
            del flying[n]
            if s == "completed":
                ok, usd, dry, u = finish(target, n, r)
                st[n].update(status="done" if ok else "bad_answer", usd=usd, dry=dry,
                             tokens=[u.get("input_tokens"), u.get("output_tokens")],
                             minutes=round((time.time() - st[n]["t"]) / 60, 1))
                print(n, st[n]["status"], f"${usd}", st[n]["minutes"], "min |", dry, flush=True)
            else:
                st[n].update(status=s)
                print(n, s, json.dumps(r.get("error"))[:200], flush=True)
                if st[n]["tries"] < 3:
                    queue.append(n)
            json.dump(st, open(sp, "w", encoding="utf-8"), indent=1)
    cost = sum(v.get("usd") or 0 for v in st.values())
    print(tag, "done; cost so far", f"${cost:.2f}", flush=True)


if __name__ == "__main__":
    a = [x for x in sys.argv[1:] if not x.startswith("--")]
    o = dict(x[2:].split("=", 1) for x in sys.argv[1:] if x.startswith("--") and "=" in x)
    run(a[0], int(a[1]) if len(a) > 1 else 3, o.get("tag", a[0]), o["only"].split(",") if "only" in o else None,
        o.get("effort", "high"))
