"""
验证 OCR 解析功能
"""
import sys
import os

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.utils import parse_deepseek_ocr_response, clean_ocr_text

# 测试数据（模拟 DeepSeek OCR 返回格式）
test_content = """<|ref|>text<|/ref|><|det|>[[36, 25, 912, 185]]<|/det|>       
42.(10分)现有 \\(n(n>100000)\\) 个数保存在一维数组M中,需要查找M中最小的10个数。请回答下列问题。                             
<|ref|>text<|/ref|><|det|>[[67, 194, 914, 345]]<|/det|>      
（1）设计一个完成上述查找任务的算法，要求平均情况下的比较次数尽可能少，简述其算法思想（不需要程序实现）。                 
<|ref|>text<|/ref|><|det|>[[68, 361, 680, 420]]<|/det|>      
（2）说明你所设计的算法平均情况下的时间复杂度 和空间复杂度。 

<|ref|>text<|/ref|><|det|>[[34, 680, 928, 997]]<|/det|>      
43.(15分）某CPU中部分数据通路如图所示，其中，GPRs为通用寄存器组；FR为标志寄存器，用于存放ALU产生的标志信息；带箭头虚线表示控制信号，如控制信号Read，Write分别表示主存读、主存写，MDRin 表示内部总线上数据写入MDR，MDRout表示MDR的内容送内部总线。"""

print("=" * 80)
print("验证 DeepSeek OCR 解析功能")
print("=" * 80)

# 测试 1: 解析文本块
print("\n【测试 1】解析文本块:")
print("-" * 80)
blocks = parse_deepseek_ocr_response(test_content)
print(f"✓ 解析出 {len(blocks)} 个文本块")

if len(blocks) == 0:
    print("❌ 错误：没有解析出任何文本块！")
    sys.exit(1)

print()
for i, block in enumerate(blocks, 1):
    print(f"文本块 {i}:")
    print(f"  坐标: {block['box']}")
    print(f"  文本: {block['text'][:60]}...")
    print()

# 测试 2: 验证坐标
print("\n【测试 2】验证坐标信息:")
print("-" * 80)
expected_coords = [
    [36, 25, 912, 185],
    [67, 194, 914, 345],
    [68, 361, 680, 420],
    [34, 680, 928, 997]
]

all_coords_correct = True
for i, (block, expected) in enumerate(zip(blocks, expected_coords), 1):
    if block['box'] == expected:
        print(f"✓ 文本块 {i} 坐标正确: {block['box']}")
    else:
        print(f"❌ 文本块 {i} 坐标错误:")
        print(f"   期望: {expected}")
        print(f"   实际: {block['box']}")
        all_coords_correct = False

# 测试 3: 验证文本内容
print("\n【测试 3】验证文本内容:")
print("-" * 80)
expected_texts = [
    "42.(10分)现有",
    "（1）设计一个完成上述查找任务的算法",
    "（2）说明你所设计的算法平均情况下的时间复杂度",
    "43.(15分）某CPU中部分数据通路如图所示"
]

all_texts_correct = True
for i, (block, expected_start) in enumerate(zip(blocks, expected_texts), 1):
    if block['text'].startswith(expected_start):
        print(f"✓ 文本块 {i} 内容正确")
    else:
        print(f"❌ 文本块 {i} 内容错误:")
        print(f"   期望开头: {expected_start}")
        print(f"   实际开头: {block['text'][:30]}")
        all_texts_correct = False

# 测试 4: 清理文本
print("\n【测试 4】清理文本标记:")
print("-" * 80)
clean_text = clean_ocr_text(test_content)
if '<|ref|>' in clean_text or '<|det|>' in clean_text:
    print("❌ 错误：清理后的文本仍包含标记")
    all_texts_correct = False
else:
    print("✓ 文本标记已成功清理")
    print(f"\n清理后的文本（前100字符）:\n{clean_text[:100]}...")

# 总结
print("\n" + "=" * 80)
if len(blocks) == 4 and all_coords_correct and all_texts_correct:
    print("✅ 所有测试通过！OCR 解析功能正常工作")
    print("=" * 80)
    sys.exit(0)
else:
    print("❌ 部分测试失败，请检查解析逻辑")
    print("=" * 80)
    sys.exit(1)

