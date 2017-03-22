import cv2
import numpy as np
import h5py
from keras.models import Sequential, load_model
from keras.layers import Dense, Convolution2D, MaxPooling2D, Activation
from keras.layers import BatchNormalization
from keras.optimizers import SGD
from keras.layers import Flatten

### This class holds the logic for the nueral network. This is 
### where the nueral networks are created, trained, fine-tuned,
### and used for eye dection
class NeuralNetwork:

  ### Methods ##############################################################
    # Purpose - The constructor, compiles the specified type of nueral network
    #           requested
    # 
    # Takes - The type of nueralnetwork wanted
    #
    # Returns - an untrained nueral network
    def __init__(self, model_type, **op_paramsnum_categories):
        if model_type.lower() == "basic":
            self.model = NeuralNetwork.get_basic_model(
                                            op_params[num_categories])

        elif model_type.lower() == "model_a":
            self.model =  NeuralNetwork.get_model_a(
                                             op_params[num_categories])

        elif model_type.lower() == "model_b":
            self.model = NeuralNetwork.get_model_b(
                                            op_params[num_categories])
        elif model_type.lower() == "load":
            self.model = NeuralNetwork.load(op_params[file_path])

        else:
            self.model = NeuralNetwork.get_basic_model(
                                            op_params[num_categories])
            print ("Please specify a valid model")
            return


    # Purpose - compiles a very simple neural network, used just for testing
    #           uses keras framework 
    # Takes - nothing
    #
    # Returns - a simple nueral network
    @staticmethod
    def get_basic_model(num_categories):
        model = Sequential()

        # add 5 filters each 3 by 3 pixels in shape
        model.add(Convolution2D(5, 3, 3, border_mode='same',
            input_shape=(1, 100, 100), activation='relu'))

        # Batch normaliztion speeds up convergence and eliminates the
        # need for drop out
        model.add(BatchNormalization(epsilon=1e-05, mode=0, axis=1))

        # if you don't know what max pooling is look it up
        model.add(MaxPooling2D(pool_size=(2, 2)))

        model.add(Flatten())

        # Add a dense layer that has as many outputs as there are categories to
        # choose from
        model.add(Dense(num_categories, activation='softmax'))


        model.compile(loss='categorical_crossentropy'
                , optimizer=SGD(lr=0.001, momentum=0.9,decay=0.001)
                , metrics=['accuracy'])
        return model


    # Purpose - compiles a more complex neural network, model a means
    #           its the first attempt beyond the basic model
    #
    # Takes - nothing
    #
    # Returns - a simple nueral network
    @staticmethod
    def get_model_a(num_categories):
        model = Sequential()

        model.add(Convolution2D(25, 3, 3, border_mode='same',
            input_shape=(1, 100, 100), activation='relu'))
        model.add(BatchNormalization(epsilon=1e-05, mode=0, axis=1))
        model.add(MaxPooling2D(pool_size=(2,2)))

        ## Second layer is another convolutional layer
        model.add(Convolution2D(25, 3, 3,
            activation='relu', border_mode='same'))
        model.add(BatchNormalization(epsilon=1e-05, mode=0, axis=1))
        model.add(MaxPooling2D(pool_size=(2,2)))


       ## Third layer is another convolutional layer
        model.add(Convolution2D(25, 3, 3,
            activation='relu', border_mode='same'))
        model.add(BatchNormalization(epsilon=1e-05, mode=0, axis=1))
        model.add(MaxPooling2D(pool_size=(2,2)))

        ## Forth layer is another convolutional layer
        model.add(Convolution2D(25, 3, 3
            , activation='relu', border_mode='same'))
        model.add(BatchNormalization(epsilon=1e-05, mode=0, axis=1))
        model.add(MaxPooling2D(pool_size=(2,2)))

        ## Flatten out the convolutional layer so we can have
        # a fully connected layer
        model.add(Flatten())
        model.add(Dense(num_categories, activation='softmax'))
        model.summary()
        model.compile(loss='categorical_crossentropy'
                , optimizer=SGD(lr=0.001, momentum=0.9,decay=0.001)
                , metrics=['accuracy'])

        return model
    
    
    # Purpose - compiles a more complex neural network. More layers
    #
    # Takes - nothing
    #
    # Returns - a simple nueral network
    @staticmethod
    def get_model_b():
        model = Sequential()

        model.add(Convolution2D(25, 3, 3, border_mode='same',
            input_shape=(1, 100, 100), activation='relu'))
        model.add(BatchNormalization(epsilon=1e-05, mode=0, axis=1))
        model.add(MaxPooling2D(pool_size=(2,2)))

        ## Second layer is another convolutional layer
        model.add(Convolution2D(25, 3, 3,
            activation='relu', border_mode='same'))
        model.add(BatchNormalization(epsilon=1e-05, mode=0, axis=1))
        model.add(MaxPooling2D(pool_size=(2,2)))


        ## Third layer is another convolutional layer
        model.add(Convolution2D(25, 3, 3,
            activation='relu', border_mode='same'))
        model.add(BatchNormalization(epsilon=1e-05, mode=0, axis=1))
        model.add(MaxPooling2D(pool_size=(2,2)))

        ## Forth layer is another convolutional layer
        model.add(Convolution2D(25, 3, 3
            , activation='relu', border_mode='same'))
        model.add(BatchNormalization(epsilon=1e-05, mode=0, axis=1))
        model.add(MaxPooling2D(pool_size=(2,2)))
        
        ## Fifth layer is another convolutional layer
        model.add(Convolution2D(25, 3, 3
            , activation='relu', border_mode='same'))
        model.add(BatchNormalization(epsilon=1e-05, mode=0, axis=1))
        model.add(MaxPooling2D(pool_size=(2,2)))
        
        ## Six layer is another convolutional layer
        model.add(Convolution2D(25, 3, 3
            , activation='relu', border_mode='same'))
        model.add(BatchNormalization(epsilon=1e-05, mode=0, axis=1))
        model.add(MaxPooling2D(pool_size=(2,2)))

        ## Flatten out the convolutional layer so we can have
        # a fully connected layer
        model.add(Flatten())
        model.add(Dense(100, activation="tanh"))
        model.add(Dense(100, activation="tanh"))
        model.add(Dense(num_categories, activation='softmax'))
        model.summary()
        model.compile(loss='categorical_crossentropy'
                , optimizer=SGD(lr=0.0005, momentum=0.9,decay=0.001)
                , metrics=['accuracy'])

        return model

    # Purpose - trains model
    #
    # Takes - images: the images to train on
    #         labels: what category does each image belong too
    #         epochs: how many epochs should it train
    #
    # Returns - a history of its trainning
    def train(self, images, labels, epochs):
        history = self.model.fit(images, labels, batch_size=10, nb_epoch=epochs
                ,verbose=1, callbacks=[], shuffle=True, class_weight='auto'
                , sample_weight=None)
        return history


    # Purpose - given a set of images, it predicts the category of each image
    #
    # Takes - a set of images
    #
    # Returns - a list of labels
    def predict(self,images):
        return self.model.predict(images)

    # Purpose - saves a model into a file, so we can load it later
    #
    # Takes - the path of the file where it should be saved
    #
    # Returns - nothing, saves the model into the file
    def save(self, file_path):
        self.model.save(file_path)
        return

    # Purpose - load a model from a saved file
    #
    # Takes - the path of the file where the model is
    #         saved
    # Returns - model that was loaded from saved file
    @staticmethod
    def load(file_path):
        return load_model(file_path)










