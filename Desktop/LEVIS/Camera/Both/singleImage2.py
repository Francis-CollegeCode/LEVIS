# USAGE
# python dlib_predict_image.py --images dataset/gray/test/images/ --models  models/ --upsample 1

# import the necessary packages
from imutils import face_utils
from imutils import paths
import numpy as np
import imutils
import argparse 
import imutils
import time
import dlib
import cv2
import os
import json

def detect():
    #for json file
    x_coords = []
    y_coords = []

    # Construct argument parser
    # ap = argparse.ArgumentParser()
    # ap.add_argument("-i", "--images", required=True,
    # 	help="path to the images")
    # ap.add_argument("-m", "--models", required=True,
    # 	help="path to the models")
    # ap.add_argument("-u", "--upsample", type=int, default=0,
    # 	help="# of upsampling times")
    # args = vars(ap.parse_args())

    # load the face detector (HOG-SVM)
    #print("[INFO] loading dlib thermal face detector...")
    #detector = dlib.simple_object_detector(os.path.join(args["models"], "dlib_face_detector.svm"))
    detector = dlib.get_frontal_face_detector()
     


    # load the facial landmarks predictor
    #print("[INFO] loading facial landmark predictor...")
    #predictor = dlib.shape_predictor(os.path.join(args["models"], "dlib_landmark_predictor.dat"))
    predictor = dlib.shape_predictor("/home/pi/Desktop/LEVIS/Camera/Both/shape_predictor_68_face_landmarks.dat")


    # set image to be tested with detector
    imagePath = "/home/pi/Desktop/LEVIS/Camera/Both/RGBPic.png"
    img = dlib.load_rgb_image(imagePath)

    # grabs path to image
    # imagePath = paths.list_files(img)
    # print(str(imagePath))
    #dataset/gray/test/images/133_2_2_7_108_21_1.png

    # use detector
    #print("[INFO] Processing image")
    # load the image
    image = cv2.imread(imagePath)

    # resize the image
    image = imutils.resize(image, height=640)
    image = imutils.resize(image, width=480)

    # copy the image
    image_copy = image.copy()

    # convert the image to grayscale
    image = cv2.cvtColor(image, cv2.COLOR_BGRA2GRAY)

    # detect faces in the image 
    #rects = detector(image, upsample_num_times=args["upsample"])
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
                #cv2.circle(image_copy, (sx, sy), 2, (0, 0, 255), -1)
                #lists to store initial data in to make it a type(list)

                #get x and y coordinates and put them in a list
                newX = round(int(sx)/4+2)
                newY = round(int(sy)/4-10)
                
                x_coords.append(newX)
                y_coords.append(newY)

                print(newX,newY)
            landmarks +=1;

    # show the image
    #print("[INFO] Finished analysis")
    #print("Number of landmarks:", landmarks)
    # cv2.imshow("Image", image_copy)
    # key = cv2.waitKey(0) & 0xFF

    #put x and y coords into dictionary format and store in seperate lists
    coordData = {"x-coordinates":x_coords, "y-coordinates":y_coords}

    # Serializing json
    json_object = json.dumps(coordData, indent=2)

    # Writing to today's date file
    with open("/home/pi/Desktop/LEVIS/Camera/Both/CoordinateData.json", "w") as outfile:
        outfile.write(json_object)
    
    return 0

