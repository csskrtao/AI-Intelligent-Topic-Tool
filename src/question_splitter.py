"""
题目分割算法模块
实现基于正则表达式的题目自动分割
"""

import re
from typing import List, Tuple, Optional
from .models import Question, TextBlock, BoundingBox, OCRResult


class QuestionSplitter:
    """题目分割器"""
    
    # 题号匹配的正则表达式模式
    QUESTION_NUMBER_PATTERNS = [
        r'^\s*(\d+)[\.、．]\s*',  # 匹配: 1. 2、 3．
        r'^\s*\((\d+)\)\s*',      # 匹配: (1) (2)
        r'^\s*（(\d+)）\s*',      # 匹配: （1） （2）
        r'^\s*\[(\d+)\]\s*',      # 匹配: [1] [2]
        r'^\s*【(\d+)】\s*',      # 匹配: 【1】 【2】
        r'^\s*([一二三四五六七八九十]+)[\.、．]\s*',  # 匹配: 一、 二、
    ]
    
    def __init__(self, patterns: Optional[List[str]] = None):
        """
        初始化题目分割器
        
        Args:
            patterns: 自定义的题号匹配模式列表，如果为 None 则使用默认模式
        """
        self.patterns = patterns or self.QUESTION_NUMBER_PATTERNS
        self.compiled_patterns = [re.compile(p) for p in self.patterns]
    
    def is_question_start(self, text: str) -> Tuple[bool, Optional[str]]:
        """
        判断文本是否是题目的开始（包含题号）
        
        Args:
            text: 要检查的文本
            
        Returns:
            Tuple[bool, Optional[str]]: (是否是题目开始, 题号)
        """
        for pattern in self.compiled_patterns:
            match = pattern.match(text.strip())
            if match:
                question_number = match.group(1)
                return True, question_number
        return False, None
    
    def split_text_by_lines(self, text: str) -> List[Question]:
        """
        按行分割文本为题目列表（简单版本，用于纯文本）
        
        Args:
            text: 完整文本
            
        Returns:
            List[Question]: 题目列表
        """
        lines = text.split('\n')
        questions = []
        current_question_id = 0
        current_question = None
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            is_start, question_num = self.is_question_start(line)
            
            if is_start:
                # 保存上一道题
                if current_question is not None:
                    questions.append(current_question)
                
                # 开始新题
                current_question_id += 1
                current_question = Question(question_id=current_question_id)
                
                # 添加当前行作为文本块（使用占位坐标）
                current_question.add_text_block(
                    TextBlock(text=line, box=BoundingBox(0, 0, 0, 0))
                )
            else:
                # 如果还没有开始任何题目，创建第一道题
                if current_question is None:
                    current_question_id += 1
                    current_question = Question(question_id=current_question_id)
                
                # 添加到当前题目
                current_question.add_text_block(
                    TextBlock(text=line, box=BoundingBox(0, 0, 0, 0))
                )
        
        # 保存最后一道题
        if current_question is not None:
            questions.append(current_question)
        
        return questions
    
    def split_ocr_result(self, ocr_result: OCRResult) -> List[Question]:
        """
        分割 OCR 识别结果为题目列表
        
        Args:
            ocr_result: OCR 识别结果
            
        Returns:
            List[Question]: 题目列表
        """
        # 对文本块进行排序（按 y 坐标，然后按 x 坐标）
        sorted_blocks = self._sort_text_blocks(ocr_result.text_blocks)
        
        questions = []
        current_question_id = 0
        current_question = None
        
        for block in sorted_blocks:
            is_start, question_num = self.is_question_start(block.text)
            
            if is_start:
                # 保存上一道题
                if current_question is not None:
                    questions.append(current_question)
                
                # 开始新题
                current_question_id += 1
                current_question = Question(question_id=current_question_id)
                current_question.add_text_block(block)
            else:
                # 如果还没有开始任何题目，创建第一道题
                if current_question is None:
                    current_question_id += 1
                    current_question = Question(question_id=current_question_id)
                
                # 添加到当前题目
                current_question.add_text_block(block)
        
        # 保存最后一道题
        if current_question is not None:
            questions.append(current_question)
        
        return questions
    
    def _sort_text_blocks(self, blocks: List[TextBlock]) -> List[TextBlock]:
        """
        对文本块进行排序，模拟人类阅读顺序
        
        Args:
            blocks: 文本块列表
            
        Returns:
            List[TextBlock]: 排序后的文本块列表
        """
        # 按 y 坐标升序，y 相近时按 x 坐标升序
        # y 坐标差异小于 10 像素认为是同一行
        return sorted(
            blocks,
            key=lambda b: (round(b.box.y1 / 10) * 10, b.box.x1)
        )
    
    def merge_questions(self, questions: List[Question], indices: List[int]) -> Question:
        """
        合并多道题目
        
        Args:
            questions: 题目列表
            indices: 要合并的题目索引列表
            
        Returns:
            Question: 合并后的题目
        """
        if not indices:
            raise ValueError("索引列表不能为空")
        
        # 使用第一道题的 ID
        merged = Question(question_id=questions[indices[0]].question_id)
        
        # 合并所有文本块
        for idx in sorted(indices):
            if 0 <= idx < len(questions):
                merged.merge_with(questions[idx])
        
        return merged


# 全局题目分割器实例
question_splitter = QuestionSplitter()


if __name__ == '__main__':
    # 测试题目分割功能
    test_text = """
1. 这是第一道题目
这是第一道题的内容
2. 这是第二道题目
3、这是第三道题目
（4）这是第四道题目
一、这是第五道题目
    """
    
    splitter = QuestionSplitter()
    questions = splitter.split_text_by_lines(test_text)
    
    print(f"分割出 {len(questions)} 道题目:")
    for q in questions:
        print(f"\n题目 {q.question_id}:")
        print(q.text)

