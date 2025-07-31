
from flask import Blueprint, request, jsonify, current_app
from werkzeug.utils import secure_filename
import os
import uuid
from datetime import datetime
import json
import cv2
import base64
import numpy as np
from io import BytesIO
from PIL import Image

from services.growth_analysis import compare_and_score_growth, extract_metrics
from core.Preprocessing.preprocess import preprocess_image
from utils.performance_monitor import performance_monitor

analysis_bp = Blueprint('analysis', __name__)

# In-memory storage (replace with database in production)
analysis_results = {}
uploaded_images = {}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'png', 'jpg', 'jpeg', 'gif'}

def base64_to_cv2(base64_string):
    """Convert base64 string to OpenCV image"""
    # Remove data URL prefix if present
    if ',' in base64_string:
        base64_string = base64_string.split(',')[1]
    
    # Decode base64
    img_data = base64.b64decode(base64_string)
    img = Image.open(BytesIO(img_data)).convert('RGB')
    return cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)

@analysis_bp.route('/upload', methods=['POST'])
def upload_images():
    """Upload two plant images for analysis"""
    try:
        data = request.get_json()
        
        if not data or 'beforeImage' not in data or 'afterImage' not in data:
            return jsonify({"error": "Both beforeImage and afterImage are required"}), 400
        
        # Generate unique session ID
        session_id = str(uuid.uuid4())
        
        # Store base64 images
        uploaded_images[session_id] = {
            'before_image': data['beforeImage'],
            'after_image': data['afterImage'],
            'species': data.get('species', 'unknown'),
            'timestamp': datetime.utcnow().isoformat()
        }
        
        return jsonify({
            "message": "Images uploaded successfully",
            "session_id": session_id,
            "timestamp": datetime.utcnow().isoformat()
        }), 200
        
    except Exception as e:
        return jsonify({"error": f"Upload failed: {str(e)}"}), 500

@analysis_bp.route('/analyze', methods=['POST'])
@performance_monitor.timing_decorator("full_analysis_pipeline")
def analyze_growth():
    """Analyze plant growth from uploaded images"""
    try:
        data = request.get_json()
        
        if not data or 'beforeImage' not in data or 'afterImage' not in data:
            return jsonify({"error": "Both images are required for analysis"}), 400
        
        # Convert base64 images to OpenCV format
        before_img = base64_to_cv2(data['beforeImage'])
        after_img = base64_to_cv2(data['afterImage'])
        
        # Extract metrics from both images
        before_metrics = extract_metrics(before_img)
        after_metrics = extract_metrics(after_img)
        
        # Calculate growth score and deltas
        growth_score = 0
        deltas = {}
        
        # Standard weights for all metrics
        weights = {
            "bounding_box_area": 0.25,
            "green_pixel_ratio": 0.25,
            "leaf_count": 0.20,
            "color_health_index": 0.20,
            "sunlight_proxy": 0.10
        }
        
        for key in before_metrics:
            if key in after_metrics and key in weights:
                prev_val = before_metrics[key]
                curr_val = after_metrics[key]
                
                # Calculate percentage change
                if prev_val > 0:
                    delta = ((curr_val - prev_val) / prev_val) * 100
                else:
                    delta = 0
                
                deltas[key] = round(delta, 2)
                
                # Normalize delta for scoring (-100 to +100 -> -1 to +1)
                normalized_delta = max(min(delta / 100, 1.0), -1.0)
                growth_score += weights[key] * normalized_delta
        
        # Convert growth score to 0-100 scale
        final_score = max(0, min(100, (growth_score + 1) * 50))
        
        # Generate suggestions based on score
        if final_score >= 80:
            suggestion = "Excellent growth! Your plant is thriving with strong development across all metrics."
        elif final_score >= 60:
            suggestion = "Good growth progress. Consider optimizing watering and light conditions for better results."
        elif final_score >= 40:
            suggestion = "Moderate growth detected. Check soil nutrition and ensure adequate sunlight exposure."
        else:
            suggestion = "Growth appears limited. Review care routine including water, light, and soil conditions."
        
        # Prepare response data
        analysis_id = str(uuid.uuid4())
        result = {
            "analysis_id": analysis_id,
            "growth_score": round(final_score, 1),
            "metrics": {
                "leafCount": {
                    "value": after_metrics.get("leaf_count", 0),
                    "previousValue": before_metrics.get("leaf_count", 0),
                    "unit": "leaves",
                    "description": "Number of individual leaves detected on the plant"
                },
                "greenPixelRatio": {
                    "value": after_metrics.get("green_pixel_ratio", 0) * 100,
                    "previousValue": before_metrics.get("green_pixel_ratio", 0) * 100,
                    "unit": "%",
                    "description": "Percentage of image pixels classified as healthy green plant material"
                },
                "boundingBoxArea": {
                    "value": after_metrics.get("bounding_box_area", 0),
                    "previousValue": before_metrics.get("bounding_box_area", 0),
                    "unit": "pixels²",
                    "description": "Total area covered by the plant's bounding rectangle"
                },
                "colorHealthIndex": {
                    "value": after_metrics.get("color_health_index", 0) * 100,
                    "previousValue": before_metrics.get("color_health_index", 0) * 100,
                    "unit": "%",
                    "description": "Health score based on color vibrancy and saturation"
                },
                "sunlightProxy": {
                    "value": after_metrics.get("sunlight_proxy", 0) * 100,
                    "previousValue": before_metrics.get("sunlight_proxy", 0) * 100,
                    "unit": "%",
                    "description": "Estimated sunlight exposure based on image brightness"
                }
            },
            "delta_metrics": deltas,
            "suggestion": suggestion,
            "timestamp": datetime.utcnow().isoformat(),
            "chart_data": [
                {
                    "date": "Before",
                    "growthScore": max(0, final_score - 20),
                    "leafCount": before_metrics.get("leaf_count", 0),
                    "greenPixelRatio": before_metrics.get("green_pixel_ratio", 0) * 100,
                    "boundingBoxArea": before_metrics.get("bounding_box_area", 0) / 1000,
                    "colorHealthIndex": before_metrics.get("color_health_index", 0) * 100
                },
                {
                    "date": "After",
                    "growthScore": final_score,
                    "leafCount": after_metrics.get("leaf_count", 0),
                    "greenPixelRatio": after_metrics.get("green_pixel_ratio", 0) * 100,
                    "boundingBoxArea": after_metrics.get("bounding_box_area", 0) / 1000,
                    "colorHealthIndex": after_metrics.get("color_health_index", 0) * 100
                }
            ]
        }
        
        # Store result for future retrieval
        analysis_results[analysis_id] = result
        
        return jsonify(result), 200
        
    except Exception as e:
        return jsonify({"error": f"Analysis failed: {str(e)}"}), 500

@analysis_bp.route('/metrics/<analysis_id>', methods=['GET'])
def get_metrics(analysis_id):
    """Retrieve previously computed analysis results"""
    if analysis_id in analysis_results:
        return jsonify(analysis_results[analysis_id]), 200
    else:
        return jsonify({"error": "Analysis not found"}), 404

@analysis_bp.route('/history', methods=['GET'])
def get_history():
    """Get all previous analyses"""
    history = list(analysis_results.values())
    # Sort by timestamp, newest first
    history.sort(key=lambda x: x['timestamp'], reverse=True)
    return jsonify({"analyses": history}), 200
