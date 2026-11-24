#!/usr/bin/env python3
"""Extract numbered tables (title + cells) from a .docx into JSON: docx_tables.py in.docx out.json"""
import json, re, sys
import docx
from docx.document import Document as _D
from docx.oxml.ns import qn
from docx.table import Table
from docx.text.paragraph import Paragraph

d = docx.Document(sys.argv[1])
body = d.element.body
items = []
for child in body.iterchildren():
    if child.tag == qn("w:p"):
        items.append(("p", Paragraph(child, d).text.strip()))
    elif child.tag == qn("w:tbl"):
        items.append(("t", Table(child, d)))
out = {}
for i, (k, v) in enumerate(items):
    if k != "t":
        continue
    num = title = None
    for j in range(i - 1, max(i - 5, -1), -1):
        if items[j][0] == "p":
            m = re.match(r"^Таблиця\s+([0-9А-ЯA-Z]+\.[0-9]+)\s*(.*)$", items[j][1])
            if m:
                num = m.group(1)
                title = m.group(2).strip() or (items[j + 1][1] if items[j + 1][0] == "p" else "")
                break
    if not num or num in out:
        continue
    rows = []
    for r in v.rows:
        cells = []
        prev = None
        for c in r.cells:
            if c._tc is prev:
                continue
            prev = c._tc
            cells.append(" ".join(c.text.split()))
        rows.append(cells)
    notes = []
    for j in range(i + 1, min(i + 4, len(items))):
        if items[j][0] == "p" and (items[j][1].startswith("Джерело") or items[j][1].startswith("Примітка")):
            notes.append(items[j][1])
    out[num] = {"title": title, "rows": rows, "notes": notes}
json.dump(out, open(sys.argv[2], "w", encoding="utf-8"), ensure_ascii=False, indent=0)
print(len(out), "tables")
