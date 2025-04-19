# OCRCardDetector

**OCRCardDetector** is a Python-based tool that uses Tesseract OCR to detect whether an image contains an Aadhaar or PAN card and extracts key information such as name, date of birth, gender, Aadhaar number, or PAN number. It supports both English and Hindi text.

## 📌 Features
- Preprocesses images for improved OCR accuracy
- Uses Tesseract to extract text from Aadhaar or PAN card images
- Automatically detects the type of card (Aadhaar or PAN)
- Extracts relevant fields using regex patterns
- Logs extraction results and saves them to a CSV file

## 🖼️ Supported Card Types
- Aadhaar Cards (with text in English or Hindi)
- PAN Cards

## 🛠️ How to Use

1. **Install Dependencies**

```bash
pip install pytesseract opencv-python pillow numpy
```

2. **Install Tesseract OCR**

Download and install Tesseract from:  
https://github.com/tesseract-ocr/tesseract

Update the path in the script:
```python
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
```

3. **Place the image**

Replace `'Aadhar.jpg'` in the script with the actual path to your Aadhaar or PAN card image.

4. **Run the script**

```bash
python detection.py
```

5. **Check the output**

- Extracted text will be printed in the console
- Detected card type will be displayed
- Extracted details will be logged and saved to `extracted_details.csv`
- Raw text (if detection fails) is saved to `extracted_text_debug.txt`
- Logs are stored in `ocr_log.txt`

## 🧪 Example Output

```
Detected Card Type: Aadhaar
Name: Rahul Sharma
DOB: 15/08/1990
Gender: Male
Aadhaar Number: 1234 5678 9012
```

## 📄 Output Files
- `extracted_details.csv` – structured extracted data
- `ocr_log.txt` – log of the process
- `extracted_text_debug.txt` – raw OCR text if type is undetected

## 🔧 Dependencies
- `pytesseract`
- `opencv-python`
- `Pillow`
- `numpy`
- `re` (built-in)
- `csv` (built-in)

## 📄 License
Open source — feel free to use, modify, and contribute!

