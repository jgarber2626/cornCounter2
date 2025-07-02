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
#cap = cv2.VideoCapture('video_col992_row3.h264')
#cap = cv2.VideoCapture('video_col6_row7.h264')
#cap = cv2.VideoCapture('video_col222_row7.h264')
#cap = cv2.VideoCapture('video_col3_row61.h264')

i =18
video_folder = "Good Videoss"

video_files = [f for f in os.listdir(video_folder)]


windowWidth = 600
windowWidthCropped = int((windowWidth / 3))
windowHeight = int(1920 / 3)

print(video_files)
if not video_files:
    print("No video files found in the specified folder")


for video_file in video_files:
    video_path = os.path.join(video_folder, video_file)

    print(video_path)
    cap = cv2.VideoCapture(video_path)

    #z variable is to track small plants to see if they are already taken into account.
    #q variable is the indicator that there is a a stalk that did not get picked up the by the normal counter
    #but has enough green HSV values to get picked up by the bigContour code.
    z=0
    q=0

    images = []
    jpegNumber = 0
    initBB = None
    s = 0
    Rang = 3
    Row = 1

    #This loads the video that you would like to analyze
    #cap = cv2.VideoCapture('video_col224_row1.h264')

    w, h, fps = (int(cap.get(x)) for x in (cv2.CAP_PROP_FRAME_WIDTH, cv2.CAP_PROP_FRAME_HEIGHT, cv2.CAP_PROP_FPS))
    output_filename = f"{video_file[:-4]}.mp4"
    #print(w,h,fps)
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')

    #Use this code when trying to narrow a video to just the row.
    video_writer = cv2.VideoWriter(output_filename, fourcc, fps,(int(windowWidthCropped), windowHeight))
    print(windowHeight)
    print(windowWidthCropped)


    contourXPoints = []
    contourYPoints = []
    contourPoints = []

    while cap.isOpened():

        ## grab the current frame, then handle if we are using a
        # VideoStream or VideoCapture object
        ret, frame = cap.read()

        #If no frame, usually becasue the video has ended, the loop will end.
        if frame is None:
            break

        #This will rotate the video 90 degrees so that the corn are moving from the bottom of the screen to the top of the screen
        #If this code is needed, you will need to update lines 58, 236, 239, 242.
        frame = cv2.rotate(frame,cv2.ROTATE_90_COUNTERCLOCKWISE)



        crop_frame = frame





        #Use Gaussian Blur to blur video. The blur allows the computer to better threshold because it
        #takes out outlier pixel colors within a corn plant and give the corn plant an average green
        #color. Note that Gaussian Blur must be an odd number (ie. 15)
        crop_frame = cv2.GaussianBlur(crop_frame, (9, 9), cv2.BORDER_DEFAULT)

        """crop_frame = cv2.resize(crop_frame,(int(crop_frame.shape[1]/2.5),int(crop_frame.shape[0]/2.5)))
        print(crop_frame.shape[0])"""




        #Convert frame to HSV for image analysis
        hsv_nemo = cv2.cvtColor(crop_frame, cv2.COLOR_RGB2HSV)


        #These are the ranges to eliminate the ground behind the corn stalks. We first try to eliminate (make the background black) first
        #so that our next inRange function focusing on just the areas around the corn.
        light_orange = (100, 0, 30)
        dark_orange = (255, 255, 255)
        mask = cv2.inRange(hsv_nemo, light_orange, dark_orange)

        light_orange = (0, 0, 30)
        dark_orange = (255, 25, 255)
        mask = cv2.inRange(hsv_nemo, light_orange, dark_orange)

        #cv2.imshow("Frame8", mask)

        #First we swap the white and black colors so that the erode function makes the ground (black) section larger and eliminates
        #any small green areas in the frame.
        mask = cv2.bitwise_not(mask)
        kernel = np.ones((5, 5), np.uint8)
        mask = cv2.erode(mask, kernel, iterations=1)


        #The bitwise_and function adjusts the crop_frame picture to add (eliminate the parts of the picture that are dirt)
        # any black space that was in the mask created above.
        Only_plants = cv2.bitwise_and(crop_frame, crop_frame, mask = mask)

        #Converts the new picture that eliminated the dirt background to HSV.
        Only_plants = cv2.cvtColor(Only_plants, cv2.COLOR_RGB2HSV)

        #cv2.imshow("frame4", Only_plants)

        #The ranges below should be the ranges of green hsv color.
        light_orange = (25, 60,30)
        dark_orange = (75, 255, 222)
        #This is the mask range to get the contour of the swirl at v2/v3
        light_orange = (55, 190, 30)
        dark_orange = (85, 255, 240)
        light_orange = (55, 160, 30)
        dark_orange = (85, 255, 240)
        mask = cv2.inRange(Only_plants, light_orange, dark_orange)

        light_orange = (0, 0, 0)
        dark_orange = (0, 0, 0)
        mask8 = cv2.inRange(hsv_nemo, light_orange, dark_orange)

        result = cv2.bitwise_or(mask,mask8)
        #cv2.imshow("maskadd", mask)

        #find the contours in the mask. These contours are the green corn stalks.
        contours, hierarchy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)


        #This for loop goes through and finds any contours that have an area greater than 6000 pixels and will fill it in with white. If
        #the contour is smaller than 10 pixels, it assumes that contour is not a corn stalk and fills in the contour with black.
        i = 0
        for c in contours:

            if cv2.contourArea(c) < 5:
                cv2.drawContours(mask, contours, i, (0,0,0), thickness=cv2.FILLED)
                i+=1
                continue
            else:
                cv2.drawContours(mask, contours, i, (255,255,255), thickness=cv2.FILLED)
                i+=1

        #After the analysis of contour area, we find the new contours on the mask.
        contours, hierarchy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)



        #This dilate makes the white sections (corn stalks) larger by 11 pixels.
        kernel = np.ones((20, 20), np.uint8)
        mask = cv2.dilate(mask,kernel,iterations=1)




        #find of contours after the most recent dilation.
        contours, hierarchy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)


        #This try/for loop looks to find if any of the contours are inside of another contour. If it is,
        #inside another contour, it is assumed the contour is inside a corn stalk so we fill it with white pixels.
        i=0
        try:
            for h in hierarchy[0]:

                if h[3] != -1:
                    cv2.drawContours(mask, contours, i, (255, 255, 255), thickness=cv2.FILLED)
                i += 1
        except:
            r = 1



        # find of contours after the most recent for loop
        contours, hierarchy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)


        #this for loop finds the middle of each contour and saves it in teh contourPoints list.
        for c in contours:

            M = cv2.moments(c)

            try:
                # print(M)
                cX = int(M["m10"] / M["m00"])
                cY = int(M["m01"] / M["m00"])
                print(cY)
                contourXPoints.append(cX)
                contourYPoints.append(cY)
                contourPoints.append((cX, cY))
                if len(contourXPoints) > 25:
                    del contourXPoints[0]
                    del contourYPoints[0]
            except:
                x = 1



        #The try function gets the average x middle and y middle of the contours so that we can adjust the frame and only see
        #the corn row.
        try:
            xMiddle = sum(contourXPoints) / len(contourXPoints)
            yMiddle = sum(contourYPoints) / len(contourYPoints)
        except:
            print("no contours")

        #If there are no contours on the first picture, we give the xMiddle as the middle of the screen
        try:
            xMiddle

        except:
            xMiddle = crop_frame.shape[1]/2




        #based on the centroids of the contours, I narrow the mask image so it is focused on the row and does not look at anything outside a 300 pixel width
        #mask = mask[1:mask.shape[0], (int(xMiddle) - 100):(int(xMiddle) + 100)]

        frame_width = frame.shape[1]

        # Ensure xMiddle is an integer
        xMiddle = int(xMiddle)
        #print(xMiddle)

        # Calculate left and right bounds safely
        half_crop_width = int(windowWidth/2)
        left = max(0, xMiddle - half_crop_width)
        right = left + windowWidth

        # Adjust if right goes beyond the frame width
        if right > frame_width:
            right = frame_width
            left = max(0, right - windowWidth)

        # Crop the frame
        crop_frame_Writing = frame[0:frame.shape[0], left:right]

        #crop_frame_Writing=frame[0:frame.shape[0], (int(xMiddle) - 240):(int(xMiddle) + 240)]
        #crop_frame1 = crop_frame
        try:
            crop_frame_Writing = cv2.resize(crop_frame_Writing,(windowWidthCropped,windowHeight))
            #print(crop_frame_Writing.shape)
        except:
            print(crop_frame_Writing.shape)
        if crop_frame_Writing.shape[0] == windowHeight and crop_frame_Writing.shape[1] == windowWidthCropped:
            #use the code below when writing a croped frame
            video_writer.write(crop_frame_Writing)
            #use th code below when writing the original frame



        #print(ct.objects)
        #print(ct.disappeared)

        #cv2.imshow("Frame", crop_frame1)

        #this if statment checks if q = 1. If so that indicates that we found a small plant that was not counted
        #but we took a picture of it so we should start counting the z variable to know that after 6 frames,
        #the small plant will be out of the video.
        if q==1:
            z+=1
        #key = cv2.waitKey(0) & 0xFF == ord('q')


time.sleep(4)
video_writer.release()
cv2.destroyAllWindows()