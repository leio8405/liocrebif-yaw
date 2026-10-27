# -*- coding: utf-8 -*-
"""assembled.json -> src/data/products/*.ts（6 分类文件 + index.ts）"""
import os, re, json
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

CAT_DIR = os.path.join(ROOT, "src", "data", "products")
HERE = os.path.dirname(__file__)
data = json.load(open(os.path.join(HERE, "assembled.json"), encoding="utf-8"))

CATS = [
    (1, "fog", "Fiber Optic Gyroscopes", "光纤陀螺系列", "fog-gyroscopes",
     "Single-axis to tri-axis FOG from industrial to navigation grade", "从工业级到导航级的单轴至三轴光纤陀螺"),
    (2, "mems-gyroscopes", "MEMS Gyroscopes", "MEMS 陀螺系列", "mems-gyroscopes",
     "MEMS gyro chips and multi-axis combinations", "MEMS 陀螺芯片与多轴组合"),
    (3, "imu", "IMU & North Seekers", "IMU 与寻北仪", "imu",
     "FOG & MEMS inertial measurement units and north seekers", "光纤与 MEMS 惯性测量单元及寻北仪"),
    (4, "ins", "INS / GNSS Navigation", "INS 组合导航", "inertial-navigation-systems",
     "Tactical-grade integrated navigation systems", "战术级组合导航系统"),
    (5, "accelerometers", "Accelerometers", "加速度计", "accelerometers",
     "Quartz and MEMS accelerometers", "石英与 MEMS 加速度计"),
    (6, "devices", "Fiber Devices & Equipment", "光纤器件与设备", "fiber-optic",
     "Fiber, components, winding machines and test equipment", "光纤器件、绕制与测试设备"),
]

SUB_TAG = {
    "单轴光纤陀螺": ("Single-Axis FOG", "单轴 FOG"),
    "双轴光纤陀螺": ("Dual-Axis FOG", "双轴 FOG"),
    "三轴光纤陀螺": ("Tri-Axis FOG", "三轴 FOG"),
    "MEMS单轴芯片": ("MEMS Chip", "MEMS 芯片"),
    "MEMS三轴陀螺": ("MEMS Gyro", "MEMS 陀螺"),
    "光纤IMU": ("FOG IMU", "光纤 IMU"),
    "MEMS IMU": ("MEMS IMU", "MEMS IMU"),
    "光纤INS": ("FOG INS", "光纤 INS"),
    "MEMS INS": ("MEMS INS", "MEMS INS"),
    "水下惯导": ("Underwater INS", "水下惯导"),
    "保偏光纤": ("PM Fiber", "保偏光纤"),
    "单模光纤": ("Single-Mode Fiber", "单模光纤"),
    "全尺寸光纤环圈定制": ("Fiber Coil", "光纤环圈"),
    "光学器件": ("Optical Component", "光学器件"),
    "硅光三轴集成陀螺收发组件": ("SiPh Transceiver", "硅光收发组件"),
    "标准光纤陀螺光学模块": ("Optical Module", "光学模块"),
    "生产设备": ("Production Equipment", "生产设备"),
    "测试设备": ("Test Equipment", "测试设备"),
    "胶水": ("Adhesive", "胶水"),
    "光纤预制棒": ("Fiber Preform", "光纤预制棒"),
    "光纤筒": ("Fiber Coil Bobbin", "光纤筒"),
    "石英加速度计": ("Quartz Accelerometer", "石英加速度计"),
    "MEMS加速度计": ("MEMS Accelerometer", "MEMS 加速度计"),
}


NAME_ZH_FIX = {
    "低水峰单模光纤": "Low Water Peak Single-Mode Fiber",
    "超低损耗单模光纤": "Ultra-Low Loss Single-Mode Fiber",
    "低损耗弯曲不敏感单模光纤": "Low-Loss Bend-Insensitive Single-Mode Fiber",
    "超强弯曲不敏感单模光纤": "Ultra Bend-Insensitive Single-Mode Fiber",
    "三合一集成光学器件": "Three-in-One Integrated Optical Device",
}

# 中文名修正：按 EN DataSheet 名（产品身份）校正——提取阶段中文名与文档配对错位/截断
NAME_ZH_BY_EN = {
    "LKF-PM(1310&1550)Coil Winding Panda PM Fiber": "(1310&1550)绕环用熊猫保偏光纤",
    "LKF-PM(1310&1550)WaveGuide Panda PM Fiber": "(1310&1550)波导用熊猫保偏光纤",
    "LKF-RH04 Fiber Coil Winding Machine": "RH04型光纤环绕制机",
    "LKF-RH16 Fiber Coil Winding Machine": "RH16型光纤环绕制机",
    "LKF-RH16A Fiber Coil Winding Machine": "RH16A光纤环绕制机",
}

# 英文名修正：目录 md 的 G652 三条共用同一资料夹（只有一份 enDoc），需按中文名指定各自英文款名
NAME_EN_BY_MODEL = {
    "LKF-MIOC1310": "LKF-MIOC 1310nm (Y-waveguide)",
    "LKF-MIOC1550": "LKF-MIOC 1550nm (Y-waveguide)",
    "LKF-SPC1310": "LKF-SPC1310 Three-in-One Integrated Optical Device",
}

NAME_EN_BY_ZH = {
    "低水峰单模光纤": "LKF-G652 Low-Water Peak Single-Mode Fiber",
    "低损耗单模光纤": "LKF-G652 Low-Loss Single-Mode Fiber",
    "超低损耗单模光纤": "LKF-G652 Ultra Low-Loss Single-Mode Fiber",
    "低水峰弯曲不敏感单模光纤": "LKF-G657A2 Low Water Peak Bend-Insensitive Single-Mode Fiber",
    "低损耗弯曲不敏感单模光纤": "LKF-G657A1 Low-Loss Bend-Insensitive Single-Mode Fiber",
    "超强弯曲不敏感单模光纤": "LKF-G657B3 Ultra-Strong Bend-Insensitive Single-Mode Fiber",
}

# 同型号多规格产品（共用 model）的 URL 区分
SLUG_BY_EN = {
    "LKF-PM(1310&1550)Coil Winding Panda PM Fiber": "lkf-pm-coil-winding",
    "LKF-PM(1310&1550)WaveGuide Panda PM Fiber": "lkf-pm-waveguide",
    "LKF-PM Polarization-Maintaining Photonic Crystal Fiber": "lkf-pm-pcf",
}
SLUG_BY_ZH = {
    "低水峰单模光纤": "lkf-g652",
    "低损耗单模光纤": "lkf-g652-low-loss",
    "超低损耗单模光纤": "lkf-g652-ultra-low-loss",
    "低水峰弯曲不敏感单模光纤": "lkf-g657a2",
    "低损耗弯曲不敏感单模光纤": "lkf-g657a1",
    "超强弯曲不敏感单模光纤": "lkf-g657b3",
}

def clean_en_name(r):
    """从 EN DataSheet 文件名清洗出英文产品名"""
    en = r.get("enDoc")
    if not en:
        return None
    base = os.path.splitext(os.path.basename(en))[0]
    base = re.sub(r"^\d+(\.\d+)?、", "", base)
    base = re.sub(r"\s*V\d+(\.\d+)?\s*Data\s*Sheet\s*_EN.*$", "", base, flags=re.I)
    base = re.sub(r"\s*Data\s*Sheet\s*_EN.*$", "", base, flags=re.I)
    base = base.strip()
    return base if len(base) >= 8 and re.search(r"[A-Za-z]{3,}", base) else None

def esc(s):
    if s is None:
        return ""
    return s.replace("\\", "\\\\").replace("'", "\\'").replace("\n", " ").strip()

IMG_DIR = os.path.join(ROOT, "public", "images", "products")

MANUAL_IMAGES = {
    "LKF-FSI206": "/images/products/LKF-FSI206.jpg",  # 用户提供的手动截图（docx 内为尺寸图无实物照）
    "LKF-SPC1310": "/images/products/LKF-SPC1310.png",  # 提取记录缺 image 字段（图片文件已在库）
}

# 参数表覆盖（目录 md 缺失/错位的产品，改由源 docx 解析产出：parse_fiber_specs.py）
SPEC_OVERRIDE = {}
_ov_path = os.path.join(HERE, "spec_override.json")
if os.path.exists(_ov_path):
    SPEC_OVERRIDE = json.load(open(_ov_path, encoding="utf-8"))

# 简介覆盖（目录 md 无简介的产品，从源 docx 提取：parse_desc.py）
DESC_OVERRIDE = {}
_dp = os.path.join(HERE, "desc_override.json")
if os.path.exists(_dp):
    DESC_OVERRIDE = json.load(open(_dp, encoding="utf-8"))

def probe_image(r):
    """按实际存在的图片文件解析 image 路径；无文件返回 None（详情页显示型号占位）"""
    manual = MANUAL_IMAGES.get(r.get("model"))
    if manual and os.path.exists(os.path.join(IMG_DIR, os.path.basename(manual))):
        return manual
    img = r.get("image")
    if not img:
        return None
    base = os.path.splitext(os.path.basename(img))[0]
    for e in (".png", ".jpeg", ".jpg", ".webp"):
        if os.path.exists(os.path.join(IMG_DIR, base + e)):
            return "/images/products/" + base + e
    return None

def ts_entry(r):
    model = esc(r["model"])
    tag_en, tag_zh = SUB_TAG.get(r.get("sub") or "", ("", ""))
    if not tag_en:
        tag_en, tag_zh = r.get("sub") or "Product", r.get("sub") or "产品"
    name_en = esc(NAME_EN_BY_MODEL.get(model)) or esc(NAME_EN_BY_ZH.get(r["nameZh"])) or esc(clean_en_name(r)) or esc(r.get("nameEn")) or NAME_ZH_FIX.get(r["nameZh"]) or ""
    if not name_en:
        name_en = esc(r["nameZh"])
    name_zh = esc(NAME_ZH_BY_EN.get(clean_en_name(r)) or r["nameZh"])
    product_slug = SLUG_BY_ZH.get(r["nameZh"]) or SLUG_BY_EN.get(clean_en_name(r))
    ov_key = product_slug or model.lower().replace(" ", "-")  # 覆盖数据查找键
    _desc = DESC_OVERRIDE.get(ov_key) or {}
    desc_en = esc(_desc.get("descEn") or r.get("descEn"))
    desc_zh = esc(_desc.get("descZh") or r.get("descZh"))
    apps_en = ", ".join(f"'{esc(a)}'" for a in (r.get("appsEn") or [])[:6])
    apps_zh = ", ".join(f"'{esc(a)}'" for a in (r.get("appsZh") or [])[:6])
    img = probe_image(r)
    lines = [
        "  {",
        f"    model: '{model}',",
    ]
    if product_slug:
        lines.append(f"    slug: '{product_slug}',")
    lines += [
        f"    subZh: '{esc(tag_zh)}',",
        f"    subEn: '{esc(tag_en)}',",
        f"    tagEn: '{esc(tag_en)}',",
        f"    tagZh: '{esc(tag_zh)}',",
        f"    nameEn: '{name_en}',",
        f"    nameZh: '{name_zh}',",
    ]
    if desc_en:
        lines.append(f"    descEn: '{desc_en}',")
    if desc_zh:
        lines.append(f"    descZh: '{desc_zh}',")
    st = SPEC_OVERRIDE.get(ov_key) or r.get("specTable")
    if st and st.get("rows"):
        hs = ", ".join(f"'{esc(h)}'" for h in st["headers"])
        rl = []
        for row in st["rows"][:200]:
            k_en = row.get("kEn") or row["k"]
            vs = ", ".join(f"'{esc(v)}'" for v in row["v"])
            ven = row.get("vEn") or row["v"]
            vse = ", ".join(f"'{esc(v)}'" for v in ven)
            rl.append("{ k: '" + esc(row["k"]) + "', kEn: '" + esc(k_en) + "', v: [" + vs + "], vEn: [" + vse + "] }")
        lines.append("    specTable: {")
        lines.append(f"      headers: [{hs}],")
        lines.append("      rows: [")
        for x in rl:
            lines.append("        " + x + ",")
        lines.append("      ],")
        lines.append("    },")
    if apps_en:
        lines.append(f"    appsEn: [{apps_en}],")
    if apps_zh:
        lines.append(f"    appsZh: [{apps_zh}],")
    if img:
        lines.append(f"    image: '{img}',")
    lines.append("  },")
    return "\n".join(lines)

def main():
    os.makedirs(CAT_DIR, exist_ok=True)
    by_series = {}
    for r in data:
        s = str(r["series"])
        s = re.match(r"^(\d+)", s).group(1) if re.match(r"^(\d+)", s) else s
        by_series.setdefault(int(s), []).append(r)
    exports = []
    for num, slug, title_en, title_zh, old_slug, sub_en, sub_zh in CATS:
        rows = by_series.get(num, [])
        var = {
            1: "fogGyros", 2: "memsGyros", 3: "imus",
            4: "insSystems", 5: "accelerometers", 6: "devices",
        }[num]
        header = (
            f"// {title_en} · {title_zh}（目录 {num:02d} 册，自动生成，勿手改：改 .extract/build_data.py）\n"
            f"import type {{ Product }} from './types';\n\n"
            f"export const {var}: Product[] = [\n"
        )
        body = "\n".join(ts_entry(r) for r in rows)
        open(os.path.join(CAT_DIR, f"{slug}.ts"), "w", encoding="utf-8").write(header + body + "\n];\n")
        exports.append((var, slug, title_en, title_zh, old_slug, sub_en, sub_zh, len(rows)))
        print(f"{slug}.ts: {len(rows)} 条")

    # index.ts
    idx = ["// 产品分类汇总（自动生成）"]
    for var, slug, title_en, title_zh, old_slug, sub_en, sub_zh, n in exports:
        idx.append(f"import {{ {var} }} from './{slug}';")
    idx.append("export type { Product } from './types';")
    idx.append("export { " + ", ".join(var for var, *_ in exports) + " };")
    idx.append("export interface ProductCategory {")
    idx.append("  slug: string;")
    idx.append("  titleEn: string;")
    idx.append("  titleZh: string;")
    idx.append("  descEn: string;")
    idx.append("  descZh: string;")
    idx.append("  products: Product[];")
    idx.append("}")
    idx.append("")
    idx.append("export const productCategories: ProductCategory[] = [")
    for var, slug, title_en, title_zh, old_slug, sub_en, sub_zh, n in exports:
        idx.append("  {")
        idx.append(f"    slug: '{old_slug}',")
        idx.append(f"    titleEn: '{title_en}',")
        idx.append(f"    titleZh: '{title_zh}',")
        idx.append(f"    descEn: '{sub_en}',")
        idx.append(f"    descZh: '{sub_zh}',")
        idx.append(f"    products: {var},")
        idx.append("  },")
    idx.append("];")
    open(os.path.join(CAT_DIR, "index.ts"), "w", encoding="utf-8").write("\n".join(idx) + "\n")
    print("index.ts 完成")

if __name__ == "__main__":
    main()
