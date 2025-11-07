"""
工具函数模块
提供通用的辅助函数，如文件处理、Base64 编码等
"""

import re
import json
import base64
from pathlib import Path
from typing import Optional, List, Tuple, Dict
from PIL import Image


# 支持的图片格式
SUPPORTED_IMAGE_FORMATS = {'.jpg', '.jpeg', '.png', '.bmp'}


def encode_image_to_base64(image_path: str) -> str:
    """
    将图片文件编码为 Base64 字符串
    
    Args:
        image_path: 图片文件路径
        
    Returns:
        str: Base64 编码的字符串
        
    Raises:
        FileNotFoundError: 文件不存在
        ValueError: 文件格式不支持
    """
    path = Path(image_path)
    
    if not path.exists():
        raise FileNotFoundError(f"图片文件不存在: {image_path}")
    
    if path.suffix.lower() not in SUPPORTED_IMAGE_FORMATS:
        raise ValueError(f"不支持的图片格式: {path.suffix}")
    
    with open(image_path, 'rb') as image_file:
        encoded = base64.b64encode(image_file.read()).decode('utf-8')
    
    return encoded


def get_image_data_url(image_path: str) -> str:
    """
    获取图片的 Data URL（用于 API 请求）
    
    Args:
        image_path: 图片文件路径
        
    Returns:
        str: Data URL 格式的字符串，如 "data:image/jpeg;base64,..."
    """
    base64_str = encode_image_to_base64(image_path)
    
    # 根据文件扩展名确定 MIME 类型
    path = Path(image_path)
    mime_type_map = {
        '.jpg': 'image/jpeg',
        '.jpeg': 'image/jpeg',
        '.png': 'image/png',
        '.bmp': 'image/bmp'
    }
    mime_type = mime_type_map.get(path.suffix.lower(), 'image/jpeg')
    
    return f"data:{mime_type};base64,{base64_str}"


def validate_image_file(file_path: str) -> tuple[bool, Optional[str]]:
    """
    验证图片文件是否有效
    
    Args:
        file_path: 文件路径
        
    Returns:
        tuple[bool, Optional[str]]: (是否有效, 错误信息)
    """
    path = Path(file_path)
    
    # 检查文件是否存在
    if not path.exists():
        return False, f"文件不存在: {file_path}"
    
    # 检查是否是文件
    if not path.is_file():
        return False, f"不是有效的文件: {file_path}"
    
    # 检查文件扩展名
    if path.suffix.lower() not in SUPPORTED_IMAGE_FORMATS:
        return False, f"不支持的文件格式: {path.suffix}，支持的格式: {', '.join(SUPPORTED_IMAGE_FORMATS)}"
    
    # 尝试打开图片验证完整性
    try:
        with Image.open(file_path) as img:
            img.verify()
        return True, None
    except Exception as e:
        return False, f"图片文件损坏或无法读取: {str(e)}"


def get_safe_filename(filename: str, max_length: int = 100) -> str:
    """
    生成安全的文件名（移除特殊字符）
    
    Args:
        filename: 原始文件名
        max_length: 最大长度
        
    Returns:
        str: 安全的文件名
    """
    # 移除或替换不安全的字符
    unsafe_chars = '<>:"/\\|?*'
    safe_name = filename
    for char in unsafe_chars:
        safe_name = safe_name.replace(char, '_')
    
    # 限制长度
    if len(safe_name) > max_length:
        name_part = Path(safe_name).stem[:max_length-10]
        ext_part = Path(safe_name).suffix
        safe_name = f"{name_part}{ext_part}"
    
    return safe_name


def format_file_size(size_bytes: int) -> str:
    """
    格式化文件大小为人类可读的格式

    Args:
        size_bytes: 文件大小（字节）

    Returns:
        str: 格式化后的字符串，如 "1.5 MB"
    """
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.1f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.1f} TB"


def parse_deepseek_ocr_response(content: str) -> List[Dict[str, any]]:
    """
    解析 DeepSeek OCR API 返回的内容

    DeepSeek OCR 返回格式示例:
    <|ref|>text<|/ref|><|det|>[[x1, y1, x2, y2]]<|/det|>
    实际文本内容

    Args:
        content: OCR API 返回的原始内容

    Returns:
        List[Dict]: 解析后的文本块列表，每个包含 'text' 和 'box' 字段
    """
    blocks = []

    # 按行分割内容
    lines = content.split('\n')
    current_box = None
    current_text_lines = []

    for line in lines:
        # 检查是否包含坐标标记（注意：| 不需要转义，因为在字符类外）
        det_match = re.search(r'<\|det\|>(\[\[.*?\]\])</\|det\|>', line)

        if det_match:
            # 保存上一个文本块
            if current_box is not None and current_text_lines:
                text = '\n'.join(current_text_lines).strip()
                if text:
                    blocks.append({
                        'text': text,
                        'box': current_box
                    })

            # 解析新的坐标
            try:
                coords_str = det_match.group(1)
                coords = json.loads(coords_str)  # [[x1, y1, x2, y2]]
                if coords and len(coords) > 0 and len(coords[0]) == 4:
                    current_box = coords[0]  # [x1, y1, x2, y2]
                else:
                    current_box = [0, 0, 0, 0]
            except (json.JSONDecodeError, IndexError, ValueError):
                current_box = [0, 0, 0, 0]

            # 重置文本行
            current_text_lines = []

            # 提取当前行中标记后面的文本
            text_after_tag = re.sub(r'<\|ref\|>.*?</\|ref\|>', '', line)
            text_after_tag = re.sub(r'<\|det\|>.*?</\|det\|>', '', text_after_tag)
            text_after_tag = text_after_tag.strip()
            if text_after_tag:
                current_text_lines.append(text_after_tag)
        else:
            # 普通文本行，添加到当前文本块
            clean_line = re.sub(r'<\|ref\|>.*?</\|ref\|>', '', line)
            clean_line = clean_line.strip()
            if clean_line:
                current_text_lines.append(clean_line)

    # 保存最后一个文本块
    if current_box is not None and current_text_lines:
        text = '\n'.join(current_text_lines).strip()
        if text:
            blocks.append({
                'text': text,
                'box': current_box
            })

    return blocks


def clean_ocr_text(text: str) -> str:
    """
    清理 OCR 文本中的特殊标记

    Args:
        text: 原始 OCR 文本

    Returns:
        str: 清理后的纯文本
    """
    # 移除所有 DeepSeek OCR 标记
    text = re.sub(r'<\|ref\|>.*?</\|ref\|>', '', text)
    text = re.sub(r'<\|det\|>.*?</\|det\|>', '', text)

    # 移除多余的空白行
    lines = [line.strip() for line in text.split('\n') if line.strip()]

    return '\n'.join(lines)


if __name__ == '__main__':
    # 测试工具函数
    print("工具函数模块测试")
    print(f"支持的图片格式: {SUPPORTED_IMAGE_FORMATS}")
    print(f"文件大小格式化测试: {format_file_size(1536000)}")

