import cv2
import pytesseract
from PIL import Image
import os
from pytesseract import Output
import numpy as np
import re

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

config = r'--oem 3 --psm 6 -c tessedit_char_whitelist=0123456789/:AMPMAm'

def replace_characters(text):
    # Replace all periods and similar characters with colons
    text = re.sub(r'[.;,|/\\]+', ':', text)

    # Replace all exclamation points with I
    text = text.replace('!', 'I')

    # Remove lines with no characters
    text = '\n'.join([line for line in text.split('\n') if len(line.strip()) > 0])

    # Remove substrings with length less than 3, except for "am" or "pm"
    text = '\n'.join([' '.join([word for word in line.split() if len(word) >= 3 or word in ['am', 'pm']]) for line in text.split('\n')])

    return text

def extract_text(image_path):
    try:
        filename = os.path.split(image_path)[1]
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
        text = replace_characters(text)
        print(text)
        return text
    except Exception as e:
        print(f"Error processing image: {e}")
        return None
