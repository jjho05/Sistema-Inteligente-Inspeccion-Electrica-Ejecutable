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
        
        # Check if vector database is initialized
        vector_store = get_vector_store()
        if vector_store.is_empty():
            print("\n⚠️  Vector database is empty!")
            print("Running setup...")
            import setup
            if not setup.main():
                print("\n✗ Setup failed. Please run setup.py manually.")
                return False
        
        # Initialize agents
        integrator = IntegratorAgent()
        doc_generator = DocumentGenerator()
        
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
        temp_path = Path('data/temp') / image.filename
        temp_path.parent.mkdir(parents=True, exist_ok=True)
        image.save(str(temp_path))
        
        # Analyze
        print(f"Analyzing {image.filename} as {installation_type}...")
        analysis = integrator.generate_complete_analysis(
            str(temp_path),
            installation_type
        )
        
        # Clean up
        try:
            temp_path.unlink()
        except FileNotFoundError:
            pass  # File already deleted, ignore
        
        return jsonify({
            'success': True,
            'analysis': analysis
        })
        
    except Exception as e:
        print(f"Error in analysis: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'success': False, 'error': str(e)}), 500


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
    vector_store = get_vector_store()
    return jsonify({
        'status': 'healthy',
        'vector_db_chunks': vector_store.count()
    })


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
    if not initialize_system():
        print("\n✗ Failed to initialize system")
        sys.exit(1)
    
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
    
    app.run(host=args.host, port=args.port, debug=DEBUG)


if __name__ == '__main__':
    main()
