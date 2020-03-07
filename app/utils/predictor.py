import os
import numpy as np
from keras.models import load_model
from keras.preprocessing import image
import cv2
from PIL import ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = True


def convert_image(path):
    files = image.load_img(path, target_size=(64, 64))

    # converting to array
    test_image = image.img_to_array(files)

    # extend by 1 dimension to (64,64,3)
    converted_image = np.expand_dims(test_image, axis=0)
    return converted_image


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class GlassesPredictor(metaclass=Singleton):
    """Predictor for 'with glasses' and 'without glasses' classes"""

    def __init__(self):
        self.model = load_model("utils/models/20.loss.epo-156-v_acc-1.0000-v_loss-0.0000.h5")
        self.cascade = cv2.CascadeClassifier("utils/models/haarcascade_frontalface_default.xml")

    def predict(self, image_path):
        """Reads the image and returns response"""

        image_to_predict = convert_image(image_path)

        result = self.model.predict(image_to_predict)
        print(f"LOG : PREDICT GLASSES RESULT : {result}")

        if result >= 0.5:
            return 'With glasses'
        else:
            return 'Without glasses'


class GenderPredictor(metaclass=Singleton):
    """Predictor for 'man' and 'woman' classes"""

    def __init__(self):
        self.model = load_model("utils/models/20.loss.epo-177-v_acc-0.9654-v_loss-0.0939-genders.h5")
        self.cascade = cv2.CascadeClassifier("utils/models/haarcascade_frontalface_default.xml")

    def predict(self, image_path):
        """Reads the image and returns response"""
        image_to_predict = convert_image(image_path)

        result = self.model.predict(image_to_predict)
        print(f"LOG : PREDICT GENDER RESULT : {result}")

        if result >= 0.5:
            return 'Women'
        else:
            return 'Men'
