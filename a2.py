#!/usr/local/bin/python


import cv2
import numpy as np
np.set_printoptions(threshold=np.inf)
from PIL import Image, ImageCms, ImageEnhance
from skimage import color
from scipy import ndimage
import matplotlib.pyplot as plt
import os


def openImage(fname):
    return cv2.imread(fname)


<<<<<<< Updated upstream
def varianceFilter(img):
=======

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



def varianceFilter(img, fname):

>>>>>>> Stashed changes


    b, g, r = cv2.split(img)

    ndi = NDI(img)

    r_var = ndimage.generic_filter(r, np.var, size=3)
    g_var = ndimage.generic_filter(g, np.var, size=3)
    b_var = ndimage.generic_filter(b, np.var, size=3)

    mean = np.zeros(shape=(img.shape[0], img.shape[1]))

    # gray_threshold
    for k in range(0, img.shape[0]):
        for i in range(0, img.shape[1]):
            mean_val = int(r_var[k, i]) + int(g_var[k, i]) + int(b_var[k, i])
            if mean_val <= 270:
                mean[k, i] = 0
            else:
                mean[k, i] = 255


    # convert image to YCrcb color space
    ycrcb = cv2.cvtColor(img, 36)
    y, cr, cb = cv2.split(ycrcb)


    cr[cr >= 140] = 254
    cr[cr < 140] = 1

    cr[cr == 1] = 255
    cr[cr == 254] = 0



    cb[(cb > 120) | (cb < 30)] = 0
    cb[(cb >= 30) & (cb <= 120)] = 255


   # gray_threshold
    for k in range(0, img.shape[0]):
        for i in range(0, img.shape[1]):

            if ndi[k, i] == 0 and mean[k, i] == 0 and cr[k, i] == 0 and cb[k, i] == 255:
               b[k, i] = 0
               g[k, i] = 0
               r[k, i] = 0


    if not os.path.exists('results'):
        os.makedirs('results')


    final = cv2.merge((b, g, r))

    cv2.imwrite("results/" + os.path.splitext(fname)[0] + "_fix.png", final)




def NDI(img):

    b, g, r = cv2.split(img)

    ndi = np.zeros(shape=(img.shape[0], img.shape[1]))

    for k in range(0, img.shape[0]):
        for i in range(0, img.shape[1]):
            top = int(g[k, i]) - int(r[k, i])
            bot = int(g[k, i]) + int(r[k, i])

            if bot != 0:
                val = float(top) / float(bot)

                if val > 0:
                    ndi[k, i] = 255


    # cv2.imwrite("ndi.png", ndi)

    return ndi


if __name__ == '__main__':

    imageList = os.listdir("./images/")

    for k in imageList:

        image = cv2.imread("images/" + k, 1)

        # shadow_res = shadowReduce(image)
        varianceFilter(image, k)


