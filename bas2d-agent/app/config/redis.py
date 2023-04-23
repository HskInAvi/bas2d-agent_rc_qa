import os


class RedisConfig:
    def __init__(self):
        self.host = os.getenv("REDIS_IP", "192.168.1.240")
        self.port = int(os.getenv("REDIS_PORT", "30379"))
        self.database = os.getenv("REDIS_DB", "0")
        self.channel = RedisConfig._create_channel_name(os.getenv('AGENT_NO'))

    @classmethod
    def _create_channel_name(cls, agent_no: int):
        return f"bas:agent:{agent_no}"

    @staticmethod
    def load():
        """load offset configuration
        """
        return vars(RedisConfig())
