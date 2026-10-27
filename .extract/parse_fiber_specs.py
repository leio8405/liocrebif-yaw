# -*- coding: utf-8 -*-
"""从源 docx 生成 LKF-G652 三款光纤的完整参数表覆盖数据（目录 md 缺光学段且取值列错位）

输出 .extract/spec_override.json：{slug: {headers, rows}}，由 gen_ts 在生成时覆盖。
中文表与英文 DataSheet 表格逐行对齐（同版本 V3.0），条件并进参数名，值单列。
"""
import json, os, re, zipfile

SRC = r"D:\利科夫\2026年产品资料-利科夫\6、光纤陀螺解决方案\002.单模光纤\G652"
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "spec_override.json")

PRODUCTS = {
    "lkf-g652": (
        r"1、LKF-G652低水峰单模光纤简介V3.0_三页_中文.docx",
        r"1.1、LKF-G652 Low-Water Peak Single-Mode Fiber V3.0 Data Sheet _EN.docx",
    ),
    "lkf-g652-low-loss": (
        r"2、LKF-G652低损耗单模光纤简介V3.0_三页_中文.docx",
        r"2.1、LKF-G652 Low-Loss Single-Mode Fiber V3.0 Data Sheet _EN.docx",
    ),
    "lkf-g652-ultra-low-loss": (
        r"3、LKF-G652超低损耗单模光纤简介V3.0_三页_中文.docx",
        r"3.1、LKF-G652 Ultra Low-Loss Single-Mode Fiber V3.0 Data Sheet _EN.docx",
    ),
}


def tables(path):
    with zipfile.ZipFile(os.path.join(SRC, path)) as z:
        xml = z.read("word/document.xml").decode("utf-8", "ignore")
    out = []
    for tbl in re.findall(r"<w:tbl>.*?</w:tbl>", xml, re.S):
        rows = []
        for tr in re.findall(r"<w:tr[ >].*?</w:tr>", tbl, re.S):
            cells = []
            for tc in re.findall(r"<w:tc>.*?</w:tc>", tr, re.S):
                cells.append("".join(re.findall(r"<w:t[^>]*>([^<]*)</w:t>", tc)).strip())
            if any(cells):
                rows.append(cells)
        if rows:
            out.append(rows)
    return out


def flat(rows):
    """把 (特性|条件…|数据) 压成 [(特性+条件, 值)]"""
    out, last_k = [], ""
    for cells in rows:
        if len(cells) == 1:          # 分节标题（光学特性/几何特性…）
            continue
        k = cells[0].strip()
        if k in ("特性", "Parameter", "项目"):
            continue
        if k:
            last_k = k
        conds = [c.strip() for c in cells[1:-1] if c.strip() and c.strip() != "--"]
        val = cells[-1].strip()
        if not last_k or not val:
            continue
        label = last_k + ("（" + "，".join(conds) + "）" if conds and "（" not in conds[0] else (" " + "，".join(conds) if conds else ""))
        out.append((label, val))
    return out


override = {}
for slug, (zh_doc, en_doc) in PRODUCTS.items():
    zh = flat([r for t in tables(zh_doc)[:2] for r in t])
    en = flat([r for t in tables(en_doc)[:2] for r in t])
    if len(zh) != len(en):
        print(f"⚠️ {slug}: 中文 {len(zh)} 行 / 英文 {len(en)} 行 不对齐，跳过")
        continue
    rows = []
    for (k, v), (k_en, v_en) in zip(zh, en):
        k_en = k_en.replace("（", " (").replace("）", ")")
        rows.append({"k": k, "kEn": k_en, "v": [v], "vEn": [v_en]})
    override[slug] = {"headers": ["特性", "数据"], "rows": rows}
    print(f"✓ {slug}: {len(rows)} 行")

json.dump(override, open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("写入:", OUT)

sample = override.get("lkf-g652-low-loss", {}).get("rows", [])[:6]
for r in sample:
    print("   样例 |", r["k"], "=", r["v"][0], "||", r["kEn"], "=", r["vEn"][0])
