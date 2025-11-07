import React, { useState } from 'react';
import { Layout, message } from 'antd';
import UploadPanel from './components/UploadPanel';
import PreviewPanel from './components/PreviewPanel';
import './App.css';

const { Header, Content } = Layout;
const API_BASE_URL = 'http://localhost:8000';

function App() {
  const [imageUrl, setImageUrl] = useState(null);
  const [questions, setQuestions] = useState([]);
  const [loading, setLoading] = useState(false);

  const handleUploadSuccess = (data) => {
    // 将相对路径转换为完整 URL
    const fullImageUrl = data.image_url.startsWith('http')
      ? data.image_url
      : `${API_BASE_URL}${data.image_url}`;

    console.log('上传成功，数据:', data);
    console.log('图片 URL:', fullImageUrl);
    console.log('题目数量:', data.questions.length);

    setImageUrl(fullImageUrl);
    setQuestions(data.questions);
    message.success(`图片识别成功！识别到 ${data.questions.length} 道题目`);
  };

  const handleUploadError = (error) => {
    message.error(`上传失败: ${error.message}`);
  };

  return (
    <Layout style={{ height: '100vh' }}>
      <Header style={{ 
        background: '#fff', 
        padding: '0 24px',
        borderBottom: '1px solid #f0f0f0',
        display: 'flex',
        alignItems: 'center'
      }}>
        <h1 style={{ margin: 0, fontSize: '20px', fontWeight: 600 }}>
          🎯 AI 智能切题工具
        </h1>
      </Header>
      <Content style={{ padding: '24px', overflow: 'hidden' }}>
        {!imageUrl ? (
          <UploadPanel 
            onSuccess={handleUploadSuccess}
            onError={handleUploadError}
            loading={loading}
            setLoading={setLoading}
          />
        ) : (
          <PreviewPanel 
            imageUrl={imageUrl}
            questions={questions}
            setQuestions={setQuestions}
            onReset={() => {
              setImageUrl(null);
              setQuestions([]);
            }}
          />
        )}
      </Content>
    </Layout>
  );
}

export default App;

