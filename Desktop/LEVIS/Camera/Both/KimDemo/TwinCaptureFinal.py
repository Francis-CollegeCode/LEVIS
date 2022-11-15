#This is a recreation of what LEVIS showed Dr. Kim for a software demo mid fall
#The program uses multiprocessing to essentially take two pictures (RGB & thermal)
#at once. In between, a face is detected in the rgb image. The coordinates of the
#nose specifically are taken and transfered into the thermal pic, where the
#corresponding temperatures are found.


import multiprocessing
import os
import cv2
import time
from DetectToJson import detect    #From DetectToJson.py import the function



#turn on RGB
def RGBCam_capture():
    cv2.imwrite('RGBPic.png',frame)
    detect()
    print("Captured RGB")
    
# #turn on the thermal camera
def ThermalCam_capture():
    os.system("./CoordsWTemps -tl 3")
    print("Captured Thrml")

p1 = multiprocessing.Process(target=RGBCam_capture)
p2 = multiprocessing.Process(target=ThermalCam_capture)

cap = cv2.VideoCapture(0) # video capture source camera (Here webcam of laptop) 

while(True):
    ret,frame = cap.read() # return a single frame in variable `frame`
    cv2.imshow('img',frame) #display the captured image
    k = cv2.waitKey(30) & 0xFF
    if k == ord('y'): #save on pressing 'y' 
        p1.start()
        p2.start()
    elif k == 27:
        break

cap.release()
cv2.destroyAllWindows()

print("\nProgram Done")