import numpy as np
import cv2 as cv
from matplotlib import pyplot as plt

def analyzeDisks():
    return NotImplemented


def edgeDetection(x):
    img = cv.imread(x,0)
    edges = cv.Canny(img,100,200)

    plt.subplot(121),plt.imshow(img,cmap='gray')
    plt.title('Original Image')
    plt.subplot(122),plt.imshow(edges,cmap='gray')
    plt.title('Edge Dectection')
    plt.show()

def main():
    edgeDetection('../photos/leafDiskMildew.png')
    

main()
