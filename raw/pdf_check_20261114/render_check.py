"""PDF check, step 3: every page of each PDF scanned for text that reaches the sheet edge (within 12pt) or leaves it,
and a contact sheet of sample pages (spread over the book, plus the pages given) rendered for looking at.
GitHub housekeeper (Claude Opus 5.5 at effort high), 14 Nov 2026.
Usage: python -I -B render_check.py OUT_PREFIX PDF [page,page,...]"""
import json, pathlib, sys
import fitz
from PIL import Image
sys.stdout.reconfigure(encoding="utf-8")
out, pdf = pathlib.Path(sys.argv[1]), pathlib.Path(sys.argv[2])
extra = [int(x) for x in sys.argv[3].split(",")] if len(sys.argv) > 3 and sys.argv[3] else []
doc = fitz.open(pdf)
n = doc.page_count
edge = []
for i, page in enumerate(doc):
    W, H = page.rect.width, page.rect.height
    for b in page.get_text("dict")["blocks"]:
        for line in b.get("lines", []):
            for s in line["spans"]:
                if not s["text"].strip():
                    continue
                x0, y0, x1, y1 = s["bbox"]
                if x0 < 12 or x1 > W - 12 or y0 < 12 or y1 > H - 12:
                    edge.append((i + 1, round(x0, 1), round(x1, 1), round(W, 1), s["text"][:40]))
sample = sorted(set([1, 2] + [max(1, round(n * k / 8)) for k in range(1, 8)] + [n] + extra))
sample = [p for p in sample if 1 <= p <= n]
ims = []
for p in sample:
    pix = doc[p - 1].get_pixmap(dpi=40)
    ims.append(Image.frombytes("RGB", (pix.width, pix.height), pix.samples))
cols = 6
w, h = max(i.width for i in ims), max(i.height for i in ims)
rows = (len(ims) + cols - 1) // cols
sheet = Image.new("RGB", (cols * w, rows * h), "white")
for k, im in enumerate(ims):
    sheet.paste(im, ((k % cols) * w, (k // cols) * h))
sheet.save(str(out) + "_sheet.png")
for p in extra:
    if 1 <= p <= n:
        pix = doc[p - 1].get_pixmap(dpi=80)
        pix.save(str(out) + f"_p{p}.png")
res = dict(pdf=pdf.name, pages=n, sample=sample, edge_spans=len(edge), edge_pages=sorted({e[0] for e in edge}), edge_examples=edge[:8])
json.dump(res, open(str(out) + "_check.json", "w", encoding="utf-8"), indent=1)
print(json.dumps(res, ensure_ascii=False))
