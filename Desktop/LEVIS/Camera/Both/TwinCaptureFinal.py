import multiprocessing
import os
import cv2
from singleImage2 import detect



#turn on RGB
def RGBCam_capture():
    cv2.imwrite('RGBPic.png',frame)
    detect()
    print("captured RGB")
    
# #turn on the thermal camera
def ThermalCam_capture():
    os.system("./thermalScreenshot -tl 3")
    #os.system("./new -tl 3")
    print("captured Thrml")


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

 
if __name__ == "__main__":
 
    print("Program Done")