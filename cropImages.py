# This file takes an image of a worm and crops it so it only shows the head
# in a 100 x 100 pixel image. It uses image subtraction

import cv2
import numpy as np
import glob
import os
import shutil

def Listdir_nohidden(path):
    for f in os.listdir(path):
        if not f.startswith('.'):
            yield f

def CleanAndMakeDir(destinationFolder):
    if (os.path.isdir(destinationFolder)):
        shutil.rmtree(destinationFolder)
    os.mkdir(destinationFolder)


def CropImage(imageDiff, origImage, threshold, search_range, crop_size):
    height, width = imageDiff.shape
    min = 0
    maxcount = 0
    min_i = 0
    min_j = 0
    search_range = search_range / 2
    crop_size = crop_size / 2

    for i in range(0,height):
        for j in range(0,width):
            if (imageDiff[i,j] < -threshold):
                count = 0
                sum = 0
            for k in range(i-search_range,i+search_range):
                for l in range(j-search_range,j+search_range):
                    if ((k > 0) and (k < height) and (l > 0) and (l < width)):
                        if (imageDiff[k,l] < -threshold):
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

    imagecrop = origImage[min_i-crop_size:min_i+crop_size, min_j-crop_size:min_j+crop_size]

    return imagecrop


def CropAllImages(destinationFolder, sourceFolder, threshold, search_range, crop_size):
    CleanAndMakeDir(destinationFolder)
    categories = Listdir_nohidden(sourceFolder)

    for category in categories:
        os.mkdir(destinationFolder + "/" + category)
        plates = listdir_nohidden(sourceFolder + "/" + category)

        for plate in plates:
            os.mkdir(destinationFolder + "/" + category + "/" + plate)
            files = listdir_nohidden(sourceFolder + "/" + category + "/" + plate)
            images = []

            for img in files:
                images.append(img)

            path = sourceFolder + "/" + category + "/" + plate + "/"
            for i in range(1,len(images)):
                image1 = cv2.imread(path + images[i-1],0)
                image1 = image1.astype(np.int16)
                image2 = cv2.imread(path + images[i],0)
                image2 = image2.astype(np.int16)
                imageDiff = image2 - image1

                imagecrop = CropImage(imageDiff, image2, threshold, search_range, crop_size)
                cv2.imwrite(destinationFolder
                        + "/" + category + "/" + plate + "/" + str(i+1) + ".jpeg", imagecrop)

CropAllImages("Cropped", "plates", 10, 10, 100)
