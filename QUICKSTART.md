# 快速启动指南

## 🚀 5 分钟快速开始

### 步骤 1: 配置 API Key

1. 复制环境变量文件：
```bash
cp .env.example .env
```

2. 编辑 `.env` 文件，填入您的 API Key：
```env
MODELVERSE_API_KEY=your_api_key_here
```

> 💡 获取 API Key: 访问 [https://www.compshare.cn/](https://www.compshare.cn/)

### 步骤 2: 安装 Python 依赖

```bash
pip install -r requirements.txt
```

### 步骤 3: 测试后端服务

```bash
python backend_api.py
```

访问 http://localhost:8000 查看 API 状态

访问 http://localhost:8000/docs 查看 API 文档

### 步骤 4: 测试 OCR 功能（可选）

```bash
python -m src.ocr_service <图片路径>
```

示例：
```bash
python -m src.ocr_service test_image.jpg
```

## 📦 当前可用功能

### 1. 后端 API 测试

使用 curl 或 Postman 测试 API：

#### 上传图片并识别
```bash
curl -X POST "http://localhost:8000/api/upload" \
  -F "file=@test_image.jpg"
```

#### 导出题目
```bash
curl -X POST "http://localhost:8000/api/export" \
  -H "Content-Type: application/json" \
  -d '{
    "question_ids": [1, 2],
    "export_format": "both"
  }'
```

### 2. Python 模块测试

#### 测试配置
```bash
python -m src.config
```

#### 测试题目分割
```bash
python -m src.question_splitter
```

#### 测试导出功能
```bash
python -m src.exporter
```

## 🔧 故障排除

### 问题 1: API Key 未配置
**错误**: `配置无效: 未配置 MODELVERSE_API_KEY`

**解决**: 确保 `.env` 文件存在且包含有效的 API Key

### 问题 2: 模块导入错误
**错误**: `ModuleNotFoundError: No module named 'xxx'`

**解决**: 
```bash
pip install -r requirements.txt
```

### 问题 3: 图片格式不支持
**错误**: `不支持的文件格式`

**解决**: 确保图片格式为 `.jpg`, `.png`, 或 `.bmp`

### 问题 4: API 请求超时
**错误**: `API 请求超时`

**解决**: 
1. 检查网络连接
2. 增加 `.env` 中的 `OCR_TIMEOUT` 值
3. 确认 API Key 有效

## 📁 导出文件位置

默认导出目录: `./exports/`

可在 `.env` 文件中修改：
```env
EXPORT_DIR=your_custom_path
```

## 🎯 下一步

1. **等待前端完成**: React 界面正在开发中
2. **手动测试 API**: 使用 Postman 或 curl 测试所有端点
3. **准备测试图片**: 准备一些包含题目的图片进行测试

## 💡 提示

- 首次使用建议先用小图片测试
- 查看 `backend_api.py` 的日志输出了解处理过程
- 导出的文件会自动添加时间戳避免覆盖
- 支持的题号格式见 `src/question_splitter.py`

## 📞 需要帮助？

查看完整文档: [README.md](README.md)

查看项目实现总结: [issues/项目实现总结.md](issues/项目实现总结.md)

