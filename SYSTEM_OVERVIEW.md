# RAG QA System - Complete Overview

## What is This System?

A **Retrieval-Augmented Generation (RAG)** question-answering system that:

1. **Accepts documents** (PDF, TXT, MD)
2. **Chunks and indexes** them using FAISS
3. **Answers questions** by retrieving relevant sections
4. **Uses LLM** (GPT-3.5/4) to generate natural language answers
5. **Shows sources** - where each answer came from

## Architecture Overview

```
┌─────────────────────────────────────────────────────────┐
│                      WEB INTERFACE                       │
│                  (React - Port 3000)                    │
│  - Upload documents                                      │
│  - Ask questions                                         │
│  - View answers with sources                            │
└────────────────────────┬────────────────────────────────┘
                         │
                         ↓
┌─────────────────────────────────────────────────────────┐
│                   FASTAPI BACKEND                        │
│                   (Python - Port 8000)                  │
├──────────────────────────────────────────────────────────┤
│  Routes:                                                 │
│  - POST /upload    → Process documents                  │
│  - POST /ask       → Answer questions                   │
│  - POST /retrieve  → Get relevant docs                  │
│  - GET  /status    → System status                      │
└────────────┬─────────────────────────────────┬──────────┘
             │                                 │
             ↓                                 ↓
    ┌─────────────────┐            ┌──────────────────┐
    │  VECTOR STORE   │            │  LANGUAGE MODEL  │
    │  (FAISS)        │            │  (OpenAI GPT)    │
    │                 │            │                  │
    │ - Embeddings    │            │ - Generation     │
    │ - Similarity    │            │ - Reasoning      │
    │   Search        │            │ - Summarization  │
    └────────┬────────┘            └──────────────────┘
             │
             ↓
    ┌─────────────────┐
    │  DOCUMENTS      │
    │  (File Storage) │
    │                 │
    │ PDFs, TXT, MD   │
    └─────────────────┘
```

## How It Works

### 1. Document Upload

```
User uploads document.pdf
    ↓
DocumentProcessor loads PDF
    ↓
RecursiveCharacterTextSplitter chunks text
    (chunk_size=1000, overlap=200)
    ↓
HuggingFace creates embeddings for each chunk
    ↓
FAISS indexes all embeddings
    ↓
Vector store saved to disk
    ↓
Ready for queries
```

### 2. Question Answering

```
User: "What is X?"
    ↓
FAISS similarity search finds top-k chunks
    (k=4 by default)
    ↓
Chunks formatted as context
    ↓
Prompt: "Context: [chunks]... Question: What is X?"
    ↓
OpenAI GPT generates answer
    ↓
Answer + source documents returned to user
```

## Core Components

### Backend (`backend/`)

**main.py** - FastAPI application
- HTTP endpoints for upload/ask/retrieve
- Error handling and validation
- CORS support for frontend
- Startup/shutdown events

**config.py** - Configuration management
- Chunk size: 1000 tokens
- Embedding model: sentence-transformers/all-MiniLM-L6-v2
- LLM model: gpt-3.5-turbo
- Paths for data storage

**document_loader.py** - Document processing
- Loads PDF, TXT, MD files
- Splits text into chunks
- Recursive chunking for better context
- Batch processing support

**vector_store.py** - FAISS management
- Creates vector index
- Adds documents to index
- Similarity search
- Save/load functionality

**rag_engine.py** - RAG pipeline
- Chains retriever + LLM
- Custom prompt templates
- Source attribution
- Error handling

### Frontend (`frontend/`)

**App.js** - Main React component
- Status monitoring
- Document management
- Question interface
- Response display

**Components:**
- `DocumentUpload.js` - Drag-drop file upload
- `QuestionForm.js` - Question input
- `AnswerDisplay.js` - Markdown answer rendering
- `SourcesList.js` - Collapsible source documents

**api.js** - HTTP client
- Status endpoint
- Upload endpoint
- Question endpoint
- Error handling

## Data Flow Examples

### Example 1: Upload Document

```javascript
// Frontend sends file
axios.post('/upload', formData, {
  headers: { 'Content-Type': 'multipart/form-data' }
})

// Backend receives
# main.py /upload endpoint
file_path = save_uploaded_file()
chunks = doc_processor.load_and_process(file_path)
vector_store_manager.add_documents(chunks)
vector_store_manager.save_vector_store()

// Frontend shows success
"✓ Document processed with 15 chunks"
```

### Example 2: Ask Question

```javascript
// Frontend sends question
axios.post('/ask', {
  question: "What is machine learning?"
})

// Backend flow
1. vector_store.retrieve_documents(question, k=4)
   → Returns top 4 similar chunks

2. rag_engine.answer_question(question)
   → Creates prompt with context
   → Calls OpenAI API
   → Gets generated answer

3. Returns {
     answer: "Machine learning is...",
     sources: [
       { content: "...", metadata: {...} },
       ...
     ]
   }

// Frontend displays answer + sources
```

## Key Features Explained

### 1. Semantic Search (FAISS)

- **What:** Finds chunks semantically similar to question
- **How:** Converts question to embeddings, finds nearest neighbors
- **Why:** Much better than keyword search
- **Example:**
  ```
  Question: "How was X discovered?"
  Search: Embeddings similar to this question
  Result: Chunk about "Finding X" or "History of X"
  ```

### 2. Context in Prompts

- **What:** LLM sees relevant document sections
- **Why:** Grounds answers in actual content
- **Example:**
  ```
  System Prompt:
  "Context: [4 relevant chunks]
   Question: What is Y?
   Answer based on context above."
  ```

### 3. Source Attribution

- **What:** Shows which documents the answer came from
- **Why:** Improves trust and allows verification
- **How:** Returns metadata with each chunk

### 4. Streaming Ready

- **Current:** Returns full answer at once
- **Future:** Can stream tokens for faster perceived response

## Configuration & Tuning

### For Better Answers

```python
# config.py
chunk_size = 2000        # More context per chunk
chunk_overlap = 500      # Better continuity
```

```javascript
// api.js - When retrieving
k = 8  // Get more context documents
```

### For Faster Response

```python
chunk_size = 500         # Smaller = faster search
```

```javascript
k = 2  // Fewer documents to process
```

### Different Models

```python
# gpt-4 for better quality
llm = ChatOpenAI(model_name="gpt-4")

# Different embeddings
embeddings = HuggingFaceEmbeddings(
    model_name="all-mpnet-base-v2"  # Better quality
)
```

## Limitations & Considerations

### Current Limitations

- **Context Window:** GPT-3.5 has 4K tokens (includes prompt)
- **Cost:** OpenAI API charges per token
- **File Size:** Limited by available RAM
- **Speed:** First embeddings download model (~400MB)
- **No Conversation:** Each question is independent

### When to Use

✅ **Good for:**
- Document-based Q&A
- Knowledge bases
- FAQ systems
- Technical documentation
- Research paper analysis

❌ **Not ideal for:**
- Real-time systems (slow)
- Multi-turn conversations
- Very large corpora (scale needed)
- Privacy-sensitive data (uses OpenAI)

## Performance Metrics

| Operation | Time | Notes |
|-----------|------|-------|
| Upload 10 pages | 5-10s | First run downloads model |
| Vector search | <100ms | FAISS is very fast |
| LLM generation | 1-3s | Depends on OpenAI load |
| Full Q&A cycle | 2-5s | Total end-to-end |

## Costs

**OpenAI API Pricing (approximate):**
- GPT-3.5 Input: $0.50 / 1M tokens
- GPT-3.5 Output: $1.50 / 1M tokens
- GPT-4 Input: $10 / 1M tokens
- GPT-4 Output: $30 / 1M tokens

**Typical usage:**
- One question: 100-500 output tokens (~$0.0005-0.002)
- 100 questions/month: $0.05-0.20

## Deployment Options

### Development
```bash
# Run locally
python backend/main.py
npm start (frontend)
```

### Docker
```bash
docker-compose up
```

### Cloud
- AWS: EC2 + RDS for metadata
- GCP: Cloud Run + Firestore
- Azure: App Service + Cosmos DB

## Integration Examples

### Python Script
```python
from api import apiClient

result = await apiClient.askQuestion("Question?")
print(result["answer"])
```

### JavaScript/Node
```javascript
import { apiClient } from './api.js'

const result = await apiClient.askQuestion("Question?")
console.log(result.answer)
```

### cURL
```bash
curl -X POST http://localhost:8000/ask \
  -H "Content-Type: application/json" \
  -d '{"question": "Your question"}'
```

## Roadmap & Future Enhancements

- [ ] Streaming responses
- [ ] Conversation history
- [ ] Multi-document queries
- [ ] User authentication
- [ ] Document versioning
- [ ] Advanced filtering
- [ ] Custom embeddings
- [ ] Local LLM support
- [ ] Database persistence
- [ ] Performance analytics

## Troubleshooting Reference

| Issue | Cause | Fix |
|-------|-------|-----|
| Wrong answers | Poor context | Increase k, adjust chunk size |
| Slow responses | Network lag | Check API status, reduce k |
| Out of memory | Large documents | Reduce chunk size |
| API errors | Rate limit | Wait or upgrade OpenAI plan |

## For More Information

- **Quick start:** See QUICKSTART.md
- **Setup details:** See SETUP.md
- **API docs:** See README.md#api-endpoints
- **Configuration:** Edit backend/config.py
- **Architecture:** See this file

---

**System built with:** LangChain, FAISS, HuggingFace, FastAPI, React, OpenAI
