#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""直接测试并输出到文件"""
import sys
import os

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.utils import parse_deepseek_ocr_response, clean_ocr_text

# 测试数据
test_content = """<|ref|>text<|/ref|><|det|>[[36, 25, 912, 185]]<|/det|>       
42.(10分)现有 \\(n(n>100000)\\) 个数保存在一维数组M中,需要查找M中最小的10个数。请回答下列问题。                             
<|ref|>text<|/ref|><|det|>[[67, 194, 914, 345]]<|/det|>      
（1）设计一个完成上述查找任务的算法，要求平均情况下的比较次数尽可能少，简述其算法思想（不需要程序实现）。                 
<|ref|>text<|/ref|><|det|>[[68, 361, 680, 420]]<|/det|>      
（2）说明你所设计的算法平均情况下的时间复杂度 和空间复杂度。 

<|ref|>text<|/ref|><|det|>[[34, 680, 928, 997]]<|/det|>      
43.(15分）某CPU中部分数据通路如图所示，其中，GPRs为通用寄存器组；FR为标志寄存器，用于存放ALU产生的标志信息；带箭头虚线表示控制信号，如控制信号Read，Write分别表示主存读、主存写，MDRin 表示内部总线上数据写入MDR，MDRout表示MDR的内容送内部总线。"""

# 输出到文件
with open('test_output.txt', 'w', encoding='utf-8') as f:
    f.write("=" * 80 + "\n")
    f.write("DeepSeek OCR 解析功能测试\n")
    f.write("=" * 80 + "\n\n")
    
    # 测试解析
    f.write("【测试 1】解析文本块\n")
    f.write("-" * 80 + "\n")
    blocks = parse_deepseek_ocr_response(test_content)
    f.write(f"解析出 {len(blocks)} 个文本块\n\n")
    
    for i, block in enumerate(blocks, 1):
        f.write(f"文本块 {i}:\n")
        f.write(f"  坐标: {block['box']}\n")
        f.write(f"  文本: {block['text']}\n\n")
    
    # 测试清理
    f.write("\n【测试 2】清理文本\n")
    f.write("-" * 80 + "\n")
    clean_text = clean_ocr_text(test_content)
    f.write(clean_text + "\n")
    f.write("-" * 80 + "\n\n")
    
    # 验证
    f.write("\n【测试 3】验证结果\n")
    f.write("-" * 80 + "\n")
    
    expected_count = 4
    if len(blocks) == expected_count:
        f.write(f"✓ 文本块数量正确: {len(blocks)}\n")
    else:
        f.write(f"❌ 文本块数量错误: 期望 {expected_count}, 实际 {len(blocks)}\n")
    
    expected_coords = [
        [36, 25, 912, 185],
        [67, 194, 914, 345],
        [68, 361, 680, 420],
        [34, 680, 928, 997]
    ]
    
    for i, (block, expected) in enumerate(zip(blocks, expected_coords), 1):
        if block['box'] == expected:
            f.write(f"✓ 文本块 {i} 坐标正确\n")
        else:
            f.write(f"❌ 文本块 {i} 坐标错误: 期望 {expected}, 实际 {block['box']}\n")
    
    if '<|ref|>' not in clean_text and '<|det|>' not in clean_text:
        f.write("✓ 文本标记已清理\n")
    else:
        f.write("❌ 文本标记未清理\n")
    
    f.write("\n" + "=" * 80 + "\n")
    f.write("测试完成！结果已保存到 test_output.txt\n")
    f.write("=" * 80 + "\n")

print("测试完成！请查看 test_output.txt 文件")

