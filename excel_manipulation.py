import pandas as pd
import string
from openpyxl.utils.exceptions import IllegalCharacterError
import datetime
import calendar
import re

def replace_characters(text):
    # Replace all periods and similar characters with colons
    text = re.sub(r'[.;,|/\\]+', ':', text)

    # Replace all exclamation points with I
    text = re.sub(r'[!]|[)|\]|}|{|(|\[]+', 'I', text)

    # Remove lines with no characters
    text = '\n'.join([line for line in text.split('\n') if len(line.strip()) > 0])

    # Remove substrings with length less than 3, except for "am" or "pm"
    text = '\n'.join([' '.join([word for word in line.split() if len(word) >= 3 or word in ['am', 'pm']]) for line in text.split('\n')])

    return text

def parse_schedule(schedule_string):
    schedule_string = replace_characters(schedule_string)
    # Split the data into separate schedules by day
    schedules_by_day = {}
    date = None
    current_day = None
    current_schedule = None
    current_year = datetime.datetime.now().year  # get the current year
    previous_date = None
    for line in schedule_string.split('\n'):
        # Check if the line contains a day of the week
        if re.search(r'\b(M[o|n|t|u|e|w|d|t|h|f|s|a|u]{2,5}?|Tu[e|s]{1,2}?|We[d]{1,2}?|Thu[r]{1,2}?|Fri|Sat|Sun)\w*\b', line):
            current_day = line.strip()
            current_schedule = []
            schedules_by_day[current_day] = current_schedule
            month_day_match = re.search(r'\b(January|February|March|April|May|June|July|August|September|October|November|December)\s(\d{1,2})\b', current_day)
            if month_day_match:
                month = month_day_match.group(1)
                day = int(month_day_match.group(2))
            if day > calendar.monthrange(current_year,datetime.datetime.strptime(month, '%B').month)[1]:
                month_day_match = None
            
            if month_day_match:
                date = datetime.datetime(current_year, datetime.datetime.strptime(month, '%B').month, day)
                previous_date = date
            elif previous_date:
                previous_date += datetime.timedelta(days=1)
                date = previous_date
                print("Couldnt find the date for this entry, compensating: ",line, "new date is: ",date) 
            else:
                print("Couldnt find the date for this entry: ",line)        
        elif current_schedule is not None:
            worker_match = re.search(r'([A-Z\s]+)\s+(\d+):(\d+)\s+([ap]m)\s+(\d+):(\d+)\s+([ap]m)', line)
            if worker_match:
                name = worker_match.group(1).strip()
                start_hour = int(worker_match.group(2))
                start_ampm = worker_match.group(4)
                end_hour = int(worker_match.group(5))
                end_ampm = worker_match.group(7)
                
                if end_ampm == 'pm':
                    if end_hour > 11:
                        end_hour = 11
                        
                        
                start_time = str(start_hour)+':00 '+start_ampm
                end_time = str(end_hour)+':00 '+end_ampm
                current_schedule.append({
                    'name': name if name else 'ERROR',
                    'start_time': start_time if start_time else 'ERROR',
                    'end_time': end_time if end_time else 'ERROR',
                    'date': date.strftime('%B %d %Y') if date else 'ERROR'
                })
    
    return schedules_by_day

def filter_schedule_by_worker(schedule_by_day, worker_name):
    for day, schedule in schedule_by_day.items():
        filtered_schedule = list(filter(lambda shift: any(substring.lower() in shift['name'].lower() for substring in worker_name.split()), schedule))
        schedule_by_day[day] = filtered_schedule
    return schedule_by_day

def sanitize(value):
    if value is None:
        return ''
    """Replace illegal characters in value with an underscore"""
    valid_chars = f"-_.(): {string.ascii_letters}{string.digits}"
    return ''.join(c if c in valid_chars else '_' for c in value)

def write_to_excel(schedule_by_day, output_file):
    try:
        print("If you want to filter by employee name (otherwise enter nothing): ")
        name = input()
        if name:
            schedule_by_day = filter_schedule_by_worker(schedule_by_day, str.upper(name))
        # Create an empty list to hold the rows of the final output
        rows = []

        # Loop through each day in the schedule
        for day, workers in schedule_by_day.items():
            # Loop through each worker for the current day
            for worker in workers:
                # Create a new row with the day, date, name, start time, and end time
                row = [day, worker['date'], worker['name'], worker['start_time'], worker['end_time']]
                # Append the row to the list of rows
                rows.append(row)

        # Create a DataFrame from the list of rows
        dataframe = pd.DataFrame(rows, columns=['Day', 'Date', 'Name', 'Start Time', 'End Time'])

        # Sanitize dataframe values
        dataframe = dataframe.applymap(sanitize)

        # Write dataframe to Excel spreadsheet
        dataframe.to_excel(output_file, index=False)

    except IllegalCharacterError as e:
        print(f"Error: {e}")