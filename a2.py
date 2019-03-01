#!/usr/bin/python3


import cv2
import numpy as np
np.set_printoptions(threshold=np.nan)
from PIL import Image, ImageCms, ImageEnhance
from skimage import color


def openImage(fname):
	return Image.open(fname).convert('RGB')



def shadowReduce(image):
	print("do this")

	# # create colour spaces
	# srgb_p = ImageCms.createProfile("sRGB")
	# lab_p  = ImageCms.createProfile("LAB")

	# # build colour space conversions
	# rgb2lab = ImageCms.buildTransformFromOpenProfiles(srgb_p, lab_p, "RGB", "LAB")
	# Lab = ImageCms.applyTransform(image, rgb2lab)

	# # cather the images in the LAB colour spaces
	# L, a, b = Lab.split()
	# L.save('L.png')
	# a.save('a.png')
	# b.save('b.png')


	# print(Lab)
	
	enhancer = ImageEnhance.Brightness(image)
	Lab = enhancer.enhance(1.3)


	# # combined = ','.join(fin_L, a, b)

	# lab2rgb = ImageCms.buildTransformFromOpenProfiles(lab_p, srgb_p, "LAB", "RGB")
	# Lab2 = ImageCms.applyTransform(Lab, lab2rgb)


	# initial = color.rgb2hsv(np.asarray(image))


	# initial[:, :, 2] += 10



	# final = color.hsv2rgb(initial)

	# img = Image.fromarray(final, 'RGB')

	# img.save('final.png')




	Lab.save('L_Change.png')





def kMeansAlgo():
	print("do this too")



if __name__ == '__main__':
	image = openImage("./images/orange1.jpg")

	shadowReduce(image)




