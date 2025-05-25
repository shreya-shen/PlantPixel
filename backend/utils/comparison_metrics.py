
import cv2
import numpy as np
from core.Preprocessing.dynamicThresholding import get_dynamic_green_bounds

def calculate_bounding_box_area(mask):
    """
    Calculates the bounding box area of the largest contour in the binary mask.

    Parameters:
    - mask: binary image with plant segmented.

    Returns:
    - bounding_box_area (int): Area in pixels of the bounding rectangle.
    - bounding_box_coords (tuple): Coordinates of the bounding box (x, y, w, h).
    """
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if not contours:
        return 0, None

    # Take the largest contour
    largest_contour = max(contours, key=cv2.contourArea)

    # Get bounding rectangle
    x, y, w, h = cv2.boundingRect(largest_contour)
    area = w * h

    return area, (x, y, w, h)

def calculate_green_pixel_count(mask):
    """
    Calculates the green pixel count and ratio from a precomputed green mask.

    Parameters:
    - mask (np.ndarray): Binary mask where green pixels are 255.

    Returns:
    - green_pixel_count (int): Number of green pixels in the mask.
    - green_pixel_ratio (float): Ratio of green pixels to total pixels.
    """
    green_pixel_count = np.count_nonzero(mask)
    total_pixel_count = mask.shape[0] * mask.shape[1]
    green_pixel_ratio = green_pixel_count / total_pixel_count

    return green_pixel_count, green_pixel_ratio

def estimate_leaf_count(mask, min_leaf_area=100):
    """
    Estimate number of leaves using the watershed segmentation method.

    Parameters:
    - mask (np.ndarray): Binary plant mask (255 for plant, 0 for background).
    - min_leaf_area (int): Minimum area in pixels to consider a valid leaf.

    Returns:
    - leaf_count (int): Number of leaf regions detected.
    - markers (np.ndarray): Watershed-labeled segmentation map.
    """
    # Step 1: Noise removal
    kernel = np.ones((3, 3), np.uint8)
    cleaned_mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel, iterations=2)

    # Step 2: Sure background area (dilated mask)
    sure_bg = cv2.dilate(cleaned_mask, kernel, iterations=3)

    # Step 3: Sure foreground (leaf centers) using distance transform
    dist_transform = cv2.distanceTransform(cleaned_mask, cv2.DIST_L2, 5)
    _, sure_fg = cv2.threshold(dist_transform, 0.4 * dist_transform.max(), 255, 0)
    sure_fg = np.uint8(sure_fg)

    # Step 4: Unknown region (border)
    unknown = cv2.subtract(sure_bg, sure_fg)

    # Step 5: Marker labelling
    _, markers = cv2.connectedComponents(sure_fg)

    # Step 6: Add one to all labels so background is not 0, but 1
    markers = markers + 1

    # Step 7: Mark unknown region as 0
    markers[unknown == 255] = 0

    # Step 8: Convert original mask to BGR for watershed input
    mask_bgr = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)
    markers = cv2.watershed(mask_bgr, markers)

    # Step 9: Count unique segments (ignoring background and border)
    leaf_regions = []
    for label in np.unique(markers):
        if label in [0, 1, -1]:
            continue  # ignore background and border
        
        region_mask = np.uint8(markers == label)
        area = cv2.countNonZero(region_mask)
        if area >= min_leaf_area:
            leaf_regions.append(label)

    leaf_count = len(leaf_regions)

    return leaf_count, markers

def calculate_color_health_index(masked_image, mask):
    """
    Calculates Color Health Index (CHI) using HSV values of masked plant image.

    Parameters:
    - masked_image (np.ndarray): Image containing only plant pixels.
    - mask (np.ndarray): Binary mask of the plant.

    Returns:
    - chi (float): Color Health Index between 0 and 1.
    - avg_hue (float): Average Hue of green pixels.
    - avg_sat (float): Average Saturation of green pixels.
    """
    # Convert to HSV
    hsv = cv2.cvtColor(masked_image, cv2.COLOR_BGR2HSV)

    # Filter out only the green regions based on mask
    hue = hsv[:, :, 0][mask > 0]
    sat = hsv[:, :, 1][mask > 0]

    if hue.size == 0 or sat.size == 0:
        return 0.0, 0.0, 0.0

    avg_hue = np.mean(hue)
    avg_sat = np.mean(sat)

    # Ideal green hue range is ~60–90 in OpenCV HSV scale
    hue_score = np.clip((avg_hue - 60) / 30, 0, 1)
    sat_score = np.clip(avg_sat / 255, 0, 1)

    chi = (0.6 * hue_score) + (0.4 * sat_score)

    return round(chi, 2), round(avg_hue, 2), round(avg_sat, 2)

def estimate_sunlight_proxy(hsv_image, mask, weather_data, alpha=0.6):
    """
    Combines image-based brightness, shadow density, and weather data
    into a hybrid sunlight exposure proxy score in the range [0.0, 1.0].

    Parameters:
    - hsv_image (np.ndarray): HSV image of the plant
    - mask (np.ndarray): binary mask of the plant region
    - weather_data (dict): weather API response containing 'clouds', 'uvi', etc.
    - alpha (float): weight for image-based features (default: 0.6)

    Returns:
    - final_sunlight_score (float): hybrid normalized sunlight proxy [0.0 - 1.0]
    - debug_info (dict): intermediate values for debugging and visualization
    """

    # Step 1: Image-based Brightness
    value_channel = hsv_image[:, :, 2]
    plant_values = value_channel[mask > 0]

    if len(plant_values) == 0:
        return 0.0, {"error": "Empty plant region in mask."}

    avg_brightness = np.mean(plant_values)
    normalized_brightness = avg_brightness / 255.0

    # Step 2: Shadow Density in Plant Region
    # Define "shadow" as pixels with low brightness (below 25%)
    shadow_threshold = 0.25 * 255
    shadow_pixels = np.sum((plant_values < shadow_threshold))
    total_pixels = len(plant_values)
    shadow_density = shadow_pixels / total_pixels if total_pixels > 0 else 0.0

    # Adjust brightness by shadow density (more shadow = lower brightness)
    adjusted_brightness = normalized_brightness * (1 - shadow_density)

    # Step 3: Weather-Based Sunlight Proxy
    cloudiness = weather_data.get('clouds', 100)  # default cloudy
    uv_index = weather_data.get('uvi', 5)  # fallback to mid
    description = weather_data.get('weather', [{}])[0].get('main', '').lower()

    # Basic cloud-based normalization
    cloud_factor = (100 - cloudiness) / 100.0

    # Adjust for textual weather description
    boost = 0
    if 'clear' in description:
        boost = 0.1
    elif 'sun' in description:
        boost = 0.15
    elif 'rain' in description or 'storm' in description:
        boost = -0.1
    elif 'cloud' in description:
        boost = -0.05

    sep_weather = np.clip(cloud_factor + boost, 0.0, 1.0)

    # Step 4: Combine into Hybrid Score
    hybrid_score = alpha * adjusted_brightness + (1 - alpha) * sep_weather
    final_sunlight_score = round(np.clip(hybrid_score, 0.0, 1.0), 3)

    # Debug Info (for logging / analysis)
    debug_info = {
        "avg_brightness": round(normalized_brightness, 3),
        "shadow_density": round(shadow_density, 3),
        "adjusted_brightness": round(adjusted_brightness, 3),
        "sep_weather": sep_weather,
        "final_hybrid_score": final_sunlight_score,
        "description": description,
        "cloudiness": cloudiness,
        "uv_index": uv_index
    }

    return final_sunlight_score, debug_info
