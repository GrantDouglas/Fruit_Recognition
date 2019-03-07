#!/usr/local/bin/python


##
#
# Citrus 4 should have about 22 circles
#
#


import os
import cv2
import numpy as np


BLUE = (255, 0, 0)
GREEN = (0, 255, 0)
ORANGE = (66, 134, 244)
PURPLE = (226, 66, 244)
RED = (0, 0, 255)
PINK= (255, 255, 0)



def circleCount(fname):

    img = cv2.imread("masks/" + fname + "_mask.jpg",0)
    color = cv2.imread("images/" + fname + ".jpg",1)

    img = cv2.medianBlur(img,5)
    cimg = cv2.cvtColor(img,cv2.COLOR_GRAY2BGR)

    circles = cv2.HoughCircles(img,cv2.HOUGH_GRADIENT,2,150,
                                param1=100,param2=100, minRadius=0,maxRadius=3000)

    circles = np.uint16(np.around(circles))


    count = 0
    num = 0
    averageR = 0
    for i in circles[0,:]:

        if num == 12:
            cv2.circle(cimg,(i[0],i[1]),i[2],RED,10)


        if  (averageR == 0) or (averageR != 0 and i[2] <= averageR*1.5 and  i[2] >= averageR*0.5):

            mask = np.zeros(shape=(img.shape[0], img.shape[1]))
            cv2.circle(mask,(i[0],i[1]),i[2],255, -1)
            vals = countWhite(mask, img, (i[0],i[1]),i[2], num)

            ratio = int(vals[1] / float(vals[0])*100)

            if ratio >= 50:
                count += 1

                if averageR == 0:
                    averageR = i[2]
                else:
                    averageR = (averageR + i[2]) / 2.0

                # draw the outer circle
                cv2.circle(cimg,(i[0],i[1]),i[2],GREEN,10)
                cv2.circle(color,(i[0],i[1]),i[2],GREEN,10)
                # draw the center of the circle
                cv2.circle(color,(i[0],i[1]),2,BLUE,5)

            elif ratio >= 30:

                print(ratio)
                if i[2] <= averageR*1.2 and  i[2] >= averageR*0.8:

                    cv2.circle(cimg,(i[0],i[1]),i[2],ORANGE,10)
                    cv2.circle(color,(i[0],i[1]),i[2],ORANGE,10)
                    # draw the center of the circle
                    cv2.circle(color,(i[0],i[1]),2,BLUE,5)

                elif i[2] <= averageR*1.4:
                    cv2.circle(cimg,(i[0],i[1]),i[2],RED,10)
            else:

                print(ratio)



                if i[2] <= averageR*1.3:
                    cv2.circle(cimg,(i[0],i[1]),i[2],PURPLE,10)

            # write the circle number
            cv2.putText(cimg,str(num),(i[0],i[1]), cv2.FONT_HERSHEY_COMPLEX_SMALL , 2,BLUE,2,cv2.LINE_AA)

        else:
            if i[2] <= averageR*1.8 and  i[2] >= averageR*0.2:
                cv2.circle(cimg,(i[0],i[1]),i[2],PINK,10)
        num +=1


    print(count)

    if not os.path.exists('circle_stage1'):
        os.makedirs('circle_stage1')

    if not os.path.exists('final'):
        os.makedirs('final')

    cv2.imwrite("circle_stage1/" +  fname + "_circles.png", cimg)
    cv2.imwrite("final/" +  fname + "_circles.png", color)


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

    circleCount("citrus1")
    # circleCount("citrus2")
    # circleCount("citrus3")
    # circleCount("citrus4")
    # circleCount("citrus5")
    # circleCount("citrus6")
    # circleCount("citrus7")
    # circleCount("citrus8")
    # circleCount("orange1")
