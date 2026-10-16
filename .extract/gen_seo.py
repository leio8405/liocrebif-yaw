# -*- coding: utf-8 -*-
"""生成 sitemap.xml + robots.txt（自动化任务每日调用，确保新文章自动进 sitemap）"""
import json, re, os
from datetime import date

BASE = "https://www.liocrebif-yaw.top"
TODAY = date.today().isoformat()
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 1. 产品详情页（assembled.json）
products = []
if os.path.exists(os.path.join(os.path.dirname(__file__), "assembled.json")):
    data = json.load(open(os.path.join(os.path.dirname(__file__), "assembled.json"), encoding="utf-8"))
    products = [r["model"].lower() for r in data]

# 2. 资源文章 slug（从 resources.ts 提取）
ts_path = os.path.join(ROOT, "src", "data", "resources.ts")
slugs = []
if os.path.exists(ts_path):
    ts = open(ts_path, encoding="utf-8").read()
    slugs = re.findall(r"slug:\s*'([a-z0-9-]+)'", ts)

# 3. 组装 URL
static_pages = ["/", "/about/", "/contact/", "/products/",
                "/products/fog-gyroscopes/", "/products/mems-gyroscopes/", "/products/imu/",
                "/products/inertial-navigation-systems/", "/products/accelerometers/", "/products/fiber-optic/",
                "/resources/"]
urls = []
for p in static_pages:
    pri = "1.0" if p == "/" else ("0.9" if p in ("/products/", "/resources/") else "0.8")
    urls.append((BASE + p, pri))
    urls.append((BASE + "/zh" + p, pri))
for m in sorted(set(products)):
    urls.append((f"{BASE}/products/{m}/", "0.7"))
    urls.append((f"{BASE}/zh/products/{m}/", "0.7"))
for sl in sorted(set(slugs)):
    urls.append((f"{BASE}/resources/{sl}/", "0.7"))
    urls.append((f"{BASE}/zh/resources/{sl}/", "0.7"))

xml = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
for loc, pri in urls:
    xml.append(f'  <url><loc>{loc}</loc><lastmod>{TODAY}</lastmod><priority>{pri}</priority></url>')
xml.append('</urlset>')
open(os.path.join(ROOT, "public", "sitemap.xml"), "w", encoding="utf-8").write("\n".join(xml))

robots = f"User-agent: *\nAllow: /\n\nSitemap: {BASE}/sitemap.xml\n"
open(os.path.join(ROOT, "public", "robots.txt"), "w", encoding="utf-8").write(robots)
print(f"sitemap: {len(urls)} URLs | robots.txt | {TODAY}")
