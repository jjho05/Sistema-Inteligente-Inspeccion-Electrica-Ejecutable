"""
Configuration module for the electrical inspection system.
Loads environment variables and provides configuration settings.
"""

import os
from dotenv import load_dotenv
from pathlib import Path

# Load environment variables
load_dotenv()

# Base paths
BASE_DIR = Path(__file__).resolve().parent.parent.parent
DATA_DIR = BASE_DIR / "data"

# API Configuration
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")

# Paths
VECTOR_DB_PATH = os.getenv("VECTOR_DB_PATH", str(DATA_DIR / "vector_db"))
NORMAS_PATH = os.getenv("NORMAS_PATH", str(DATA_DIR / "normas"))
TEMPLATES_PATH = os.getenv("TEMPLATES_PATH", str(DATA_DIR / "templates"))
GENERATED_PATH = os.getenv("GENERATED_PATH", str(DATA_DIR / "generated"))

# Server configuration
HOST = os.getenv('HOST', '0.0.0.0')
PORT = int(os.getenv('PORT', 8080))
DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'

# RAG Configuration
CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", 1000))
CHUNK_OVERLAP = int(os.getenv("CHUNK_OVERLAP", 200))
TOP_K_RESULTS = int(os.getenv("TOP_K_RESULTS", 5))

# Gemini Model Configuration
GEMINI_MODEL = "gemini-1.5-flash-latest"
GEMINI_VISION_MODEL = "gemini-1.5-flash-latest"
GEMINI_EMBEDDING_MODEL = "gemini-embedding-001"

def validate_config():
    """Validate that all required configuration is present."""
    if not GEMINI_API_KEY:
        raise ValueError(
            "GEMINI_API_KEY not found in environment variables. "
            "Please set it in your .env file."
        )
    
    # Create directories if they don't exist
    for path in [VECTOR_DB_PATH, GENERATED_PATH]:
        Path(path).mkdir(parents=True, exist_ok=True)
    
    # Verify normas and templates exist
    if not Path(NORMAS_PATH).exists():
        raise FileNotFoundError(f"Normas directory not found: {NORMAS_PATH}")
    
    if not Path(TEMPLATES_PATH).exists():
        raise FileNotFoundError(f"Templates directory not found: {TEMPLATES_PATH}")
    
    return True
