import cv2
import os
import numpy as np
import dlib

# Gets video feed
cap = cv2.VideoCapture(0)
cap.set(3,160*2) # set Width 320
cap.set(4,120*2) # set Height 180

frame = [0] * 768

# Load the detector
detector = dlib.get_frontal_face_detector()

# Load the predictor
predictor = dlib.shape_predictor("/home/pi/Blue (thermal camera, without mask)/shape_predictor_68_face_landmarks.dat")

while True:
    _, frame = cap.read()
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
#         coordinates = np.empty([])
        # Loop through all the points
        for n in range(31, 36): #(0, 68) for all points. (31, 35) for nostil region
            x = landmarks.part(n).x
            y = landmarks.part(n).y

            # ~ coordinates =[n][0] = landmarks.part(n).x
            # ~ coordinates = [n][1] = landmarks.part(n).y

            print(x, y, n)

            # Draw a circle
            cv2.circle(img=frame, center=(x, y), radius=3, color=(0, 255, 0), thickness=-1)  # img=frame
        print("\n")
    # show the image
    cv2.imshow(winname="Nose", mat=frame)  # mat=frame
    
    k = cv2.waitKey(30) & 0xff
    if k == 27: # press 'ESC' to quit
        break
    
cap.release()
cv2.destroyAllWindows()
