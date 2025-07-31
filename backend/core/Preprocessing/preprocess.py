
import cv2
import numpy as np
import requests
import os
from io import BytesIO
from PIL import Image
from .dynamicThresholding import get_dynamic_green_bounds


def url_to_cv2_image(url):
    """Fetch image from URL and convert to OpenCV format"""
    response = requests.get(url)
    img = Image.open(BytesIO(response.content)).convert('RGB')
    return cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)

def preprocess_image(img, size=(300, 300)):
    """
    Enhanced image preprocessing with improved noise reduction,
    adaptive masking, and better plant isolation.
    
    Parameters:
    - img: Input image
    - size: Target size for resizing
    
    Returns:
    - Dictionary with processed image variants
    """
    if img is None:
        # Return default empty results
        empty_img = np.zeros((size[0], size[1], 3), dtype=np.uint8)
        empty_mask = np.zeros((size[0], size[1]), dtype=np.uint8)
        return {
            "original": empty_img,
            "blurred": empty_img,
            "mask": empty_mask,
            "plant_only": empty_img
        }
    
    # Resize with better interpolation
    img_resized = cv2.resize(img, size, interpolation=cv2.INTER_AREA)

    # Enhanced denoising
    # Apply bilateral filter to reduce noise while preserving edges
    denoised = cv2.bilateralFilter(img_resized, 9, 75, 75)
    
    # Gaussian blur for additional smoothing
    blurred = cv2.GaussianBlur(denoised, (5, 5), 0)

    # Enhanced green mask creation using multiple techniques
    
    # Method 1: Dynamic thresholding
    lower_green, upper_green = get_dynamic_green_bounds(img_resized)
    
    # Method 2: HSV-based green detection
    hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)
    mask_hsv = cv2.inRange(hsv, lower_green, upper_green)
    
    # Method 3: LAB color space green detection
    lab = cv2.cvtColor(blurred, cv2.COLOR_BGR2LAB)
    a_channel = lab[:, :, 1]
    _, mask_lab = cv2.threshold(a_channel, 120, 255, cv2.THRESH_BINARY_INV)
    
    # Method 4: Adaptive threshold on green channel
    green_channel = img_resized[:, :, 1]  # Green channel in BGR
    mask_adaptive = cv2.adaptiveThreshold(
        green_channel, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
        cv2.THRESH_BINARY, 11, 2
    )
    
    # Combine masks for robust detection
    combined_mask = cv2.bitwise_or(mask_hsv, mask_lab)
    combined_mask = cv2.bitwise_and(combined_mask, mask_adaptive)
    
    # Enhanced morphological operations to clean the mask
    kernel_small = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
    kernel_large = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
    
    # Remove small noise
    mask_clean = cv2.morphologyEx(combined_mask, cv2.MORPH_OPEN, kernel_small, iterations=2)
    
    # Fill small gaps
    mask_clean = cv2.morphologyEx(mask_clean, cv2.MORPH_CLOSE, kernel_large, iterations=2)
    
    # Remove very small components
    contours, _ = cv2.findContours(mask_clean, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    for contour in contours:
        if cv2.contourArea(contour) < 100:  # Remove very small areas
            cv2.fillPoly(mask_clean, [contour], 0)

    # Create enhanced plant-only image
    plant_only = cv2.bitwise_and(img_resized, img_resized, mask=mask_clean)

    return {
        "original": img_resized,
        "blurred": blurred,
        "mask": mask_clean,
        "plant_only": plant_only
    }
