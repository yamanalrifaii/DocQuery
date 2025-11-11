import React, { useState } from 'react';
import { Send } from 'lucide-react';
import './QuestionForm.css';

function QuestionForm({ onSubmit, isLoading, isDisabled }) {
  const [question, setQuestion] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!question.trim() || isLoading || isDisabled) return;
    onSubmit(question.trim());
    setQuestion('');
  };

  return (
    <form className="question-form" onSubmit={handleSubmit}>
      <div className="form-group">
        <input
          type="text"
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
          placeholder="Ask a question about your documents..."
          disabled={isLoading || isDisabled}
          className="question-input"
        />
        <button
          type="submit"
          disabled={isLoading || isDisabled || !question.trim()}
          className="submit-button"
        >
          {isLoading ? (
            <>
              <div className="button-spinner"></div>
              <span>Answering...</span>
            </>
          ) : (
            <>
              <Send className="button-icon" />
              <span>Ask</span>
            </>
          )}
        </button>
      </div>
      {isDisabled && (
        <p className="form-hint">Upload documents first to ask questions</p>
      )}
    </form>
  );
}

export default QuestionForm;
