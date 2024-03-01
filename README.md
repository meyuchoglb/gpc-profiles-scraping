# GCP Profile Scraping Documentation

This documentation covers the setup and usage of a Python script designed to verify and mark student progress in specifics learning paths in Googl'es Cloud Skill Boost portal by scraping data from public profiles. The script accesses a Google Sheet where the studens and path data should be completed, scrapes web pages for course titles, and updates the sheet accordingly.

## Prerequisites

Before you can run the script, ensure that you have:

- Python 3.8 or higher installed on your system.
- `pip` installed (Python’s package installer).

## Installation

Follow these steps to set up your environment for the script:

1. **Install Required Python Packages**

   Create a file named `requirements.txt` with the following content:

   ```plaintext
   gspread==5.4.0
   oauth2client==4.1.3
   beautifulsoup4==4.11.1
   requests==2.28.1
   ```

   Install the packages using `pip`:

   ```shell
   pip install -r requirements.txt
   ```

2. **Google Sheets API Setup**

   - Go to the [Google Developers Console](https://console.developers.google.com/).
   - Create a new project or select an existing one.
   - Enable the Google Sheets API for your project.
   - Create a service account for your project.
   - Download the JSON key file for your service account and place it in a folder called **secrets/**
   - Share your Google Sheet with the service account using the email found in the JSON key file.

3. **Prepare the Google Sheet**

   - The first row must contain the following column headers:
     - `studentName`
     - `studentLastName`
     - `studentEmail`
     - `publicProfileURL`
     - Course titles starting from the fifth column. They have to be the exact text of the course name in the Path section of Cloud Skill Boost page.
   - Rows below the headers should contain the respective student data, with course columns left empty for the script to fill.

## Usage

1. **Configure the Script**

   - Open the script with a text editor.
   - Set the `credentials` variable to the path of your JSON key file.
   - Set `spreadsheet_name` to the name of your Google Sheet.
   - Set the spreadsheet ID in the line 19. The ID is part of the URL of the file: https://docs.google.com/spreadsheets/d/<ID>?
   - Set `worksheet_name` to the name of the specific worksheet you're using.

2. **Run the Script**

   Execute the script in your terminal:

   ```shell
   python path_to_script.py
   ```

   The script will process each student, scrape the public profile URLs for course titles, and update the Google Sheet with 'Y' to indicate if the course title was found, which means that the student has completed this course.

   In every excecution, the script will start in row 2 and only search for the course title if the cell is empty (to avoid searching whet it already has a Y). It is very important that those cells should not be edited manually.

## Notes

- The script includes a delay between processing each student to avoid potential blocking by the server hosting the public profiles.
- Make sure you have the legal right to scrape the public profiles.
- Always comply with the terms of service of the website you are scraping.

## Troubleshooting

If you encounter any issues, check the following:

- Ensure that the Google Sheet is shared correctly with the service account's email address.
- Make sure the JSON key file path is correct in the script.
- Confirm that the Google Sheet and worksheet names are correctly set in the script.
- If you receive an `ImportError`, ensure that all packages are compatible with your Python version.

For further assistance, consult the error messages and traceback to diagnose and resolve issues.