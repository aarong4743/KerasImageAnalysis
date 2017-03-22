import cv2
import numpy as np
import os
import shutil
import re
import random
import math

# This class contains all the helper methods that are not unique
# to any one class
class MyUtils:
    
  ###### Class Variables ####################################################
    # Constants for the different categories
    NO_EYES = "0_Eyes"
    ONE_EYE = "1_Eye"
    TWO_EYES = "2_Eyes"
    NOT_SURE = "Not_Sure"
    DEAD = "Dead"
    BAD_ANGLE = "Bad_Angle"
    RESULTS = "results.txt"

    # Converets the text to an int if it is an number
    @staticmethod
    def atoi(text):
        return int(text) if text.isdigit() else text

    # A method that can be passed into sort to allow files
    # with numbers in their names to be sorted as numbers
    # instead of characters. For eaxmple 1,2,10 instead of
    # 1,10,2.
    @staticmethod
    def natural_keys(text):
        return [MyUtils.atoi(c) for c in re.split('(\d+)', text) ]

    # Lists all non hidden files in the given directory
    @staticmethod
    def listdir_nohidden(path):
        lst = os.listdir(path)
        lst.sort(key=MyUtils.natural_keys)
        for f in lst:
            if not f.startswith('.') and f != MyUtils.RESULTS:
                yield f

    # Checks to see if the given path is already a directory
    # if it is then clean it. If it is not already a directory
    # then create it
    @staticmethod
    def clean_and_make_dir(destinationFolder):
        if (os.path.isdir(destinationFolder)):
            shutil.rmtree(destinationFolder)
        os.mkdir(destinationFolder)


    # Returns a list of the paths of all the images in that folder
    @staticmethod
    def images_in_folder(path):
        lst = os.listdir(path)
        lst.sort(key=MyUtils.natural_keys)
        for f in lst:
            if '.jpeg' in f and not f.startswith('.'):
                yield f

    # Counts the number of non hidden directories in the current dirc
    @staticmethod
    def count_folders(path):
        return len([name for name in os.listdir(path)
            if not name.startswith('.')])

    # Returns a list of trainning labels, a list of trainning images, a list of
    # test labels and a list of test images
    # The size of the test set is determined by test_size.
    # test_size should be a number between 0-100. 0 means no test set,
    #  100 means all test set, 50 means half and half.
    @staticmethod
    def get_all_labels_and_images(path, test_size):
        images = []
        labels = []
        folders = list(MyUtils.listdir_nohidden(path))
        for idx, folder in enumerate(folders):
            print 'Loading Images in folder ' + folder
            all_images = list(MyUtils.images_in_folder(path + '/' + folder))
            for img in all_images:
                encoding = [0] * len(folders)
                pixels = cv2.imread(path + '/' + folder + '/' + img,0)
                if pixels is None:
                    print 'Bad'
                    continue
                images.append(pixels.reshape(1, 100, 100))
                encoding[idx] = 1
                labels.append(encoding)

        # Shuffle the images
        combined = zip(labels, images)
        random.shuffle(combined)
        labels , images = zip(*combined)
        labels = np.array(list(labels))
        images = np.array(list(images))

        percent_test = test_size * 1.0 / 100
        split = int(math.ceil(len(labels) * percent_test))
        labels_test = labels[:split]
        labels = labels[split:]
        images_test = images[:split]
        images = images[split:]

        return labels, images, labels_test, images_test, folders

    #Finds the category with the highest confidence and the category
    # with the second highest. If the difference between the two
    # category does not meet the thresehold then it returns Not Sure
    @staticmethod
    def max_pred(labels, encoding):
        THRESHOLD = 0.5
        maxIdx = None
        second_place_val = None
        maxVal = None
        for idx, val in enumerate(labels):
            if maxIdx is None or val > maxVal:
                maxIdx = idx
                second_place_val = maxVal
                maxVal = val
            elif val <= maxVal and val > second_place_val:
                second_place_val = val

        if maxVal - second_place_val > THRESHOLD:
            return encoding[maxIdx]
        else:
            return MyUtils.NOT_SURE 

