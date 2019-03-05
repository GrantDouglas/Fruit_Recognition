#!/usr/bin/python3

import os
import cv2
import numpy as np



def circleCount(fname):

	img = cv2.imread("masks/" + fname,0)
	img = cv2.medianBlur(img,5)
	cimg = cv2.cvtColor(img,cv2.COLOR_GRAY2BGR)

	circles = cv2.HoughCircles(img,cv2.HOUGH_GRADIENT,2,30,
	                            param1=100,param2=100, minRadius=100,maxRadius=3000)
	print(len(circles))

	circles = np.uint16(np.around(circles))
	for i in circles[0,:]:
	    # draw the outer circle
	    cv2.circle(cimg,(i[0],i[1]),i[2],(0,255,0),2)
	    # draw the center of the circle
	    cv2.circle(cimg,(i[0],i[1]),2,(0,0,255),3)


	cv2.imwrite("final.png", cimg)



if __name__ == '__main__':

    # imageList = os.listdir("./images/")

    imageList = "citrus4_mask_invert.jpg"

    circleCount(imageList)