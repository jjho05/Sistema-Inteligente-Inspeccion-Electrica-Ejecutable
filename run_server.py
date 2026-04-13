"""
Main server script for the electrical inspection system.
Runs Flask server and handles API requests.
"""

import sys
import os
import webbrowser
from pathlib import Path
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import argparse
import threading
import time

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent))

from backend.utils.config import HOST, PORT, DEBUG, validate_config
from backend.agents.integrator_agent import IntegratorAgent
from backend.rag.vector_store import get_vector_store
from backend.knowledge.installation_types import get_type_names
from backend.utils.document_generator import DocumentGenerator
from backend.utils.file_cleanup import cleanup_old_files

print("\n" + "🚀" * 30)
print("INICIANDO SERVIDOR DE INSPECCIÓN ELÉCTRICA")
print("SISTEMA ARRANCANDO...")
print("🚀" * 30 + "\n")

# Initialize Flask app
app = Flask(__name__, static_folder='frontend', static_url_path='')
CORS(app)

# Global state for background initialization
system_ready = False
initialization_error = None
integrator = None
doc_generator = None

def initialize_system():
    """Initialize system components."""
    global integrator, doc_generator, system_ready, initialization_error
    
    print("\n" + "⚙️" * 30)
    print("BACKGROUND INITIALIZATION STARTING")
    print("⚙️" * 30 + "\n")
    
    try:
        # Validate configuration
        validate_config()
        
        # ALWAYS Initialize agents first so they are available
        integrator = IntegratorAgent()
        doc_generator = DocumentGenerator()
        
        # Check if vector database is initialized
        vector_store = get_vector_store()
        if vector_store.is_empty():
            print("\n⚠️  Vector database is empty!")
            print("Running setup...")
            import setup
            if not setup.main():
                print("\n✗ Setup failed. Please run setup.py manually.")
                # We return True anyway because agents are initialized 
                # and vision analysis can work without the DB
                return True
        
        
        print("\n" + "✓" * 30)
        print("SYSTEM INITIALIZED SUCCESSFULLY")
        print("✓" * 30 + "\n")
        system_ready = True
        return True
        
    except Exception as e:
        print(f"\n✗ Initialization failed: {e}")
        import traceback
        traceback.print_exc()
        initialization_error = str(e)
        return False


# Routes
@app.route('/')
def index():
    """Serve main page."""
    return send_from_directory('frontend', 'index.html')


@app.route('/api/installation-types', methods=['GET'])
def get_installation_types():
    """Get available installation types."""
    try:
        types = get_type_names()
        return jsonify({'success': True, 'types': types})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/analyze', methods=['POST'])
def analyze_installation():
    """Analyze installation images (multiple)."""
    try:
        # Get installation type
        installation_type = request.form.get('installation_type', 'tablero_distribucion')
        
        # Collect images from files and URLs
        images_to_process = []
        
        # 1. Handle uploaded files
        if 'images' in request.files:
            files = request.files.getlist('images')
            for file in files:
                if file.filename:
                    images_to_process.append(('file', file))
        elif 'image' in request.files:
            file = request.files['image']
            if file.filename:
                images_to_process.append(('file', file))
        
        # 2. Handle URLs
        if 'image_urls' in request.form:
            urls = request.form.getlist('image_urls')
            for url in urls:
                if url.strip():
                    images_to_process.append(('url', url.strip()))
        
        if not images_to_process:
            return jsonify({'success': False, 'error': 'No images provided'}), 400
        
        # Save images temporarily
        import tempfile
        import uuid
        import urllib.request
        
        temp_dir = Path(tempfile.gettempdir()) / "electrica_temp"
        temp_dir.mkdir(parents=True, exist_ok=True)
        
        saved_paths = []
        saved_filenames = []
        
        for kind, item in images_to_process:
            try:
                unique_name = f"{uuid.uuid4()}"
                
                if kind == 'file':
                    ext = Path(item.filename).suffix or '.jpg'
                    filename = f"{unique_name}{ext}"
                    path = temp_dir / filename
                    item.save(str(path))
                    saved_paths.append(str(path))
                    saved_filenames.append(filename)
                    
                elif kind == 'url':
                    # Download URL
                    ext = '.jpg' # Default extension if unknown
                    if '.' in item.split('/')[-1]:
                        ext = '.' + item.split('/')[-1].split('.')[-1].split('?')[0]
                    
                    filename = f"{unique_name}{ext}"
                    path = temp_dir / filename
                    
                    # Download with user agent to avoid blocks
                    opener = urllib.request.build_opener()
                    opener.addheaders = [('User-agent', 'Mozilla/5.0')]
                    urllib.request.install_opener(opener)
                    urllib.request.urlretrieve(item, str(path))
                    
                    saved_paths.append(str(path))
                    saved_filenames.append(filename)
                    
            except Exception as img_err:
                print(f"Error processing image {item}: {img_err}")
                continue

        if not saved_paths:
             return jsonify({'success': False, 'error': 'Failed to process any images'}), 500

        # Analyze
        print(f"Analyzing {len(saved_paths)} images as {installation_type}...")
        try:
            # We pass the LIST of paths to the agent
            analysis = integrator.generate_complete_analysis(
                saved_paths,  # Passing list now
                installation_type
            )
        except Exception as analysis_err:
            print(f"Analysis internal error: {analysis_err}")
            import traceback
            traceback.print_exc()
            return jsonify({'success': False, 'error': f"Error interno en agentes: {str(analysis_err)}"}), 500
        
        # We DO NOT delete temp files immediately so user can download them
        # Cleanup handles old files later
        
        return jsonify({
            'success': True,
            'analysis': analysis,
            'image_filenames': saved_filenames, # Return list
            'image_filename': saved_filenames[0] if saved_filenames else None # Legacy compatibility
        })
        
    except Exception as e:
        print(f"Global error in analysis route: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'success': False, 'error': f"Error global: {str(e)}"}), 500


@app.route('/api/generate-dictamen', methods=['POST'])
def generate_dictamen():
    """Generate PDF dictamen document directly."""
    try:
        data = request.json
        analysis = data.get('analysis')
        inspection_data = data.get('inspection_data', {})
        
        # Generate dictamen data
        dictamen_data = integrator.generate_dictamen_data(analysis, inspection_data)
        
        # Resolve image paths
        image_filenames = data.get('image_filenames', [])
        # Fallback for legacy/single image
        if 'image_filename' in data and not image_filenames:
            image_filenames = [data['image_filename']]
            
        image_paths = []
        import tempfile
        temp_dir = Path(tempfile.gettempdir()) / "electrica_temp"
        
        for fname in image_filenames:
            path = temp_dir / fname
            if path.exists():
                image_paths.append(str(path))
            
        # Generate PDF directly
        from backend.utils.pdf_generator import PDFGenerator
        pdf_gen = PDFGenerator()
        pdf_path = pdf_gen.generate_dictamen(dictamen_data, image_paths=image_paths) # Pass list
        
        return jsonify({
            'success': True,
            'document_path': pdf_path,
            'filename': Path(pdf_path).name
        })
        
    except Exception as e:
        print(f"Error generating dictamen: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/generate-dictamen-word', methods=['POST'])
def generate_dictamen_word():
    """Generate Word dictamen document."""
    try:
        data = request.json
        analysis = data.get('analysis')
        inspection_data = data.get('inspection_data', {})
        
        # Generate dictamen data
        dictamen_data = integrator.generate_dictamen_data(analysis, inspection_data)
        
        # Resolve image paths
        image_filenames = data.get('image_filenames', [])
        # Fallback
        if 'image_filename' in data and not image_filenames:
            image_filenames = [data['image_filename']]
            
        image_paths = []
        import tempfile
        temp_dir = Path(tempfile.gettempdir()) / "electrica_temp"
        
        for fname in image_filenames:
            path = temp_dir / fname
            if path.exists():
                image_paths.append(str(path))
            
        # Generate Word document
        from backend.utils.word_generator import WordGenerator
        word_gen = WordGenerator()
        
        word_path = word_gen.generate_dictamen(dictamen_data, image_paths=image_paths) # Pass list
        
        return jsonify({
            'success': True,
            'document_path': word_path,
            'filename': Path(word_path).name
        })
        
    except Exception as e:
        print(f"Error generating Word dictamen: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/download-photo/<filename>')
def download_photo(filename):
    """Download original analyzed photo."""
    try:
        import tempfile
        temp_dir = Path(tempfile.gettempdir()) / "electrica_temp"
        return send_from_directory(temp_dir, filename, as_attachment=True)
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 404


@app.route('/api/download/<filename>')
def download_file(filename):
    """Download generated document."""
    try:
        return send_from_directory('data/generated', filename, as_attachment=True)
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 404


@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    global system_ready, initialization_error
    
    try:
        if system_ready:
            vector_store = get_vector_store()
            count = vector_store.count()
            status = 'healthy'
        else:
            count = 0
            status = 'initializing'
            if initialization_error:
                status = 'error'
    except Exception as e:
        count = f"Error: {str(e)}"
        status = 'error'
        
    return jsonify({
        'status': status,
        'ready': system_ready,
        'error': initialization_error,
        'vector_db_chunks': count,
        'model': os.getenv('GEMINI_MODEL', 'Default')
    })


@app.route('/api/debug-env', methods=['GET'])
def debug_env():
    """Endpoint for debugging environment variables on Hugging Face."""
    config_keys = [
        'GEMINI_API_KEY', 'PORT', 'HOST', 'DEBUG', 
        'VECTOR_DB_PATH', 'NORMAS_PATH'
    ]
    
    debug_data = {
        'os_env': {k: "SET (Hidden)" if "KEY" in k else os.getenv(k, "NOT SET") for k in config_keys},
        'current_directory': os.getcwd(),
        'files_in_data': os.listdir('data') if os.path.exists('data') else "data folder missing"
    }
    
    # Try to list models using new SDK
    try:
        from google import genai
        if os.getenv('GEMINI_API_KEY'):
            client = genai.Client(api_key=os.getenv('GEMINI_API_KEY'))
            models = [m.name for m in client.models.list() if 'generateContent' in m.supported_generation_methods]
            debug_data['available_models'] = models
        else:
            debug_data['available_models'] = "No API Key found to list models"
    except Exception as e:
        debug_data['available_models_error'] = str(e)
        
    return jsonify(debug_data)


def main():
    """Main function."""
    # Get port from environment (for cloud deployment) or use default
    port = int(os.getenv('PORT', PORT))
    host = os.getenv('HOST', HOST)
    
    parser = argparse.ArgumentParser(description='Electrical Inspection System Server')
    parser.add_argument('--port', type=int, default=port, help='Port to run server on')
    parser.add_argument('--host', default=host, help='Host to run server on')
    parser.add_argument('--no-browser', action='store_true', help='Do not open browser')
    args = parser.parse_args()
    
    print("=" * 60)
    print("Sistema de Inspección Eléctrica")
    print("=" * 60)
    
    # Start background initialization
    init_thread = threading.Thread(target=initialize_system, daemon=True)
    init_thread.start()
    
    # Run server
    # In cloud, bind to 0.0.0.0 to accept external connections
    if is_cloud:
        args.host = '0.0.0.0'
        print("☁️ Cloud environment detected, binding to 0.0.0.0")
    
    print(f"\n✓ Server starting on http://{args.host}:{args.port}")
    print("Press Ctrl+C to stop\n")
    
    # Use threaded=True for better concurrency in production
    app.run(
        host=args.host,
        port=args.port,
        debug=False, # Force debug off in production initialization flow
        threaded=True,
        use_reloader=False  # Disable reloader in production
    )


if __name__ == '__main__':
    main()
