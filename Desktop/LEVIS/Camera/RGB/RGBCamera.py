import cv2

picture = cv2.VideoCapture(0)

picture.set(3,640)
picture.set(4,480)

while True:
    _,frame = picture.read()
    cv2.imshow(winname="Window Name",mat=frame)
    
    k = cv2.waitKey(30) & 0xff
    if k == 27:
        break

picture.release()
cv2.destroyAllWindows()