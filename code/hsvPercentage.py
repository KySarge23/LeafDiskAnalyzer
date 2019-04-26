import cv2 as cv
import numpy as np
import math

'''
This program uses hsv detection to return mildew percentage on
the leaf'''


'''
This function returns ratio based on hsv detection
'''
def hsvRatio(image):
    image = cv.resize(image,(423,280)) 
    hsv = cv.cvtColor(image, cv.COLOR_BGR2HSV)

    #getting height and width of image (for testing purposes)
    height, width, channel= hsv.shape


    #I used my background removal algorithm to remove the background from
    #the total pixel count (can replace this with circle detecter from the original code
    #=================================================================
    totalArea = backgroundRemove(image)
    #=================================================================
    

    #adding hsv values to list
    hsvValues = []
    for x in range(0, width):
        for y in range(0, height):
            pixel= hsv[y, x]
            #print(pixel)
            hsvValues.append(pixel)


    #find the amount of pixels above a specified brightness value (I chose 150)
    #runs through the array of hsv values and counts the pixels over 150 brightned
    numOfPixels = 0
    for j in range(0, len(hsvValues)):
        #print(hsvValues[j])
        if(np.all(hsvValues[j] > np.array([0,0,150]))):
            numOfPixels +=1

    return numOfPixels/totalArea


'''
This Function I used to get total area of the leaf.
In our original design we used circle detection
this function can replace with the circle function
'''

def backgroundRemove(img):
    height, width = img.shape[:2]

    #Create a mask holder
    mask = np.zeros(img.shape[:2],np.uint8)

    #Grab Cut the object
    bgdModel = np.zeros((1,65),np.float64)
    fgdModel = np.zeros((1,65),np.float64)


    #create Rect The object must lie witin
    rect = (2,0,width-5,height)
    cv.grabCut(img,mask,rect,bgdModel,fgdModel,4,cv.GC_INIT_WITH_RECT)
    mask = np.where((mask==2)|(mask==0),0,1).astype('uint8')
    img1 = img*mask[:,:,np.newaxis]

    #Get the background
    background = img - img1

    #Change all pixels in the background to what ever color you want
    #I went with Red because of high contast with the green leaf disk
    background[np.where((background > [0,0,0]).all(axis = 2))] = [0,0,0]

    #Add the background and the image
    final = background + img1
    
    height, width, channel= final.shape

    #remove background from pixel count
    totalArea = 0
    for x in range(0, width):
        for y in range(0, height):
            pixel= final[y, x]
            if(np.any(pixel > np.array([0,0,0]))):
                totalArea +=1
    #print(totalArea)

    return totalArea

'''
This function I'm not sure if its necessary
It creates an array of all pixels but sets all non-pathogens
pixel data to [0,0,0]

'''
def showOnlyPathogen(image):
    image = cv.resize(image,(423,280))
    hsv = cv.cvtColor(image, cv.COLOR_BGR2HSV)

    #darker colors (to mask out)
    lower_green = np.array([0,0, 150])
    #lighter colors
    upper_green = np.array([255, 255, 255])

    #masking pixels to remove irrelevant data
    mask = cv.inRange(hsv, lower_green, upper_green)
    res = cv.bitwise_and(image, image, mask=mask)

    '''
    #show image (for testing purposes)
    cv2.imshow('res1.png', res)
    cv2.waitKey(0)
    '''

    height, width, channel= res.shape

    #creates an array of all pixels in the image
    #The value of al pixels that are not the pathogen are set to [0,0,0]
    resValues = []
    for x in range(0, width):
        for y in range(0, height):
            pixel= res[y, x]
            #print(pixel)
            resValues.append(pixel)


def main():
    
    img = cv.imread('fileName.png',1)

    print(hsvRatio(img))

    showOnlyPathogen(img)

main()
