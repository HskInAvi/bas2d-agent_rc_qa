import logging

from routine.port.process import ProcessPort
import simplejpeg
import numpy as np

logger = logging.getLogger(__name__)


class EncodingProcess(ProcessPort):

    def process(self, input_data): # pylint: disable=R0201
        if EncodingProcess._is_valid_type(input_data):
            logger.error(f"input data should be numpy for processing but ({type(input_data)})")
            return input_data

        frame = EncodingProcess._convert_to_contiguous(input_data)
        return simplejpeg.encode_jpeg(
            frame,
            quality=50,
            colorspace="BGR",
            colorsubsampling="422",
            fastdct=True,
        )

    @classmethod
    def _is_valid_type(cls, input_data):
        return type(input_data) is not np.ndarray # pylint: disable=C0123

    @classmethod
    def _convert_to_contiguous(cls, input_data):
        if not input_data.flags["C_CONTIGUOUS"]:
            # check whether the incoming frame is contiguous
            return np.ascontiguousarray(input_data, dtype=input_data.dtype)
        return input_data
