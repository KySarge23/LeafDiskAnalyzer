import numpy as np
import cv2 as cv
from matplotlib import pyplot as plt

def analyzeDisks():
    #waiting to implement
    return NotImplemented


def edgeDetection(x):
    #second param: (1= color, 0= grayscale, -1 = unchanged)
    #however OCV uses BGR coloring and Matplot uses RGB coloring, so
    #when reading in with OCV, need to change to RGB if showing with matplot
    #if we want pictures to show up in RGB correctly colored.
    #notice when matplot pops up, color is distorted.
    #use line(s) 20/21 to remedy the problem
    #comment out line 19 and uncomment line 18 to see this effect.
    #img = cv.imread(x,1)
    img = cv.imread(x,0)
    

    #cv.imshow('Original', img)
    
    #Converting img to RGB:
    #img = cv.cvtColor(img, cv.COLOR_BGR2RGB)
    
    edges = cv.Canny(img,100,200) #use canny algorithm for edge detection see https://docs.opencv.org/3.4/da/d22/tutorial_py_canny.html for more details.

    #creation of subplots 
    plt.subplot(121),plt.imshow(img,cmap='gray')
    plt.title('Original Image')
    plt.subplot(122),plt.imshow(edges,cmap='gray')
    plt.title('Edge Dectection')
    plt.show()

def main():
    #retrieve image from photos folder and pass as param.
    edgeDetection('../photos/leafDiskMildew.png')
    

main()
