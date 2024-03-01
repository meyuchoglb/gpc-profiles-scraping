import pandas as pd
import requests
from bs4 import BeautifulSoup
import time

# Define the Excel file path
input_file = 'gcp_challenge_profiles.xlsx'
output_file = 'gcp_challenge_profiles.xlsx'

print("Opening file:", input_file)
df = pd.read_excel(input_file)

# Function to check if a course is mentioned in the public profile
def check_course_in_profile(url, course_title):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            return course_title in soup.get_text()
        else:
            print(f"Failed to retrieve {url}")
            return False
    except requests.RequestException as e:
        print(f"Request failed: {e}")
        return False

# Total number of students in the DataFrame
total_students = df.shape[0]

# Iterate over each student row
for index, row in df.iterrows():
    current_student = index + 1  # Current student number (1-indexed)
    print(f"Scraping profile {current_student} of {total_students}: {row['studentName']} {row['studentLastName']}")

    # Iterate over each course column starting from 'Course A title'
    for column in df.columns[4:]:
        course_title = row[column]
        if pd.isnull(course_title):
            # Public profile URL is in the fourth column
            if check_course_in_profile(row['publicProfileURL'], column):
                df.loc[index, column] = 'Y'
            else:
                df.loc[index, column] = 'N'
    
    # Delay between rows to avoid being blocked
    print(f"Waiting before processing the next profile...")
    time.sleep(1)

# Save the updated DataFrame back to Excel
print(f"Saving the updated data to {output_file}")
df.to_excel(output_file, index=False)
print("Update complete.")