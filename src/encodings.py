from abc import ABCMeta, abstractmethod
from enum import Enum
from typing import List
from tensorflow import keras
from PIL import Image
from skimage.color import rgb2hsv
import numpy as np


class Metric(Enum):
    COLOR = 'color-encoding'
    CONTENT = 'encoding'


class Encoding(metaclass=ABCMeta):

    metric: Metric

    def __init__(self, metric: Metric):
        self.metric = metric

    def __str__(self):
        return f'Encoding for {self.metric.name} metric'

    @abstractmethod
    def compute_for_one(self, img: Image) -> List[float]:
        pass


class ContentEncoding(Encoding):

    def __init__(self):
        super().__init__(Metric('encoding'))
        self.model = keras.applications.vgg16.VGG16(include_top=False, weights='imagenet', input_tensor=None,
                                                    input_shape=(224, 224, 3), pooling="max", classes=1000)

    def compute_for_one(self, img: Image) -> List[float]:
        tensor = np.stack([np.asarray(img.resize([224, 224], Image.NEAREST))], axis=0)
        content_encoding = self.model.predict(tensor, batch_size=1, verbose=1)
        return content_encoding.tolist()


class ColorEncoding(Encoding):

    def __init__(self):
        super().__init__(Metric('color-encoding'))

    def compute_for_one(self, img: Image) -> List[float]:
        img_hsv = rgb2hsv(np.asarray(img))
        hue_hist, bin_edges = np.histogram(img_hsv[:, :, 0], bins=np.linspace(0, 1, 8 + 1), density=True)
        sat_hist, bin_edges = np.histogram(img_hsv[:, :, 1], bins=np.linspace(0, 1, 4 + 1), density=True)
        value_hist, bin_edges = np.histogram(img_hsv[:, :, 2], bins=np.linspace(0, 1, 4 + 1), density=True)
        color_enconding = np.hstack([hue_hist, sat_hist, value_hist])
        return list(color_enconding)


def create_encoding_dict():
    d = {
        'CONTENT': ContentEncoding(),
        'COLOR': ColorEncoding(),
    }
    return d






