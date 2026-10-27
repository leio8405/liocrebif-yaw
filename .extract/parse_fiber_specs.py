# -*- coding: utf-8 -*-
"""从源 docx 生成单模光纤（LKF-G652 / G657 各三款）的完整参数表覆盖数据

目录 md 缺光学段、且 4 列表把「数据」列取成了「条件」列（页面上显示 --），
故改由 docx 重建：中文简介表 + 英文 DataSheet 表逐行对齐（同 V3.0），
条件并进参数名、值单列。

输出 .extract/spec_override.json：{slug: {headers, rows}}，由 gen_ts 按 slug 覆盖。
"""
import json, os, re, zipfile

SRC = r"D:\利科夫\2026年产品资料-利科夫\6、光纤陀螺解决方案\002.单模光纤"
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "spec_override.json")

PRODUCTS = {
    # LKF-G652 系列
    "lkf-g652": (
        "G652/1、LKF-G652低水峰单模光纤简介V3.0_三页_中文.docx",
        "G652/1.1、LKF-G652 Low-Water Peak Single-Mode Fiber V3.0 Data Sheet _EN.docx",
    ),
    "lkf-g652-low-loss": (
        "G652/2、LKF-G652低损耗单模光纤简介V3.0_三页_中文.docx",
        "G652/2.1、LKF-G652 Low-Loss Single-Mode Fiber V3.0 Data Sheet _EN.docx",
    ),
    "lkf-g652-ultra-low-loss": (
        "G652/3、LKF-G652超低损耗单模光纤简介V3.0_三页_中文.docx",
        "G652/3.1、LKF-G652 Ultra Low-Loss Single-Mode Fiber V3.0 Data Sheet _EN.docx",
    ),
    # LKF-G657 系列（B3 的英文 DataSheet 文件名误写 A1，内文标题为 B3）
    "lkf-g657a1": (
        "G657/2、LKF-G657A1低损耗弯曲不敏感单模光纤简介V3.0_三页_中文.docx",
        "G657/2.1、LKF-G657A1 Low-Loss Bend-Insensitive Single-Mode Fiber V3.0 Data Sheet _EN.docx",
    ),
    "lkf-g657a2": (
        "G657/1、LKF-G657A2低水峰弯曲不敏感单模光纤简介V3.0_三页_中文.docx",
        "G657/1.1、LKF-G657A2 Low Water Peak Bend-Insensitive Single-Mode Fiber V3.0 Data Sheet _EN.docx",
    ),
    "lkf-g657b3": (
        "G657/3、LKF-G657B3超强弯曲不敏感单模光纤简介V3.0_三页_中文.docx",
        "G657/3.1、LKF-G657A1 Ultra-Strong Bend-Insensitive Single-Mode Fiber V3.0 Data Sheet _EN.docx",
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
        if conds:
            joined = "，".join(conds)
            label = last_k + ("（" + joined + "）" if "（" not in conds[0] else " " + joined)
        else:
            label = last_k
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
