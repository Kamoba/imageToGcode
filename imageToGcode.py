import cv2
import numpy as np
import scipy.ndimage
import imutils
import fonctions
import sys
import os
import time
from math import hypot

# Retrieve image name from argument
img = sys.argv[1]



#$home = '/home/pi/'
home = os.getcwd()

path = home+'/'+img
print(path)
image = cv2.imread(path)


# creating copy of original image
orig = image.copy()


# resize image so it can be processed
# choose optimal dimensions such that important content is not lost
#image = cv2.resize(image, (0,0), fx=0.5, fy=0.5)
#image = cv2.resize(image, (1500, 880))

#Set arbitraty max size (big size arout 3000 tested not working)

MAX_SIZE = 1600
height, width, channels = image.shape

if(width > MAX_SIZE):
	height = round((MAX_SIZE*height)/width)
	width = MAX_SIZE
	image = cv2.resize(image, (width, height))
if(height > MAX_SIZE):
	image = cv2.resize(image, ( round((MAX_SIZE*width)/height), MAX_SIZE ))




###########################
# get sheet paper

###########################
# remove noises
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
blurred = cv2.GaussianBlur(image, (5, 5), 0)

hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

# use script "get HSV and RGB Color.py" to get right settings
lower_white = np.array([0,0,100],dtype=np.uint8)
upper_white = np.array([179,255,255],dtype=np.uint8)

mask = cv2.inRange(hsv, lower_white, upper_white)

##(4) find all the external contours on the threshed S
#_, cnts, _ = cv2.findContours(threshed, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
cnts = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]

canvas  = image.copy()
cv2.drawContours(canvas, cnts, -1, (0,255,0), 1)

## sort and choose the largest contour
cnts = sorted(cnts, key = cv2.contourArea)
cnt = cnts[-1]



## approx the contour, so the get the corner points
arclen = cv2.arcLength(cnt, True)
approx = cv2.approxPolyDP(cnt, 0.02* arclen, True)
#cv2.drawContours(canvas, [cnt], -1, (255,0,0), 2, cv2.LINE_AA)
cv2.drawContours(canvas, [approx], -1, (0, 0, 255), 2, cv2.LINE_AA)





###########################
# convert image to sketch
###########################
def grayscale(rgb):
	return np.dot(rgb[...,:3],[0.259,0.587,0.114])  #  0.299,0.587,0.114  0.109,0.587,0.254
                              #0.199       0.001
def dodge(front,back):
	result=front*255/(255-back)
	result[result>255]=255
	result[back==255]=255
	return result.astype('uint8')

g=grayscale(image)
i=255-g

b=scipy.ndimage.filters.gaussian_filter(i,sigma=10)
sketch=dodge(b,g)


########################
# convert contours to line
########################
ret, mask = cv2.threshold(sketch, 0, 255,cv2.THRESH_BINARY_INV |cv2.THRESH_OTSU)
#image[mask == 255] = [0, 0, 255]


sketch = mask

'''
# Testing
cv2.namedWindow('sketch',cv2.WINDOW_NORMAL)
cv2.resizeWindow('sketch', 700, 900)
cv2.imshow('sketch',sketch)
cv2.waitKey(0)
cv2.destroyAllWindows()
'''


# Invert image balck n white
invertedImage = cv2.bitwise_not(sketch)



# save image 
cv2.imwrite('sketch.jpg',invertedImage)

# Wait for 1 seconds
time.sleep(1)

# generate gcode from rastercarve 
gcode = os.popen("rastercarve --width 10 sketch.jpg").read()

# save gcode file to dataURI
f = open(home+'./sketch.gcode', 'w')
f.write(gcode)
f.close()
