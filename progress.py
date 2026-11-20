"""Build a static evidence inventory, not a proof-verification tracker."""
from html import escape
from pathlib import Path
import re

TOPICS = (
    ("Determinants", "Определители"), ("Positivity", "Положительность"),
    ("Towers", "Башни"), ("Finite moments", "Конечные моменты"),
    ("Period averages", "Средние по периоду"), ("Congruences", "Сравнения"),
)
CREDIT = "https://brunoloff.github.io/assets/rh-progress.html"
CSS = """
main{max-width:70rem}.chapter-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,15rem),1fr));gap:.75rem}
details{border:1px solid #bad0de;border-radius:.6rem;padding:.8rem;background:#f0f7fb;min-width:0}
summary{cursor:pointer;font-weight:bold}summary:focus-visible{outline:.18rem solid #174a90;outline-offset:.2rem}
.stats{display:flex;gap:1rem;flex-wrap:wrap;padding:0;list-style:none}.stats li{background:#e9f2fa;padding:.5rem .75rem;border-radius:.4rem}
.line-track{height:.5rem;background:#d3e2ed;margin:.7rem 0;border-radius:.3rem;overflow:hidden}
.line-fill{display:block;height:100%;background:#226284}
.steps{padding-inline-start:1.3rem}
"""

def dashboard(root):
    files = sorted((root / "toy-lean").glob("0*.lean"))
    if len(files) != len(TOPICS):
        raise ValueError("Expected six numbered chapter files")
    rows = []
    for file, (en, ru) in zip(files, TOPICS, strict=True):
        raw = file.read_bytes()
        src = raw.decode("utf-8")
        rows.append((file.name, en, ru, len(src.splitlines()), len(raw),
                     len(re.findall(r"^theorem case_\d+\s*:", src, re.M))))
    cards = []
    cap = max(row[3] for row in rows)
    for name, en, ru, lines, size, cases in rows:
        cards.append(f"""<details><summary>{escape(en)} / <span lang="ru">{escape(ru)}</span></summary>
<div class="line-track" aria-hidden="true"><span class="line-fill" style="width:{lines/cap:.1%}"></span></div>
<p>{lines:,} lines / <span lang="ru">строк</span> · {size:,} bytes / <span lang="ru">байт</span></p>
<p>{cases:,} generated examples / <span lang="ru">учебных примеров</span></p><p><code>{escape(name)}</code></p></details>""")
    return f"""<style>{CSS}</style><section aria-labelledby="toy-progress">
<h2 id="toy-progress">Toy Lean corpus / <span lang="ru">Учебный корпус Lean</span></h2>
<p>Static snapshot of the six generated chapter files; totals exclude the support module. It does not track the original proof.</p>
<p lang="ru">Статический снимок шести сгенерированных глав; вспомогательный модуль не учитывается. Это не отчёт о проверке оригинального доказательства.</p>
<ul class="stats"><li>{len(rows)} chapters / <span lang="ru">глав</span></li>
<li>{sum(row[5] for row in rows):,} examples / <span lang="ru">примеров</span></li>
<li>{sum(row[3] for row in rows):,} lines / <span lang="ru">строк</span></li></ul>
<ol class="steps"><li>Sources generated / <span lang="ru">исходники сгенерированы</span></li>
<li>Lean compilation not run / <span lang="ru">компиляция Lean не запускалась</span></li>
<li>RH and GRH not verified here / <span lang="ru">RH и GRH здесь не проверены</span></li></ol>
<p>Open each chapter for counts. Bars compare source lines with the largest chapter, not verification progress.</p>
<p lang="ru">Откройте главу для подробностей. Полосы показывают объём исходников относительно самой большой главы, а не прогресс проверки.</p>
<div class="chapter-grid">{''.join(cards)}</div>
<p><a href="{CREDIT}">Dashboard inspiration: Bruno Loff’s RH Lean check</a></p></section>"""
