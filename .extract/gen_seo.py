# -*- coding: utf-8 -*-
"""生成 sitemap.xml + robots.txt（自动化任务每日调用，确保新文章自动进 sitemap）

两个数据源必须与站点实际生成的路由一致：
- 产品：src/data/products/*.ts（站点真实渲染的产品集，slug 用连字符代替空格）
- 文章：src/data/resources.ts（仅当文章对象含 zh 内容时才收录中文页）
"""
import re, os
from datetime import date

BASE = "https://www.liocrebif-yaw.top"
TODAY = date.today().isoformat()
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def slugify(model):
    """型号 -> URL slug（与 src/data/products/slug.ts 保持一致）"""
    return re.sub(r"\s+", "-", model.lower())


# 1. 产品详情页：以站点数据为准
prod_dir = os.path.join(ROOT, "src", "data", "products")
products = []
for fn in sorted(os.listdir(prod_dir)):
    if not fn.endswith(".ts") or fn in ("types.ts", "index.ts", "slug.ts"):
        continue
    ts = open(os.path.join(prod_dir, fn), encoding="utf-8").read()
    products += re.findall(r"^\s{4}model: '([^']+)'", ts, re.M)

# 2. 资源文章：slug + 是否有中文版
articles = {}
ts_path = os.path.join(ROOT, "src", "data", "resources.ts")
if os.path.exists(ts_path):
    ts = open(ts_path, encoding="utf-8").read()
    for chunk in ts.split("slug: '")[1:]:
        m = re.match(r"([a-z0-9-]+)'", chunk)
        if not m:
            continue
        articles[m.group(1)] = bool(re.search(r"^\s{4}zh: \{", chunk, re.M))

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
for m in sorted(set(slugify(x) for x in products)):
    urls.append((f"{BASE}/products/{m}/", "0.7"))
    urls.append((f"{BASE}/zh/products/{m}/", "0.7"))
for sl, has_zh in sorted(articles.items()):
    urls.append((f"{BASE}/resources/{sl}/", "0.7"))
    if has_zh:
        urls.append((f"{BASE}/zh/resources/{sl}/", "0.7"))

xml = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
for loc, pri in urls:
    xml.append(f'  <url><loc>{loc}</loc><lastmod>{TODAY}</lastmod><priority>{pri}</priority></url>')
xml.append('</urlset>')
open(os.path.join(ROOT, "public", "sitemap.xml"), "w", encoding="utf-8").write("\n".join(xml))

robots = f"User-agent: *\nAllow: /\n\nSitemap: {BASE}/sitemap.xml\n"
open(os.path.join(ROOT, "public", "robots.txt"), "w", encoding="utf-8").write(robots)
print(f"sitemap: {len(urls)} URLs | 产品 {len(set(products))} | 文章 {len(articles)}（含中文 {sum(articles.values())}）| {TODAY}")
