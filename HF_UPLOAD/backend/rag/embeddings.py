"""
Embeddings generator for RAG system.
Uses local Sentence Transformers for unlimited, offline embeddings.
"""

from typing import List, Dict, Any
from backend.rag.local_embeddings import get_local_embeddings_generator


class EmbeddingsGenerator:
    """Generates embeddings for text chunks using local model."""
    
    def __init__(self):
        """Initialize embeddings generator with local model."""
        self.generator = get_local_embeddings_generator()
    
    def generate_embeddings(self, texts: List[str]) -> List[List[float]]:
        """
        Generate embeddings for a list of texts.
        
        Args:
            texts: List of text strings
            
        Returns:
            List of embedding vectors
        """
        return self.generator.generate_embeddings(texts)
    
    def generate_query_embedding(self, query: str) -> List[float]:
        """
        Generate embedding for a single query.
        
        Args:
            query: Query text
            
        Returns:
            Embedding vector
        """
        return self.generator.generate_query_embedding(query)
    
    def generate_document_embeddings(self, documents: List[Dict[str, Any]], 
                                     use_cache: bool = True) -> List[Dict[str, Any]]:
        """
        Generate embeddings for processed documents with caching support.
        
        Args:
            documents: List of processed documents from PDF processor
            use_cache: Whether to use cache (default: True)
            
        Returns:
            Documents with embeddings added
        """
        import time
        from backend.rag.embeddings_cache import get_cache
        
        cache = get_cache() if use_cache else None
        
        print("Generating embeddings for documents...")
        if cache:
            stats = cache.get_stats()
            print(f"Cache: {stats['cached_chunks']} chunks cached ({stats['total_size_mb']:.2f} MB)")
        
        # Rate limiting for free tier: 100 requests/minute
        requests_per_minute = 100
        delay_between_batches = 60.0 / requests_per_minute  # ~0.6 seconds
        
        for doc in documents:
            chunks = doc['chunks']
            norm_id = doc['norm_id']
            print(f"\nProcessing {doc['filename']}: {len(chunks)} chunks...")
            
            # Generate embeddings in batches (larger batch = faster processing)
            batch_size = 100
            all_embeddings = []
            cache_hits = 0
            api_calls = 0
            
            for i in range(0, len(chunks), batch_size):
                batch = chunks[i:i + batch_size]
                batch_embeddings = []
                texts_to_embed = []
                indices_to_embed = []
                
                # Check cache first
                for j, text in enumerate(batch):
                    chunk_idx = i + j
                    
                    if cache:
                        cached_embedding = cache.get(text, norm_id, chunk_idx)
                        if cached_embedding:
                            batch_embeddings.append(cached_embedding)
                            cache_hits += 1
                            continue
                    
                    # Not in cache, need to generate
                    texts_to_embed.append(text)
                    indices_to_embed.append(chunk_idx)
                    batch_embeddings.append(None)  # Placeholder
                
                # Generate embeddings for uncached texts
                if texts_to_embed:
                    try:
                        new_embeddings = self.generate_embeddings(texts_to_embed)
                        api_calls += len(texts_to_embed)
                        
                        # Fill in the placeholders and cache
                        new_emb_idx = 0
                        for j, emb in enumerate(batch_embeddings):
                            if emb is None:  # Was a placeholder
                                embedding = new_embeddings[new_emb_idx]
                                batch_embeddings[j] = embedding
                                
                                # Cache it
                                if cache:
                                    chunk_idx = indices_to_embed[new_emb_idx]
                                    cache.set(batch[j], norm_id, chunk_idx, embedding)
                                
                                new_emb_idx += 1
                        
                        # Rate limiting: wait between batches
                        if i + batch_size < len(chunks):
                            time.sleep(delay_between_batches * len(texts_to_embed))
                            
                    except Exception as e:
                        if "429" in str(e) or "quota" in str(e).lower():
                            # Rate limit hit, wait longer
                            print(f"\n⚠️  Rate limit reached. Waiting 60 seconds...")
                            time.sleep(60)
                            # Retry this batch
                            try:
                                new_embeddings = self.generate_embeddings(texts_to_embed)
                                api_calls += len(texts_to_embed)
                                
                                # Fill in and cache
                                new_emb_idx = 0
                                for j, emb in enumerate(batch_embeddings):
                                    if emb is None:
                                        embedding = new_embeddings[new_emb_idx]
                                        batch_embeddings[j] = embedding
                                        if cache:
                                            chunk_idx = indices_to_embed[new_emb_idx]
                                            cache.set(batch[j], norm_id, chunk_idx, embedding)
                                        new_emb_idx += 1
                            except Exception as retry_error:
                                print(f"✗ Error even after retry: {retry_error}")
                                raise
                        else:
                            raise
                
                all_embeddings.extend(batch_embeddings)
                
                # Progress update
                if (i // batch_size + 1) % 5 == 0 or i + batch_size >= len(chunks):
                    progress = min(i + batch_size, len(chunks))
                    print(f"  Progress: {progress}/{len(chunks)} chunks "
                          f"(Cache: {cache_hits}, API: {api_calls})")
            
            doc['embeddings'] = all_embeddings
            print(f"✓ Completed {doc['filename']}: {cache_hits} from cache, {api_calls} API calls")
        
        return documents


def generate_embeddings_for_documents(documents: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Convenience function to generate embeddings."""
    generator = EmbeddingsGenerator()
    return generator.generate_document_embeddings(documents)
