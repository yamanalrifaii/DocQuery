import React, { useState, useRef } from 'react';
import { Upload, CheckCircle, AlertCircle } from 'lucide-react';
import './DocumentUpload.css';

function DocumentUpload({ onUpload }) {
  const [isDragging, setIsDragging] = useState(false);
  const [isUploading, setIsUploading] = useState(false);
  const [uploadStatus, setUploadStatus] = useState(null);
  const fileInputRef = useRef(null);

  const handleDragEnter = (e) => {
    e.preventDefault();
    setIsDragging(true);
  };

  const handleDragLeave = (e) => {
    e.preventDefault();
    setIsDragging(false);
  };

  const handleDragOver = (e) => {
    e.preventDefault();
  };

  const handleDrop = (e) => {
    e.preventDefault();
    setIsDragging(false);
    const files = e.dataTransfer.files;
    if (files.length > 0) {
      handleFile(files[0]);
    }
  };

  const handleFileSelect = (e) => {
    if (e.target.files.length > 0) {
      handleFile(e.target.files[0]);
    }
  };

  const handleFile = async (file) => {
    // Validate file type
    const validTypes = ['application/pdf', 'text/plain', 'text/markdown'];
    if (!validTypes.includes(file.type) && !file.name.endsWith('.md')) {
      setUploadStatus({
        type: 'error',
        message: 'Only PDF, TXT, and Markdown files are supported',
      });
      return;
    }

    setIsUploading(true);
    setUploadStatus(null);

    try {
      const result = await onUpload(file);
      setUploadStatus({
        type: result.success ? 'success' : 'error',
        message: result.message,
      });
    } catch (error) {
      setUploadStatus({
        type: 'error',
        message: error.message,
      });
    } finally {
      setIsUploading(false);
      // Reset file input
      if (fileInputRef.current) {
        fileInputRef.current.value = '';
      }
    }
  };

  return (
    <div className="document-upload">
      <div
        className={`upload-zone ${isDragging ? 'dragging' : ''} ${
          isUploading ? 'uploading' : ''
        }`}
        onDragEnter={handleDragEnter}
        onDragLeave={handleDragLeave}
        onDragOver={handleDragOver}
        onDrop={handleDrop}
      >
        <input
          ref={fileInputRef}
          type="file"
          onChange={handleFileSelect}
          disabled={isUploading}
          accept=".pdf,.txt,.md"
          style={{ display: 'none' }}
        />

        <div className="upload-content">
          {isUploading ? (
            <>
              <div className="upload-spinner"></div>
              <p>Uploading and processing...</p>
            </>
          ) : (
            <>
              <Upload className="upload-icon" />
              <p className="upload-text">
                Drag and drop your document here, or{' '}
                <button
                  className="upload-button"
                  onClick={() => fileInputRef.current?.click()}
                >
                  click to select
                </button>
              </p>
              <p className="upload-hint">
                Supports PDF, TXT, and Markdown files
              </p>
            </>
          )}
        </div>
      </div>

      {uploadStatus && (
        <div className={`upload-status ${uploadStatus.type}`}>
          {uploadStatus.type === 'success' ? (
            <CheckCircle className="status-icon" />
          ) : (
            <AlertCircle className="status-icon" />
          )}
          <span>{uploadStatus.message}</span>
        </div>
      )}
    </div>
  );
}

export default DocumentUpload;
