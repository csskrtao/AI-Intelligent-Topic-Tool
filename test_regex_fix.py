#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""直接测试正则表达式修复"""
import re

test_line = """<|ref|>text<|/ref|><|det|>[[36, 25, 912, 185]]<|/det|>       
42.(10分)现有题目"""

print("=" * 80)
print("测试正则表达式修复")
print("=" * 80)
print()

# 测试修正后的正则表达式
pattern = r'<\|det\|>(\[\[.*?\]\])<\/\|det\|>'
print(f"正则模式: {pattern}")
print(f"测试字符串: {test_line[:80]}...")
print()

match = re.search(pattern, test_line)
if match:
    print(f"✓ 匹配成功！")
    print(f"  匹配内容: {match.group(1)}")
else:
    print(f"❌ 匹配失败")

print()
print("-" * 80)

# 测试清理
print("测试清理功能:")
cleaned = re.sub(r'<\|ref\|>.*?<\/\|ref\|>', '', test_line)
cleaned = re.sub(r'<\|det\|>.*?<\/\|det\|>', '', cleaned)
cleaned = cleaned.strip()

print(f"清理后: {cleaned}")

if '<|ref|>' not in cleaned and '<|det|>' not in cleaned:
    print("✓ 标记已清理")
else:
    print("❌ 标记未清理")

print()
print("=" * 80)

