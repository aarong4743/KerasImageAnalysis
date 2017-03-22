import MyUtils_
import ImageCropper_
import Predictor_
import NeuralNetwork_
import Evaluator_
from MyUtils_ import MyUtils
from ImageCropper_ import ImageCropper
from Predictor_ import Predictor
from NeuralNetwork_ import NeuralNetwork
from Evaluator_ import Evaluator



# This class has throw away methods to run in the interpretor
class Main:
    @staticmethod
    def train_and_pred():
        print 'Loading Images Please Be Patient'
        labels, imgs, labels_test, imgs_test, encoding = \
                MyUtils.get_all_labels_and_images(
                        '/Users/patrickhayes/Desktop/Trainning_Sets/Base', 0)
        print (imgs.shape)
        print 'Done Loading Images'
        print ' '
        print 'Starting to train'
        model = NeuralNetwork("basic", len(encoding))
        history = model.train(imgs, labels, 5)
        print 'Done Training'
        print ' '
        print 'Starting to predict'
        Predictor.predict_all_well(
                '/Users/patrickhayes/Desktop/Test_Sets/Small'
                ,encoding, model)



