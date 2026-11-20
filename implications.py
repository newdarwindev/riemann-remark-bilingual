"""Static bilingual impact tables; no network or third-party scripts."""
import json
from html import escape
from pathlib import Path

STYLE = """
main{max-width:73rem}.intro{font-size:1.17rem;max-width:68ch}
table{width:100%;border-collapse:collapse;margin:1rem 0 2rem;font-size:.96rem}
th,td{padding:.8rem;text-align:left;vertical-align:top;border-bottom:1px solid #bdd0df}
thead th{background:#173650;color:white}tbody th{width:22%;color:#15344b;background:#eff6fa}
td{width:26%;overflow-wrap:anywhere}
caption{text-align:left;font-size:1.3rem;font-weight:700;margin-bottom:.6rem}
.callout{padding:.7rem 1rem;border-left:.35rem solid #b55e17;background:#fff1df}
@media(max-width:44rem){table,tbody,tr,td,th{display:block;width:100%}
thead{position:absolute;width:1px;height:1px;overflow:hidden;clip-path:inset(50%)}
tbody tr{border:1px solid #bdd0df;border-radius:.5rem;margin-bottom:.7rem;overflow:hidden}
tbody td:before{content:attr(data-label);display:block;font-weight:700;color:#204a69}
tbody th{width:100%}}
"""

def write_implications(root: Path, out: Path, common_css: str):
    data = json.loads((root / "implications.json").read_text(encoding="utf-8"))
    for lang, page in data.items():
        other = "ru" if lang == "en" else "en"
        parts = []
        labels = page["headers"]
        for group, rows in page["tables"]:
            body = []
            for topic, claim, limit, sources in rows:
                cells = ''.join(f'<td data-label="{escape(label)}">{escape(value)}</td>'
                                for label, value in zip(labels[1:3], (claim, limit), strict=True))
                refs = '<br>'.join(f'<a href="{escape(url)}">{escape(label)}</a>' for label, url in sources)
                body.append(f'<tr><th scope="row">{escape(topic)}</th>{cells}<td data-label="{escape(labels[3])}">{refs}</td></tr>')
            cols = ''.join(f'<th scope="col">{escape(label)}</th>' for label in labels)
            parts.append(f'<table><caption>{escape(group)}</caption><thead><tr>{cols}</tr></thead><tbody>{"".join(body)}</tbody></table>')
        title = escape(page["title"])
        html = f'''<!doctype html><html lang="{lang}"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1"><title>{title}</title>
<style>{common_css}{STYLE}</style></head><body><main>
<nav><a href="index.html">{escape(page["home"])}</a> · <a href="implications-{other}.html" hreflang="{other}" lang="{other}">{escape(page["other"])}</a></nav>
<h1>{title}</h1><p class="intro">{escape(page["intro"])}</p>
<p class="callout">{escape(page["boundary"])}</p>{''.join(parts)}
<footer><p>{escape(page["note"])}</p></footer></main></body></html>
'''
        (out / f"implications-{lang}.html").write_text(html, encoding="utf-8")
