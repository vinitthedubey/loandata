#importing libraries
import pytesseract
import cv2
import re
import os

#setting path for tesseract
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

def preprocess_image(path):
    image = cv2.imread(path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5,5), 0)
    _, thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    return thresh

def extract_text(image):
    return pytesseract.image_to_string(image)

def extract_fields(text):
    fields = {}
    fields['Name'] = re.search(r'Name[:\-]?\s*(.*)', text)
    fields['Address'] = re.search(r'Address[:\-]?\s*(.*)', text)
    fields['PAN'] = re.search(r'[A-Z]{5}[0-9]{4}[A-Z]', text)
    fields['Income'] = re.search(r'Income[:\-]?\s*Rs\.?\s*([\d,]+)', text)
    fields['Loan Amount'] = re.search(r'Loan Amount[:\-]?\s*Rs\.?\s*([\d,]+)', text)
    return {
        'Name': fields['Name'].group(1).strip() if fields['Name'] else '',
        'Address': fields['Address'].group(1).strip() if fields['Address'] else '',
        'PAN': fields['PAN'].group(0) if fields['PAN'] else '',
        'Income': fields['Income'].group(1) if fields['Income'] else '',
        'Loan Amount': fields['Loan Amount'].group(1) if fields['Loan Amount'] else '',
    }

def process_loan_document(path):
    image = preprocess_image(path)
    text = extract_text(image)
    return extract_fields(text)
