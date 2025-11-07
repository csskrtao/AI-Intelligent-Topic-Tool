import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 60000, // OCR 可能需要较长时间
});

/**
 * 上传图片并进行 OCR 识别
 * @param {File} file - 图片文件
 * @returns {Promise} - 返回识别结果
 */
export const uploadImage = async (file) => {
  const formData = new FormData();
  formData.append('file', file);

  const response = await api.post('/api/upload', formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  });

  return response.data;
};

/**
 * 导出题目
 * @param {Array<number>} questionIds - 题目 ID 列表
 * @param {string} exportFormat - 导出格式 ('text' | 'image' | 'both')
 * @returns {Promise} - 返回导出结果
 */
export const exportQuestions = async (questionIds, exportFormat = 'both') => {
  const response = await api.post('/api/export', {
    question_ids: questionIds,
    export_format: exportFormat,
  });

  return response.data;
};

/**
 * 获取图片 URL
 * @param {string} filename - 文件名
 * @returns {string} - 图片 URL
 */
export const getImageUrl = (filename) => {
  return `${API_BASE_URL}/api/image/${filename}`;
};

/**
 * 健康检查
 * @returns {Promise} - 返回健康状态
 */
export const healthCheck = async () => {
  const response = await api.get('/health');
  return response.data;
};

export default api;

