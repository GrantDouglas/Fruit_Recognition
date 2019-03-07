#!/usr/local/bin/python


##
#
# Citrus 4 should have about 22 circles
#
#


import os
import cv2
import numpy as np
from joblib import Parallel, delayed
import multiprocessing


BLUE = (255, 0, 0)
GREEN = (0, 255, 0)
ORANGE = (66, 134, 244)
PURPLE = (226, 66, 244)
RED = (0, 0, 255)
CYAN= (255, 255, 0)
MAROON = (76, 19, 76)



def circleCount(fname):

    img = cv2.imread("masks/" + fname + "_mask.jpg",0)
    color = cv2.imread("images/" + fname + ".jpg",1)

    img = cv2.medianBlur(img,3)
    cimg = cv2.cvtColor(img,cv2.COLOR_GRAY2BGR)

    circles = cv2.HoughCircles(img,cv2.HOUGH_GRADIENT,2.5,150,
                                param1=100,param2=100, minRadius=0,maxRadius=3000)

    circles = np.uint16(np.around(circles))


    count = 0
    num = 0
    averageR = 0
    for i in circles[0,:]:

        if (i[2] > img.shape[0] / 4 or i[2] > img.shape[1] / 4):
            print("r is > 1/4 of size")
            continue

        mask = np.zeros(shape=(img.shape[0], img.shape[1]))
        cv2.circle(mask,(i[0],i[1]),i[2],255, -1)
        ratio = countWhite(mask, img, (i[0],i[1]),i[2], num)


        if ratio < 20:
            continue

        print(num, " ", ratio)
        # write the circle number


        #if num == 22:
        #    cv2.circle(cimg,(i[0],i[1]),i[2],RED,10)


        if  (averageR == 0) or (averageR != 0 and i[2] <= averageR*1.5 and  i[2] >= averageR*0.5):


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
                    cv2.circle(cimg,(i[0],i[1]),i[2],RED,10)            # slightly larger or too small
                    cv2.circle(color,(i[0],i[1]),i[2],RED,10)

                else:
                    cv2.circle(cimg,(i[0],i[1]),i[2],PURPLE,10)         # too large, (altho could still be valid)
                    cv2.circle(color,(i[0],i[1]),i[2],PURPLE,10)

            else:

                # not filled enough but close in size
                if i[2] <= averageR*1.2 and  i[2] >= averageR*0.8:
                    cv2.circle(color,(i[0],i[1]),i[2],MAROON,10)
                    cv2.circle(cimg,(i[0],i[1]),i[2],MAROON,10)

            cv2.putText(cimg,str(num),(i[0],i[1]), cv2.FONT_HERSHEY_COMPLEX_SMALL , 2,BLUE,2,cv2.LINE_AA)
        else:

            if ratio > 40:
                cv2.circle(cimg,(i[0],i[1]),i[2],CYAN,10)
                cv2.putText(cimg,str(num),(i[0],i[1]), cv2.FONT_HERSHEY_COMPLEX_SMALL , 2,BLUE,2,cv2.LINE_AA)
        num +=1


    print(count)

    if not os.path.exists('circle_stage1'):
        os.makedirs('circle_stage1')

    if not os.path.exists('final'):
        os.makedirs('final')

    cv2.imwrite("circle_stage1/" +  fname + "_circles.png", cimg)
    cv2.imwrite("final/" +  fname + "_circles.png", color)


##
## This will return a the percentage of the black pixles in the circle * 100
## If the circle goes off the edge of the page and < 40% is outside the page then
## those pixels will be counted as if they are filled in
def countWhite(mask, img, center, radius, index):

    numTotal = int(3.14 * radius**2)
    numWhite = 0
    numOutside = numTotal

    white = np.zeros(shape=(img.shape[0], img.shape[1]))
    count = np.zeros(shape=(img.shape[0], img.shape[1]))

    white[(mask == 255) & (img == 0)] = 255
    count[(mask == 255) ] = 255

    unique, counts = np.unique(white, return_counts=True)
    res = dict(zip(unique, counts))

    numWhite = res.get(255)

    unique, counts = np.unique(count, return_counts=True)
    res = dict(zip(unique, counts))

    numInFrame = res.get(255)

    numOutside -= numInFrame

    if (numOutside / float(numTotal)*100) > 40:
        print("too much outside of img: ", (numOutside / float(numTotal)*100))

    else:
        numWhite += numOutside

    #print("index:", index, numTotal, numWhite)


    ratio1 = int(numWhite / float(numTotal)*100)
    ratio2 = int(numWhite / float(numInFrame)*100)


    if ratio2 < ratio1:
        print("too much white in frame")

    return min(ratio1, ratio2)





if __name__ == '__main__':

    # imageList = os.listdir("./images/")

    imageList = [
        "citrus1",
        "citrus2",
        "citrus3",
        "citrus4",
        "citrus5",
        "citrus6",
        "citrus7",
        "citrus8",
        "orange1"]
    #cpu_count = multiprocessing.cpu_count()
    #res = Parallel(n_jobs=cpu_count)(delayed(circleCount)(k) for k in imageList)

    circleCount("citrus1")
    circleCount("citrus2")
    #circleCount("citrus3")
    #circleCount("citrus4")
    #circleCount("citrus5")
    #circleCount("citrus6")
    #circleCount("citrus7")
    #circleCount("citrus8")
    #circleCount("orange1")
