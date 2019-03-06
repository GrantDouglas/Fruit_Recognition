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
	color = cv2.imread("images/citrus1.jpg",1)

	#kernel = np.ones((10,10),np.uint8)

	#img = cv2.morphologyEx(img, cv2.MORPH_OPEN, kernel)
	#cv2.imwrite("open.png", img)


	img = cv2.medianBlur(img,5)
	cimg = cv2.cvtColor(img,cv2.COLOR_GRAY2BGR)

	circles = cv2.HoughCircles(img,cv2.HOUGH_GRADIENT,2,200,
	                            param1=100,param2=100, minRadius=0,maxRadius=3000)

	circles = np.uint16(np.around(circles))


	count = 0
	num = 0
	averageR = 0
	for i in circles[0,:]:


 		if  (averageR == 0 and i[2] < 450) or (averageR != 0 and i[2] <= averageR*1.5 and  i[2] >= averageR*0.5):

			mask = np.zeros(shape=(img.shape[0], img.shape[1]))
			cv2.circle(mask,(i[0],i[1]),i[2],255, -1)
			cv2.imwrite("mask.png", mask)
			vals = countWhite(mask, img, (i[0],i[1]),i[2], num)

			ratio = int(vals[1] / float(vals[0])*100)

			if ratio >= 50:
				count += 1



				if averageR == 0:
					averageR = i[2]
				else:
					if i[2] <= averageR*1.5 and  i[2] >= averageR*0.5:
						averageR = (averageR + i[2]) / 2.0
					else:
						print("Circcle that is > 50% is either too big or too small");
						cv2.circle(cimg,(i[0],i[1]),i[2],(226, 66, 244),10)
						# draw the center of the circle
						cv2.putText(cimg,str(num),(i[0],i[1]), cv2.FONT_HERSHEY_COMPLEX_SMALL, 2,(0,0,255),2,cv2.LINE_AA)
						continue

				# draw the outer circle
				cv2.circle(cimg,(i[0],i[1]),i[2],(0,255,0),10)
			    # draw the center of the circle
				#cv2.circle(cimg,(i[0],i[1]),2,(0,0,255),5)
				cv2.putText(cimg,str(num),(i[0],i[1]), cv2.FONT_HERSHEY_COMPLEX_SMALL , 2,(0,0,255),2,cv2.LINE_AA)

				cv2.circle(color,(i[0],i[1]),i[2],(0,255,0),10)
			    # draw the center of the circle
				cv2.circle(color,(i[0],i[1]),2,(0,0,255),5)

			elif ratio >= 30:

				print(ratio)
				if i[2] <= averageR*1.2 and  i[2] >= averageR*0.2:
					cv2.circle(cimg,(i[0],i[1]),i[2],(66, 134, 244),10)

					cv2.circle(color,(i[0],i[1]),i[2],(66, 134, 244),10)
				    # draw the center of the circle
					cv2.circle(color,(i[0],i[1]),2,(0,0,255),5)

				else:
					cv2.circle(cimg,(i[0],i[1]),i[2],(0, 8, 255),10)

				# draw the center of the circle
				cv2.putText(cimg,str(num),(i[0],i[1]), cv2.FONT_HERSHEY_COMPLEX_SMALL, 2,(0,0,255),2,cv2.LINE_AA)
			else:

				print(ratio)
				cv2.circle(cimg,(i[0],i[1]),i[2],(226, 66, 244),10)
				# draw the center of the circle
				cv2.putText(cimg,str(num),(i[0],i[1]), cv2.FONT_HERSHEY_COMPLEX_SMALL, 2,(0,0,255),2,cv2.LINE_AA)


		num +=1


	print(count)
	cv2.imwrite("final.png", cimg)
	cv2.imwrite("out.png", color)


def countWhite(mask, img, center, radius, index):

	numTotal = int(3.14 * radius**2)
	numWhite = 0
	numOutside = numTotal


	lowerbound_out = max(int(center[1]) - radius, 0)
	upperbound_out = min(center[1] + radius, img.shape[0])

	lowerbound_in = max(int(center[0]) - radius, 0)
	upperbound_in = min(center[0] + radius, img.shape[1])

	for k in range(lowerbound_out, upperbound_out):
		for i in range(lowerbound_in, upperbound_in):

			if (mask[k,i] == 255 and img[k,i] == 0):
				numWhite += 1

			if (mask[k,i] == 255):
				numOutside -= 1



	if (numOutside / float(numTotal)*100) > 40:
		print("too much outside of img: ", (numOutside / float(numTotal)*100))

	else:
		numWhite += numOutside

	print("index:", index, numTotal, numWhite)

	return (numTotal, numWhite)

if __name__ == '__main__':

    # imageList = os.listdir("./images/")

    imageList = "citrus1_mask.jpg"

    circleCount(imageList)
