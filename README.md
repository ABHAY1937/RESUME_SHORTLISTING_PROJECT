
![Screenshot from 2023-09-06 11-54-33](https://github.com/tinugh/Resume_Shortlisting/assets/132256255/47b7dbd4-0efc-4f4f-9eb5-ff7a3ea90962)


# Resume Shortlisting Project

This is a Python-based project that aims to automate the process of shortlisting resumes for various job roles based on predefined keywords. The project uses Optical Character Recognition (OCR) to extract text from resume images, matches keywords with the extracted text, and classifies resumes into different job categories.


## Getting Started

To get started with this project, follow the instructions below.

### Prerequisites

Before running the project, you need to have the following prerequisites installed:

- Python 3.x
- OpenCV (cv2)
- PyTesseract
- MySQL Connector
- pdf2image
- Other dependencies mentioned in the project

You also need access to a MySQL database where you can store the shortlisted resumes.

### Usage

1. Clone the repository to your local machine:

   ```bash
   git clone https://github.com/your-username/resume-shortlisting-project.git
   ```

2. Install the required Python dependencies:

   ```bash
   pip install opencv-python pytesseract mysql-connector-python pdf2image
   ```

3. Update the database connection details in the code:

   Open the `main.py` file and modify the following lines with your database credentials:

   ```python
   conn = mysql.connector.connect(
       host="localhost",
       database="database_name",
       user="root",
       password="YourPasswordHere")
   ```

4. Customize keywords and job role mappings:

   You can customize the keywords and job roles in the `main.py` file by editing the `keywords` and `job_roles_keywords` dictionaries.

5. Run the project:

   ```bash
   python main.py
   ```

   The project will process the resume images, extract text, match keywords, and store the shortlisted resumes in the database.

## Contributing

If you want to contribute to this project, you can follow these steps:

1. Fork the repository on GitHub.
2. Create a new branch for your feature or bug fix: `git checkout -b feature/your-feature-name` or `git checkout -b bugfix/issue-number`.
3. Make your changes and commit them with descriptive messages.
4. Push your changes to your fork: `git push origin feature/your-feature-name`.
5. Create a pull request on the original repository to propose your changes.
