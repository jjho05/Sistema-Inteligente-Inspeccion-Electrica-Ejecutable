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

# Initialize agents
integrator = None
doc_generator = None


def initialize_system():
    """Initialize system components."""
    global integrator, doc_generator
    
    print("Initializing system...")
    
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
        
        print("✓ System initialized successfully")
        return True
        
    except Exception as e:
        print(f"✗ Initialization failed: {e}")
        import traceback
        traceback.print_exc()
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
    """Analyze installation image."""
    try:
        # Get image and installation type
        if 'image' not in request.files:
            return jsonify({'success': False, 'error': 'No image provided'}), 400
        
        image = request.files['image']
        installation_type = request.form.get('installation_type', 'tablero_distribucion')
        
        # Save image temporarily
        import tempfile
        import uuid
        
        # Use system temp directory which is always writable
        temp_dir = Path(tempfile.gettempdir()) / "electrica_temp"
        temp_dir.mkdir(parents=True, exist_ok=True)
        
        # Unique filename to avoid collisions
        unique_filename = f"{uuid.uuid4()}_{image.filename}"
        temp_path = temp_dir / unique_filename
        image.save(str(temp_path))
        
        # Analyze
        print(f"Analyzing {image.filename} as {installation_type}...")
        try:
            analysis = integrator.generate_complete_analysis(
                str(temp_path),
                installation_type
            )
        except Exception as analysis_err:
            print(f"Analysis internal error: {analysis_err}")
            import traceback
            traceback.print_exc()
            return jsonify({'success': False, 'error': f"Error interno en agentes: {str(analysis_err)}"}), 500
        
        # Clean up
        try:
            temp_path.unlink()
        except Exception:
            pass  # Ignore cleanup errors
        
        return jsonify({
            'success': True,
            'analysis': analysis
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
        
        # Generate PDF directly (no Word conversion needed)
        from backend.utils.pdf_generator import PDFGenerator
        pdf_gen = PDFGenerator()
        pdf_path = pdf_gen.generate_dictamen(dictamen_data)
        
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
        
        # Generate Word document
        from backend.utils.word_generator import WordGenerator
        word_gen = WordGenerator()
        word_path = word_gen.generate_dictamen(dictamen_data)
        
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
    try:
        vector_store = get_vector_store()
        count = vector_store.count()
    except:
        count = "Error/Incomplete"
        
    return jsonify({
        'status': 'healthy',
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
    
    # Try to list models
    try:
        import google.generativeai as genai
        if os.getenv('GEMINI_API_KEY'):
            genai.configure(api_key=os.getenv('GEMINI_API_KEY'))
            models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
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
    
    # Initialize system
    success = initialize_system()
    if not success:
        print("\n⚠️  Warning: System initialization failed or incomplete.")
        print("The server will start, but some features may be unavailable until setup is complete.")
        print("Please ensure PDF files are in data/normas/ and database is initialized.\n")
    
    # Cleanup old files (older than 120 days)
    cleanup_old_files(days=120)
    
    # Open browser (only in main process, not in reloader, and not in cloud)
    is_cloud = os.getenv('RENDER') or os.getenv('RAILWAY_ENVIRONMENT')
    if not args.no_browser and not os.environ.get('WERKZEUG_RUN_MAIN') and not is_cloud:
        url = f"http://{args.host}:{args.port}"
        print(f"\nOpening browser at {url}...")
        webbrowser.open(url)
    
    # Run server
    # In cloud, bind to 0.0.0.0 to accept external connections
    if is_cloud:
        args.host = '0.0.0.0'
    
    print(f"\n✓ Server starting on http://{args.host}:{args.port}")
    print("Press Ctrl+C to stop\n")
    
    # Use threaded=True for better concurrency in production
    app.run(
        host=args.host,
        port=args.port,
        debug=DEBUG,
        threaded=True,
        use_reloader=False  # Disable reloader in production
    )


if __name__ == '__main__':
    main()
