from dotenv import load_dotenv

from config.netgear import NetgearConfig
from config.camera import CameraConfig
from config.redis import RedisConfig

load_dotenv(verbose=True)


class Config:
    @classmethod
    def load_camera_config(cls) -> CameraConfig:
        """load camera config
        Returns:
            CameraConfig: camera config
        """
        return CameraConfig.load()

    @classmethod
    def load_netgear_config(cls) -> NetgearConfig:
        """load netgear config
        Returns:
            NetgearConfig: netgear config
        """
        return NetgearConfig.load()

    @classmethod
    def load_redis_config(cls) -> RedisConfig:
        """load redis config
        Returns:
            RedisConfig: redis config
        """
        return RedisConfig.load()
