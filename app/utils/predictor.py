import os
import numpy as np
from keras.models import load_model
from keras.preprocessing import image
import cv2


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

        # img = cv2.imread(image_path)
        #
        # minisize = (img.shape[1], img.shape[0])
        # miniframe = cv2.resize(img, minisize)
        #
        # faces = self.cascade.detectMultiScale(miniframe)
        #
        # for f in faces:
        #     x, y, w, h = [v for v in f]
        #     cv2.rectangle(img, (x, y), (x + w, y + h), (255, 255, 255))
        #
        #     sub_face = img[y:y + h, x:x + w]
        #     face_file_name = "faces/face_" + str(y) + ".jpg"
        #     cv2.imwrite(face_file_name, sub_face)
        # print(faces)

        image_to_predict = convert_image(image_path)

        result = self.model.predict(image_to_predict)
        print(f"LOG : PREDICT GLASSES RESULT : {result}")

        if result >= 0.5:
            return 'with glasses'
        else:
            return 'without glasses'


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
            return 'woman'
        else:
            return 'man'
