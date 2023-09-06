import cv2
import numpy as np
import mysql.connector
import os
import pytesseract

conn = mysql.connector.connect(
    host="localhost",
    database="Resume_sorting",
    user="root",
    password="Password@123" )

cursor = conn.cursor()
cursor.execute("SELECT * FROM Resume_sorting")
for row in cursor:
    print(row)

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
    resumes_folder = ""
    keywords = ["python", "java", "machine learning", "data analysis"]  # Add relevant keywords here
    threshold_score = 2  # Adjust the threshold score as per your requirements
    
    shortlisted_resumes = []
    for resume_file in os.listdir(resumes_folder):
        resume_path = os.path.join(resumes_folder, resume_file)
        image = load_image(resume_path)
        extracted_text = extract_text_from_image(image)
        score = calculate_score(extracted_text, keywords)
        
        if score >= threshold_score:
            shortlisted_resumes.append((resume_path, score))
    
    print("Shortlisted Resumes:")
    for resume_path, score in shortlisted_resumes:
        print(f"Resume: {resume_path}, Score: {score}")