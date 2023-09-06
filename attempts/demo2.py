import cv2
import numpy as np
import mysql.connector
import os
import pytesseract
import re
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

# Function to extract email from the OCR text using regular expression
def extract_email(text):
    email_match = re.search(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', text.lower())
    return email_match.group() if email_match else None

if __name__ == "__main__":
    # Connect to the database
    conn = mysql.connector.connect(
        host="localhost",
        database="Resume_sorting",
        user="root",
        password="Password@123")
    cursor = conn.cursor()

    # Fetch data from the database
    cursor.execute("SELECT * FROM url_project")

    # Consume any unread results from the SELECT query
    cursor.fetchall()

    # Assuming resumes are in the "resumes" folder located in "Documents/DL Projects/resume_Analyzer"
    resumes_folder = os.path.join(os.path.expanduser("/home/abhay/Documents/DL Projects/ResumeAnalyzing_OCR_PROJECT"), "resume")

    keywords = ["python", "mysql", "machine learning", "data analysis",
                'natural language processing', 'tableau', 'powerbi',
                'data science', "deep learning", 'hadoop', 'spark', 'pyspark', 'aws',
                'Html', 'Css','Bootstrap','Javascript','Angular','React','Material UI','Mongodb',
                'Node js','Typescript','Flutter','Dart','Mobile App Development',
                'Cross-Platform Development','UI/UX Design','Widget']  # Adding relevant keywords 
    threshold_score = 5  # minimum required score for selecting the resume

    job_roles = ['data_scientist', 'data_engineer', 'data_analyst','Front-End Developer','Flutter Developer']
    date = ['2023-09-11','2023-09-15','2023-09-20','2023-09-23','2023-09-30']
    all_shortlisted_resumes = []

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
                    else:
                        job_category = 'nill'

                    resume_name = resume_file  # Extract only the name
                    email = extract_email(extracted_text)  # Extract email using the provided pattern

                    shortlisted_resumes.append((date, resume_name, email, job_category))

                # Remove the temporary image file
                os.remove(temp_image_path)

        if shortlisted_resumes:
            print("Shortlisted Resumes:")
            for date, resume_name, email, job_category in shortlisted_resumes:
                print(f"Interview Date: {date}")
                print(f"Name: {resume_name}")
                print(f"Email: {email}")
                print(f"Job Category: {job_category}")
                print()

                # Check if the URL already exists in the table to avoid duplicates
                query = "SELECT * FROM Modified_resumes WHERE name = %s"
                data = (resume_name,)
                cursor.execute(query, data)
                result = cursor.fetchone()

                if not result:
                    # URL doesn't exist in the table, so insert it
                    # Modify the data format for "date" column to store as comma-separated values
                    query = "INSERT INTO Modified_resumes (Interview_date, name, email, job_category) VALUES (%s, %s, %s, %s)"
                    insert_data = (",".join(date), resume_name, email, job_category)
                    cursor.execute(query, insert_data)

    # Commit the changes to the database after processing all job roles
    conn.commit()

    # Close the database connection after processing all job roles
    cursor.close()
    conn.close()

    # Print the list of selected candidates for each job role along with the corresponding job category
    print("Selected Candidates for Each Job Role:")
    for entry in all_shortlisted_resumes:
        print(f"Job Category: {entry['Job Category']}")
        print("Shortlisted Resumes:")
        for date, resume_name, email, job_category in entry['Resumes']:
            print(f"Interview Date: {date}")
            print(f"Name: {resume_name}")
            print(f"Email: {email}")
            print(f"Job Category: {job_category}")
            print()
