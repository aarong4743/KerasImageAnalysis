import cv2
import numpy as np
import glob

images = []
for img in glob.glob("../../Pictures/Training set for eye detection/Adult worms/2 eyes/1/*.jpeg"):
  images.append(img)
#for a in range(1, len(images)):
#	print images[a]
for a in range(1,len(images)):
  str1 = "../../Pictures/Training set for eye detection/Adult worms/2 eyes/1/"
        a_str = str(a)
        str2 = ".jpeg"
        img1_toread = str1 + a_str + str2
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
            if (image3[i,j] < -10):
              #if (b == 7):
                                                #print "i is: " + str(i)
                                                #print "j is: " + str(j)
                                count = 0
                                sum = 0
                                for k in range(i-10,i+10):
                                  for l in range(j-10,j+10):
                                    if ((k > 0) and (k < 1024) and (l > 0) and (l < 1280)):
                                      if (image3[k,l] < -10):
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
        imagecrop = image2b[min_i-50:min_i+50, min_j-50:min_j+50]
        longname = img2_toread
        baseindex = longname.rindex("/") + 1;
        #print a + 1;
        #print longname;
        #print baseindex;
        cv2.imwrite("PlateOneNew/" + longname[baseindex:], imagecrop)
        #if a == 7:
        #	cv2.namedWindow('image',cv2.WINDOW_NORMAL)
        #	cv2.imshow('image',imagecrop)
        #	cv2.waitKey(0)
#for i in range(10, 20):
#	px = image3[i,0]
#	print px
