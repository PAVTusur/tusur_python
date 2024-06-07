from ..image_processing import mark_plot
from PIL import Image
import numpy as np


def test_mark_add():
    test_array = np.zeros((2000, 2000, 3)).astype(np.uint8)
    image = Image.fromarray(test_array)
    mark_plot(image, 1, 1, 1)
