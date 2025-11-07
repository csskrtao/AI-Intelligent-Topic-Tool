import React, { useState } from 'react';
import { Row, Col, Button, Space, message } from 'antd';
import { ReloadOutlined } from '@ant-design/icons';
import ImageViewer from './ImageViewer';
import QuestionList from './QuestionList';
import { exportQuestions } from '../services/api';
import './PreviewPanel.css';

const PreviewPanel = ({ imageUrl, questions, setQuestions, onReset }) => {
  const [selectedQuestions, setSelectedQuestions] = useState([]);
  const [exporting, setExporting] = useState(false);
  const [hoveredQuestionId, setHoveredQuestionId] = useState(null);

  const handleMerge = () => {
    if (selectedQuestions.length < 2) {
      message.warning('请至少选择两道题目进行合并');
      return;
    }

    // 按 ID 排序
    const sortedIds = [...selectedQuestions].sort((a, b) => a - b);
    
    // 找到要合并的题目
    const questionsToMerge = questions.filter(q => sortedIds.includes(q.question_id));
    
    // 合并文本
    const mergedText = questionsToMerge.map(q => q.text).join('\n\n');
    
    // 创建新题目
    const newQuestion = {
      question_id: sortedIds[0],
      text: mergedText,
    };

    // 移除被合并的题目，添加新题目
    const newQuestions = questions
      .filter(q => !sortedIds.includes(q.question_id))
      .concat(newQuestion)
      .sort((a, b) => a.question_id - b.question_id);

    setQuestions(newQuestions);
    setSelectedQuestions([]);
    message.success('题目合并成功');
  };

  const handleExport = async (format) => {
    if (selectedQuestions.length === 0) {
      message.warning('请至少选择一道题目进行导出');
      return;
    }

    setExporting(true);
    try {
      const result = await exportQuestions(selectedQuestions, format);
      message.success(`导出成功！文件保存在: ${result.export_dir}`);
    } catch (error) {
      message.error(`导出失败: ${error.message}`);
    } finally {
      setExporting(false);
    }
  };

  return (
    <div className="preview-panel">
      <Space style={{ marginBottom: 16 }}>
        <Button icon={<ReloadOutlined />} onClick={onReset}>
          重新上传
        </Button>
        <Button 
          type="primary" 
          onClick={handleMerge}
          disabled={selectedQuestions.length < 2}
        >
          合并选中题目
        </Button>
        <Button 
          onClick={() => handleExport('text')}
          disabled={selectedQuestions.length === 0}
          loading={exporting}
        >
          导出为文本
        </Button>
        <Button 
          onClick={() => handleExport('image')}
          disabled={selectedQuestions.length === 0}
          loading={exporting}
        >
          导出为图片
        </Button>
        <Button 
          type="primary"
          onClick={() => handleExport('both')}
          disabled={selectedQuestions.length === 0}
          loading={exporting}
        >
          导出全部
        </Button>
      </Space>

      <Row gutter={24} style={{ height: 'calc(100% - 48px)' }}>
        <Col span={12} style={{ height: '100%' }}>
          <ImageViewer
            imageUrl={imageUrl}
            questions={questions}
            selectedQuestionId={hoveredQuestionId}
            onQuestionHover={setHoveredQuestionId}
          />
        </Col>
        <Col span={12} style={{ height: '100%' }}>
          <QuestionList
            questions={questions}
            selectedQuestions={selectedQuestions}
            setSelectedQuestions={setSelectedQuestions}
            hoveredQuestionId={hoveredQuestionId}
          />
        </Col>
      </Row>
    </div>
  );
};

export default PreviewPanel;

