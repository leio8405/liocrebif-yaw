"""校验 resources.ts 指定文章：字数、禁词、内链、结构。临时脚本。"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "src" / "data" / "resources.ts"

BANNED = [
    "strategically", "optimize", "optimise", "commitment", "resilience", "insight",
    "journey", "unlock", "empower", "leverage", "seamless", "cutting-edge",
    "robust solution", "state-of-the-art", "comprehensive", "revolutionary",
    "game-changing",
]

slug = sys.argv[1] if len(sys.argv) > 1 else "what-is-bias-stability"
text = SRC.read_text(encoding="utf-8")

start = text.index(f"slug: '{slug}'")
# 文章对象结束：下一个同级 slug 出现处
nxt = text.find("\n  {\n    slug: ", start + 10)
block = text[start: nxt if nxt != -1 else len(text)]

# 正文纯文本（仅 sections 部分）
sec_start = block.index("sections: [")
sec_end = block.index("faq: [")
body = block[sec_start:sec_end]

plain = re.sub(r"<[^>]+>", " ", body)
plain = re.sub(r"\s+", " ", plain)
words = [w for w in plain.split(" ") if re.search(r"[A-Za-z0-9]", w)]

# 包含标题与 description 的总字数
desc_m = re.search(r"title: '(.*?)',\n\s*description:", block, re.S)
title = desc_m.group(1) if desc_m else ""
allplain = title + " " + plain
allwords = [w for w in allplain.split(" ") if re.search(r"[A-Za-z0-9]", w)]

print(f"body words (sections only): {len(words)}")
print(f"with title:                {len(allwords)}")
print(f"H2 count:                  {block.count('h2: ')}")
print(f"tables:                    {body.count('<table')}")
print(f"lists (ul):                {body.count('<ul')}")
print(f"FAQ count:                 {block.count('        q: ')}")

links = re.findall(r'href="(/products/[^"]+)"', body)
print(f"internal links ({len(links)}): {links}")

# 禁词扫描：整块（含 title/description/faq）
low = block.lower()
hits = [b for b in BANNED if b in low]
print(f"BANNED HITS: {hits if hits else 'NONE'}")

# 关键词是否出现在正文前 100 词
kw = "bias stability"
first100 = " ".join(words[:100]).lower()
print(f"keyword in first 100 words: {kw in first100}")
