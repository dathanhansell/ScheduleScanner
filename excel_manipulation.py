import pandas as pd
import string
from openpyxl.utils.exceptions import IllegalCharacterError
import datetime
import re

def parse_schedule(schedule_data):
    # Split the data into separate schedules by day
    schedules_by_day = {}
    current_day = None
    current_schedule = None
    for line in schedule_data.split('\n'):
        # Check if the line contains a day of the week
        if re.search(r'\b(Monday|Tuesday|Wednesday|Thursday|Friday|Saturday|Sunday)\b', line):
            current_day = line.strip()
            current_schedule = []
            schedules_by_day[current_day] = current_schedule
        elif current_schedule is not None:
            match = re.search(r'([A-Z\s]+)\s+(\d+:\d+ [ap]m)\s+(\d+:\d+ [ap]m)', line)
            if match:
                name = match.group(1).strip()
                start_time = match.group(2)
                end_time = match.group(3)
                current_schedule.append({'name': name, 'start_time': start_time, 'end_time': end_time, 'date': current_day})
            else:
                current_schedule.append({'name': match, 'start_time': 'ERROR', 'end_time': 'ERROR', 'date': 'ERROR'})

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
    valid_chars = f"-_.() {string.ascii_letters}{string.digits}"
    return ''.join(c if c in valid_chars else '_' for c in value)

def write_to_excel(schedule_by_day, output_file):
    try:
        #schedule_by_day = filter_schedule_by_worker(schedule_by_day, "HANNAH SWIECKI")
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