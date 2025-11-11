"""FastAPI backend for RAG QA system"""
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import shutil
import os
from pathlib import Path

from config import settings
from document_loader import DocumentProcessor
from vector_store import VectorStoreManager
from rag_engine import RAGEngine

# Initialize FastAPI app
app = FastAPI(title="RAG QA System", version="1.0.0")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize components
doc_processor = DocumentProcessor()
vector_store_manager = VectorStoreManager()
rag_engine = None


# Request/Response models
class DocumentUploadRequest(BaseModel):
    """Request model for document upload"""
    filename: str


class QuestionRequest(BaseModel):
    """Request model for question answering"""
    question: str


class SourceDocument(BaseModel):
    """Source document in answer"""
    content: str
    metadata: dict


class AnswerResponse(BaseModel):
    """Response model for question answering"""
    answer: str
    sources: List[SourceDocument]
    success: bool
    error: Optional[str] = None


class StatusResponse(BaseModel):
    """Status response"""
    initialized: bool
    documents_indexed: int
    message: str


# Utility functions
def ensure_data_directories():
    """Ensure data directories exist"""
    Path(settings.documents_path).mkdir(parents=True, exist_ok=True)
    Path(settings.faiss_index_path).parent.mkdir(parents=True, exist_ok=True)


def initialize_rag_engine():
    """Initialize RAG engine if vector store exists and API key is set"""
    global rag_engine
    try:
        if vector_store_manager.is_initialized() and settings.openai_api_key:
            vector_store_manager.load_vector_store()
            rag_engine = RAGEngine(vector_store_manager)
    except Exception as e:
        print(f"Could not initialize RAG engine: {e}")
        rag_engine = None


# API Endpoints
@app.on_event("startup")
async def startup_event():
    """Initialize system on startup"""
    ensure_data_directories()
    initialize_rag_engine()


@app.get("/", tags=["Health"])
async def root():
    """Root endpoint"""
    return {
        "name": "RAG QA System",
        "version": "1.0.0",
        "status": "running"
    }


@app.get("/status", response_model=StatusResponse, tags=["Health"])
async def get_status():
    """Get system status"""
    global rag_engine

    is_initialized = vector_store_manager.is_initialized()

    # Try to reinitialize RAG engine if it's not ready but vector store exists and API key is set
    if not rag_engine and is_initialized and settings.openai_api_key:
        try:
            vector_store_manager.load_vector_store()
            rag_engine = RAGEngine(vector_store_manager)
        except Exception as e:
            print(f"Could not reinitialize RAG engine: {e}")

    message = "System ready for queries" if is_initialized else "No documents indexed yet"

    return {
        "initialized": is_initialized,
        "documents_indexed": 0,  # Could count from index
        "message": message
    }


@app.post("/upload", tags=["Documents"])
async def upload_document(file: UploadFile = File(...)):
    """Upload and process a document"""
    global rag_engine

    try:
        # Validate file type
        if file.filename and not any(file.filename.endswith(ext) for ext in ['.pdf', '.txt', '.md']):
            raise HTTPException(
                status_code=400,
                detail="Only PDF, TXT, and MD files are supported"
            )

        # Save uploaded file
        file_path = os.path.join(settings.documents_path, file.filename or "document")
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # Process document
        chunks = doc_processor.load_and_process(file_path)

        if not chunks:
            raise HTTPException(
                status_code=400,
                detail="Document contains no text"
            )

        # Add to vector store
        if vector_store_manager.vector_store is None:
            vector_store_manager.create_vector_store(chunks)
        else:
            vector_store_manager.add_documents(chunks)

        # Save vector store
        vector_store_manager.save_vector_store()

        # Reinitialize RAG engine if API key is set
        if settings.openai_api_key:
            try:
                rag_engine = RAGEngine(vector_store_manager)
            except Exception as e:
                print(f"Warning: Could not initialize RAG engine: {e}")
                rag_engine = None
        else:
            print("Warning: OPENAI_API_KEY not set. RAG engine not initialized.")
            rag_engine = None

        return {
            "status": "success",
            "filename": file.filename,
            "chunks_created": len(chunks),
            "message": f"Document processed successfully with {len(chunks)} chunks"
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error processing document: {str(e)}"
        )


@app.post("/ask", response_model=AnswerResponse, tags=["QA"])
async def ask_question(request: QuestionRequest):
    """Answer a question using RAG"""
    global rag_engine

    try:
        # Check if vector store is initialized
        is_vec_initialized = vector_store_manager.is_initialized()
        print(f"Vector store initialized: {is_vec_initialized}")
        print(f"RAG engine: {rag_engine}")
        print(f"OpenAI API key set: {bool(settings.openai_api_key)}")

        if not is_vec_initialized:
            raise HTTPException(
                status_code=400,
                detail="No documents indexed yet. Please upload documents first."
            )

        # Initialize RAG engine if needed
        if rag_engine is None and settings.openai_api_key:
            try:
                if vector_store_manager.vector_store is None:
                    vector_store_manager.load_vector_store()
                rag_engine = RAGEngine(vector_store_manager)
                print("RAG engine initialized successfully")
            except Exception as e:
                print(f"Error initializing RAG engine: {e}")
                raise

        if rag_engine is None:
            raise HTTPException(
                status_code=500,
                detail="RAG engine not initialized. Check your OpenAI API key."
            )

        result = rag_engine.answer_question(request.question)

        return AnswerResponse(
            answer=result["answer"],
            sources=[
                SourceDocument(
                    content=source["content"],
                    metadata=source["metadata"]
                )
                for source in result["sources"]
            ],
            success=result["success"],
            error=result.get("error")
        )

    except HTTPException:
        raise
    except Exception as e:
        print(f"Exception in ask_question: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Error processing question: {str(e)}"
        )


@app.post("/retrieve", tags=["QA"])
async def retrieve_documents(request: QuestionRequest, k: int = 4):
    """Retrieve relevant documents for a question"""
    try:
        if not vector_store_manager.is_initialized():
            raise HTTPException(
                status_code=400,
                detail="No documents indexed yet"
            )

        if vector_store_manager.vector_store is None:
            vector_store_manager.load_vector_store()

        docs = vector_store_manager.retrieve_documents(request.question, k=k)

        return {
            "question": request.question,
            "documents": [
                {
                    "content": doc.page_content,
                    "metadata": doc.metadata
                }
                for doc in docs
            ],
            "count": len(docs)
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error retrieving documents: {str(e)}"
        )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
