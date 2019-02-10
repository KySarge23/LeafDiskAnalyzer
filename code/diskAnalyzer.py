
import numpy as np
import cv2 as cv
import matplotlib.image as mpimg
import tkinter
import os
from tkinter import Tk as tk
from tkinter.filedialog import askopenfilenames
from matplotlib import pyplot as plt


#Authors: Kyle Sargent, 

def analyzeDisks(x):
    return NotImplemented

def cannyEdgeDetection(x):
    #second param: (1= color, 0= grayscale, -1 = unchanged)
    #however OCV uses BGR coloring and Matplot uses RGB coloring, so
    #when reading in with OCV, need to change to RGB if showing with matplot
    #if we want pictures to show up in RGB correctly colored.
    #notice when matplot pops up, color is distorted.
    #use line(s) 26 to remedy the problem
    #comment out line 20 and uncomment line 21 to see this effect
    
    #Reading of the same photo, in color for displaying and grayscale for edgeDetection.
    imgC = cv.imread(x,1)
    imgG = cv.imread(x,0)

    #cv.imshow('Original', img)

    #Converting img to RGB:
    imgC = cv.cvtColor(imgC, cv.COLOR_BGR2RGB)

    #use canny algorithm for edge detection
    #see https://docs.opencv.org/3.4/da/d22/tutorial_py_canny.html
    #for more details.
    edges = cv.Canny(imgG,150,200)

    #Save image into photos folder for now. so can be used in analyzeDisks method()
    #mpimg.imsave("../photos/edges.png", edges)

    cv.imshow('Edge detection', edges) #show the edge detection photo in its own window
    cv.waitKey(0) #wait 0 seconds 
    cv.destroyAllWindows() #destroy all windows on press of any character
              
def main():
    tk().withdraw() #we dont want root window to pop up so we get hide it.
    imgPath = input("Enter a date in the form of x-xx-xx xdpi\n")
    imgPath = "../photos/" + imgPath #based off hierarchy of files, is subject to change
    print(os.path.abspath(imgPath))
    imgPaths = askopenfilenames(initialdir = os.path.abspath(imgPath))

    #allow user to grab all images they wish to upload. this returns a tuple of strings
    #for path in imgPaths:  #for every image we clicked on in file explorer, run edgeDetection on it.
       #cannyEdgeDetection(path)
main()
