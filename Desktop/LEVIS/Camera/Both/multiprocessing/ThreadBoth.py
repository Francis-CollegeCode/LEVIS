import multiprocessing
import os

#turn on RGB
def RGBCam_function():
    print("started RGB")
    os.system("./ThreadRGB")
    
# #turn on the thermal camera
def ThermalCam_function():
    print("started Thrml")
    os.system('sudo sh -c "echo performance > /sys/devices/system/cpu/cpufreq/policy0/scaling_governor"')
    os.system("./raspberrypi_video -tl 3")
 
if __name__ == "__main__":
 
    # Creates two processes
    p1 = multiprocessing.Process(target=RGBCam_function)
    p2 = multiprocessing.Process(target=ThermalCam_function)
 
    # Starts both processes
    p1.start()
    p2.start()
 
    print("Program Done")