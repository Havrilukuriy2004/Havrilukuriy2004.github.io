"""Remove names of real banks that appear as *simulated* defaults in the interbank slides and report.

The contagion results list the banks that default in each reconstructed-network scenario. These are model
artefacts (see the report), so the published PDFs replace the list column with a neutral note and drop the names
from the explanatory paragraph. Run after prepare_assets.py:  python tools/redact_interbank.py
"""
import re
import shutil
from pathlib import Path

import fitz  # PyMuPDF

ROOT = Path(__file__).resolve().parent.parent / "files" / "interbank"
SRC = {
    "interbank_network_modelling_slides_uk.pdf": None,  # already copied by prepare_assets.py
    "interbank_model_report.pdf": None,
}
FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
NAME = re.compile(r'(?:П?АТ)\s*["«“][^"»”]{2,40}["»”]')
NOTE = "назви банків не публікуються: склад дефолтів у реконструйованих мережах є модельним артефактом"


def redact(path):
    doc = fitz.open(path)
    changed = 0
    for page in doc:
        text = page.get_text()
        names = NAME.findall(text)
        if not names and "дефолтні банки" not in text and "дефолтних банків" not in text:
            continue
        frags = {f.strip() for m in names for f in m.split("\n") if len(f.strip()) >= 3}
        name_rects = [r for f in frags for r in page.search_for(f)]
        inserts = []
        heads = page.search_for("Список дефолтних банків") + page.search_for("Ключові дефолтні банки")
        boxes = []
        for h in heads:  # results tables: blank the whole column of bank names
            alg = [r for r in page.search_for("Алгоритм") if abs(r.y0 - h.y0) < 40][0]
            loss = [r for r in page.search_for("капіталу") if abs(r.y0 - h.y0) < 40 and r.x1 < h.x0][0]
            nxt = min([g.y0 for g in heads if g.y0 > h.y0 + 5] + [page.rect.y1])
            algo = [r for k in ("Furfine", "Eisenberg") for r in page.search_for(k)
                    if r.x0 > alg.x0 - 25 and r.x1 < alg.x1 + 25 and h.y0 < r.y0 < nxt]
            y0 = min(r.y0 for r in algo) - 2
            y1 = max(r.y1 for r in algo) + 6
            x0 = loss.x1 + 4
            words = [w for w in page.get_text("words") if w[0] >= x0 and y0 <= w[1] <= y1]
            x1 = max([h.x1 + (h.x0 - x0)] + [w[2] for w in words]) + 2
            box = fitz.Rect(x0, y0, min(x1, page.rect.x1 - 4), y1)
            boxes.append(box)
            page.add_redact_annot(box, fill=(0.95, 0.95, 0.95))
            inserts.append((box + (4, 4, -4, 0), NOTE, 8.5, (0.35, 0.35, 0.35), fitz.TEXT_ALIGN_CENTER))
        head = bool(boxes)
        for b in page.get_text("blocks"):
            rect, btxt = fitz.Rect(b[:4]), b[4]
            if NAME.search(btxt) and not any(rect.intersects(bx) for bx in boxes):
                spans = [s for blk in page.get_text("dict", clip=rect)["blocks"] for ln in blk.get("lines", [])
                         for s in ln["spans"]]
                size = round(sum(s["size"] for s in spans) / max(len(spans), 1), 1) if spans else 10
                clean = re.sub(r"\s*\((?:\s*П?АТ[^)]*)\)", "", btxt.replace("\n", " "))
                clean = re.sub(r"\s{2,}", " ", clean).strip()
                page.add_redact_annot(rect, fill=(1, 1, 1))
                inserts.append((rect + (0, 0, 0, 20), clean, size, (0, 0, 0), fitz.TEXT_ALIGN_JUSTIFY))
        for r in name_rects:  # anything left (names outside the table/paragraph)
            if not any(r.intersects(bx) for bx in boxes):
                page.add_redact_annot(r, fill=(1, 1, 1))
        page.apply_redactions(images=fitz.PDF_REDACT_IMAGE_NONE)
        for rect, txt, size, color, align in inserts:
            fs = size
            while page.insert_textbox(rect, txt, fontsize=fs, fontname="dejavu", fontfile=FONT,
                                      color=color, align=align) < 0 and fs > 5:
                fs -= 0.5
        changed += 1
    tmp = path.with_suffix(".tmp.pdf")
    doc.save(tmp, garbage=3, deflate=True)
    doc.close()
    shutil.move(tmp, path)
    return changed


if __name__ == "__main__":
    for name in SRC:
        print(name, "pages changed:", redact(ROOT / name))
