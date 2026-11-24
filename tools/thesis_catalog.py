#!/usr/bin/env python3
"""Build a catalog of figures and tables from a pandoc-gfm export of a thesis.

Usage: thesis_catalog.py thesis.md media_dir out_json out_img_dir prefix
"""
import json, re, sys, shutil
from pathlib import Path
from PIL import Image

md, media, out_json, out_dir, prefix = sys.argv[1:6]
lines = Path(md).read_text(encoding="utf-8").splitlines()
out_dir = Path(out_dir); out_dir.mkdir(parents=True, exist_ok=True)
figs, tabs = {}, {}
img_re = re.compile(r'<img src="([^"]+)"|!\[[^\]]*\]\(([^)\s]+)')
cap_re = re.compile(r'^\**Рис(?:унок)?\.?\s*([0-9А-ЯA-Z]+\.[0-9]+)\.?\**\s*(.*)$')
tab_re = re.compile(r'^\**Таблиця\s+([0-9А-ЯA-Z]+\.[0-9]+)\**\s*$')

def clean_cell(s):
    s = re.sub(r'\$\$\\mathbf\{(.*?)\}\$\$', r'\1', s)
    s = re.sub(r'\$\$(.*?)\$\$', r'$\1$', s)
    s = s.replace('\\ ', ' ')
    return s

for i, l in enumerate(lines):
    m = cap_re.match(l.strip())
    if m:
        num, cap = m.group(1), m.group(2).strip().strip('*')
        img = None
        for j in range(i - 1, max(i - 8, -1), -1):
            mm = img_re.search(lines[j])
            if mm:
                img = mm.group(1) or mm.group(2); break
        src = ""
        for j in range(i + 1, min(i + 6, len(lines))):
            if lines[j].startswith("Джерело"):
                src = lines[j].strip(); break
        if img and num not in figs:
            p = Path(media).parent / img if not Path(img).is_absolute() else Path(img)
            if not p.exists():
                p = Path(md).parent / img
            name = f"{prefix}fig_{num.replace('.', '_')}.png"
            im = Image.open(p).convert("RGB")
            if im.width > 1500:
                im = im.resize((1500, round(im.height * 1500 / im.width)), Image.LANCZOS)
            im.save(out_dir / name, optimize=True)
            figs[num] = {"file": name, "caption": f"Рис. {num}. {cap}", "source": src}
        continue
    m = tab_re.match(l.strip())
    if m:
        num = m.group(1)
        if num in tabs:
            continue
        j = i + 1
        while j < len(lines) and not lines[j].strip():
            j += 1
        title = lines[j].strip().strip('*') if j < len(lines) and not lines[j].startswith('|') else ""
        k = j + 1 if title else j
        while k < len(lines) and not lines[k].startswith('|') and k < j + 4:
            k += 1
        rows = []
        while k < len(lines) and lines[k].startswith('|'):
            rows.append(clean_cell(lines[k])); k += 1
        notes = []
        while k < len(lines) and len(notes) < 2:
            t = lines[k].strip()
            if t.startswith("Джерело") or t.startswith("Примітка"):
                notes.append(t)
            elif t and notes:
                break
            k += 1
        if rows:
            tabs[num] = {"title": f"Таблиця {num}. {title}", "md": "\n".join(rows), "notes": notes}
Path(out_json).write_text(json.dumps({"figures": figs, "tables": tabs}, ensure_ascii=False, indent=1), encoding="utf-8")
print(len(figs), "figures,", len(tabs), "tables")
