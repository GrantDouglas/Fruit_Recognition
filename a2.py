#!/usr/bin/python3


import cv2
import numpy as np
from PIL import Image, ImageCms, ImageEnhance
from skimage import color
from scipy import ndimage
import matplotlib.pyplot as plt


def openImage(fname):
    return cv2.imread(fname)



def shadowReduce(image):

    # convert original to LAB, split the channels
    lab = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
    l, a, b = cv2.split(lab)

    # increase luminosity if the value will not overflow
    l[l < 245] += 10

    # merge channels together and convert back to RGB
    limg = cv2.merge((l, a, b))
    img = cv2.cvtColor(limg, cv2.COLOR_LAB2BGR)

    # make intermediary for testing purposes
    cv2.imwrite("shadow.png", img)

    return img



def varianceFilter(img):

    wmean, wsqrmean = (cv2.boxFilter(x, -1, (3, 3), borderType=cv2.BORDER_REFLECT) for x in (img, img*img))
    win_var = wsqrmean - wmean**2

    gray = cv2.cvtColor(win_var, cv2.COLOR_BGR2GRAY)
    cv2.imwrite("var.png", gray)


def kMeansAlgo():
    print("do this too")


if __name__ == '__main__':
    image = openImage("./images/orange1.jpg")

    shadow_res = shadowReduce(image)
    varianceFilter(shadow_res)





