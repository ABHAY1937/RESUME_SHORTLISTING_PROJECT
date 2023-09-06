import cv2
import numpy as np
import mysql.connector
import os
import pytesseract
from pdf2image import convert_from_path

# Function to load the resume image
def load_image(image_path):
    return cv2.imread(image_path)

# Function to perform OCR on the image
def extract_text_from_image(image):
    return pytesseract.image_to_string(image)

# Function to calculate the score based on keyword matching
def calculate_score(text, keywords):
    text_lower = text.lower()
    score = sum(keyword.lower() in text_lower for keyword in keywords)
    return score

if __name__ == "__main__":
    # Connect to the database
    conn = mysql.connector.connect(
        host="localhost",
        database="Resume_sorting",
        user="root",
        password="Password@123"
    )
    cursor = conn.cursor()

    # Fetch data from the database
    cursor.execute("SELECT * FROM Resume_sorting")

    # Assuming resumes are in the "resumes" folder located in "Documents/DL Projects/resume_Analyzer"
    resumes_folder = os.path.join(os.path.expanduser("~/Documents/DL Projects/resume_Analyzer"), "resumes")

    keywords = ["python", "java", "machine learning", "data analysis"]  # Add relevant keywords here
    threshold_score = 2  # Adjust the threshold score as per your requirements
    
    shortlisted_resumes = []
    for resume_file in os.listdir(resumes_folder):
        resume_path = os.path.join(resumes_folder, resume_file)

        # Convert PDF to images using pdf2image
        images = convert_from_path(resume_path)

        for idx, image in enumerate(images):
            # Save the image temporarily to process with pytesseract
            temp_image_path = f"temp_image_{idx}.png"
            image.save(temp_image_path)
            
            # Process the image with pytesseract
            image_cv2 = load_image(temp_image_path)
            extracted_text = extract_text_from_image(image_cv2)
            score = calculate_score(extracted_text, keywords)
            
            if score >= threshold_score:
                shortlisted_resumes.append((resume_path, score))
            
            # Remove the temporary image file
            os.remove(temp_image_path)
    
    print("Shortlisted Resumes:")
    for resume_path, score in shortlisted_resumes:
        print(f"Resume: {resume_path}, Score: {score}")

#info and demo2,demo1 anu work chiyuna code olle