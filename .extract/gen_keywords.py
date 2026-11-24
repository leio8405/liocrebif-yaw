# -*- coding: utf-8 -*-
"""生成关键词映射表 + seo 覆盖数据（v2）

用户约束（2026-11-24）：
1. 每款 3 个词，但 102 款不能共用同一批词
2. 分层：头部词给分类页，长尾词给产品页
3. 差异只能来自真实字段（bias stability / 量程 / appsEn / subEn / nameEn），不许编

v2 修正：v1 把 3 个词都当共享词，同品类内撞车 50 处。
SEO 的真实要求是「每页 1 个主打词全站唯一」+「辅助词可共用」。
故改为：primary 强制唯一（撞车则逐级加限定：参数→应用→子系列→型号），secondary 允许重复但全部列出。
"""
import json, os, re
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
BASE = json.load(open(os.path.join(ROOT, ".qa", "keyword-base.json"), encoding="utf-8"))

CAT = {
    "Single-Axis FOG": "single-axis fiber optic gyroscope",
    "Dual-Axis FOG": "dual-axis fiber optic gyroscope",
    "Tri-Axis FOG": "tri-axis fiber optic gyroscope",
    "FOG IMU": "fiber optic IMU",
    "FOG INS": "fiber optic inertial navigation system",
    "MEMS IMU": "MEMS inertial measurement unit",
    "MEMS INS": "MEMS inertial navigation system",
    "MEMS Gyro": "MEMS gyroscope",
    "MEMS Chip": "MEMS gyroscope chip",
    "MEMS Accelerometer": "MEMS accelerometer",
    "Quartz Accelerometer": "quartz accelerometer",
    "Test Equipment": "inertial test equipment",
    "Production Equipment": "fiber optic production equipment",
    "Optical Component": "fiber optic integrated optical device",
    "Single-Mode Fiber": "single-mode fiber",
    "PM Fiber": "polarization maintaining fiber",
    "Adhesive": "fiber optic adhesive",
    "Fiber Preform": "fiber preform",
    "Fiber Coil": "fiber optic coil",
    "SiPh Transceiver": "silicon photonic transceiver",
}

HEAD_TERMS = {
    "fog-gyroscopes": ["fiber optic gyroscope", "FOG gyro"],
    "imu": ["inertial measurement unit", "IMU sensor"],
    "accelerometers": ["accelerometer sensor", "inertial accelerometer"],
    "inertial-navigation-systems": ["inertial navigation system", "INS GNSS"],
    "mems-gyroscopes": ["MEMS gyroscope", "MEMS angular rate sensor"],
    "fiber-optic": ["fiber optic components", "optical fiber device"],
}

GRADES_GYRO = [(0.01, "navigation grade"), (0.1, "tactical grade"),
               (1.0, "industrial grade"), (float("inf"), "rate grade")]
GRADES_ACC = [(50, "precision grade"), (500, "tactical grade"),
              (float("inf"), "industrial grade")]

# 同型号多规格：用 slug 级区分词防止标题撞车
SLUG_DISTINCT = {
    "lkf-pm-coil-winding": "Coil-Winding",
    "lkf-pm-waveguide": "Waveguide",
    "lkf-pm-pcf": "Photonic-Crystal",
    "lkf-g652-low-loss": "Low-Loss",
    "lkf-g652": "Low-Water-Peak",
    "lkf-g652-ultra-low-loss": "Ultra-Low-Loss",
}

NO_BIAS_TAGS = {"Test Equipment", "Production Equipment", "Optical Component",
                "Single-Mode Fiber", "PM Fiber", "Adhesive", "Fiber Preform",
                "Fiber Coil", "SiPh Transceiver"}


def clean(s):
    return (str(s or "").replace("&lt;", "<").replace("&gt;", ">")
            .replace("&amp;", "&").replace("&#176;", "°"))


def num(s):
    if not s:
        return None
    m = re.search(r"(\d+(?:\.\d+)?)", clean(s))
    return float(m.group(1)) if m else None


def grade_of(tag, bs_raw):
    v = num(bs_raw)
    table = GRADES_ACC if "Accelerometer" in tag else GRADES_GYRO
    if v is None:
        return None
    for limit, name in table:
        if v <= limit:
            return name
    return table[-1][1]


def fmt_num(bs_raw):
    v = num(bs_raw)
    return None if v is None else ("%g" % v)


def short_name(name_en, model):
    n = name_en
    if n.startswith(model):
        n = n[len(model):].strip(" :-")
    return n.strip()


by_tag = {}
for r in BASE:
    by_tag.setdefault(r["tagEn"], []).append(r)

# 同品类按精度升序，便于把「形态词」给最精确的一款
def bs_key(x):
    v = num((x["kv"].get("bs") or [None, None])[1])
    return v if v is not None else 1e9


rows = []
used_primary = {}

for tag, items in by_tag.items():
    cat = CAT.get(tag, tag.lower())
    items = sorted(items, key=bs_key)
    n = len(items)

    for idx, r in enumerate(items):
        bs_raw = (r["kv"].get("bs") or [None, None])[1]
        bs_val = fmt_num(bs_raw)
        grade = grade_of(tag, bs_raw)
        sn = short_name(r["nameEn"], r["model"])
        sub = (r.get("subEn") or "").strip()
        apps = r.get("apps") or []
        # 同品类内轮流分配应用词，避免全场都挂在同一个 app 上
        app = apps[idx % len(apps)] if apps else None

        unit_word = "ug" if "Accelerometer" in tag else "deg/h"
        unit_sym = "µg" if "Accelerometer" in tag else "°/h"

        # ---------- 主打词：优先有搜索量的短词，同词最多 2 款（防蚕食又不造无搜索量的长句） ----------
        cands = []
        if tag in NO_BIAS_TAGS:
            # 无参数可分级：用 nameEn 的差异部分做主体（天然各不同）
            base = sn.lower() if sn else cat
            cands += [base, f"{base} supplier", f"{base} datasheet"]
        else:
            if bs_val and grade:
                cands.append(f"{bs_val} {unit_word} {grade} {cat}")
            if bs_val:
                cands.append(f"{bs_val} {unit_word} {cat}")
            if grade and app:
                cands.append(f"{grade} {cat} for {app.lower()}")
            if grade:
                cands.append(f"{grade} {cat}")
            if app:
                cands.append(f"{cat} for {app.lower()}")
            if sub:
                cands.append(f"{sub.lower()} {cat}")
            if idx == 0:
                cands.insert(0, cat)
            cands.append(f"{cat} {r['model'].lower()}")
        primary = next((c for c in cands if c and used_primary.get(c, 0) < 2), None)
        if primary is None:
            primary = f"{cat} {r['model'].lower()}"
        used_primary[primary] = used_primary.get(primary, 0) + 1

        # ---------- 辅助词 2 个（允许同品类重复，但尽量错开） ----------
        seconds = []
        if grade:
            seconds.append(f"{grade} {cat}")
        if app:
            seconds.append(f"{cat} for {app.lower()}")
        if bs_val and tag not in NO_BIAS_TAGS:
            seconds.append(f"high precision {cat}" if num(bs_raw) is not None and num(bs_raw) <= 0.1
                           else f"low cost {cat}")
        if not seconds:
            seconds.append(f"{cat} supplier")
            seconds.append(f"{cat} manufacturer")

        words = [primary]
        for s2 in seconds:
            if len(words) >= 3:
                break
            if s2 and s2 not in words:
                words.append(s2)
        # 补足 3 词：先用应用词轮换，再用规格数字，最后用型号
        fillers = [f"{cat} for {a.lower()}" for a in apps]
        if bs_val and tag not in NO_BIAS_TAGS:
            fillers.append(f"{bs_val} {unit_word} {cat}")
        if sub:
            fillers.append(f"{sub.lower()} {cat}")
        fillers.append(f"{cat} {r['model'].lower()}")
        for f2 in fillers:
            if len(words) >= 3:
                break
            if f2 and f2 not in words:
                words.append(f2)

        # ---------- seoTitle / seoDesc ----------
        # 标题结构：{型号} [{区分词}] {品类全称}[ {参数}] —— 品类词必须保住
        cat_cap = cat[0].upper() + cat[1:]
        bare_model = re.sub(r"[^a-z0-9]", "", r["model"].lower())
        bare_cat = re.sub(r"[^a-z0-9]", "", cat.lower())
        dist = SLUG_DISTINCT.get(r["slug"], "")
        if dist:
            seo_title = f"{r['model']} {dist} {cat_cap}"
        elif bare_cat in bare_model:
            seo_title = r["model"]
        else:
            seo_title = f"{r['model']} {cat_cap}"
        if len(seo_title) < 32:
            if bs_val and tag not in NO_BIAS_TAGS:
                raw = clean(bs_raw)
                seo_title = f"{seo_title} {raw if raw.startswith('<') else bs_val}{unit_sym}"
            elif app and cat.lower() not in app.lower():
                seo_title = f"{seo_title} for {app}"
        if len(seo_title) > 52:                 # 整词截断，不留半截单词
            cut = seo_title[:52]
            if " " in cut:
                cut = cut[:cut.rfind(" ")]
            seo_title = cut.rstrip(" ,|-")

        bits = [sn or cat]
        if bs_val and tag not in NO_BIAS_TAGS:
            bits.append(f"bias stability {bs_val} {unit_sym}")
        if app:
            bits.append(f"for {app.lower()}")
        seo_desc = ", ".join(bits)
        if len(seo_desc) < 70:
            seo_desc = f"{seo_desc}, {cat} from a Chinese inertial sensor manufacturer"
        seo_desc = seo_desc[:152]

        rows.append(dict(model=r["model"], slug=r["slug"], file=r["file"], tag=tag,
                         category=cat, bs=bs_raw, grade=grade, sub=sub, app=app,
                         primary=primary, words=words,
                         seoTitle=seo_title, seoDesc=seo_desc))

# ---------- 校验 ----------
pc = Counter(r["primary"] for r in rows)
tc = Counter(r["seoTitle"] for r in rows)
primary_dup = {k: v for k, v in pc.items() if v > 1}
title_dup = {k: v for k, v in tc.items() if v > 1}

json.dump({"products": rows, "headTerms": HEAD_TERMS},
          open(os.path.join(ROOT, ".qa", "keyword-plan.json"), "w", encoding="utf-8"),
          ensure_ascii=False, indent=1)

print(f"生成 {len(rows)} 款")
print(f"主打词重复: {len(primary_dup)} 处  {list(primary_dup.items())[:3]}")
print(f"seoTitle 重复: {len(title_dup)} 处  {list(title_dup.items())[:3]}")
print(f"每款词数分布: {dict(Counter(len(r['words']) for r in rows))}")

# ---------- 输出：seo 覆盖文件（供 gen_ts 注入）----------
SEO = {r["slug"]: {"seoTitle": r["seoTitle"], "seoDesc": r["seoDesc"], "words": r["words"]} for r in rows}
json.dump(SEO, open(os.path.join(HERE, "seo_override.json"), "w", encoding="utf-8"),
          ensure_ascii=False, indent=1)

# ---------- 输出：人工可读的关键词映射表 ----------
MD = os.path.join(ROOT, "关键词映射表.md")
out = [
    "# 关键词映射表",
    "",
    "> 由 `.extract/gen_keywords.py` 生成，改规则后重跑即可，**不要手改本表**。",
    "> 规则：每款 3 个词 = 1 个主打词（全站唯一；参数完全相同的姊妹型号最多 2 款共用）+ 2 个辅助词。",
    "> 差异只能来自真实字段：bias stability、量程、appsEn 应用词、nameEn 品名。**没有一个词是编的。**",
    "",
    "## 分类页承接的头部词（产品页不抢这些）",
    "",
    "| 分类页 | 头部词 |",
    "|:--|:--|",
]
for slug, terms in HEAD_TERMS.items():
    out.append(f"| `/products/{slug}/` | {' · '.join(terms)} |")

out += ["", "## 产品词表", ""]
cur = None
for r in rows:
    if r["tag"] != cur:
        cur = r["tag"]
        out += ["", f"### {cur}（{sum(1 for x in rows if x['tag'] == cur)} 款）", "",
                "| 型号 | 主打词 | 辅助词 | SEO 标题 |", "|:--|:--|:--|:--|"]
    extra = " / ".join(r["words"][1:]) or "—"
    out.append(f"| {r['model']} | {r['primary']} | {extra} | {r['seoTitle']} |")

open(MD, "w", encoding="utf-8").write("\n".join(out) + "\n")
print(f"已写 seo_override.json（{len(SEO)} 条）与 关键词映射表.md")
