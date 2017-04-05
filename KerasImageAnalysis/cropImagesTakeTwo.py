# This file takes an image of a worm and crops it so it only shows the head
# in a 100 x 100 pixel image. It uses image subtraction

import cv2
import numpy as np
import glob
import os
import shutil
import re

def atoi(text):
    return int(text) if text.isdigit() else text

def natural_keys(text):
    return [ atoi(c) for c in re.split('(\d+)', text) ]

def Listdir_nohidden(path):
    lst = os.listdir(path)
    lst.sort(key=natural_keys)
    for f in lst:
        if not f.startswith('.'):
            yield f

def CleanAndMakeDir(destinationFolder):
    if (os.path.isdir(destinationFolder)):
        shutil.rmtree(destinationFolder)
    os.mkdir(destinationFolder)


def CropImage(imageDiff, origImage, threshold_anchor, threshold_range, search_range, crop_size):
    height, width = imageDiff.shape
    min = 0
    maxcount = 0
    maxsum = 0
    min_i = 0
    min_j = 0
    search_range = search_range / 2
    crop_size = crop_size / 2

    for i in range(0,height):
        for j in range(0,width):
            if (imageDiff[i,j] < -threshold_anchor):
                count = 0
                sum = 0
                for k in range(i-search_range,i+search_range):
                    for l in range(j-search_range,j+search_range):
                        if ((k > 0) and (k < height) and (l > 0) and (l < width)):
                            if (imageDiff[k,l] < -threshold_range):
                                count = count + 1
                                sum = sum + (-1*imageDiff[k,l])

                if (sum > maxsum):
                    min_i = i
                    min_j = j
                    min = imageDiff[i,j]
                    maxsum = sum

    #keeps it from cropping off the side of the picture
    if ((min_i - crop_size)<0): min_i = crop_size
    if ((min_i + crop_size) >= height): min_i = height - crop_size - 1
    if ((min_j - crop_size) < 0): min_j = crop_size
    if ((min_j + crop_size) >= width): min_j = width - crop_size - 1

    imagecrop = origImage[min_i-crop_size:min_i+crop_size, min_j-crop_size:min_j+crop_size]

    return (maxsum, imagecrop)


def CropAllImages(destinationFolder, sourceFolder, threshold_anchor, threshold_range, search_range, crop_size):
    CleanAndMakeDir(destinationFolder)
    categories = Listdir_nohidden(sourceFolder)

    for category in categories:
        os.mkdir(destinationFolder + "/" + category)
        plates = Listdir_nohidden(sourceFolder + "/" + category)

        for plate in plates:
            os.mkdir(destinationFolder + "/" + category + "/" + plate)
            files = Listdir_nohidden(sourceFolder + "/" + category + "/" + plate)
            images = []

            for img in files:
                images.append(img)

            path = sourceFolder + "/" + category + "/" + plate + "/"
            for i in range(1,len(images)):
                print "reading image: " + path + images[i-1]
                image1 = cv2.imread(path + images[i-1],0)
                if (image1 is None):
                    error_image = destinationFolder + "/" + category + "/" + plate + "/" + str(i+1) + ".jpeg"
                    print error_image + "has a null type"
                    continue;
                image1 = image1.astype(np.int16)
                print "reading image: " + path + images[i]
                image2 = cv2.imread(path + images[i],0)
                if (image2 is None):
                    error_image = destinationFolder + "/" + category + "/" + plate + "/" + str(i+1) + ".jpeg"
                    print error_image + "has a null type"
                    continue;
                image2 = image2.astype(np.int16)
                imageDiff = image2 - image1

                (maxsum, imagecrop) = CropImage(imageDiff, image2, threshold_anchor, threshold_range, search_range, crop_size)
                writepath = destinationFolder + "/" + category + "/" + plate + "/" + str(i+1) + "_" + str(maxsum)+".jpeg"
                print "writing image: " + writepath
                cv2.imwrite(writepath, imagecrop)

# Crop all New Data Images
#CropAllImages("Anchor10_Range10_NewData_TakeTwo", "/Users/aarong4743/Pictures/SARA_EYE_ANALYSIS", 10, 10, 10, 100)
#CropAllImages("Anchor10_Range5_NewData", "/Users/aarong4743/Pictures/SARA_EYE_ANALYSIS", 10, 5, 10, 100)
#CropAllImages("Anchor10_Range7_NewData", "/Users/aarong4743/Pictures/SARA_EYE_ANALYSIS", 10, 7, 10, 100)
#CropAllImages("Anchor7_Range5_NewData", "/Users/aarong4743/Pictures/SARA_EYE_ANALYSIS", 7, 5, 10, 100)
#CropAllImages("Anchor7_Range7_NewData", "/Users/aarong4743/Pictures/SARA_EYE_ANALYSIS", 7, 7, 10, 100)
#CropAllImages("Anchor5_Range5_NewData", "/Users/aarong4743/Pictures/SARA_EYE_ANALYSIS", 5, 5, 10, 100)
#CropAllImages("Anchor5_Range7_NewData", "/Users/aarong4743/Pictures/SARA_EYE_ANALYSIS", 5, 7, 10, 100)
#CropAllImages("Anchor5_Range10_NewData", "/Users/aarong4743/Pictures/SARA_EYE_ANALYSIS", 5, 10, 10, 100)
#CropAllImages("Anchor7_Range10_NewData", "/Users/aarong4743/Pictures/SARA_EYE_ANALYSIS", 7, 10, 10, 100)

# Crop all Google Drive Images
CropAllImages("Anchor10_Range10_Official_TakeTwo", "/Users/aarong4743/Pictures/Official", 10, 10, 10, 100)
CropAllImages("Anchor10_Range10_nonmoving_worms_TakeTwo", "/Users/aarong4743/Pictures/nonmoving_worms", 10, 10, 10, 100)
#CropAllImages("Anchor10_Range5_GoogleDrive", "/Users/aarong4743/Pictures/TRAINING_SET_FOR_EYE_DETECTION", 10, 5, 10, 100)
#CropAllImages("Anchor10_Range7_GoogleDrive", "/Users/aarong4743/Pictures/TRAINING_SET_FOR_EYE_DETECTION", 10, 7, 10, 100)
#CropAllImages("Anchor7_Range5_GoogleDrive", "/Users/aarong4743/Pictures/TRAINING_SET_FOR_EYE_DETECTION", 7, 5, 10, 100)
#CropAllImages("Anchor7_Range7_GoogleDrive", "/Users/aarong4743/Pictures/TRAINING_SET_FOR_EYE_DETECTION", 7, 7, 10, 100)
#CropAllImages("Anchor5_Range5_GoogleDrive", "/Users/aarong4743/Pictures/TRAINING_SET_FOR_EYE_DETECTION", 5, 5, 10, 100)
#CropAllImages("Anchor5_Range7_GoogleDrive", "/Users/aarong4743/Pictures/TRAINING_SET_FOR_EYE_DETECTION", 5, 7, 10, 100)
#CropAllImages("Anchor5_Range10_GoogleDrive", "/Users/aarong4743/Pictures/TRAINING_SET_FOR_EYE_DETECTION", 5, 10, 10, 100)
CropAllImages("Anchor7_Range10_GoogleDrive", "/Users/aarong4743/Pictures/TRAINING_SET_FOR_EYE_DETECTION", 7, 10, 10, 100)