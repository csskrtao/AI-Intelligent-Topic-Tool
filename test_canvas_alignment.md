# Canvas 对齐问题修复验证

## 修复内容

### 问题原因
1. **图片缩放**：图片有 `max-width: 100%` CSS 样式，会被缩放显示
2. **Canvas 尺寸不匹配**：Canvas 的内部尺寸（width/height 属性）设置为原始图片尺寸，但 CSS 显示尺寸没有同步
3. **坐标系统不一致**：导致边界框位置偏移

### 修复方案

#### 1. ImageViewer.jsx
- 获取图片的原始尺寸（naturalWidth/naturalHeight）
- 获取图片的实际显示尺寸（offsetWidth/offsetHeight）
- 将两种尺寸都传递给 BoundingBoxCanvas

#### 2. BoundingBoxCanvas.jsx
- Canvas 的 `width/height` 属性设置为原始尺寸（用于绘制坐标系统）
- Canvas 的 CSS `width/height` 设置为显示尺寸（用于视觉对齐）
- 鼠标事件坐标转换：显示坐标 → 原始坐标

## 验证步骤

### 1. 启动服务
```bash
# 后端
python backend_api.py

# 前端
npm run dev
```

### 2. 打开浏览器
访问: http://localhost:5173

### 3. 上传测试图片
上传 `test.png` 或任何包含题目的图片

### 4. 检查控制台日志
应该看到以下日志：

```
📐 图片尺寸信息: {
  原始尺寸: "948 x 1024",
  显示尺寸: "500 x 540",  // 实际值取决于浏览器窗口大小
  缩放比例: "52.7%"
}

🎨 Canvas 绘制信息: {
  Canvas内部尺寸: "948 x 1024",
  Canvas显示尺寸: "500 x 540",
  题目数量: 4
}

📦 第一个边界框坐标: {
  x1: 36,
  y1: 25,
  x2: 912,
  y2: 185
}
```

### 5. 视觉验证
- ✅ 边界框应该精确框选题目区域
- ✅ 题号标签应该在边界框左上角
- ✅ 鼠标悬停边界框时，光标变为 pointer
- ✅ 悬停时边框加粗，显示半透明填充
- ✅ 题目列表对应项高亮

### 6. 交互验证
- ✅ 鼠标悬停边界框，右侧题目列表对应项高亮
- ✅ 鼠标移出边界框，高亮消失
- ✅ 不同题目使用不同颜色

## 技术细节

### Canvas 尺寸设置
```jsx
<canvas
  width={imageSize.naturalWidth}      // 内部绘制尺寸（原始图片尺寸）
  height={imageSize.naturalHeight}
  style={{
    width: `${imageSize.displayWidth}px`,   // CSS 显示尺寸
    height: `${imageSize.displayHeight}px`
  }}
/>
```

### 坐标转换
```javascript
// 鼠标显示坐标 → Canvas 内部坐标
const scaleX = imageSize.naturalWidth / imageSize.displayWidth;
const scaleY = imageSize.naturalHeight / imageSize.displayHeight;
const x = displayX * scaleX;
const y = displayY * scaleY;
```

### 工作原理
1. **Canvas 内部坐标系统**：使用原始图片尺寸（naturalWidth x naturalHeight）
2. **OCR 坐标系统**：也是基于原始图片尺寸
3. **Canvas 显示尺寸**：通过 CSS 设置为与图片显示尺寸一致
4. **浏览器自动缩放**：将 Canvas 内容从内部尺寸缩放到显示尺寸
5. **鼠标坐标转换**：将鼠标的显示坐标转换为内部坐标，用于碰撞检测

## 预期结果

✅ 边界框位置完全对齐  
✅ 无论浏览器窗口大小如何变化，边界框始终准确  
✅ 鼠标交互正常  
✅ 视觉效果清晰美观  

## 如果仍然不对齐

### 检查清单
1. 检查控制台日志，确认尺寸信息正确
2. 使用浏览器开发者工具检查 Canvas 元素的实际尺寸
3. 检查图片是否完全加载
4. 尝试刷新页面
5. 检查后端返回的边界框坐标是否正确

### 调试命令
```javascript
// 在浏览器控制台执行
const img = document.querySelector('.preview-image');
const canvas = document.querySelector('.bounding-box-canvas');

console.log('图片:', {
  naturalWidth: img.naturalWidth,
  naturalHeight: img.naturalHeight,
  offsetWidth: img.offsetWidth,
  offsetHeight: img.offsetHeight
});

console.log('Canvas:', {
  width: canvas.width,
  height: canvas.height,
  offsetWidth: canvas.offsetWidth,
  offsetHeight: canvas.offsetHeight
});
```

## 修复文件清单

- ✅ `src/components/ImageViewer.jsx` - 获取图片显示尺寸
- ✅ `src/components/BoundingBoxCanvas.jsx` - 设置 Canvas 显示尺寸，坐标转换
- ✅ 添加调试日志

## 测试完成标志

当您看到边界框精确框选题目区域时，修复成功！🎉

