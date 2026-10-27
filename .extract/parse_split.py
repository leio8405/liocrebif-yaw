# -*- coding: utf-8 -*-
"""把「光纤胶水」「光纤预制棒」两个合订产品拆成 6 个独立产品

- 胶水 → LKF-UV500 / LKF-UV100 / LKF-H01（型号取自文档标题 LKF-UV100/UV500/H01）
- 预制棒 → LKF-Boron-Doped / LKF-Fluorine-Doped / LKF-Germanium-Doped（文档内标题）
- 参数表按 gridSpan 展开合并单元格；中文表与英文表逐行对齐后合并
输出 .extract/split_products.json：{原 model: [新产品记录...]}，由 gen_ts 替换原记录。
"""
import json, os, re, zipfile

SRC = r"D:\利科夫\2026年产品资料-利科夫\6、光纤陀螺解决方案"
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "split_products.json")

DOCS = {
    "adhesive": (
        os.path.join(SRC, r"009.胶水\1、LKF-光纤胶水简介V3.0_双页_中文.docx"),
        os.path.join(SRC, r"009.胶水\1.1、LKF-Fiber Adhesive V3.0 Data Sheet _EN.docx"),
    ),
    "preform": (
        os.path.join(SRC, r"010.光纤预制棒\1、LKF-光纤预制棒简介V3.0_多页_中文.docx"),
        os.path.join(SRC, r"010.光纤预制棒\1.1、LKF-Fiber Preform V3.0 Data Sheet _EN.docx"),
    ),
}


def doc(path):
    with zipfile.ZipFile(path) as z:
        xml = z.read("word/document.xml").decode("utf-8", "ignore")
    return xml


def paragraphs(xml):
    out = []
    for p in re.findall(r"<w:p[ >].*?</w:p>", xml, re.S):
        t = "".join(re.findall(r"<w:t[^>]*>([^<]*)</w:t>", p)).strip()
        if t:
            out.append(t)
    return out


def tables(xml):
    """返回 [[ [cell,cell...] ]] ，合并单元格按 gridSpan 横向复制"""
    out = []
    for tbl in re.findall(r"<w:tbl>.*?</w:tbl>", xml, re.S):
        rows = []
        for tr in re.findall(r"<w:tr[ >].*?</w:tr>", tbl, re.S):
            cells = []
            for tc in re.findall(r"<w:tc>.*?</w:tc>", tr, re.S):
                span = re.search(r'<w:gridSpan w:val="(\d+)"', tc)
                n = int(span.group(1)) if span else 1
                txt = "".join(re.findall(r"<w:t[^>]*>([^<]*)</w:t>", tc)).strip()
                cells.extend([txt] * n)
            if any(cells):
                rows.append(cells)
        out.append(rows)
    return out


def find_desc(paras, key, min_len=15):
    for t in paras:
        if key in t and len(t) > min_len:
            return t
    return ""


# ---------------- 胶水 ----------------
zh_xml, en_xml = doc(DOCS["adhesive"][0]), doc(DOCS["adhesive"][1])
zh_par, en_par = paragraphs(zh_xml), paragraphs(en_xml)
zh_t, en_t = tables(zh_xml), tables(en_xml)

# UV500：源表为「表头分两行 + 数据一行」的 5 列错行结构，列序按 gridSpan 推定：
# 模量 / 强度 / 伸长率 / 粘度 / 操作时间
uv500_vals = zh_t[0][2][:5]
uv500_en = en_t[0][2][:5]
assert len(uv500_vals) == 5 and len(uv500_en) == 5, "UV500 源表结构变化"
UV500_HEAD = ["模量 (MPa)", "强度 (MPa)", "伸长率 (%)", "粘度 (mPa·s)", "操作时间 (h)"]
UV500_HEAD_EN = ["Modulus (MPa)", "Strength (MPa)", "Elongation (%)", "Viscosity (mPa·s)", "Working time (h)"]


def rows_from(tbl_rows, kv_filter_head=True):
    """表头行之后的数据行 -> [(k, [vals])]"""
    out = []
    for i, cells in enumerate(tbl_rows):
        if i == 0:
            continue
        k = cells[0].strip()
        vals = [c.strip() for c in cells[1:]]
        out.append((k, vals))
    return out


# UV100：项目 | 条件 | 指标
uv100 = rows_from(zh_t[1])
uv100_en = rows_from(en_t[1])
# H01：项目 | 典型数据(A/B 合并) ，空项目行归属上一行
h01, h01_en = [], []
for src, dst in ((zh_t[2], h01), (en_t[2], h01_en)):
    for i, cells in enumerate(src):
        if i == 0:
            continue
        k = cells[0].strip() if cells else ""
        vals = [c.strip() for c in cells[1:] if c.strip()]
        if not k and dst:                      # 续行（如 A/B 组份外观）
            prev_k, prev_v = dst[-1]
            if len(vals) >= 2:
                dst[-1] = (prev_k, [f"A: {vals[0]}；B: {vals[1]}"])
            continue
        dst.append((k, [vals[0] if vals else ""]))


def fold(rows_zh, rows_en, fold_cond=True):
    """(k, [v1, v2...]) -> SpecRow；条件并进 k"""
    out = []
    for (k, vals), (k_en, vals_en) in zip(rows_zh, rows_en):
        cond = vals[0] if len(vals) > 1 else ""
        val = vals[-1] if vals else ""
        val_en = vals_en[-1] if vals_en else ""
        kk = f"{k}（{cond}）" if fold_cond and cond and cond not in ("——", "--") else k
        out.append({"k": kk, "kEn": k_en, "v": [val], "vEn": [val_en]})
    return out


ADHESIVE_IMG = "/images/products/LKF-FiberAdhesive.png"
PREFORM_IMG = "/images/products/LKF-FiberPreform.png"

adhesive = [
    {
        "model": "LKF-UV500", "slug": "lkf-uv500", "image": ADHESIVE_IMG,
        "nameZh": "UV500 绕环胶", "nameEn": "UV500 Winding Adhesive",
        "descZh": find_desc(zh_par, "UV500 是光纤环绕制工序"), "descEn": find_desc(en_par, "UV500 is", 60),
        "specTable": {
            "headers": ["项目", "典型值 / Typical"],
            "rows": [
                {"k": h, "kEn": he, "v": [v], "vEn": [ve]}
                for h, he, v, ve in zip(UV500_HEAD, UV500_HEAD_EN, uv500_vals, uv500_en)
            ],
        },
    },
    {
        "model": "LKF-UV100", "slug": "lkf-uv100", "image": ADHESIVE_IMG,
        "nameZh": "UV100 尾纤胶", "nameEn": "UV100 Pigtail Adhesive",
        "descZh": find_desc(zh_par, "UV100 是紫外光固化"), "descEn": find_desc(en_par, "UV100 is", 60),
        "specTable": {"headers": ["项目", "指标 / Value"], "rows": fold(uv100, uv100_en)},
    },
    {
        "model": "LKF-H01", "slug": "lkf-h01", "image": ADHESIVE_IMG,
        "nameZh": "H01 粘环胶", "nameEn": "H01 Coil Bonding Adhesive",
        "descZh": find_desc(zh_par, "H01 是一款双组份"), "descEn": find_desc(en_par, "H01 is", 60),
        "specTable": {"headers": ["项目", "典型值 / Typical"], "rows": fold(h01, h01_en, fold_cond=False)},
    },
]

# ---------------- 预制棒 ----------------
zh_xml, en_xml = doc(DOCS["preform"][0]), doc(DOCS["preform"][1])
zh_par, en_par = paragraphs(zh_xml), paragraphs(en_xml)
zh_t, en_t = tables(zh_xml), tables(en_xml)

PREFORM = [
    ("LKF-Boron-Doped", "lkf-boron-doped", "硼掺杂光纤预制棒", "Boron-Doped Fiber Preform", "硼掺杂", 0),
    ("LKF-Fluorine-Doped", "lkf-fluorine-doped", "氟掺杂光纤预制棒", "Fluorine-Doped Fiber Preform", "氟掺杂", 1),
    ("LKF-Germanium-Doped", "lkf-germanium-doped", "锗掺杂光纤预制棒", "Germanium-Doped Fiber Preform", "锗掺杂", 2),
]
preform = []
for model, slug, name_zh, name_en, kw, ti in PREFORM:
    zt, et = zh_t[ti], en_t[ti]
    head_zh = [c for c in zt[0][1:] if c]
    head_en = [c for c in et[0][1:] if c]
    if len(head_zh) != len(head_en):
        raise SystemExit(f"{model} 中英表头列数不一致: {head_zh} / {head_en}")
    # 表头用中英合并，避免英文页出现中文列名
    headers = ["项目"] + [a if a == b else f"{a} / {b}" for a, b in zip(head_zh, head_en)]
    zrows, erows = zt[1:], et[1:]
    if len(zrows) != len(erows):
        raise SystemExit(f"{model} 中英行数不一致: {len(zrows)} / {len(erows)}")
    rows = []
    for zr, er in zip(zrows, erows):
        k, k_en = zr[0], er[0]
        vals = [c for c in zr[1:]][: len(head_zh)]
        vals_en = [c for c in er[1:]][: len(head_en)]
        rows.append({"k": k, "kEn": k_en, "v": vals, "vEn": vals_en})
    preform.append({
        "model": model, "slug": slug, "image": PREFORM_IMG,
        "nameZh": name_zh, "nameEn": name_en,
        "descZh": find_desc(zh_par, f"{kw}预制棒") or find_desc(zh_par, name_zh),
        "descEn": find_desc(en_par, name_en.split(" Fiber")[0], 60),
        "specTable": {"headers": headers, "rows": rows},
    })

data = {"LKF-Fiber Adhesive": adhesive, "LKF-Fiber Preform": preform}
json.dump(data, open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("写入:", OUT)
for k, items in data.items():
    print(f"{k}: → {len(items)} 款")
    for it in items:
        print(f"   {it['model']:22} {it['slug']:22} 参数 {len(it['specTable']['rows']):2} 行 | 简介 {len(it['descZh'])} 字 / {len(it['descEn'])} 字符")
