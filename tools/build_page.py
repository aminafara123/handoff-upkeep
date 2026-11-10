#!/usr/bin/env python3
"""Render README.md to docs/index.html with a plain stylesheet. Run after any README change."""
import re, markdown, pathlib
root = pathlib.Path(__file__).resolve().parent.parent
md = (root / "README.md").read_text()
md = re.sub(r"^Also published as a page: .*\n", "", md, flags=re.M).replace("docs/img/", "img/")
body = markdown.markdown(md, extensions=["tables", "nl2br", "fenced_code"])
css = """
body{font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Helvetica,Arial,sans-serif;font-size:16px;line-height:1.5;color:#1f2328;background:#fff;max-width:860px;margin:0 auto;padding:32px 16px}
h1,h2{border-bottom:1px solid #d0d7de;padding-bottom:.3em}h1{font-size:2em}h2{font-size:1.5em;margin-top:1.6em}h3{font-size:1.25em;margin-top:1.4em}
a{color:#0969da}img{max-width:100%;height:auto}
table{border-collapse:collapse;display:block;overflow-x:auto;max-width:100%;margin:1em 0}th,td{border:1px solid #d0d7de;padding:6px 13px;text-align:left;vertical-align:top}tr:nth-child(2n){background:#f6f8fa}
code{font-family:ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;font-size:85%;background:#f6f8fa;padding:.2em .4em;border-radius:6px}pre{background:#f6f8fa;padding:16px;overflow:auto;border-radius:6px}pre code{background:none;padding:0}
@media (prefers-color-scheme: dark){body{color:#e6edf3;background:#0d1117}h1,h2{border-color:#30363d}th,td{border-color:#30363d}tr:nth-child(2n){background:#161b22}code,pre{background:#161b22}a{color:#4493f8}}
"""
html = f'<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>Handoff Upkeep</title><style>{css}</style></head>\n<body>\n{body}\n<p><a href="https://github.com/aminafara123/handoff-upkeep">Source on GitHub</a></p>\n</body></html>\n'
(root / "docs" / "index.html").write_text(html)
print("docs/index.html", len(html), "bytes")
