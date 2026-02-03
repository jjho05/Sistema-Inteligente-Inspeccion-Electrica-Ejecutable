"""
Local embeddings generator using Sentence Transformers.
Provides offline, unlimited embeddings without API calls.
"""

from typing import List
from sentence_transformers import SentenceTransformer


class LocalEmbeddingsGenerator:
    """Generates embeddings using local Sentence Transformers model."""
    
    def __init__(self, model_name: str = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"):
        """
        Initialize local embeddings generator.
        
        Args:
            model_name: Name of the Sentence Transformers model
        """
        print(f"Loading local embeddings model: {model_name}")
        print("(This may take a few minutes on first run...)")
        
        self.model = SentenceTransformer(model_name)
        
        print(f"✓ Model loaded successfully")
        print(f"  Embedding dimension: {self.model.get_sentence_embedding_dimension()}")
    
    def generate_embeddings(self, texts: List[str]) -> List[List[float]]:
        """
        Generate embeddings for a list of texts.
        
        Args:
            texts: List of text strings
            
        Returns:
            List of embedding vectors
        """
        embeddings = self.model.encode(texts, show_progress_bar=False)
        return embeddings.tolist()
    
    def generate_query_embedding(self, query: str) -> List[float]:
        """
        Generate embedding for a single query.
        
        Args:
            query: Query text
            
        Returns:
            Embedding vector
        """
        embedding = self.model.encode([query], show_progress_bar=False)
        return embedding[0].tolist()


def get_local_embeddings_generator() -> LocalEmbeddingsGenerator:
    """Get or create local embeddings generator instance."""
    return LocalEmbeddingsGenerator()
