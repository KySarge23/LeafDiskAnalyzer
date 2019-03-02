#!/usr/bin/python3


import numpy as np
import cv2


def backgroundRemove(x):
    #Load the Image
    img = cv2.imread(x)
    height, width = img.shape[:2]

    #Create a mask holder
    mask = np.zeros(img.shape[:2],np.uint8)

    #Grab Cut the object
    bgdModel = np.zeros((1,65),np.float64)
    fgdModel = np.zeros((1,65),np.float64)


    #create Rect The object must lie witin
    rect = (2,0,width-5,height)
    cv2.grabCut(img,mask,rect,bgdModel,fgdModel,4,cv2.GC_INIT_WITH_RECT)
    mask = np.where((mask==2)|(mask==0),0,1).astype('uint8')
    img1 = img*mask[:,:,np.newaxis]

    #Get the background
    background = img - img1

    #Change all pixels in the background to what ever color you want
    #I went with Red because of high contast with the green leaf disk
    background[np.where((background > [0,0,0]).all(axis = 2))] = [0,0,255]

    #Add the background and the image
    final = background + img1

    ###Code to diplay new image in box
    cv2.namedWindow('image', cv2.WINDOW_NORMAL)
    cv2.imshow('image', final )

    cv2.imwrite("backgroundRemoved1.png", final)


def main():
    backgroundRemove('../photos/9-15-18 2dpi/tray 1/1-160x271_T1S.tiff')

main()
    



