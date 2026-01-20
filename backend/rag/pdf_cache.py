"""
PDF text extraction cache to avoid reprocessing PDFs.
Stores extracted text and chunks for faster subsequent runs.
"""

import json
import hashlib
from pathlib import Path
from typing import Dict, Any, Optional


class PDFCache:
    """Manages caching of extracted PDF text and chunks."""
    
    def __init__(self, cache_dir: str = "data/pdf_cache"):
        """Initialize PDF cache manager."""
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(parents=True, exist_ok=True)
    
    def _get_file_hash(self, pdf_path: str) -> str:
        """Generate hash of PDF file for cache key."""
        path = Path(pdf_path)
        
        # Use file size and modification time for quick hash
        stat = path.stat()
        content = f"{path.name}_{stat.st_size}_{stat.st_mtime}"
        
        return hashlib.md5(content.encode()).hexdigest()
    
    def _get_cache_path(self, pdf_path: str) -> Path:
        """Get cache file path for PDF."""
        file_hash = self._get_file_hash(pdf_path)
        return self.cache_dir / f"{file_hash}.json"
    
    def get(self, pdf_path: str) -> Optional[Dict[str, Any]]:
        """
        Get cached PDF data if it exists.
        
        Args:
            pdf_path: Path to PDF file
            
        Returns:
            Cached data or None
        """
        cache_path = self._get_cache_path(pdf_path)
        
        if cache_path.exists():
            try:
                with open(cache_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    return data
            except Exception as e:
                print(f"Warning: Error reading PDF cache: {e}")
                return None
        
        return None
    
    def set(self, pdf_path: str, data: Dict[str, Any]):
        """
        Cache PDF extraction data.
        
        Args:
            pdf_path: Path to PDF file
            data: Extracted data (text, chunks, metadata)
        """
        cache_path = self._get_cache_path(pdf_path)
        
        try:
            with open(cache_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"Warning: Error writing PDF cache: {e}")
    
    def clear(self):
        """Clear all cached PDF data."""
        import shutil
        if self.cache_dir.exists():
            shutil.rmtree(self.cache_dir)
            self.cache_dir.mkdir(parents=True, exist_ok=True)
            print("✓ PDF cache cleared")
    
    def get_stats(self) -> Dict[str, Any]:
        """Get cache statistics."""
        cache_files = list(self.cache_dir.glob("*.json"))
        total_size = sum(f.stat().st_size for f in cache_files)
        
        return {
            'cached_pdfs': len(cache_files),
            'total_size_mb': total_size / (1024 * 1024),
            'cache_dir': str(self.cache_dir)
        }


def get_pdf_cache() -> PDFCache:
    """Get or create PDF cache instance."""
    return PDFCache()
