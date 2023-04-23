import os

from app.config.camera import CameraConfig


def test_should_return_camera_config_when_valid_input_given():
    # given
    DEVICE_PATH = "/dev/video0"
    os.environ["CAMERA_DEVICE"] = DEVICE_PATH
    os.environ["CAMERA_WIDTH"] = "1280"
    os.environ["CAMERA_HEIGHT"] = "960"
    os.environ["CAMERA_FPS"] = "60"
    os.environ["CAMERA_BUF_SIZE"] = "1"

    # when
    config = CameraConfig.load()

    # then
    assert config.buffer_size == 1, "buf size shoud be 1"
    assert config.device == DEVICE_PATH, "devcie shoud be /dev/video0"
    assert type(config.width) is int and config.width == 1280, "width should be 1280"
    assert type(config.height) is int  and config.height == 960, "height should be 960"
    assert type(config.fps) is int and config.fps == 60, "fps should be 60"
