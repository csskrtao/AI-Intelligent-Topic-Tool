"""
测试边界框 API 返回
验证后端是否正确返回边界框坐标数据
"""

import requests
import json
from pathlib import Path

def test_upload_api():
    """测试上传 API 是否返回边界框数据"""
    
    # API 端点
    url = "http://localhost:8000/api/upload"
    
    # 测试图片
    test_image = Path("test.png")
    
    if not test_image.exists():
        print(f"❌ 测试图片不存在: {test_image}")
        return
    
    print("=" * 80)
    print("测试边界框 API")
    print("=" * 80)
    print(f"\n📤 上传图片: {test_image}")
    
    # 上传图片
    with open(test_image, 'rb') as f:
        files = {'file': (test_image.name, f, 'image/png')}
        response = requests.post(url, files=files)
    
    # 检查响应
    if response.status_code != 200:
        print(f"\n❌ API 请求失败: {response.status_code}")
        print(response.text)
        return
    
    # 解析响应
    data = response.json()
    
    print(f"\n✅ API 请求成功")
    print(f"   - 成功: {data.get('success')}")
    print(f"   - 消息: {data.get('message')}")
    print(f"   - 图片 URL: {data.get('image_url')}")
    print(f"   - 题目数量: {len(data.get('questions', []))}")
    
    # 检查每个题目的边界框
    print("\n" + "=" * 80)
    print("题目边界框数据")
    print("=" * 80)
    
    questions = data.get('questions', [])
    
    for i, question in enumerate(questions, 1):
        print(f"\n题目 {i}:")
        print(f"   - ID: {question.get('question_id')}")
        print(f"   - 有边界框: {question.get('has_bounding_box')}")
        
        bbox = question.get('bounding_box')
        if bbox:
            print(f"   - 边界框坐标:")
            print(f"     • x1: {bbox.get('x1')}")
            print(f"     • y1: {bbox.get('y1')}")
            print(f"     • x2: {bbox.get('x2')}")
            print(f"     • y2: {bbox.get('y2')}")
            print(f"     • 宽度: {bbox.get('x2') - bbox.get('x1')}")
            print(f"     • 高度: {bbox.get('y2') - bbox.get('y1')}")
        else:
            print(f"   - ⚠️  无边界框数据")
        
        # 显示文本预览
        text = question.get('text', '')
        preview = text[:100].replace('\n', ' ') + ('...' if len(text) > 100 else '')
        print(f"   - 文本预览: {preview}")
    
    # 统计
    print("\n" + "=" * 80)
    print("统计信息")
    print("=" * 80)
    
    total = len(questions)
    with_bbox = sum(1 for q in questions if q.get('bounding_box'))
    without_bbox = total - with_bbox
    
    print(f"\n总题目数: {total}")
    print(f"有边界框: {with_bbox} ({with_bbox/total*100:.1f}%)" if total > 0 else "有边界框: 0")
    print(f"无边界框: {without_bbox} ({without_bbox/total*100:.1f}%)" if total > 0 else "无边界框: 0")
    
    if with_bbox == total and total > 0:
        print("\n✅ 所有题目都有边界框数据！")
    elif with_bbox > 0:
        print(f"\n⚠️  部分题目缺少边界框数据")
    else:
        print(f"\n❌ 所有题目都没有边界框数据")
    
    print("\n" + "=" * 80)
    print("✅ 测试完成！")
    print("=" * 80)

if __name__ == '__main__':
    try:
        test_upload_api()
    except requests.exceptions.ConnectionError:
        print("\n❌ 无法连接到后端服务")
        print("   请确保后端服务正在运行: python backend_api.py")
    except Exception as e:
        print(f"\n❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()

