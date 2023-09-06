keywords = ["python", "mysql", "machine learning", "data analysis",
            'natural language processing', 'tableau', 'powerbi',
            'data science', "deep learning", 'hadoop', 'spark', 'pyspark', 'aws']

job_roles = ['data_scientist', 'data_engineer', 'data_analyst', 'python_developer', 'ML_engineer']

# Loop through each job role
for role in job_roles:
    print(f"Job Role: {role}")
    
    # Check for keywords matching the job role (case-insensitive)
    matched_keywords = [keyword for keyword in keywords if keyword.lower() in role.lower()]
    
    # Determine the corresponding job category based on the matched keywords
    if not matched_keywords:
        print("No matched keywords found.")
    elif any(keyword in ['hadoop', 'spark', 'mysql', 'data science','machine learning',
                         'natural language processing','aws'] for keyword in matched_keywords):
        print("Data Engineer")
    elif any(keyword in ['powerbi', 'tableau', 'data analytics', 'machine learning'] for keyword in matched_keywords):
        print("Data Analyst")
    elif any(keywords in['python','mysql','machine learning']for keyword in matched_keywords):
        print('python developer')
    elif any(keywords in ['mysql', 'data science','machine learning',
                          'natural language processing','deep learning','tableau','aws']for keyword in matched_keywords):
        print("ML engineer")

    else:
        print("Data Scientist")
    
    print() 
