import os
import logging
import cv2
from v4l2_capture.v4l2_capture_core_cu135 import V4l2CaptureCU135

class V4l2CaptureMng :
    def __init__(self, _video_device) :
        self.__v4l2Cap = V4l2CaptureCU135(_video_device)
        self.__v4l2Cap.set_logger(logging.INFO)
        self.frame_buffer = []
        self.__current_frame = None

    def setup_webcamvideostream(self, _width, _height, _fps, _buf_size = 1) :
        self.__v4l2Cap.query_video_capability_CU135()
        self.__v4l2Cap.set_format_CU135(_width, _height)

        self.__v4l2Cap.set_custom_frame_rate(_fps)
        self.__v4l2Cap.init_stream_param_CU135()

        self.__v4l2Cap.init_mmap_CU135(_buf_size)
        self.__v4l2Cap.init_buf_CU135()

        ret = self.__v4l2Cap.do_mmap_CU135(self.frame_buffer)
        if ret is 0:
            self.__v4l2Cap.set_stream_on_CU135()
        else :
            print("[mng - setup] do_mmap was failed. can't start stream.")
            os._exit(os.EX_OK)

    def frame_read(self) :
        self.__v4l2Cap.request_dqueue_CU135()
        buf_index = self.__v4l2Cap.get_buffer_index_CU135()
        p_frame_string = self.frame_buffer[buf_index]
        cv_frame = self.__v4l2Cap.convert_UYVY_to_BGR_CU135(p_frame_string)
        self.__v4l2Cap.requeue_buffer_CU135(p_frame_string)
        return cv_frame

    def release_v4l2(self) :
        self.__v4l2Cap.terminate_stream_CU135()
