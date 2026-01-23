"""
Gemini API client for multimodal analysis and embeddings.
Handles all interactions with Google's Gemini API.
"""

import google.generativeai as genai
from typing import List, Dict, Any, Optional
import base64
from PIL import Image
import io

from backend.utils.config import GEMINI_API_KEY, GEMINI_MODEL, GEMINI_VISION_MODEL, GEMINI_EMBEDDING_MODEL

# Safety settings to avoid false positives in technical analysis
SAFETY_SETTINGS = [
    {
        "category": "HARM_CATEGORY_HARASSMENT",
        "threshold": "BLOCK_NONE",
    },
    {
        "category": "HARM_CATEGORY_HATE_SPEECH",
        "threshold": "BLOCK_NONE",
    },
    {
        "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
        "threshold": "BLOCK_NONE",
    },
    {
        "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
        "threshold": "BLOCK_NONE",
    },
]


class GeminiClient:
    """Client for interacting with Gemini API."""
    
    def __init__(self):
        """Initialize Gemini client with API key."""
        if not GEMINI_API_KEY:
            raise ValueError("GEMINI_API_KEY is required")
        
        genai.configure(api_key=GEMINI_API_KEY)
        
        # Log available models to help debug 404 errors
        try:
            print("Available models:")
            for m in genai.list_models():
                if 'generateContent' in m.supported_generation_methods:
                    print(f" - {m.name}")
        except Exception as e:
            print(f"Could not list models: {e}")
            
        self.model = genai.GenerativeModel(GEMINI_MODEL)
        self.vision_model = genai.GenerativeModel(GEMINI_VISION_MODEL)
    
    def generate_text(self, prompt: str, **kwargs) -> str:
        """
        Generate text using Gemini.
        
        Args:
            prompt: The prompt to send to Gemini
            **kwargs: Additional generation parameters
            
        Returns:
            Generated text response
        """
        try:
            response = self.model.generate_content(
                prompt, 
                safety_settings=SAFETY_SETTINGS,
                **kwargs
            )
            if not response.candidates or not response.candidates[0].content.parts:
                return "Error: El modelo no generó una respuesta válida (posible bloqueo o respuesta vacía)."
            return response.text
        except Exception as e:
            print(f"Error generating text: {e}")
            raise
    
    def analyze_image(self, image_path: str, prompt: str, **kwargs) -> str:
        """
        Analyze an image with Gemini Vision.
        
        Args:
            image_path: Path to the image file
            prompt: The prompt describing what to analyze
            **kwargs: Additional generation parameters
            
        Returns:
            Analysis result as text
        """
        try:
            # Load and prepare image
            image = Image.open(image_path)
            
            # Generate content with image and prompt
            response = self.vision_model.generate_content(
                [prompt, image], 
                safety_settings=SAFETY_SETTINGS,
                **kwargs
            )
            
            if not response.candidates or not response.candidates[0].content.parts:
                # Check for blocking
                if response.prompt_feedback:
                    return f"Error: La imagen fue bloqueada por el filtro de seguridad. Feedback: {response.prompt_feedback}"
                return "Error: El análisis visual no generó resultados (respuesta vacía)."
                
            return response.text
        except Exception as e:
            print(f"Error analyzing image: {e}")
            raise
    
    def analyze_image_bytes(self, image_bytes: bytes, prompt: str, **kwargs) -> str:
        """
        Analyze an image from bytes with Gemini Vision.
        
        Args:
            image_bytes: Image data as bytes
            prompt: The prompt describing what to analyze
            **kwargs: Additional generation parameters
            
        Returns:
            Analysis result as text
        """
        try:
            # Load image from bytes
            image = Image.open(io.BytesIO(image_bytes))
            
            # Generate content with image and prompt
            response = self.vision_model.generate_content(
                [prompt, image], 
                safety_settings=SAFETY_SETTINGS,
                **kwargs
            )
            
            if not response.candidates or not response.candidates[0].content.parts:
                if response.prompt_feedback:
                    return f"Error: La imagen fue bloqueada por el filtro de seguridad (bytes). Feedback: {response.prompt_feedback}"
                return "Error: El análisis visual de bytes no generó resultados (respuesta vacía)."
                
            return response.text
        except Exception as e:
            print(f"Error analyzing image from bytes: {e}")
            raise
    
    def generate_embeddings(self, texts: List[str]) -> List[List[float]]:
        """
        Generate embeddings for a list of texts.
        
        Args:
            texts: List of text strings to embed
            
        Returns:
            List of embedding vectors
        """
        try:
            embeddings = []
            for text in texts:
                result = genai.embed_content(
                    model=GEMINI_EMBEDDING_MODEL,
                    content=text,
                    task_type="retrieval_document"
                )
                embeddings.append(result['embedding'])
            return embeddings
        except Exception as e:
            print(f"Error generating embeddings: {e}")
            raise
    
    def generate_query_embedding(self, query: str) -> List[float]:
        """
        Generate embedding for a search query.
        
        Args:
            query: Query text to embed
            
        Returns:
            Embedding vector
        """
        try:
            result = genai.embed_content(
                model=GEMINI_EMBEDDING_MODEL,
                content=query,
                task_type="retrieval_query"
            )
            return result['embedding']
        except Exception as e:
            print(f"Error generating query embedding: {e}")
            raise


# Singleton instance
_client = None

def get_gemini_client() -> GeminiClient:
    """Get or create Gemini client singleton."""
    global _client
    if _client is None:
        _client = GeminiClient()
    return _client
