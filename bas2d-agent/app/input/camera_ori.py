import logging

from routine.port.input import InputPort
import cv2

from config import Config

logger = logging.getLogger(__name__)


class CameraAdapter(InputPort):
    def __init__(self, device: str = None):
        super().__init__()
        config = Config.load_camera_config()
        self.stream = cv2.VideoCapture(device or config.device, cv2.CAP_V4L2)
        if not self.stream.isOpened():
            logger.exception("fail to open camera")
            exit(-1)
        self._set_option(config)

    def _set_option(self, config):
        self.stream.set(cv2.CAP_PROP_BUFFERSIZE, config.buffer_size)
        self.stream.set(cv2.CAP_PROP_FRAME_WIDTH, config.width)
        self.stream.set(cv2.CAP_PROP_FRAME_HEIGHT, config.height)
        self.stream.set(cv2.CAP_PROP_FPS, config.fps)

    def read(self):
        """read
        """
        ret, frame = self.stream.read()
        if ret:
            return frame
        logger.warning("Fail to read camera")
        raise

    def release(self):
        """relase resource
        """
        self.stream.release()
        cv2.destroyAllWindows()
