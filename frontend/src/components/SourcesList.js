import React, { useState } from 'react';
import { ChevronDown, ChevronUp, FileText } from 'lucide-react';
import './SourcesList.css';

function SourcesList({ sources }) {
  const [expandedIndex, setExpandedIndex] = useState(null);

  if (!sources || sources.length === 0) {
    return null;
  }

  const toggleExpand = (index) => {
    setExpandedIndex(expandedIndex === index ? null : index);
  };

  return (
    <div className="sources-list">
      <h3 className="sources-title">Source Documents ({sources.length})</h3>
      <div className="sources-container">
        {sources.map((source, index) => (
          <div key={index} className="source-item">
            <button
              className="source-header"
              onClick={() => toggleExpand(index)}
            >
              <FileText className="source-icon" />
              <span className="source-label">
                Source {index + 1}
                {source.metadata?.source && ` - ${source.metadata.source}`}
              </span>
              {expandedIndex === index ? (
                <ChevronUp className="source-chevron" />
              ) : (
                <ChevronDown className="source-chevron" />
              )}
            </button>
            {expandedIndex === index && (
              <div className="source-content">
                <p>{source.content}</p>
                {Object.keys(source.metadata || {}).length > 0 && (
                  <div className="source-metadata">
                    <h4>Metadata</h4>
                    <ul>
                      {Object.entries(source.metadata).map(([key, value]) => (
                        <li key={key}>
                          <strong>{key}:</strong> {String(value)}
                        </li>
                      ))}
                    </ul>
                  </div>
                )}
              </div>
            )}
          </div>
        ))}
      </div>
    </div>
  );
}

export default SourcesList;
