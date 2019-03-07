#!/usr/bin/python3


import cv2
import numpy as np
np.set_printoptions(threshold=np.inf)
from scipy import ndimage
import os
from joblib import Parallel, delayed
import multiprocessing


def openImage(fname):
    return cv2.imread(fname)

def varianceFilter(fname):

    print(fname)

    img = cv2.imread("images/" + fname, 1)

    b, g, r = cv2.split(img)

    ndi = NDI(img)

    # r_var = ndimage.generic_filter(r, np.var, size=3)
    # g_var = ndimage.generic_filter(g, np.var, size=3)
    # b_var = ndimage.generic_filter(b, np.var, size=3)

    # mean = np.zeros(shape=(img.shape[0], img.shape[1]))

    # mean[(r_var + g_var + b_var) > 270] = 255

    # gray_threshold
    # for k in range(0, img.shape[0]):
    #     for i in range(0, img.shape[1]):
    #         mean_val = int(r_var[k, i]) + int(g_var[k, i]) + int(b_var[k, i])
    #         if mean_val <= 270:
    #             mean[k, i] = 0
    #         else:
    #             mean[k, i] = 255


    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)


    # test, mean = cv2.threshold(imgGray, 89, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)

    mean = cv2.adaptiveThreshold(imgGray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 3, -5)


    edges = cv2.Canny(imgGray, 100, 200)

    cv2.imwrite("edges.jpg", edges)


    # convert image to YCrcb color space
    ycrcb = cv2.cvtColor(img, 36)
    y, cr, cb = cv2.split(ycrcb)


    cr[cr >= 140] = 254
    cr[cr < 140] = 1

    cr[cr == 1] = 255
    cr[cr == 254] = 0

    cb[(cb > 120) | (cb < 30)] = 255
    cb[(cb >= 30) & (cb <= 120)] = 0


    # mask = np.full((img.shape[0], img.shape[1]), 255)


    # mask[(ndi == 0) & (mean == 0) & (cr == 0) & (cb == 255)] = 0
    b[(ndi == 0) & (mean == 0) & (cr == 0) & (cb == 255)] = 0
    g[(ndi == 0) & (mean == 0) & (cr == 0) & (cb == 255)] = 0
    r[(ndi == 0) & (mean == 0) & (cr == 0) & (cb == 255)] = 0

    print(ndi, mean)

    mask = ndi + mean + cr + cb



   # gray_threshold
    # for k in range(0, img.shape[0]):
    #     for i in range(0, img.shape[1]):

    #         if ndi[k, i] == 0 and mean[k, i] == 0 and cr[k, i] == 0 and cb[k, i] == 255:
    #             mask[k, i] = 0
    #             b[k, i] = 0
    #             g[k, i] = 0
    #             r[k, i] = 0





    if not os.path.exists('results'):
        os.makedirs('results')

    if not os.path.exists('masks'):
        os.makedirs('masks')

    cv2.imwrite("masks/" + os.path.splitext(fname)[0] + "_mask.jpg", mask)


    final = cv2.merge((b, g, r))

    cv2.imwrite("results/" + os.path.splitext(fname)[0] + "_fix.jpg", final)



    ## Print all the intermidatrys
    #if not os.path.exists('intermediaries'):
    #    os.makedirs('intermediaries')

    cv2.imwrite("intermediaries/" + os.path.splitext(fname)[0] + "_NDI.jpg", ndi)
    cv2.imwrite("intermediaries/" + os.path.splitext(fname)[0] + "_mean.jpg", mean)
    cv2.imwrite("intermediaries/" + os.path.splitext(fname)[0] + "_cr.jpg", cr)
    cv2.imwrite("intermediaries/" + os.path.splitext(fname)[0] + "_cb.jpg", cb)
    cv2.imwrite("intermediaries/" + os.path.splitext(fname)[0] + "_mask.jpg", mask)
    cv2.imwrite("intermediaries/" + os.path.splitext(fname)[0] + "_final.jpg", final)



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

    return ndi


if __name__ == '__main__':

    imageList = os.listdir("./images/")
    cpu_count = multiprocessing.cpu_count()
    res = Parallel(n_jobs=cpu_count)(delayed(varianceFilter)(k) for k in imageList)


    #varianceFilter("citrus4.jpg")
