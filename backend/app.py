
from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from datetime import datetime
import uuid
import json
from werkzeug.utils import secure_filename

# Import our custom modules
from routes.analysis_routes import analysis_bp
from services.growth_analysis import compare_and_score_growth, extract_metrics
from core.Preprocessing.preprocess import url_to_cv2_image, preprocess_image

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend integration

# Configuration
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Ensure upload directory exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# In-memory storage for demo (replace with MongoDB for production)
analysis_store = {}
image_store = {}

# Register blueprints
app.register_blueprint(analysis_bp, url_prefix='/api')

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy", "timestamp": datetime.utcnow().isoformat()})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
