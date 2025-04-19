import pytesseract
from PIL import Image
import re
import cv2
import numpy as np
import logging
import csv

# Set up logging for debugging
logging.basicConfig(filename="ocr_log.txt", level=logging.INFO)

# Set the path to the tesseract executable
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Function to preprocess image for better OCR accuracy
def preprocess_image(image_path):
    image = cv2.imread(image_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # Denoise the image
    denoised = cv2.GaussianBlur(gray, (5, 5), 0)
    # Adaptive thresholding
    thresh = cv2.adaptiveThreshold(denoised, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
    return thresh

# Function to extract text from image
def extract_text_from_image(image_path, lang='eng+hin'):
    processed_image = preprocess_image(image_path)
    text = pytesseract.image_to_string(processed_image, lang=lang)
    return text

# Function to detect card type based on specific patterns
def detect_card_type(text):
    if re.search(r'\b\d{4}[-\s]?\d{4}[-\s]?\d{4}\b', text):  # Aadhaar pattern
        return "Aadhaar"
    elif re.search(r'\b[A-Z]{5}\d{4}[A-Z]\b', text):  # PAN pattern
        return "PAN"
    return "Unknown"

# Function to extract Aadhaar details
def extract_aadhaar_details(text):
    # Adjusting the regex patterns for better matching based on the extracted text
    name_english_regex = re.compile(r'(?:Name|नाम)\s*[:\-]?\s*([A-Z][a-zA-Z\s]+)', re.IGNORECASE)
    dob_regex = re.compile(r'(?:DOB|जन्म तिथि)\s*[:\-]?\s*(\d{2}/\d{2}/\d{4})')
    gender_regex = re.compile(r'(?:Gender|लिंग)\s*[:\-]?\s*(Male|Female|पुरुष|महिला)', re.IGNORECASE)
    aadhaar_regex = re.compile(r'\b(\d{4}\s\d{4}\s\d{4})\b')

    # Searching for the patterns in the extracted text
    name_english = name_english_regex.search(text)
    dob = dob_regex.search(text)
    gender = gender_regex.search(text)
    aadhaar_number = aadhaar_regex.search(text)

    return {
        "Name": name_english.group(1).strip() if name_english else "Not found",
        "DOB": dob.group(1) if dob else "Not found",
        "Gender": gender.group(1) if gender else "Not found",
        "Aadhaar Number": aadhaar_number.group(0) if aadhaar_number else "Not found"
    }


# Function to extract PAN details
def extract_pan_details(text):
    name_regex = re.compile(r'Name\s*([A-Z][a-zA-Z\s]+)\n')
    father_name_regex = re.compile(r'Father\'s Name\s*([A-Z][a-zA-Z\s]+)')
    dob_regex = re.compile(r'Date of Birth[: ]?\s*(\d{2}/\d{2}/\d{4})')
    pan_regex = re.compile(r'\b[A-Z]{5}\d{4}[A-Z]\b')

    name = name_regex.search(text)
    father_name = father_name_regex.search(text)
    dob = dob_regex.search(text)
    pan_number = pan_regex.search(text)

    return {
        "Name": name.group(1).strip() if name else "Not found",
        "Father's Name": father_name.group(1).strip() if father_name else "Not found",
        "Date of Birth": dob.group(1) if dob else "Not found",
        "PAN Number": pan_number.group(0) if pan_number else "Not found"
    }

# Function to log extraction results
def log_extraction_result(details):
    logging.info("Extraction Results: %s", details)

# Function to save extracted data to CSV
def save_to_csv(details, filename='extracted_details.csv'):
    with open(filename, mode='a', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=details.keys())
        writer.writerow(details)

# Main function to detect card type and extract relevant details
if __name__ == "__main__":
    # Path to your image (Replace with actual image path)
    image_path = 'Aadhar.jpg'  # Use the image path for PAN or Aadhaar card

    # Extract text from the image
    extracted_text = extract_text_from_image(image_path)
    print(f"Extracted Text: {extracted_text}")

    # Detect card type
    card_type = detect_card_type(extracted_text)
    print(f"Detected Card Type: {card_type}")

    if card_type == "Aadhaar":
        details = extract_aadhaar_details(extracted_text)
    elif card_type == "PAN":
        details = extract_pan_details(extracted_text)
    else:
        details = {"Error": "Could not determine card type"}
        # Log extracted text for debugging using UTF-8 encoding
        with open("extracted_text_debug.txt", "w", encoding='utf-8') as f:
            f.write(extracted_text)

    # Log and print extracted details
    log_extraction_result(details)
    
    for key, value in details.items():
        print(f"{key}: {value}")

    # Save the extracted details to a CSV file
    save_to_csv(details)
