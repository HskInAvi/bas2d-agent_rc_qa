import logging
import datetime

from routine.port.output import OutputPort
from amq.queue import QueueOption
from amq.mq.rkv import Setter
from config import Config

logger = logging.getLogger(__name__)


class RedisAdapter(OutputPort):
    def __init__(self) -> None:
        super().__init__()
        self.amq_setter = Setter(QueueOption(**Config.load_redis_config()))

    def send(self, data):
        return self.amq_setter.set(data, datetime.timedelta(seconds=1))
