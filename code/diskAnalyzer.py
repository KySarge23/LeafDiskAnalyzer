#!/usr/bin/env python3

import math
import cv2 as cv
import numpy as np
import matplotlib.image as mpimg
import tkinter
import os
import threading as thr
import time
import imghdr
import sys
from pathlib import Path as pth
from tkinter import Tk as tk
from tkinter.filedialog import askopenfilenames
from matplotlib import pyplot as plt


#Author(s): Kyle Sargent, Erica Gitlin, Connor Jansen
#Version: 1.8

def findCircleArea(x):

    """Area finding function, Will utilize HoughCircle method to detect circles
       within the photo or hard coded method to detect circles . Then will use that circle to find the area within it which
       is what will be used later in the edge detection"""

    img = cv.imread(x,0) #read in as Grayscale
    img = cv.medianBlur(img,5) #add blur to reduce noise on photo.
    cimg = cv.cvtColor(img,cv.COLOR_GRAY2BGR) #convert back to BGR scale for the drawn circle to show up as whatever color specified.
    """The following lines can be used to have an algorithm detect circles for us.
       or can use the hard-coded version that is commented out below"""

    #params are as follows: (image, method = cv.HOUGH_GRADIENT is the only one that works
    #thus far, dp, minDist, parap1 = gradient value,
    #param2 = accumulator threshold value for method input, minRadius, maxRadius)
    #for more details on HoughCircles, visit: http://www.bmva.org/bmvc/1989/avc-89-029.pdf or https://www.pyimagesearch.com/2014/07/21/detecting-circles-images-using-opencv-hough-circles/

    """This is how the Hough Transformation works for circles:

        1. First, we create the accumulator(a two dimensional array) space, which is made up of a cell for each pixel.
           Initially each cell is set to 0.
        2. For each edge point (i, j) in the image, increment all cells which according to the equation of a circle (i-a)^{2}+(j-b)^{2}=r^{2}
           could be the center of a circle.
           These cells are represented by the letter a in the equation.
        3. For each possible value of  a found in the previous step, find all possible values of b which satisfy the equation.
        4. Search for local maxima in the accumulator space. These cells represent circles that were detected by the algorithm.

        If we do not know the radius of the circle we are trying to locate beforehand,
        we can use a three-dimensional accumulator space to search for circles with an arbitrary radius.
        Naturally, this is more computationally expensive.
        This method can also detect circles that are partially outside of the accumulator space, as long as enough of the circle's area is still present within it. """


    #circles = cv.HoughCircles(img,cv.HOUGH_GRADIENT,1,200,
                                        #param1=50,param2=30,minRadius=0,maxRadius=0)

    #circles = np.uint8(np.around(circles))

    #for circ in circles[0,:]:
        #draw the detected outer circle
        #params are as follows: (image, center coords, radius, bgr values, thickness)
     #   cv.circle(cimg,(circ[0],circ[1]),circ[2],(0,255,0),2) #this is the only circle drawn
      #  rad = circ[2] #grab the radius


    """The following lines can be used to hard-code in the circle
       or can use above to use an algorithm to detect the circle"""

    h,w = img.shape[:2]
    print("height is: " + str(h))
    print("width is: " + str(w))


    center = (int(w / 2), int(h / 2))
    rad = 200
    cv.circle(cimg, center, rad, (0,0,255), 2)


    area = math.pi * rad ** 2 #calculate the area of the circle detected in pixels
    print("Area of circle drawn is: " + str(int(area))+"px\n")

    cimg = cimg[0:h, 30:w-30]
    cv.imshow(x ,cimg)
    cv.waitKey(0)
    cv.destroyAllWindows()
    cv.imwrite("crop.png" , cimg)

    return area

def cannyEdgeDetection(x):

    """Edge detection function. Utilizes canny edge detection to detect edges found in the picture
       input will be cropped image from the findCircleArea() function.
       output should be an image with found mildew/edges"""

    print("Edge Detection Starting")

    #second param: (1= color, 0= grayscale, -1 = unchanged)
    #however OCV uses BGR coloring and Matplot uses RGB coloring, so
    #when reading in with OCV, need to change to RGB if showing with matplot
    #if we want pictures to show up in RGB correctly colored.
    #notice when matplot pops up, color is distorted.
    #Reading of the same photo, in color for displaying and grayscale for edgeDetection.
    #imgC = cv.imread(x,1)

    imgG = cv.imread(x,0)

    #cv.imshow('Original', img)

    #Converting img to RGB:
    #imgC = cv.cvtColor(imgC, cv.COLOR_BGR2RGB)

    #use canny algorithm for edge detection
    #see https://docs.opencv.org/3.4/da/d22/tutorial_py_canny.html
    #for more details.
    edges = cv.Canny(imgG,145,200)
    cv.imshow("edges", edges)
    cv.waitKey(0)
    #Save image into photos folder for now. so can be used in analyzeDisks method
    cv.destroyAllWindows()
    print("Edge Detection Complete")
    print("Closing window")

    #we now set a threshold using cv.threshhold. This will help to detect possible
    #contours that are greater than the value (127,255,0), a color which was detected
    #on the leaf that is dark green. This is the baseline color. Essentially this is
    #the normal color of the image.
    ret, imgG = cv.threshold(imgG,130,255,cv.ADAPTIVE_THRESH_MEAN_C)
    mask = np.zeros(imgG.shape,np.uint8)
    #we must now find the contours. We apply the findContours using our threshold value.
    #we want the contours as a list not as a tree. The next parameter is extremely important
    #this is the method of approximating the contours. The Chain Approximation finds contours
    #that are relatively the same intensity and throws out redundant points
    contours, hierarchy = cv.findContours(imgG,cv.RETR_LIST, cv.CHAIN_APPROX_SIMPLE)

    #we create a local variable called total_area. We then loop through all contours and add the area to the
    #running total. We return the int value in pixels.

    mildewArea = 0
    for cont in contours:
        area = cv.contourArea(cont)
        mildewArea += area

    cv.imshow("photo", imgG)
    cv.waitKey(0)
    cv.destroyAllWindows()

    return mildewArea


def threadHandler(date, tray, picNum):
    '''
    This Function accepts the three user inputs from the main function/GUI as arguments.
    It then builds a valid filepath based on the arguments. Once a valid path is created,
    this function sends that path to the findCircleArea and cannyEdgeDetection functions.
    '''
    print(thr.current_thread())

    dirName = "../photos/" + date + "/tray " + str(tray) + "/"
    fName = str(picNum) + "-160x271_" + str(picNum)

    path = dirName + fName
    path = os.path.abspath(path)

    if os.path.exists(path + ".png"): #validate the path
            print("Valid path found, staging for analyzing..")
            path = path + ".png"
            circArea = findCircleArea(path)
            mildewArea = cannyEdgeDetection(path)
            mildewRatio = mildewArea/circArea * 100
            print("Mildew to leaf ratio is: " + str(mildewRatio) + "%")
    elif os.path.exists(path + ".jpeg"): #validate the path
            path = path + ".jpeg"
            print("Valid path found, staging for analyzing..\n")
            findCircleArea(path)
            cannyEdgeDetection(path)
    elif os.path.exists(path + ".tiff"): #validate the path
            path = path + ".tiff"
            print("Valid path found, staging for analyzing..\n")
            circArea = findCircleArea(path)
            mildewArea = cannyEdgeDetection(path)
            mildewRatio = mildewArea/circArea * 100
            print("Mildew to leaf ratio is: " + str(mildewRatio) + "%")
    elif os.path.exists(path + ".tif"): #validate the path
            path = path + ".tif"
            circArea = findCircleArea(path)
            mildewArea = cannyEdgeDetection(path)
            mildewRatio = mildewArea/circArea * 100
            print("Mildew to leaf ratio is: " + str(mildewRatio) + "%")
    else: #let user know the software has detected an invalid path
            print("Invalid path detected, No file or directory resides in: \n" + path)



def main():
    tk().withdraw() #we dont want root window to pop up so we get hide it.
   
    threads = [] #creates a list of all threads to be used
    date = input("Enter a date in the form of x-xx-xx xdpi:\n") #retrieve user input
    trays = [1] #placeholder until user input is working properly
    picNums = [2] #placeholder until user input is working properly

    if len(trays)*len(picNums) > 8: #this sets the max number of pictures that can be 
        raise Exception("Too many Threads Started") #stops program from running if threads
    
    #start a new thread for every picture and tray, add it to the list, and start it
    for i in range(len(trays)):
        for j in range(len(picNums)): 
            t = thr.Thread(target = threadHandler, args = [date, trays[i], picNums[j]])
            threads.append(t)
            t.start()
    
    for t in threads:
        t.join()

main()
