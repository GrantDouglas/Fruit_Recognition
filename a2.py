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

    b, g, r = cv2.split(img)

    NDI(img)



    r_var = ndimage.generic_filter(r, np.var, size=3)
    g_var = ndimage.generic_filter(g, np.var, size=3)
    b_var = ndimage.generic_filter(b, np.var, size=3)

    cv2.imwrite("var1.png", r_var)
    cv2.imwrite("var2.png", g_var)
    cv2.imwrite("var3.png", b_var)

    fin = (r_var + g_var + b_var) / 3

    cv2.imwrite("var4.png", fin)

    # gray_threshold
    for k in range(0, img.shape[0]):
        for i in range(0, img.shape[1]):
            if fin[k, i] <= 90:
                fin[k, i] = 0
            else:
                fin[k, i] = 255

    cv2.imwrite("var5.png", fin)


    # convert image to YCrBr color space
    ycrbr = cv2.cvtColor(img, 36)
    y, cr, br = cv2.split(ycrbr)

    # cr threshold
    for k in range(0, img.shape[0]):
        for i in range(0, img.shape[1]):
            if cr[k, i] >= 150:
                cr[k, i] = 0
            else:
                cr[k, i] = 255

    cv2.imwrite("cr.png", cr)

    # br threshold
    for k in range(0, img.shape[0]):
        for i in range(0, img.shape[1]):
            if br[k, i] > 100:
                br[k, i] = 0
            else:
                br[k, i] = 255

    cv2.imwrite("br.png", br)


def NDI(img):

    b, g, r = cv2.split(img)


    ndi = np.zeros(shape=(img.shape[0], img.shape[1]))

    for k in range(0, img.shape[0]):
        for i in range(0, img.shape[1]):
            top = int(g[k, i]) - int(r[k, i])
            bot = int(g[k, i]) + int(r[k, i])

            if bot != 0:
                val = top / bot

                if val > 0:
                    ndi[k, i] = 255
                elif val == 0:
                    ndi[k, i] = 0
            else:
                ndi[k, i] = 0



    fin = np.zeros(shape=(img.shape[0], img.shape[1]))

    cv2.imwrite("ndi.png", ndi)



def kMeansAlgo():
    print("do this too")


if __name__ == '__main__':
    image = openImage("./images/orange1.jpg")

    shadow_res = shadowReduce(image)
    varianceFilter(shadow_res)





