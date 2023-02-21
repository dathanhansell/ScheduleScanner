import os
from image_processing import extract_text
from excel_manipulation import parse_schedule, write_to_excel
from ical import write_ical

# Set directory path
directory = 'schedule'

# Iterate over images in directory
text = ""
for filename in os.listdir(directory):
    # Only process image files
    if filename.endswith('.jpg') or filename.endswith('.png'):
        input = os.path.join(directory, str(filename))
        # Extract text from image
        text += extract_text(str(input)) + "\n"
data = parse_schedule(text)
path = os.path.join(directory, "all.xlsx")
write_to_excel(data,path)
write_ical(path)