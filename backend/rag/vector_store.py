"""
Vector store for semantic search using ChromaDB.
Stores and retrieves normative document chunks based on similarity.
"""

import chromadb
from chromadb.config import Settings
from typing import List, Dict, Any, Optional
from pathlib import Path
import json

from backend.utils.config import VECTOR_DB_PATH, TOP_K_RESULTS
from backend.rag.embeddings import EmbeddingsGenerator


class VectorStore:
    """Vector database for storing and searching document embeddings."""
    
    def __init__(self, persist_directory: str = VECTOR_DB_PATH):
        """
        Initialize vector store.
        
        Args:
            persist_directory: Directory to persist the database
        """
        self.persist_directory = Path(persist_directory)
        self.persist_directory.mkdir(parents=True, exist_ok=True)
        
        # Initialize ChromaDB client
        self.client = chromadb.PersistentClient(
            path=str(self.persist_directory)
        )
        
        # Get or create collection
        self.collection = self.client.get_or_create_collection(
            name="normas_electricas",
            metadata={"description": "Normativa eléctrica mexicana"}
        )
        
        self.embeddings_generator = EmbeddingsGenerator()
    
    def add_documents(self, documents: List[Dict[str, Any]]):
        """
        Add documents to the vector store.
        
        Args:
            documents: List of processed documents with embeddings
        """
        print("Adding documents to vector store...")
        
        all_ids = []
        all_embeddings = []
        all_documents = []
        all_metadatas = []
        
        for doc in documents:
            norm_id = doc['norm_id']
            chunks = doc['chunks']
            embeddings = doc.get('embeddings', [])
            
            if not embeddings:
                print(f"Warning: No embeddings found for {doc['filename']}, skipping...")
                continue
            
            for i, (chunk, embedding) in enumerate(zip(chunks, embeddings)):
                chunk_id = f"{norm_id}_chunk_{i}"
                
                all_ids.append(chunk_id)
                all_embeddings.append(embedding)
                all_documents.append(chunk)
                all_metadatas.append({
                    'norm_id': norm_id,
                    'filename': doc['filename'],
                    'chunk_index': i,
                    'total_chunks': len(chunks)
                })
        
        # Add to collection in batches
        batch_size = 100
        for i in range(0, len(all_ids), batch_size):
            end_idx = min(i + batch_size, len(all_ids))
            
            self.collection.add(
                ids=all_ids[i:end_idx],
                embeddings=all_embeddings[i:end_idx],
                documents=all_documents[i:end_idx],
                metadatas=all_metadatas[i:end_idx]
            )
            
            print(f"Added batch {i // batch_size + 1}: {end_idx - i} chunks")
        
        print(f"✓ Successfully added {len(all_ids)} chunks to vector store")
    
    def search(self, query: str, n_results: int = TOP_K_RESULTS, 
               norm_filter: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Search for relevant document chunks.
        
        Args:
            query: Search query
            n_results: Number of results to return
            norm_filter: Optional filter by norm ID (e.g., 'NOM-001-SEDE-2012')
            
        Returns:
            List of search results with content and metadata
        """
        # Generate query embedding
        query_embedding = self.embeddings_generator.generate_query_embedding(query)
        
        # Prepare where filter
        where_filter = None
        if norm_filter:
            where_filter = {"norm_id": norm_filter}
        
        # Search
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=n_results,
            where=where_filter
        )
        
        # Format results
        formatted_results = []
        if results['ids'] and len(results['ids']) > 0:
            for i in range(len(results['ids'][0])):
                formatted_results.append({
                    'id': results['ids'][0][i],
                    'content': results['documents'][0][i],
                    'metadata': results['metadatas'][0][i],
                    'distance': results['distances'][0][i] if 'distances' in results else None
                })
        
        return formatted_results
    
    def get_by_norm(self, norm_id: str, limit: int = 100) -> List[Dict[str, Any]]:
        """
        Get all chunks from a specific norm.
        
        Args:
            norm_id: Norm identifier
            limit: Maximum number of chunks to return
            
        Returns:
            List of chunks from the specified norm
        """
        results = self.collection.get(
            where={"norm_id": norm_id},
            limit=limit
        )
        
        formatted_results = []
        if results['ids']:
            for i in range(len(results['ids'])):
                formatted_results.append({
                    'id': results['ids'][i],
                    'content': results['documents'][i],
                    'metadata': results['metadatas'][i]
                })
        
        return formatted_results
    
    def count(self) -> int:
        """Get total number of chunks in the vector store."""
        return self.collection.count()
    
    def is_empty(self) -> bool:
        """Check if vector store is empty."""
        return self.count() == 0
    
    def clear(self):
        """Clear all data from the vector store."""
        self.client.delete_collection("normas_electricas")
        self.collection = self.client.get_or_create_collection(
            name="normas_electricas",
            metadata={"description": "Normativa eléctrica mexicana"}
        )
        print("✓ Vector store cleared")


def get_vector_store() -> VectorStore:
    """Get or create vector store instance."""
    return VectorStore()
