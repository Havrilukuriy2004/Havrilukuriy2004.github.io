#!/usr/bin/env python3
"""Crop numbered figures from a PDF: pdf_figs.py in.pdf out_dir prefix catalog.json [merge]
Finds caption lines 'Рис. X.Y', unions drawings/images just above them, renders the clip."""
import json, re, sys
from pathlib import Path
import pymupdf as fitz

pdf, out_dir, prefix, cat_path = sys.argv[1:5]
out = Path(out_dir); out.mkdir(parents=True, exist_ok=True)
cat = json.load(open(cat_path, encoding="utf-8")) if Path(cat_path).exists() else {"figures": {}}
doc = fitz.open(pdf)
cap_re = re.compile(r"^Рис(?:унок)?\.?\s*(\d+)\.\s*(\d+)\.?\s*(.*)$")
added = 0
for pno, page in enumerate(doc):
    lines = []
    for b in page.get_text("dict")["blocks"]:
        for l in b.get("lines", []):
            t = "".join(s["text"] for s in l["spans"]).strip()
            if t:
                lines.append((fitz.Rect(l["bbox"]), t))
    rects = [fitz.Rect(d["rect"]) for d in page.get_drawings() if fitz.Rect(d["rect"]).width < page.rect.width * 0.98]
    rects += [fitz.Rect(i["bbox"]) for i in page.get_image_info()]
    for i, (r, t) in enumerate(lines):
        m = cap_re.match(t)
        if not m:
            continue
        num = f"{m.group(1)}.{m.group(2)}"
        if num in cat["figures"]:
            continue
        # caption may continue on next line
        cap = m.group(3)
        if i + 1 < len(lines) and abs(lines[i + 1][0].y0 - r.y1) < 4 and not lines[i + 1][1].startswith("Джерело"):
            cap += " " + lines[i + 1][1]
        cand = sorted([x for x in rects if x.y1 <= r.y0 + 4 and x.y1 >= r.y0 - 520 and x.height > 0.5], key=lambda x: -x.y1)
        if not cand:
            continue
        box = fitz.Rect(cand[0])
        top = box.y0
        for x in cand[1:]:
            if x.y1 >= top - 30:
                box |= x
                top = box.y0
        if box.height < 60 or box.width < 120:
            continue
        # include axis labels and legend text inside / just around the box
        for lr, lt in lines:
            if lr.y0 >= box.y0 - 6 and lr.y1 <= r.y0 + 1 and lr.intersects(fitz.Rect(box.x0 - 40, box.y0 - 6, box.x1 + 40, r.y0)):
                box |= lr
        clip = (box + (-6, -6, 6, 4)) & page.rect
        name = f"{prefix}fig_{num.replace('.', '_')}.png"
        page.get_pixmap(matrix=fitz.Matrix(2.2, 2.2), clip=clip).save(out / name)
        cat["figures"][num] = {"file": name, "caption": f"Рис. {num}. {cap.strip()}", "source": "", "page": pno + 1}
        added += 1
json.dump(cat, open(cat_path, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("added", added, "total", len(cat["figures"]))
