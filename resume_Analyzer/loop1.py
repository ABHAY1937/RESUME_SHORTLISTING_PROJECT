keywords = ["python", "mysql", "machine learning", "data analysis",
            'natural language processing', 'tableau', 'powerbi',
            'data science', "deep learning", 'hadoop', 'spark', 'pyspark', 'aws']

job_roles = ['data_scientist', 'data_engineer', 'data_analyst', 'python_developer', 'ML_engineer']

# Loop through each job role
for role in job_roles:
    print(f"Job Role: {role}")

    # Check for keywords matching the job role (case-insensitive)
    matched_keywords = [keyword for keyword in keywords if keyword.lower() in role.lower()]

    # Set initial job category to None
    job_category = None

    # Determine the corresponding job category based on the matched keywords
    for keyword in matched_keywords:
        if keyword.lower() in ['hadoop', 'spark', 'mysql', 'data science', 'machine learning',
                               'natural language processing', 'aws']:
            job_category = "Data Engineer"
            break
        elif keyword.lower() in ['powerbi', 'tableau', 'data analytics', 'machine learning']:
            job_category = "Data Analyst"
            break
        elif keyword.lower() in ['python', 'mysql', 'machine learning']:
            job_category = 'Python Developer'
            break
        elif keyword.lower() in ['mysql', 'data science', 'machine learning',
                                 'natural language processing', 'deep learning', 'tableau', 'aws']:
            job_category = "ML Engineer"
            break
        else:
            job_category = "Data Scientist"

    if job_category:
        print(f"Job Category: {job_category}")
    else:
        print("No matched keywords found.")

    print()
