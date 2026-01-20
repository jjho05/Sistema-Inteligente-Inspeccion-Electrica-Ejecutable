"""
Setup script for initial configuration and database initialization.
Runs on first execution to prepare the system.
"""

import sys
from pathlib import Path

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent))

from backend.utils.config import validate_config, VECTOR_DB_PATH, NORMAS_PATH, TEMPLATES_PATH
from backend.rag.pdf_processor import process_normas
from backend.rag.embeddings import generate_embeddings_for_documents
from backend.rag.vector_store import get_vector_store


def setup_directories():
    """Create necessary directories."""
    print("=== Setting up directories ===")
    
    directories = [
        VECTOR_DB_PATH,
        "data/generated",
        "data/examples"
    ]
    
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
        print(f"✓ {directory}")


def check_normas():
    """Check if normas PDFs exist."""
    print("\n=== Checking normas ===")
    
    normas_path = Path(NORMAS_PATH)
    pdf_files = list(normas_path.glob("*.pdf"))
    
    if not pdf_files:
        print("⚠️  No PDF files found in data/normas/")
        print("Please add normative PDF files to data/normas/")
        return False
    
    print(f"✓ Found {len(pdf_files)} PDF files:")
    for pdf in pdf_files:
        print(f"  - {pdf.name}")
    
    return True


def check_template():
    """Check if Word template exists."""
    print("\n=== Checking template ===")
    
    template_path = Path(TEMPLATES_PATH) / "DictamenElectricoPlantilla.docx"
    
    if not template_path.exists():
        print("⚠️  Template not found: DictamenElectricoPlantilla.docx")
        print("Please add the template to data/templates/")
        return False
    
    print(f"✓ Template found: {template_path.name}")
    return True


def initialize_vector_database():
    """Initialize vector database with normative documents."""
    print("\n=== Initializing vector database ===")
    
    # Check if already initialized
    vector_store = get_vector_store()
    if not vector_store.is_empty():
        print(f"✓ Vector database already initialized ({vector_store.count()} chunks)")
        return True
    
    print("Processing normative documents...")
    
    try:
        # Process PDFs
        print("\n[1/3] Extracting text from PDFs...")
        documents = process_normas()
        
        if not documents:
            print("✗ No documents processed")
            return False
        
        # Generate embeddings
        print("\n[2/3] Generating embeddings...")
        documents_with_embeddings = generate_embeddings_for_documents(documents)
        
        # Add to vector store
        print("\n[3/3] Adding to vector database...")
        vector_store.add_documents(documents_with_embeddings)
        
        print(f"\n✓ Vector database initialized successfully!")
        print(f"  Total chunks: {vector_store.count()}")
        
        return True
        
    except Exception as e:
        print(f"\n✗ Error initializing vector database: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Main setup function."""
    print("=" * 60)
    print("Sistema de Inspección Eléctrica - Setup")
    print("=" * 60)
    
    try:
        # Validate configuration
        print("\n=== Validating configuration ===")
        validate_config()
        print("✓ Configuration valid")
        
        # Setup directories
        setup_directories()
        
        # Check normas
        if not check_normas():
            print("\n⚠️  Setup incomplete: Missing normas")
            return False
        
        # Check template
        if not check_template():
            print("\n⚠️  Setup incomplete: Missing template")
            return False
        
        # Initialize vector database
        if not initialize_vector_database():
            print("\n⚠️  Setup incomplete: Vector database initialization failed")
            return False
        
        print("\n" + "=" * 60)
        print("✓ Setup completed successfully!")
        print("=" * 60)
        print("\nYou can now run the server with: python3 run_server.py")
        
        return True
        
    except Exception as e:
        print(f"\n✗ Setup failed: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
