"""Vector store management with FAISS"""
import os
from pathlib import Path
from typing import List
from langchain_core.documents import Document
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from config import settings


class VectorStoreManager:
    """Manage FAISS vector store for document retrieval"""

    def __init__(self, model_name: str = settings.embedding_model):
        self.embeddings = HuggingFaceEmbeddings(model_name=model_name)
        self.vector_store = None
        self.index_path = settings.faiss_index_path

        # Ensure data directory exists
        Path(settings.documents_path).mkdir(parents=True, exist_ok=True)
        Path(settings.faiss_index_path).parent.mkdir(parents=True, exist_ok=True)

    def create_vector_store(self, documents: List[Document]) -> FAISS:
        """Create a new vector store from documents"""
        if not documents:
            raise ValueError("No documents provided")

        self.vector_store = FAISS.from_documents(documents, self.embeddings)
        return self.vector_store

    def save_vector_store(self):
        """Save the vector store to disk"""
        if self.vector_store is None:
            raise ValueError("No vector store to save")

        self.vector_store.save_local(self.index_path)

    def load_vector_store(self) -> FAISS:
        """Load existing vector store from disk"""
        try:
            self.vector_store = FAISS.load_local(self.index_path, self.embeddings)
            return self.vector_store
        except Exception as e:
            raise FileNotFoundError(f"Vector store not found or corrupted: {e}")

    def add_documents(self, documents: List[Document]):
        """Add documents to existing vector store"""
        if self.vector_store is None:
            self.create_vector_store(documents)
        else:
            self.vector_store.add_documents(documents)

    def retrieve_documents(self, query: str, k: int = 4) -> List[Document]:
        """Retrieve top-k relevant documents for a query"""
        if self.vector_store is None:
            raise ValueError("Vector store not initialized")

        docs = self.vector_store.similarity_search(query, k=k)
        return docs

    def retrieve_with_scores(self, query: str, k: int = 4) -> List[tuple]:
        """Retrieve documents with relevance scores"""
        if self.vector_store is None:
            raise ValueError("Vector store not initialized")

        results = self.vector_store.similarity_search_with_score(query, k=k)
        return results

    def is_initialized(self) -> bool:
        """Check if vector store is initialized or exists on disk"""
        return self.vector_store is not None or os.path.exists(
            os.path.join(self.index_path, "index.faiss")
        )
