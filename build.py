#!/usr/bin/env python3
"""Build a pair of UTF-8 static pages from the adjacent, curated content."""
import json
from html import escape
from pathlib import Path
import argparse

ROOT = Path(__file__).resolve().parent
SOURCE = "https://alpo.ge/remark.pdf"
VERIFY = "https://github.com/SINF-KEN/rh-lean-check"
CSS = """*{box-sizing:border-box}body{margin:0;padding:2rem 1rem;
font:1.08rem/1.6 system-ui,sans-serif;background:#f6f8fb;color:#172335}
main{max-width:46rem;margin:auto;background:white;padding:clamp(1rem,4vw,3rem);
border:1px solid #dce3ed;border-radius:1rem}h1,h2{line-height:1.2}
h1{font-size:clamp(1.8rem,6vw,3rem);margin-top:.5rem}
h2{font-size:1.35rem;margin:1.5rem 0 0}p{margin:.5rem 0 1rem}
nav{font-size:.95rem}a{color:#174a90;text-underline-offset:.2em}
a:focus-visible{outline:.18rem solid #174a90;outline-offset:.2rem}
.status{display:inline-block;background:#ffefce;color:#572e00;
padding:.25rem .6rem;border-radius:.3rem;font-weight:700}
footer{margin-top:2rem;padding-top:.8rem;border-top:1px solid #dce3ed}"""
FILES = {"en":"en.html", "ru":"ru.html"}

def page(lang, data):
    g = lambda key: escape(data[key])
    links = " · ".join(
        f'<a href="{FILES[k]}" lang="{k}" hreflang="{k}">' +
        ("English" if k == "en" else "Русский") + "</a>"
        if k != lang else f'<span aria-current="page" lang="{k}">' +
        ("English" if k == "en" else "Русский") + "</span>"
        for k in FILES
    )
    sections = "".join(f"<section><h2>{escape(h)}</h2><p>{escape(p)}</p></section>" for h,p in data["sections"])
    return f"""<!doctype html>
<html lang="{lang}">
<head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{g('title')}</title><meta name="description" content="{g('description')}">
<style>{CSS}</style></head>
<body><main><nav><a href="index.html">Русский / English</a> · {links}</nav>
<header><h1>{g('title')}</h1><p>{g('description')}</p><p class="status">{g('status')}</p></header>
{sections}
<footer><p><a href="{SOURCE}">{g('sourceLabel')}</a></p>
<p><a href="{VERIFY}">{g('verificationLabel')}</a></p></footer>
</main></body></html>
"""

def parallel(data):
    en, ru = data["en"], data["ru"]
    if len(en["sections"]) != len(ru["sections"]):
        raise ValueError("Russian and English sections must align")
    rows = []
    for left, right in zip(ru["sections"], en["sections"], strict=True):
        halves = "".join(
            f'<article lang="{lang}"><small>{label}</small><h2>{escape(h)}</h2><p>{escape(p)}</p></article>'
            for lang, label, (h, p) in (("ru", "РУССКИЙ", left), ("en", "ENGLISH", right))
        )
        rows.append(f'<div class="pair">{halves}</div>')
    extra = """
    main{max-width:72rem}.pair{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:1rem;margin:1rem 0}
    article{padding:1rem;border:1px solid #dce3ed;border-radius:.65rem;background:#f8faff}
    article h2{margin:.25rem 0 .5rem}article p{margin:0}small{letter-spacing:.12em;color:#334d6a}
    @media(max-width:43rem){.pair{grid-template-columns:1fr;gap:.45rem;margin:1.25rem 0}}
    """
    lines = "\n".join(rows)
    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Remark on RH Proof Grounded Hallucinated Proof Annotation Paper</title><style>{CSS}{extra}</style></head>
<body><main><header>
<nav><a href="ru.html" lang="ru">Только русский</a> · <a href="en.html">English only</a></nav>
<h1>Remark on RH Proof Grounded Hallucinated Proof Annotation Paper</h1>
<p>Independent reading companion to Levent Alpöge’s “Remark” (November 20, 2026). Original summaries and invented teaching examples, not a translation or proof.</p>
<p lang="ru">Самостоятельный обзор заметки Левента Алпёге от 20 ноября 2026 года. Краткое изложение и учебные примеры, не полный перевод и не доказательство.</p>
<p class="status">Claim not verified here · <span lang="ru">Утверждение здесь не проверено</span></p>
</header>{lines}
<footer><a href="{SOURCE}">Original PDF / <span lang="ru">Оригинал PDF</span></a> ·
<a href="{VERIFY}">Independent verification / <span lang="ru">Независимая проверка</span></a></footer>
</main></body></html>"""

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", type=Path, default=ROOT / "dist")
    args = parser.parse_args()
    data = json.loads((ROOT / "content.json").read_text(encoding="utf-8"))
    args.out.mkdir(parents=True, exist_ok=True)
    for lang, filename in FILES.items():
        (args.out / filename).write_text(page(lang, data[lang]), encoding="utf-8")

    (args.out / "index.html").write_text(parallel(data), encoding="utf-8")
