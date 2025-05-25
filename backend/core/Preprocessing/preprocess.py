
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
    Preprocesses an image:
    - Resize
    - Blur to reduce noise
    - Convert to HSV for color masking
    - Optional contrast enhancement
    - Background masking (basic)
    """
    # Resize
    img_resized = cv2.resize(img, size)

    # Gaussian blur to reduce noise
    blurred = cv2.GaussianBlur(img_resized, (5, 5), 0)

    # Convert to HSV
    hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)

    # Create a green mask (to isolate plant)
    lower_green, upper_green = get_dynamic_green_bounds(img_resized)

    # Convert to HSV and create mask
    hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, lower_green, upper_green)

    # Bitwise mask to extract plant region
    plant_only = cv2.bitwise_and(img_resized, img_resized, mask=mask)

    return {
        "original": img_resized,
        "blurred": blurred,
        "mask": mask,
        "plant_only": plant_only
    }
