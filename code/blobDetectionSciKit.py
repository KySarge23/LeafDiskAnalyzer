from math import sqrt
from math import pi
from skimage import data
from skimage.feature import blob_dog, blob_log, blob_doh
from skimage.color import rgb2gray
from tkinter.filedialog import askopenfilename, askopenfilenames, asksaveasfilename

import matplotlib.pyplot as plt
import skimage
import cv2 as cv #opencv-python
import numpy as np
import tkinter as tk

def backgroundRemove(img):
    height, width = img.shape[:2]

    #Create a mask holder
    mask = np.zeros(img.shape[:2],np.uint8)

    #Grab Cut the object
    bgdModel = np.zeros((1,65),np.float64)
    fgdModel = np.zeros((1,65),np.float64)

    #create Rect The object must lie witin
    rect = (2,0,width-10,height)
    cv.grabCut(img,mask,rect,bgdModel,fgdModel,100,cv.GC_INIT_WITH_RECT)
    mask = np.where((mask==2)|(mask==0),0,1).astype('uint8')
    final = img*mask[:,:,np.newaxis]

    # cv.imshow("im1", final)
    # cv.waitKey(0)
    # cv.destroyAllWindows()

    return final


root = tk.Tk()
root.withdraw() 



image = skimage.io.imread(askopenfilename(initialdir = "../photos", title = "Choose Photo"))

print(image.shape)

h,w = image.shape[:2]

if h > 280 and w > 423:
        image = cv.resize(image,(423,280)) #resize image, for easier reading and faster execution.

try:
    image = backgroundRemove(image)
except:
    image = cv.cvtColor(image, cv.COLOR_BGRA2BGR)
    # cv.imshow("new photo", image)
    image = backgroundRemove(image)
    # cv.imshow("Background removed", image)
    # cv.waitKey(0)
    # cv.destroyAllWindows()

image = cv.medianBlur(image,3) #add blur to reduce noise on photo.


hsv = cv.cvtColor(image, cv.COLOR_BGR2HSV)

# cv.imshow('hsv', hsv)
# cv.waitKey(0)
# cv.destroyAllWindows()

#darker colors (to mask out)
lower_green = np.array([0,0, 180])
#lighter colors
upper_green = np.array([255, 255, 255])

#masking pixels to remove irrelevant data
mask = cv.inRange(hsv, lower_green, upper_green)
res = cv.bitwise_and(image, image, mask=mask)

image_gray = rgb2gray(res)

# cv.imshow('gray mildew', image_gray)
# cv.waitKey(0)
# cv.destroyAllWindows()

blobs_log = blob_log(image_gray, max_sigma=30, num_sigma=10, threshold=0.091)
# Compute radii in the 3rd column.
blobs_log[:, 2] = blobs_log[:, 2] * sqrt(2)

blobs_dog = blob_dog(image_gray, max_sigma=30, threshold=.1)
blobs_dog[:, 2] = blobs_dog[:, 2] * sqrt(2)

blobs_doh = blob_doh(image_gray, max_sigma=30, threshold=.075)

blobs_list = [blobs_log, blobs_dog, blobs_doh]
colors = ['yellow', 'lime', 'red']
titles = ['Laplacian of Gaussian', 'Difference of Gaussian',
        'Determinant of Hessian']
sequence = zip(blobs_list, colors, titles)

fig, axes = plt.subplots(1, 3, figsize=(9, 3), sharex=True, sharey=True)
ax = axes.ravel()

blobArea = 0
for idx, (blobs, color, title) in enumerate(sequence):
    ax[idx].set_title(title)    
    ax[idx].imshow(image)
    if idx == 0:
        for blob in blobs:
            y, x, r = blob
            # print(r)
            c = plt.Circle((x, y), r, color=color, linewidth=2, fill=False)
            blobArea += pi * (r**2)
            ax[idx].add_patch(c)
        ax[idx].set_axis_off()
    else:
        for blob in blobs:
            y, x, r = blob
            c = plt.Circle((x, y), r, color=color, linewidth=2, fill=False)
            ax[idx].add_patch(c)
        ax[idx].set_axis_off()

plt.tight_layout()
plt.show()


root.mainloop()
root.destroy()