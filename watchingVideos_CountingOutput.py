import time
import cv2
from datetime import datetime

import time
import cv2
import numpy as np
import sys
import os
import re
import openpyxl
from tkinter import Tk, filedialog

#This loads the video that you would like to analyze
#cap = cv2.VideoCapture('row9.mp4')
#cap = cv2.VideoCapture('video_col992_row3.h264')qqqqqqq
#cap = cv2.VideoCapture('video_col6_row7.h264')
#cap = cv2.VideoCapture('video_col222_row7.h264')
#cap = cv2.VideoCapturqqe('video_col3_row61.h264')

i =18
video_folder = "Output Videos"
video_files = [f for f in os.listdir(video_folder)]

print(video_files)
if not video_files:
    print("No video files found in the specified folder")


for video_file in video_files:
    video_path = os.path.join(video_folder, video_file)

    print(video_path)
    cap = cv2.VideoCapture(video_path)

    while cap.isOpened():
        ret, frame = cap.read()

        if frame is None:
            break

        #frame = cv2.resize(frame,(int(frame.shape[1]*2),int(frame.shape[0]*2)))
        line_y = int(frame.shape[0] * 0.5)
        cv2.line(frame, (0, line_y), (frame.shape[1], line_y), (0, 0, 255), 2)
        #qqqqqqqqqqcv2.line(frame, (0, line_y+30), (frame.shape[1], line_y+30), (0, 0, 255), 2)# Example: red line with thickness 2
        cv2.imshow("s", frame)
        i += 1
        #time.sleep(.5)
        cv2.waitKey(0) & 0xFF == ord('q')

cv2.destroyAllWindows()

"""
while True:

    ## grab the current frame, then handle if we are using a
    # VideoStream or VideoCapture object
    ret, frame = cap.read()
    crop_frame = cv2.resize(frame, (int(frame.shape[1] / 2.5), int(frame.shape[0] / 2.5)))

    #time.sleep(0.1)

    #If no frame, usually becasue the video has ended, the loop will end.
    if frame is None:
        break


    #crop_frame = frame[0:1920,0:1080]
    cv2.imshow("s", crop_frame)
    if i % 8 ==0:
        current_time=datetime.now()
        timestamp_string = current_time.strftime("%Y-%m-%d %H:%M:%S")
        filename_addition = str(timestamp_string + str(i))
        filename = "Pictures/%s.jpg" % i
        cv2.imwrite(filename, frame)

    i+=1
    time.sleep(.01)
    if cv2.waitKey(25) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()
"""