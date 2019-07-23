import numpy as np
import cv2
from collections import Counter
from barcode_utils import decode
import math


def grab_contours(cnts):

    if len(cnts) == 2:
        cnts = cnts[0]


    elif len(cnts) == 3:
        cnts = cnts[1]

    else:
        raise Exception(("Contours tuple must have length 2 or 3"))

    return cnts

def scan():
    #reading image
    path='data/code1.png'
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
    _, img_bin = cv2.threshold(blurred, 225, 255, cv2.THRESH_BINARY)

    # construct a closing kernel and apply it to the thresholded image
    '''Creating a rectangular kernel with width greater than height. Helps
    in closing the vertical gaps within the barcodes'''
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (21, 7))
    #Applying morphological operation to close the gaps within the barcode
    closed = cv2.morphologyEx(img_bin, cv2.MORPH_CLOSE, kernel)

    #Performing erosion and dilation to remove unnecessary blobs
    closed = cv2.erode(closed,None,iterations=4)
    closed = cv2.dilate(closed, None, iterations=4)

    # find the contours in the binary image, then sort the contours
    # by their area, keeping only the largest one
    cnts = cv2.findContours(closed.copy(), cv2.RETR_EXTERNAL,
                            cv2.CHAIN_APPROX_SIMPLE)
    cnts = grab_contours(cnts)
    c = sorted(cnts, key=cv2.contourArea, reverse=True)[0]

    # compute the rotated bounding box of the largest contour
    rect = cv2.minAreaRect(c)
    box = cv2.boxPoints(rect)
    box = np.int0(box)
    min_vals = np.amin(box,axis=0)
    max_vals = np.amax(box,axis=0)

    """Cropping the barcode region"""
    crop_image = image[min_vals[1]:min_vals[1]+20, min_vals[0]:max_vals[0]]
    img_gray = cv2.cvtColor(crop_image, cv2.COLOR_BGR2GRAY)
    """Enhancing contrast"""
    crop_image_new = cv2.convertScaleAbs(img_gray, alpha=1.5, beta=0)
    """Converting barcode to binary image"""
    ret, bin_img = cv2.threshold(crop_image_new, 200, 255, cv2.THRESH_BINARY)

    """Creating ideal binary image"""
    rows_count,cols_count = bin_img.shape
    for i in range(cols_count):
        col_vals = bin_img[:,i]
        ct_vals = Counter(col_vals)
        bin_img[:,i] = 255 if ct_vals[255] > ct_vals[0] else 0
        

    #TODO: Try with canny edges

    width_list = []
    prev_val = bin_img[0][0]
    count = 1
    for val in bin_img[0]:
        if val == prev_val:
            count+=1
        else:
            width_list.append(count)
            count=1
            prev_val = val

    """Calculating bar widths relative to the number pixels of the first bar"""
    width_list = list(map(lambda x: int(math.ceil(x/width_list[2])),width_list))
    decode(width_list)

    cv2.drawContours(image, [box], -1, (0, 255, 0), 3)
    cv2.imshow("Image", image)
    cv2.imshow("Bin Image ", bin_img)
    cv2.waitKey(0)

scan()
