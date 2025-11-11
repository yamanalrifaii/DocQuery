"""RAG (Retrieval-Augmented Generation) engine"""
from typing import List, Optional
from langchain_core.documents import Document
from langchain_openai import ChatOpenAI
from vector_store import VectorStoreManager
from config import settings


class RAGEngine:
    """Retrieval-Augmented Generation for question answering"""

    def __init__(self, vector_store_manager: VectorStoreManager,
                 model_name: str = settings.model_name,
                 api_key: Optional[str] = None):
        self.vector_store_manager = vector_store_manager
        self.model_name = model_name
        self.api_key = api_key or settings.openai_api_key
        self.llm = None
        self._initialize_llm()

    def _initialize_llm(self):
        """Initialize the language model"""
        if not self.api_key:
            raise ValueError("OpenAI API key not provided")

        self.llm = ChatOpenAI(
            model_name=self.model_name,
            api_key=self.api_key,
            temperature=0.7,
            max_tokens=1024
        )

    def answer_question(self, question: str) -> dict:
        """Answer a question using RAG"""
        try:
            if not self.vector_store_manager.is_initialized():
                raise ValueError("Vector store not initialized")

            # Load vector store if not already loaded
            if self.vector_store_manager.vector_store is None:
                self.vector_store_manager.load_vector_store()

            # Retrieve relevant documents
            docs = self.vector_store_manager.retrieve_documents(question, k=4)

            if not docs:
                return {
                    "answer": "No relevant documents found to answer this question.",
                    "sources": [],
                    "success": True
                }

            # Format context from retrieved documents
            context = "\n\n".join([doc.page_content for doc in docs])

            # Create prompt
            prompt = f"""Use the following pieces of context to answer the question at the end.
If you don't know the answer, just say that you don't know, don't try to make up an answer.

Context:
{context}

Question: {question}

Answer:"""

            # Get answer from LLM
            response = self.llm.invoke(prompt)
            answer = response.content if hasattr(response, 'content') else str(response)

            return {
                "answer": answer,
                "sources": [
                    {
                        "content": doc.page_content,
                        "metadata": doc.metadata
                    }
                    for doc in docs
                ],
                "success": True
            }
        except Exception as e:
            return {
                "answer": f"Error processing question: {str(e)}",
                "sources": [],
                "success": False,
                "error": str(e)
            }

    def retrieve_relevant_documents(self, question: str, k: int = 4) -> List[Document]:
        """Retrieve documents relevant to the question without generation"""
        return self.vector_store_manager.retrieve_documents(question, k=k)

    def is_ready(self) -> bool:
        """Check if RAG engine is ready for queries"""
        return self.vector_store_manager.is_initialized()
