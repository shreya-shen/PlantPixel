
import cv2
import numpy as np
from sklearn.cluster import KMeans
from scipy.signal import find_peaks

def apply_clahe_to_hsv(hsv_img):
    """Apply CLAHE to the V channel of an HSV image"""
    h, s, v = cv2.split(hsv_img)
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    v_eq = clahe.apply(v)
    return cv2.merge([h, s, v_eq])

def compute_histogram_peak(hsv_img):
    """Find dominant hue values using histogram peak detection"""
    hue_channel = hsv_img[:, :, 0]
    hist = cv2.calcHist([hue_channel], [0], None, [180], [0, 180])
    hist = hist.flatten()
    peaks, _ = find_peaks(hist, distance=10, prominence=50)
    return peaks

def get_dynamic_green_bounds(bgr_img, k=3, margin=20):
    """
    Compute dynamic lower and upper HSV bounds for green using:
    - KMeans color clustering
    - Histogram peak validation
    - CLAHE on the V channel
    """
    # Preprocess
    resized = cv2.resize(bgr_img, (300, 300))
    blurred = cv2.GaussianBlur(resized, (5, 5), 0)
    hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)
    hsv_clahe = apply_clahe_to_hsv(hsv)

    # Flatten for clustering
    pixels = hsv_clahe.reshape((-1, 3))
    kmeans = KMeans(n_clusters=k, n_init='auto')
    kmeans.fit(pixels)
    centers = kmeans.cluster_centers_

    # Filter greenish clusters (Hue between 35–85)
    greenish_clusters = [c for c in centers if 35 <= c[0] <= 85]

    # Validate using histogram
    hue_peaks = compute_histogram_peak(hsv_clahe)
    if not greenish_clusters or not any(35 <= p <= 85 for p in hue_peaks):
        # Fallback to static bounds
        return np.array([25, 40, 40]), np.array([90, 255, 255])

    green_center = greenish_clusters[0]

    # Define lower and upper bounds with margin
    lower = np.clip(green_center - [margin, 50, 50], [0, 0, 0], [179, 255, 255])
    upper = np.clip(green_center + [margin, 50, 50], [0, 0, 0], [179, 255, 255])

    return lower.astype(np.uint8), upper.astype(np.uint8)
