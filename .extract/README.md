# 产品数据提取管线（2026-10-16）

从母版资料自动生成网站产品数据的三个脚本，**改完按顺序执行 1→2→3**：

```
1. python extract_products.py   # 母版 docx → extracted.json（中英简介+图）+ 图片到 public/images/products/
2. python build_data.py         # 目录 md 参数表 + extracted 匹配 → assembled.json（kEn/vEn 翻译）
3. python gen_ts.py             # assembled.json → src/data/products/*.ts（6 分类文件+index.ts）
```

- 数据源：目录 `D:/利科夫/利科夫产品目录_2026/`（参数表权威）+ 母版 `D:/利科夫/2026年产品资料-利科夫/`（简介/图）
- 99 条目：fog 23 / mems 4 / imu 21 / ins 6 / accelerometers 5 / devices 40
- 匹配规则：型号精确→子串→名称关键词→中文段互含→公共子串≥6→同前缀变体共享
- 术语表：build_data.py TERMS（参数名）/APP_MAP（应用领域）/VAL_ZH_MAP（参数值备注）——补词直接加
- 未匹配边缘：G652低水峰/超低损耗等5条无独立资料（已共享/留参数表），FOGTS001 孤儿弃用
# 产品数据提取管线（2026-10-16）

从母版资料自动生成网站产品数据的三个脚本，**改完按顺序执行 1→2→3**：

```
1. python extract_products.py   # 母版 docx → extracted.json（中英简介+图）+ 图片到 public/images/products/
2. python build_data.py         # 目录 md 参数表 + extracted 匹配 → assembled.json（kEn/vEn 翻译）
3. python gen_ts.py             # assembled.json → src/data/products/*.ts（6 分类文件+index.ts）
```

- 数据源：目录 `D:\利科夫\利科夫产品目录_2026\`（参数表权威）+ 母版 `D:\利科夫\2026年产品资料-利科夫\`（简介/图）
- 99 条目：fog 23 / mems 4 / imu 21 / ins 6 / accelerometers 5 / devices 40
- 匹配规则：型号精确→子串→名称关键词→中文段互含→公共子串≥6→同前缀变体共享
- 术语表：build_data.py TERMS（参数名）/APP_MAP（应用领域）/VAL_ZH_MAP（参数值备注）——补词直接加
- 未匹配边缘：G652低水峰/超低损耗等5条无独立资料（已共享/留参数表），FOGTS001 孤儿弃用

## 图片筛选（2026-10-16）
- 启发式：尺寸图=白底(>50%)+近零饱和(<6)；白底渲染图(sat>5)保留；黑底实物照 sat 低但 white≈0 不误判
- 通用图黑名单：md5 跨 ≥4 文档重复 = logo/页眉装饰，排除
- image 路径由 gen_ts probe_image 按实际文件探测（png/jpeg/jpg），无图=型号占位
- 已知残留：约10张白底带标注渲染图（如 FS80）边界情况保留
