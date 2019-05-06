import numpy as np
import cv2


def grab_contours(cnts):

    if len(cnts) == 2:
        cnts = cnts[0]


    elif len(cnts) == 3:
        cnts = cnts[1]

    else:
        raise Exception(("Contours tuple must have length 2 or 3"))

    # return the actual contours array
    return cnts

#reading image
path='/users/Stephanie/Pictures/tea.jpg'
image = cv2.imread(path)
gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)

#computing the Scharr gradient magnitude representation of the images in both x and y direction
gradX = cv2.Sobel(gray,ddepth=cv2.CV_32F,dx=1, dy=0,ksize=-1)
gradY = cv2.Sobel(gray,ddepth=cv2.CV_32F, dx = 0, dy = 1, ksize=-1)

#subtract the y-gradient from the x-gradient
'''Performing this subtraction creates regions with high horizontal gradients
and low vertical gradients'''
gradient = cv2.subtract(gradX,gradY)
gradient = cv2.convertScaleAbs(gradient)


'''Ignore noise and focus only on barcode region
'''

#Blurring using a 9x9 kernel for smoothing out high frequency noise

''' Thresholding to binary image. Any value less than 255 is made 0 (black)
otherwise white
'''
blurred = cv2.blur(gradient, (9, 9))
(_, thresh) = cv2.threshold(blurred, 225, 255, cv2.THRESH_BINARY)


# construct a closing kernel and apply it to the thresholded image
'''Creating a rectangular kernel with width greater than height. Helps
in closing the vertical gaps within the barcodes'''
kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (21, 7))
#Applying morphological operation to close the gaps within the barcode
closed = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)

#Performing erosion to erode the white pixels and removes small blobs
closed = cv2.erode(closed,None,iterations=4)

closed = cv2.dilate(closed, None, iterations=4)

# find the contours in the thresholded image, then sort the contours
# by their area, keeping only the largest one
cnts = cv2.findContours(closed.copy(), cv2.RETR_EXTERNAL,
                        cv2.CHAIN_APPROX_SIMPLE)
cnts = grab_contours(cnts)
c = sorted(cnts, key=cv2.contourArea, reverse=True)[0]

# compute the rotated bounding box of the largest contour
rect = cv2.minAreaRect(c)
box = cv2.boxPoints(rect)
box = np.int0(box)

# draw a bounding box arounded the detected barcode and display the
# image
cv2.drawContours(image, [box], -1, (0, 255, 0), 3)
cv2.imshow("Image", image)
cv2.waitKey(0)
