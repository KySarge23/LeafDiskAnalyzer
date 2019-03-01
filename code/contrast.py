import numpy as np
import cv2 as cv
from matplotlib import pyplot as plt

def contour_detection(x):

    img = cv.imread(x)

    gray = cv.cvtColor(img,cv.COLOR_BGR2GRAY)
    ret,gray = cv.threshold(gray,127,255, 0)
    mask = np.zeros(gray.shape,np.uint8)

    contours, hierarchy = cv.findContours(gray, cv.RETR_LIST, cv.CHAIN_APPROX_SIMPLE)

    for cnt in contours:
        area = cv.contourArea(cnt)
        x,y,w,h = cv.boundingRect(cnt)
        rect_area = w*h
        extent = float(area)/rect_area
        print(extent)
        cv.drawContours(img,[cnt],0,(0,255,0),2)
        cv.drawContours(mask,[cnt],0,255,0)
        cv.imshow("IMG", gray)
        cv.waitKey(0)
        cv.destroyAllWindows()

def main():
    
    contour_detection('../photos/9-15-18 2dpi/tray 1/LeafDiskMildew.png')
    

main()
