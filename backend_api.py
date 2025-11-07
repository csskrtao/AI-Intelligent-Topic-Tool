"""
FastAPI 后端服务
提供 OCR、题目分割、导出等 RESTful API
"""

import os
import shutil
import traceback
from pathlib import Path
from typing import List, Optional
from fastapi import FastAPI, File, UploadFile, HTTPException, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse
from pydantic import BaseModel
import uvicorn

# 导入自定义模块
from src.config import config
from src.ocr_service import ocr_service
from src.question_splitter import question_splitter
from src.exporter import exporter
from src.utils import validate_image_file


# 创建 FastAPI 应用
app = FastAPI(
    title="AI 智能切题工具 API",
    description="自动识别、分割图片中的题目",
    version="1.0.0"
)

# 配置 CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 生产环境应该限制具体域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 临时文件目录
TEMP_DIR = Path("temp_uploads")
TEMP_DIR.mkdir(exist_ok=True)


# ============ 数据模型 ============

class QuestionResponse(BaseModel):
    """题目响应模型"""
    question_id: int
    text: str
    has_bounding_box: bool


class OCRResponse(BaseModel):
    """OCR 响应模型"""
    success: bool
    message: str
    questions: List[QuestionResponse]
    image_url: str


class ExportRequest(BaseModel):
    """导出请求模型"""
    question_ids: List[int]
    export_format: str = 'both'  # 'text', 'image', 'both'


# ============ API 端点 ============

@app.get("/")
async def root():
    """根路径"""
    return {
        "name": "AI 智能切题工具 API",
        "version": "1.0.0",
        "status": "running"
    }


@app.get("/health")
async def health_check():
    """健康检查"""
    is_valid, error_msg = config.validate()
    return {
        "status": "healthy" if is_valid else "unhealthy",
        "config_valid": is_valid,
        "error": error_msg
    }


@app.post("/api/upload", response_model=OCRResponse)
async def upload_and_process(file: UploadFile = File(...)):
    """
    上传图片并进行 OCR 识别和题目分割
    """
    try:
        # 验证文件类型
        if not file.filename:
            raise HTTPException(status_code=400, detail="文件名无效")
        
        file_ext = Path(file.filename).suffix.lower()
        if file_ext not in ['.jpg', '.jpeg', '.png', '.bmp']:
            raise HTTPException(
                status_code=400,
                detail=f"不支持的文件格式: {file_ext}"
            )
        
        # 保存上传的文件
        temp_file_path = TEMP_DIR / file.filename
        with open(temp_file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # 验证图片文件
        is_valid, error_msg = validate_image_file(str(temp_file_path))
        if not is_valid:
            temp_file_path.unlink()
            raise HTTPException(status_code=400, detail=error_msg)
        
        # 调用 OCR 服务
        ocr_result = ocr_service.recognize_image(str(temp_file_path))
        
        # 分割题目
        questions = question_splitter.split_text_by_lines(ocr_result.full_text)
        
        # 构造响应
        question_responses = [
            QuestionResponse(
                question_id=q.question_id,
                text=q.text,
                has_bounding_box=q.bounding_box is not None
            )
            for q in questions
        ]
        
        # 将题目和图片路径存储在全局变量中（简化版，生产环境应使用数据库）
        app.state.current_questions = questions
        app.state.current_image_path = str(temp_file_path)

        # 构造图片 URL
        image_url = f"/api/image/{temp_file_path.name}"

        return OCRResponse(
            success=True,
            message=f"成功识别并分割出 {len(questions)} 道题目",
            questions=question_responses,
            image_url=image_url
        )
    
    except Exception as e:
        error_detail = f"处理失败: {str(e)}"
        print(f"\n❌ 错误详情:\n{traceback.format_exc()}")
        raise HTTPException(status_code=500, detail=error_detail)


@app.post("/api/export")
async def export_questions(request: ExportRequest):
    """
    导出选中的题目
    """
    try:
        # 获取当前的题目列表和图片路径
        if not hasattr(app.state, 'current_questions'):
            raise HTTPException(status_code=400, detail="没有可导出的题目，请先上传图片")
        
        questions = app.state.current_questions
        image_path = app.state.current_image_path
        
        # 筛选要导出的题目
        selected_questions = [
            q for q in questions if q.question_id in request.question_ids
        ]
        
        if not selected_questions:
            raise HTTPException(status_code=400, detail="未找到指定的题目")
        
        # 批量导出
        results = exporter.export_questions_batch(
            selected_questions,
            image_path,
            export_format=request.export_format
        )
        
        return {
            "success": True,
            "message": f"成功导出 {len(selected_questions)} 道题目",
            "results": results,
            "export_dir": exporter.get_export_dir()
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"导出失败: {str(e)}")


@app.get("/api/image/{filename}")
async def get_image(filename: str):
    """获取上传的图片"""
    file_path = TEMP_DIR / filename
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="图片不存在")
    return FileResponse(file_path)


# ============ 启动服务 ============

if __name__ == "__main__":
    print("🚀 启动 AI 智能切题工具后端服务...")
    print(f"📁 导出目录: {config.export_dir}")
    print(f"🔑 API Key: {'已配置' if config.api_key else '未配置'}")
    
    uvicorn.run(
        app,
        host="127.0.0.1",
        port=8000,
        log_level="info"
    )

