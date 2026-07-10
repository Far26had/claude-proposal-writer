#!/usr/bin/env python3
"""
تبدیل پروپوزالِ Markdown به PDF فارسیِ راست‌به‌چپ با ظاهرِ حرفه‌ای.
مسیر: Markdown -> HTML استایل‌دار (RTL) -> PDF از طریق Chrome/Edge headless.

استفاده:
    python md_to_pdf.py input.md [output.pdf]
"""
import sys
import os
import re
import subprocess
import tempfile

import markdown  # pip install markdown

CHROME_CANDIDATES = [
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
    r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
]

CSS = """
@page { size: A4; margin: 18mm 16mm; }
* { box-sizing: border-box; }
body {
    font-family: "Vazirmatn", "IRANSans", "Segoe UI", "Tahoma", sans-serif;
    direction: rtl; text-align: right;
    color: #1f2933; line-height: 1.9; font-size: 12pt;
    -webkit-print-color-adjust: exact; print-color-adjust: exact;
}
h1 {
    font-size: 21pt; color: #0f766e; margin: 0 0 4pt;
    border-bottom: 3px solid #0f766e; padding-bottom: 10pt; line-height: 1.5;
}
h2 {
    font-size: 15pt; color: #0f766e; margin: 22pt 0 8pt;
    padding-right: 10pt; border-right: 4px solid #14b8a6;
}
h3 { font-size: 13pt; color: #334e68; margin: 14pt 0 6pt; }
p { margin: 6pt 0; }
strong { color: #102a43; }
a { color: #0f766e; text-decoration: none; }
ul, ol { margin: 6pt 0; padding-right: 22pt; }
li { margin: 3pt 0; }
hr { border: none; border-top: 1px solid #d9e2ec; margin: 16pt 0; }
blockquote {
    margin: 12pt 0; padding: 10pt 14pt;
    background: #f0fdfa; border-right: 4px solid #14b8a6;
    color: #134e4a; border-radius: 4px;
}
table {
    border-collapse: collapse; width: 100%; margin: 10pt 0; font-size: 11pt;
    page-break-inside: avoid;
}
th, td { border: 1px solid #d9e2ec; padding: 7pt 10pt; text-align: right; }
thead th { background: #0f766e; color: #fff; font-weight: 700; }
tbody tr:nth-child(even) { background: #f7fafc; }
h2 { page-break-after: avoid; }
table, blockquote { page-break-inside: avoid; }
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
<style>{CSS}</style></head><body>{html_body}</body></html>"""

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
