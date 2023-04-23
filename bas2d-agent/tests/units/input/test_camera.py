import numpy as np
import pytest

from app.input.camera import CameraAdapter


@pytest.mark.skip('This test need to use default camera number 0')
def test_should_return_image_ndarray_when_camera_no_given():
    # given
    camera_adapter = CameraAdapter(0)

    # when
    result = camera_adapter.read_cam()

    # then
    assert type(result) is np.ndarray, 'Fail to read camera image'


def test_should_raise_when_camera_no_is_none():
    # given
    camera_adapter = CameraAdapter(0)

    # when
    data = camera_adapter.read()

    # then
    assert data is None, "data should be none"
