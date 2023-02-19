import pandas as pd
from icalendar import Calendar, Event
from datetime import datetime

# Read the data from the input file
df = pd.read_excel('schedule/all.xlsx')

# Create a new calendar
cal = Calendar()

# Iterate through the rows of the DataFrame
for index, row in df.iterrows():

    # Extract the values from the row
    date_str = row['Date']
    name = row['Name']
    start_time_str = row['Start Time']
    end_time_str = row['End Time']

    # Parse the date string and create a datetime object
    date_obj = datetime.strptime(date_str, '%B %d %Y')

    # Parse the start time string and create a datetime object
    start_time_obj = datetime.strptime(start_time_str, '%I:%M %p').time()

    # Parse the end time string and create a datetime object
    end_time_obj = datetime.strptime(end_time_str, '%I:%M %p').time()

    # Combine the date and start time into a single datetime object
    start_datetime = datetime.combine(date_obj, start_time_obj)

    # Combine the date and end time into a single datetime object
    end_datetime = datetime.combine(date_obj, end_time_obj)

    # Create a new event
    event = Event()

    # Set the event details
    event.add('summary', name)
    event.add('dtstart', start_datetime)
    event.add('dtend', end_datetime)

    # Add the event to the calendar
    cal.add_component(event)

# Write the calendar to a file
with open('cal.ics', 'wb') as f:
    f.write(cal.to_ical())