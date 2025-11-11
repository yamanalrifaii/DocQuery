# RAG QA System - Project Index

Complete guide to all files and their purposes.

## 📋 Getting Started

**Start here if you're new:**

1. [QUICKSTART.md](QUICKSTART.md) - Get running in 5 minutes
2. [SETUP.md](SETUP.md) - Detailed setup instructions
3. [README.md](README.md) - Full documentation
4. [SYSTEM_OVERVIEW.md](SYSTEM_OVERVIEW.md) - How it works

## 📁 Project Structure

```
qa-system/
├── Backend (Python/FastAPI)
│   ├── backend/
│   │   ├── __init__.py
│   │   ├── main.py           [FastAPI app & endpoints]
│   │   ├── config.py         [Configuration settings]
│   │   ├── document_loader.py [Document processing]
│   │   ├── vector_store.py    [FAISS management]
│   │   ├── rag_engine.py      [RAG pipeline]
│   │   └── Dockerfile         [Container config]
│   └── requirements.txt        [Python dependencies]
│
├── Frontend (React/Node)
│   ├── frontend/
│   │   ├── public/
│   │   │   └── index.html
│   │   ├── src/
│   │   │   ├── index.js       [React entry point]
│   │   │   ├── index.css      [Global styles]
│   │   │   ├── App.js         [Main component]
│   │   │   ├── App.css        [Main styles]
│   │   │   ├── api.js         [API client]
│   │   │   └── components/
│   │   │       ├── DocumentUpload.js [File upload]
│   │   │       ├── DocumentUpload.css
│   │   │       ├── QuestionForm.js  [Question input]
│   │   │       ├── QuestionForm.css
│   │   │       ├── AnswerDisplay.js [Answer rendering]
│   │   │       ├── AnswerDisplay.css
│   │   │       ├── SourcesList.js   [Source documents]
│   │   │       └── SourcesList.css
│   │   ├── package.json       [Node dependencies]
│   │   ├── Dockerfile         [Container config]
│   │   └── .gitignore
│   └──
│
├── Configuration & Deployment
│   ├── .env.example           [Environment template]
│   ├── .env                   [Environment variables (secret)]
│   ├── .gitignore             [Git ignore rules]
│   ├── docker-compose.yml     [Docker orchestration]
│   └── start.sh               [Startup script]
│
├── Documentation
│   ├── README.md              [Main documentation]
│   ├── QUICKSTART.md          [Quick start guide]
│   ├── SETUP.md               [Detailed setup]
│   ├── SYSTEM_OVERVIEW.md     [Architecture overview]
│   └── INDEX.md               [This file]
│
└── Sample Data
    └── sample_document.txt    [Test document]
```

## 🔧 Configuration Files

### [.env.example](.env.example)
Template for environment variables.

**Key variables:**
- `OPENAI_API_KEY` - Your OpenAI API key (required)
- `MODEL_NAME` - LLM model (default: gpt-3.5-turbo)
- `EMBEDDING_MODEL` - Embeddings model

**Setup:**
```bash
cp .env.example .env
# Edit .env with your API key
```

### [backend/config.py](backend/config.py)
Python configuration class.

**What it controls:**
- Chunk size (1000 tokens)
- Chunk overlap (200 tokens)
- Embedding model selection
- File paths for storage
- Max documents limit

**How to modify:**
Edit the `Settings` class with your preferences.

### [docker-compose.yml](docker-compose.yml)
Docker container orchestration.

**Services:**
- Backend service (port 8000)
- Frontend service (port 3000)
- Shared volume for data

**Usage:**
```bash
docker-compose up
```

## 📦 Backend Files

### [backend/main.py](backend/main.py) - FastAPI Application
**Responsibilities:**
- HTTP server setup
- API endpoint definitions
- Request/response handling
- Error management
- CORS configuration

**Key endpoints:**
- `GET /` - Health check
- `GET /status` - System status
- `POST /upload` - Upload document
- `POST /ask` - Answer question
- `POST /retrieve` - Retrieve docs

**Size:** ~350 lines

### [backend/config.py](backend/config.py) - Configuration
**Responsibilities:**
- Settings management
- Environment variable loading
- Default values
- Path configuration

**Customizable settings:**
- Chunk size
- Embedding model
- LLM model
- Storage paths

**Size:** ~20 lines

### [backend/document_loader.py](backend/document_loader.py) - Document Processing
**Responsibilities:**
- Load PDF, TXT, MD files
- Split documents into chunks
- Batch processing
- Error handling

**Main classes:**
- `DocumentProcessor` - Loads and chunks documents

**Key methods:**
- `load_document()` - Load single file
- `process_documents()` - Split into chunks
- `load_and_process()` - Combined operation
- `batch_process_directory()` - Multiple files

**Size:** ~90 lines

### [backend/vector_store.py](backend/vector_store.py) - Vector Database
**Responsibilities:**
- FAISS index management
- Vector embedding creation
- Similarity search
- Index persistence

**Main classes:**
- `VectorStoreManager` - Manages FAISS index

**Key methods:**
- `create_vector_store()` - Create new index
- `add_documents()` - Add to index
- `retrieve_documents()` - Similarity search
- `save_vector_store()` - Save to disk
- `load_vector_store()` - Load from disk

**Size:** ~100 lines

### [backend/rag_engine.py](backend/rag_engine.py) - RAG Pipeline
**Responsibilities:**
- LLM initialization
- QA chain creation
- Question answering
- Context formatting

**Main classes:**
- `RAGEngine` - Orchestrates retrieval + generation

**Key methods:**
- `answer_question()` - Generate answer
- `retrieve_relevant_documents()` - Get context
- `is_ready()` - Check initialization

**Size:** ~120 lines

### [requirements.txt](requirements.txt) - Python Dependencies
**Framework:**
- fastapi, uvicorn

**NLP/ML:**
- langchain, transformers, torch
- sentence-transformers, faiss-cpu

**Utils:**
- PyPDF2, python-dotenv, pydantic

**Version:** See file for exact versions

## 🎨 Frontend Files

### [frontend/src/App.js](frontend/src/App.js) - Main Component
**Responsibilities:**
- System state management
- Component orchestration
- API integration
- Status polling

**State:**
- System status
- Upload count
- Current answer
- Error messages

**Size:** ~150 lines

### [frontend/src/components/DocumentUpload.js](frontend/src/components/DocumentUpload.js)
**Functionality:**
- Drag-and-drop file upload
- File type validation
- Upload progress indication
- Success/error feedback

**Features:**
- Accept PDF, TXT, MD
- Visual feedback
- Loading state
- Error messages

**Size:** ~100 lines

### [frontend/src/components/QuestionForm.js](frontend/src/components/QuestionForm.js)
**Functionality:**
- Question input field
- Submit button
- Loading state
- Disabled state handling

**States:**
- Default (enabled)
- Loading (answering)
- Disabled (no documents)

**Size:** ~40 lines

### [frontend/src/components/AnswerDisplay.js](frontend/src/components/AnswerDisplay.js)
**Functionality:**
- Display generated answer
- Markdown rendering
- Syntax highlighting

**Format:**
- Markdown support
- Lists, code blocks
- Links, formatting

**Size:** ~30 lines

### [frontend/src/components/SourcesList.js](frontend/src/components/SourcesList.js)
**Functionality:**
- Show source documents
- Collapsible sections
- Metadata display
- Source highlighting

**Features:**
- Expandable sources
- Metadata display
- Document count
- Relevant excerpt display

**Size:** ~70 lines

### [frontend/src/api.js](frontend/src/api.js) - HTTP Client
**Responsibilities:**
- API communication
- Axios configuration
- Error handling
- Base URL management

**Methods:**
- `getStatus()` - Get system status
- `uploadDocument()` - Upload file
- `askQuestion()` - Ask question
- `retrieveDocuments()` - Get context

**Size:** ~80 lines

### [frontend/package.json](frontend/package.json) - Dependencies
**Framework:**
- react, react-dom, react-scripts

**Libraries:**
- axios, react-markdown, lucide-react

## 📚 Documentation Files

### [README.md](README.md)
**Complete project documentation:**
- Features overview
- Architecture explanation
- Installation steps
- API reference
- Configuration guide
- Troubleshooting
- Performance tuning
- Future roadmap

**Sections:** 20+ comprehensive sections
**Length:** ~500 lines

### [QUICKSTART.md](QUICKSTART.md)
**Fast setup guide:**
- 5-minute setup
- Step-by-step instructions
- Testing procedures
- Troubleshooting
- Common questions

**Audience:** First-time users
**Length:** ~150 lines

### [SETUP.md](SETUP.md)
**Detailed setup guide:**
- Detailed prerequisites
- Step-by-step backend setup
- Step-by-step frontend setup
- Configuration options
- Development setup
- Deployment preparation

**Audience:** Users wanting full details
**Length:** ~250 lines

### [SYSTEM_OVERVIEW.md](SYSTEM_OVERVIEW.md)
**Architecture & design:**
- System overview
- Architecture diagrams
- Data flow examples
- Component explanations
- Configuration guide
- Performance metrics
- Integration examples

**Audience:** Developers, architects
**Length:** ~400 lines

### [INDEX.md](INDEX.md)
**Project index:** (This file)
- File locations
- File purposes
- File sizes
- Quick reference

**Audience:** Anyone learning codebase

## 🧪 Test & Sample Files

### [sample_document.txt](sample_document.txt)
**Content:**
- Machine Learning introduction
- Historical overview
- Key concepts
- Applications
- Challenges

**Purpose:**
- Test document for QA system
- Demonstrates system capabilities
- ~1500 tokens

## 🚀 Startup & Deployment

### [start.sh](start.sh)
**Automated startup script:**
- Checks Python/Node installation
- Creates virtual environment
- Installs dependencies
- Starts both servers
- Shows URLs

**Usage:**
```bash
chmod +x start.sh
./start.sh
```

### [docker-compose.yml](docker-compose.yml)
**Docker orchestration:**
- Backend service definition
- Frontend service definition
- Environment variable passing
- Volume configuration
- Health checks

**Usage:**
```bash
docker-compose up
```

### [backend/Dockerfile](backend/Dockerfile)
**Backend containerization:**
- Python 3.11 slim base
- Dependency installation
- Code copying
- Port exposure
- Health check

### [frontend/Dockerfile](frontend/Dockerfile)
**Frontend containerization:**
- Node build stage
- Production serve stage
- Static file serving
- Port 3000 exposure

## 📊 File Statistics

### Backend
- Python files: 5
- Total lines: ~660
- Complexity: Medium

### Frontend
- JavaScript files: 6
- CSS files: 5
- Total lines: ~800
- Complexity: Medium

### Documentation
- Markdown files: 5
- Total lines: ~1500

### Configuration
- Config files: 4
- Total lines: ~100

## 🔍 Quick Reference

### To Edit...

**Backend settings:**
→ `backend/config.py`

**Backend API logic:**
→ `backend/main.py`

**Document processing:**
→ `backend/document_loader.py`

**Vector search:**
→ `backend/vector_store.py`

**RAG pipeline:**
→ `backend/rag_engine.py`

**UI layout:**
→ `frontend/src/App.js`

**Document upload UI:**
→ `frontend/src/components/DocumentUpload.js`

**Answer display:**
→ `frontend/src/components/AnswerDisplay.js`

**API communication:**
→ `frontend/src/api.js`

**Environment variables:**
→ `.env`

**Docker setup:**
→ `docker-compose.yml`

## 🎯 Navigation Guide

**I want to...**

- **Get started:** → [QUICKSTART.md](QUICKSTART.md)
- **Set up fully:** → [SETUP.md](SETUP.md)
- **Understand architecture:** → [SYSTEM_OVERVIEW.md](SYSTEM_OVERVIEW.md)
- **API reference:** → [README.md](README.md#api-endpoints)
- **Fix a problem:** → [README.md](README.md#troubleshooting)
- **Deploy to production:** → [docker-compose.yml](docker-compose.yml)
- **Find a file:** → [INDEX.md](INDEX.md) (this file)

## 📈 Project Growth Path

### Current Features
- Document upload (PDF, TXT, MD)
- Vector search (FAISS)
- QA with OpenAI GPT
- Source attribution
- Web UI (React)
- REST API (FastAPI)

### Next Steps
- User authentication
- Conversation history
- Multiple documents per query
- Local LLM support
- Advanced filtering
- Response streaming

### Future Enhancements
- Database persistence
- Vector visualization
- Analytics dashboard
- Custom embedding models
- Multi-language support
- Feedback loop for improvements

---

**For quick navigation, see [QUICKSTART.md](QUICKSTART.md) or [README.md](README.md)**
