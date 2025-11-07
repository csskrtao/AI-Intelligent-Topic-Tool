import React, { useState } from 'react';
import { Upload, Button, Space, Typography, Spin } from 'antd';
import { InboxOutlined, UploadOutlined } from '@ant-design/icons';
import { uploadImage } from '../services/api';
import './UploadPanel.css';

const { Dragger } = Upload;
const { Title, Text } = Typography;

const UploadPanel = ({ onSuccess, onError, loading, setLoading }) => {
  const [fileList, setFileList] = useState([]);

  const handleUpload = async (file) => {
    setLoading(true);
    try {
      const data = await uploadImage(file);
      onSuccess(data);
      setFileList([]);
    } catch (error) {
      onError(error);
    } finally {
      setLoading(false);
    }
    return false; // 阻止自动上传
  };

  const uploadProps = {
    name: 'file',
    multiple: false,
    fileList,
    accept: '.jpg,.jpeg,.png,.bmp',
    beforeUpload: handleUpload,
    onChange: (info) => {
      setFileList(info.fileList.slice(-1)); // 只保留最新的文件
    },
    onDrop: (e) => {
      console.log('Dropped files', e.dataTransfer.files);
    },
  };

  return (
    <div className="upload-panel">
      <Spin spinning={loading} tip="正在识别图片，请稍候...">
        <Space direction="vertical" size="large" style={{ width: '100%', maxWidth: 600 }}>
          <div style={{ textAlign: 'center' }}>
            <Title level={3}>上传图片开始识别</Title>
            <Text type="secondary">
              支持 JPG、PNG、BMP 格式，文件大小不超过 10MB
            </Text>
          </div>

          <Dragger {...uploadProps} style={{ padding: '40px 20px' }}>
            <p className="ant-upload-drag-icon">
              <InboxOutlined style={{ fontSize: 64, color: '#1890ff' }} />
            </p>
            <p className="ant-upload-text">点击或拖拽图片到此区域上传</p>
            <p className="ant-upload-hint">
              系统将自动识别图片中的题目并进行智能分割
            </p>
          </Dragger>

          <div style={{ textAlign: 'center' }}>
            <Text type="secondary" style={{ fontSize: 12 }}>
              💡 提示：图片越清晰，识别效果越好
            </Text>
          </div>
        </Space>
      </Spin>
    </div>
  );
};

export default UploadPanel;

