#!/usr/bin/env python3

import numpy as np
import cv2 as cv
import matplotlib.image as mpimg
import tkinter
import os
from tkinter import Tk as tk
from tkinter.filedialog import askopenfilenames
from matplotlib import pyplot as plt


#Author(s): Kyle Sargent

def analyzeDisks(x):
    return NotImplemented

def cannyEdgeDetection(x):
    print("Edge Detection starting")
    #second param: (1= color, 0= grayscale, -1 = unchanged)
    #however OCV uses BGR coloring and Matplot uses RGB coloring, so
    #when reading in with OCV, need to change to RGB if showing with matplot
    #if we want pictures to show up in RGB correctly colored.
    #notice when matplot pops up, color is distorted.
    #use line(s) 26 to remedy the problem
    #comment out line 20 and uncomment line 21 to see this effect
    
    #Reading of the same photo, in color for displaying and grayscale for edgeDetection.
    #imgC = cv.imread(x,1)
    imgG = cv.imread(x,0)

    #cv.imshow('Original', img)

    #Converting img to RGB:
    #imgC = cv.cvtColor(imgC, cv.COLOR_BGR2RGB)

    #use canny algorithm for edge detection
    #see https://docs.opencv.org/3.4/da/d22/tutorial_py_canny.html
    #for more details.
    edges = cv.Canny(imgG,150,200)

    #Save image into photos folder for now. so can be used in analyzeDisks method()
    #mpimg.imsave("../photos/edges.png", edges)

    print("Edge Detection Complete")
    
    cv.imshow('Edge detection', edges) #show the edge detection photo in its own window
    cv.waitKey(0) #wait "forerver" for more details go to: https://docs.opencv.org/2.4/modules/highgui/doc/user_interface.html?highlight=waitkey#waitkey
    cv.destroyAllWindows() #destroy all windows on press of any character
    print("Closing Window")
    
              
def main():
    tk().withdraw() #we dont want root window to pop up so we get hide it.
    datePath = input("Enter a date in the form of x-xx-xx xdpi:\n") #retrieve user input
    datePath = "../photos/" + datePath #based off hierarchy of files, is subject to change

    #get tray number from user
    trayPath = input("Enter the tray number(s) you wish to use in the form of '1-3' or '1,3,5': ")
    #amend the path to specific folder.
    trayPath = datePath + "/tray " + str(trayPath) #only works with single tray #s thus far.

    print(trayPath)

    #error checking against the filepath gained from the two inputs.
    if os.path.exists(trayPath):
        #askopenfilenames() does the following: allow user to grab all images they wish to upload Then this returns a tuple of strings
        imgPaths = askopenfilenames(initialdir = os.path.abspath(trayPath)) #converts the input retrieved from user into an absolute path, and opens a explorer in that file
        
        for path in imgPaths:  #for every image we clicked on in file explorer, run edgeDetection on it. #refactor if-else into own function later? maybe.
           if os.path.exists(path): #validate the path
               print("Valid path entered, staging for analyzing..")
               cannyEdgeDetection(path)
               
           else: #let user know the software has detected an invalid path
               print("Invalid path detected, No file or directory resides in: \n" + path)
               
    #if the path input is not valid, then let user know without entering the loop.         
    else: print("Invalid path detected, No directory found of: " + os.path.abspath(trayPath))






main()
