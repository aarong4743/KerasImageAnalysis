import cv2
import numpy as np
import glob

for r in range(0,3):
	images = []
	path = "../../Pictures/labeled_cropped/" + str(r) + "_Eyes/*.jpeg"
	writepath = "labeled_cropped_contrasted_only/" + str(r) + "_Eyes/"
	for img in glob.glob(path):
		images.append(img)

	for a in range(1,len(images)):

		image1 = cv2.imread(images[a],0)

		height, width = image1.shape
		min_im = image1.min()
		max_im = image1.max()

		image2 = np.zeros((height, width), np.uint8)

		#for i in range(0,height):
			#for j in range(0,width):
				#image2[i,j] = image1[i,j]

		for i in range(0,height):
			for j in range(0,width):
				temp = 255 * (image1[i,j] - min_im) / ((0.9 * max_im) - min_im)
				if (temp >= 255):
					image2[i,j] = 255
				else:
					image2[i,j] = temp
				print "image 1 is: " + str(image1[i,j])
				print "image 2 is: " + str(image2[i,j])
				print "temp is: " + str(temp)
		print "the min value is: " + str(min_im)
		print "the max value is: " + str(max_im)

		longname = images[a]
		baseindex = longname.rindex("/") + 1;

		cv2.imwrite(writepath + longname[baseindex:],image2)
#cv2.namedWindow('image',cv2.WINDOW_NORMAL)
#cv2.imshow('image',image2)
#cv2.waitKey(0)
#for i in range(10, 20):
#	px = image3[i,0]
#	print px