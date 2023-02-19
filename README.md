# ScheduleScanner

A python script that takes in many images of employee shift times and processes and formats the data and outputs an excel file.

Ideal image data will be straight on with no shadows. Here's an example of the schedule format

<img src="example.jpg" width="300" >

The program will output debug images of the opencv process to show the processed image as well as the ocr text recognition boxes if the image is not being read right.

<img src="exampledebug.jpg" width="300" >

There's also a script called ical.py that if you run it will create an ical file of the excel file in your schedule folder so you can import it into your favorite calendar app.
