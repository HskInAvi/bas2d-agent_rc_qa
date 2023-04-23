import logging

from routine.port.output import OutputPort
from zmq.sugar.constants import NOBLOCK

from output.netgear_impl.gears.netgear import NetGear
from config import Config

logger = logging.getLogger(__name__)


class NetgearAdapter(OutputPort):
    def __init__(self):
        super().__init__()
        self._sock = NetgearAdapter._setup(Config.load_netgear_config())

    @classmethod
    def _setup(cls, config):
        preset_option = {"flag": NOBLOCK }
        return NetGear(
            address=config.ip_addr,
            port=config.port,
            protocol="tcp",
            pattern=1,
            logging=False,
            **preset_option.update(config.option))

    def send(self, data):
        try:
            self._sock.send(data)
        except RuntimeError:
            logger.exception("fail to send message")
