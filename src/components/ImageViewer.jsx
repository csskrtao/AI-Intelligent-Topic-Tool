import React, { useState, useRef, useEffect } from 'react';
import { Card, Spin, Alert } from 'antd';
import BoundingBoxCanvas from './BoundingBoxCanvas';
import './ImageViewer.css';

const ImageViewer = ({ imageUrl, questions = [], selectedQuestionId, onQuestionHover }) => {
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(false);
  const [imageSize, setImageSize] = useState({
    naturalWidth: 0,
    naturalHeight: 0,
    displayWidth: 0,
    displayHeight: 0
  });
  const imageRef = useRef(null);

  const handleImageLoad = () => {
    console.log('图片加载成功:', imageUrl);
    setLoading(false);
    setError(false);

    // 使用 requestAnimationFrame 确保图片已经渲染到 DOM
    // 双重 RAF 确保浏览器完成布局和绘制
    requestAnimationFrame(() => {
      requestAnimationFrame(() => {
        if (imageRef.current) {
          const { naturalWidth, naturalHeight, offsetWidth, offsetHeight } = imageRef.current;

          // 如果 offsetWidth 仍然为 0，使用 naturalWidth 作为后备
          const displayWidth = offsetWidth || naturalWidth;
          const displayHeight = offsetHeight || naturalHeight;

          setImageSize({
            naturalWidth,
            naturalHeight,
            displayWidth,
            displayHeight
          });

          console.log('📐 图片尺寸信息:', {
            原始尺寸: `${naturalWidth} x ${naturalHeight}`,
            显示尺寸: `${displayWidth} x ${displayHeight}`,
            缩放比例: displayWidth ? `${(displayWidth / naturalWidth * 100).toFixed(1)}%` : 'N/A',
            是否使用后备尺寸: offsetWidth === 0
          });
        }
      });
    });
  };

  const handleImageError = (e) => {
    console.error('图片加载失败:', imageUrl, e);
    setLoading(false);
    setError(true);
  };

  // 监听图片尺寸变化，如果显示尺寸为 0 则重新获取
  useEffect(() => {
    if (!loading && !error && imageSize.displayWidth === 0 && imageRef.current) {
      console.log('⚠️ 检测到显示尺寸为 0，尝试重新获取...');

      const timer = setTimeout(() => {
        if (imageRef.current) {
          const { naturalWidth, naturalHeight, offsetWidth, offsetHeight } = imageRef.current;
          const displayWidth = offsetWidth || naturalWidth;
          const displayHeight = offsetHeight || naturalHeight;

          setImageSize({
            naturalWidth,
            naturalHeight,
            displayWidth,
            displayHeight
          });

          console.log('🔄 重新获取图片尺寸:', {
            原始尺寸: `${naturalWidth} x ${naturalHeight}`,
            显示尺寸: `${displayWidth} x ${displayHeight}`,
            是否使用后备尺寸: offsetWidth === 0
          });
        }
      }, 100);

      return () => clearTimeout(timer);
    }
  }, [loading, error, imageSize.displayWidth]);

  return (
    <Card
      title={`原图预览 ${questions.length > 0 ? `(${questions.filter(q => q.bounding_box).length} 个边界框)` : ''}`}
      className="image-viewer-card"
      bodyStyle={{
        height: 'calc(100% - 57px)',
        overflow: 'auto',
        padding: 16,
        background: '#fafafa'
      }}
    >
      <div className="image-container">
        {loading && (
          <div style={{ textAlign: 'center', padding: '50px 0' }}>
            <Spin tip="加载图片中..." />
          </div>
        )}
        {error && (
          <Alert
            message="图片加载失败"
            description={`无法加载图片: ${imageUrl}`}
            type="error"
            showIcon
          />
        )}
        <div className="image-wrapper" style={{ position: 'relative', display: 'inline-block' }}>
          <img
            ref={imageRef}
            src={imageUrl}
            alt="上传的图片"
            className="preview-image"
            onLoad={handleImageLoad}
            onError={handleImageError}
            style={{ display: loading || error ? 'none' : 'block' }}
          />
          {!loading && !error && imageSize.naturalWidth > 0 && (
            <BoundingBoxCanvas
              questions={questions}
              imageSize={imageSize}
              selectedQuestionId={selectedQuestionId}
              onQuestionHover={onQuestionHover}
            />
          )}
        </div>
      </div>
    </Card>
  );
};

export default ImageViewer;

