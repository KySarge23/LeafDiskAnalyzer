import cv2
import numpy as np

img = cv2.imread('leafDiskMildew.png',1)
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

#print(hsv)

#getting height and width of image
height, width, channel= hsv.shape
print (height, width)

#adding hsv values to list
hsvValues = []
for x in range(0, width):
    for y in range(0, height):
        pixel= hsv[y, x]
        #print(pixel)
        hsvValues.append(pixel)

#code below prints hsv values (takes a long time so I commented it out)
'''
for j in range(0, len(hsvValues)):
    print(hsvValues[j])
'''

#HSV = [hugh, saturation, value(Brightness)]

'''Code below maskes out code below a certain brightness
    This is a common thing HSV is used for from what I've seen'''

#darker colors (to mask out)
lower_green = np.array([0,0, 150])
#lighter colors
upper_green = np.array([255, 255, 255])


#
mask = cv2.inRange(hsv, lower_green, upper_green)
res = cv2.bitwise_and(img, img, mask=mask)

cv2.imshow('res1.png', res)
cv2.waitKey(0)






