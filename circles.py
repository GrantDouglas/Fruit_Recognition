#!/usr/local/bin/python


##
#
# Citrus 4 should have about 22 circles
#
#


import os
import cv2
import numpy as np



def circleCount(fname):

	img = cv2.imread("masks/" + fname,0)
	kernel = np.ones((10,10),np.uint8)

	img = cv2.morphologyEx(img, cv2.MORPH_OPEN, kernel)
	cv2.imwrite("open.png", img)


	img = cv2.medianBlur(img,5)
	cimg = cv2.cvtColor(img,cv2.COLOR_GRAY2BGR)

	circles = cv2.HoughCircles(img,cv2.HOUGH_GRADIENT,2,200,
	                            param1=100,param2=100, minRadius=0,maxRadius=3000)

	circles = np.uint16(np.around(circles))


	count = 0
	for i in circles[0,:]:

 		if i[2] < 500:

			mask = np.zeros(shape=(img.shape[0], img.shape[1]))
			cv2.circle(mask,(i[0],i[1]),i[2],255, -1)
			vals = countWhite(mask, img, (i[0],i[1]),i[2])

			if vals[1] >  vals[0] / 2:
				count += 1
				# draw the outer circle
				cv2.circle(cimg,(i[0],i[1]),i[2],(0,255,0),2)
			    # draw the center of the circle

				cv2.circle(cimg,(i[0],i[1]),2,(0,0,255),3)



	print(count)
	cv2.imwrite("final.png", cimg)


def countWhite(mask, img, center, radius):

	numTotal = 3.14 * radius**2
	numWhite = 0


	lowerbound_out = max(center[1] - radius, 0)
	upperbound_out = min(center[1] + radius, img.shape[0])

	lowerbound_in = max(center[0] - radius, 0)
	upperbound_in = min(center[0] + radius, img.shape[1])


	for k in range(lowerbound_out, upperbound_out):
		for i in range(lowerbound_in, upperbound_in):

			if (mask[k,i] == 255 and img[k,i] == 255):
				numWhite += 1



	print(numTotal, " ", numWhite)

	return (numTotal, numWhite)

if __name__ == '__main__':

    # imageList = os.listdir("./images/")

    imageList = "citrus4_mask_invert.jpg"

    circleCount(imageList)
