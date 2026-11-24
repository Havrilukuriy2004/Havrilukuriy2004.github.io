#!/usr/bin/env python3
"""Генератор двомовного академічного сайту (українська / English).

    pip install markdown pyyaml
    python build.py            # збирає сайт у _site/
    python build.py --drafts   # разом із чернетками (draft: true)

Вміст: content/ (YAML і Markdown). Файли для завантаження: files/.
Українська версія лежить у корені сайту, англійська — у теці en/.
"""
from __future__ import annotations

import datetime as dt
import html
import json
import re
import shutil
import sys
from pathlib import Path

import markdown
import yaml

ROOT = Path(__file__).resolve().parent
CONTENT = ROOT / "content"
OUT = ROOT / "_site"
SHOW_DRAFTS = "--drafts" in sys.argv
LANGS = ("uk", "en")
PREFIX = {"uk": "", "en": "en/"}
e = html.escape

MONTHS = {
    "uk": ["січня", "лютого", "березня", "квітня", "травня", "червня", "липня", "серпня", "вересня", "жовтня", "листопада", "грудня"],
    "en": ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"],
}

UI = {
    "uk": {
        "home": "Головна", "research": "Дослідження", "blog": "Блог", "analytics": "Аналітика", "publications": "Публікації",
        "teaching": "Викладання", "club": "Фінансовий клуб", "cv": "CV", "updated": "Оновлено", "download": "Завантажити",
        "material": "Матеріал", "format": "Формат", "size": "Розмір", "abstract": "Анотація", "findings": "Основні результати",
        "materials": "Матеріали для завантаження", "posts": "Записи блогу", "structure": "Структура роботи", "cite": "Як цитувати",
        "all_posts": "Усі записи →", "no_posts": "Записів поки немає.", "about": "Про мене", "current": "Поточні дослідження",
        "education": "Освіта", "experience": "Досвід", "awards": "Нагороди", "skills": "Навички", "recent": "Останні записи",
        "contacts": "Контакти", "more": "Детальніше →", "topic": "Тема", "slides": "Слайди", "practice": "Практика",
        "no_file": "—", "pending": "буде додано", "program": "Програма і матеріали", "lang_name": "Українська",
        "post_project": "Проєкт", "read_more": "Читати", "related": "Пов'язані матеріали",
    },
    "en": {
        "home": "Home", "research": "Research", "blog": "Blog", "analytics": "Analytics", "publications": "Publications",
        "teaching": "Teaching", "club": "Finance Club", "cv": "CV", "updated": "Updated", "download": "Download",
        "material": "Material", "format": "Format", "size": "Size", "abstract": "Abstract", "findings": "Key findings",
        "materials": "Materials to download", "posts": "Blog posts", "structure": "Structure", "cite": "How to cite",
        "all_posts": "All posts →", "no_posts": "No posts yet.", "about": "About", "current": "Current research",
        "education": "Education", "experience": "Experience", "awards": "Awards", "skills": "Skills", "recent": "Recent posts",
        "contacts": "Contact", "more": "More →", "topic": "Topic", "slides": "Slides", "practice": "Practice",
        "no_file": "—", "pending": "coming soon", "program": "Programme and materials", "lang_name": "English",
        "post_project": "Project", "read_more": "Read", "related": "Related materials",
    },
}

NAV = [("index.html", "home"), ("research.html", "research"), ("blog.html", "blog"), ("analytics.html", "analytics"),
       ("publications.html", "publications"), ("teaching.html", "teaching"), ("club.html", "club")]

ENV_NAMES = {
    "uk": {"definition": "Визначення", "proposition": "Твердження", "lemma": "Лема", "example": "Приклад", "remark": "Зауваження", "hypothesis": "Гіпотеза", "result": "Результат"},
    "en": {"definition": "Definition", "proposition": "Proposition", "lemma": "Lemma", "example": "Example", "remark": "Remark", "hypothesis": "Hypothesis", "result": "Result"},
}


# ---------------------------------------------------------------- helpers
def T(x, lang):
    """Translate a bilingual value {uk:.., en:..}; plain values pass through."""
    if isinstance(x, dict) and ("uk" in x or "en" in x):
        return x.get(lang) if x.get(lang) not in (None, "") else x.get("uk", x.get("en", ""))
    return x if x is not None else ""


def load_yaml(rel):
    with open(CONTENT / rel, encoding="utf-8") as f:
        return yaml.safe_load(f)


def fmt_date(d, lang):
    if isinstance(d, str):
        d = dt.date.fromisoformat(d)
    if lang == "en":
        return f"{d.day} {MONTHS['en'][d.month - 1]} {d.year}"
    return f"{d.day} {MONTHS['uk'][d.month - 1]} {d.year}"


def human_size(n, lang):
    units = ["Б", "КБ", "МБ", "ГБ"] if lang == "uk" else ["B", "KB", "MB", "GB"]
    for u in units:
        if n < 1024 or u == units[-1]:
            s = f"{n:.0f} {u}" if u == units[0] else f"{n:.1f} {u}"
            return s.replace(".", ",") if lang == "uk" else s
        n /= 1024
    return ""


def fmt_of(path):
    ext = Path(path).suffix.lower().lstrip(".")
    return {"xlsx": "XLSX", "pdf": "PDF", "zip": "ZIP", "csv": "CSV", "docx": "DOCX", "r": "R", "py": "Python", "parquet": "Parquet", "json": "JSON"}.get(ext, ext.upper())


class Ctx:
    """Rendering context for one page: language and relative path depth."""

    def __init__(self, lang, path):
        self.lang, self.path = lang, path
        depth = path.count("/") + (1 if lang == "en" else 0)
        self.base = "../" * depth

    def page(self, target):
        return self.base + PREFIX[self.lang] + target

    def other(self):
        o = "en" if self.lang == "uk" else "uk"
        return self.base + PREFIX[o] + self.path

    def file(self, rel):
        return self.base + "files/" + rel

    def static(self, rel):
        return self.base + "static/" + rel

    def t(self, x):
        return T(x, self.lang)

    def ui(self, k):
        return UI[self.lang][k]


CATALOGS = {}


def load_catalogs():
    for key in ("master", "bachelor", "esg"):
        f, t = CONTENT / f"catalog_{key}.json", CONTENT / f"tables_{key}.json"
        CATALOGS[key] = {
            "figures": json.load(open(f, encoding="utf-8"))["figures"] if f.exists() else {},
            "tables": json.load(open(t, encoding="utf-8")) if t.exists() else {},
            "fig_dir": f"{key}/thesis_figures/",
        }


CHART_HEAD = '<script defer src="https://cdn.plot.ly/plotly-2.35.2.min.js"></script><script defer src="{js}"></script>'

REFNAME = {
    "master": {"uk": "магістерської роботи", "en": "of the master's thesis"},
    "bachelor": {"uk": "бакалаврської роботи", "en": "of the bachelor's thesis"},
    "esg": {"uk": "статті", "en": "of the paper"},
}


def shortcodes(text, ctx):
    """Numbered figures and tables inside a post.
    {{fig [src:]2.11 | caption | source}}   thesis figure from the catalog
    {{img path/under/files.png | caption | source}}   any image (PNG, GIF)
    {{gallery path :: caption ;; path :: caption}}   grid of images (animations)
    {{tab [src:]2.6 | title | rows=1-8 | cols=0,1,3}}   thesis table from the catalog
    Table: title   (line right before a Markdown table) -> numbered table title"""
    n = {"fig": 0, "tab": 0}
    FIG = {"uk": "Рис.", "en": "Fig."}[ctx.lang]
    TAB = {"uk": "Таблиця", "en": "Table"}[ctx.lang]

    def figure_html(url, cap, srcline):
        n["fig"] += 1
        return (f'\n\n<figure><a href="{url}"><img src="{url}" alt="{e(cap)}" loading="lazy"></a>'
                f'<figcaption><strong>{FIG} {n["fig"]}.</strong> {e(cap)}{"<br><span class=src>" + e(srcline) + "</span>" if srcline else ""}</figcaption></figure>\n\n')

    def fig(m):
        args = [a.strip() for a in m.group(1).split("|")]
        src, num = (args[0].split(":", 1) if ":" in args[0] else ("master", args[0]))
        f = CATALOGS[src]["figures"].get(num)
        if not f:
            return f"<p class='muted'>[figure {e(num)}]</p>"
        cap = args[1] if len(args) > 1 and args[1] else re.sub(r"^Рис\.\s*[\dА-Я]+\.\d+\.\s*\.?\s*\*?", "", f["caption"]).strip()
        if len(args) > 2 and args[2]:
            srcline = args[2]
        else:
            srcline = (f.get("source", "") or "").rstrip(".")
            if ctx.lang == "en":
                srcline = "Source: author's calculations" + (" based on NBU data" if src == "master" else "")
            srcline = srcline + "." if srcline else ""
        return figure_html(ctx.file(CATALOGS[src]["fig_dir"] + f["file"]), cap, srcline)

    def img(m):
        args = [a.strip() for a in m.group(1).split("|")]
        cap = args[1] if len(args) > 1 else ""
        srcline = args[2] if len(args) > 2 else ""
        return figure_html(ctx.file(args[0]), cap, srcline)

    def gallery(m):
        items = []
        for it in m.group(1).split(";;"):
            path, _, cap = it.partition("::")
            n["fig"] += 1
            url = ctx.file(path.strip())
            items.append(f'<figure><a href="{url}"><img src="{url}" alt="{e(cap.strip())}" loading="lazy"></a>'
                         f'<figcaption><strong>{FIG} {n["fig"]}.</strong> {e(cap.strip())}</figcaption></figure>')
        return f'\n\n<div class="anim-grid">{"".join(items)}</div>\n\n'

    def tab(m):
        args = [a.strip() for a in m.group(1).split("|")]
        src, num = (args[0].split(":", 1) if ":" in args[0] else ("master", args[0]))
        t = CATALOGS[src]["tables"].get(num)
        if not t:
            return f"<p class='muted'>[table {e(num)}]</p>"
        title = t["title"].strip(" .") or ""
        rows = t["rows"]
        cols = None
        for a in args[1:]:
            if a.startswith("rows="):
                keep = []
                for part in a[5:].split(","):
                    a0, _, a1 = part.partition("-")
                    keep += list(range(int(a0), int(a1 or a0) + 1))
                rows = [rows[0]] + [rows[i] for i in keep if i < len(rows)]
            elif a.startswith("cols="):
                cols = [int(x) for x in a[5:].split(",")]
            elif a:
                title = a
        if cols:
            rows = [[r[c] for c in cols if c < len(r)] for r in rows]
        n["tab"] += 1
        head = "".join(f"<th>{e(c)}</th>" for c in rows[0])
        body = "".join("<tr>" + "".join(f"<td>{e(c)}</td>" for c in r) + "</tr>" for r in rows[1:])
        notes = "".join(f"<div>{e(x)}</div>" for x in t.get("notes", [])) if ctx.lang == "uk" else ""
        ref = t.get("source") or ({"uk": "Джерело: розрахунки автора за даними НБУ.", "en": "Source: author's calculations based on NBU data."}[ctx.lang])
        if ctx.lang == "uk" and any(x.strip().startswith("Джерело") for x in t.get("notes", [])):
            ref = ""
        return (f'\n\n<div class="dtable"><div class="dtable-title"><strong>{TAB} {n["tab"]}.</strong> {e(title)}</div><div class="dtable-scroll"><table>'
                f'<thead><tr>{head}</tr></thead><tbody>{body}</tbody></table></div><div class="dtable-notes">{notes}<div class="src">{e(ref)}</div></div></div>\n\n')

    def chart(m):
        args = [a.strip() for a in m.group(1).split("|")]
        n["fig"] += 1
        cap = args[1] if len(args) > 1 else ""
        srcline = args[2] if len(args) > 2 else ""
        return (f'\n\n<figure class="ichart"><div class="ichart-box" data-chart="{ctx.file("charts/" + args[0] + ".json")}" data-lang="{ctx.lang}"></div>'
                f'<figcaption><strong>{FIG} {n["fig"]}.</strong> {e(cap)}{"<br><span class=src>" + e(srcline) + "</span>" if srcline else ""}</figcaption></figure>\n\n')

    def mdtab(m):
        n["tab"] += 1
        return f'\n\n<div class="dtable-title md"><strong>{TAB} {n["tab"]}.</strong> {e(m.group(1).strip())}</div>\n\n'

    text = re.sub(r"\{\{fig ([^}]+)\}\}", fig, text)
    text = re.sub(r"\{\{img ([^}]+)\}\}", img, text)
    text = re.sub(r"\{\{chart ([^}]+)\}\}", chart, text)
    text = re.sub(r"\{\{gallery ([^}]+)\}\}", gallery, text)
    text = re.sub(r"\{\{tab ([^}]+)\}\}", tab, text)
    text = re.sub(r"^(?:Table|Таблиця):[ \t]+(.+)$", mdtab, text, flags=re.M)
    return text


def md(text, ctx):
    """Markdown -> HTML with protected LaTeX, numbered academic blocks and {{files}}/{{site}} placeholders."""
    text = (text or "").replace("{{files}}", ctx.base + "files").replace("{{site}}/", ctx.base + PREFIX[ctx.lang])
    text = shortcodes(text, ctx)
    store = []

    def keep(m, display=False):
        store.append(m.group(0))
        tok = f"\x00MATH{len(store) - 1}\x00"
        return f"\n\n{tok}\n\n" if display else tok

    disp = lambda m: keep(m, True)
    text = re.sub(r"\\begin\{(equation|align|gather|multline|eqnarray|flalign)(\*?)\}.+?\\end\{\1\2\}", disp, text, flags=re.S)
    text = re.sub(r"\$\$.+?\$\$", disp, text, flags=re.S)
    text = re.sub(r"\\\[.+?\\\]", disp, text, flags=re.S)
    text = re.sub(r"\\\(.+?\\\)", keep, text)
    text = re.sub(r"(?<![\\$])\$(?!\s)[^$\n]+?(?<!\s)\$", keep, text)
    counters = {}

    def env(m):
        kind = m.group(1).lower()
        counters[kind] = counters.get(kind, 0) + 1
        title = f"{ENV_NAMES[ctx.lang].get(kind, m.group(1))} {counters[kind]}"
        if m.group(2).strip():
            title += f" ({m.group(2).strip()})"
        inner = markdown.markdown(m.group(3), extensions=["tables", "sane_lists"])
        return f'\n\n<div class="env env-{kind}"><div class="env-title">{e(title)}.</div>{inner}</div>\n\n'

    text = re.sub(r"^:::[ \t]*(\w+)[ \t]*(.*?)\n(.*?)\n:::[ \t]*$", env, text, flags=re.S | re.M)

    def figure(m):
        src, cap = m.group(2), m.group(1)
        return f'\n\n<figure><img src="{src}" alt="{e(cap)}" loading="lazy"><figcaption>{e(cap)}</figcaption></figure>\n\n'

    text = re.sub(r"^!\[([^\]]+)\]\(([^)]+)\)\s*$", figure, text, flags=re.M)
    out = markdown.markdown(text, extensions=["tables", "fenced_code", "sane_lists"])
    for i, s in enumerate(store):
        tok = f"\x00MATH{i}\x00"
        out = out.replace(f"<p>{tok}</p>", f'<div class="math-display">{e(s, quote=False)}</div>')
        out = out.replace(tok, e(s, quote=False))
    return out


def file_link(rel, ctx, label=None, missing=None):
    p = ROOT / "files" / rel
    if p.is_file():
        return f'<a href="{ctx.file(rel)}" download>{e(label or ctx.ui("download"))}</a>', human_size(p.stat().st_size, ctx.lang)
    return f'<span class="muted">{missing or ctx.ui("pending")}</span>', ""


def materials_table(items, ctx, show_format=True):
    rows = []
    for it in items:
        title = ctx.t(it["title"])
        note = ctx.t(it.get("note", ""))
        sub = f"<span class='m-note'>{e(note)}</span>" if note else ""
        if it.get("link"):
            href = it["link"] if it["link"].startswith("http") else ctx.page(it["link"])
            fmt, size, ext = ctx.t(it.get("fmt", "")) or "WEB", "", ""
        else:
            lk, size = file_link(it["file"], ctx)
            m = re.search(r'href="([^"]+)"', lk)
            href = m.group(1) if m else ""
            fmt = ctx.t(it.get("fmt")) or fmt_of(it["file"])
            ext = " target='_blank' rel='noopener'" if href.endswith(".pdf") else (" download" if href else "")
        key = re.sub(r"[^a-z]", "", fmt.lower())[:4] or "file"
        badge = f"<span class='m-fmt f-{key}'>{e(fmt)}</span>" if show_format else ""
        t = f"<a href='{e(href)}'{ext}>{e(title)}</a>" if href else e(title)
        meta = f"<span class='m-size'>{size}</span>" if size else ""
        rows.append(f"<li>{badge}<span class='m-title'>{t}{sub}</span>{meta}</li>")
    return f"<ul class='mlist'>{''.join(rows)}</ul>"


def groups_html(groups, ctx):
    out = []
    for g in groups or []:
        desc = f"<p class='muted'>{e(ctx.t(g['desc']))}</p>" if g.get("desc") else ""
        out.append(f"<h3>{e(ctx.t(g['title']))}</h3>{desc}{materials_table(g['items'], ctx)}")
    return "".join(out)


def entry(left, right, sub_left="", sub_right="", note=""):
    s = f'<div class="entry"><div class="row"><strong>{e(left)}</strong><span>{e(right)}</span></div>'
    if sub_left or sub_right:
        s += f'<div class="row sub"><em>{e(sub_left)}</em><span>{e(sub_right)}</span></div>'
    if note:
        s += f'<p class="note">{e(note)}</p>'
    return s + "</div>"


# ---------------------------------------------------------------- layout
def page(ctx, title, body, *, active="", math=False, description="", wide=False, extra_head="", body_attr=""):
    prof = SITE
    name = ctx.t(prof["name"])
    links = " · ".join(f'<a href="{e(l["url"])}">{e(ctx.t(l["label"]))}</a>' for l in prof["links"])
    nav = "".join(f'<a href="{ctx.page(h)}"{" class=\"active\"" if h == active else ""}>{e(ctx.ui(k))}</a>' for h, k in NAV)
    nav += f'<a href="{ctx.file(prof["cv_file"])}">CV</a>'
    uk_on = ' class="on"' if ctx.lang == "uk" else ""
    en_on = ' class="on"' if ctx.lang == "en" else ""
    here = ctx.base + PREFIX[ctx.lang] + ctx.path
    other = ctx.other()
    lang_sw = (f'<div class="lang"><a{uk_on} href="{here if ctx.lang == "uk" else other}" hreflang="uk">UA</a>'
               f' | <a{en_on} href="{here if ctx.lang == "en" else other}" hreflang="en">EN</a></div>')
    mathjax = ""
    if math:
        macros = json.dumps(MACROS, ensure_ascii=False)
        mathjax = (
            "<script>window.MathJax={tex:{inlineMath:[['$','$'],['\\\\(','\\\\)']],displayMath:[['$$','$$'],['\\\\[','\\\\]']],"
            "tags:'ams',processEscapes:true,macros:" + macros + "},svg:{fontCache:'global',scale:1.05},options:{enableMenu:false}};</script>"
            '<script defer src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-svg-full.js"></script>')
    full_title = f"{title} | {name}" if title != name else name
    alt_uk = ctx.base + ctx.path if ctx.lang == "en" else here
    alt_en = ctx.base + "en/" + ctx.path if ctx.lang == "uk" else here
    return f"""<!DOCTYPE html>
<html lang="{ctx.lang}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(full_title)}</title>
<meta name="description" content="{e(description or ctx.t(prof['tagline']))}">
<meta name="author" content="{e(name)}">
<link rel="alternate" hreflang="uk" href="{alt_uk}">
<link rel="alternate" hreflang="en" href="{alt_en}">
<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'%3E%3Crect width='32' height='32' fill='%23111'/%3E%3Ctext x='16' y='22' font-family='Arial' font-size='15' font-weight='bold' fill='%23fff' text-anchor='middle'%3EYH%3C/text%3E%3C/svg%3E">
<link rel="stylesheet" href="{ctx.static('style.css')}">
{mathjax}{extra_head}
</head>
<body data-root="{ctx.base}"{body_attr}>
<header class="masthead">
  {lang_sw}
  <a class="name" href="{ctx.page('index.html')}">{e(name)}</a>
  <div class="contact">{e(ctx.t(prof['city']))} · <span>{e(prof['email'])}</span> · {links}</div>
  <nav>{nav}</nav>
</header>
<main{' class="wide"' if wide else ''}>
{body}
</main>
<footer>© {dt.date.today().year} {e(name)} · {ctx.ui('updated')} {fmt_date(dt.date.today(), ctx.lang)}</footer>
</body>
</html>
"""


NUM_CELL = re.compile(r"^[\s\u2212+\-–(]*[\d.,\s\u202f]+[%*ᵃᵇᶜ)\s]*(\([\d.,\s\u2212-]+\)[*\s]*)?$")


def _cell_class(body):
    plain = re.sub(r"<[^>]+>", "", body).strip()
    if not plain:
        return None
    if NUM_CELL.match(plain) and len(plain) < 30:
        return "n"
    return "t tl" if len(plain) > 30 else "t"


def _tag_table(m):
    table = m.group(0)
    rows = re.findall(r"<tr[^>]*>.*?</tr>", table, flags=re.S)
    numcols = {}
    for r in rows:
        for i, (_, body) in enumerate(re.findall(r"<td([^>]*)>(.*?)</td>", r, flags=re.S)):
            c = _cell_class(body)
            if c:
                numcols.setdefault(i, []).append(c == "n")

    def fix_row(rm):
        row = rm.group(0)
        idx = [0]

        def td(cm):
            attrs, body = cm.group("a"), cm.group("b")
            i = idx[0]; idx[0] += 1
            if "class=" in attrs:
                return cm.group(0)
            c = _cell_class(body) or "t"
            if c == "n" and " (" in body:
                a, b2 = body.split(" (", 1)
                body = f'<span class="nw">{a}</span> <span class="nw">({b2}</span>'
            return f'<td class="{c}"{attrs}>{body}</td>'

        def th(cm):
            attrs, body = cm.group("a"), cm.group("b")
            i = idx[0]; idx[0] += 1
            v = numcols.get(i, [])
            if "class=" not in attrs and i > 0 and v and sum(v) > len(v) / 2:
                return f'<th class="n"{attrs}>{body}</th>'
            return cm.group(0)

        def cell(cm):
            return (td if cm.group("tag") == "td" else th)(cm)

        return re.sub(r"<(?P<tag>t[hd])(?P<a>[^>]*)>(?P<b>.*?)</(?P=tag)>", cell, row, flags=re.S)

    out = re.sub(r"<tr[^>]*>.*?</tr>", fix_row, table, flags=re.S)
    ncols = max((len(re.findall(r"<t[hd][ >]", r)) for r in rows), default=0)
    if ncols >= 8:
        out = re.sub(r"^<table(?![^>]*class=)", '<table class="wide"', out)
    return out


def tag_table_cells(html_text):
    def one(m):
        pre, table = m.group(1), m.group(2)
        out = _tag_table(re.match(r".*", table, flags=re.S))
        if pre or table.startswith("<table class="):
            return (pre or "") + out
        return f'<div class="tscroll">{out}</div>'

    return re.sub(r'(<div class="dtable-scroll">\s*)?(<table[^>]*>.*?</table>)', one, html_text, flags=re.S)


def write(ctx, html_text):
    html_text = tag_table_cells(html_text)
    p = OUT / PREFIX[ctx.lang] / ctx.path
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(html_text, encoding="utf-8")


# ---------------------------------------------------------------- posts
def parse_post(path, lang):
    raw = path.read_text(encoding="utf-8")
    meta, body = {}, raw
    if raw.startswith("---"):
        _, fm, body = raw.split("---", 2)
        for line in fm.strip().splitlines():
            if ":" in line:
                k, v = line.split(":", 1)
                v = v.strip()
                if len(v) >= 2 and v[0] == v[-1] and v[0] in "\"'":
                    v = v[1:-1]
                meta[k.strip()] = v
    meta.update(slug=path.parent.name, body=body.strip(), lang=lang,
                draft=meta.get("draft", "false").lower() == "true", order=int(meta.get("order", 0)),
                section=meta.get("section", "research"), date=dt.date.fromisoformat(meta["date"]))
    return meta


def load_posts(lang):
    posts = []
    for d in sorted((CONTENT / "posts").iterdir()):
        f = d / f"{lang}.md"
        if not f.is_file():
            f = d / "uk.md"
        if f.is_file():
            posts.append(parse_post(f, lang))
    if not SHOW_DRAFTS:
        posts = [p for p in posts if not p["draft"]]
    return sorted(posts, key=lambda p: (p["date"], -p["order"]), reverse=True)


def post_list(posts, ctx):
    if not posts:
        return f'<p class="muted">{ctx.ui("no_posts")}</p>'
    rows = []
    for p in posts:
        draft = ' <span class="tag">draft</span>' if p["draft"] else ""
        rows.append(f'<li><div class="date">{fmt_date(p["date"], ctx.lang)}</div>'
                    f'<div><a class="post-title" href="{ctx.page("posts/" + p["slug"] + ".html")}">{e(p["title"])}</a>{draft}'
                    f'<p class="summary">{e(p.get("summary", ""))}</p></div></li>')
    return '<ul class="posts">' + "".join(rows) + "</ul>"


# ---------------------------------------------------------------- pages
def build_index(lang, posts):
    ctx = Ctx(lang, "index.html")
    p = SITE
    edu = "".join(entry(ctx.t(x["org"]), ctx.t(x["place"]), ctx.t(x["degree"]), x["dates"]) for x in p["education"])
    exp = "".join(entry(ctx.t(x["org"]), ctx.t(x["place"]), ctx.t(x["role"]), ctx.t(x["dates"]), ctx.t(x.get("note", ""))) for x in p["experience"])
    aw = "".join(entry(ctx.t(x["title"]), ctx.t(x["dates"]), note=ctx.t(x.get("note", ""))) for x in p["awards"])
    skills = "".join(f"<tr><th>{e(ctx.t(s['label']))}</th><td>{e(ctx.t(s['value']))}</td></tr>" for s in p["skills"])
    interests = "".join(f"<li>{e(i)}</li>" for i in ctx.t(p["interests"]))
    cards = []
    for pr in PROJECTS:
        cards.append(f"<div class='card'><span class='tag'>{e(ctx.t(pr['kicker']))}</span>"
                     f"<h3><a href='{ctx.page('research/' + pr['slug'] + '.html')}'>{e(ctx.t(pr['title']))}</a></h3>"
                     f"<p>{e(ctx.t(pr['card']))}</p></div>")
    body = f"""
<section><h2>{ctx.ui('about')}</h2>{md(ctx.t(p['about']), ctx)}<ul class="inline">{interests}</ul></section>
<section><h2>{ctx.ui('current')}</h2><div class="cards">{''.join(cards)}</div></section>
<section><h2>{ctx.ui('education')}</h2>{edu}</section>
<section><h2>{ctx.ui('experience')}</h2>{exp}</section>
<section><h2>{ctx.ui('awards')}</h2>{aw}</section>
<section><h2>{ctx.ui('skills')}</h2><table class="kv">{skills}</table></section>
<section><h2>{ctx.ui('recent')}</h2>{post_list(posts[:4], ctx)}<p><a href="{ctx.page('blog.html')}">{ctx.ui('all_posts')}</a></p></section>
<section><h2>{ctx.ui('contacts')}</h2><p>{e(p['email'])} · {' · '.join(f'<a href="{e(l["url"])}">{e(ctx.t(l["label"]))}</a>' for l in p['links'])} · <a href="{ctx.file(p['cv_file'])}">CV (PDF)</a></p></section>
"""
    write(ctx, page(ctx, ctx.t(p["name"]), body, active="index.html"))


def build_research_hub(lang):
    ctx = Ctx(lang, "research.html")
    blocks = []
    for pr in PROJECTS:
        url = ctx.page("research/" + pr["slug"] + ".html")
        blocks.append(f"<div class='entry'><p class='kicker' style='margin:22px 0 2px'>{e(ctx.t(pr['kicker']))}</p>"
                      f"<h2 style='border:0;margin:0 0 4px'><a href='{url}' style='color:inherit;text-decoration:none'>{e(ctx.t(pr['title']))}</a></h2>"
                      f"<p class='muted' style='margin:0 0 6px'><em>{e(ctx.t(pr['subtitle']))}</em></p>"
                      f"<p>{e(ctx.t(pr['card']))}</p><p><a href='{url}'>{ctx.ui('more')}</a></p></div>")
    body = f"<h1>{ctx.ui('research')}</h1>" + "<hr style='border:0;border-top:1px solid #d9d9d9'>".join(blocks)
    write(ctx, page(ctx, ctx.ui("research"), body, active="research.html"))


def build_project(lang, pr, posts):
    ctx = Ctx(lang, f"research/{pr['slug']}.html")
    meta = "".join(f"<tr><th>{e(ctx.t(m['k']))}</th><td>{e(ctx.t(m['v']))}</td></tr>" for m in pr.get("meta", []))
    findings = "".join(f"<li>{md(f, ctx)[3:-4]}</li>" for f in ctx.t(pr.get("findings", [])))
    struct = "".join(f"<li>{e(s)}</li>" for s in ctx.t(pr.get("structure", [])) or [])
    fig = ""
    if pr.get("figure"):
        fg = pr["figure"]
        src = fg["file_en"] if lang == "en" and fg.get("file_en") else fg["file"]
        fig = f"<figure><img src='{ctx.file(src)}' alt='{e(ctx.t(fg['caption']))}' loading='lazy'><figcaption>{e(ctx.t(fg['caption']))}</figcaption></figure>"
    rel_posts = [p for p in posts if p["section"] == pr["slug"]]
    rel_posts = sorted(rel_posts, key=lambda p: p["order"], reverse=True)
    cite = f"<h2>{ctx.ui('cite')}</h2><pre>{e(pr['citation'].strip())}</pre>" if pr.get("citation") else ""
    note = f"<div class='note-box'>{md(ctx.t(pr['note']), ctx)}</div>" if pr.get("note") else ""
    body = f"""
<article class="thesis">
  <p class="kicker"><a href="{ctx.page('research.html')}">{ctx.ui('research')}</a> · {e(ctx.t(pr['kicker']))}</p>
  <h1>{e(ctx.t(pr['title']))}</h1>
  <p class="subtitle"><em>{e(ctx.t(pr['subtitle']))}</em></p>
  <table class="kv">{meta}</table>
  <h2>{ctx.ui('abstract')}</h2>
  {md(ctx.t(pr['abstract']), ctx)}
  {fig}
  <h2>{ctx.ui('findings')}</h2>
  <ol class="findings">{findings}</ol>
  {f"<h2>{ctx.ui('structure')}</h2><ul class='plain'>{struct}</ul>" if struct else ''}
  <h2>{ctx.ui('posts')}</h2>
  {post_list(list(reversed(rel_posts)), ctx)}
  <h2>{ctx.ui('materials')}</h2>
  {note}
  {groups_html(pr.get('groups'), ctx)}
  {cite}
</article>
"""
    write(ctx, page(ctx, ctx.t(pr["title"]), body, active="research.html", description=ctx.t(pr["card"])))


def build_blog(lang, posts):
    ctx = Ctx(lang, "blog.html")
    parts = []
    for sec in BLOG_SECTIONS:
        items = sorted([p for p in posts if p["section"] == sec["key"]], key=lambda p: p["order"])
        if not items:
            continue
        link = f" <a class='small' href='{ctx.page(sec['link'])}'>{e(ctx.t(sec['link_label']))} →</a>" if sec.get("link") else ""
        parts.append(f"<h2>{e(ctx.t(sec['title']))}{link}</h2>{post_list(items, ctx)}")
    body = f"<h1>{ctx.ui('blog')}</h1><p class='lead'>{e(ctx.t(BLOG_INTRO))}</p>" + "".join(parts)
    write(ctx, page(ctx, ctx.ui("blog"), body, active="blog.html"))


def build_post(lang, p, posts):
    ctx = Ctx(lang, f"posts/{p['slug']}.html")
    same = sorted([x for x in posts if x["section"] == p["section"]], key=lambda x: x["order"])
    i = same.index(p)
    prev_, next_ = (same[i - 1] if i > 0 else None), (same[i + 1] if i + 1 < len(same) else None)
    pn = "<nav class='prevnext'>"
    pn += f"<a href='{prev_['slug']}.html'>← {e(prev_['title'])}</a>" if prev_ else "<span></span>"
    pn += f"<a href='{next_['slug']}.html'>{e(next_['title'])} →</a>" if next_ else "<span></span>"
    pn += "</nav>"
    sec = next((s for s in BLOG_SECTIONS if s["key"] == p["section"]), None)
    sec_link = ""
    if sec and sec.get("link"):
        sec_link = f" · <a href='{ctx.page(sec['link'])}'>{e(ctx.t(sec['title']))}</a>"
    author = f" · {e(p['author'])}" if p.get("author") else ""
    body = f"""
<article class="post">
  <p class="kicker"><a href="{ctx.page('blog.html')}">{ctx.ui('blog')}</a>{sec_link}</p>
  <h1>{e(p['title'])}</h1>
  <p class="meta">{fmt_date(p['date'], lang)}{author}</p>
  {md(p['body'], ctx)}
  {pn}
</article>
"""
    math = bool(re.search(r"\$|\\\(|\\\[|\\begin\{", p["body"]))
    active = "club.html" if p["section"] == "club" else "blog.html"
    head = CHART_HEAD.format(js=ctx.static("charts.js")) if "{{chart " in p["body"] else ""
    write(ctx, page(ctx, p["title"], body, active=active, math=math, description=p.get("summary", ""), extra_head=head))


def build_publications(lang):
    ctx = Ctx(lang, "publications.html")
    pubs = load_yaml("publications.yaml")
    order = [("preprint", {"uk": "Препринти та роботи в процесі", "en": "Preprints and work in progress"}),
             ("article", {"uk": "Статті у фахових журналах", "en": "Journal articles"}),
             ("thesis", {"uk": "Кваліфікаційні роботи", "en": "Theses"}),
             ("conference", {"uk": "Тези конференцій", "en": "Conference papers"})]
    parts = []
    for key, label in order:
        items = sorted([x for x in pubs if x["type"] == key], key=lambda x: -int(x["year"]))
        if not items:
            continue
        lis = []
        for x in items:
            title = e(ctx.t(x["title"]))
            if x.get("link"):
                title = f'<a href="{ctx.page(x["link"])}">{title}</a>'
            doi = f' DOI: <a href="https://doi.org/{e(x["doi"])}">{e(x["doi"])}</a>.' if x.get("doi") else ""
            extra = ""
            if x.get("file"):
                lk, _ = file_link(x["file"], ctx, "PDF", "")
                extra = " " + lk if "href" in lk else ""
            lis.append(f"<li>{e(ctx.t(x['authors']))} ({x['year']}). {title}. <em>{e(ctx.t(x['venue']))}</em>.{doi}{extra}</li>")
        parts.append(f"<h2>{e(T(label, lang))}</h2><ol class='refs'>{''.join(lis)}</ol>")
    body = f"<h1>{ctx.ui('publications')}</h1>" + "".join(parts)
    write(ctx, page(ctx, ctx.ui("publications"), body, active="publications.html"))


def build_collection(lang, c, path, active, parent=None):
    """Course or club category page: description, optional topic table, material groups."""
    ctx = Ctx(lang, path)
    meta = " · ".join(x for x in [ctx.t(c.get("where", "")), ctx.t(c.get("period", ""))] if x)
    topics = ""
    if c.get("topics"):
        rows = []
        for i, t in enumerate(c["topics"], 1):
            s, _ = file_link(t["slides"], ctx, ctx.ui("slides"), ctx.ui("no_file")) if t.get("slides") else (ctx.ui("no_file"), "")
            pr = []
            for f in t.get("practice", []):
                lk, _ = file_link(f["file"], ctx, ctx.t(f["label"]), "")
                if "href" in lk:
                    pr.append(lk)
            prc = "<br>".join(pr) if pr else f"<span class='muted'>{ctx.ui('no_file')}</span>"
            num = t.get("n", i)
            rows.append(f"<tr><td class='num'>{num}</td><td>{e(ctx.t(t['title']))}</td><td class='act'>{s}</td><td class='act' style='white-space:normal;width:190px'>{prc}</td></tr>")
        topics = (f"<h2>{e(ctx.t(c.get('topics_title', {'uk': 'Програма курсу', 'en': 'Course outline'})))}</h2>"
                  f"<table class='files'><thead><tr><th class='num'>№</th><th>{ctx.ui('topic')}</th><th class='act'>{ctx.ui('slides')}</th>"
                  f"<th class='act'>{ctx.ui('practice')}</th></tr></thead><tbody>{''.join(rows)}</tbody></table>")
    groups = ""
    for g in c.get("groups", []):
        desc = f"<p class='muted'>{e(ctx.t(g['desc']))}</p>" if g.get("desc") else ""
        groups += f"<h2>{e(ctx.t(g['title']))}</h2>{desc}{materials_table(g['items'], ctx)}"
    crumb = f"<p class='kicker'><a href='{ctx.page(parent[0])}'>{e(ctx.t(parent[1]))}</a></p>" if parent else ""
    sub = f"<p class='subtitle'><em>{e(ctx.t(c.get('subtitle', '')))}</em>{(' · ' + e(meta)) if meta else ''}</p>"
    body = f"{crumb}<h1>{e(ctx.t(c['title']))}</h1>{sub}{md(ctx.t(c['description']), ctx)}{topics}{groups}"
    write(ctx, page(ctx, ctx.t(c["title"]), body, active=active))


def build_teaching(lang):
    ctx = Ctx(lang, "teaching.html")
    cards = []
    for c in TEACHING["courses"]:
        cards.append(f"<div class='course'><h2><a href='{ctx.page(c['page'])}'>{e(ctx.t(c['title']))}</a></h2>"
                     f"<p class='muted'><em>{e(ctx.t(c['where']))}</em></p>{md(ctx.t(c['summary']), ctx)}"
                     f"<p><a href='{ctx.page(c['page'])}'>{ctx.ui('program')} →</a></p></div>")
    body = f"<h1>{ctx.ui('teaching')}</h1><p class='lead'>{e(ctx.t(TEACHING['intro']))}</p>" + "".join(cards)
    write(ctx, page(ctx, ctx.ui("teaching"), body, active="teaching.html"))


def build_club(lang, posts):
    ctx = Ctx(lang, "club.html")
    c = CLUB
    acts = "".join(f"<li>{e(a)}</li>" for a in ctx.t(c["activities"]))
    cards = "".join(
        f"<div class='card'><span class='tag'>{e(ctx.t(k['tag']))}</span><h3><a href='{ctx.page(k['page'])}'>{e(ctx.t(k['title']))}</a></h3>"
        f"<p>{e(ctx.t(k['desc']))}</p></div>" for k in c["categories"])
    notes = []
    for n in c["notes"]:
        files = []
        for f in n["files"]:
            lk, size = file_link(f["file"], ctx, ctx.t(f["label"]), "")
            if "href" in lk:
                files.append(f"{lk} <span class='muted'>({size})</span>")
        post = f" · <a href='{ctx.page('posts/' + n['post'] + '.html')}'>{ctx.ui('read_more')} →</a>" if n.get("post") else ""
        notes.append(f"<li><div class='date'>{e(ctx.t(n['date']))}</div><div><strong>{e(ctx.t(n['title']))}</strong>"
                     f"<p class='summary'>{e(ctx.t(n['desc']))}</p><p class='summary files-inline'>{' '.join(files)}{post}</p></div></li>")
    tg = c.get("telegram", "")
    tg_lbl = ctx.t({"uk": "Telegram-канал клубу", "en": "Club Telegram channel"})
    addr = "<br>".join(e(x) for x in ctx.t(c["contacts"]))
    body = f"""
<div class="club-head">
<img src="{ctx.static(c['logo'])}" alt="{e(ctx.t(c['name']))}" width="96" height="90">
<div><h1>{e(ctx.t(c['name']))}</h1>
<p class="subtitle">{e(ctx.t(c['role']))}</p>
<p class="club-links"><a class="btn" href="{tg}" target="_blank" rel="noopener">{tg_lbl} →</a> <a href="mailto:{c['email']}">{c['email']}</a></p></div>
</div>
<h2>{e(ctx.t({'uk': 'Про клуб', 'en': 'About the club'}))}</h2>
{md(ctx.t(c['about']), ctx)}
<ul>{acts}</ul>
<h2>{e(ctx.t({'uk': 'Курси та лекції клубу', 'en': 'Club courses and lectures'}))}</h2>
<div class="cards">{cards}</div>
<h2>{e(ctx.t({'uk': 'Аналітичні записки', 'en': 'Research notes'}))}</h2>
<ul class="posts">{''.join(notes)}</ul>
<h2>{e(ctx.t({'uk': 'Публікації клубу в блозі', 'en': 'Club posts'}))}</h2>
{post_list([p for p in posts if p['section'] == 'club'], ctx)}
<h2>{ctx.ui('contacts')}</h2>
<div class="club-contacts">
<p>{addr}</p>
<p><a href="mailto:{c['email']}">{c['email']}</a><br><a href="tel:{c['phone'].replace(' ', '')}">{c['phone']}</a><br>
<a href="{tg}" target="_blank" rel="noopener">t.me/macrofinoneu</a></p>
</div>
<p class="muted small">{e(ctx.t({'uk': 'Голова клубу', 'en': 'Head of the club'}))}: <a href="mailto:{c['contact']}">{c['contact']}</a></p>
"""
    write(ctx, page(ctx, ctx.ui("club"), body, active="club.html"))


def build_analytics(lang):
    ctx = Ctx(lang, "analytics.html")
    a = ANALYTICS
    charts = []
    for ch in a["charts"]:
        charts.append(f"<div class='chart'><h3>{e(ctx.t(ch['title']))}</h3><p>{e(ctx.t(ch['desc']))}</p><div id='{ch['id']}' class='chart-box'></div></div>")
    tools = []
    for tl in a["tools"]:
        fl = []
        for f in tl["files"]:
            lk, size = file_link(f["file"], ctx, ctx.t(f["label"]), "")
            if "href" in lk:
                fl.append(f"{lk} <span class='muted'>({size})</span>")
        tools.append(f"<div class='card'><span class='tag'>{e(ctx.t(tl['tag']))}</span><h3>{e(ctx.t(tl['title']))}</h3>"
                     f"{md(ctx.t(tl['desc']), ctx)}<p class='files-inline'>{' '.join(fl)}</p></div>")
    bank_charts = "".join(
        f"<div class='chart'><h3>{e(ctx.t(t))}</h3><div id='{i}' class='chart-box'></div></div>"
        for i, t in a["bank_charts"])
    dcards = "".join(
        f"<div class='card dash-card'><span class='tag'>{e(ctx.t(d['tag']))}</span>"
        f"<h3><a href='{ctx.page(d['page'])}'>{e(ctx.t(d['title']))}</a></h3><p>{e(ctx.t(d['desc']))}</p>"
        f"<p class='files-inline'><a class='btn' href='{ctx.page(d['page'])}'>{e(ctx.t(a['dash_page']))}</a></p></div>"
        for d in a["dashboards"])
    body = f"""
<h1>{ctx.ui('analytics')}</h1>
{md(ctx.t(a['intro']), ctx)}
<h2 id="apps">{e(ctx.t({'uk': 'Інтерактивні дашборди', 'en': 'Interactive dashboards'}))}</h2>
<div class="cards two">{dcards}</div>
<h2 id="dashboard">{e(ctx.t(a['dash_title']))}</h2>
<div class="dash-head"><p class="muted" style="margin:0">{e(ctx.t(a['dash_sub']))} <span id="asof"></span></p><div id="range" role="group"></div></div>
<p id="dash-error" class="note-box" hidden>{e(ctx.t(a['dash_error']))}</p>
<div id="kpis" class="kpis"></div>
<div class="dash-grid">{''.join(charts)}</div>
<h2 id="banks">{e(ctx.t(a['bank_title']))}</h2>
<p class="muted">{e(ctx.t(a['bank_sub']))}</p>
<div class="bank-pick"><select id="bank-select" aria-label="bank"></select><span id="bank-info" class="muted"></span></div>
<div class="dash-grid">{bank_charts}</div>
<p class="muted" style="font-size:13.5px">{md(ctx.t(a['dash_note']), ctx)[3:-4]}</p>
<h2 id="tools">{e(ctx.t(a['tools_title']))}</h2>
{md(ctx.t(a['tools_intro']), ctx)}
<div class="cards">{''.join(tools)}</div>
<h2 id="data">{e(ctx.t(a['data_title']))}</h2>
{groups_html(a['data_groups'], ctx)}
"""
    head = '<script defer src="https://cdn.plot.ly/plotly-2.35.2.min.js"></script>' + f'<script defer src="{ctx.static("dashboard.js")}"></script>'
    write(ctx, page(ctx, ctx.ui("analytics"), body, active="analytics.html", wide=True, extra_head=head))
    for d in a["dashboards"]:
        build_dashboard_page(lang, d)


def build_dashboard_page(lang, d):
    a = ANALYTICS
    ctx = Ctx(lang, d["page"])
    extra = ""
    if d.get("code"):
        lk, size = file_link(d["code"], ctx, ctx.t(a["dash_code"]), "")
        if "href" in lk:
            extra += f" <span>{lk} <span class='muted'>({size})</span></span>"
    if d.get("post"):
        extra += f" <a href='{ctx.page('posts/' + d['post'] + '.html')}'>{e(ctx.t({'uk': 'Огляд за жовтень 2026', 'en': 'October 2026 review'}))} →</a>"
    snap = ""
    if d["id"] == "ulci":
        snap = (f"<h2>{e(ctx.t({'uk': 'Знімок індексу', 'en': 'Index snapshot'}))}</h2>"
                + md("{{chart ulci_level | " + ctx.t({'uk': 'Рівень ULCI, 31.01.2021 = 100. Жовтень 2026 року за даними до 26 жовтня', 'en': 'ULCI level, 31 Jan 2021 = 100. October 2026 uses data to 26 October'})
                     + " | " + ctx.t({'uk': 'Джерело: розрахунки автора, ціни EODHD, курси ЄЦБ.', 'en': 'Source: author\'s calculations, EODHD prices, ECB FX rates.'}) + "}}", ctx))
    body = f"""
<p class="crumbs"><a href="{ctx.page('analytics.html')}">{ctx.ui('analytics')}</a> / {e(ctx.t(d['title']))}</p>
<h1>{e(ctx.t(d['title']))}</h1>
<p>{e(ctx.t(d['desc']))}</p>
<p class="dash-actions"><a class="btn" href="{d['url']}" target="_blank" rel="noopener">{e(ctx.t(a['dash_open']))}</a>{extra}</p>
<p class="muted" style="font-size:13.5px">{e(ctx.t(a['dash_sleep']))}</p>
<div class="embed"><iframe src="{d['url']}?embed=true&amp;embed_options=light_theme" title="{e(ctx.t(d['title']))}" loading="lazy" allow="clipboard-write; fullscreen"></iframe></div>
{snap}
"""
    head = CHART_HEAD.format(js=ctx.static("charts.js")) if snap else ""
    write(ctx, page(ctx, ctx.t(d["title"]), body, active="analytics.html", wide=True, extra_head=head))


# ---------------------------------------------------------------- main
def main():
    global SITE, MACROS, PROJECTS, RESEARCH_INTRO, BLOG_SECTIONS, BLOG_INTRO, TEACHING, CLUB, ANALYTICS
    SITE = load_yaml("site.yaml")
    MACROS = load_yaml("macros.yaml") or {}
    rs = load_yaml("research/index.yaml")
    RESEARCH_INTRO = rs.get("intro")
    PROJECTS = [load_yaml(f"research/{s}.yaml") for s in rs["order"]]
    bl = load_yaml("blog.yaml")
    BLOG_SECTIONS, BLOG_INTRO = bl["sections"], bl["intro"]
    TEACHING = load_yaml("teaching.yaml")
    CLUB = load_yaml("club.yaml")
    ANALYTICS = load_yaml("analytics.yaml")
    collections = load_yaml("collections.yaml")
    load_catalogs()

    if OUT.exists():
        shutil.rmtree(OUT)
    OUT.mkdir()
    shutil.copytree(ROOT / "static", OUT / "static")
    shutil.copytree(ROOT / "files", OUT / "files", ignore=shutil.ignore_patterns(".gitkeep", ".DS_Store"))
    (OUT / ".nojekyll").write_text("")

    for lang in LANGS:
        posts = load_posts(lang)
        build_index(lang, posts)
        build_research_hub(lang)
        for pr in PROJECTS:
            build_project(lang, pr, posts)
        build_blog(lang, posts)
        for p in posts:
            build_post(lang, p, posts)
        build_publications(lang)
        build_teaching(lang)
        build_club(lang, posts)
        build_analytics(lang)
        for col in collections:
            parent = (col["parent"], col["parent_label"]) if col.get("parent") else None
            build_collection(lang, col, col["path"], col["active"], parent)
    n = sum(1 for _ in OUT.rglob("*.html"))
    print(f"Готово / Done: {OUT}  ({n} HTML-сторінок{', з чернетками' if SHOW_DRAFTS else ''})")


if __name__ == "__main__":
    main()
