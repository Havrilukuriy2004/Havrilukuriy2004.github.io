#!/usr/bin/env python3
"""Crop numbered charts ('01 Title') from the left column of FMC research notes: note_charts.py in.pdf out_dir"""
import re, sys
from pathlib import Path
import pymupdf as fitz
src, out = sys.argv[1], Path(sys.argv[2]); out.mkdir(parents=True, exist_ok=True)
doc = fitz.open(src)
for page in doc:
    W = page.rect.width
    lines = []
    for b in page.get_text("dict")["blocks"]:
        for l in b.get("lines", []):
            t = "".join(s["text"] for s in l["spans"]).strip()
            if t:
                lines.append((fitz.Rect(l["bbox"]), t))
    heads = sorted([(r, t) for r, t in lines if re.match(r"^0\d\s+\S", t) and r.x0 < W * 0.5], key=lambda x: x[0].y0)
    draws = [fitz.Rect(d["rect"]) for d in page.get_drawings()]
    for i, (r, t) in enumerate(heads):
        ybot = heads[i + 1][0].y0 - 2 if i + 1 < len(heads) else page.rect.height - 40
        col = [d for d in draws if d.y0 >= r.y0 - 2 and d.y1 <= ybot and d.x1 < W * 0.52 and d.height < 400]
        dbot = max([d.y1 for d in col] + [r.y1])
        dright = max([d.x1 for d in col] + [r.x1])
        box = fitz.Rect(r)
        for d in col:
            box |= d
        for lr, lt in lines:
            if lr.y0 >= r.y0 - 1 and lr.y1 <= min(ybot, dbot + 16) and lr.x1 <= dright + 6:
                box |= lr
        clip = (box + (-4, -4, 4, 4)) & page.rect
        page.get_pixmap(matrix=fitz.Matrix(3, 3), clip=clip).save(out / f"chart_{t[:2]}.png")
        print(t[:60])
