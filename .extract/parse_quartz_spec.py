# -*- coding: utf-8 -*-
"""LKF-Quartz Accelerometer 参数表：源文档为 4 个子系列 × T180/T150/T125 三型号并列

合并为一张三列表（headers: 项目 / T180 / T150 / T125），行名加子系列前缀以区分。
写回 .extract/spec_override.json（不动其它产品的覆盖数据）。
"""
import json, os, re, zipfile

SRC = r"D:\利科夫\2026年产品资料-利科夫\5、加速度计\1.石英加速度计"
ZH = "1、LKF-石英加速度计简介V3.0_多页_中文.docx"
EN = "1.1、LKF-Quartz Accelerometer V3.0 Data Sheet _EN.docx"
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "spec_override.json")
SLUG = "lkf-quartz-accelerometer"

VARIANTS = ["高温抗震大表", "高温抗震小表", "高精度", "普通"]
VARIANTS_EN = ["High-temp / shock-resistant, large", "High-temp / shock-resistant, small", "High precision", "Standard"]


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
        out.append(rows)
    return out


def body(rows):
    """去掉表头行与型号行，返回 [(参数, [3 个值])]"""
    out = []
    for cells in rows:
        if not cells or len(cells) < 2:
            continue
        k = cells[0].strip()
        if k in ("项目", "Parameter") or k in ("型号", "Model"):
            continue
        vals = [c.strip() for c in cells[1:4]]
        if len(vals) < 3:
            vals += [""] * (3 - len(vals))
        out.append((k, vals))
    return out


zh_t, en_t = tables(ZH), tables(EN)
if len(zh_t) != len(en_t):
    raise SystemExit(f"表数量不一致: zh {len(zh_t)} / en {len(en_t)}")

rows = []
for i, (zt, et) in enumerate(zip(zh_t, en_t)):
    zh_rows, en_rows = body(zt), body(et)
    if len(zh_rows) != len(en_rows):
        raise SystemExit(f"第 {i+1} 表行数不一致: zh {len(zh_rows)} / en {len(en_rows)}")
    for (k, v), (k_en, v_en) in zip(zh_rows, en_rows):
        rows.append({
            "k": f"{VARIANTS[i]} · {k}",
            "kEn": f"{VARIANTS_EN[i]} · {k_en}",
            "v": v,
            "vEn": v_en,
        })

data = json.load(open(OUT, encoding="utf-8")) if os.path.exists(OUT) else {}
data[SLUG] = {"headers": ["项目", "T180", "T150", "T125"], "rows": rows}
json.dump(data, open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(f"✓ {SLUG}: {len(rows)} 行（4 子系列合并）")
for r in rows[:3]:
    print("   ", r["k"], "=", r["v"])
