import cv2
import numpy as np
import glob
import os
import shutil

def listdir_nohidden(path):
    for f in os.listdir(path):
        if not f.startswith('.'):
            yield f

#def listdir_nohidden_filesonly(path):
#    for f in os.listdir(path):
 #   	print f
  #      if not f.startswith('.'):
   #     	if os.path.isfile(f):
    #    		yield f

shutil.rmtree("SARA_EYE_ANALYSIS_CROPPED")
os.mkdir("SARA_EYE_ANALYSIS_CROPPED")

dirs = listdir_nohidden("../../Pictures/SARA_EYE_ANALYSIS")
for dir_one in dirs:
	os.mkdir("SARA_EYE_ANALYSIS_CROPPED/" + dir_one)
	dirname = "../../Pictures/SARA_EYE_ANALYSIS/" + dir_one
	dirs_two = listdir_nohidden(dirname)
	for dir_two in dirs_two:
		os.mkdir("SARA_EYE_ANALYSIS_CROPPED/" + dir_one + "/" + dir_two)
		dirname_two = dirname + "/" + dir_two
		files = listdir_nohidden(dirname_two)
		images = []
		for img in files:
			#print img
			images.append(img)
		#for a in range(1, len(images)):
		#	print images[a]
		print len(images)
		for a in range(1,len(images)):
			str1 = dirname_two + "/"
			a_str = str(a)
			str2 = ".jpeg"
			img1_toread = str1 + a_str + str2
			#print img1_toread
			b = a + 1;
			b_str = str(b)
			img2_toread = str1 + b_str + str2
			image1 = cv2.imread(img1_toread,0)
			image1 = image1.astype(np.int16)
			image2 = cv2.imread(img2_toread,0)
			image2 = image2.astype(np.int16)
			image3 = image2 - image1
			image2b = cv2.imread(img2_toread)
			#print img1_toread
			#print img2_toread
		#print type(image3)
		#print image2[55,56]
		#print image2b[55,56]
			height, width = image3.shape
		#print height
		#print width
		#print channels
			min = 0;
			maxcount = 0;
			min_i = 0;
			min_j = 0;

			for i in range(0,height):
				for j in range(0,width):
					if (image3[i,j] < -5):
							#if (b == 7):
								#print "i is: " + str(i)
								#print "j is: " + str(j)
						count = 0
						sum = 0
						for k in range(i-10,i+10):
							for l in range(j-10,j+10):
								if ((k > 0) and (k < 1024) and (l > 0) and (l < 1280)):
									if (image3[k,l] < -5):
										count = count + 1
										sum = sum + (-1*image3[k,l])
										#print "k is: " + str(k)
										#print "l is: " + str(l)
										#print "value is: " + str(image3[k,l])
						if (b == 30):
							print "i is: " + str(i)
							print "j is: " + str(j)
							print "count is: " + str(count)
							print "average is: " + str(sum/400)
						if (count > maxcount):
							min_i = i
							min_j = j
							min = image3[i,j]
							maxcount = count
			#print min_i
			#print min_j
		#print min
		#print image1[55,56]
		#print image2[55,56]

			#for d in range(min_i - 50, min_i + 50):
			#	for e in range(min_j - 50, min_j + 50):
			#		image2b[d,e][0] = 255
			if ((min_i - 50) <= 0):
				min_i = 51
			if ((min_i + 50) >= 1024):
				min_i = 973
			if ((min_j - 50) < 0):
				min_j = 51
			if ((min_j + 50) >= 1280):
				min_j = 1229
			imagecrop = image2b[min_i-50:min_i+50, min_j-50:min_j+50]
			longname = img2_toread
			baseindex = longname.index("/") + 1;
			longname = longname[baseindex:]
			baseindex = longname.index("/") + 1;
			longname = longname[baseindex:]
			baseindex = longname.index("/") + 1;
			longname = longname[baseindex:]
			baseindex = longname.index("/") + 1;
			print longname[baseindex:]
			#print a + 1;
			#print longname;
			#print baseindex;
			cv2.imwrite("SARA_EYE_ANALYSIS_CROPPED/" + longname[baseindex:], imagecrop)
			#if a == 7:
			#	cv2.namedWindow('image',cv2.WINDOW_NORMAL)
			#	cv2.imshow('image',imagecrop)
			#	cv2.waitKey(0)
		#for i in range(10, 20):
		#	px = image3[i,0]
		#	print px