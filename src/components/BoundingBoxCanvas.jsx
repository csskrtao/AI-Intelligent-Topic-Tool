import React, { useRef, useEffect, useState, useCallback } from 'react';
import './BoundingBoxCanvas.css';

const BoundingBoxCanvas = ({ questions, imageSize, selectedQuestionId, onQuestionHover }) => {
  const canvasRef = useRef(null);
  const [hoveredQuestionId, setHoveredQuestionId] = useState(null);

  // 预定义的颜色数组，用于区分不同题目
  const colors = [
    '#1890ff', // 蓝色
    '#52c41a', // 绿色
    '#faad14', // 橙色
    '#f5222d', // 红色
    '#722ed1', // 紫色
    '#13c2c2', // 青色
    '#eb2f96', // 粉色
    '#fa8c16', // 橙红色
  ];

  // 获取题目对应的颜色
  const getColor = (questionId) => {
    return colors[(questionId - 1) % colors.length];
  };

  // 绘制所有边界框
  const drawBoundingBoxes = useCallback(() => {
    const canvas = canvasRef.current;
    if (!canvas || !imageSize.naturalWidth || !imageSize.naturalHeight) return;

    const ctx = canvas.getContext('2d');

    // 清空画布
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    console.log('🎨 Canvas 绘制信息:', {
      Canvas内部尺寸: `${canvas.width} x ${canvas.height}`,
      Canvas显示尺寸: `${canvas.offsetWidth} x ${canvas.offsetHeight}`,
      题目数量: questions.filter(q => q.bounding_box).length
    });

    // 过滤出有边界框的题目
    const questionsWithBox = questions.filter(q => q.bounding_box);

    questionsWithBox.forEach((question, index) => {
      const { question_id, bounding_box } = question;
      const color = getColor(question_id);

      // 调试：打印第一个边界框的坐标
      if (index === 0) {
        console.log('📦 第一个边界框坐标:', bounding_box);
      }

      // 判断是否被悬停或选中
      const isHovered = hoveredQuestionId === question_id;
      const isSelected = selectedQuestionId === question_id;
      const isHighlighted = isHovered || isSelected;

      // 绘制边界框
      ctx.strokeStyle = color;
      ctx.lineWidth = isHighlighted ? 4 : 2;
      ctx.strokeRect(
        bounding_box.x1,
        bounding_box.y1,
        bounding_box.x2 - bounding_box.x1,
        bounding_box.y2 - bounding_box.y1
      );

      // 绘制半透明填充（仅在高亮时）
      if (isHighlighted) {
        ctx.fillStyle = color + '20'; // 添加透明度
        ctx.fillRect(
          bounding_box.x1,
          bounding_box.y1,
          bounding_box.x2 - bounding_box.x1,
          bounding_box.y2 - bounding_box.y1
        );
      }

      // 绘制题号标签
      const labelText = `题目 ${question_id}`;
      const fontSize = isHighlighted ? 16 : 14;
      ctx.font = `bold ${fontSize}px Arial, sans-serif`;

      // 测量文本宽度
      const textMetrics = ctx.measureText(labelText);
      const textWidth = textMetrics.width;
      const padding = 6;
      const labelHeight = fontSize + padding * 2;

      // 绘制标签背景
      ctx.fillStyle = color;
      ctx.fillRect(
        bounding_box.x1,
        bounding_box.y1 - labelHeight,
        textWidth + padding * 2,
        labelHeight
      );

      // 绘制标签文字
      ctx.fillStyle = '#ffffff';
      ctx.textBaseline = 'top';
      ctx.fillText(
        labelText,
        bounding_box.x1 + padding,
        bounding_box.y1 - labelHeight + padding
      );
    });
  }, [questions, imageSize, hoveredQuestionId, selectedQuestionId]);

  // 处理鼠标移动事件
  const handleMouseMove = (e) => {
    const canvas = canvasRef.current;
    if (!canvas) return;

    const rect = canvas.getBoundingClientRect();
    // 鼠标在 Canvas 显示区域的坐标
    const displayX = e.clientX - rect.left;
    const displayY = e.clientY - rect.top;

    // 转换为 Canvas 内部坐标系统（原始图片坐标系统）
    const scaleX = imageSize.naturalWidth / imageSize.displayWidth;
    const scaleY = imageSize.naturalHeight / imageSize.displayHeight;
    const x = displayX * scaleX;
    const y = displayY * scaleY;

    // 检查鼠标是否在某个边界框内
    let foundQuestionId = null;
    const questionsWithBox = questions.filter(q => q.bounding_box);

    for (const question of questionsWithBox) {
      const { question_id, bounding_box } = question;
      if (
        x >= bounding_box.x1 &&
        x <= bounding_box.x2 &&
        y >= bounding_box.y1 &&
        y <= bounding_box.y2
      ) {
        foundQuestionId = question_id;
        break;
      }
    }

    if (foundQuestionId !== hoveredQuestionId) {
      setHoveredQuestionId(foundQuestionId);
      if (onQuestionHover) {
        onQuestionHover(foundQuestionId);
      }
    }

    // 更改鼠标样式
    canvas.style.cursor = foundQuestionId ? 'pointer' : 'default';
  };

  // 处理鼠标离开事件
  const handleMouseLeave = () => {
    setHoveredQuestionId(null);
    if (onQuestionHover) {
      onQuestionHover(null);
    }
  };

  // 当 questions、imageSize 或 hoveredQuestionId 变化时重新绘制
  useEffect(() => {
    drawBoundingBoxes();
  }, [drawBoundingBoxes]);

  return (
    <canvas
      ref={canvasRef}
      className="bounding-box-canvas"
      width={imageSize.naturalWidth}
      height={imageSize.naturalHeight}
      style={{
        width: `${imageSize.displayWidth}px`,
        height: `${imageSize.displayHeight}px`
      }}
      onMouseMove={handleMouseMove}
      onMouseLeave={handleMouseLeave}
    />
  );
};

export default BoundingBoxCanvas;

