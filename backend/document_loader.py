"""Document loading and processing module"""
import os
from pathlib import Path
from typing import List
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain_core.documents import Document
from config import settings


class DocumentProcessor:
    """Handle document loading, parsing, and chunking"""

    def __init__(self, chunk_size: int = settings.chunk_size,
                 chunk_overlap: int = settings.chunk_overlap):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            separators=["\n\n", "\n", " ", ""]
        )

    def load_document(self, file_path: str) -> List[Document]:
        """Load a document from file path"""
        path = Path(file_path)

        if not path.exists():
            raise FileNotFoundError(f"Document not found: {file_path}")

        if path.suffix.lower() == ".pdf":
            loader = PyPDFLoader(file_path)
        elif path.suffix.lower() in [".txt", ".md"]:
            loader = TextLoader(file_path)
        else:
            raise ValueError(f"Unsupported file type: {path.suffix}")

        documents = loader.load()
        return documents

    def process_documents(self, documents: List[Document]) -> List[Document]:
        """Split documents into chunks"""
        chunks = self.text_splitter.split_documents(documents)
        return chunks

    def load_and_process(self, file_path: str) -> List[Document]:
        """Load and process a document in one step"""
        documents = self.load_document(file_path)
        chunks = self.process_documents(documents)
        return chunks

    def batch_process_directory(self, directory: str) -> List[Document]:
        """Process all documents in a directory"""
        all_chunks = []
        dir_path = Path(directory)

        if not dir_path.exists():
            return all_chunks

        for file_path in dir_path.glob("*"):
            if file_path.is_file() and file_path.suffix.lower() in [".pdf", ".txt", ".md"]:
                try:
                    chunks = self.load_and_process(str(file_path))
                    all_chunks.extend(chunks)
                except Exception as e:
                    print(f"Error processing {file_path}: {e}")

        return all_chunks
