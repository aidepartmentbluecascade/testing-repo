#!/usr/bin/env python3
"""Rebuild the self-contained portal. Use --pdf path/to/workbook.pdf to replace the embedded source."""
from pathlib import Path
import argparse
import base64
import json
import re

root = Path(__file__).resolve().parent
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--pdf', type=Path)
args = parser.parse_args()
if args.pdf:
    raw = args.pdf.read_bytes()
    if not raw.startswith(b'%PDF-'):
        raise SystemExit('The selected file is not a PDF.')
    pdf64 = base64.b64encode(raw).decode('ascii')
else:
    existing = (root / 'index.html').read_text(encoding='utf-8')
    match = re.search(r'<script id="pdf-data"[^>]*>(.*?)</script>', existing, re.S)
    if not match:
        raise SystemExit('No embedded source PDF found. Rebuild with --pdf your_workbook.pdf')
    pdf64 = match.group(1).strip()
    if not base64.b64decode(pdf64).startswith(b'%PDF-'):
        raise SystemExit('The embedded PDF is not valid.')
course = json.loads((root / 'course.json').read_text(encoding='utf-8'))
values = {
    '__CSS__': (root / 'styles.css').read_text(encoding='utf-8'),
    '__DATA__': json.dumps(course, ensure_ascii=False).replace('</', '<\\/'),
    '__PDF__': pdf64,
    '__JS__': (root / 'app.js').read_text(encoding='utf-8').replace('</script', '<\\/script'),
}
html = (root / 'template.html').read_text(encoding='utf-8')
for key, value in values.items():
    html = html.replace(key, value)
(root / 'index.html').write_text(html, encoding='utf-8')
print('Rebuilt index.html. Reopen or refresh your browser to load the updated application.')
