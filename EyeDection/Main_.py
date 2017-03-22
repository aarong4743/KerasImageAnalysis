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
    def train_and_pred(trainning_set, test_set, **op_params):
        print 'Loading Images Please Be Patient'
        labels, imgs, labels_test, imgs_test, encoding = \
                MyUtils.get_all_labels_and_images(
                        '/Users/patrickhayes/Desktop/Trainning_Sets/'
                        + trainning_set, 0)
        print (imgs.shape)
        print 'Done Loading Images'
        print ' '
        print 'Starting to train'
        model = NeuralNetwork("model_a", num_categories=len(encoding))
        history = model.train(imgs, labels, 20)
        print 'Done Training'
        print ' '
        print 'Starting to predict'
        if (Predictor.CONTRAST in op_params
                and op_params[Predictor.CONTRAST] == True):
            Predictor.predict_all_well(
                '/Users/patrickhayes/Desktop/Test_Sets/' + test_set
                ,encoding, model, Contrast=True)
        else:
             Predictor.predict_all_well(
                '/Users/patrickhayes/Desktop/Test_Sets/' + test_set
                ,encoding, model)
        



