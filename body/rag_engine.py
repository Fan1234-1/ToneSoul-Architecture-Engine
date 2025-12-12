"""
ToneSoul RAG Module - Knowledge Retrieval System
=================================================
Enables ToneSoul to query its own documentation as a knowledge base.

Features:
- Document ingestion from markdown files
- Vector embeddings using sentence-transformers
- Local ChromaDB for vector storage
- Context-aware query augmentation

Author: Antigravity + 黃梵威
Created: 2025-12-06
"""

import os
import re
import json
from pathlib import Path
from typing import List, Dict, Any, Optional
from dataclasses import dataclass


@dataclass
class Document:
    """Represents a document chunk for RAG"""
    content: str
    source: str
    metadata: Dict[str, Any]


@dataclass
class RAGConfig:
    """Configuration for RAG system"""
    collection_name: str = "tonesoul_knowledge"
    embedding_model: str = "all-MiniLM-L6-v2"  # Fast, small, good quality
    chunk_size: int = 500
    chunk_overlap: int = 50
    top_k: int = 3
    persist_directory: str = "./data/chromadb"


class DocumentProcessor:
    """Processes markdown files into chunks for embedding"""
    
    def __init__(self, config: RAGConfig):
        self.config = config
    
    def load_markdown(self, file_path: str) -> str:
        """Load a markdown file"""
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    
    def chunk_text(self, text: str, source: str) -> List[Document]:
        """Split text into overlapping chunks"""
        chunks = []
        
        # Split by paragraphs first
        paragraphs = re.split(r'\n\n+', text)
        
        current_chunk = ""
        for para in paragraphs:
            if len(current_chunk) + len(para) < self.config.chunk_size:
                current_chunk += para + "\n\n"
            else:
                if current_chunk.strip():
                    chunks.append(Document(
                        content=current_chunk.strip(),
                        source=source,
                        metadata={"type": "text"}
                    ))
                current_chunk = para + "\n\n"
        
        # Don't forget the last chunk
        if current_chunk.strip():
            chunks.append(Document(
                content=current_chunk.strip(),
                source=source,
                metadata={"type": "text"}
            ))
        
        return chunks
    
    def process_directory(self, directory: str, extensions: List[str] = [".md"]) -> List[Document]:
        """Process all matching files in a directory"""
        documents = []
        
        for ext in extensions:
            for file_path in Path(directory).rglob(f"*{ext}"):
                # Skip node_modules, .git, etc.
                if any(skip in str(file_path) for skip in [".git", "node_modules", "__pycache__", ".venv"]):
                    continue
                
                try:
                    content = self.load_markdown(str(file_path))
                    relative_path = str(file_path.relative_to(directory))
                    chunks = self.chunk_text(content, relative_path)
                    documents.extend(chunks)
                    print(f"  ✅ Processed: {relative_path} ({len(chunks)} chunks)")
                except Exception as e:
                    print(f"  ⚠️ Failed: {file_path} - {e}")
        
        return documents


class RAGEngine:
    """Main RAG engine for ToneSoul"""
    
    def __init__(self, config: Optional[RAGConfig] = None):
        self.config = config or RAGConfig()
        self.collection = None
        self.embedding_fn = None
        self._initialized = False
    
    def _lazy_init(self):
        """Lazy initialization of heavy dependencies"""
        if self._initialized:
            return
        
        try:
            import chromadb
            from chromadb.utils import embedding_functions
            
            # Create persistent client
            os.makedirs(self.config.persist_directory, exist_ok=True)
            self.client = chromadb.PersistentClient(path=self.config.persist_directory)
            
            # Use sentence-transformers for embeddings
            self.embedding_fn = embedding_functions.SentenceTransformerEmbeddingFunction(
                model_name=self.config.embedding_model
            )
            
            # Get or create collection
            self.collection = self.client.get_or_create_collection(
                name=self.config.collection_name,
                embedding_function=self.embedding_fn,
                metadata={"description": "ToneSoul knowledge base"}
            )
            
            self._initialized = True
            print(f"[RAG] Initialized with {self.collection.count()} documents")
            
        except ImportError as e:
            print(f"[RAG] Warning: Dependencies not installed - {e}")
            print("[RAG] Run: pip install chromadb sentence-transformers")
            raise
    
    def ingest_documents(self, documents: List[Document]):
        """Add documents to the vector store"""
        self._lazy_init()
        
        if not documents:
            print("[RAG] No documents to ingest")
            return
        
        # Prepare data for ChromaDB
        ids = [f"doc_{i}" for i in range(len(documents))]
        contents = [doc.content for doc in documents]
        metadatas = [{"source": doc.source, **doc.metadata} for doc in documents]
        
        # Add to collection (will upsert if IDs exist)
        self.collection.add(
            ids=ids,
            documents=contents,
            metadatas=metadatas
        )
        
        print(f"[RAG] Ingested {len(documents)} document chunks")
    
    def query(self, query_text: str, n_results: Optional[int] = None) -> List[Dict]:
        """Query the knowledge base and return relevant documents"""
        self._lazy_init()
        
        n = n_results or self.config.top_k
        
        results = self.collection.query(
            query_texts=[query_text],
            n_results=n
        )
        
        # Format results
        formatted = []
        if results and results['documents']:
            for i, doc in enumerate(results['documents'][0]):
                formatted.append({
                    "content": doc,
                    "source": results['metadatas'][0][i].get('source', 'unknown'),
                    "distance": results['distances'][0][i] if results.get('distances') else None
                })
        
        return formatted
    
    def augment_prompt(self, user_query: str, system_prompt: str = "") -> str:
        """Augment the prompt with relevant context from knowledge base"""
        results = self.query(user_query)
        
        if not results:
            return system_prompt
        
        # Build context section
        context_parts = []
        for i, result in enumerate(results, 1):
            context_parts.append(f"[Reference {i} from {result['source']}]\n{result['content']}")
        
        context = "\n\n---\n\n".join(context_parts)
        
        augmented = f"""{system_prompt}

## Retrieved Knowledge Context
The following information was retrieved from the ToneSoul knowledge base and may be relevant:

{context}

---

Use this context to inform your response, but don't just copy it. Synthesize and apply it appropriately."""
        
        return augmented
    
    def get_stats(self) -> Dict[str, Any]:
        """Get statistics about the knowledge base"""
        self._lazy_init()
        
        return {
            "collection_name": self.config.collection_name,
            "document_count": self.collection.count(),
            "embedding_model": self.config.embedding_model,
            "persist_directory": self.config.persist_directory
        }


def build_knowledge_base(source_dir: str, config: Optional[RAGConfig] = None):
    """Helper function to build complete knowledge base from a directory"""
    config = config or RAGConfig()
    
    print("[RAG] Building ToneSoul Knowledge Base")
    print(f"[RAG] Source: {source_dir}")
    print(f"[RAG] Persist: {config.persist_directory}")
    print()
    
    # Process documents
    processor = DocumentProcessor(config)
    documents = processor.process_directory(source_dir)
    
    print(f"\n[RAG] Total chunks: {len(documents)}")
    
    # Create engine and ingest
    engine = RAGEngine(config)
    engine.ingest_documents(documents)
    
    print(f"\n[RAG] Knowledge base ready! Stats: {engine.get_stats()}")
    
    return engine


if __name__ == "__main__":
    # Build knowledge base from ToneSoul docs
    import sys
    
    source = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    print(f"Building knowledge base from: {source}")
    
    try:
        engine = build_knowledge_base(source)
        
        # Test query
        print("\n" + "="*50)
        print("Testing query: 'What are the 7 axioms?'")
        print("="*50 + "\n")
        
        results = engine.query("What are the 7 axioms of ToneSoul?")
        for i, r in enumerate(results, 1):
            print(f"[Result {i}] Source: {r['source']}")
            print(f"  {r['content'][:200]}...")
            print()
            
    except ImportError:
        print("\n❌ Dependencies not installed!")
        print("Run: pip install chromadb sentence-transformers")
