import React from 'react';
import ReactMarkdown from 'react-markdown';
import { MessageCircle } from 'lucide-react';
import './AnswerDisplay.css';

function AnswerDisplay({ answer }) {
  return (
    <div className="answer-display">
      <div className="answer-header">
        <MessageCircle className="answer-icon" />
        <h3>Answer</h3>
      </div>
      <div className="answer-content">
        <ReactMarkdown>{answer}</ReactMarkdown>
      </div>
    </div>
  );
}

export default AnswerDisplay;
