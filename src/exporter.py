"""
导出功能模块
实现题目导出为文本和图片
"""

from pathlib import Path
from typing import List, Optional
from datetime import datetime

from .models import Question
from .image_processor import image_processor
from .utils import get_safe_filename
from .config import config


class Exporter:
    """题目导出器"""
    
    def __init__(self, export_dir: Optional[Path] = None):
        """
        初始化导出器
        
        Args:
            export_dir: 导出目录，如果为 None 则使用配置中的目录
        """
        self.export_dir = export_dir or config.export_dir
        self.export_dir.mkdir(parents=True, exist_ok=True)
    
    def export_question_as_text(
        self,
        question: Question,
        filename: Optional[str] = None,
        include_question_id: bool = True
    ) -> str:
        """
        导出题目为文本文件
        
        Args:
            question: 题目对象
            filename: 文件名，如果为 None 则自动生成
            include_question_id: 是否在文件名中包含题目 ID
            
        Returns:
            str: 导出文件的完整路径
        """
        # 生成文件名
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            if include_question_id:
                filename = f"question_{question.question_id}_{timestamp}.txt"
            else:
                filename = f"question_{timestamp}.txt"
        
        # 确保文件名安全
        safe_filename = get_safe_filename(filename)
        output_path = self.export_dir / safe_filename
        
        # 写入文件
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(question.text)
        
        return str(output_path)
    
    def export_question_as_image(
        self,
        question: Question,
        original_image_path: str,
        filename: Optional[str] = None,
        include_question_id: bool = True,
        padding: int = 10
    ) -> Optional[str]:
        """
        导出题目为图片文件
        
        Args:
            question: 题目对象
            original_image_path: 原始图片路径
            filename: 文件名，如果为 None 则自动生成
            include_question_id: 是否在文件名中包含题目 ID
            padding: 裁剪时的边距（像素）
            
        Returns:
            Optional[str]: 导出文件的完整路径，如果题目没有边界框则返回 None
        """
        # 检查题目是否有边界框
        if question.bounding_box is None:
            return None
        
        # 生成文件名
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            if include_question_id:
                filename = f"question_{question.question_id}_{timestamp}.png"
            else:
                filename = f"question_{timestamp}.png"
        
        # 确保文件名安全且为 .png 格式
        safe_filename = get_safe_filename(filename)
        if not safe_filename.lower().endswith('.png'):
            safe_filename = Path(safe_filename).stem + '.png'
        
        output_path = self.export_dir / safe_filename
        
        # 裁剪并保存图片
        image_processor.crop_question_image(
            original_image_path,
            question,
            str(output_path),
            padding
        )
        
        return str(output_path)
    
    def export_questions_batch(
        self,
        questions: List[Question],
        original_image_path: str,
        export_format: str = 'both',
        prefix: str = ''
    ) -> dict:
        """
        批量导出题目
        
        Args:
            questions: 题目列表
            original_image_path: 原始图片路径
            export_format: 导出格式，可选 'text', 'image', 'both'
            prefix: 文件名前缀
            
        Returns:
            dict: 导出结果，格式为 {question_id: {'text': path, 'image': path}}
        """
        results = {}
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        for question in questions:
            result = {}
            
            # 导出文本
            if export_format in ['text', 'both']:
                text_filename = f"{prefix}question_{question.question_id}_{timestamp}.txt"
                text_path = self.export_question_as_text(
                    question,
                    filename=text_filename,
                    include_question_id=False
                )
                result['text'] = text_path
            
            # 导出图片
            if export_format in ['image', 'both']:
                image_filename = f"{prefix}question_{question.question_id}_{timestamp}.png"
                image_path = self.export_question_as_image(
                    question,
                    original_image_path,
                    filename=image_filename,
                    include_question_id=False
                )
                if image_path:
                    result['image'] = image_path
            
            results[question.question_id] = result
        
        return results
    
    def get_export_dir(self) -> str:
        """获取导出目录路径"""
        return str(self.export_dir)
    
    def set_export_dir(self, export_dir: str):
        """
        设置导出目录
        
        Args:
            export_dir: 新的导出目录路径
        """
        self.export_dir = Path(export_dir)
        self.export_dir.mkdir(parents=True, exist_ok=True)


# 全局导出器实例
exporter = Exporter()


if __name__ == '__main__':
    # 测试导出功能
    from .models import TextBlock, BoundingBox
    
    # 创建测试题目
    test_question = Question(question_id=1)
    test_question.add_text_block(
        TextBlock(text="1. 这是一道测试题目", box=BoundingBox(10, 10, 200, 50))
    )
    test_question.add_text_block(
        TextBlock(text="这是题目的内容部分", box=BoundingBox(10, 60, 200, 100))
    )
    
    # 测试导出文本
    text_path = exporter.export_question_as_text(test_question)
    print(f"文本导出成功: {text_path}")
    
    print(f"导出目录: {exporter.get_export_dir()}")

