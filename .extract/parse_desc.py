# -*- coding: utf-8 -*-
"""为缺简介的 7 款产品，从源 docx 提取中英文简介

规则：
- 中文：取「产品简介」标题后的段落；没有该标题则取首段 >80 字、非公司通用介绍的内容
- 英文：取首个 >90 字符、非公司通用介绍（"Liocrebif is a high-tech enterprise"）的段落
输出 .extract/desc_override.json：{slug: {descZh, descEn}}，由 gen_ts 覆盖。
"""
import json, os, re, zipfile

SRC = r"D:\利科夫\2026年产品资料-利科夫"
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "desc_override.json")

BOILER_ZH = "利科夫公司是一家"
BOILER_EN = "liocrebif is a high-tech enterprise"

PRODUCTS = {
    "lkf-pm-waveguide": (
        r"6、光纤陀螺解决方案\001.保偏光纤\02、波导用熊猫保偏光纤\1、LKF-PM(1310&1550)波导用熊猫保偏光纤简介V3.0_双页_中文.docx",
        r"6、光纤陀螺解决方案\001.保偏光纤\02、波导用熊猫保偏光纤\1.1、LKF-PM(1310&1550)WaveGuide Panda PM Fiber V3.0 Data Sheet _EN.docx",
    ),
    "lkf-pm-pcf": (
        r"6、光纤陀螺解决方案\001.保偏光纤\03、保偏光子晶体光纤\1、LKF-PM保偏光子晶体光纤简介V3.0_双页_中文.docx",
        r"6、光纤陀螺解决方案\001.保偏光纤\03、保偏光子晶体光纤\1.1、LKF-PM Polarization-Maintaining Photonic Crystal FiberV3.0 Data Sheet _EN.docx",
    ),
    "lkf-spc1310": (
        r"6、光纤陀螺解决方案\004.光学器件\三合一集成光学器件\1、LKF-SPC1310三合一集成光学器件简介V3.0_双页_中文.docx",
        r"6、光纤陀螺解决方案\004.光学器件\三合一集成光学器件\1.1、LKF-SPC1310 Three-in-One Integrated Optical Device V3.0 Data Sheet _EN.docx",
    ),
    "lkf-tios1310": (
        r"6、光纤陀螺解决方案\005.硅光三轴集成陀螺收发组件\1、LKF-TIOS1310硅光三轴集成陀螺收发组件简介V3.0_双页_中文.docx",
        r"6、光纤陀螺解决方案\005.硅光三轴集成陀螺收发组件\1.1、LKF-TIOS1310 Silicon-Photonic Three-Axis Integrated Gyro Transceiver Assembly V3.0 Data Sheet _EN.docx",
    ),
    "lkf-fmtp": (
        r"6、光纤陀螺解决方案\008.测试设备\05.FMTP光纤环多功能测试平台\1、LKF-FMTP光纤环多功能测试平台简介V3.0_三页_中文.docx",
        r"6、光纤陀螺解决方案\008.测试设备\05.FMTP光纤环多功能测试平台\1.1、LKF-FMTP Fiber Coil Multifunction Test Platform V3.0 Data Sheet _EN.docx",
    ),
    "lkf-msu105": (
        r"3、IMU系列\2.MEMS IMU\MSU105微型MEMS惯性组合导航系统(MS105)\1、LKF-MSU105 微型MEMS惯性组合导航系统简介V3.0_三页_中文.docx",
        r"3、IMU系列\2.MEMS IMU\MSU105微型MEMS惯性组合导航系统(MS105)\1.1、LKF-MSU105 Mini MEMS Integrated Inertial Navigation System V3.0 Data Sheet _EN.docx",
    ),
    "lkf-msi100": (
        r"4、INS系统\2.MEMS INS\MSI100\1、LKF-MSI100 MEMS组合导航系统V3.0_双页_中文.docx",
        r"4、INS系统\2.MEMS INS\MSI100\1.1、LKF-MSI100 MEMS_GNSS Inertial Navigation System V3.0 Datasheet _EN.docx",
    ),
}


def paras(path):
    with zipfile.ZipFile(os.path.join(SRC, path)) as z:
        xml = z.read("word/document.xml").decode("utf-8", "ignore")
    out = []
    for p in re.findall(r"<w:p[ >].*?</w:p>", xml, re.S):
        t = "".join(re.findall(r"<w:t[^>]*>([^<]*)</w:t>", p)).strip()
        if t:
            out.append(t)
    return out


def pick_zh(ps):
    if "产品简介" in ps:
        i = ps.index("产品简介")
        for t in ps[i + 1: i + 3]:
            if len(t) > 40 and BOILER_ZH not in t:
                return t
    for t in ps:
        if len(t) > 80 and BOILER_ZH not in t and t not in ("产品简介", "独特技术"):
            return t
    return ""


def pick_en(ps):
    """优先取以 Liocrebif 开头或含型号的段落（避开纯功能条目）"""
    cands = [t for t in ps if len(t) > 90 and BOILER_EN not in t.lower()]
    for t in cands:
        if t.startswith("Liocrebif") or re.search(r"\b[A-Z]{2,}\d{2,}\b", t):
            return t
    return cands[0] if cands else ""


out, missing = {}, []
for slug, (zh_doc, en_doc) in PRODUCTS.items():
    try:
        zh = pick_zh(paras(zh_doc))
        en = pick_en(paras(en_doc))
    except FileNotFoundError as e:
        missing.append((slug, str(e)))
        continue
    out[slug] = {"descZh": zh, "descEn": en}
    print(f"✓ {slug}: ZH {len(zh)} 字 | EN {len(en)} 字符")

json.dump(out, open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("写入:", OUT)
for m in missing:
    print("⚠️ 缺文件:", m)
