from pytest import fixture
import numpy as np
from PIL import Image


@fixture
def mock_image():
    image = Image.new("RGB", (1280, 960), (255, 255, 255))
    return np.array(image)
