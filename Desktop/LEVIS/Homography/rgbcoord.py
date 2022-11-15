import numpy as np
import cv2 as cv
import glob

################ FIND CHESSBOARD CORNERS - OBJECT POINTS AND IMAGE POINTS #############################
chessboardSize = (8,6)
frameSize = (1440,1080)

# termination criteria
criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 30, 0.001)

# prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
objp = np.zeros((chessboardSize[0] * chessboardSize[1], 3), np.float32)
objp[:,:2] = np.mgrid[0:chessboardSize[0],0:chessboardSize[1]].T.reshape(-1,2)

size_of_chessboard_squares_mm = 20
objp = objp * size_of_chessboard_squares_mm

# Arrays to store object points and image points from all the images.
objpoints = [] # 3d point in real world space
imgpointsR = [] # 2d points in the right image plane.
imgpointsL = [] # 2d points in the left image plane.
#reteiving the path to the left and right camera images. 
imagesL = glob.glob('/home/pi/python_stereo_camera_calibrate/screenshots/*.png')
imagesR = glob.glob('/home/pi/python_stereo_camera_calibrate/homographypics/*.png')

for imager in imagesR:
    imgR = cv.imread(imager)
    grayR = cv.cvtColor(imgR, cv.COLOR_BGR2GRAY)
    # Find the chess board corners
    retR, cornersR = cv.findChessboardCorners(grayR, chessboardSize, None)
    print(retR)
    
    
for imagel in imagesL:
    imgL = cv.imread(imagel)
    grayL = cv.cvtColor(imgL, cv.COLOR_BGR2GRAY)
    # Find the chess board corners
    retL, cornersL = cv.findChessboardCorners(grayL, chessboardSize, None)
    print(retL)
    
    if retR and retL:
         # Draw and display the corners
        objpoints.append(objp)
        corners2R = cv.cornerSubPix(grayR, cornersR, (11,11), (-1,-1), criteria)
        corners2L = cv.cornerSubPix(grayL, cornersL, (11,11), (-1,-1), criteria)
        imgpointsL.append(cornersL)
        imgpointsR.append(cornersR)
        cv.drawChessboardCorners(imgR, chessboardSize, corners2R, retR)
        cv.drawChessboardCorners(imgL, chessboardSize, corners2L, retL)
        #cv.imshow('cornersR',imgR)
        #cv.imshow('cornersL',imgL)
        cv.waitKey(100)
        
print(objpoints)
        
retL, mtxL, distL, rvecsL, tvecsL = cv.calibrateCamera(objpoints,imgpointsL,grayL.shape[::-1],None,None)
#hL,wL= imgL_gray.shape[:2]
#new_mtxL, roiL= cv2.getOptimalNewCameraMatrix(mtxL,distL,(wL,hL),1,(wL,hL))
 
# Calibrating right camera
retR, mtxR, distR, rvecsR, tvecsR = cv.calibrateCamera(objpoints,imgpointsR,grayR.shape[::-1],None,None)
#hR,wR= imgR_gray.shape[:2]
#new_mtxR, roiR= cv2.getOptimalNewCameraMatrix(mtxR,distR,(wR,hR),1,(wR,hR))


rvec1, tvec1 = cv.solvePnP(np.asarray(objpoints), corners2L, mtxL, distL, rvecsL, tvecsL , flags=0)
#print("rvec\n\n", rvec1)
























'''
print(" left camera matrix")
print(mtxL)
print("\n left Distortion coefficient:")
print(distL)
 
print("\n left Rotation Vectors:")
print(rvecsL)
 
print("\n left Translation Vectors:")
print(tvecsL)

print("\n")

print(" right camera matrix")
print(mtxR)
print("\n right Distortion coefficient:")
print(distR)
 
print("\n right Rotation Vectors:")
print(rvecsR)
 
print("\n right Translation Vectors:")
print(tvecsR)
'''        
    
    



