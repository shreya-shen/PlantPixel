
import cv2
import numpy as np
from sklearn.cluster import KMeans
from scipy.signal import find_peaks

def apply_clahe_to_hsv(hsv_img):
    """Enhanced CLAHE application to HSV image with optimized parameters"""
    h, s, v = cv2.split(hsv_img)
    
    # Apply CLAHE to V channel with optimized parameters
    clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))
    v_eq = clahe.apply(v)
    
    # Optional: slight enhancement to saturation channel for better color discrimination
    clahe_sat = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    s_eq = clahe_sat.apply(s)
    
    # Combine enhanced channels
    return cv2.merge([h, s_eq, v_eq])

def compute_histogram_peak(hsv_img):
    """Enhanced dominant hue detection using improved histogram analysis"""
    hue_channel = hsv_img[:, :, 0]
    sat_channel = hsv_img[:, :, 1]
    val_channel = hsv_img[:, :, 2]
    
    # Create mask for meaningful pixels (avoid very dark or unsaturated pixels)
    meaningful_mask = (sat_channel > 20) & (val_channel > 30)
    
    if np.sum(meaningful_mask) > 0:
        meaningful_hues = hue_channel[meaningful_mask]
        hist = cv2.calcHist([meaningful_hues], [0], None, [180], [0, 180])
    else:
        hist = cv2.calcHist([hue_channel], [0], None, [180], [0, 180])
    
    hist = hist.flatten()
    
    # Enhanced peak detection with better parameters
    peaks, properties = find_peaks(
        hist, 
        distance=15,        # Minimum distance between peaks
        prominence=30,      # Minimum prominence
        height=50          # Minimum height
    )
    
    # Sort peaks by prominence (stronger peaks first)
    if len(peaks) > 0 and 'prominences' in properties:
        peak_strengths = properties['prominences']
        sorted_indices = np.argsort(peak_strengths)[::-1]
        peaks = peaks[sorted_indices]
    
    return peaks

def get_dynamic_green_bounds(bgr_img, k=4, margin=15):
    """
    Enhanced dynamic HSV bounds computation for green using:
    - Improved KMeans color clustering with better initialization
    - Multi-scale histogram analysis
    - CLAHE enhancement with optimized parameters
    - Robust fallback mechanisms
    """
    if bgr_img is None or bgr_img.size == 0:
        # Fallback bounds
        return np.array([25, 40, 40]), np.array([90, 255, 255])
    
    try:
        # Enhanced preprocessing
        resized = cv2.resize(bgr_img, (300, 300), interpolation=cv2.INTER_AREA)
        
        # Apply bilateral filter to reduce noise while preserving edges
        denoised = cv2.bilateralFilter(resized, 9, 75, 75)
        
        # Additional Gaussian blur for smoothing
        blurred = cv2.GaussianBlur(denoised, (5, 5), 0)
        
        hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)
        hsv_clahe = apply_clahe_to_hsv(hsv)

        # Enhanced clustering approach
        # Sample more strategically - focus on non-black pixels
        pixels = hsv_clahe.reshape((-1, 3))
        
        # Filter out very dark pixels (likely shadows/background)
        brightness_mask = pixels[:, 2] > 30  # V channel > 30
        if np.sum(brightness_mask) > 100:
            pixels = pixels[brightness_mask]
        
        # Reduce sample size for efficiency while maintaining diversity
        if len(pixels) > 10000:
            indices = np.random.choice(len(pixels), 10000, replace=False)
            pixels = pixels[indices]
        
        # Enhanced KMeans with better initialization
        kmeans = KMeans(n_clusters=k, n_init=10, init='k-means++', random_state=42)
        kmeans.fit(pixels)
        centers = kmeans.cluster_centers_

        # Enhanced green cluster detection
        # Multiple criteria for green identification
        greenish_clusters = []
        for center in centers:
            hue, sat, val = center
            
            # Primary green range (more restrictive)
            if 40 <= hue <= 80 and sat >= 30 and val >= 40:
                greenish_clusters.append((center, 1.0))  # High confidence
            # Extended green range (less restrictive)
            elif 25 <= hue <= 95 and sat >= 20 and val >= 30:
                greenish_clusters.append((center, 0.6))  # Medium confidence
        
        # Enhanced histogram validation
        hue_peaks = compute_histogram_peak(hsv_clahe)
        green_peaks = [p for p in hue_peaks if 25 <= p <= 95]
        
        # Choose best green cluster
        if greenish_clusters:
            # Sort by confidence and saturation
            greenish_clusters.sort(key=lambda x: (x[1], x[0][1]), reverse=True)
            green_center = greenish_clusters[0][0]
            
            # Validate against histogram peaks
            if not green_peaks:
                # If no histogram validation, adjust center towards typical green
                typical_green = np.array([60, 100, 100])  # Typical healthy green
                green_center = 0.7 * green_center + 0.3 * typical_green
        
        elif green_peaks:
            # Use histogram peak as fallback
            best_peak = green_peaks[0]
            green_center = np.array([best_peak, 80, 80])  # Reasonable sat/val
        
        else:
            # Ultimate fallback to static bounds
            return np.array([30, 40, 40]), np.array([85, 255, 255])

        # Enhanced bounds calculation
        hue, sat, val = green_center
        
        # Adaptive margin based on saturation and value
        hue_margin = max(10, min(margin, 25 - sat // 10))  # Smaller margin for saturated colors
        sat_margin = min(60, max(40, 100 - sat))  # Larger margin for low saturation
        val_margin = min(60, max(40, 120 - val))  # Larger margin for dark colors
        
        # Calculate bounds with adaptive margins
        lower = np.array([
            max(0, hue - hue_margin),
            max(0, sat - sat_margin),
            max(0, val - val_margin)
        ])
        
        upper = np.array([
            min(179, hue + hue_margin),
            255,  # Allow full saturation range
            255   # Allow full value range
        ])

        return lower.astype(np.uint8), upper.astype(np.uint8)
        
    except Exception as e:
        # Robust fallback in case of any errors
        print(f"Warning: Dynamic thresholding failed ({e}), using fallback bounds")
        return np.array([30, 40, 40]), np.array([85, 255, 255])
