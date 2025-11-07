"""
图像处理模块
提供图片裁剪、坐标计算等功能
"""

from pathlib import Path
from typing import List, Tuple, Optional
from PIL import Image

from .models import BoundingBox, Question


class ImageProcessor:
    """图像处理类"""
    
    @staticmethod
    def crop_image_by_box(
        image_path: str, 
        box: BoundingBox, 
        output_path: str,
        padding: int = 10
    ) -> str:
        """
        根据边界框裁剪图片
        
        Args:
            image_path: 原始图片路径
            box: 边界框坐标
            output_path: 输出图片路径
            padding: 边距（像素），默认 10
            
        Returns:
            str: 输出图片路径
            
        Raises:
            FileNotFoundError: 图片文件不存在
            ValueError: 坐标无效
        """
        if not Path(image_path).exists():
            raise FileNotFoundError(f"图片文件不存在: {image_path}")
        
        # 打开图片
        with Image.open(image_path) as img:
            width, height = img.size
            
            # 添加边距并确保坐标在图片范围内
            x1 = max(0, int(box.x1) - padding)
            y1 = max(0, int(box.y1) - padding)
            x2 = min(width, int(box.x2) + padding)
            y2 = min(height, int(box.y2) + padding)
            
            # 验证坐标
            if x1 >= x2 or y1 >= y2:
                raise ValueError(f"无效的裁剪坐标: ({x1}, {y1}, {x2}, {y2})")
            
            # 裁剪图片
            cropped = img.crop((x1, y1, x2, y2))
            
            # 确保输出目录存在
            Path(output_path).parent.mkdir(parents=True, exist_ok=True)
            
            # 保存裁剪后的图片
            cropped.save(output_path)
        
        return output_path
    
    @staticmethod
    def crop_question_image(
        image_path: str,
        question: Question,
        output_path: str,
        padding: int = 10
    ) -> Optional[str]:
        """
        裁剪题目对应的图片区域
        
        Args:
            image_path: 原始图片路径
            question: 题目对象
            output_path: 输出图片路径
            padding: 边距（像素）
            
        Returns:
            Optional[str]: 输出图片路径，如果题目没有边界框则返回 None
        """
        box = question.bounding_box
        if box is None:
            return None
        
        return ImageProcessor.crop_image_by_box(
            image_path, 
            box, 
            output_path, 
            padding
        )
    
    @staticmethod
    def calculate_bounding_box(boxes: List[BoundingBox]) -> Optional[BoundingBox]:
        """
        计算多个边界框的最小包围盒
        
        Args:
            boxes: 边界框列表
            
        Returns:
            Optional[BoundingBox]: 最小包围盒，如果列表为空则返回 None
        """
        if not boxes:
            return None
        
        min_x = min(box.x1 for box in boxes)
        min_y = min(box.y1 for box in boxes)
        max_x = max(box.x2 for box in boxes)
        max_y = max(box.y2 for box in boxes)
        
        return BoundingBox(min_x, min_y, max_x, max_y)
    
    @staticmethod
    def get_image_size(image_path: str) -> Tuple[int, int]:
        """
        获取图片尺寸
        
        Args:
            image_path: 图片路径
            
        Returns:
            Tuple[int, int]: (宽度, 高度)
        """
        with Image.open(image_path) as img:
            return img.size
    
    @staticmethod
    def resize_image(
        image_path: str,
        output_path: str,
        max_width: Optional[int] = None,
        max_height: Optional[int] = None,
        quality: int = 95
    ) -> str:
        """
        调整图片大小（保持宽高比）
        
        Args:
            image_path: 原始图片路径
            output_path: 输出图片路径
            max_width: 最大宽度
            max_height: 最大高度
            quality: 输出质量（1-100）
            
        Returns:
            str: 输出图片路径
        """
        with Image.open(image_path) as img:
            width, height = img.size
            
            # 计算缩放比例
            scale = 1.0
            if max_width and width > max_width:
                scale = min(scale, max_width / width)
            if max_height and height > max_height:
                scale = min(scale, max_height / height)
            
            # 如果需要缩放
            if scale < 1.0:
                new_width = int(width * scale)
                new_height = int(height * scale)
                resized = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
            else:
                resized = img
            
            # 确保输出目录存在
            Path(output_path).parent.mkdir(parents=True, exist_ok=True)
            
            # 保存图片
            resized.save(output_path, quality=quality)
        
        return output_path


# 全局图像处理器实例
image_processor = ImageProcessor()


if __name__ == '__main__':
    # 测试图像处理功能
    print("图像处理模块测试")
    
    # 测试边界框计算
    boxes = [
        BoundingBox(10, 20, 100, 80),
        BoundingBox(50, 60, 150, 120),
        BoundingBox(30, 40, 120, 100)
    ]
    result_box = ImageProcessor.calculate_bounding_box(boxes)
    print(f"最小包围盒: {result_box.to_tuple()}")

