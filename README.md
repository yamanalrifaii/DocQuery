# RAG QA System

A production-ready question-answering system built with **Retrieval-Augmented Generation (RAG)** that answers natural language questions based on uploaded documents.

## Features

- 🚀 **Fast & Scalable**: Uses FAISS for efficient vector similarity search
- 📄 **Multi-Format Support**: Accepts PDF, TXT, and Markdown documents
- 🧠 **Advanced NLP**: Leverages LangChain, HuggingFace embeddings, and OpenAI GPT
- 🎨 **Modern Web UI**: React-based interface with real-time feedback
- 📊 **Source Attribution**: Returns relevant document excerpts for each answer
- 🔄 **Dynamic Updates**: Add documents to the system at any time
- 🛡️ **Production Ready**: Error handling, validation, and logging throughout

## Architecture

### Tech Stack

**Backend:**
- FastAPI - Modern Python web framework
- LangChain - LLM orchestration and RAG pipeline
- FAISS - Vector similarity search
- HuggingFace - Sentence embeddings
- OpenAI - LLM for answer generation
- Pydantic - Data validation

**Frontend:**
- React 18 - UI framework
- Axios - HTTP client
- React Markdown - Rich text rendering
- Lucide React - Icons

### System Flow

```
User Question
    ↓
Vector Store Search (FAISS)
    ↓
Retrieve Top-K Documents
    ↓
LLM (GPT) with Context
    ↓
Generate Answer
    ↓
Display with Sources
```

## Installation

### Prerequisites

- Python 3.10+
- Node.js 16+
- OpenAI API key

### Backend Setup

1. **Navigate to project directory:**
```bash
cd qa-system
```

2. **Create Python virtual environment:**
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies:**
```bash
pip install -r requirements.txt
```

4. **Set up environment variables:**
```bash
cp .env.example .env
# Edit .env and add your OpenAI API key
export OPENAI_API_KEY=sk-...
```

5. **Start the backend server:**
```bash
cd backend
python main.py
```

The API will be available at `http://localhost:8000`

### Frontend Setup

1. **Navigate to frontend directory:**
```bash
cd frontend
```

2. **Install dependencies:**
```bash
npm install
```

3. **Set environment variables (optional):**
```bash
# Create .env.local if backend is on different port
echo "REACT_APP_API_URL=http://localhost:8000" > .env.local
```

4. **Start development server:**
```bash
npm start
```

The UI will be available at `http://localhost:3000`


## Supported File Types

- **PDF**
- **Text** 
- **Markdown**


