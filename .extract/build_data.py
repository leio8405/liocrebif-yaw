# -*- coding: utf-8 -*-
"""
组装网站产品数据：
1. 解析目录 7 分册 md -> 型号 + 参数表（中文）
2. 匹配 extracted.json（简介中英 + 图片）
3. 参数名中->英 术语映射
4. 生成 src/data/products/<cat>.ts 六个分类文件 + 诊断报告
"""
import os, re, json
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
from phrase_fixes import PHRASES, V_EN_FIX, MODEL_EN, K_EN_FIX

CAT_DIR = os.path.join(ROOT, "src", "data", "products")
CATALOG_DIR = r"D:\利科夫\利科夫产品目录_2026"
EXTRACT = os.path.join(os.path.dirname(__file__), "extracted.json")

FILES = {
    1: "01_光纤陀螺系列.md",
    2: "02_MEMS陀螺系列.md",
    3: "03_IMU系列.md",
    4: "04_INS系统.md",
    5: "05_加速度计.md",
    6: "06_光纤陀螺解决方案.md",
    7: "07_光纤筒.md",
}

# ---------------- 1. 解析目录 md ----------------
def parse_cells(line):
    cells = [c.strip() for c in line.strip().strip("|").split("|")]
    return cells

def parse_catalog():
    entries = []
    for idx, fn in FILES.items():
        path = os.path.join(CATALOG_DIR, fn)
        text = open(path, encoding="utf-8").read()
        lines = text.split("\n")
        sub = None
        i = 0
        while i < len(lines):
            ln = lines[i]
            m_sub = re.match(r"^### (\d+\.\d+)\s+(.+)$", ln)
            if m_sub:
                sub = m_sub.group(2).strip()
            m = re.match(r"^#### (\S+?)（(.+?)）\s*$", ln)
            if not m:
                m2 = re.match(r"^#### (\S+)\s*$", ln)
                if m2:
                    entries.append({"series": idx, "sub": sub, "model": m2.group(1),
                                    "nameZh": m2.group(1), "specTable": None})
                    i += 1
                    continue
                i += 1
                continue
            model, nameZh = m.group(1), m.group(2)
            # 收集后面的 markdown 表
            j = i + 1
            table_lines = []
            while j < len(lines):
                if lines[j].startswith("|"):
                    table_lines.append(lines[j])
                elif table_lines and not lines[j].strip():
                    pass
                elif table_lines:
                    break
                j += 1
            spec = parse_table(table_lines)
            entries.append({"series": idx, "sub": sub, "model": model, "nameZh": nameZh,
                            "specTable": spec})
            i = j
    return entries

def parse_table(tlines):
    if len(tlines) < 2:
        return None
    rows = [parse_cells(l) for l in tlines if not re.match(r"^\|[\s\-|]+\|$", l)]
    if not rows:
        return None
    header = rows[0]
    # 横向多型号表：表头含"型号"且有 3+ 列
    if len(header) >= 3 and header[0] in ("型号", "项目", "参数"):
        headers = header[1:]
        body = []
        for r in rows[1:]:
            k = r[0]
            vals = [c for c in r[1:]]
            if not k or all(not v for v in vals):
                continue
            body.append({"k": k, "v": vals})
        if "型号" == header[0] and headers and all(headers):
            return {"mode": "models", "headers": headers, "rows": body}
        return {"mode": "multi", "headers": headers, "rows": body}
    # 纵向两列
    body = []
    for r in rows[1:]:
        if len(r) < 2 or not r[0]:
            continue
        v = r[1] if len(r) > 1 else ""
        if not v:
            continue  # 分组行
        body.append({"k": r[0], "v": [v]})
    if not body:
        return None
    return {"mode": "kv", "headers": ["项目", "技术指标"], "rows": body}

# ---------------- 2. 术语映射（参数名 中->英） ----------------
TERMS = [
    ("全温", "Full-Temp "), ("全温", "Full-Temp "), ("零偏稳定性", "Bias Stability"),
    ("零偏不稳定性", "Bias Instability"),
    ("零偏重复性", "Bias Repeatability"),
    ("全温零偏重复性", "Full-Temp Bias Repeatability"),
    ("全温零偏", "Full-Temp Bias"),
    ("零偏温漂", "Bias Temp Drift"),
    ("校准后零偏温漂", "Calibrated Bias Temp Drift"),
    ("角度随机游走", "Angle Random Walk"),
    ("随机游走系数", "Angle Random Walk"),
    ("标度因数非线性度", "Scale Factor Nonlinearity"),
    ("标度因数重复性", "Scale Factor Repeatability"),
    ("标度因数温漂", "Scale Factor Temp Drift"),
    ("标度因子非线性", "Scale Factor Nonlinearity"),
    ("标度因子重复性", "Scale Factor Repeatability"),
    ("标度因子温漂", "Scale Factor Temp Drift"),
    ("标度因数非线性", "Scale Factor Nonlinearity"),
    ("标度因数", "Scale Factor"),
    ("标度因子", "Scale Factor"),
    ("动态范围", "Dynamic Range"),
    ("磁场敏感性", "Magnetic Sensitivity"),
    ("稳定时间", "Settling Time"),
    ("启动时间", "Start-up Time"),
    ("上电时间", "Power-on Time"),
    ("更新率", "Update Rate"),
    ("数据输出率", "Output Data Rate"),
    ("群延时", "Group Delay"),
    ("分辨率", "Resolution"),
    ("量程", "Measurement Range"),
    ("测量范围", "Measurement Range"),
    ("带宽", "Bandwidth"),
    ("峰值噪声", "Peak-to-Peak Noise"),
    ("零偏", "Bias"),
    ("工作温度", "Operating Temperature"),
    ("存储温度", "Storage Temperature"),
    ("储存温度", "Storage Temperature"),
    ("振动整流误差", "Vibration Rectification Error"),
    ("抗冲击", "Shock Survival"),
    ("冲击", "Shock"),
    ("振动", "Vibration"),
    ("重量", "Weight"),
    ("尺寸", "Dimensions"),
    ("电源电压", "Supply Voltage"),
    ("稳态功率", "Steady-state Power"),
    ("功率", "Power"),
    ("电流", "Current"),
    ("交叉耦合", "Cross Coupling"),
    ("阈值", "Threshold"),
    ("工作波长", "Operating Wavelength"),
    ("截止波长", "Cutoff Wavelength"),
    ("模场直径", "Mode Field Diameter"),
    ("衰减", "Attenuation"),
    ("拍长", "Beat Length"),
    ("消光比", "Extinction Ratio"),
    ("光纤类型", "Fiber Type"),
    ("驱动轴频率", "Drive Axis Frequency"),
    ("陀螺仪", "Gyroscope"),
    ("加速度计", "Accelerometer"),
    ("电气/机械接口", "Electrical / Mechanical"),
    ("使用环境", "Environment"),
    ("接口", "Interface"),
    ("电源", "Power Supply"),
    ("型号", "Model"),
    ("项目", "Item"),
    ("参数", "Parameter"),
    ("技术指标", "Specification"),
    ("偏值", "Bias"),
    ("二阶非线性", "2nd-order Nonlinearity"),
]
def translate_key(k):
    out = k
    for zh, en in sorted(TERMS, key=lambda x: -len(x[0])):
        if zh in out:
            out = out.replace(zh, en)
    for zh, en in sorted(PHRASES, key=lambda x: -len(x[0])):
        out = out.replace(zh, en)
    # PHRASES 之后再跑一轮 TERMS（如 "Current响应度" -> "Current Responsivity"）
    for zh, en in sorted(TERMS, key=lambda x: -len(x[0])):
        if zh in out:
            out = out.replace(zh, en)
    import html as _html
    out = _html.unescape(out)
    out = re.sub(r"([a-z])([A-Z][a-z])", r"\1 \2", out)  # 拆驼峰但保留 dB/kV/mV 等单位
    out = re.sub(r"\s+", " ", out).replace("( ", "(").replace(" )", ")")
    out = re.sub(r",\s*\)", ")", out).replace(",,", ",").replace(",,", ",").strip()
    return K_EN_FIX.get(out, out)

def has_cjk(s):
    return bool(re.search(r"[\u4e00-\u9fff]", s))

# 参数值中文备注词典（精确匹配）
VAL_ZH_MAP = {
    "常温": "Room temp.", "震动": "Vibration", "量程": "Range",
    "2h连续测试，10s平滑结果": "2h test, 10s smoothing",
    "2h连续测试，100s平滑结果": "2h test, 100s smoothing",
    "6次测试数据计算结果": "Calculated from 6 test runs",
    "3次测试数据计算结果": "Calculated from 3 test runs",
    "典型平均值": "Typical average",
    "绝对力 [N]": "Absolute force [N]",
    "扫频振动无谐振": "Swept sine, no resonance",
    "X轴和Y轴 / Z轴": "X & Y axis / Z axis",
    "无划伤、开裂、锈蚀现象": "No scratches, cracks or rust",
    "见产品图纸 Q, E, T, U": "See product drawing Q, E, T, U",
    "5~12(纹波≤100mV)": "5~12 V (ripple ≤100mV)",
    "-10℃ 到85℃，98% 相对湿度": "-10°C to 85°C, 98% RH",
    "23℃, 30 天": "23°C, 30 days",
    "85℃，85%相对湿度，30天": "85°C, 85% RH, 30 days",
    "85℃，30天": "85°C, 30 days",
    "-60℃ 到85℃": "-60°C to 85°C",
    "-65℃ 到85℃": "-65°C to 85°C",
    "100圈，半径30mm": "100 turns, 30mm radius",
    "RS422（默认）, RS232（可选）": "RS422 (default), RS232 (optional)",
    "3个, DS18B20, 航空插头": "3× DS18B20, aviation connector",
    "0.5ms, 1/2正弦波": "0.5ms, 1/2 sine wave",
    "16K正负5%": "16K ±5%",
    "应答式输出，最大200Hz": "Interrogator mode, max 200Hz",
}

def translate_val(v):
    """参数值中文 -> 英文（词典优先，通用替换兜底）"""
    if not v or not has_cjk(v):
        return v
    if v in VAL_ZH_MAP:
        return VAL_ZH_MAP[v]
    if v in V_EN_FIX:
        return V_EN_FIX[v]
    out = v
    for zh, en in sorted(PHRASES, key=lambda x: -len(x[0])):
        out = out.replace(zh, en)
    out = re.sub(r"\s+", " ", out).replace("( ", "(").replace(" )", ")").strip()
    if not has_cjk(out):
        return out
    # 二轮：TERMS 再扫一遍后仍中文则放弃
    for zh, en in sorted(TERMS, key=lambda x: -len(x[0])):
        if zh in out:
            out = out.replace(zh, en)
    if not has_cjk(out):
        return out
    for a, b in [
        ("常温", " Room temp."), ("到", " to "), ("天", " days"), ("相对湿度", "RH"),
        ("（默认）", " (default)"), ("(默认)", " (default)"), ("（可选）", " (optional)"), ("(可选)", " (optional)"),
        ("可定制支持", "customizable to "), ("可定制", "customizable"), ("典型", "typical"),
        ("纹波", "ripple"), ("最大值", "max"), ("航空插头", "aviation connector"),
        ("单点", "single-point"), ("基线双天线", "baseline dual-antenna"), ("动态", "dynamic"),
        ("正弦波", "sine wave"), ("正负", "±"), ("筛选谱", "screening profile"),
        ("线圈", "coil"), ("匝数", "turns"), ("张力", "tension"), ("层数", "layers"),
        ("主轴转动方向", "spindle rotation"), ("排线方向", "traverse direction"),
        ("转速", "speed"), ("可实时显示当前层的已绕长度", "real-time wound-length display"),
        ("骨架直径", "bobbin diameter"), ("骨架宽度", "bobbin width"),
        ("不含台体", "excluding table"), ("电路盒", "electronics box"), ("传感表头", "sensor header"),
        ("平均值", "average"), ("单天线", "single-antenna"), ("双天线", "dual-antenna"),
        ("路", "-channel "), ("°平均法", "° averaging"),
        ("应答式输出", "Interrogator output"), ("最大", "max"),
    ]:
        out = out.replace(a, b)
    if has_cjk(out):
        return v  # 翻译不全保留原文
    return out

# ---------------- 3. 加载 extracted + 匹配 ----------------
def load_extract():
    return json.load(open(EXTRACT, encoding="utf-8"))

def core_keys(s):
    """从名称提取核心匹配码"""
    s = re.sub(r"[（(].*?[)）]", "", s)
    s = s.replace("LKF-", "").replace(" ", "")
    return s

def cjk_seg(s):
    return "".join(re.findall(r"[\u4e00-\u9fff]+", s))

def match_entry(entry, extracts, used):
    """目录条目 -> extracted 记录（三轮：精确 / 子串 / 中文段互含）"""
    series = f"{entry['series']}、"
    model = entry["model"]
    keys = core_keys(model)
    cands = [e for e in extracts if e["series"].startswith(series) and id(e) not in used]
    if not cands:
        return None
    # 1) 精确：short == model 或 folder 核心码 == keys
    for e in cands:
        if (e.get("short") or "") == model or (keys and core_keys(e["folder"]) == keys):
            return e
    # 2) 子串（型号核心码出现在 folder/short）
    for e in cands:
        f = core_keys(e["folder"]); s = (e.get("short") or "").replace("LKF-", "")
        if keys and len(keys) >= 4 and (keys in f or keys in s):
            return e
    # 3) 中文名称关键词与 folder 交集（≥2 分）
    kw = [w for w in re.split(r"[（()）\s/&]", entry["nameZh"]) if len(w) >= 2]
    best, best_score = None, 0
    for e in cands:
        folder = e["folder"]
        score = sum(1 for w in kw if w in folder)
        if score > best_score:
            best, best_score = e, score
    if best_score >= 2:
        return best
    # 4) 中文段互含（胶水/光纤筒等短名）
    kz = cjk_seg(keys) or cjk_seg(entry["nameZh"])
    if kz:
        for e in cands:
            fz = cjk_seg(e["folder"])
            if fz and (fz in kz or kz in fz):
                return e
    # 5) 中文段最长公共子串 ≥6（如 FIOS：目录"四合一全集成光学器件" vs folder"四合一全集成光学传感器件"）
    if kz:
        for e in cands:
            fz = cjk_seg(e["folder"])
            if not fz:
                continue
            best = 0
            for i in range(len(kz)):
                for j in range(len(fz)):
                    n = 0
                    while i + n < len(kz) and j + n < len(fz) and kz[i + n] == fz[j + n]:
                        n += 1
                    best = max(best, n)
            if best >= 6:
                return e
    return None

# ---------------- 4. 简介拆分 ----------------
def split_intro(text, is_en=False):
    """返回 (name, features[], apps[], desc)"""
    if not text:
        return None, [], [], None
    seps = ["Key Features", "Main Features", "Features", "Typical Applications", "Application Fields",
            "Applications", "Application", "Product Description",
            "Product Overview", "Product Introduction", "Introduction"] if is_en else \
           ["主要特点", "应用领域", "产品简介"]
    # 找到分隔位置（长词优先，避免 Features 匹配进 Key Features）
    pattern = "|".join(re.escape(s) for s in sorted(seps, key=len, reverse=True))
    idxs = [(m.start(), m.group(0)) for m in re.finditer(pattern, text)]
    if not idxs:
        return text[:80], [], [], text
    name = text[: idxs[0][0]].strip()
    segs = {}
    for n, (i, s) in enumerate(idxs):
        end = idxs[n + 1][0] if n + 1 < len(idxs) else len(text)
        segs[s] = text[i + len(s): end].strip()
    feat = segs.get("主要特点") or segs.get("Key Features") or segs.get("Main Features") or segs.get("Features") or ""
    # 截断：产品简介段里若混入参数表（"项目"），截断
    desc = (segs.get("产品简介") or segs.get("Product Description") or segs.get("Product Overview")
            or segs.get("Product Introduction") or segs.get("Introduction") or "")
    for cut in ["项目 ", "项目\t", " 项目", "Item ", "Specification", "Specifications", "项目数据"]:
        if cut in desc:
            desc = desc.split(cut)[0]
            break
    desc = re.sub(r"^独特技术\s*", "", desc).strip()
    # 若简介段实为参数表头污染（含 2+ 个单位括号模式），置空
    if len(re.findall(r"\((?:nm|dB|dBm|Hz|kHz|°C|μm|ug|μg)\)", desc)) >= 2:
        desc = ""
    apps_raw = (segs.get("应用领域") or segs.get("Applications") or segs.get("Application Fields")
                or segs.get("Typical Applications") or segs.get("Application") or "")
    # 中文应用标签用词典正向最长匹配切分（简介里条目间是单空格，无法按空格拆）
    apps = segment_apps(apps_raw)
    feats = [a.strip() for a in re.split(r"\s{2,}|、|，", feat) if a.strip()]
    return name or None, feats, apps, desc or None

def segment_apps(text):
    """按 APP_MAP 词典对应用领域整段做最长匹配切分"""
    if not text:
        return []
    keys = sorted(APP_MAP.keys(), key=len, reverse=True)
    out, i, n = [], 0, len(text)
    while i < n:
        ch = text[i]
        is_word = ch.isascii() and ch.isalpha() if ch.isascii() else ('\u4e00' <= ch <= '\u9fff')
        if not is_word:
            i += 1
            continue
        hit = None
        for k in keys:
            if text.startswith(k, i):
                hit = k
                break
        if hit:
            out.append(hit)
            i += len(hit)
        else:
            i += 1
    return out

# 应用领域 中->英 映射（网站标签用）
APP_MAP = {
    "光电吊舱": "Electro-optical Pod", "飞控平台": "Flight Control", "飞行控制": "Flight Control",
    "飞控": "Flight Control", "光学/摄影平台": "Optical/Photography Platform", "光学平台": "Optical Platform",
    "平台稳定装置": "Platform Stabilization", "平台稳定": "Platform Stabilization",
    "动中通": "SatCom-on-the-Move", "动中通卫星通信": "SatCom-on-the-Move",
    "惯性测量单元": "Inertial Measurement Unit", "IMU": "IMU", "轻型无人机": "Lightweight UAV",
    "无人机": "UAV", "无人机姿态与飞控": "UAV Attitude & Flight Control", "无人机姿态参考": "UAV Attitude Reference",
    "寻北": "North Seeking", "寻北仪": "North Seeker", "钻探系统": "Drilling Systems",
    "车辆/舰船姿态": "Vehicle/Vessel Attitude", "车辆姿态": "Vehicle Attitude",
    "光纤陀螺": "Fiber Optic Gyroscope", "光纤陀螺仪": "Fiber Optic Gyroscope",
    "导航": "Navigation", "组合导航": "Integrated Navigation", "惯导": "INS",
    "测绘": "Surveying & Mapping", "移动测绘": "Mobile Mapping", "移动测绘与工程检测": "Mobile Mapping & Engineering Survey",
    "航空航天": "Aerospace", "航空": "Aviation", "航天": "Aerospace", "海洋": "Ocean", "船舶": "Ships",
    "舰船": "Naval Vessels", "汽车": "Automotive", "自动驾驶": "Autonomous Vehicles",
    "电力": "Electric Power", "交通": "Transportation", "国防": "Defense", "工业": "Industrial",
    "导弹导航": "Missile Navigation", "导弹": "Missile", "制导炸弹": "Guided Bombs", "导弹飞行控制": "Missile Flight Control",
    "姿态控制": "Attitude Control", "导航制导": "Navigation & Guidance", "制导": "Guidance",
    "稳定平台": "Stabilized Platforms", "伺服控制": "Servo Control", "雷达稳定": "Radar Stabilization",
    "导引头稳定": "Seeker Stabilization", "水下高精度导航": "Underwater Navigation",
    "水下导航": "Underwater Navigation", "水下": "Underwater", "车船姿态基准": "Vehicle/Vessel Attitude Reference",
    "姿态参考": "Attitude Reference", "船舶导航": "Ship Navigation", "飞机导航": "Aircraft Navigation",
    "光纤电流传感": "Fiber Current Sensing", "光纤传感": "Fiber Optic Sensing", "其它光纤传感": "Other Fiber Sensing",
    "偏振敏感器件": "Polarization-Sensitive Devices", "熔锥型保偏耦合器": "Fused PM Couplers",
    "性能测试": "Performance Testing", "标定": "Calibration", "传感器标定": "Sensor Calibration",
    "石油": "Oil & Gas", "煤矿": "Mining", "矿山": "Mining", "机器人": "Robotics",
    "工程测量": "Engineering Surveying", "地质勘探": "Geological Exploration",
    "天线稳定": "Antenna Stabilization", "激光雷达": "LiDAR", "农用机械": "Agricultural Machinery",
    "高铁检测": "Railway Inspection", "桥梁检测": "Bridge Inspection",
    "惯性导航": "Inertial Navigation", "惯性测量": "Inertial Measurement",
    "光纤环圈": "Fiber Coil", "光纤环": "Fiber Coil", "四极缠绕": "Quadrupole Winding",
    "八极缠绕": "Octupole Winding", "自动涂胶": "Automatic Glue Coating", "精密排纤": "Precision Fiber Laying",
    "保偏光纤环": "PM Fiber Coils", "光学芯片": "Optical Chips", "耦合器": "Couplers", "光源模块": "Source Modules",
    "速率转台": "Rate Tables", "精密转台": "Precision Turntables", "环境测试": "Environmental Testing",
    "光谱分析": "Spectral Analysis", "相干通信": "Coherent Communication", "气体检测": "Gas Detection",
    "水声探测": "Underwater Acoustic Detection", "干涉测量": "Interferometry", "医疗": "Medical",
    "中长航时无人机": "Medium-Long Endurance UAV", "车载定位定向": "Vehicular Positioning & Orientation",
    "雷达/红外天线稳定平台": "Radar/IR Antenna Stabilized Platform", "港口测量系统": "Port Surveying Systems",
    "姿态控制": "Attitude Control", "稳控稳瞄设备": "Stabilization & Sighting Equipment",
    "掘进机/煤炭自动开采": "TBM / Automated Coal Mining", "传感器": "Sensors", "陀螺仪": "Gyroscopes",
    "干涉仪": "Interferometers", "伺服稳定": "Servo Stabilization", "卫星姿控": "Satellite Attitude Control",
    "保偏光纤制造": "PM Fiber Manufacturing", "光学器件": "Optical Devices",
    "自动化控制": "Automation Control", "机器人控制": "Robot Control",
    "云台稳定及控制": "Gimbal Stabilization & Control", "仪器仪表": "Instruments & Meters",
    "光纤制导导弹": "Fiber-Optic Guided Missiles", "系留无人机": "Tethered UAV",
    "水下ROV": "Underwater ROV", "铌酸锂波导尾纤": "LiNbO3 Waveguide Pigtail",
    "光纤偏振传感器": "Fiber Polarization Sensors", "其他固化应用": "Other Curing Applications",
    "光纤环测试": "Fiber Coil Testing", "保偏或单模光纤检测": "PM/SM Fiber Inspection",
    "光纤环生产测试": "Fiber Coil Production Testing", "光纤环使用前的筛选测试": "Fiber Coil Screening Tests",
    "光纤等的消光比测试": "Fiber Extinction Ratio Testing", "无源器件测试": "Passive Device Testing",
    "光纤陀螺及IMU的研究试验": "FOG & IMU Research & Testing", "全光缆结构适配": "Full Cable Structure Adaptation",
    "O-E-S-C-L全波段": "O-E-S-C-L Full Band", "FTTx高速路由": "FTTx High-Speed Routing",
    "小弯曲半径场景": "Small Bend Radius", "小尺寸器件适用": "Compact Devices",
    "无人机/车/船/艇姿态参考": "UAV/Vehicle/Boat Attitude Reference",
    "卫星稳定控制": "Satellite Stabilization Control", "多协议兼容": "Multi-Protocol Compatible",
    "WDM适配": "WDM Adaptation", "三级网络": "Tier-3 Networks", "综合业务": "Integrated Services",
    "全光缆适配": "Full Cable Adaptation", "天线稳定平台": "Antenna Stabilized Platform",
    "无人机姿态参考/航迹控制": "UAV Attitude Reference / Track Control",
    "车船姿态测量": "Vehicle/Vessel Attitude Measurement", "移动测绘系统": "Mobile Mapping Systems",
    "自动驾考系统": "Automated Driving Test Systems", "个人导航系统": "Personal Navigation Systems",
    "对光纤重新复绕或分切": "Fiber Rewinding & Cutting", "延时环圈": "Delay Coils",
    "导航制导与控制": "Navigation, Guidance & Control", "工程机械": "Construction Machinery",
    "高精度测绘": "High-Precision Surveying", "船舶与海洋作业": "Ship & Marine Operations",
    "惯性测量单元（IMU）": "IMU", "航空电子": "Avionics", "平台稳定系统": "Platform Stabilization Systems",
    "GPS辅助导航": "GPS-Aided Navigation", "无人机导航系统": "UAV Navigation Systems",
    "无人船": "Unmanned Surface Vessels", "水下航行器": "Underwater Vehicles",
    "智能驾驶": "Intelligent Driving", "弹载控制": "Missile-Borne Control",
    "智能矿山寻北": "Smart Mining North-Seeking", "检测与生产": "Testing & Production",
    "生物医学影像": "Biomedical Imaging", "生产调试和维修校准": "Production Debugging & Calibration",
    "速率和位置功能试验": "Rate & Position Function Tests",
    "其他惯性元件及装置的试验测试": "Other Inertial Component Testing",
    "用于激光二极管模块的研发": "Laser Diode Module R&D",
    "矿井等复杂环境定向": "Mine Environment Orientation", "单兵寻北": "Soldier North-Seeking",
    "石油测斜寻北": "Oil Well North-Seeking", "管道测量": "Pipeline Surveying",
    "轨道检测": "Rail Inspection", "商用车基准IMU": "Commercial Vehicle Reference IMU",
    "移动测量与姿态基准": "Mobile Positioning & Attitude Reference",
    "测绘与寻北": "Surveying & North-Seeking", "自动驾驶与弹载": "Autonomous Driving & Missile-Borne",
    "移动测量位置和姿态参考": "Mobile Position & Attitude Reference",
    "无人车": "Unmanned Ground Vehicles", "绕制光纤环圈": "Fiber Coil Winding",
    "高过载弹载使用": "High-G Missile-Borne Applications",
    "陀螺光模块生产测试": "Gyro Optical Module Production Testing",
    "陀螺光模块使用前的筛选测试": "Gyro Optical Module Screening Tests",
    "无人机/车/船/艇位置和姿态参考": "UAV/Vehicle/Boat Position & Attitude Reference",
    "光纤环圈": "Fiber Coils", "光纤环": "Fiber Coils",
}

# ---------------- 主流程 ----------------
def main():
    catalog = parse_catalog()
    extracts = load_extract()
    print(f"目录条目: {len(catalog)} | extracted: {len(extracts)}")

    used_ext = set()
    ext_by_id = {id(e): e for e in extracts}
    out, unmatched_cat, matched_ext = [], [], []
    recs_by_key = {}
    for e in catalog:
        if e["specTable"]:
            for row in e["specTable"]["rows"]:
                row["kEn"] = translate_key(row["k"])
                row["vEn"] = [translate_val(v) for v in row["v"]]
        rec = {
            "series": e["series"], "sub": e["sub"],
            "model": MODEL_EN.get(e["model"], e["model"]),
            "nameZh": e["nameZh"], "specTable": e["specTable"],
            "nameEn": None, "descZh": None, "descEn": None,
            "featsZh": [], "appsZh": [], "appsEn": [], "image": None,
        }
        ext = match_entry(e, extracts, used_ext)
        if ext:
            used_ext.add(id(ext))
            matched_ext.append(ext["model"])
            rec["folder"] = ext["folder"]
            nameZh, featsZh, appsZh, descZh = split_intro(ext.get("descZh") or "")
            _, _, _, descEn = split_intro(ext.get("descEn") or "", is_en=True)
            rec["nameEn"] = ext.get("nameEn")
            rec["enDoc"] = ext.get("enDoc")
            rec["descZh"], rec["descEn"] = descZh, descEn
            rec["featsZh"] = featsZh
            rec["appsZh"] = appsZh
            rec["appsEn"] = [APP_MAP.get(a, a) for a in appsZh]
            rec["image"] = ext.get("image")
        else:
            unmatched_cat.append(f"{e['model']}（{e['nameZh']}）")
            recs_by_key[(e["series"], re.sub(r"\d+$", "", e["model"]), e["sub"])] = rec
        out.append(rec)
    # 变体共享轮：同系列同 model 前缀（如 G652 低水峰 ← 低损耗；G657B3 ← G657A2）复用资料
    still = [r for r in out if not r.get("folder")]
    for r in still:
        prefix = re.sub(r"[A-Z]?\d+$", "", r["model"])  # 去变体后缀（数字或字母+数字）
        donor = next((x for x in out if x.get("folder") and x["series"] == r["series"]
                      and re.sub(r"[A-Z]?\d+$", "", x["model"]) == prefix
                      and x["sub"] == r["sub"] and x is not r), None)
        if donor:
            for k in ("nameEn", "descZh", "descEn", "featsZh", "appsZh", "appsEn", "image"):
                r[k] = donor[k]
            r["sharedFrom"] = donor["model"]

    orphan_ext = [e["model"] + "@" + e["folder"] for e in extracts if id(e) not in used_ext]
    # 中文 k 残留统计
    cjk_keys = []
    for r in out:
        if r["specTable"]:
            for row in r["specTable"]["rows"]:
                if has_cjk(row["k"]) and not any(zh in row["k"] for zh, _ in TERMS if zh in row["k"]):
                    cjk_keys.append(f"{r['model']}: {row['k']}")
                elif has_cjk(row["k"]):
                    pass
    json.dump(out, open(os.path.join(os.path.dirname(__file__), "assembled.json"), "w", encoding="utf-8"),
              ensure_ascii=False, indent=1)

    print(f"匹配成功: {len(out) - len(unmatched_cat)} | 目录未匹配: {len(unmatched_cat)} | extracted 孤儿: {len(orphan_ext)}")
    if unmatched_cat:
        print("未匹配目录条目:")
        for u in unmatched_cat:
            print("  -", u)
    if orphan_ext:
        print("孤儿 extracted:")
        for u in orphan_ext:
            print("  -", u)

if __name__ == "__main__":
    main()
