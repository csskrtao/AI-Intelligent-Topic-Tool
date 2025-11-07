"""
OCR 服务模块
封装 DeepSeek OCR API 调用逻辑
"""

import requests
from typing import Optional, Dict, Any, List
from pathlib import Path

from .config import config
from .models import OCRResult, TextBlock, BoundingBox
from .utils import get_image_data_url, parse_deepseek_ocr_response, clean_ocr_text


class OCRService:
    """DeepSeek OCR API 服务类"""
    
    def __init__(self):
        """初始化 OCR 服务"""
        self.api_key = config.api_key
        self.api_url = config.get_api_endpoint('chat/completions')
        self.model_name = config.ocr_model_name
        self.timeout = config.ocr_timeout
        self.max_tokens = config.max_tokens
    
    def recognize_image(
        self, 
        image_path: str, 
        prompt: str = "请识别图片中的所有文字，保持原有格式和布局",
        stream: bool = False
    ) -> OCRResult:
        """
        识别图片中的文字
        
        Args:
            image_path: 图片文件路径
            prompt: 提示词，指定识别要求
            stream: 是否使用流式响应
            
        Returns:
            OCRResult: OCR 识别结果
            
        Raises:
            FileNotFoundError: 图片文件不存在
            ValueError: API 配置无效或响应格式错误
            requests.RequestException: API 请求失败
        """
        # 验证配置
        is_valid, error_msg = config.validate()
        if not is_valid:
            raise ValueError(f"配置无效: {error_msg}")
        
        # 验证文件
        if not Path(image_path).exists():
            raise FileNotFoundError(f"图片文件不存在: {image_path}")
        
        # 获取图片的 Data URL
        image_data_url = get_image_data_url(image_path)
        
        # 构造请求体
        payload = {
            "model": self.model_name,
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": prompt
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": image_data_url
                            }
                        }
                    ]
                }
            ],
            "max_tokens": self.max_tokens,
            "stream": stream
        }
        
        # 设置请求头
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }
        
        try:
            # 发送请求（禁用代理以避免代理连接问题）
            response = requests.post(
                self.api_url,
                json=payload,
                headers=headers,
                timeout=self.timeout,
                proxies={'http': None, 'https': None}  # 禁用代理
            )
            response.raise_for_status()
            
            # 解析响应
            result_data = response.json()
            
            # 提取识别的文本
            if 'choices' not in result_data or len(result_data['choices']) == 0:
                raise ValueError("API 响应格式错误：缺少 choices 字段")

            content = result_data['choices'][0]['message']['content']

            # 创建 OCRResult 对象
            ocr_result = OCRResult(
                image_path=image_path,
                raw_response=result_data
            )

            # 解析 DeepSeek OCR 的响应格式
            # DeepSeek OCR 返回包含文本和边界框坐标的特殊格式
            parsed_blocks = parse_deepseek_ocr_response(content)

            if parsed_blocks:
                # 添加解析后的文本块（包含坐标信息）
                for block in parsed_blocks:
                    box_coords = block['box']  # [x1, y1, x2, y2]
                    ocr_result.add_text_block(
                        text=block['text'],
                        box=BoundingBox(
                            x1=box_coords[0],
                            y1=box_coords[1],
                            x2=box_coords[2],
                            y2=box_coords[3]
                        ),
                        confidence=None
                    )
            else:
                # 如果解析失败，使用清理后的纯文本
                clean_text = clean_ocr_text(content)
                ocr_result.add_text_block(
                    text=clean_text,
                    box=BoundingBox(0, 0, 0, 0),
                    confidence=None
                )

            return ocr_result
            
        except requests.exceptions.Timeout:
            raise requests.RequestException(f"API 请求超时（超过 {self.timeout} 秒）")
        except requests.exceptions.RequestException as e:
            raise requests.RequestException(f"API 请求失败: {str(e)}")
        except (KeyError, IndexError) as e:
            raise ValueError(f"API 响应解析失败: {str(e)}")
    
    def recognize_with_markdown(self, image_path: str) -> str:
        """
        识别图片并转换为 Markdown 格式
        
        Args:
            image_path: 图片文件路径
            
        Returns:
            str: Markdown 格式的文本
        """
        result = self.recognize_image(
            image_path, 
            prompt="convert to markdown"
        )
        return result.full_text


# 全局 OCR 服务实例
ocr_service = OCRService()


if __name__ == '__main__':
    # 测试 OCR 服务
    import sys
    
    if len(sys.argv) > 1:
        test_image = sys.argv[1]
        print(f"正在识别图片: {test_image}")
        try:
            result = ocr_service.recognize_image(test_image)
            print(f"\n识别结果:\n{result.full_text}")
        except Exception as e:
            print(f"错误: {e}")
    else:
        print("用法: python -m src.ocr_service <图片路径>")

