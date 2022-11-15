# This program takes a .png file, detects the nose coordinates inside the
# picture, changes them in "stereo vision," and finally stores them in a
# json files


# import the necessary packages
from imutils import face_utils
import numpy as np
import imutils
import argparse 
import imutils
import time
import dlib
import cv2
import os

def detect():
    #for json file
    data_coords = []

    # load the face detector (HOG-SVM)
    detector = dlib.get_frontal_face_detector()
    
    # load the facial landmarks predictor
    predictor = dlib.shape_predictor("/home/pi/Desktop/LEVIS/Camera/Both/KimDemo/shape_predictor_68_face_landmarks.dat")

    # set image to be tested with detector
    imagePath = "/home/pi/Desktop/LEVIS/Camera/Both/KimDemoRevised/RGBPic.png"
    img = dlib.load_rgb_image(imagePath)

    #use detector
    #first load the image
    image = cv2.imread(imagePath)

    # resize the image
    image = imutils.resize(image, height=640)
    image = imutils.resize(image, width=480)

    # copy the image
    image_copy = image.copy()

    # convert the image to grayscale
    image = cv2.cvtColor(image, cv2.COLOR_BGRA2GRAY)

    # detect faces in the image 
    rects = detector(image, 1)

    #Count number of landmarks
    landmarks = 0

    for rect in rects:
        # predict the location of facial landmark coordinates, 
        # then convert the prediction to an easily parsable NumPy array
        shape = predictor(image, rect)
        shape = face_utils.shape_to_np(shape)

        # loop over the (x, y)-coordinates from our dlib shape
        # predictor model draw them on the image
        for (sx, sy) in shape:        
            if landmarks >= 31 and landmarks <= 35:
                
                #get x and y coordinates and put them in a list
                #Below is current "stereo vision"
                newX = round(int(sx)/4 * 1.25) # positive is right
                newY = round(int(sy)/4 * 1.25) # positive is down
                
                data_coords.append(newX)
                data_coords.append(newY)

                print(newX,newY)
            landmarks +=1;

    #open and send over fifo
    #adding stop flag to end the input stream in c++
    data_coords.append(42069)
    # Path to be created
    FIFO = "/home/pi/Desktop/LEVIS/Camera/Both/StreamCapture/mypipe"
    
        #try to make the pipe
    try:
        os.mkfifo(FIFO)

    #check if pipe is already made
    except OSError as e:
        pass
        #print ("Failed to create FIFO: ", e)
    
    #open file as write
    with open(FIFO, "w") as fifo:
        print("Opening FIFO...")
        #for loop that sends data in list
        for r in range(len(data_coords)):
            #write num in list to pipe
            #***IMPORTANT*** Will send everything as one string 
            fifo.write(str(data_coords[r])+".")
            #print data sent
            #print('Sent: ', data_coords[r])
    #fifo.close()
    return 0