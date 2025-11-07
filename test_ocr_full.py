"""
完整测试 OCR 服务和解析功能
"""

from src.ocr_service import ocr_service
from src.question_splitter import question_splitter

print("=" * 80)
print("测试 OCR 服务和题目分割")
print("=" * 80)

# 测试图片
test_image = "test.png"

print(f"\n1. 正在识别图片: {test_image}")
print("-" * 80)

try:
    # 调用 OCR 服务
    result = ocr_service.recognize_image(test_image)
    
    print(f"\n2. OCR 识别完成")
    print(f"   - 识别到 {len(result.text_blocks)} 个文本块")
    print()
    
    # 显示每个文本块
    for i, block in enumerate(result.text_blocks, 1):
        print(f"   文本块 {i}:")
        print(f"   - 坐标: ({block.box.x1}, {block.box.y1}) -> ({block.box.x2}, {block.box.y2})")
        print(f"   - 文本: {block.text[:80]}...")
        print()
    
    print("\n3. 分割题目")
    print("-" * 80)
    
    # 分割题目
    questions = question_splitter.split_ocr_result(result)
    
    print(f"\n   分割出 {len(questions)} 道题目:")
    print()
    
    for q in questions:
        print(f"   题目 {q.question_id}:")
        print(f"   {q.text[:100]}...")
        print()
    
    print("=" * 80)
    print("✅ 测试完成！")
    print("=" * 80)
    
except Exception as e:
    print(f"\n❌ 错误: {e}")
    import traceback
    traceback.print_exc()

