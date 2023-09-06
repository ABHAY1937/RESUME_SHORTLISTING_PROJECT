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

    # Assuming resumes are in the "resumes" folder located in "Documents/DL Projects/ResumeAnalyzing_OCR_PROJECT"
    resumes_folder = os.path.join(os.path.expanduser("/home/abhay/Documents/DL Projects/ResumeAnalyzing_OCR_PROJECT"), "resume")
    
    keywords = ["python", "mysql", "machine learning", "data analysis",
                'natural language processing', 'tableau', 'powerbi',
                'data science', "deep learning", 'hadoop', 'spark', 'pyspark', 'aws',
                'Html', 'Css','Bootstrap','Javascript','Angular','React','Material UI','Mongodb',
                'Node js','Typescript','Flutter','Dart','Mobile App Development',
                'Cross-Platform Development','UI/UX Design','Widget',"ETL"]  # Adding relevant keywords 
    threshold_score = 5 #adding minimum keywords to be selected

    job_roles= ["Data Scientist","Data Engineer","Data Analyst","Front_End Developer","Flutter Developer"]
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
                        if any(keyword in ['Big Data','mysql','data science', 'machine learning',
                                        'natural language processing', "Deep Learning",'Visualizaion'] for keyword in matched_keywords):
                            job_roles = 'Data Scientist'
                            pass
                        elif any(keyword in ["ETL","Data preprocessing","Data Science","aws","Machine Learning","data analytics"] for keyword in matched_keywords):
                            job_roles = "Data Engineer"
                            pass
                        elif any (keyword in ['Data Analysis',"Machine Learning","Tableau","powerBI","Data modelling"] for keyword in matched_keywords):
                            job_roles = "Data Analyst"
                            pass
                        elif any(keyword in ['Html', 'Css','Bootstrap','Javascript','Angular','React',
                                             'Material UI','Mongodb','Node js'] for keyword in matched_keywords):
                            job_roles = 'Front_End Developer'
                            pass
                        elif any(keyword in ['Flutter','Dart','Mobile App Development',
                                             'Cross-Platform Development','UI/UX Design','Widget'] for keyword in matched_keywords):
                            job_roles = 'Flutter Developer'
                            
                    else:
                        print('None')

                        

                        shortlisted_resumes.append((resume_path, score, job_roles))

                    # Remove the temporary image file
                    os.remove(temp_image_path)

            if shortlisted_resumes:
                print("Shortlisted Resumes:")
                for resume_path, score, job_roles in shortlisted_resumes:
                    print(f"Resume: {resume_path}, Score: {score}, Job Category:{job_category}")

                    # Check if the URL already exists in the table to avoid duplicates
                    query = "SELECT * FROM Selected_resumes WHERE url = %s AND job_role = %s"
                    data = (resume_path,job_roles)
                    cursor.execute(query, data)
                    result = cursor.fetchone()

                    if not result:
                        # URL doesn't exist in the table, so insert it
                        query = "INSERT INTO Selected_resumes (url,job_role) VALUES (%s,%s)"
                        cursor.execute(query, data)

            else:
                print("No matched keywords found.")

            print()

    # Commit the changes to the database
    conn.commit()

    # Close the database connection
    cursor.close()
    conn.close()
