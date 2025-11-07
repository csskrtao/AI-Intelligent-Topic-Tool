# -*- coding: utf-8 -*-
"""
快速 OCR 测试 - 验证修复后的解析功能
"""
import sys
import os

sys.path.insert(0, '.')

from src.utils import parse_deepseek_ocr_response, clean_ocr_text

# 模拟 DeepSeek OCR 返回的内容
test_content = """<|ref|>text<|/ref|><|det|>[[36, 25, 912, 185]]<|/det|>       
42.(10分)现有 \\(n(n>100000)\\) 个数保存在一维数组M中,需要查找M中最小的10个数。请回答下列问题。
<|ref|>text<|/ref|><|det|>[[67, 194, 914, 345]]<|/det|>      
（1）设计一个完成上述查找任务的算法，要求平均情况下的比较次数尽可能少，简述其算法思想（不需要程序实现）。
<|ref|>text<|/ref|><|det|>[[68, 361, 680, 420]]<|/det|>      
（2）说明你所设计的算法平均情况下的时间复杂度 和空间复杂度。
<|ref|>text<|/ref|><|det|>[[34, 680, 928, 997]]<|/det|>      
43.(15分）某CPU中部分数据通路如图所示，其中，GPRs为通用寄存器组；FR为标志寄存器，用于存放ALU产生的标志信息；带箭头虚线表示控制信号，如控制信号Read，Write分别表示主存读、主存写，MDRin 表示内部总线上数据写入MDR，MDRout表示MDR的内容送内部总线。"""

print("=" * 80)
print("快速 OCR 解析测试")
print("=" * 80)
print()

# 测试解析功能
blocks = parse_deepseek_ocr_response(test_content)

print(f"✅ 解析结果: {len(blocks)} 个文本块")
print()

for i, block in enumerate(blocks, 1):
    text = block['text']
    box = block['box']
    print(f"文本块 {i}:")
    print(f"  📍 坐标: {box}")
    print(f"  📝 文本: {text[:60]}...")
    print()

# 测试清理功能
clean_text = clean_ocr_text(test_content)
print("=" * 80)
print("清理后的文本:")
print("-" * 80)
print(clean_text[:200] + "...")
print()

# 验证
print("=" * 80)
print("验证结果:")
print("-" * 80)

if len(blocks) == 4:
    print("✅ 文本块数量正确: 4")
else:
    print(f"❌ 文本块数量错误: {len(blocks)} (期望: 4)")

if all(len(b['box']) == 4 for b in blocks):
    print("✅ 所有文本块都有坐标")
else:
    print("❌ 部分文本块缺少坐标")

if '<|ref|>' not in clean_text and '<|det|>' not in clean_text:
    print("✅ 特殊标记已清理")
else:
    print("❌ 特殊标记未清理")

print()
print("=" * 80)
print("测试完成！")
print("=" * 80)

