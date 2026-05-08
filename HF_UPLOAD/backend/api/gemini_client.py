"""
Gemini API client for multimodal analysis and embeddings.
Handles all interactions with Google's Gemini API using the new google-genai SDK.
"""

import os
from typing import List, Dict, Any, Optional
import base64
import io
from PIL import Image
from google import genai
from google.genai import types

from backend.utils.config import GEMINI_API_KEY, GEMINI_MODEL, GEMINI_VISION_MODEL, GEMINI_EMBEDDING_MODEL

# Configuration for safety settings
# Note: Safety settings structure changed in the new SDK
SAFETY_CONFIG = [
    types.SafetySetting(
        category=types.HarmCategory.HARM_CATEGORY_HARASSMENT,
        threshold=types.HarmBlockThreshold.BLOCK_NONE,
    ),
    types.SafetySetting(
        category=types.HarmCategory.HARM_CATEGORY_HATE_SPEECH,
        threshold=types.HarmBlockThreshold.BLOCK_NONE,
    ),
    types.SafetySetting(
        category=types.HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT,
        threshold=types.HarmBlockThreshold.BLOCK_NONE,
    ),
    types.SafetySetting(
        category=types.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT,
        threshold=types.HarmBlockThreshold.BLOCK_NONE,
    ),
]


class GeminiClient:
    """Client for interacting with Gemini API using the new google-genai SDK."""
    
    def __init__(self):
        """Initialize Gemini client with API key."""
        if not GEMINI_API_KEY:
            raise ValueError("GEMINI_API_KEY is required")
        
        # Initialize the new SDK client
        self.client = genai.Client(api_key=GEMINI_API_KEY)
        
        # Log available models to help debug
        try:
            print("Listing available models from new SDK...")
            # The new SDK list_models returns a generator of model objects
            for m in self.client.models.list():
                # Checking if it supports content generation
                if 'generateContent' in m.supported_generation_methods:
                    # m is a Model object, name is likely m.name
                    pass # We print only if needed to avoid log clutter
            print("✓ Models listed successfully")
        except Exception as e:
            print(f"Could not list models: {e}")
            
        self.text_model = GEMINI_MODEL
        self.vision_model = GEMINI_VISION_MODEL
        self.embedding_model = GEMINI_EMBEDDING_MODEL
    
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
            config = types.GenerateContentConfig(
                safety_settings=SAFETY_CONFIG,
                **kwargs
            )
            response = self.client.models.generate_content(
                model=self.text_model,
                contents=prompt,
                config=config
            )
            
            if not response.text:
                return "Error: El modelo no generó una respuesta válida (posible bloqueo o respuesta vacía)."
            return response.text
        except Exception as e:
            print(f"Error generating text: {e}")
            raise
    
    def analyze_image(self, image_path: str, prompt: str, **kwargs) -> str:
        """Analyze single image (wrapper for analyze_images)."""
        return self.analyze_images([image_path], prompt, **kwargs)

    def analyze_images(self, image_paths: List[str], prompt: str, **kwargs) -> str:
        """
        Analyze multiple images with Gemini Vision.
        
        Args:
            image_paths: List of paths to image files
            prompt: The prompt describing what to analyze
            **kwargs: Additional generation parameters
            
        Returns:
            Analysis result as text
        """
        try:
            contents = [prompt]
            opened_images = []
            
            # Load all images and convert to Parts
            for path in image_paths:
                try:
                    img = Image.open(path)
                    
                    # Gemini supported formats: JPEG, PNG, WEBP, HEIC
                    # If it's a different format (like BMP, TIFF, GIF), or we want to be safe, convert to JPEG.
                    supported_formats = ['JPEG', 'PNG', 'WEBP']
                    fmt = img.format if img.format in supported_formats else 'JPEG'
                    
                    if fmt == 'JPEG' and img.mode != 'RGB':
                        img = img.convert('RGB')
                        
                    # Convert PIL Image to bytes
                    img_byte_arr = io.BytesIO()
                    img.save(img_byte_arr, format=fmt)
                    img_bytes = img_byte_arr.getvalue()
                    
                    # Create Part with bytes and mime_type
                    mime_type = f"image/{fmt.lower()}"
                    if mime_type == "image/jpg": mime_type = "image/jpeg"
                    
                    contents.append(types.Part.from_bytes(
                        data=img_bytes,
                        mime_type=mime_type
                    ))
                    opened_images.append(img)
                except Exception as e:
                    print(f"Error loading image {path}: {e}")
            
            if len(contents) <= 1: # Only prompt
                return "Error: No se pudieron cargar las imágenes proporcionadas."
            
            # Generate content with images and prompt
            config = types.GenerateContentConfig(
                safety_settings=SAFETY_CONFIG,
                **kwargs
            )
            
            response = self.client.models.generate_content(
                model=self.vision_model,
                contents=contents,
                config=config
            )
            
            if not response.text:
                return "Error: El análisis visual no generó resultados (respuesta vacía)."
                
            return response.text
        except Exception as e:
            print(f"Error analyzing images: {e}")
            raise
        finally:
            for img in opened_images:
                try:
                    img.close()
                except:
                    pass
    
    def analyze_image_bytes(self, image_bytes: bytes, prompt: str, **kwargs) -> str:
        """
        Analyze an image from bytes with Gemini Vision.
        """
        try:
            # Determine mime type (simple check)
            mime_type = "image/jpeg" # Default
            
            contents = [
                prompt,
                types.Part.from_bytes(data=image_bytes, mime_type=mime_type)
            ]
            
            config = types.GenerateContentConfig(
                safety_settings=SAFETY_CONFIG,
                **kwargs
            )
            
            response = self.client.models.generate_content(
                model=self.vision_model,
                contents=contents,
                config=config
            )
            
            if not response.text:
                return "Error: El análisis visual de bytes no generó resultados."
                
            return response.text
        except Exception as e:
            print(f"Error analyzing image from bytes: {e}")
            raise
    
    def generate_embeddings(self, texts: List[str]) -> List[List[float]]:
        """
        Generate embeddings for a list of texts.
        """
        try:
            embeddings = []
            for text in texts:
                result = self.client.models.embed_content(
                    model=self.embedding_model,
                    contents=text,
                    config=types.EmbedContentConfig(task_type="RETRIEVAL_DOCUMENT")
                )
                embeddings.append(result.embeddings[0].values)
            return embeddings
        except Exception as e:
            print(f"Error generating embeddings: {e}")
            raise
    
    def generate_query_embedding(self, query: str) -> List[float]:
        """
        Generate embedding for a search query.
        """
        try:
            result = self.client.models.embed_content(
                model=self.embedding_model,
                contents=query,
                config=types.EmbedContentConfig(task_type="RETRIEVAL_QUERY")
            )
            return result.embeddings[0].values
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
