"""
PDF processor for extracting and structuring content from regulatory documents.
Processes NOM and NMX documents into chunks suitable for RAG.
"""

import PyPDF2
import pdfplumber
from pathlib import Path
from typing import List, Dict, Any
import re

from backend.utils.config import NORMAS_PATH, CHUNK_SIZE, CHUNK_OVERLAP


class PDFProcessor:
    """Processes PDF documents and extracts structured content."""
    
    def __init__(self, normas_path: str = NORMAS_PATH):
        """Initialize PDF processor."""
        self.normas_path = Path(normas_path)
        if not self.normas_path.exists():
            raise FileNotFoundError(f"Normas directory not found: {normas_path}")
    
    def get_pdf_files(self) -> List[Path]:
        """Get all PDF files in the normas directory."""
        return list(self.normas_path.glob("*.pdf"))
    
    def extract_text_pypdf(self, pdf_path: Path) -> str:
        """
        Extract text from PDF using PyPDF2.
        
        Args:
            pdf_path: Path to PDF file
            
        Returns:
            Extracted text
        """
        text = ""
        try:
            with open(pdf_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                for page in pdf_reader.pages:
                    text += page.extract_text() + "\n"
        except Exception as e:
            print(f"Error extracting text with PyPDF2 from {pdf_path}: {e}")
        return text
    
    def extract_text_pdfplumber(self, pdf_path: Path) -> str:
        """
        Extract text from PDF using pdfplumber (better for complex layouts).
        
        Args:
            pdf_path: Path to PDF file
            
        Returns:
            Extracted text
        """
        text = ""
        try:
            with pdfplumber.open(pdf_path) as pdf:
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"
        except Exception as e:
            print(f"Error extracting text with pdfplumber from {pdf_path}: {e}")
        return text
    
    def extract_text(self, pdf_path: Path) -> str:
        """
        Extract text from PDF using best available method.
        
        Args:
            pdf_path: Path to PDF file
            
        Returns:
            Extracted text
        """
        # Try pdfplumber first (better quality)
        text = self.extract_text_pdfplumber(pdf_path)
        
        # Fallback to PyPDF2 if pdfplumber fails
        if not text or len(text) < 100:
            text = self.extract_text_pypdf(pdf_path)
        
        return text
    
    def identify_norm_type(self, filename: str) -> str:
        """
        Identify the type of norm from filename.
        
        Args:
            filename: Name of the PDF file
            
        Returns:
            Norm identifier (e.g., 'NOM-001-SEDE-2012')
        """
        # Extract norm identifier from filename
        patterns = [
            r'NOM-\d+-[A-Z]+-\d+',
            r'NMX-[A-Z]-\d+-[A-Z]+-\d+',
            r'NOM-\d+-SEDE-\d+'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, filename, re.IGNORECASE)
            if match:
                return match.group(0).upper()
        
        return filename
    
    def chunk_text(self, text: str, chunk_size: int = CHUNK_SIZE, 
                   overlap: int = CHUNK_OVERLAP) -> List[str]:
        """
        Split text into overlapping chunks.
        
        Args:
            text: Text to chunk
            chunk_size: Size of each chunk in characters
            overlap: Overlap between chunks
            
        Returns:
            List of text chunks
        """
        chunks = []
        start = 0
        text_length = len(text)
        
        while start < text_length:
            end = start + chunk_size
            chunk = text[start:end]
            
            # Try to break at sentence boundary
            if end < text_length:
                last_period = chunk.rfind('.')
                last_newline = chunk.rfind('\n')
                break_point = max(last_period, last_newline)
                
                if break_point > chunk_size * 0.5:  # Only if break point is reasonable
                    chunk = chunk[:break_point + 1]
                    end = start + break_point + 1
            
            chunks.append(chunk.strip())
            start = end - overlap
        
        return chunks
    
    def extract_articles(self, text: str) -> List[Dict[str, Any]]:
        """
        Extract article sections from normative text.
        
        Args:
            text: Full text of the norm
            
        Returns:
            List of dictionaries with article information
        """
        articles = []
        
        # Pattern to match article headers (e.g., "Artículo 110", "110-", "110.")
        article_pattern = r'(?:Artículo\s+)?(\d+(?:\.\d+)?(?:-\d+)?)[.\s:-]'
        
        matches = list(re.finditer(article_pattern, text, re.IGNORECASE))
        
        for i, match in enumerate(matches):
            article_num = match.group(1)
            start = match.start()
            
            # Find end of this article (start of next article or end of text)
            if i < len(matches) - 1:
                end = matches[i + 1].start()
            else:
                end = len(text)
            
            article_text = text[start:end].strip()
            
            # Only include if article has substantial content
            if len(article_text) > 50:
                articles.append({
                    'article_number': article_num,
                    'content': article_text
                })
        
        return articles
    
    def process_pdf(self, pdf_path: Path, use_cache: bool = True) -> Dict[str, Any]:
        """
        Process a single PDF file and extract structured content.
        
        Args:
            pdf_path: Path to PDF file
            use_cache: Whether to use cache (default: True)
            
        Returns:
            Dictionary with processed content
        """
        from backend.rag.pdf_cache import get_pdf_cache
        
        cache = get_pdf_cache() if use_cache else None
        
        # Check cache first
        if cache:
            cached_data = cache.get(str(pdf_path))
            if cached_data:
                print(f"✓ Loaded {pdf_path.name} from cache ({cached_data['num_chunks']} chunks)")
                return cached_data
        
        print(f"Processing {pdf_path.name}...")
        
        # Extract text
        text = self.extract_text(pdf_path)
        
        # Identify norm
        norm_id = self.identify_norm_type(pdf_path.name)
        
        # Extract articles
        articles = self.extract_articles(text)
        
        # Create chunks
        chunks = self.chunk_text(text)
        
        result = {
            'filename': pdf_path.name,
            'norm_id': norm_id,
            'full_text': text,
            'articles': articles,
            'chunks': chunks,
            'num_articles': len(articles),
            'num_chunks': len(chunks)
        }
        
        # Cache the result
        if cache:
            cache.set(str(pdf_path), result)
        
        return result
    
    def process_all_pdfs(self) -> List[Dict[str, Any]]:
        """
        Process all PDF files in the normas directory.
        
        Returns:
            List of processed documents
        """
        pdf_files = self.get_pdf_files()
        print(f"Found {len(pdf_files)} PDF files to process")
        
        processed_docs = []
        for pdf_path in pdf_files:
            try:
                doc = self.process_pdf(pdf_path)
                processed_docs.append(doc)
                print(f"✓ Processed {pdf_path.name}: {doc['num_chunks']} chunks, {doc['num_articles']} articles")
            except Exception as e:
                print(f"✗ Error processing {pdf_path.name}: {e}")
        
        return processed_docs


def process_normas() -> List[Dict[str, Any]]:
    """Convenience function to process all normas."""
    processor = PDFProcessor()
    return processor.process_all_pdfs()
