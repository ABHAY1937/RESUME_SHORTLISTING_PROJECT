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

    keywords = ["python", "mysql", "machine learning", "data analysis",
                'natural language processing','tableau','powerbi',
                'data science',"deep learning",'hadoop','spark','pyspark','aws']  # Adding relevant keywords 
    threshold_score = 5  # minimum required score for selecting the resume

    job_roles = ['data_scientist', 'data_engineer', 'data_analyst', 'python_developer', 'ML_engineer']

    for role in job_roles:
        print(f"Job Role: {role}")

        # Create a list to store shortlisted resumes for each job role
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
                    # Job role classification logic
                    matched_keywords = [keyword for keyword in keywords if keyword.lower() in extracted_text.lower()]
                    job_category = None
                    if any(keyword in ['hadoop', 'spark', 'mysql', 'data science', 'machine learning',
                                      'natural language processing', 'aws'] for keyword in matched_keywords):
                        job_category = 'Data Engineer'
                        pass
                    elif any(keyword in ['powerbi', 'tableau', 'data analytics', 'machine learning'] for keyword in matched_keywords):
                        job_category = 'Data Analyst'
                        pass
                    elif any(keyword in ['python', 'mysql', 'machine learning'] for keyword in matched_keywords):
                        job_category = 'Python Developer'
                        pass
                    elif any(keyword in ['mysql', 'data science', 'machine learning',
                                         'natural language processing', 'deep learning', 'tableau', 'aws'] for keyword in matched_keywords):
                        job_category = 'ML Engineer'
                        pass
                    else:
                        job_category = 'Data Scientist'

                    shortlisted_resumes.append((resume_path, score, job_category))

                # Remove the temporary image file
                os.remove(temp_image_path)

        if shortlisted_resumes:
            print("Shortlisted Resumes:")
            for resume_path, score, job_category in shortlisted_resumes:
                print(f"Resume: {resume_path}, Score: {score}, Job Category: {job_category}")

                # Check if the URL already exists in the table to avoid duplicates
                query = "SELECT * FROM Sorted_resumes WHERE job_role = %s AND url = %s"
                data = (job_category, resume_path)

                # Create a separate cursor for fetching results
                fetch_cursor = conn.cursor()
                fetch_cursor.execute(query, data)
                result = fetch_cursor.fetchone()
                fetch_cursor.close()

                if not result:
                    # URL doesn't exist in the table, so insert it
                    insert_query = "INSERT INTO Sorted_resumes (job_role, url) VALUES (%s, %s)"
                    cursor.execute(insert_query, data)

                print()

    else:
        print("No matched keywords found.")


    # Commit the changes to the database
    conn.commit()

    # Close the database connection and cursor properly
    cursor.close()
    conn.close()
