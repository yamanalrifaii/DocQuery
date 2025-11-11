import React, { useState, useEffect } from 'react';
import './App.css';
import DocumentUpload from './components/DocumentUpload';
import QuestionForm from './components/QuestionForm';
import AnswerDisplay from './components/AnswerDisplay';
import SourcesList from './components/SourcesList';
import { apiClient } from './api';
import { FileText, MessageSquare, AlertCircle } from 'lucide-react';

function App() {
  const [status, setStatus] = useState(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);
  const [isAnswering, setIsAnswering] = useState(false);
  const [answer, setAnswer] = useState(null);
  const [sources, setSources] = useState([]);
  const [uploadCount, setUploadCount] = useState(0);

  // Fetch status on component mount
  useEffect(() => {
    fetchStatus();
    const interval = setInterval(fetchStatus, 5000);
    return () => clearInterval(interval);
  }, []);

  const fetchStatus = async () => {
    try {
      const data = await apiClient.getStatus();
      setStatus(data);
      setIsLoading(false);
      setError(null);
    } catch (err) {
      setError('Failed to connect to backend. Make sure the server is running.');
      setIsLoading(false);
    }
  };

  const handleDocumentUpload = async (file) => {
    try {
      setError(null);
      const result = await apiClient.uploadDocument(file);
      setUploadCount(prev => prev + 1);
      return {
        success: true,
        message: result.message,
      };
    } catch (err) {
      setError(err.message);
      return {
        success: false,
        message: err.message,
      };
    }
  };

  const handleAskQuestion = async (question) => {
    setIsAnswering(true);
    setError(null);
    try {
      const result = await apiClient.askQuestion(question);
      setAnswer(result.answer);
      setSources(result.sources);
    } catch (err) {
      setError(err.message);
      setAnswer(null);
      setSources([]);
    } finally {
      setIsAnswering(false);
    }
  };

  return (
    <div className="app">
      <header className="app-header">
        <div className="header-content">
          <h1>
            <FileText className="header-icon" />
            RAG QA System
          </h1>
          <p>Ask questions about your documents powered by RAG</p>
        </div>
      </header>

      <main className="app-main">
        {isLoading ? (
          <div className="loading-container">
            <div className="spinner"></div>
            <p>Connecting to server...</p>
          </div>
        ) : (
          <>
            {error && (
              <div className="error-message">
                <AlertCircle className="error-icon" />
                {error}
              </div>
            )}

            {!status?.initialized && !error && (
              <div className="info-banner">
                <MessageSquare className="info-icon" />
                <span>Upload documents to get started</span>
              </div>
            )}

            <div className="content-grid">
              <section className="section upload-section">
                <h2>Upload Documents</h2>
                <DocumentUpload onUpload={handleDocumentUpload} />
                {status?.initialized && (
                  <p className="status-text">✓ Documents indexed and ready</p>
                )}
              </section>

              <section className="section qa-section">
                <h2>Ask Questions</h2>
                <QuestionForm
                  onSubmit={handleAskQuestion}
                  isLoading={isAnswering}
                  isDisabled={!status?.initialized}
                />

                {answer && (
                  <>
                    <AnswerDisplay answer={answer} />
                    <SourcesList sources={sources} />
                  </>
                )}
              </section>
            </div>
          </>
        )}
      </main>

      <footer className="app-footer">
        <p>RAG QA System • Powered by LangChain, FAISS, and OpenAI</p>
      </footer>
    </div>
  );
}

export default App;
