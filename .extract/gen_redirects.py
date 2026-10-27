# -*- coding: utf-8 -*-
"""生成 public/_redirects：固定跳转 + 自动补齐「无中文版的文章」的 /zh/ 跳转

GSC 报 404 的页面大多是旧 sitemap 里 /zh/resources/<slug>/（英文-only 文章没有中文页），
统一 301 到英文原文，而不是留 404。
"""
import os, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "public", "_redirects")

STATIC = [
    ("/products/lkf-pm/", "/products/lkf-pm-pcf/"),
    ("/zh/products/lkf-pm/", "/zh/products/lkf-pm-pcf/"),
    ("/products/lkf-g652-low-water-peak/", "/products/lkf-g652/"),
    ("/zh/products/lkf-g652-low-water-peak/", "/zh/products/lkf-g652/"),
    # 合订产品拆分：旧页指向其主要子产品
    ("/products/lkf-fiber-adhesive/", "/products/lkf-uv500/"),
    ("/zh/products/lkf-fiber-adhesive/", "/zh/products/lkf-uv500/"),
    ("/products/lkf-fiber-preform/", "/products/lkf-boron-doped/"),
    ("/zh/products/lkf-fiber-preform/", "/zh/products/lkf-boron-doped/"),
    # 已下线产品（历史上进过 sitemap）
    ("/products/lkf-fiber%20coil%20bobbin/", "/products/fiber-optic/"),
    ("/zh/products/lkf-fiber%20coil%20bobbin/", "/zh/products/fiber-optic/"),
]

# 英文-only 文章：中文页 301 到英文原文
ts = open(os.path.join(ROOT, "src", "data", "resources.ts"), encoding="utf-8").read()
en_only = []
for chunk in ts.split("slug: '")[1:]:
    m = re.match(r"([a-z0-9-]+)'", chunk)
    if not m:
        continue
    if not re.search(r"^\s{4}zh: \{", chunk, re.M):
        en_only.append(m.group(1))

lines = ["# 自动生成：改 .extract/gen_redirects.py 后重跑，勿手改", ""]
for src, dst in STATIC:
    lines.append(f"{src} {dst} 301")
lines.append("")
for sl in en_only:
    lines.append(f"/zh/resources/{sl}/ /resources/{sl}/ 301")
lines.append("")

open(OUT, "w", encoding="utf-8").write("\n".join(lines))
print(f"写入 {OUT} | 固定 {len(STATIC)} 条 + 中文跳英文 {len(en_only)} 条")
