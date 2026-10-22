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
}

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
    name_en = esc(clean_en_name(r)) or esc(r.get("nameEn")) or NAME_ZH_FIX.get(r["nameZh"]) or ""
    if not name_en:
        name_en = esc(r["nameZh"])
    name_zh = esc(r["nameZh"])
    desc_en = esc(r.get("descEn"))
    desc_zh = esc(r.get("descZh"))
    apps_en = ", ".join(f"'{esc(a)}'" for a in (r.get("appsEn") or [])[:6])
    apps_zh = ", ".join(f"'{esc(a)}'" for a in (r.get("appsZh") or [])[:6])
    img = probe_image(r)
    lines = [
        "  {",
        f"    model: '{model}',",
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
    st = r.get("specTable")
    if st and st.get("rows"):
        hs = ", ".join(f"'{esc(h)}'" for h in st["headers"])
        rl = []
        for row in st["rows"][:30]:
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
