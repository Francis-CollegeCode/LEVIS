import cv2
import dlib

picture = cv2.VideoCapture(0)
picture.set(3,640) # set Width 160
picture.set(4,480) # set Height 120

noseTaken = False

# Load the detector
detector = dlib.get_frontal_face_detector()

# Load the predictor
predictor = dlib.shape_predictor("/home/pi/Blue (thermal camera, without mask)/shape_predictor_68_face_landmarks.dat")

count = 0

while True:
    _, frame = picture.read()
    
    # Convert image into grayscale
    gray = cv2.cvtColor(src=frame, code=cv2.COLOR_BGR2GRAY)  # src=frame

    # Use detector to find landmarks
    faces = detector(gray) 

    # Facial features dots
    for face in faces:
        print("\nIn facial feature dot loop")
        x1 = face.left()  # left point
        y1 = face.top()  # top point
        x2 = face.right()  # right point
        y2 = face.bottom()  # bottom point

        # Create landmark object
        landmarks = predictor(image=frame, box=face)

        # Loop through all the points
        for n in range(31, 36): #(0, 68) for all points. (31, 35) for nostil region
            x = landmarks.part(n).x
            y = landmarks.part(n).y
            
            
            print("pixel #: ", n, "(",x,",", y, ")")

            # Draw a circle
            cv2.circle(img=frame, center=(x, y), radius=3, color=(0, 255, 0), thickness=-1)  # img=frame
        noseTaken = True
        
    # show the image
    cv2.imshow(winname="Nose", mat=frame)  # mat=frame
    k = cv2.waitKey(30) & 0xff
    if k == 27: # press 'ESC' to quit
        break
    ret,frame = picture.read()
    
    count += 1

#    print(noseTaken, count)

#     if (noseTaken==False):
#         print("No nose detected.")
#     else:
#         print("^Detected Coordinates")
    
picture.release()
cv2.destroyAllWindows()

