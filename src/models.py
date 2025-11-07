"""
数据模型模块
定义应用程序中使用的数据结构
"""

from dataclasses import dataclass, field
from typing import List, Tuple, Optional


@dataclass
class BoundingBox:
    """文本块的边界框坐标"""
    x1: float  # 左上角 x 坐标
    y1: float  # 左上角 y 坐标
    x2: float  # 右下角 x 坐标
    y2: float  # 右下角 y 坐标
    
    @property
    def width(self) -> float:
        """获取宽度"""
        return self.x2 - self.x1
    
    @property
    def height(self) -> float:
        """获取高度"""
        return self.y2 - self.y1
    
    @property
    def center_x(self) -> float:
        """获取中心点 x 坐标"""
        return (self.x1 + self.x2) / 2
    
    @property
    def center_y(self) -> float:
        """获取中心点 y 坐标"""
        return (self.y1 + self.y2) / 2
    
    def to_tuple(self) -> Tuple[float, float, float, float]:
        """转换为元组格式 (x1, y1, x2, y2)"""
        return (self.x1, self.y1, self.x2, self.y2)
    
    @classmethod
    def from_list(cls, coords: List[float]) -> 'BoundingBox':
        """
        从坐标列表创建 BoundingBox
        
        Args:
            coords: 坐标列表，格式为 [x1, y1, x2, y2] 或 [[x1, y1], [x2, y2]]
        """
        if len(coords) == 4:
            return cls(coords[0], coords[1], coords[2], coords[3])
        elif len(coords) == 2 and len(coords[0]) == 2:
            return cls(coords[0][0], coords[0][1], coords[1][0], coords[1][1])
        else:
            raise ValueError(f"无效的坐标格式: {coords}")


@dataclass
class TextBlock:
    """OCR 识别的文本块"""
    text: str  # 文本内容
    box: BoundingBox  # 边界框
    confidence: Optional[float] = None  # 置信度（可选）
    
    def __repr__(self) -> str:
        return f"TextBlock(text='{self.text[:20]}...', box={self.box.to_tuple()})"


@dataclass
class Question:
    """题目数据模型"""
    question_id: int  # 题目编号
    text_blocks: List[TextBlock] = field(default_factory=list)  # 包含的文本块列表
    
    @property
    def text(self) -> str:
        """获取题目的完整文本"""
        return '\n'.join(block.text for block in self.text_blocks)
    
    @property
    def bounding_box(self) -> Optional[BoundingBox]:
        """
        计算包含所有文本块的最小边界框
        
        Returns:
            BoundingBox: 最小包围盒，如果没有文本块则返回 None
        """
        if not self.text_blocks:
            return None
        
        min_x = min(block.box.x1 for block in self.text_blocks)
        min_y = min(block.box.y1 for block in self.text_blocks)
        max_x = max(block.box.x2 for block in self.text_blocks)
        max_y = max(block.box.y2 for block in self.text_blocks)
        
        return BoundingBox(min_x, min_y, max_x, max_y)
    
    def add_text_block(self, block: TextBlock):
        """添加文本块"""
        self.text_blocks.append(block)
    
    def merge_with(self, other: 'Question'):
        """
        合并另一个题目
        
        Args:
            other: 要合并的题目
        """
        self.text_blocks.extend(other.text_blocks)
    
    def __repr__(self) -> str:
        preview = self.text[:50].replace('\n', ' ') if self.text else ''
        return f"Question(id={self.question_id}, text='{preview}...', blocks={len(self.text_blocks)})"


@dataclass
class OCRResult:
    """OCR 识别结果"""
    image_path: str  # 原始图片路径
    text_blocks: List[TextBlock] = field(default_factory=list)  # 所有识别的文本块
    raw_response: Optional[dict] = None  # 原始 API 响应（用于调试）
    
    def add_text_block(self, text: str, box: BoundingBox, confidence: Optional[float] = None):
        """添加文本块"""
        self.text_blocks.append(TextBlock(text, box, confidence))
    
    @property
    def full_text(self) -> str:
        """获取完整文本"""
        return '\n'.join(block.text for block in self.text_blocks)
    
    def __repr__(self) -> str:
        return f"OCRResult(image={self.image_path}, blocks={len(self.text_blocks)})"

