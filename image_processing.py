import cv2
import pytesseract
from PIL import Image
import os
from pytesseract import Output
import numpy as np
import re
'''
def preprocess_image(image_path):
    # Load image
    img = cv2.imread(image_path)
    print(f"Image dimensions: {img.shape}") # Add this line

    # Convert to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Apply Canny edge detection

    edges = gray
    # Apply morphological operations to clean up small artifacts and noise
    kernel = np.ones((3,3), np.uint8)
    edges = cv2.erode(edges, kernel, iterations=1)
    edges = cv2.dilate(edges, kernel, iterations=1)
    
    # Apply thresholding
    thresh = cv2.threshold(edges, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]

    return thresh
'''

def preprocess_image(image_path):
    
    img = cv2.imread(image_path)
    
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    filtered = cv2.bilateralFilter(gray, 5, 75, 75)
    thresh = cv2.adaptiveThreshold(filtered, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 8)
    thresh = cv2.bitwise_not(thresh)
    
    

    
    return thresh

config = r'--oem 3 --psm 6 -c tessedit_char_whitelist=0123456789/:AMPMAm'

def extract_text(image_path):
    
    try:
        filename = os.path.split(image_path)[1]
        print(f"Reading:",filename)
        # Preprocess image
        image = preprocess_image(image_path)
       
        # Convert image to string
        cv2.imwrite("cv_debug/"+filename+"normal.jpg",image)
        text = pytesseract.image_to_string(image)
        
        d = pytesseract.image_to_data(image, output_type=Output.DICT)
        n_boxes = len(d['level'])
        for i in range(n_boxes):
            (x, y, w, h) = (d['left'][i], d['top'][i], d['width'][i], d['height'][i])
            cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
        
        cv2.imwrite("cv_debug/"+filename,image)
        return text
    except Exception as e:
        print(f"Error processing image: {e}")
        return None
