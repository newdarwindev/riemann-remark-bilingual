"""Create a one-page PDF of the original EN/RU summary, never the source PDF."""
from html import escape
from pathlib import Path
import json

from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

root = Path(__file__).resolve().parent
data = json.loads((root / "content.json").read_text(encoding="utf-8"))
font_dir = Path("/usr/share/fonts/truetype/dejavu")
pdfmetrics.registerFont(TTFont("Body", str(font_dir / "DejaVuSans.ttf")))
pdfmetrics.registerFont(TTFont("Heading", str(font_dir / "DejaVuSans-Bold.ttf")))
title = ParagraphStyle("title", fontName="Heading", fontSize=23, leading=28, textColor=colors.HexColor("#152642"))
status = ParagraphStyle("status", fontName="Heading", fontSize=9, leading=14, textColor=colors.HexColor("#754307"))
label = ParagraphStyle("label", fontName="Heading", fontSize=9, leading=12, textColor=colors.HexColor("#2a5178"))
head = ParagraphStyle("head", parent=label, fontSize=12, leading=16, spaceAfter=6)
body = ParagraphStyle("body", fontName="Body", fontSize=10, leading=15, alignment=TA_LEFT, textColor=colors.HexColor("#18263a"))
foot = ParagraphStyle("foot", parent=body, fontSize=8, leading=12)
path = root / "remark-summary-ru-en.pdf"
doc = SimpleDocTemplate(str(path), pagesize=(297*mm,210*mm), leftMargin=15*mm, rightMargin=15*mm,
                        topMargin=12*mm, bottomMargin=12*mm, title="Remark: bilingual reading companion")
story = [Paragraph("Remark · Русский / English", title), Spacer(1, 5),
         Paragraph("Краткий обзор / Original summary. Mathematical claim not verified here.", status), Spacer(1, 14)]
rows = [[Paragraph("РУССКИЙ",label),Paragraph("ENGLISH",label)]]
for ru, en in zip(data["ru"]["sections"], data["en"]["sections"], strict=True):
    rows.append([[Paragraph(escape(h),head),Paragraph(escape(p),body)] for h,p in (ru,en)])
t = Table(rows, colWidths=[doc.width/2]*2, hAlign="LEFT")
t.setStyle(TableStyle([("VALIGN",(0,0),(-1,-1),"TOP"),("ROWBACKGROUNDS",(0,0),(-1,-1),[colors.HexColor("#f0f5fa"),colors.white]),
  ("LINEBELOW",(0,0),(-1,-1),.45,colors.HexColor("#cfd9e6")),("LINEAFTER",(0,0),(0,-1),.45,colors.HexColor("#cfd9e6")),
  ("TOPPADDING",(0,0),(-1,-1),8),("BOTTOMPADDING",(0,0),(-1,-1),8),("LEFTPADDING",(0,0),(-1,-1),12),("RIGHTPADDING",(0,0),(-1,-1),12)]))
story += [t, Spacer(1, 14), Paragraph('Источник / Source: <link href="https://alpo.ge/remark.pdf" color="#174a90">Levent Alpöge, Remark (PDF)</link>. This page contains original summaries, not a full translation.', foot)]
doc.build(story)
print(path)
