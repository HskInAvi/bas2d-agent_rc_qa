import os
import logging

from routine.event_loop import MainEventLoop

from input.camera import CameraAdapter
from output.redis import RedisAdapter
from process.encoding import EncodingProcess

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

os.environ['AGENT_NO'] = '0'

def run():
    """main function"""
    logger.info("Running bas2d agent: ")
    main_loop = MainEventLoop(
        CameraAdapter(),
        RedisAdapter(),
        EncodingProcess())
    main_loop.run_until_complete()

if __name__ == "__main__":
    run()
