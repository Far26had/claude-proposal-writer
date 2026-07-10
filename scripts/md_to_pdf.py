#!/usr/bin/env python3
"""
تبدیل پروپوزالِ Markdown به PDF فارسیِ راست‌به‌چپ با ظاهرِ حرفه‌ای و برندِ آیوند.
مسیر: Markdown -> HTML استایل‌دار (RTL، فونت Vazirmatn جاسازی‌شده) -> PDF از Chrome/Edge headless.

استفاده:
    python md_to_pdf.py input.md [output.pdf]
"""
import sys
import os
import base64
import subprocess
import tempfile

import markdown  # pip install markdown

HERE = os.path.dirname(os.path.abspath(__file__))
FONT_DIR = os.path.join(HERE, "fonts")

CHROME_CANDIDATES = [
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
    r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
]

# ---- رنگ‌های سازمانیِ آیوند (استخراج‌شده از aivand.com) ----
NAVY = "#0e1a2b"       # سرمه‌ای اصلی (تیترها، متن)
NAVY2 = "#16263d"
GOLD = "#c8943b"       # طلاییِ برند (اکسنت)
GOLD_DARK = "#9a6f1f"
GOLD_SOFT = "#e3c489"
TEAL = "#2c7a7b"       # فیروزه‌ای (اکسنت دوم)
PAPER = "#fbf9f4"      # پس‌زمینه‌ی کاغذی
PAPER_SOFT = "#f4f0e7"
BORDER = "#e7e1d4"
MUTED = "#5b6675"


def _font_face(family, filename, weight):
    path = os.path.join(FONT_DIR, filename)
    with open(path, "rb") as f:
        b64 = base64.b64encode(f.read()).decode("ascii")
    return (
        f"@font-face{{font-family:'{family}';font-style:normal;"
        f"font-weight:{weight};src:url(data:font/woff2;base64,{b64}) "
        f"format('woff2');}}"
    )


def build_css():
    faces = "".join([
        _font_face("Vazirmatn", "Vazirmatn-Regular.woff2", 400),
        _font_face("Vazirmatn", "Vazirmatn-Medium.woff2", 500),
        _font_face("Vazirmatn", "Vazirmatn-Bold.woff2", 700),
    ])
    return faces + f"""
@page {{ size: A4; margin: 18mm 16mm; }}
* {{ box-sizing: border-box; }}
body {{
    font-family: "Vazirmatn", "Segoe UI", "Tahoma", sans-serif;
    direction: rtl; text-align: right;
    color: {NAVY}; line-height: 1.9; font-size: 12pt;
    background: #fff;
    -webkit-print-color-adjust: exact; print-color-adjust: exact;
}}
h1 {{
    font-size: 21pt; font-weight: 700; color: {NAVY}; margin: 0 0 4pt;
    border-bottom: 3px solid {GOLD}; padding-bottom: 10pt; line-height: 1.5;
}}
h2 {{
    font-size: 15pt; font-weight: 700; color: {NAVY}; margin: 22pt 0 8pt;
    padding-right: 10pt; border-right: 4px solid {GOLD};
    page-break-after: avoid;
}}
h3 {{ font-size: 13pt; font-weight: 500; color: {TEAL}; margin: 14pt 0 6pt; }}
p {{ margin: 6pt 0; }}
strong {{ color: {NAVY2}; font-weight: 700; }}
a {{ color: {GOLD_DARK}; text-decoration: none; }}
ul, ol {{ margin: 6pt 0; padding-right: 22pt; }}
li {{ margin: 3pt 0; }}
li::marker {{ color: {GOLD}; }}
hr {{ border: none; border-top: 1px solid {BORDER}; margin: 16pt 0; }}
blockquote {{
    margin: 12pt 0; padding: 10pt 14pt;
    background: {PAPER_SOFT}; border-right: 4px solid {GOLD};
    color: {NAVY2}; border-radius: 4px;
}}
table {{
    border-collapse: collapse; width: 100%; margin: 10pt 0; font-size: 11pt;
    page-break-inside: avoid;
}}
th, td {{ border: 1px solid {BORDER}; padding: 7pt 10pt; text-align: right; }}
thead th {{ background: {NAVY}; color: {PAPER}; font-weight: 700; }}
tbody tr:nth-child(even) {{ background: {PAPER}; }}
table, blockquote {{ page-break-inside: avoid; }}
"""


def convert(md_path, pdf_path=None):
    with open(md_path, encoding="utf-8") as f:
        text = f.read()

    if pdf_path is None:
        pdf_path = os.path.splitext(md_path)[0] + ".pdf"
    # Chrome resolves --print-to-pdf relative to its own cwd, so force absolute.
    pdf_path = os.path.abspath(pdf_path)

    html_body = markdown.markdown(text, extensions=["tables", "sane_lists"])
    html = f"""<!DOCTYPE html>
<html lang="fa" dir="rtl"><head><meta charset="utf-8">
<style>{build_css()}</style></head><body>{html_body}</body></html>"""

    tmp_html = tempfile.NamedTemporaryFile(
        suffix=".html", delete=False, mode="w", encoding="utf-8"
    )
    tmp_html.write(html)
    tmp_html.close()

    chrome = next((c for c in CHROME_CANDIDATES if os.path.exists(c)), None)
    if not chrome:
        raise SystemExit("Chrome/Edge not found. Install Chrome or Edge.")

    file_url = "file:///" + tmp_html.name.replace("\\", "/")
    subprocess.run([
        chrome, "--headless", "--disable-gpu", "--no-pdf-header-footer",
        f"--print-to-pdf={pdf_path}", file_url,
    ], check=True)
    os.unlink(tmp_html.name)
    print(f"PDF created: {pdf_path}")
    return pdf_path


if __name__ == "__main__":
    if len(sys.argv) < 2:
        raise SystemExit("Usage: python md_to_pdf.py input.md [output.pdf]")
    convert(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else None)
