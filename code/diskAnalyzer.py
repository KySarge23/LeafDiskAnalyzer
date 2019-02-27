#!/usr/bin/env python3

import cv2 as cv
import numpy as np
import matplotlib.image as mpimg
import tkinter
import os
from tkinter import Tk as tk
from tkinter.filedialog import askopenfilenames
from matplotlib import pyplot as plt


#Author(s): Kyle Sargent

def findCircle(x):
    img = cv.imread(x,0)
    img = cv.medianBlur(img,5)
    cimg = cv.cvtColor(img,cv.COLOR_GRAY2BGR)

    #params are as follows: (image, method = cv2.HOUGH_GRADIENT is the only one that works thus far, dp, minDist, parap1 = gradient value,
    #param2 = accumulator threshold value for method input, minRadius, maxRadius)
    circles = cv.HoughCircles(img,cv.HOUGH_GRADIENT,1,150,
                            param1=50,param2=30,minRadius=0,maxRadius=0)

    circles = np.uint8(np.around(circles))
    for i in circles[0,:]:
        # draw the detected outer circle
        #params are as follows: (image, center coords,bgr values, thickness)
        cv.circle(cimg,(i[0],i[1]),i[2],(0,255,0),2)
        print(cv.circle(cimg,(i[0],i[1]),i[2],(0,255,0),2))
    cv.imshow('detected circles',cimg)
    cv.waitKey(0)
    cv.destroyAllWindows() 
    return NotImplemented

def cannyEdgeDetection(x):
    print("Edge Detection starting")
    
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
    edges = cv.Canny(imgG,150,250)

    #Save image into photos folder for now. so can be used in analyzeDisks method

    mpimg.imsave("../photos/edges.png", edges)

    print("Edge Detection Complete")
    
    cv.imshow('Edge detection', edges) #show the edge detection photo in its own window
    cv.waitKey(0) #wait "forerver" for more details go to: https://docs.opencv.org/2.4/modules/highgui/doc/user_interface.html?highlight=waitkey#waitkey
    cv.destroyAllWindows() #destroy all windows on press of any character
    print("Closing Window")
    
              
def main():
    tk().withdraw() #we dont want root window to pop up so we get hide it.
    
    #datePath = input("Enter a date in the form of x-xx-xx xdpi:\n") #retrieve user input
    #datePath = "../photos/" + datePath #based off hierarchy of files, is subject to change

    #get tray number from user
    #trayPath = input("Enter the tray number(s) you wish to use in the form of '1-3' or '1,3,5': ")
    #amend the path to specific folder.
    #trayPath = datePath + "/tray " + str(trayPath) #only works with single tray #s thus far.

    #print(trayPath)

    #error checking against the filepath gained from the two inputs.
    #if os.path.exists(trayPath):
        #askopenfilenames() does the following: allow user to grab all images they wish to upload Then this returns a tuple of strings
        
    imgPaths = askopenfilenames(initialdir = '../photos/') #converts the input retrieved from user into an absolute path, and opens a explorer in that file
    for path in imgPaths:  #for every image we clicked on in file explorer, run edgeDetection on it. #refactor if-else into own function later? maybe.
        if os.path.exists(path): #validate the path
            print("Valid path entered, staging for analyzing..")
            findCircle(path)
            cannyEdgeDetection(path)
        else: #let user know the software has detected an invalid path
            print("Invalid path detected, No file or directory resides in: \n" + path)

    #if the path input is not valid, then let user know without entering the loop.         
    #else: print("Invalid path detected, No directory found of: " + os.path.abspath(trayPath)





main()
