import React, { useState } from 'react';
import { Card, Spin, Alert } from 'antd';
import './ImageViewer.css';

const ImageViewer = ({ imageUrl }) => {
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(false);

  const handleImageLoad = () => {
    console.log('图片加载成功:', imageUrl);
    setLoading(false);
    setError(false);
  };

  const handleImageError = (e) => {
    console.error('图片加载失败:', imageUrl, e);
    setLoading(false);
    setError(true);
  };

  return (
    <Card
      title="原图预览"
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
        <img
          src={imageUrl}
          alt="上传的图片"
          className="preview-image"
          onLoad={handleImageLoad}
          onError={handleImageError}
          style={{ display: loading || error ? 'none' : 'block' }}
        />
      </div>
    </Card>
  );
};

export default ImageViewer;

