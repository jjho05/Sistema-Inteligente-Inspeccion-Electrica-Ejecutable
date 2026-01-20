"""
Embeddings cache manager for storing and retrieving embeddings.
Allows resuming processing and avoiding duplicate API calls.
"""

import json
import hashlib
from pathlib import Path
from typing import List, Dict, Any, Optional


class EmbeddingsCache:
    """Manages caching of embeddings to disk."""
    
    def __init__(self, cache_dir: str = "data/embeddings_cache"):
        """Initialize cache manager."""
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(parents=True, exist_ok=True)
    
    def _get_cache_key(self, text: str, norm_id: str, chunk_index: int) -> str:
        """Generate unique cache key for a chunk."""
        # Use hash of text + metadata for uniqueness
        content = f"{norm_id}_{chunk_index}_{text[:100]}"
        return hashlib.md5(content.encode()).hexdigest()
    
    def _get_cache_path(self, cache_key: str) -> Path:
        """Get file path for cache key."""
        return self.cache_dir / f"{cache_key}.json"
    
    def get(self, text: str, norm_id: str, chunk_index: int) -> Optional[List[float]]:
        """
        Get cached embedding if it exists.
        
        Args:
            text: Chunk text
            norm_id: Norm identifier
            chunk_index: Index of chunk
            
        Returns:
            Cached embedding or None
        """
        cache_key = self._get_cache_key(text, norm_id, chunk_index)
        cache_path = self._get_cache_path(cache_key)
        
        if cache_path.exists():
            try:
                with open(cache_path, 'r') as f:
                    data = json.load(f)
                    return data['embedding']
            except Exception as e:
                print(f"Warning: Error reading cache {cache_key}: {e}")
                return None
        
        return None
    
    def set(self, text: str, norm_id: str, chunk_index: int, embedding: List[float]):
        """
        Cache an embedding.
        
        Args:
            text: Chunk text
            norm_id: Norm identifier
            chunk_index: Index of chunk
            embedding: Embedding vector
        """
        cache_key = self._get_cache_key(text, norm_id, chunk_index)
        cache_path = self._get_cache_path(cache_key)
        
        try:
            data = {
                'norm_id': norm_id,
                'chunk_index': chunk_index,
                'text_preview': text[:200],
                'embedding': embedding
            }
            with open(cache_path, 'w') as f:
                json.dump(data, f)
        except Exception as e:
            print(f"Warning: Error writing cache {cache_key}: {e}")
    
    def clear(self):
        """Clear all cached embeddings."""
        import shutil
        if self.cache_dir.exists():
            shutil.rmtree(self.cache_dir)
            self.cache_dir.mkdir(parents=True, exist_ok=True)
            print("✓ Cache cleared")
    
    def get_stats(self) -> Dict[str, Any]:
        """Get cache statistics."""
        cache_files = list(self.cache_dir.glob("*.json"))
        total_size = sum(f.stat().st_size for f in cache_files)
        
        return {
            'cached_chunks': len(cache_files),
            'total_size_mb': total_size / (1024 * 1024),
            'cache_dir': str(self.cache_dir)
        }


def get_cache() -> EmbeddingsCache:
    """Get or create cache instance."""
    return EmbeddingsCache()
