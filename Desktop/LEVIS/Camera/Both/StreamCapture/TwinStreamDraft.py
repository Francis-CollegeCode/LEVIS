#This is a recreation of what LEVIS showed Dr. Kim for a software demo mid fall
#The program uses multiprocessing to essentially take two pictures (RGB & thermal)
#at once. In between, a face is detected in the rgb image. The coordinates of the
#nose specifically are taken and transfered into the thermal pic, where the
#corresponding temperatures are found.


import multiprocessing
import os
import cv2
import dlib

#store points in
data_coords = []
# Path for fifo to be created
FIFO = "/home/pi/Desktop/LEVIS/Camera/Both/StreamCapture/mypipe"


#turn on RGB
def RGBCam_capture():
    cv2.imwrite('RGBPic.png',frame)
    detect()
    print("Captured RGB")
#     
# #turn on the thermal camera
def ThermalCam_capture():
    os.system("./Thermal_Capture -tl 3")
    print("Captured Thrml")
# 
p1 = multiprocessing.Process(target=RGBCam_capture)
p2 = multiprocessing.Process(target=ThermalCam_capture)



cap = cv2.VideoCapture(0) # video capture source camera (Here webcam of laptop) 
cap.set(3,160*4) # set Width 640
cap.set(4,120*4) # set Height 480
frame = [0] * 768

# Load the detector
detector = dlib.get_frontal_face_detector()
# Load the predictor
predictor = dlib.shape_predictor("/home/pi/Desktop/LEVIS/Camera/Both/StreamCapture/shape_predictor_68_face_landmarks.dat")

#try to make the pipe
try:
    os.mkfifo(FIFO)

#check if pipe is already made
except OSError as e:
    pass
    #print ("Failed to create FIFO: ", e)

while(True):
    ret,frame = cap.read() # return a single frame in variable `frame`
    
    # Convert image into grayscale
    gray = cv2.cvtColor(src=frame, code=cv2.COLOR_BGR2GRAY)  # src=frame

    # Use detector to find landmarks
    faces = detector(gray) 

    # Facial features dots
    for face in faces:
        x1 = face.left()  # left point
        y1 = face.top()  # top point
        x2 = face.right()  # right point
        y2 = face.bottom()  # bottom point

        # Create landmark object
        landmarks = predictor(image=frame, box=face)

        #Creates empty array for coordinates
        #coordinates = np.empty([])
        # Loop through all the points
        for n in range(31, 36): #(0, 68) for all points. (31, 35) for nostil region
            x = landmarks.part(n).x
            y = landmarks.part(n).y

            # ~ coordinates =[n][0] = landmarks.part(n).x
            # ~ coordinates = [n][1] = landmarks.part(n).y

            #get x and y coordinates and put them in a list
            #Below is current "stereo vision"
            newX = round(int(x)/4) # positive is right
            newY = round(int(y)/4) # positive is down
            
            data_coords.append(newX)
            data_coords.append(newY)

            print(newX,newY)

            # Draw a circle
            cv2.circle(img=frame, center=(x, y), radius=3, color=(0, 255, 0), thickness=-1)  # img=frame
        
        #adding stop flag to end the input stream in c++
        data_coords.append(42069)
        
        #open file as write
        with open(FIFO, "w") as fifo:
            print("Opening FIFO...")
            #for loop that sends data in list
            for r in range(len(data_coords)):
                #write num in list to pipe
                #***IMPORTANT*** Will send everything as one string 
                fifo.write(str(data_coords[r])+".")
                #print('Sent: ', data_coords[r])
        
        print("\n") #SEPERATE noses
        #print("data coords: ", data_coords)    #debugging
        data_coords = []    #clear the list for next set of coords
        
    # show the image
    cv2.imshow(winname="RGB", mat=frame)  # mat=frame
    
    k = cv2.waitKey(30) & 0xff
    if k == 27: # press 'ESC' to quit
        #open file as write
        with open(FIFO, "w") as fifo:
            print("Opening FIFO...")
            #for loop that sends data in list
            fifo.write("69420")
            print("Ending FIFO Stream")
        break

cap.release()
cv2.destroyAllWindows()

print("\nProgram Done")
