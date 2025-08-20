import cv2
import numpy as np
from core.Preprocessing.dynamicThresholding import get_dynamic_green_bounds

def calculate_bounding_box_area(mask):
    """
    Enhanced bounding box area calculation with improved contour detection.
    Uses better filtering and multiple validation criteria.

    Parameters:
    - mask: binary image with plant segmented.

    Returns:
    - bounding_box_area (int): Area in pixels of the bounding rectangle.
    - bounding_box_coords (tuple): Coordinates of the bounding box (x, y, w, h).
    """
    if mask is None or np.sum(mask) == 0:
        return 0, None
    
    # Enhanced preprocessing
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
    cleaned_mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel, iterations=1)
    cleaned_mask = cv2.morphologyEx(cleaned_mask, cv2.MORPH_CLOSE, kernel, iterations=2)
    
    # Find contours with better parameters
    contours, _ = cv2.findContours(cleaned_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if not contours:
        return 0, None

    # Filter contours by area and shape characteristics
    valid_contours = []
    for contour in contours:
        area = cv2.contourArea(contour)
        if area < 50:  # Too small
            continue
        
        # Check aspect ratio to filter out noise
        x, y, w, h = cv2.boundingRect(contour)
        aspect_ratio = float(w) / h
        if aspect_ratio > 10 or aspect_ratio < 0.1:  # Too elongated
            continue
            
        valid_contours.append(contour)
    
    if not valid_contours:
        return 0, None

    # Take the largest valid contour
    largest_contour = max(valid_contours, key=cv2.contourArea)

    # Get bounding rectangle
    x, y, w, h = cv2.boundingRect(largest_contour)
    area = w * h

    return area, (x, y, w, h)

def calculate_green_pixel_count(mask):
    """
    Enhanced green pixel count calculation with improved accuracy.
    Uses morphological operations and multi-threshold analysis.

    Parameters:
    - mask (np.ndarray): Binary mask where green pixels are 255.

    Returns:
    - green_pixel_count (int): Number of green pixels in the mask.
    - green_pixel_ratio (float): Ratio of green pixels to total pixels.
    """
    if mask is None or mask.size == 0:
        return 0, 0.0
    
    # Apply morphological operations to clean the mask
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
    
    # Remove noise with opening
    cleaned_mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel, iterations=1)
    
    # Fill small gaps with closing
    cleaned_mask = cv2.morphologyEx(cleaned_mask, cv2.MORPH_CLOSE, kernel, iterations=2)
    
    # Count cleaned pixels
    green_pixel_count = np.count_nonzero(cleaned_mask)
    total_pixel_count = cleaned_mask.shape[0] * cleaned_mask.shape[1]
    green_pixel_ratio = green_pixel_count / total_pixel_count

    return green_pixel_count, green_pixel_ratio

def estimate_leaf_count(mask, min_leaf_area=50):
    """
    Enhanced leaf count estimation using improved watershed segmentation.
    Includes better preprocessing and seed detection.

    Parameters:
    - mask (np.ndarray): Binary plant mask (255 for plant, 0 for background).
    - min_leaf_area (int): Minimum area in pixels to consider a valid leaf.

    Returns:
    - leaf_count (int): Number of leaf regions detected.
    - markers (np.ndarray): Watershed-labeled segmentation map.
    """
    if mask is None or np.sum(mask) == 0:
        return 0, mask
    
    # Enhanced preprocessing with multiple morphological operations
    kernel_small = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
    kernel_large = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
    
    # Step 1: Noise removal with opening
    cleaned_mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel_small, iterations=2)
    
    # Step 2: Fill small holes with closing
    cleaned_mask = cv2.morphologyEx(cleaned_mask, cv2.MORPH_CLOSE, kernel_large, iterations=1)

    # Step 3: Sure background area (dilated mask)
    sure_bg = cv2.dilate(cleaned_mask, kernel_large, iterations=3)

    # Step 4: Enhanced distance transform for better seed detection
    dist_transform = cv2.distanceTransform(cleaned_mask, cv2.DIST_L2, 5)
    
    # Use adaptive threshold based on image characteristics
    max_dist = dist_transform.max()
    if max_dist > 0:
        # Dynamic threshold: higher for larger objects, lower for smaller
        threshold_factor = min(0.6, max(0.3, max_dist / 50))
        _, sure_fg = cv2.threshold(dist_transform, threshold_factor * max_dist, 255, 0)
    else:
        return 0, cleaned_mask
    
    sure_fg = np.uint8(sure_fg)

    # Step 5: Unknown region (border)
    # Ensure sure_fg is the same shape as sure_bg for subtraction
    if sure_fg.shape != sure_bg.shape:
        sure_fg_resized = cv2.resize(np.array(sure_fg, dtype=np.uint8), (sure_bg.shape[1], sure_bg.shape[0]), interpolation=cv2.INTER_NEAREST)
    else:
        sure_fg_resized = np.array(sure_fg, dtype=np.uint8)
    unknown = cv2.subtract(sure_bg, sure_fg_resized)

    # Step 6: Enhanced marker labelling with connectivity analysis
    _, markers = cv2.connectedComponents(sure_fg) # type: ignore

    # Step 7: Add one to all labels so background is not 0, but 1
    markers = markers + 1

    # Step 8: Mark unknown region as 0
    markers[unknown == 255] = 0

    # Step 9: Convert original mask to BGR for watershed input
    mask_bgr = cv2.cvtColor(cleaned_mask, cv2.COLOR_GRAY2BGR)
    
    # Apply watershed with error handling
    try:
        markers = cv2.watershed(mask_bgr, markers)
    except cv2.error:
        return 0, cleaned_mask

    # Step 10: Count valid leaf regions with improved filtering
    leaf_regions = []
    for label in np.unique(markers):
        if label in [0, 1, -1]:
            continue  # ignore background and border
        
        region_mask = np.uint8(markers == label)
        area = cv2.countNonZero(region_mask) # type: ignore
        
        # Enhanced validation: check area and shape characteristics
        if area >= min_leaf_area:
            # Additional shape validation
            contours, _ = cv2.findContours(region_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE) # type: ignore
            if contours:
                contour = contours[0]
                perimeter = cv2.arcLength(contour, True)
                if perimeter > 0:
                    # Check if shape is reasonable (not too elongated)
                    circularity = 4 * np.pi * area / (perimeter * perimeter)
                    if circularity > 0.1:  # Reasonable shape
                        leaf_regions.append(label)

    leaf_count = len(leaf_regions)
    return leaf_count, markers

def calculate_color_health_index(masked_image, mask):
    """
    Enhanced Color Health Index (CHI) calculation using multiple color spaces
    and improved health metrics.

    Parameters:
    - masked_image (np.ndarray): Image containing only plant pixels.
    - mask (np.ndarray): Binary mask of the plant.

    Returns:
    - chi (float): Color Health Index between 0 and 1.
    - avg_hue (float): Average Hue of green pixels.
    - avg_sat (float): Average Saturation of green pixels.
    """
    if masked_image is None or mask is None or np.sum(mask) == 0:
        return 0.0, 0.0, 0.0
    
    # Convert to multiple color spaces for robust analysis
    hsv = cv2.cvtColor(masked_image, cv2.COLOR_BGR2HSV)
    lab = cv2.cvtColor(masked_image, cv2.COLOR_BGR2LAB)

    # Extract plant pixels from both color spaces
    hue = hsv[:, :, 0][mask > 0]
    sat = hsv[:, :, 1][mask > 0]
    val = hsv[:, :, 2][mask > 0]
    
    l_channel = lab[:, :, 0][mask > 0]
    a_channel = lab[:, :, 1][mask > 0]

    if hue.size == 0 or sat.size == 0:
        return 0.0, 0.0, 0.0

    # Calculate enhanced metrics
    avg_hue = np.mean(hue)
    avg_sat = np.mean(sat)
    avg_val = np.mean(val)
    avg_l = np.mean(l_channel)
    avg_a = np.mean(a_channel)

    # 1. Enhanced hue analysis (ideal green range: 40-80 in OpenCV)
    hue_deviation = abs(avg_hue - 60)  # 60 is ideal green
    hue_score = max(0, 1 - (hue_deviation / 40))  # Normalize deviation
    
    # 2. Saturation score (higher is better for healthy plants)
    sat_score = np.clip(avg_sat / 255, 0, 1)
    
    # 3. Value/brightness appropriateness (not too dark, not overexposed)
    optimal_brightness = 128
    brightness_deviation = abs(avg_val - optimal_brightness)
    brightness_score = max(0, 1 - (brightness_deviation / optimal_brightness))
    
    # 4. LAB color space green intensity (lower A values = more green)
    green_intensity = (128 - avg_a) / 128  # Normalize to 0-1
    green_score = np.clip(green_intensity, 0, 1)
    
    # 5. Color consistency (lower std = more consistent = healthier)
    hue_consistency = max(0, 1 - (np.std(hue) / 50))
    sat_consistency = max(0, 1 - (np.std(sat) / 100))
    
    # Weighted combination of all health indicators
    chi = (
        0.25 * hue_score +          # Correct green hue
        0.20 * sat_score +          # Vibrant colors
        0.15 * brightness_score +   # Appropriate brightness
        0.20 * green_score +        # Green intensity in LAB
        0.10 * hue_consistency +    # Color consistency
        0.10 * sat_consistency      # Saturation consistency
    )

    return round(np.clip(chi, 0, 1), 3), round(avg_hue, 2), round(avg_sat, 2)

def estimate_sunlight_proxy(hsv_image, mask, weather_data, alpha=0.7):
    """
    Enhanced sunlight exposure estimation combining multiple image analysis
    techniques with weather data for improved accuracy.

    Parameters:
    - hsv_image (np.ndarray): HSV image of the plant
    - mask (np.ndarray): binary mask of the plant region
    - weather_data (dict): weather API response containing 'clouds', 'uvi', etc.
    - alpha (float): weight for image-based features (default: 0.7)

    Returns:
    - final_sunlight_score (float): hybrid normalized sunlight proxy [0.0 - 1.0]
    - debug_info (dict): intermediate values for debugging and visualization
    """
    if hsv_image is None or mask is None or np.sum(mask) == 0:
        return 0.0, {"error": "Invalid input data"}

    # Enhanced brightness analysis using multiple channels
    value_channel = hsv_image[:, :, 2]
    saturation_channel = hsv_image[:, :, 1]
    hue_channel = hsv_image[:, :, 0]
    
    plant_values = value_channel[mask > 0]
    plant_saturations = saturation_channel[mask > 0]
    plant_hues = hue_channel[mask > 0]

    if len(plant_values) == 0:
        return 0.0, {"error": "Empty plant region in mask."}

    # Multi-level brightness analysis
    brightness_mean = np.mean(plant_values)
    brightness_std = np.std(plant_values)
    brightness_median = np.median(plant_values)
    
    # Normalized brightness metrics
    normalized_brightness = brightness_mean / 255.0
    brightness_uniformity = max(0, 1 - (brightness_std / 128))  # More uniform = better lighting
    
    # Enhanced shadow analysis with multiple thresholds
    shadow_thresholds = [0.15 * 255, 0.25 * 255, 0.35 * 255]
    shadow_scores = []
    
    for threshold in shadow_thresholds:
        shadow_pixels = np.sum(plant_values < threshold)
        shadow_density = shadow_pixels / len(plant_values)
        shadow_scores.append(1 - shadow_density)  # Higher score = less shadows
    
    # Weighted shadow score (emphasize deep shadows more)
    shadow_score = (0.5 * shadow_scores[0] + 0.3 * shadow_scores[1] + 0.2 * shadow_scores[2])
    
    # Saturation analysis (well-lit plants tend to be more saturated)
    saturation_mean = np.mean(plant_saturations)
    saturation_score = np.clip(saturation_mean / 255, 0, 1)
    
    # Highlight analysis (overexposure detection)
    highlight_threshold = 0.9 * 255
    highlight_pixels = np.sum(plant_values > highlight_threshold)
    highlight_ratio = highlight_pixels / len(plant_values)
    highlight_penalty = min(0.2, highlight_ratio * 2)  # Penalize overexposure
    
    # Combined image-based score
    image_brightness_score = (
        0.4 * normalized_brightness +
        0.3 * shadow_score +
        0.2 * brightness_uniformity +
        0.1 * saturation_score -
        highlight_penalty
    )
    image_brightness_score = np.clip(image_brightness_score, 0, 1)

    # Enhanced weather analysis
    cloudiness = weather_data.get('clouds', 50)
    uv_index = weather_data.get('uvi', 5)
    description = weather_data.get('weather', [{}])[0].get('main', '').lower()

    # Non-linear cloud factor (clearer skies have disproportionate impact)
    cloud_factor = ((100 - cloudiness) / 100.0) ** 0.8

    # UV index normalization with appropriate scaling
    uv_factor = min(uv_index / 10.0, 1.0)  # Scale to 0-1, cap at 10

    # Enhanced weather description modifiers
    weather_modifier = 0
    description_lower = description.lower()
    
    if any(term in description_lower for term in ['clear', 'sunny']):
        weather_modifier = 0.15
    elif any(term in description_lower for term in ['partly', 'few clouds']):
        weather_modifier = 0.05
    elif any(term in description_lower for term in ['scattered', 'broken']):
        weather_modifier = -0.05
    elif any(term in description_lower for term in ['overcast', 'cloudy']):
        weather_modifier = -0.15
    elif any(term in description_lower for term in ['rain', 'storm', 'drizzle']):
        weather_modifier = -0.25

    # Combined weather score
    weather_score = np.clip(
        0.6 * cloud_factor + 0.4 * uv_factor + weather_modifier,
        0.0, 1.0
    )

    # Final hybrid score with enhanced weighting
    hybrid_score = alpha * image_brightness_score + (1 - alpha) * weather_score
    final_sunlight_score = np.clip(hybrid_score, 0.0, 1.0)

    # Comprehensive debug information
    debug_info = {
        "brightness_mean": round(normalized_brightness, 3),
        "brightness_uniformity": round(brightness_uniformity, 3),
        "shadow_score": round(shadow_score, 3),
        "saturation_score": round(saturation_score, 3),
        "highlight_penalty": round(highlight_penalty, 3),
        "image_brightness_score": round(image_brightness_score, 3),
        "weather_score": round(weather_score, 3),
        "final_hybrid_score": round(final_sunlight_score, 3),
        "description": description,
        "cloudiness": cloudiness,
        "uv_index": uv_index,
        "weather_modifier": weather_modifier,
        "cloud_factor": round(cloud_factor, 3),
        "uv_factor": round(uv_factor, 3)
    }

    return final_sunlight_score, debug_info
