import cv2
import numpy as np
import requests
from typing import List, Tuple
import io
from PIL import Image

def download_image_from_url(image_url: str) -> np.ndarray:
    """Download image from URL and convert to OpenCV format"""
    try:
        response = requests.get(image_url)
        response.raise_for_status()
        
        # Convert bytes to PIL Image
        pil_image = Image.open(io.BytesIO(response.content))
        
        # Convert PIL to OpenCV format (BGR)
        cv_image = cv2.cvtColor(np.array(pil_image), cv2.COLOR_RGB2BGR)
        return cv_image
    except Exception as e:
        print(f"Error downloading image: {e}")
        return None

def identify_drought_points(image_url: str) -> List[Tuple[float, float]]:
    """
    Identify drought points in NDWI satellite image based on our color scheme.
    Drought areas appear as black/dark colors in our NDWI palette.
    """
    image = download_image_from_url(image_url)
    if image is None:
        return []
    
    # Convert to HSV for better color detection
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    
    # Define drought color ranges based on our NDWI palette
    # Black to dark gray colors (drought conditions)
    drought_lower1 = np.array([0, 0, 0])      # Pure black
    drought_upper1 = np.array([180, 255, 50])  # Dark gray
    
    # Create mask for drought colors
    drought_mask = cv2.inRange(hsv, drought_lower1, drought_upper1)
    
    # Find contours of drought areas
    contours, _ = cv2.findContours(drought_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    drought_points = []
    for contour in contours:
        # Calculate centroid of each drought area
        M = cv2.moments(contour)
        if M["m00"] != 0:
            cx = int(M["m10"] / M["m00"])
            cy = int(M["m01"] / M["m00"])
            
            # Convert pixel coordinates to relative coordinates (0-1)
            height, width = image.shape[:2]
            rel_x = cx / width
            rel_y = cy / height
            
            # Only include significant drought areas (filter small noise)
            area = cv2.contourArea(contour)
            if area > 100:  # Minimum area threshold
                drought_points.append((rel_x, rel_y))
    
    return drought_points

def identify_acidic_points(image_url: str) -> List[Tuple[float, float]]:
    """
    Identify acidic soil points based on NDVI color scheme.
    Acidic conditions often correlate with poor vegetation (red/yellow colors).
    """
    image = download_image_from_url(image_url)
    if image is None:
        return []
    
    # Convert to HSV for better color detection
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    
    # Define acidic soil color ranges based on our NDVI palette
    # Red to yellow colors indicate poor soil conditions (potential acidity)
    
    # Red range (bare soil, acidic conditions)
    red_lower1 = np.array([0, 50, 50])
    red_upper1 = np.array([10, 255, 255])
    red_lower2 = np.array([170, 50, 50])
    red_upper2 = np.array([180, 255, 255])
    
    # Orange range (very poor soil)
    orange_lower = np.array([10, 50, 50])
    orange_upper = np.array([25, 255, 255])
    
    # Create masks for acidic soil colors
    red_mask1 = cv2.inRange(hsv, red_lower1, red_upper1)
    red_mask2 = cv2.inRange(hsv, red_lower2, red_upper2)
    orange_mask = cv2.inRange(hsv, orange_lower, orange_upper)
    
    # Combine masks
    acidic_mask = cv2.bitwise_or(red_mask1, red_mask2)
    acidic_mask = cv2.bitwise_or(acidic_mask, orange_mask)
    
    # Find contours of acidic areas
    contours, _ = cv2.findContours(acidic_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    acidic_points = []
    for contour in contours:
        # Calculate centroid of each acidic area
        M = cv2.moments(contour)
        if M["m00"] != 0:
            cx = int(M["m10"] / M["m00"])
            cy = int(M["m01"] / M["m00"])
            
            # Convert pixel coordinates to relative coordinates (0-1)
            height, width = image.shape[:2]
            rel_x = cx / width
            rel_y = cy / height
            
            # Only include significant acidic areas
            area = cv2.contourArea(contour)
            if area > 150:  # Minimum area threshold
                acidic_points.append((rel_x, rel_y))
    
    return acidic_points

def identify_poor_plant_health(image_url: str) -> List[Tuple[float, float]]:
    """
    Identify poor plant health points based on NDVI color scheme.
    Poor health appears as red, orange, yellow colors in our NDVI palette.
    """
    image = download_image_from_url(image_url)
    if image is None:
        return []
    
    # Convert to HSV for better color detection
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    
    # Define poor plant health color ranges based on our NDVI palette
    # Red, orange, yellow colors indicate poor vegetation health
    
    # Red range (bare soil, stressed plants)
    red_lower1 = np.array([0, 50, 50])
    red_upper1 = np.array([10, 255, 255])
    red_lower2 = np.array([170, 50, 50])
    red_upper2 = np.array([180, 255, 255])
    
    # Orange range (very stressed plants)
    orange_lower = np.array([10, 50, 50])
    orange_upper = np.array([25, 255, 255])
    
    # Yellow range (moderately stressed plants)
    yellow_lower = np.array([25, 50, 50])
    yellow_upper = np.array([35, 255, 255])
    
    # Create masks for poor health colors
    red_mask1 = cv2.inRange(hsv, red_lower1, red_upper1)
    red_mask2 = cv2.inRange(hsv, red_lower2, red_upper2)
    orange_mask = cv2.inRange(hsv, orange_lower, orange_upper)
    yellow_mask = cv2.inRange(hsv, yellow_lower, yellow_upper)
    
    # Combine masks
    poor_health_mask = cv2.bitwise_or(red_mask1, red_mask2)
    poor_health_mask = cv2.bitwise_or(poor_health_mask, orange_mask)
    poor_health_mask = cv2.bitwise_or(poor_health_mask, yellow_mask)
    
    # Find contours of poor health areas
    contours, _ = cv2.findContours(poor_health_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    poor_health_points = []
    for contour in contours:
        # Calculate centroid of each poor health area
        M = cv2.moments(contour)
        if M["m00"] != 0:
            cx = int(M["m10"] / M["m00"])
            cy = int(M["m01"] / M["m00"])
            
            # Convert pixel coordinates to relative coordinates (0-1)
            height, width = image.shape[:2]
            rel_x = cx / width
            rel_y = cy / height
            
            # Only include significant poor health areas
            area = cv2.contourArea(contour)
            if area > 100:  # Minimum area threshold
                poor_health_points.append((rel_x, rel_y))
    
    return poor_health_points

def analyze_satellite_image(image_url: str, analysis_type: str = "all") -> dict:
    """
    Comprehensive analysis of satellite image for agricultural issues.
    
    Args:
        image_url: URL of the satellite image
        analysis_type: "drought", "acidic", "poor_health", or "all"
    
    Returns:
        Dictionary with analysis results
    """
    results = {
        "image_url": image_url,
        "analysis_type": analysis_type,
        "drought_points": [],
        "acidic_points": [],
        "poor_health_points": [],
        "summary": {}
    }
    
    if analysis_type in ["drought", "all"]:
        drought_points = identify_drought_points(image_url)
        results["drought_points"] = drought_points
        results["summary"]["drought_count"] = len(drought_points)
        results["summary"]["drought_severity"] = "high" if len(drought_points) > 10 else "moderate" if len(drought_points) > 5 else "low"
    
    if analysis_type in ["acidic", "all"]:
        acidic_points = identify_acidic_points(image_url)
        results["acidic_points"] = acidic_points
        results["summary"]["acidic_count"] = len(acidic_points)
        results["summary"]["acidic_severity"] = "high" if len(acidic_points) > 8 else "moderate" if len(acidic_points) > 4 else "low"
    
    if analysis_type in ["poor_health", "all"]:
        poor_health_points = identify_poor_plant_health(image_url)
        results["poor_health_points"] = poor_health_points
        results["summary"]["poor_health_count"] = len(poor_health_points)
        results["summary"]["health_severity"] = "poor" if len(poor_health_points) > 12 else "moderate" if len(poor_health_points) > 6 else "good"
    
    return results

