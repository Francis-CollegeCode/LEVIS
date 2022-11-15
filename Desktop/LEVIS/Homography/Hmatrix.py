import cv2 as cv
import numpy as np
 
if __name__ == '__main__' :
 
    # Read source image.
    im_src = cv.imread('/home/pi/Desktop/LEVIS/Homography/RGBPic1.png')
    # Four corners of the book in source image
    pts_src = np.array([[224, 210], [231, 212], [239, 213],[246, 211], [253, 209]])
 
    # Read destination image.
    im_dst = cv.imread('/home/pi/Desktop/LEVIS/Homography/RGBPic2.png')
    # Four corners of the book in destination image.
    pts_dst = np.array([[262, 193],[271, 196],[280, 199],[291, 197],[300, 194]])
    array = [262, 193,1] 
    # Calculate Homography
    h, status = cv.findHomography(pts_src, pts_dst)
    print(h)
    print("\n ")
    final = array*h
    print(final)
    
 
    # Warp source image to destination based on homography
    im_out = cv.warpPerspective(im_src, h, (im_dst.shape[1],im_dst.shape[0]))
 
    # Display images
    cv.imshow("Source Image", im_src)
    cv.imshow("Destination Image", im_dst)
    cv.imshow("Warped Source Image", im_out)
  
    cv.waitKey(0)