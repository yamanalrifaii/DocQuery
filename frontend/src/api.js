import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const apiClient = {
  /**
   * Get system status
   */
  async getStatus() {
    try {
      const response = await api.get('/status');
      return response.data;
    } catch (error) {
      throw this._handleError(error);
    }
  },

  /**
   * Upload a document
   */
  async uploadDocument(file) {
    try {
      const formData = new FormData();
      formData.append('file', file);

      const response = await api.post('/upload', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
      return response.data;
    } catch (error) {
      throw this._handleError(error);
    }
  },

  /**
   * Ask a question
   */
  async askQuestion(question) {
    try {
      const response = await api.post('/ask', {
        question: question,
      });
      return response.data;
    } catch (error) {
      throw this._handleError(error);
    }
  },

  /**
   * Retrieve relevant documents
   */
  async retrieveDocuments(question, k = 4) {
    try {
      const response = await api.post('/retrieve', { question }, {
        params: { k },
      });
      return response.data;
    } catch (error) {
      throw this._handleError(error);
    }
  },

  /**
   * Handle API errors
   */
  _handleError(error) {
    if (error.response) {
      return new Error(error.response.data?.detail || 'API Error');
    } else if (error.request) {
      return new Error('Network error: No response from server');
    } else {
      return error;
    }
  },
};

export default api;
