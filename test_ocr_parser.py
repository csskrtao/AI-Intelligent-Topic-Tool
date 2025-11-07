"""
测试 DeepSeek OCR 响应解析
"""

from src.utils import parse_deepseek_ocr_response, clean_ocr_text

# 测试数据（从你提供的 OCR 结果）
test_content = """<|ref|>text<|/ref|><|det|>[[36, 25, 912, 185]]<|/det|>       
42.(10分)现有 \\(n(n>100000)\\) 个数保存在一维数组M中,需要查找M中最小的10个数。请回答下列问题。                             
<|ref|>text<|/ref|><|det|>[[67, 194, 914, 345]]<|/det|>      
（1）设计一个完成上述查找任务的算法，要求平均情况下的比较次数尽可能少，简述其算法思想（不需要程序实现）。                 
<|ref|>text<|/ref|><|det|>[[68, 361, 680, 420]]<|/det|>      
（2）说明你所设计的算法平均情况下的时间复杂度 和空间复杂度。 

<|ref|>text<|/ref|><|det|>[[34, 680, 928, 997]]<|/det|>      
43.(15分）某CPU中部分数据通路如图所示，其中，GPRs为通用寄存器组；FR为标志寄存器，用于存放ALU产生的标志信息；带箭头虚线表示控制信号，如控制信号Read，Write分别表示主存读、主存写，MDRin 表示内部总线上数据写入MDR，MDRout表示MDR的内容送内部总线。"""

print("=" * 80)
print("测试 DeepSeek OCR 响应解析")
print("=" * 80)

# 测试解析函数
print("\n1. 解析文本块:")
blocks = parse_deepseek_ocr_response(test_content)
print(f"   解析出 {len(blocks)} 个文本块\n")

for i, block in enumerate(blocks, 1):
    print(f"   文本块 {i}:")
    print(f"   - 坐标: {block['box']}")
    print(f"   - 文本: {block['text'][:50]}...")
    print()

# 测试清理函数
print("\n2. 清理后的纯文本:")
print("-" * 80)
clean_text = clean_ocr_text(test_content)
print(clean_text)
print("-" * 80)

print("\n✅ 测试完成！")

