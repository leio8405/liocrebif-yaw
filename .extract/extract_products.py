# -*- coding: utf-8 -*-
"""
从母版产品资料批量提取：中英简介文本 + 实物图
输出: 网站项目/.extract/extracted.json  + 图片到 public/images/products/
"""
import os, re, json, zipfile, shutil, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SRC = r"D:\利科夫\2026年产品资料-利科夫"
OUT_DIR = os.path.dirname(os.path.abspath(__file__))
IMG_DIR = os.path.join(ROOT, "public", "images", "products")
os.makedirs(OUT_DIR, exist_ok=True)
os.makedirs(IMG_DIR, exist_ok=True)

SERIES = ["1、光纤陀螺系列", "2、MEMS陀螺系列", "3、IMU系列", "4、INS系统", "5、加速度计", "6、光纤陀螺解决方案", "7、光纤筒"]

def docx_paragraphs(path):
    """解 docx，返回段落文本列表（跳过空段）"""
    try:
        with zipfile.ZipFile(path) as z:
            xml = z.read("word/document.xml").decode("utf-8", "ignore")
    except Exception as e:
        return None
    # 按段落切
    paras = re.split(r"</w:p>", xml)
    out = []
    for p in paras:
        texts = re.findall(r"<w:t[^>]*>([^<]*)</w:t>", p)
        t = "".join(texts).strip()
        if t:
            out.append(t)
    return out

def docx_images(path):
    """返回 [(name, size)] 按大小降序"""
    try:
        with zipfile.ZipFile(path) as z:
            media = [(n, z.getinfo(n).file_size) for n in z.namelist()
                     if n.startswith("word/media/") and n.lower().endswith((".png", ".jpg", ".jpeg"))]
    except Exception:
        return []
    return sorted(media, key=lambda x: -x[1])

def pick(paths, patterns):
    """按优先级匹配文件"""
    for pat in patterns:
        for p in paths:
            if re.search(pat, os.path.basename(p)):
                return p
    return None

NOISE = re.compile(r"^(利科夫|Liocrebif|LIOCREBIF|LKF|武汉|Wuhan|www\.|Tel|电话|邮箱|Email|地址|Add|http)", re.I)

results = []
skipped = []
for series in SERIES:
    sroot = os.path.join(SRC, series)
    if not os.path.isdir(sroot):
        continue
    for root, dirs, files in os.walk(sroot):
        docx_all = [os.path.join(root, f) for f in files if f.lower().endswith(".docx")]
        if not docx_all:
            continue
        folder = os.path.basename(root)
        if re.search(r"原厂|备份|临时|旧", folder):
            continue
        # 放宽：任何直接含 docx 的目录都是产品资料夹；型号从 docx 文件名或目录名提取
        all_names = " ".join(os.path.basename(p) for p in docx_all) + " " + folder
        short = None
        mm = re.search(r"(LKF-[A-Z0-9]+(?:\s?\d+)?)", all_names)
        if mm:
            short = mm.group(1).replace(" ", "")
        else:
            m = re.match(r"^\d+[-\d]*、(.+)$", folder)
            if m:
                short = m.group(1).strip()
            elif re.search(r"[A-Z]{2,}\d", folder):
                short = folder
        if not short:
            continue
        sub = os.path.basename(os.path.dirname(root))  # 子系列名

        zh = pick(docx_all, [r"^1、.*简介.*中文", r"^\d+、.*简介.*中文.*\.docx$"]) or \
             pick(docx_all, [r"简介.*中文.*\.docx$"])
        en = pick(docx_all, [r"Data Sheet.*_EN\.docx$", r"Datasheet.*_EN\.docx$", r"Data.*Sheet.*EN\.docx$"])

        rec = {"series": series, "sub": sub, "folder": folder, "short": short,
               "zhDoc": os.path.basename(zh) if zh else None,
               "enDoc": os.path.basename(en) if en else None,
               "descZh": None, "descEn": None, "nameEn": None, "image": None}

        # 中文名称：取文件夹 docx 文件名中的 LKF- 型号名（允许型号与数字间有空格，如 LKF-FIOS 1550）
        any_doc = zh or en or docx_all[0]
        mm = re.search(r"(LKF-[A-Z0-9]+(?:\s?\d+)?)", os.path.basename(any_doc))
        rec["model"] = mm.group(1).replace(" ", "") if mm else short

        if zh:
            paras = docx_paragraphs(zh)
            if paras:
                # 英文名称：中文简介标题后常见英文名（首段含英文长串）
                body = []
                for t in paras:
                    if NOISE.match(t):
                        continue
                    # 跳过纯数字/单位行和表头行
                    if len(t) < 8 and not re.search(r"[\u4e00-\u9fff]", t):
                        continue
                    body.append(t)
                    if len(" ".join(body)) > 1200:
                        break
                rec["descZh"] = " ".join(body)[:1500] if body else None
                # 英文名：中文简介里第一段全英文且 >10 字符的
                for t in paras[:6]:
                    if re.fullmatch(r"[A-Za-z0-9 ,\-\(\)/&\.＋]{15,}", t):
                        rec["nameEn"] = t.strip()
                        break
        if en:
            paras = docx_paragraphs(en)
            if paras:
                body = []
                for t in paras:
                    if re.match(r"^(Liocrebif|LIOCREBIF|LKF|www\.|Tel|Email|Add)", t, re.I):
                        continue
                    if not re.search(r"[A-Za-z]{4,}", t):
                        continue
                    if re.match(r"^[\d\.\s\-≤≥±<>]+$", t):
                        continue
                    body.append(t)
                    if len(" ".join(body)) > 500:
                        break
                rec["descEn"] = " ".join(body)[:2000] if body else None

        # 图片：从中文简介 docx 提取最大图
        img_src = zh or en
        if img_src:
            media = docx_images(img_src)
            big = [m for m in media if m[1] > 25000]
            if big:
                name, size = big[0]
                ext = os.path.splitext(name)[1].lower()
                safe_model = re.sub(r"[^A-Za-z0-9\-]", "", rec["model"])
                dest = os.path.join(IMG_DIR, safe_model + ext)
                try:
                    with zipfile.ZipFile(img_src) as z:
                        with z.open(name) as fsrc, open(dest, "wb") as fdst:
                            shutil.copyfileobj(fsrc, fdst)
                    rec["image"] = "/images/products/" + os.path.basename(dest)
                except Exception as e:
                    rec["imageErr"] = str(e)

        results.append(rec)

with open(os.path.join(OUT_DIR, "extracted.json"), "w", encoding="utf-8") as f:
    json.dump(results, f, ensure_ascii=False, indent=1)

ok = sum(1 for r in results if r["descZh"] and r["descEn"] and r["image"])
print(f"共 {len(results)} 条 | 简介中英+图齐全: {ok}")
print(f"缺中文简介: {sum(1 for r in results if not r['descZh'])}")
print(f"缺英文简介: {sum(1 for r in results if not r['descEn'])}")
print(f"缺图片: {sum(1 for r in results if not r['image'])}")
print("样例前3条:")
for r in results[:3]:
    print(json.dumps(r, ensure_ascii=False)[:300])
