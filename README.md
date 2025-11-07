# AI 智能切题工具

> 自动识别、分割图片中的题目，并支持导出为文本或图片

## 📖 项目简介

AI 智能切题工具是一款桌面应用程序，旨在帮助用户快速、智能地处理包含多道题目的文件（如试卷、练习册的图片）。软件能够自动识别、分割文件中的每一道题目，并允许用户将单道题目以文本或图片的形式独立保存。

### 核心功能

- ✅ **图片上传**：支持 `.jpg`, `.png`, `.bmp` 格式
- ✅ **OCR 识别**：集成 DeepSeek OCR API，高精度文字识别
- ✅ **智能分割**：基于正则表达式自动识别题号并分割题目
- ✅ **预览编辑**：双栏界面，支持题目合并、拆分
- ✅ **批量导出**：导出为文本文件或图片文件

## 🏗️ 技术架构

### 后端（Python）
- **FastAPI**：RESTful API 服务
- **Pillow**：图像处理
- **Requests**：API 调用
- **Python-dotenv**：环境变量管理

### 前端（Electron + React）
- **Electron**：跨平台桌面应用框架
- **React**：现代化 UI 框架
- **Vite**：快速开发构建工具
- **Ant Design / Material-UI**：UI 组件库（待集成）

## 📦 安装指南

### 前置要求

- Python 3.8+
- Node.js 16+
- npm 或 yarn

### 1. 克隆项目

```bash
git clone <repository-url>
cd cut_ai
```

### 2. 配置环境变量

复制 `.env.example` 为 `.env` 并填入配置：

```bash
cp .env.example .env
```

编辑 `.env` 文件，填入您的 API Key：

```env
MODELVERSE_API_KEY=your_api_key_here
```

> 获取 API Key：访问 [https://www.compshare.cn/](https://www.compshare.cn/)

### 3. 安装 Python 依赖

```bash
pip install -r requirements.txt
```

### 4. 安装 Node.js 依赖

```bash
npm install
```

## 🚀 运行项目

### 开发模式

#### 1. 启动 Python 后端

```bash
python backend_api.py
```

后端将运行在 `http://localhost:8000`

#### 2. 启动 React 前端（开发服务器）

```bash
npm run dev
```

前端将运行在 `http://localhost:5173`

#### 3. 启动 Electron

```bash
npm run electron:dev
```

### 生产模式

```bash
# 构建前端
npm run build

# 打包 Electron 应用
npm run electron:build
```

## 📁 项目结构

```
cut_ai/
├── backend_api.py          # FastAPI 后端服务
├── src/                    # Python 核心模块
│   ├── config.py          # 配置管理
│   ├── models.py          # 数据模型
│   ├── utils.py           # 工具函数
│   ├── ocr_service.py     # OCR API 调用
│   ├── image_processor.py # 图像处理
│   ├── question_splitter.py # 题目分割算法
│   └── exporter.py        # 导出功能
├── electron/              # Electron 主进程
│   ├── main.js           # 主进程入口
│   └── preload.js        # 预加载脚本
├── frontend/             # React 前端（待创建）
│   ├── src/
│   ├── public/
│   └── vite.config.js
├── exports/              # 导出文件目录
├── .env.example          # 环境变量示例
├── requirements.txt      # Python 依赖
├── package.json          # Node.js 依赖
└── README.md            # 项目文档
```

## 🔧 API 文档

### 后端 API 端点

- `GET /` - 根路径
- `GET /health` - 健康检查
- `POST /api/upload` - 上传图片并进行 OCR 识别
- `POST /api/export` - 导出选中的题目
- `GET /api/image/{filename}` - 获取上传的图片

详细 API 文档：启动后端后访问 `http://localhost:8000/docs`

## 📝 使用说明

1. **上传图片**：点击上传按钮或拖拽图片到应用窗口
2. **查看识别结果**：左侧显示原图，右侧显示自动分割的题目列表
3. **编辑题目**：
   - 选中多道题目点击"合并"按钮进行合并
   - 选中一道题目点击"拆分"按钮进行拆分
4. **导出题目**：选中题目后选择导出格式（文本/图片/两者）

## 🛠️ 开发计划

### P0: 核心功能（已完成）
- [x] 文件上传
- [x] OCR 处理
- [x] 题目自动分割
- [x] 导出功能（文本/图片）
- [x] FastAPI 后端
- [x] Electron 框架搭建

### P1: 重要功能（进行中）
- [ ] React 前端界面
- [ ] 预览与手动校准
- [ ] PDF 文件支持
- [ ] 批量处理

### P2: 扩展功能（规划中）
- [ ] 本地题库管理
- [ ] 高级导出选项
- [ ] 公式识别集成

## 📄 许可证

ISC

## 👥 贡献

欢迎提交 Issue 和 Pull Request！

## 📧 联系方式

如有问题，请联系项目维护者。

