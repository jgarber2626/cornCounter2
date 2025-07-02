from tkinter import *
from picamera import PiCamera
from time import sleep
import time
import RPi.GPIO as GPIO
from picamera2 import Picamera2, Preview
from picamera2.encoders import H264Encoder

picam2 = Picamera2()
camera_config = picam2.create_still_configuration(main={"size": (1920, 1080)}, lores={"size": (640, 480)}, display="lores")
picam2.configure(camera_config)

def take_Picture(channel):
    global counter
    global rowCounter
    global hPath
    global serpCounter
    global currentRow
    global restartDirectionIndicator

    # code for taking pictures when beginning on a field already started previously
    if directionIndicator == 1 and hPath == "Direct" and harvestDirection == "Last Range, Last Row":
        if counter < (int(fRanges) - 1):

            counter += 1
            newestLabel = Label(root, text=str(counter + 1) + "/" + str(int(sRow) + rowCounter), padx=3, bg="green")
            newestLabel.grid(row=(int(fRanges) - counter + 1), column=(int(sRow) + rowCounter))
            frame = (locationGet + str(counter + 1) + "." + str(int(sRow) + rowCounter) + fieldGet)
            output_directory = "/home/pi/Desktop/Images/"
            frame = output_directory+str(frame) + ".jpg"
            picam2.start()
            
            picam2.capture_file(frame)
            picam2.stop()
        else:

            counter = 0
            rowCounter += 1
            newestLabel = Label(root, text=str(counter + 1) + "/" + str(int(sRow) + rowCounter), padx=3,
                                bg="green")
            newestLabel.grid(row=(int(fRanges) - counter + 1), column=(int(sRow) + rowCounter))
            print("Turning Around after row" + str(rowCounter))

    if directionIndicator == 1 and hPath == "Direct" and harvestDirection == "Last Range, First Row":
        if counter < (int(fRanges) - 1):
            counter += 1
            newestLabel = Label(root, text=str(counter + 1) + "/" + str(int(sRow) - rowCounter), padx=3, bg="green")
            newestLabel.grid(row=(int(fRanges) - counter + 1), column=(int(sRow) - rowCounter))
            frame = (locationGet + str(counter + 1) + "." + str(int(sRow) - rowCounter) + fieldGet)
            output_directory = "/home/pi/Desktop/Images/"
            frame = output_directory+str(frame) + ".jpg"
            picam2.start()
            
            picam2.capture_file(frame)
            picam2.stop()
        else:
            counter = 0
            rowCounter += 1
            newestLabel = Label(root, text=str(counter + 1) + "/" + str(int(sRow) - rowCounter), padx=3,
                                bg="green")
            newestLabel.grid(row=(int(fRanges) - counter + 1), column=(int(sRow) - rowCounter))
            print("Turning Around after row" + str(rowCounter))

    if directionIndicator == 1 and hPath == "Direct" and harvestDirection == "First Range, Last Row":
        if counter > (int(0)):
            counter = counter - 1
            newestLabel = Label(root, text=str(counter + 1) + "/" + str(int(sRow) + rowCounter), padx=3, bg="green")
            newestLabel.grid(row=(int(fRanges) - counter + 1), column=(int(sRow) + rowCounter))
            frame = (locationGet + str(counter + 1) + "." + str(int(sRow) + rowCounter) + fieldGet)
            output_directory = "/home/pi/Desktop/Images/"
            frame = output_directory+str(frame) + ".jpg"
            picam2.start()
            
            picam2.capture_file(frame)
            picam2.stop()
        else:
            counter = int(fRanges) - 1
            rowCounter += 1
            newestLabel = Label(root, text=str(int(fRanges)) + "/" + str(int(sRow) + rowCounter), padx=3,
                                bg="green")
            newestLabel.grid(row=(2), column=(int(sRow) + rowCounter))
            print("Turning Around" + str(rowCounter))

    if directionIndicator == 1 and hPath == "Direct" and harvestDirection == "First Range, First Row":
        if counter > (int(0)):
            counter = counter - 1
            newestLabel = Label(root, text=str(counter + 1) + "/" + str(int(sRow) - rowCounter), padx=3, bg="green")
            newestLabel.grid(row=(int(fRanges) - counter + 1), column=(int(sRow) - rowCounter))
            frame = (locationGet + str(counter + 1) + "." + str(int(sRow) - rowCounter) + fieldGet)
            output_directory = "/home/pi/Desktop/Images/"
            frame = output_directory+str(frame) + ".jpg"
            picam2.start()
            
            picam2.capture_file(frame)
            picam2.stop()

        else:
            counter = int(fRanges) - 1
            rowCounter += 1
            newestLabel = Label(root, text=str(int(fRanges)) + "/" + str(int(sRow) - rowCounter), padx=3,
                                bg="green")
            newestLabel.grid(row=(2), column=(int(sRow) - rowCounter))
            print("Turning Around" + str(rowCounter))

    if directionIndicator == 1 and hPath == "Serpentine" and harvestDirection == "Last Range, Last Row":
        if restartDirectionIndicator == 1:
            if counter < (int(fRanges) - 1) and int(serpCounter) % 2 == 0:
                counter += 1
                newestLabel = Label(root, text=str(counter + 1) + "/" + str(int(sRow) + rowCounter), padx=3, bg="green")
                newestLabel.grid(row=(int(fRanges) - counter + 1), column=(int(sRow) + rowCounter))
                frame = (locationGet + str(counter + 1) + "." + str(int(sRow) + rowCounter) + fieldGet)
                output_directory = "/home/pi/Desktop/Images/"
                frame = output_directory+str(frame) + ".jpg"
                picam2.start()
            
                picam2.capture_file(frame)
                picam2.stop()
            elif counter < (int(fRanges) - 1) and int(serpCounter) % 2 == 1:
                counter += 1
                newestLabel = Label(root, text=str(int(fRanges) - counter) + "/" + str(int(sRow) + rowCounter), padx=3,
                                    bg="green")
                newestLabel.grid(row=(int(fRanges) - int(fRanges) + counter + 2), column=(int(sRow) + rowCounter))
                frame = (locationGet + str(int(fRanges) - counter) + "." + str(int(sRow) + rowCounter) + fieldGet)
                output_directory = "/home/pi/Desktop/Images/"
                frame = output_directory+str(frame) + ".jpg"
                picam2.start()
            
                picam2.capture_file(frame)
                picam2.stop()

            else:
                counter = 0
                rowCounter += 1
                serpCounter += 1
                if serpCounter % 2 == 0:
                    newestLabel = Label(root, text=str(int(1)) + "/" + str(int(sRow) + rowCounter),
                                        padx=3,
                                        bg="green")
                    newestLabel.grid(row=(int(fRanges) + 1), column=(int(sRow) + rowCounter))
                    print("Turning Around" + str(rowCounter))
                else:
                    newestLabel = Label(root, text=str(int(fRanges) + counter) + "/" + str(int(sRow) + rowCounter),
                                        padx=3,
                                        bg="green")
                    newestLabel.grid(row=(int(fRanges) - int(fRanges) - counter + 2), column=(int(sRow) + rowCounter))
                    print("Turning Around" + str(rowCounter))

        else:
            if counter > (int(0)) and int(serpCounter) % 2 == 0:
                counter = counter - 1
                newestLabel = Label(root, text=str(counter + 1) + "/" + str(int(sRow) + rowCounter), padx=3, bg="green")
                newestLabel.grid(row=(int(fRanges) - counter + 1), column=(int(sRow) + rowCounter))
                frame = (locationGet + str(counter + 1) + "." + str(int(sRow) + rowCounter) + fieldGet)
                output_directory = "/home/pi/Desktop/Images/"
                frame = output_directory+str(frame) + ".jpg"
                picam2.start()
            
                picam2.capture_file(frame)
                picam2.stop()

            elif counter < (int(fRanges) - 1) and int(serpCounter) % 2 == 1:
                counter += 1
                newestLabel = Label(root, text=str(counter + 1) + "/" + str(int(sRow) + rowCounter), padx=3, bg="green")
                newestLabel.grid(row=(int(fRanges) - counter + 1), column=(int(sRow) + rowCounter))
                frame = (locationGet + str(counter + 1) + "." + str(int(sRow) + rowCounter) + fieldGet)
                output_directory = "/home/pi/Desktop/Images/"
                frame = output_directory+str(frame) + ".jpg"
                picam2.start()
            
                picam2.capture_file(frame)
                picam2.stop()


            else:

                rowCounter += 1
                serpCounter += 1
                if serpCounter % 2 == 0:
                    counter = int(fRanges) - 1
                    newestLabel = Label(root, text=str(int(fRanges)) + "/" + str(int(sRow) + rowCounter), padx=3,
                                        bg="green")
                    newestLabel.grid(row=(2), column=(int(sRow) + rowCounter))
                    print("Turning Around" + str(rowCounter))
                else:
                    counter = 0
                    newestLabel = Label(root, text=str(1) + "/" + str(int(sRow) + rowCounter), padx=3,
                                        bg="green")
                    newestLabel.grid(row=(int(fRanges) - int(1) - counter + 2), column=(int(sRow) + rowCounter))
                    print("Turning Around" + str(rowCounter))

    if directionIndicator == 1 and hPath == "Serpentine" and harvestDirection == "First Range, Last Row":
        if restartDirectionIndicator == 0:
            if counter < (int(fRanges) - 1) and int(serpCounter) % 2 == 0:
                counter += 1
                newestLabel = Label(root, text=str(counter + 1) + "/" + str(int(sRow) + rowCounter), padx=3, bg="green")
                newestLabel.grid(row=(int(fRanges) - counter + 1), column=(int(sRow) + rowCounter))
                frame = (locationGet + str(counter + 1) + "." + str(int(sRow) + rowCounter) + fieldGet)
                output_directory = "/home/pi/Desktop/Images/"
                frame = output_directory+str(frame) + ".jpg"
                picam2.start()
            
                picam2.capture_file(frame)
                picam2.stop()
            elif counter < (int(fRanges) - 1) and int(serpCounter) % 2 == 1:
                counter += 1
                newestLabel = Label(root, text=str(int(fRanges) - counter) + "/" + str(int(sRow) + rowCounter), padx=3,
                                    bg="green")
                newestLabel.grid(row=(int(fRanges) - int(fRanges) + counter + 2), column=(int(sRow) + rowCounter))
                frame = (locationGet + str(int(fRanges) - counter) + "." + str(int(sRow) + rowCounter) + fieldGet)
                output_directory = "/home/pi/Desktop/Images/"
                frame = output_directory+str(frame) + ".jpg"
                picam2.start()
                
                picam2.capture_file(frame)
                picam2.stop()

            else:
                counter = 0
                rowCounter += 1
                serpCounter += 1
                if serpCounter % 2 == 0:
                    newestLabel = Label(root, text=str(int(1)) + "/" + str(int(sRow) + rowCounter),
                                        padx=3,
                                        bg="green")
                    newestLabel.grid(row=(int(fRanges) + 1), column=(int(sRow) + rowCounter))
                    print("Turning Around" + str(rowCounter))
                else:
                    newestLabel = Label(root, text=str(int(fRanges) + counter) + "/" + str(int(sRow) + rowCounter),
                                        padx=3,
                                        bg="green")
                    newestLabel.grid(row=(int(fRanges) - int(fRanges) - counter + 2), column=(int(sRow) + rowCounter))
                    print("Turning Around" + str(rowCounter))

        else:
            if counter > (int(0)) and int(serpCounter) % 2 == 0:
                counter = counter - 1
                newestLabel = Label(root, text=str(counter + 1) + "/" + str(int(sRow) + rowCounter), padx=3, bg="green")
                newestLabel.grid(row=(int(fRanges) - counter + 1), column=(int(sRow) + rowCounter))
                frame = (locationGet + str(counter + 1) + "." + str(int(sRow) + rowCounter) + fieldGet)
                output_directory = "/home/pi/Desktop/Images/"
                frame = output_directory+str(frame) + ".jpg"
                picam2.start()
                
                picam2.capture_file(frame)
                picam2.stop()

            elif counter < (int(fRanges) - 1) and int(serpCounter) % 2 == 1:
                counter += 1
                newestLabel = Label(root, text=str(counter + 1) + "/" + str(int(sRow) + rowCounter), padx=3, bg="green")
                newestLabel.grid(row=(int(fRanges) - counter + 1), column=(int(sRow) + rowCounter))
                frame = (locationGet + str(counter + 1) + "." + str(int(sRow) + rowCounter) + fieldGet)
                output_directory = "/home/pi/Desktop/Images/"
                frame = output_directory+str(frame) + ".jpg"
                picam2.start()
                
                picam2.capture_file(frame)
                picam2.stop()


            else:

                rowCounter += 1
                serpCounter += 1
                if serpCounter % 2 == 0:
                    counter = int(fRanges) - 1
                    newestLabel = Label(root, text=str(int(fRanges)) + "/" + str(int(sRow) + rowCounter), padx=3,
                                        bg="green")
                    newestLabel.grid(row=(2), column=(int(sRow) + rowCounter))
                    print("Turning Around" + str(rowCounter))
                else:
                    counter = 0
                    newestLabel = Label(root, text=str(1) + "/" + str(int(sRow) + rowCounter), padx=3,
                                        bg="green")
                    newestLabel.grid(row=(int(fRanges) - int(1) - counter + 2), column=(int(sRow) + rowCounter))
                    print("Turning Around" + str(rowCounter))

    if directionIndicator == 1 and hPath == "Serpentine" and harvestDirection == "First Range, First Row":
        if int(currentRow) % 2 == 0:
            if counter < (int(fRanges) - 1) and int(serpCounter) % 2 == 0:
                counter += 1
                newestLabel = Label(root, text=str(counter + 1) + "/" + str(int(sRow) - rowCounter), padx=3, bg="green")
                newestLabel.grid(row=(int(fRanges) - counter + 1), column=(int(sRow) - rowCounter))
                frame = (locationGet + str(counter + 1) + "." + str(int(sRow) - rowCounter) + fieldGet)
                output_directory = "/home/pi/Desktop/Images/"
                frame = output_directory+str(frame) + ".jpg"
                picam2.start()
                
                picam2.capture_file(frame)
                picam2.stop()
            elif counter < (int(fRanges) - 1) and int(serpCounter) % 2 == 1:
                counter += 1
                newestLabel = Label(root, text=str(int(fRanges) - counter) + "/" + str(int(sRow) - rowCounter), padx=3,
                                    bg="green")
                newestLabel.grid(row=(int(fRanges) - int(fRanges) + counter + 2), column=(int(sRow) - rowCounter))
                frame = (locationGet + str(int(fRanges) - counter) + "." + str(int(sRow) - rowCounter) + fieldGet)
                output_directory = "/home/pi/Desktop/Images/"
                frame = output_directory+str(frame) + ".jpg"
                picam2.start()
                
                picam2.capture_file(frame)
                picam2.stop()

            else:
                counter = 0
                rowCounter += 1
                serpCounter += 1
                if serpCounter % 2 == 0:
                    newestLabel = Label(root, text=str(int(1)) + "/" + str(int(sRow) - rowCounter),
                                        padx=3,
                                        bg="green")
                    newestLabel.grid(row=(int(fRanges) + 1), column=(int(sRow) - rowCounter))
                    print("Turning Around" + str(rowCounter))
                else:
                    newestLabel = Label(root, text=str(int(fRanges) + counter) + "/" + str(int(sRow) - rowCounter),
                                        padx=3,
                                        bg="green")
                    newestLabel.grid(row=(int(fRanges) - int(fRanges) - counter + 2), column=(int(sRow) - rowCounter))
                    print("Turning Around" + str(rowCounter))

        else:
            if counter > (int(0)) and int(serpCounter) % 2 == 0:
                counter = counter - 1
                newestLabel = Label(root, text=str(counter + 1) + "/" + str(int(sRow) - rowCounter), padx=3, bg="green")
                newestLabel.grid(row=(int(fRanges) - counter + 1), column=(int(sRow) - rowCounter))
                frame = (locationGet + str(counter + 1) + "." + str(int(sRow) - rowCounter) + fieldGet)
                output_directory = "/home/pi/Desktop/Images/"
                frame = output_directory+str(frame) + ".jpg"
                picam2.start()
                
                picam2.capture_file(frame)
                picam2.stop()

            elif counter < (int(fRanges) - 1) and int(serpCounter) % 2 == 1:
                counter += 1
                newestLabel = Label(root, text=str(counter + 1) + "/" + str(int(sRow) - rowCounter), padx=3, bg="green")
                newestLabel.grid(row=(int(fRanges) - counter + 1), column=(int(sRow) - rowCounter))
                frame = (locationGet + str(counter + 1) + "." + str(int(sRow) - rowCounter) + fieldGet)
                output_directory = "/home/pi/Desktop/Images/"
                frame = output_directory+str(frame) + ".jpg"
                picam2.start()
                
                picam2.capture_file(frame)
                picam2.stop()


            else:

                rowCounter += 1
                serpCounter += 1
                if serpCounter % 2 == 0:
                    counter = int(fRanges) - 1
                    newestLabel = Label(root, text=str(int(fRanges)) + "/" + str(int(sRow) - rowCounter), padx=3,
                                        bg="green")
                    newestLabel.grid(row=(2), column=(int(sRow) - rowCounter))
                    print("Turning Around" + str(rowCounter))
                else:
                    counter = 0
                    newestLabel = Label(root, text=str(1) + "/" + str(int(sRow) - rowCounter), padx=3,
                                        bg="green")
                    newestLabel.grid(row=(int(fRanges) - int(1) - counter + 2), column=(int(sRow) - rowCounter))
                    print("Turning Around" + str(rowCounter))

    if directionIndicator == 1 and hPath == "Serpentine" and harvestDirection == "Last Range, First Row":
        if int(currentRow) % 2 == 1:
            if counter < (int(fRanges) - 1) and int(serpCounter) % 2 == 0:
                counter += 1
                newestLabel = Label(root, text=str(counter + 1) + "/" + str(int(sRow) - rowCounter), padx=3, bg="green")
                newestLabel.grid(row=(int(fRanges) - counter + 1), column=(int(sRow) - rowCounter))
                frame = (locationGet + str(counter + 1) + "." + str(int(sRow) - rowCounter) + fieldGet)
                output_directory = "/home/pi/Desktop/Images/"
                frame = output_directory+str(frame) + ".jpg"
                picam2.start()
                
                picam2.capture_file(frame)
                picam2.stop()
            elif counter < (int(fRanges) - 1) and int(serpCounter) % 2 == 1:
                counter += 1
                newestLabel = Label(root, text=str(int(fRanges) - counter) + "/" + str(int(sRow) - rowCounter), padx=3,
                                    bg="green")
                newestLabel.grid(row=(int(fRanges) - int(fRanges) + counter + 2), column=(int(sRow) - rowCounter))
                frame = (locationGet + str(int(fRanges) - counter) + "." + str(int(sRow) - rowCounter) + fieldGet)
                output_directory = "/home/pi/Desktop/Images/"
                frame = output_directory+str(frame) + ".jpg"
                picam2.start()
                
                picam2.capture_file(frame)
                picam2.stop()

            else:
                counter = 0
                rowCounter += 1
                serpCounter += 1
                if serpCounter % 2 == 0:
                    newestLabel = Label(root, text=str(int(1)) + "/" + str(int(sRow) - rowCounter),
                                        padx=3,
                                        bg="green")
                    newestLabel.grid(row=(int(fRanges) + 1), column=(int(sRow) - rowCounter))
                    print("Turning Around" + str(rowCounter))
                else:
                    newestLabel = Label(root, text=str(int(fRanges) + counter) + "/" + str(int(sRow) - rowCounter),
                                        padx=3,
                                        bg="green")
                    newestLabel.grid(row=(int(fRanges) - int(fRanges) - counter + 2), column=(int(sRow) - rowCounter))
                    print("Turning Around" + str(rowCounter))

        else:
            if counter > (int(0)) and int(serpCounter) % 2 == 0:
                counter = counter - 1
                newestLabel = Label(root, text=str(counter + 1) + "/" + str(int(sRow) - rowCounter), padx=3, bg="green")
                newestLabel.grid(row=(int(fRanges) - counter + 1), column=(int(sRow) - rowCounter))
                frame = (locationGet + str(counter + 1) + "." + str(int(sRow) - rowCounter) + fieldGet)
                output_directory = "/home/pi/Desktop/Images/"
                frame = output_directory+str(frame) + ".jpg"
                picam2.start()
                
                picam2.capture_file(frame)
                picam2.stop()

            elif counter < (int(fRanges) - 1) and int(serpCounter) % 2 == 1:
                counter += 1
                newestLabel = Label(root, text=str(counter + 1) + "/" + str(int(sRow) - rowCounter), padx=3, bg="green")
                newestLabel.grid(row=(int(fRanges) - counter + 1), column=(int(sRow) - rowCounter))
                frame = (locationGet + str(counter + 1) + "." + str(int(sRow) - rowCounter) + fieldGet)
                output_directory = "/home/pi/Desktop/Images/"
                frame = output_directory+str(frame) + ".jpg"
                picam2.start()
                
                picam2.capture_file(frame)
                picam2.stop()


            else:

                rowCounter += 1
                serpCounter += 1
                if serpCounter % 2 == 0:
                    counter = int(fRanges) - 1
                    newestLabel = Label(root, text=str(int(fRanges)) + "/" + str(int(sRow) - rowCounter), padx=3,
                                        bg="green")
                    newestLabel.grid(row=(2), column=(int(sRow) - rowCounter))
                    print("Turning Around" + str(rowCounter))
                else:
                    counter = 0
                    newestLabel = Label(root, text=str(1) + "/" + str(int(sRow) - rowCounter), padx=3,
                                        bg="green")
                    newestLabel.grid(row=(int(fRanges) - int(1) - counter + 2), column=(int(sRow) - rowCounter))
                    print("Turning Around" + str(rowCounter))

    # code for taking pictures when starting a new field
    if hPath == "Direct" and int(sRange) == 1 and int(sRow) == 1:
        if counter < (int(fRanges) - 1):

            counter += 1
            newestLabel = Label(root, text=str(int(sRange) + counter) + "/" + str(int(sRow) + rowCounter), padx=3,
                                bg="green")
            newestLabel.grid(row=(int(fRanges) - int(sRange) - counter + 2), column=(int(sRow) + rowCounter))
            frame = locationGet + str(int(sRange) + counter) + "." + str(int(sRow) + rowCounter) + fieldGet
            print("made it here")
            output_directory = "/home/pi/Desktop/Images/"
            frame = output_directory+str(frame) + ".jpg"
            picam2.start()
            
            picam2.capture_file(frame)
            picam2.stop()
            print("made it here")
        else:

            counter = 0
            rowCounter += 1
            newestLabel = Label(root, text=str(int(sRange) + counter) + "/" + str(int(sRow) + rowCounter), padx=3,
                                bg="green")
            newestLabel.grid(row=(int(fRanges) - int(sRange) - counter + 2), column=(int(sRow) + rowCounter))
            print("Turning Around after row" + str(rowCounter))

    elif hPath == "Serpentine" and int(sRange) == 1 and int(sRow) == 1:
        if counter < (int(fRanges) - 1) and int(serpCounter) % 2 == 0:
            counter += 1
            newestLabel = Label(root, text=str(int(sRange) + counter) + "/" + str(int(sRow) + rowCounter), padx=3,
                                bg="green")
            newestLabel.grid(row=(int(fRanges) - int(sRange) - counter + 2), column=(int(sRow) + rowCounter))
            frame = (locationGet + str(int(sRange) + counter) + "." + str(int(sRow) + rowCounter) + fieldGet)
            output_directory = "/home/pi/Desktop/Images/"
            frame = output_directory+str(frame) + ".jpg"
            picam2.start()
            
            picam2.capture_file(frame)
            picam2.stop()
        elif counter < (int(fRanges) - 1) and int(serpCounter) % 2 == 1:
            counter += 1
            newestLabel = Label(root, text=str(int(fRanges) - counter) + "/" + str(int(sRow) + rowCounter), padx=3,
                                bg="green")
            newestLabel.grid(row=(int(fRanges) - int(fRanges) + counter + 2), column=(int(sRow) + rowCounter))
            frame = (locationGet + str(int(fRanges) - counter) + "." + str(int(sRow) + rowCounter) + fieldGet)
            output_directory = "/home/pi/Desktop/Images/"
            frame = output_directory+str(frame) + ".jpg"
            picam2.start()
            
            picam2.capture_file(frame)
            picam2.stop()

        else:
            counter = 0
            rowCounter += 1
            serpCounter += 1
            if serpCounter % 2 == 0:
                newestLabel = Label(root, text=str(int(sRange) + counter) + "/" + str(int(sRow) + rowCounter), padx=3,
                                    bg="green")
                newestLabel.grid(row=(int(fRanges) - int(sRange) - counter + 2), column=(int(sRow) + rowCounter))
                print("Turning Around" + str(rowCounter))
            else:
                newestLabel = Label(root, text=str(int(fRanges) + counter) + "/" + str(int(sRow) + rowCounter), padx=3,
                                    bg="green")
                newestLabel.grid(row=(int(fRanges) - int(fRanges) - counter + 2), column=(int(sRow) + rowCounter))
                print("Turning Around" + str(rowCounter))


    elif hPath == "Serpentine" and int(sRange) == 1 and int(sRow) == int(fRows):
        if counter < (int(fRanges) - 1) and int(serpCounter) % 2 == 0:
            counter += 1
            newestLabel = Label(root, text=str(int(sRange) + counter) + "/" + str(int(sRow) - rowCounter), padx=3,
                                bg="green")
            newestLabel.grid(row=(int(fRanges) - int(sRange) - counter + 2), column=(int(sRow) - rowCounter))
            frame = (locationGet + str(int(sRange) + counter) + "." + str(int(sRow) - rowCounter) + fieldGet)
            output_directory = "/home/pi/Desktop/Images/"
            frame = output_directory+str(frame) + ".jpg"
            picam2.start()
            
            picam2.capture_file(frame)
            picam2.stop()

        elif counter < (int(fRanges) - 1) and int(serpCounter) % 2 == 1:
            counter += 1
            newestLabel = Label(root, text=str(int(fRanges) - counter) + "/" + str(int(sRow) - rowCounter), padx=3,
                                bg="green")
            newestLabel.grid(row=(int(fRanges) - int(fRanges) + counter + 2), column=(int(sRow) - rowCounter))
            frame = (locationGet + str(int(fRanges) - counter) + "." + str(int(sRow) - rowCounter) + fieldGet)
            output_directory = "/home/pi/Desktop/Images/"
            frame = output_directory+str(frame) + ".jpg"
            picam2.start()
            
            picam2.capture_file(frame)
            picam2.stop()


        else:
            counter = 0
            rowCounter += 1
            serpCounter += 1
            if serpCounter % 2 == 0:
                newestLabel = Label(root, text=str(int(sRange) + counter) + "/" + str(int(sRow) - rowCounter), padx=3,
                                    bg="green")
                newestLabel.grid(row=(int(fRanges) - int(sRange) - counter + 2), column=(int(sRow) - rowCounter))
                print("Turning Around" + str(rowCounter))
            else:
                newestLabel = Label(root, text=str(int(fRanges) + counter) + "/" + str(int(sRow) - rowCounter), padx=3,
                                    bg="green")
                newestLabel.grid(row=(int(fRanges) - int(fRanges) - counter + 2), column=(int(sRow) - rowCounter))
                print("Turning Around" + str(rowCounter))


    elif hPath == "Serpentine" and int(sRange) == int(fRanges) and int(sRow) == int(fRows):
        if counter < (int(fRanges) - 1) and int(serpCounter) % 2 == 0:
            counter += 1
            newestLabel = Label(root, text=str(int(sRange) - counter) + "/" + str(int(sRow) - rowCounter), padx=3,
                                bg="green")
            newestLabel.grid(row=(int(fRanges) - int(sRange) + counter + 2), column=(int(sRow) - rowCounter))
            frame = (locationGet + str(int(sRange) - counter) + "." + str(int(sRow) - rowCounter) + fieldGet)
            output_directory = "/home/pi/Desktop/Images/"
            frame = output_directory+str(frame) + ".jpg"
            picam2.start()
            
            picam2.capture_file(frame)
            picam2.stop()

        elif counter < (int(fRanges) - 1) and int(serpCounter) % 2 == 1:
            counter += 1
            newestLabel = Label(root, text=str(int(1) + counter) + "/" + str(int(sRow) - rowCounter), padx=3,
                                bg="green")
            newestLabel.grid(row=(int(fRanges) - int(1) - counter + 2), column=(int(sRow) - rowCounter))
            frame = (locationGet + str(int(1) + counter) + "." + str(int(sRow) - rowCounter) + fieldGet)
            output_directory = "/home/pi/Desktop/Images/"
            frame = output_directory+str(frame) + ".jpg"
            picam2.start()
            
            picam2.capture_file(frame)
            picam2.stop()


        else:
            counter = 0
            rowCounter += 1
            serpCounter += 1
            if serpCounter % 2 == 0:
                newestLabel = Label(root, text=str(int(sRange) - counter) + "/" + str(int(sRow) - rowCounter), padx=3,
                                    bg="green")
                newestLabel.grid(row=(int(fRanges) - int(sRange) - counter + 2), column=(int(sRow) - rowCounter))
                print("Turning Around" + str(rowCounter))
            else:
                newestLabel = Label(root, text=str(1) + "/" + str(int(sRow) - rowCounter), padx=3,
                                    bg="green")
                newestLabel.grid(row=(int(fRanges) - int(1) - counter + 2), column=(int(sRow) - rowCounter))
                print("Turning Around" + str(rowCounter))


    elif hPath == "Serpentine" and int(sRange) == int(fRanges) and int(sRow) == int(1):
        if counter < (int(fRanges) - 1) and int(serpCounter) % 2 == 0:
            counter += 1
            newestLabel = Label(root, text=str(int(sRange) - counter) + "/" + str(int(sRow) + rowCounter), padx=3,
                                bg="green")
            newestLabel.grid(row=(int(fRanges) - int(sRange) + counter + 2), column=(int(sRow) + rowCounter))
            frame = (locationGet + str(int(sRange) - counter) + "." + str(int(sRow) + rowCounter) + fieldGet)
            output_directory = "/home/pi/Desktop/Images/"
            frame = output_directory+str(frame) + ".jpg"
            picam2.start()
            
            picam2.capture_file(frame)
            picam2.stop()

        elif counter < (int(fRanges) - 1) and int(serpCounter) % 2 == 1:
            counter += 1
            newestLabel = Label(root, text=str(int(1) + counter) + "/" + str(int(sRow) + rowCounter), padx=3,
                                bg="green")
            newestLabel.grid(row=(int(fRanges) - int(1) - counter + 2), column=(int(sRow) + rowCounter))
            frame = (locationGet + str(int(1) + counter) + "." + str(int(sRow) + rowCounter) + fieldGet)
            output_directory = "/home/pi/Desktop/Images/"
            frame = output_directory+str(frame) + ".jpg"
            picam2.start()
            
            picam2.capture_file(frame)
            picam2.stop()


        else:
            counter = 0
            rowCounter += 1
            serpCounter += 1
            if serpCounter % 2 == 0:
                newestLabel = Label(root, text=str(int(sRange) - counter) + "/" + str(int(sRow) + rowCounter), padx=3,
                                    bg="green")
                newestLabel.grid(row=(int(fRanges) - int(sRange) - counter + 2), column=(int(sRow) + rowCounter))
                print("Turning Around" + str(rowCounter))
            else:
                newestLabel = Label(root, text=str(1) + "/" + str(int(sRow) + rowCounter), padx=3,
                                    bg="green")
                newestLabel.grid(row=(int(fRanges) - int(1) - counter + 2), column=(int(sRow) + rowCounter))
                print("Turning Around" + str(rowCounter))

    elif hPath == "Direct" and int(sRange) == int(fRanges) and int(sRow) == int(fRows):
        if counter < (int(fRanges) - 1):
            counter += 1
            newestLabel = Label(root, text=str(int(sRange) - counter) + "/" + str(int(sRow) - rowCounter), padx=3,
                                bg="green")
            newestLabel.grid(row=(int(fRanges) - int(sRange) + counter + 2), column=(int(sRow) - rowCounter))
            frame = (locationGet + str(int(sRange) - counter) + "." + str(int(sRow) - rowCounter) + fieldGet)
            output_directory = "/home/pi/Desktop/Images/"
            frame = output_directory+str(frame) + ".jpg"
            picam2.start()
            
            picam2.capture_file(frame)
            picam2.stop()


        else:
            counter = 0
            rowCounter += 1
            newestLabel = Label(root, text=str(int(sRange) + counter) + "/" + str(int(sRow) - rowCounter), padx=3,
                                bg="green")
            newestLabel.grid(row=(int(fRanges) - int(sRange) + counter + 2), column=(int(sRow) - rowCounter))
            print("Turning Around" + str(rowCounter))

    elif hPath == "Direct" and int(sRange) == int(fRanges) and int(sRow) == 1:
        if counter < (int(fRanges) - 1):
            counter += 1
            newestLabel = Label(root, text=str(int(sRange) - counter) + "/" + str(int(sRow) + rowCounter), padx=3,
                                bg="green")
            newestLabel.grid(row=(int(fRanges) - int(sRange) + counter + 2), column=(int(sRow) + rowCounter))
            frame = (locationGet + str(int(sRange) - counter) + "." + str(int(sRow) + rowCounter) + fieldGet)
            output_directory = "/home/pi/Desktop/Images/"
            frame = output_directory+str(frame) + ".jpg"
            picam2.start()
            
            picam2.capture_file(frame)
            picam2.stop()


        else:
            counter = 0
            rowCounter += 1
            newestLabel = Label(root, text=str(int(sRange) + counter) + "/" + str(int(sRow) + rowCounter), padx=3,
                                bg="green")
            newestLabel.grid(row=(int(fRanges) - int(sRange) + counter + 2), column=(int(sRow) + rowCounter))
            print("Turning Around" + str(rowCounter))

    elif hPath == "Direct" and int(sRange) == int(1) and int(sRow) == int(fRows):
        if counter < (int(fRanges) - 1):
            counter += 1
            newestLabel = Label(root, text=str(int(sRange) + counter) + "/" + str(int(sRow) - rowCounter), padx=3,
                                bg="green")
            newestLabel.grid(row=(int(fRanges) - int(sRange) - counter + 2), column=(int(sRow) - rowCounter))
            frame = (locationGet + str(int(sRange) + counter) + "." + str(int(sRow) - rowCounter) + fieldGet)
            output_directory = "/home/pi/Desktop/Images/"
            frame = output_directory+str(frame) + ".jpg"
            picam2.start()
            
            picam2.capture_file(frame)
            picam2.stop()


        else:
            counter = 0
            rowCounter += 1
            newestLabel = Label(root, text=str(int(sRange) + counter) + "/" + str(int(sRow) - rowCounter), padx=3,
                                bg="green")
            newestLabel.grid(row=(int(fRanges) - int(sRange) + counter + 2), column=(int(sRow) - rowCounter))
            print("Turning Around" + str(rowCounter))





GPIO.setmode(GPIO.BCM)
GPIO.setup(6,GPIO.IN,pull_up_down=GPIO.PUD_UP)
GPIO.add_event_detect(6,GPIO.FALLING, callback=take_Picture, bouncetime=2000)
#picam2 = Picamera2()
#camera.rotation = 180






root = Tk()
root.title("Plot Capture")
newLabelGrid = []
global counter
global rowCounter
global serpCounter
global harvestDirection
global variable2
global currentRow
global restartDirectionIndicator
global input_state
#input_state = GPIO.input(18)
counter = 0
rowCounter = 0
serpCounter = 2
restartCounter = 0
directionIndicator = 0
restartDirectionIndicator = 0
"""while True:
    if input_state == False:
        take_Picture()
        time.sleep(0.4)"""

while True:
    def popup_Window():
        global fRanges
        global fRows
        global sRange
        global sRow
        global hPath
        global count
        global restartCounter
        global ogSRow
        global ogSRanges
        global directionIndicator
        global variable2
        global currentRow




        fRanges = fieldRanges.get()
        fRows = fieldRows.get()
        sRange = startingRange.get()
        sRow = startingRow.get()
        """hPath = variable.get()"""

        if (int(sRange) == int(1) and int(sRow) == int(1)) or (int(sRange) == int(1) and int(sRow) == int(fRows)) or (int(sRange) == int(fRanges) and int(sRow) == int(1)) or (int(sRange) == int(fRanges) and int(sRow) == int(fRows)):
            button_click()
        else:

            directionIndicator = 1
            newWindow = Toplevel()
            Hello = Label(newWindow, text="Please select the last plot you are harvesting", width=40, borderwidth=5)
            Hello.grid(row=1, column=0, padx=10, pady=2, columnspan=2)
            variable2 = StringVar(root)
            Options2 = ["Last Range, Last Row", "Last Range, First Row", "First Range, Last Row", "First Range, First Row"]
            variable2.set(Options[0])
            harvestPath2 = OptionMenu(newWindow, variable2, *Options2)
            harvestPath2.grid(row=2, column=1, padx=10, pady=10)
            submitButton2 = Button(newWindow, text="Start Harvesting", padx=40, pady=20, command=button_click)
            submitButton2.grid(row=3, column=0, columnspan=2)





    def button_click():
        global fRanges
        global fRows
        global sRange
        global sRow
        global hPath
        global locationGet
        global fieldGet
        global count
        global restartCounter
        global ogSRow
        global ogSRanges
        global harvestDirection
        global directionIndicator
        global variable2
        global newWindow
        global counter
        global currentRow
        global restartDirectionIndicator
        global input_state


        if directionIndicator == 1:
            harvestDirection = variable2.get()

            counter = int(sRange) -1
            currentRow = int(sRow)
            if (int(currentRow) % 2 == 0 and int(fRows) % 2 == 0) or (int(currentRow) % 2 == 1 and int(fRows) % 2 == 1):
                #This is the indicator to tell the functions below which way we are initially harvesting when someone restarts combining in the middle of a field.
                restartDirectionIndicator = 1







        fRanges = fieldRanges.get()
        fRows = fieldRows.get()
        sRange = startingRange.get()
        sRow = startingRow.get()
        hPath = variable.get()
        locationGet = location.get()
        fieldGet = field.get()



        list = root.grid_slaves()
        for l in list:
            l.destroy()

        #create field summary on window
        fieldRangesLabel = Label(root, text="Ranges in Harvest Field", width=20, borderwidth=5)
        fieldRangesLabel.grid(row=2, column=(int(fRows)+2), padx=10, pady=2)
        fieldRowsLabel = Label(root, text="Rows in Harvest Field", width=20, borderwidth=5)
        fieldRowsLabel.grid(row=3, column=(int(fRows)+2), padx=10, pady=2)
        """startingPointTitle = Label(root, text="Starting Range and Row", width=20, borderwidth=5)
        startingPointTitle.grid(row=int(fRanges)+4, column=1, padx=10, pady=2)"""
        startingRangeLabel = Label(root, text="Starting Range", width=20, borderwidth=5)
        startingRangeLabel.grid(row=4, column=(int(fRows)+2), padx=10, pady=2)
        startingRowLabel = Label(root, text="Starting Row", width=20, borderwidth=5)
        startingRowLabel.grid(row=5, column=(int(fRows)+2), padx=10, pady=2)
        """directionTitle = Label(root, text="Harvest Direction", width=20, borderwidth=5)
        starti.grid(row=int(fRanges)+7, column=1, padx=10, pady=2)"""
        harvestPathTitle = Label(root, text="Harvest Direction", width=20, borderwidth=5)
        harvestPathTitle.grid(row=6, column=(int(fRows)+2), padx=10, pady=2)

        fieldRangesAmount = Label(root, text=str(fRanges), width=20, borderwidth=5)
        fieldRangesAmount.grid(row=2, column=(int(fRows)+3), padx=10, pady=2)
        fieldRowsAmount = Label(root, text=str(fRows), width=20, borderwidth=5)
        fieldRowsAmount.grid(row=3, column=(int(fRows)+3), padx=10, pady=2)
        """startingPointTitle = Label(root, text="Starting Range and Row", width=20, borderwidth=5)
        startingPointTitle.grid(row=int(fRanges)+4, column=1, padx=10, pady=2)"""
        startingRangeAmount = Label(root, text=str(sRange), width=20, borderwidth=5)
        startingRangeAmount.grid(row=4, column=(int(fRows)+3), padx=10, pady=2)
        startingRowAmount = Label(root, text=str(sRow), width=20, borderwidth=5)
        startingRowAmount.grid(row=5, column=(int(fRows)+3), padx=10, pady=2)
        """directionTitle = Label(root, text="Harvest Direction", width=20, borderwidth=5)
        starti.grid(row=int(fRanges)+7, column=1, padx=10, pady=2)"""
        harvestPathDirection = Label(root, text=str(hPath), width=20, borderwidth=5)
        harvestPathDirection.grid(row=6, column=(int(fRows)+3), padx=10, pady=2)



        """newWindow = Toplevel(root)
        newWindow.title("Plot Sequence")"""
        newLabel = Label(root, text="Harvest Path")
        newLabel.grid(row=0,column=1, columnspan=(int(fRows)-1), padx=10, pady=2)
        for i in range(int(fRanges)):
            for j in range(int(fRows)):
                anotherLabel = Label(root,text=str(i+1)+"/"+str(j+1), padx=3)
                anotherLabel.grid(row=(int(fRanges)-i+1), column=(j+1))
        anotherLabel = Label(root, text=str(sRange)+"/"+str(sRow), padx=3, bg= "green")
        anotherLabel.grid(row=(int(fRanges)-int(sRange)+2), column=(int(sRow)))
        takePictureButton = Button(root, text="Take Picture", padx=40, pady=20, command= lambda: take_Picture(18))
        takePictureButton.grid(row=0, column=int(fRows)+2, columnspan=2)      
        previewCameraButton = Button(root, text="Preview Camera", padx=40, pady=20, command=preview_Camera)
        previewCameraButton.grid(row=7, column=int(fRows) + 2, columnspan=2)


    def preview_Camera():
        #picam2.start_preview(Preview.QTGL)
        #picam2.start()
        time.sleep(10)
        #picam2.stop_preview(Preview.QTGL)





    #define the input boxes
    fieldRanges = Entry(root, width=10, borderwidth=5)
    fieldRanges.grid(row=1,column=1, columnspan=3, padx=10, pady=2)
    fieldRows = Entry(root, width=10, borderwidth=5)
    fieldRows.grid(row=2,column=1, columnspan=3, padx=10, pady=2)
    startingRange = Entry(root, width=10, borderwidth=5)
    startingRange.grid(row=4,column=1, columnspan=3, padx=10, pady=2)
    startingRow = Entry(root, width=10, borderwidth=5)
    startingRow.grid(row=5,column=1, columnspan=3, padx=10, pady=2)
    variable = StringVar(root)
    Options = ["Direct", "Serpentine"]
    variable.set(Options[0])
    harvestPath = OptionMenu(root, variable, *Options)
    harvestPath.grid(row=7, column= 1, padx=10, pady=10)
    location = Entry(root, width=10, borderwidth=5)
    location.grid(row=8,column=1, columnspan=3, padx=10, pady=2)
    field = Entry(root, width=10, borderwidth=5)
    field.grid(row=9,column=1, columnspan=3, padx=10, pady=2)

    #define the labels
    fieldSizeTitle = Label(root, text="Field Size Parameters", width=20, borderwidth=5)
    fieldSizeTitle.grid(row=0, column=0, padx=10, pady=2)
    fieldRangesLabel = Label(root, text="Ranges in Harvest Field", width=20, borderwidth=5)
    fieldRangesLabel.grid(row=1, column=0, padx=10, pady=2)
    fieldRangesLabel = Label(root, text="Rows in Harvest Field", width=20, borderwidth=5)
    fieldRangesLabel.grid(row=2, column=0, padx=10, pady=2)
    startingPointTitle = Label(root, text="Starting Range and Row", width=20, borderwidth=5)
    startingPointTitle.grid(row=3, column=0, padx=10, pady=2)
    startingRangeLabel = Label(root, text="Starting Range", width=20, borderwidth=5)
    startingRangeLabel.grid(row=4, column=0, padx=10, pady=2)
    startingRowLabel = Label(root, text="Starting Row", width=20, borderwidth=5)
    startingRowLabel.grid(row=5, column=0, padx=10, pady=2)
    """directionTitle = Label(root, text="Harvest Direction", width=20, borderwidth=5)
    directionTitle.grid(row=6, column=0, padx=10, pady=2)"""
    harvestPathTitle = Label(root, text="Harvest Direction", width=20, borderwidth=5)
    harvestPathTitle.grid(row=7, column=0, padx=10, pady=2)
    locationLabel = Label(root, text="Location", width=20, borderwidth=5)
    locationLabel.grid(row=8, column=0, padx=10, pady=2)
    fieldLabel = Label(root, text="Field (ie. F5)", width=20, borderwidth=5)
    fieldLabel.grid(row=9, column=0, padx=10, pady=2)
 
    #submit button to show you have entered the parameters of the field and are ready to start harvesting
    submitButton = Button(root, text="Start Harvesting", padx=40, pady=20, command=popup_Window)
    submitButton.grid(row=10, column=0, columnspan=2)









    root.mainloop()

