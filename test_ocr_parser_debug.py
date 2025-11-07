"""
调试 DeepSeek OCR 响应解析
"""

import re
import json

# 测试数据
test_content = """<|ref|>text<|/ref|><|det|>[[36, 25, 912, 185]]<|/det|>       
42.(10分)现有 \\(n(n>100000)\\) 个数保存在一维数组M中,需要查找M中最小的10个数。请回答下列问题。"""

print("原始内容:")
print(repr(test_content))
print()

# 测试正则匹配
pattern = r'<\|det\|>(\[\[.*?\]\])<\/\|det\|>'
matches = re.findall(pattern, test_content)
print(f"找到 {len(matches)} 个坐标匹配:")
for m in matches:
    print(f"  - {m}")
print()

# 测试按行分割
lines = test_content.split('\n')
print(f"分割成 {len(lines)} 行:")
for i, line in enumerate(lines):
    print(f"  行 {i}: {repr(line)}")
print()

# 测试每行的匹配
for i, line in enumerate(lines):
    det_match = re.search(r'<\|det\|>(\[\[.*?\]\])<\/\|det\|>', line)
    if det_match:
        print(f"行 {i} 匹配到坐标: {det_match.group(1)}")
        
        # 提取文本
        text_after_tag = re.sub(r'<\|ref\|>.*?<\/\|ref\|>', '', line)
        text_after_tag = re.sub(r'<\|det\|>.*?<\/\|det\|>', '', text_after_tag)
        text_after_tag = text_after_tag.strip()
        print(f"  提取的文本: {repr(text_after_tag)}")

