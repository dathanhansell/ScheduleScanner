import os
from image_processing import extract_text
from excel_manipulation import parse_schedule, write_to_excel

# Set directory path
directory = 'schedule'

# Iterate over images in directory
# Iterate over images in directory
for filename in os.listdir(directory):
    # Only process image files
    if filename.endswith('.jpg') or filename.endswith('.png'):
        input = os.path.join(directory, str(filename))
        # Extract text from image
        text = extract_text(str(input))

        # Extract table data from text
        data = parse_schedule(text)

        # Write data to Excel spreadsheet
        write_to_excel(data, os.path.join(directory, filename.replace('.jpg', '.xlsx')))