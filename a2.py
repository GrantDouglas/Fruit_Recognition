#!/usr/bin/python3


import cv2
import numpy as np
np.set_printoptions(threshold=np.inf)
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

    ndi = NDI(img)

    print(img)



    r_var = ndimage.generic_filter(r, np.var, size=3)
    g_var = ndimage.generic_filter(g, np.var, size=3)
    b_var = ndimage.generic_filter(b, np.var, size=3)


    mean = np.zeros(shape=(img.shape[0], img.shape[1]))

    for k in range(0, img.shape[0]):
        for i in range(0, img.shape[1]):
            mean[k, i] = (int(r_var[k, i]) + int(g_var[k, i]) + int(b_var[k, i])) / 3


    # fin = (r_var + g_var + b_var) / 3

    cv2.imwrite("var4.png", mean)

    # gray_threshold
    for k in range(0, img.shape[0]):
        for i in range(0, img.shape[1]):
            if mean[k, i] <= 90:
                mean[k, i] = 0
            else:
                mean[k, i] = 255

    cv2.imwrite("mean.png", mean)


    # convert image to YCrcb color space
    ycrcb = cv2.cvtColor(img, 36)
    y, cr, cb = cv2.split(ycrcb)

    # cr threshold
    for k in range(0, img.shape[0]):
        for i in range(0, img.shape[1]):
            if cr[k, i] >= 140:
                cr[k, i] = 0
            else:
                cr[k, i] = 255

    cv2.imwrite("cr.png", cr)

    # cb threshold
    for k in range(0, img.shape[0]):
        for i in range(0, img.shape[1]):
            if cb[k, i] > 45 and cb[k, i] < 100:
                cb[k, i] = 255
            else:
                cb[k, i] = 0

    cv2.imwrite("cb.png", cb)


    # final = np.zeros(shape=(img.shape[0], img.shape[1]))

    # for k in range(0, img.shape[0]):
    #     for i in range(0, img.shape[1]):
    #         val = [ndi[k, i], mean[k, i], cr[k, i], cb[k, i]]
    #         if len(set(val)) == 1:
    #             pixel = 0
    #         else:
    #             pixel = 255

    #         final[k, i] = pixel


    fin_ndi = cv2.imread("ndi.png", cv2.IMREAD_GRAYSCALE)
    fin_mean = cv2.imread("mean.png", cv2.IMREAD_GRAYSCALE)
    fin_cr = cv2.imread("cr.png", cv2.IMREAD_GRAYSCALE)
    fin_cb = cv2.imread("cb.png", cv2.IMREAD_GRAYSCALE)


    fin_ndi[fin_ndi < 255] = 0
    fin_ndi[fin_ndi == 255] = 1

    fin_mean[fin_mean < 255] = 0
    fin_mean[fin_mean == 255] = 1

    fin_cr[fin_cr < 255] = 0
    fin_cr[fin_cr == 255] = 1

    fin_cb[fin_cb < 255] = 0
    fin_cb[fin_cb == 255] = 1

    res = np.zeros(shape=(img.shape[0], img.shape[1]))


   # gray_threshold
    for k in range(0, img.shape[0]):
        for i in range(0, img.shape[1]):


            if fin_ndi[k, i] == 0 and fin_mean[k, i] == 0 and fin_cr[k, i] == 0 and fin_cb[k, i] == 1:
               res[k, i] = 0
            else:
               res[k, i] = 255


   #res = np.logical_and.reduce([fin_ndi, fin_mean, fin_cr, fin_cb])
   #res.dtype = 'uint8'

   #print(res)

    cv2.imwrite("final.png", res)

    for k in range(0, img.shape[0]):
        for i in range(0, img.shape[1]):
            if res[k, i] == 0:
                b[k, i] = 0
                g[k, i] = 0
                r[k, i] = 0


    final = cv2.merge((b, g, r))

    cv2.imwrite("yay.png", final)




    # bin_ndi = cv2.threshold(fin_ndi, 255, 1, cv2.THRESH_BINARY)
    # bin_mean = cv2.threshold(fin_mean, 255, 1, cv2.THRESH_BINARY)
    # bin_cr = cv2.threshold(fin_cr, 255, 1, cv2.THRESH_BINARY)
    # bin_cb = cv2.threshold(fin_cb, 255, 1, cv2.THRESH_BINARY)


    # print(bin_ndi)

    # res1 = cv2.bitwise_and(bin_ndi, bin_mean)
    # res2 = cv2.bitwise_and(res1, bin_cr)
    # res3 = cv2.bitwise_and(res2, bin_cb)



    # final = cr + cb + mean + ndi

    # cv2.imwrite("final.png", res3)





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
                else:
                    ndi[k, i] = 0
            else:
                ndi[k, i] = 0


    cv2.imwrite("ndi.png", ndi)

    return ndi



def kMeansAlgo():
    print("do this too")


if __name__ == '__main__':
    image = openImage("./images/orange1.jpg")

    shadow_res = shadowReduce(image)
    varianceFilter(shadow_res)
