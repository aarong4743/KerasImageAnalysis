import cv2
import random
import os
import math
import numpy as np
import shutil
import re

import MyUtils_
from MyUtils_ import MyUtils

### This class has all the methods involved with cropping an image
### We crop images to make reduce the dimensionality and keep all 
### inputs to the neural network uniform
class ImageCropper:

  ### Class Variables #######################################################
    # minimum pixel difference to be considered movement
    threshold_anchor = 10
    # minimum pixel differnce to be considered movement for neighbot pixels
    threshold_range = 10
    # how close does a pixel need to be to be considered a neighbor
    search_range = 10
    # The final cropped image size. The cropped images will always be square
    crop_size = 100
  ### End Class Variables ###################################################

  ### Methods ###############################################################
    # Purpose - crops the images for multiple wells (a well is the video for
    #           one worm). Also makes a copy of the image for every rotation
    #           (90,180,270)
    #
    # Takes - destinationFolder: Where do you want the new cropped images
    #         sourceFolder: Where are the images you want to crop
    #
    # Returns - Nothing, the pictures are in the destination folder
    @staticmethod
    def crop_all_images(destinationFolder, sourceFolder):
        MyUtils.clean_and_make_dir(destinationFolder)
    	categories = MyUtils.listdir_nohidden(sourceFolder)

        #The ighest level directory will have a folder for each category
        # (0_Eyes, 1_Eye, 2_Eyes, etc.)
        for category in categories:
            os.mkdir(destinationFolder + "/" + category)
            wells = MyUtils.listdir_nohidden(sourceFolder + "/" + category)

            # Inside each category will be a bunch of folders were each folder
            # is a singel well
            for well in wells:
                os.mkdir(destinationFolder + "/" + category + "/" + well)
                files = MyUtils.listdir_nohidden(sourceFolder + "/" + category
                        + "/" + well)
                images = []
                
                # Each well will have around 50 frames (individual images)
                for img in files:
                    images.append(img)

                # Read in the image. Do the subtraction. Find the head, and
                # crop
                path = sourceFolder + "/" + category + "/" + well + "/"
                for i in range(1,len(images)):
                    image1 = cv2.imread(path + images[i-1],0)
                    if image1 is None:
                        print ("Image " + str(i) + " of well " 
                                + str(well) + " could not be opened")
                        print os.path.exists(path + images[i-1])
                        continue
                    image1 = image1.astype(np.int16)
                    image2 = cv2.imread(path + images[i],0)
                    if image2 is None:
                        print ("Image " + str(i) + " of well " 
                                + str(well) + " could not be opened")
                        continue
                    image2 = image2.astype(np.int16)
                    imageDiff = image2 - image1

                    #Crop the image
                    imagecrop = ImageCropper.crop_image(imageDiff, image2)

                    # Find the center so we can rotate around it
                    (h,w) = imagecrop.shape[:2]
                    center = (w / 2, h / 2)

                    # Compute the rotation matrix for each rotation
                    M_90 = cv2.getRotationMatrix2D(center, 90, 1.0)
                    M_180 =  cv2.getRotationMatrix2D(center, 180, 1.0)
                    M_270 =  cv2.getRotationMatrix2D(center, 270, 1.0)

                    # Create the rotated images
                    rotated_90 = cv2.warpAffine(imagecrop, M_90, (h, w))
                    rotated_180 =  cv2.warpAffine(imagecrop, M_180, (h, w))
                    rotated_270 =  cv2.warpAffine(imagecrop, M_270, (h, w))

                    # Write the images
                    cv2.imwrite(destinationFolder
                            + "/" + category + "/" + well + "/" + images[i]
                            , imagecrop)
                    cv2.imwrite(destinationFolder
                            + "/" + category + "/" + well + "/"
                            + "90_" + images[i]
                            , rotated_90)
                    cv2.imwrite(destinationFolder
                            + "/" + category + "/" + well + "/"
                            + "180_" + images[i]
                            , rotated_180)
                    cv2.imwrite(destinationFolder
                            + "/" + category + "/" + well + "/"
                            + "270_" + images[i]
                            , rotated_270)






    # Purpose - uses image subtration to crop the image to focus on the head
    #           of the worm. Works for grayscale images.Works reasonably well.
    #           Has trouble when the worm moves laterally, or if the lighting
    #           changes dramatically between frames. Completly fails if the
    #           worm is not moving.
    #
    # Takes - imageDiff: The difference between two frames.
    #         origImage: One of the frames from the image subtraction, either
    #                    one works.
    #
    # Returns - imagecrop: Hopefully a cropped image of the worm's head
    @staticmethod
    def crop_image(imageDiff, origImage):
        height, width = imageDiff.shape
        min = 0
        maxcount = 0
        min_i = 0
        min_j = 0
        search_range = ImageCropper.search_range / 2
        crop_size = ImageCropper.crop_size / 2
    
        # Traverse all the pixels in the subtracted image
        # Look for a pixel that is less thean the threshold. 
        # Once it finds a pixel that is less then the threshold it looks
        # around and counts how many pixels in the nearby area are also 
        # less than the thereshold. Keep track of pixel who has the most
        # nearby neighbors who are less then the threshold. 
        for i in range(0,height):
            for j in range(0,width):
                if (imageDiff[i,j] < -ImageCropper.threshold_anchor):
                    count = 0
                    sum = 0
                    for k in range(i-search_range,i+search_range):
                        for l in range(j-search_range,j+search_range):
                            if ((k > 0) and (k < height)
                                        and (l > 0) and (l < width)):
                                if (imageDiff[k,l]
                                        < -ImageCropper.threshold_range):
                                    count = count + 1
                                    sum = sum + (-1*imageDiff[k,l])
    
                    if (count > maxcount):
                        min_i = i
                        min_j = j
                        min = imageDiff[i,j]
                        maxcount = count
    
        #keeps it from cropping off the side of the picture
        if ((min_i - crop_size)<0): min_i = crop_size
        if ((min_i + crop_size) >= height): min_i = height - crop_size - 1
        if ((min_j - crop_size) < 0): min_j = crop_size
        if ((min_j + crop_size) >= width): min_j = width - crop_size - 1
        
        # Crop the original image around the pixel with the max number of
        # neighbors below the threshold 
        imagecrop = origImage[min_i-crop_size:min_i+crop_size
                              ,min_j-crop_size:min_j+crop_size]
    
        return imagecrop

   ### End Methods ##########################################################

### End Class ImageCropper ####################################################
