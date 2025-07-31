
import cv2
import numpy as np
from core.Preprocessing.preprocess import preprocess_image
from utils.comparison_metrics import (
    calculate_bounding_box_area,
    calculate_green_pixel_count,
    estimate_leaf_count,
    calculate_color_health_index,
    estimate_sunlight_proxy
)
from utils.performance_monitor import performance_monitor

# Standardized weights used for *all* plants
STANDARD_WEIGHTS = {
    "bounding_box_area": 0.25,
    "green_pixel_ratio": 0.25,
    "leaf_count": 0.20,
    "color_health_index": 0.20,
    "sunlight_proxy": 0.10
}

@performance_monitor.timing_decorator("image_preprocessing")
def extract_metrics(image):
    """
    Extracts all growth metrics from a given OpenCV image.
    Returns a dictionary of metrics.
    """
    try:
        # Preprocess the image
        preprocessed = preprocess_image(image)
        
        # Calculate bounding box area
        bounding_box_area, _ = calculate_bounding_box_area(preprocessed["mask"])
        
        # Calculate green pixel metrics
        green_pixel_count, green_pixel_ratio = calculate_green_pixel_count(preprocessed["mask"])
        
        # Estimate leaf count
        leaf_count, _ = estimate_leaf_count(preprocessed["mask"])
        
        # Calculate color health index
        color_health_index, _, _ = calculate_color_health_index(preprocessed["plant_only"], preprocessed["mask"])
        
        # Estimate sunlight proxy (using dummy weather data for now)
        hsv = cv2.cvtColor(preprocessed["blurred"], cv2.COLOR_BGR2HSV)
        dummy_weather = {"clouds": 30, "uvi": 6, "weather": [{"main": "Clear"}]}
        sunlight_proxy, _ = estimate_sunlight_proxy(hsv, preprocessed["mask"], dummy_weather)
        
        return {
            "bounding_box_area": bounding_box_area,
            "green_pixel_ratio": green_pixel_ratio,
            "leaf_count": leaf_count,
            "color_health_index": color_health_index,
            "sunlight_proxy": sunlight_proxy
        }
        
    except Exception as e:
        print(f"Error extracting metrics: {e}")
        # Return default values if extraction fails
        return {
            "bounding_box_area": 0,
            "green_pixel_ratio": 0.0,
            "leaf_count": 0,
            "color_health_index": 0.0,
            "sunlight_proxy": 0.0
        }

@performance_monitor.timing_decorator("growth_score_calculation")
def compare_and_score_growth(before_metrics, after_metrics):
    """
    Compare growth metrics and generate a normalized growth score.
    Uses standardized weights for all species.
    Returns the score (0-100) and delta values of each metric.
    """
    growth_score = 0
    deltas = {}
    
    for key, weight in STANDARD_WEIGHTS.items():
        if key in before_metrics and key in after_metrics:
            prev_val = before_metrics[key]
            curr_val = after_metrics[key]
            
            # Calculate percentage change
            if prev_val > 0:
                delta = ((curr_val - prev_val) / prev_val) * 100
            else:
                delta = 0 if curr_val == 0 else 100
            
            deltas[key] = delta
            
            # Normalize delta for scoring (-100 to +100 -> -1 to +1)
            normalized_delta = max(min(delta / 100, 1.0), -1.0)
            growth_score += weight * normalized_delta
    
    # Convert growth score to 0-100 scale
    final_score = max(0, min(100, (growth_score + 1) * 50))
    
    return final_score, deltas
