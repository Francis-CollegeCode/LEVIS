# import os
# # # # 
# # # # #turn on the thermal camera
# os.system('sudo sh -c "echo performance > /sys/devices/system/cpu/cpufreq/policy0/scaling_governor"')
# os.system("./raspberrypi_video -tl 3")




## Import packages
import numpy as np
import cv2
from pylepton import Lepton

# Create a buffer to save the images into
lepton_buf = np.zeros((120,160,1), dtype=np.uint16)

# Create a named window for the image to be placed into
cv2.namedWindow("Thermal", cv2.WINDOW_NORMAL) # creates window
cv2.resizeWindow('Thermal', 400,300) # resizes window to usable resolution
        
while True:
    with Lepton() as l:
        a,_ = l.capture()
        cv2.normalize(a,a, 0, 65353, cv2.NORM_MINMAX)
        # Rotate image
        a = np.rot90(a, 2)
        # Convert to uint 8
        a = (a/256).astype('uint8')
        # Resize image
        cv2.resize(a, (640,480))
        # Convert to color map
        a = cv2.applyColorMap(a, cv2.COLORMAP_JET)
        # show image
        cv2.imshow('Thermal',a)
        key = cv2.waitKey(1) & 0xFF
        # if the `q` key was pressed, break from the loop
        if key == ord("q"):
            break
