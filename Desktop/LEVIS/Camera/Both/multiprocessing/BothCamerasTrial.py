import os
import cv2
import threading

#Initialization
frame = cv2.VideoCapture(0)
frame.set(3,640)
frame.set(4,480)

def RGBCam_function():
    print("started RGB")
    os.system("raspistill --fullpreview")
#    while True:
#          _,frame = img.read()
#          cv2.imshow(winname="Window Name",mat=frame)
#          
#          k = cv2.waitKey(30) & 0xff
#          if k == 27:
#              break
#  
#     img.release()
#     cv2.destroyAllWindows()

    
#turn on the thermal camera
def ThermalCam_function():
    print("started Thrml")
    os.system('sudo sh -c "echo performance > /sys/devices/system/cpu/cpufreq/policy0/scaling_governor"')
    os.system("./raspberrypi_video -tl 3")
    
#creating threads
t1 = threading.Thread(target = RGBCam_function())
t2 = threading.Thread(target = ThermalCam_function())

t2.start()
t1.start()

t2.join()
t1.join()








