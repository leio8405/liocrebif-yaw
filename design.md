# Design — Liocrebif 官网 (liocrebif-yaw)

A locked design system for this site. Every page redesign reads this file before
emitting code. Do not regenerate per page — extend or amend this file when the
system needs to grow.

## Genre
modern-minimal（B2B 精密仪器公司 · 工程文档气质）

## Theme
Cobalt — 冷白工程纸面 + 单一电光钴蓝信号 + hairline 细线结构。
"仪器面板"而非"营销模板"。来源：hallmark catalog Cobalt，适配硬件公司
（用真实产品规格卡替代代码卡，mono 参数语言不变）。

## Colors (OKLCH / Tailwind v4 @theme in src/styles/global.css)
- `--color-paper`    oklch(98.5% 0.004 250)  冷白纸面（非纯白）
- `--color-paper-2`  oklch(96.5% 0.005 250)  次级面（数据带底）
- `--color-ink`      oklch(24% 0.02 258)     主墨色（标题）
- `--color-ink-2`    oklch(34% 0.018 257)    正文墨
- `--color-muted`    oklch(52% 0.012 256)    弱化文字
- `--color-rule`     oklch(90% 0.008 255)    hairline 细线
- `--color-accent`   oklch(58% 0.20 256)     电光钴蓝（唯一信号色，<5% 视口）
- `--color-accent-ink` oklch(98.5% 0.004 250) 钴蓝底上的文字
- `--color-graphite` oklch(22% 0.016 260)    石墨深色带 / 规格卡底
- `--color-graphite-ink` oklch(70% 0.01 256) 石墨底上的弱化文字
- `--color-focus`    = accent

强调色只用于：eyebrow tick、主按钮、focus ring、关键数据、mono 状态签、
当前导航项。禁止：大面积色块、渐变、彩色卡片。

## Typography
- Display: Space Grotesk, 500/600, letter-spacing -0.02em~-0.03em（英文标题）
- Body: Inter 400/500（英文正文）
- Mono: JetBrains Mono 400/500 — 型号、参数、eyebrow、状态签、数据标签
  （UPPERCASE + 0.06em tracking）
- 中文: Noto Sans SC 400/500/700（display 与 body 均回退到它）
- Hero 标题: clamp(2.5rem, 5vw + 0.5rem, 4rem)，墨色，**禁止渐变文字**
- 禁止斜体标题。

## Spacing
Tailwind 默认 4pt 网格。区块间距 `py-20 sm:py-28`（≈ space-2xl/3xl）。
容器 `.container-page` max-w 80rem（沿用）。

## Motion
- 无动效库。Reveal: IntersectionObserver 加 `.is-in`（fade + 10px rise，
  0.6s cubic-bezier(0.16,1,0.3,1)），可选、克制。
- Hover: 链接钴蓝下划线生长；卡片 1px 边框变钴蓝。无 scale 弹跳。
- `prefers-reduced-motion: reduce` → 全部静态可见。

## Microinteractions stance
- silent success（表单成功静默提示，不弹庆祝）
- hover tooltip delay 800ms / focus 0ms（本站基本无 tooltip）
- 悬浮联系按钮：方形 hairline 样式，无 scale 动画

## CTA voice
- Primary: 钴蓝实心，6px 圆角，"Request a Datasheet / 获取产品手册"、
  "Send Inquiry / 发送询盘"——动词+具体对象，禁止 "Learn more"
- Secondary: 墨色 1px 描边，同圆角
- 每个 CTA 区块最多一个主按钮

## Per-page allowances
- 首页（营销页）: 可用 graphite 规格卡 + 真实产品图。禁 emoji 图标。
- 产品页: 索引/数据表气质，mono 型号列。
- 关于/联系: 纯排版，无 enrichment。
- 每页最多一段 graphite 深色带（light → dark → light 节奏）。

## What pages MUST share
- Wordmark（LIOCREBIF + mono 小字 YAW TECHNOLOGY）
- 钴蓝强调色及其克制的用法
- 三字体（Space Grotesk / Inter / JetBrains Mono + Noto Sans SC 中文栈）
- CTA voice（6px 圆角、钴蓝实心/墨色描边）
- hairline 分隔语言（1px --color-rule，禁止阴影卡片、禁止玻璃拟态）
- mono UPPERCASE 标签语言

## What pages MAY differ on
- 区块顺序与数量（保持现有 IA 为准）
- 深色带的位置（首页在中段，产品页可在页尾 CTA）

## 页脚
Ft5 Statement：声明句（motto）+ 单行链接 + 版权行。禁止四列链接矩阵。
