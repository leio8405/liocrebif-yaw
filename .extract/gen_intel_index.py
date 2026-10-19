# -*- coding: utf-8 -*-
"""行业情报周报归档索引生成器
扫描 public/zh/intel/*.html（排除 index.html），从各期 <title> 提取标题，
按文件名倒序（最新在前）生成归档页 index.html。
用法：python gen_intel_index.py
新增一期：把新期 HTML（ASCII 文件名，如 2026-W43-01.html）拷进 public/zh/intel/，再跑本脚本。
"""
import os
import re
from datetime import date

INTEL_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                         "public", "zh", "intel")

pages = []
for f in sorted(os.listdir(INTEL_DIR), reverse=True):
    if not f.endswith(".html") or f == "index.html":
        continue
    html = open(os.path.join(INTEL_DIR, f), encoding="utf-8").read()
    m = re.search(r"<title>(.*?)</title>", html, re.S)
    title = m.group(1).strip() if m else f
    # 从文件名提取周标识（如 2026-W42）
    wm = re.search(r"(\d{4}-W\d{2})", f)
    week = wm.group(1) if wm else ""
    pages.append((f, title, week))

items = "\n".join(
    f'''    <a class="row" href="{fname}">
      <span class="week">{week}</span>
      <span class="t">{title}</span>
      <span class="arrow">→</span>
    </a>'''
    for fname, title, week in pages
)

html = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>行业情报周报 · 归档 | Liocrebif</title>
<meta name="robots" content="noindex, follow">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Noto+Serif+SC:wght@400;600;700&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
<style>
  :root {{
    --paper: #f9f7f2; --paper-2: #f1eee6; --rule: #d8d3c6;
    --ink: #2b2924; --muted: #7a756a; --accent: #b4342a;
  }}
  * {{ margin: 0; padding: 0; box-sizing: border-box; }}
  body {{
    font-family: "Noto Serif SC", "Songti SC", serif;
    background: var(--paper); color: var(--ink);
    max-width: 760px; margin: 0 auto; padding: 48px 20px 64px;
  }}
  .kicker {{ font-family: "JetBrains Mono", monospace; font-size: 11px;
    letter-spacing: .12em; color: var(--accent); text-transform: uppercase; }}
  h1 {{ font-size: 28px; font-weight: 700; margin: 10px 0 6px; }}
  .sub {{ color: var(--muted); font-size: 14px; margin-bottom: 36px; }}
  .list {{ border-top: 1px solid var(--rule); }}
  .row {{
    display: flex; align-items: baseline; gap: 16px;
    padding: 18px 4px; border-bottom: 1px solid var(--rule);
    text-decoration: none; color: var(--ink); transition: background .15s;
  }}
  .row:hover {{ background: var(--paper-2); }}
  .week {{ font-family: "JetBrains Mono", monospace; font-size: 12px;
    color: var(--accent); min-width: 76px; }}
  .t {{ flex: 1; font-size: 16px; font-weight: 600; }}
  .arrow {{ color: var(--muted); }}
  .back {{ display: inline-block; margin-top: 32px; font-size: 13px;
    color: var(--muted); text-decoration: none; font-family: "JetBrains Mono", monospace; }}
  .back:hover {{ color: var(--accent); }}
</style>
</head>
<body>
  <p class="kicker">Industry Intelligence · Weekly</p>
  <h1>惯性导航行业情报 · 归档</h1>
  <p class="sub">每周精选惯性导航行业动态、技术进展与市场情报。共 {len(pages)} 期。</p>
  <div class="list">
{items}
  </div>
  <a class="back" href="/zh/">← 返回首页</a>
  <p style="margin-top:24px;font-size:11px;color:var(--muted);font-family:'JetBrains Mono',monospace;">更新于 {date.today().isoformat()} · Wuhan Liocrebif Technology</p>
</body>
</html>
'''
open(os.path.join(INTEL_DIR, "index.html"), "w", encoding="utf-8").write(html)
print(f"归档页已生成：{len(pages)} 期")
