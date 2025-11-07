import React from 'react';
import { Card, List, Checkbox, Typography, Empty } from 'antd';
import { FileTextOutlined } from '@ant-design/icons';
import './QuestionList.css';

const { Text, Paragraph } = Typography;

const QuestionList = ({ questions, selectedQuestions, setSelectedQuestions }) => {
  const handleSelectChange = (questionId, checked) => {
    if (checked) {
      setSelectedQuestions([...selectedQuestions, questionId]);
    } else {
      setSelectedQuestions(selectedQuestions.filter(id => id !== questionId));
    }
  };

  const handleSelectAll = (checked) => {
    if (checked) {
      setSelectedQuestions(questions.map(q => q.question_id));
    } else {
      setSelectedQuestions([]);
    }
  };

  return (
    <Card 
      title={
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
          <span>题目列表 ({questions.length})</span>
          <Checkbox
            checked={selectedQuestions.length === questions.length && questions.length > 0}
            indeterminate={selectedQuestions.length > 0 && selectedQuestions.length < questions.length}
            onChange={(e) => handleSelectAll(e.target.checked)}
          >
            全选
          </Checkbox>
        </div>
      }
      className="question-list-card"
      bodyStyle={{ 
        height: 'calc(100% - 57px)', 
        overflow: 'auto',
        padding: 0
      }}
    >
      {questions.length === 0 ? (
        <Empty 
          description="暂无题目"
          style={{ marginTop: 60 }}
        />
      ) : (
        <List
          dataSource={questions}
          renderItem={(question) => (
            <List.Item
              key={question.question_id}
              className={`question-item ${selectedQuestions.includes(question.question_id) ? 'selected' : ''}`}
              onClick={() => handleSelectChange(
                question.question_id, 
                !selectedQuestions.includes(question.question_id)
              )}
            >
              <div className="question-content">
                <div className="question-header">
                  <Checkbox
                    checked={selectedQuestions.includes(question.question_id)}
                    onChange={(e) => {
                      e.stopPropagation();
                      handleSelectChange(question.question_id, e.target.checked);
                    }}
                  />
                  <FileTextOutlined style={{ marginLeft: 8, color: '#1890ff' }} />
                  <Text strong style={{ marginLeft: 8 }}>
                    题目 {question.question_id}
                  </Text>
                </div>
                <Paragraph 
                  className="question-text"
                  ellipsis={{ rows: 3, expandable: true, symbol: '展开' }}
                >
                  {question.text}
                </Paragraph>
              </div>
            </List.Item>
          )}
        />
      )}
    </Card>
  );
};

export default QuestionList;

