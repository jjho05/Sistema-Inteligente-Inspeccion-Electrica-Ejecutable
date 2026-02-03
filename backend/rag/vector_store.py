import numpy as np
from typing import List, Dict, Any, Optional
from pathlib import Path
import json
import pickle

from backend.utils.config import VECTOR_DB_PATH, TOP_K_RESULTS
from backend.rag.embeddings import EmbeddingsGenerator


class VectorStore:
    """Simple vector store using Numpy for storage and search (No-Chroma version)."""
    
    def __init__(self, persist_directory: str = VECTOR_DB_PATH):
        """Initialize vector store."""
        self.persist_directory = Path(persist_directory)
        self.persist_directory.mkdir(parents=True, exist_ok=True)
        self.data_path = self.persist_directory / "vector_data.pkl"
        
        # In-memory storage
        self.ids = []
        self.embeddings = []
        self.documents = []
        self.metadatas = []
        
        self.embeddings_generator = EmbeddingsGenerator()
        self._load()
    
    def _load(self):
        """Load data from disk if it exists."""
        if self.data_path.exists():
            try:
                with open(self.data_path, 'rb') as f:
                    data = pickle.load(f)
                    self.ids = data.get('ids', [])
                    self.embeddings = data.get('embeddings', [])
                    self.documents = data.get('documents', [])
                    self.metadatas = data.get('metadatas', [])
                print(f"✓ Loaded {len(self.ids)} chunks from local storage")
            except Exception as e:
                print(f"Error loading vector data: {e}")

    def _save(self):
        """Save data to disk."""
        try:
            with open(self.data_path, 'wb') as f:
                pickle.dump({
                    'ids': self.ids,
                    'embeddings': self.embeddings,
                    'documents': self.documents,
                    'metadatas': self.metadatas
                }, f)
        except Exception as e:
            print(f"Error saving vector data: {e}")

    def add_documents(self, documents: List[Dict[str, Any]]):
        """Add documents to the store."""
        print("Adding documents to simple vector store...")
        
        for doc in documents:
            norm_id = doc['norm_id']
            chunks = doc['chunks']
            embeddings = doc.get('embeddings', [])
            
            if not embeddings:
                continue
            
            for i, (chunk, embedding) in enumerate(zip(chunks, embeddings)):
                chunk_id = f"{norm_id}_chunk_{i}"
                
                if chunk_id not in self.ids:
                    self.ids.append(chunk_id)
                    self.embeddings.append(embedding)
                    self.documents.append(chunk)
                    self.metadatas.append({
                        'norm_id': norm_id,
                        'filename': doc['filename'],
                        'chunk_index': i,
                        'total_chunks': len(chunks)
                    })
        
        self._save()
        print(f"✓ Successfully added chunks to vector store. Total: {len(self.ids)}")
    
    def search(self, query: str, n_results: int = TOP_K_RESULTS, 
               norm_filter: Optional[str] = None) -> List[Dict[str, Any]]:
        """Search for relevant chunks using cosine similarity."""
        if not self.embeddings:
            return []

        try:
            # Generate query embedding
            query_embedding = np.array(self.embeddings_generator.generate_query_embedding(query))
            
            # Convert all embeddings to numpy array
            all_embeddings = np.array(self.embeddings)
            
            # Calculate cosine similarity manually
            # similarity = dot(A, B) / (norm(A) * norm(B))
            dot_products = np.dot(all_embeddings, query_embedding)
            norms = np.linalg.norm(all_embeddings, axis=1) * np.linalg.norm(query_embedding)
            similarities = dot_products / (norms + 1e-9)
            
            # Apply filter if provided
            filtered_indices = range(len(self.ids))
            if norm_filter:
                filtered_indices = [i for i, m in enumerate(self.metadatas) if m.get('norm_id') == norm_filter]
            
            if not filtered_indices:
                return []

            # Get top results from filtered indices
            filtered_similarities = [(i, similarities[i]) for i in filtered_indices]
            filtered_similarities.sort(key=lambda x: x[1], reverse=True)
            
            top_results = filtered_similarities[:n_results]
            
            formatted_results = []
            for idx, score in top_results:
                formatted_results.append({
                    'id': self.ids[idx],
                    'content': self.documents[idx],
                    'metadata': self.metadatas[idx],
                    'distance': float(1.0 - score)
                })
            
            return formatted_results
        except Exception as e:
            print(f"Error in search: {e}")
            return []
    
    def get_by_norm(self, norm_id: str, limit: int = 100) -> List[Dict[str, Any]]:
        """Get all chunks from a specific norm."""
        formatted_results = []
        count = 0
        for i, meta in enumerate(self.metadatas):
            if meta.get('norm_id') == norm_id:
                formatted_results.append({
                    'id': self.ids[i],
                    'content': self.documents[i],
                    'metadata': meta
                })
                count += 1
                if count >= limit:
                    break
        return formatted_results

    def count(self) -> int:
        """Get total number of chunks."""
        return len(self.ids)
    
    def is_empty(self) -> bool:
        """Check if empty."""
        return self.count() == 0
    
    def clear(self):
        """Clear all data."""
        self.ids = []
        self.embeddings = []
        self.documents = []
        self.metadatas = []
        if self.data_path.exists():
            self.data_path.unlink()
        print("✓ Vector store cleared")


def get_vector_store() -> VectorStore:
    """Get or create vector store instance."""
    return VectorStore()
