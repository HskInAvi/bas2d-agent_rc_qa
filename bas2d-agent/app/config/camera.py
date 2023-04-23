import os


class CameraConfig:
    device: str
    width: int
    height: int
    fps: int
    buffer_size: int

    def __init__(self):
        self.device = os.getenv("CAMERA_DEVICE", "/dev/video0")
        self.width = int(os.getenv("CAMERA_WIDTH", "1280"))
        self.height = int(os.getenv("CAMERA_HEIGHT", "960"))
        self.fps = int(os.getenv("CAMERA_FPS", "60"))
        self.buffer_size = int(os.getenv("CAMERA_BUF_SIZE", "1"))

    @staticmethod
    def load():
        """load offset configuration"""
        return CameraConfig()
