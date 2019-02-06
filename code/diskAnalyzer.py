import numpy as np
import cv2 as cv
from matplotlib import pyplot as plt

def analyzeDisks():
    edgeDetection('../photos/leafDiskMildew.png')
    return NotImplemented


def edgeDetection(x):
    #second param: (1= color, 0= grayscale, -1 = unchanged)
    #however OCV uses BGR coloring and Matplot uses RGB coloring, so
    #when reading in with OCV, need to change to RGB if showing with matplot
    #if we want pictures to show up in RGB correctly colored.
    #notice when matplot pops up, color is distorted.
    #use line(s) 26 to remedy the problem
    #comment out line 20 and uncomment line 21 to see this effect
    
    #Reading of the same photo, in color and grayscale for edgeDetection.
    imgC = cv.imread(x,1)
    imgG = cv.imread(x,0)

    #cv.imshow('Original', img)

    #Converting img to RGB:
    imgC = cv.cvtColor(imgC, cv.COLOR_BGR2RGB)

    #use canny algorithm for edge detection
    #see https://docs.opencv.org/3.4/da/d22/tutorial_py_canny.html
    #for more details.
    edges = cv.Canny(imgG,100,200)


    #creation of subplots
    plt.subplot(121),plt.imshow(imgC)
    plt.title('Original Image')
    plt.subplot(122),plt.imshow(edges,cmap='gray')
    plt.title('Edge Dectection')
    plt.show()

def main():
    #call analyzing
    analyzeDisks()
   


main()
