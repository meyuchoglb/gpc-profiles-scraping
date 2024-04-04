import gspread
from oauth2client.service_account import ServiceAccountCredentials
from bs4 import BeautifulSoup
import requests
import time
#from typing_extensions import Literal
from typing import Literal  # This will not work in Python 3.7
import sys

# Set up the connection to Google Sheets
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
credentials = ServiceAccountCredentials.from_json_keyfile_name('secrets/ydi-host-1a9d259678b4.json', scope)
gc = gspread.authorize(credentials)

# Open the Google Spreadsheet
spreadsheet_name = 'gcp_challenge_profiles'
#worksheet_name = 'ACE'
worksheet_name = sys.argv[1]
print(f"Opening Google Spreadsheet: {spreadsheet_name}")
#spreadsheet = gc.open(spreadsheet_name)
spreadsheet = gc.open_by_key('17m7bBD3jU0fyQf52scNuu4PfKwfTDS8GIXg9JyvAtHA')
worksheet = spreadsheet.worksheet(worksheet_name)

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

# Get all data from the worksheet
data = worksheet.get_all_values()
headers = data[0]
students_data = data[1:]

# Total number of students in the data
total_students = len(students_data)

# Iterate over each student row
for index, student in enumerate(students_data):
    current_student = index + 1  # Current student number (1-indexed)
    print(f"Scraping profile {current_student} of {total_students}: {student[0]} {student[1]}")

    # Iterate over each course column starting from 'Course A title'
    for col_index, course_title in enumerate(headers[5:], start=5):
        if student[col_index]:
            continue  # Skip if there's already a value in the cell
        if check_course_in_profile(student[3], course_title):  # Public profile URL is in the fourth column (index 3)
            worksheet.update_cell(current_student + 1, col_index + 1, 'Y')  # +1 because Google Sheets is 1-indexed
        #else:
        #    worksheet.update_cell(current_student + 1, col_index + 1, 'N')

    # Delay between rows to avoid being blocked
    print(f"Waiting before processing the next profile...")
    #time.sleep(1)

print("Update complete.")