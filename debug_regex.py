#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""调试正则表达式"""
import re

test_line = """<|ref|>text<|/ref|><|det|>[[36, 25, 912, 185]]<|/det|>       
42.(10分)现有题目"""

print("测试字符串:")
print(repr(test_line))
print()

# 测试当前的正则表达式（有问题的）
pattern1 = r'<\|det\|>(\[\[.*?\]\])</\|det\|>'
print(f"模式 1 (当前): {pattern1}")
match1 = re.search(pattern1, test_line)
print(f"匹配结果: {match1}")
print()

# 测试修正后的正则表达式
pattern2 = r'<\|det\|>(\[\[.*?\]\])<\/\|det\|>'
print(f"模式 2 (修正): {pattern2}")
match2 = re.search(pattern2, test_line)
print(f"匹配结果: {match2}")
if match2:
    print(f"匹配内容: {match2.group(1)}")
print()

# 测试清理正则
print("测试清理正则:")
text = test_line
print(f"原始: {text[:80]}")

# 当前的清理方式
cleaned1 = re.sub(r'<\|ref\|>.*?</\|ref\|>', '', text)
cleaned1 = re.sub(r'<\|det\|>.*?</\|det\|>', '', cleaned1)
print(f"清理后 (当前): {cleaned1[:80]}")

# 修正后的清理方式
cleaned2 = re.sub(r'<\|ref\|>.*?<\/\|ref\|>', '', text)
cleaned2 = re.sub(r'<\|det\|>.*?<\/\|det\|>', '', cleaned2)
print(f"清理后 (修正): {cleaned2[:80]}")

