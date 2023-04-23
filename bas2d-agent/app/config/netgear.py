import os


class NetgearConfig:
    ip_addr: str
    port: int
    timeout: int
    max_retries: int
    is_copy: bool
    is_compression: bool

    def __init__(self):
        self.ip_addr=os.getenv("SERVER_IP", "192.168.1.240")
        self.port=int(os.getenv("SERVER_PORT", "11118"))
        self.timeout=int(os.getenv("TIMEOUT", "10"))
        self.max_retries=int(os.getenv("MAX_RETRIES", "20"))
        self.is_copy=(os.getenv("IS_COPY", "True") == "True")
        self.is_compression=(os.getenv("IS_COMPRESSION", "False") == "True")

    @property
    def option(self):
        """option for netgear

        Returns:
            dict: netgear option property
        """
        return {
            "max_retries": self.max_retries,  # OK
            "request_timeout": self.timeout,  # OK
            "copy": self.is_copy,
            "jpeg_compression": self.is_compression,
        }

    @staticmethod
    def load():
        """load offset configuration"""
        return NetgearConfig()
