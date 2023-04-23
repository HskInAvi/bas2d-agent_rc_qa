import fcntl
import mmap
import select
import time
import os
import logging
import cv2
import numpy as np
from v4l2_capture.v4l2 import *

class V4l2CaptureCU135 :
    def __init__(self, _video_device) :
        self.__vd = open(_video_device, 'rb+', buffering=0)

        self.__cp = v4l2_capability()
        self.__fmt = v4l2_format()
        self.__param = v4l2_streamparm()
        self.__req = v4l2_requestbuffers()
        self.__buf = v4l2_buffer()
        self.__buf_type = v4l2_buf_type(V4L2_BUF_TYPE_VIDEO_CAPTURE)

        self.__width = None
        self.__height = None
        self.__frame_rate = 30
        self.__max_trial_count = 5

        self.logger = logging.getLogger()
        self.log_handler = logging.StreamHandler()

    def set_logger(self, level_param = logging.INFO) :
        self.logger.setLevel(level_param)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        self.log_handler.setFormatter(formatter)
        self.logger.addHandler(self.log_handler)

    def query_video_capability_CU135(self) :
        fcntl.ioctl(self.__vd, VIDIOC_QUERYCAP, self.__cp)

    def set_default_param_CU135(self) :
        self.__width = 1280
        self.__height = 960
        self.__frame_rate = 30

    def set_custom_frame_width(self, _val : int) :
        self.__width = _val

    def set_custom_frame_height(self, _val : int) :
        self.__height = _val

    def set_custom_frame_rate(self, _val : int) :
        self.__frame_rate = _val

    def get_current_device_format(self) :
        fcntl.ioctl(self.__vd, VIDIOC_G_FMT, self.__fmt)

    def set_current_device_default_format(self) :
        fcntl.ioctl(self.__vd, VIDIOC_G_FMT, self.__fmt)
        fcntl.ioctl(self.__vd, VIDIOC_S_FMT, self.__fmt)

    def set_custom_format(self, _width, _height, _format_type, _pixel_format) :
        self.__fmt.type = _format_type
        self.__fmt.fmt.pix.pixelformat = _pixel_format
        self.__fmt.fmt.pix.width = _width
        self.__fmt.fmt.pix.height = _height
        self.__fmt.fmt.pix.bytesperline = 2 * _width
        self.__fmt.fmt.pix.sizeimage = 2 * _width * _height
        fcntl.ioctl(self.__vd, VIDIOC_S_FMT, self.__fmt)

    def set_format_CU135(self, _width, _height) :
        self.__fmt.type = V4L2_BUF_TYPE_VIDEO_CAPTURE
        self.__fmt.fmt.pix.pixelformat = V4L2_PIX_FMT_UYVY
        self.set_custom_frame_width(_width)
        self.set_custom_frame_height(_height)

        self.__fmt.fmt.pix.width = self.__width
        self.__fmt.fmt.pix.height = self.__height

        fcntl.ioctl(self.__vd, VIDIOC_S_FMT, self.__fmt)

    def init_stream_param_CU135(self) :
        self.__param.type = V4L2_BUF_TYPE_VIDEO_CAPTURE
        self.__param.parm.capture.capability = V4L2_CAP_TIMEPERFRAME
        self.__param.parm.capture.timeperframe.numerator = 1
        self.__param.parm.capture.timeperframe.denominator = self.__frame_rate
        fcntl.ioctl(self.__vd, VIDIOC_S_PARM, self.__param)

    def init_mmap_CU135(self, _buffer_size = 1) :
        self.__req.type = V4L2_BUF_TYPE_VIDEO_CAPTURE
        self.__req.memory = V4L2_MEMORY_MMAP
        self.__req.count = _buffer_size
        fcntl.ioctl(self.__vd, VIDIOC_REQBUFS, self.__req)

    def get_buffer_size_CU135(self):
        if self.__req.count != None :
            pass
        else :
            self.__req.count = 1

        return self.__req.count

    def init_buf_CU135(self) :
        self.__buf.type = V4L2_BUF_TYPE_VIDEO_CAPTURE
        self.__buf.memory = V4L2_MEMORY_MMAP

    # 20220410 modified method to resolve VIDIOC_QBUF error issue
    def try_ioctl_buf_CU135(self, _ioctl_request, _buffer) :
        trial_count = self.__max_trial_count
        while (trial_count > 0) :
            ret = fcntl.ioctl(self.__vd, _ioctl_request, _buffer)
            if ret is 0 :
                return ret
            else :
                self.logger.info(f'[core - try_ioctl_buf] {_ioctl_request} is failed. try again.')
                trial_count = trial_count - 1

        self.logger.info(f'[core - try_ioctl_buf] {_ioctl_request} [full trial] Failed. ')
        os._exit(os.EX_OK)

    def do_mmap_CU135(self, _frame_buffer : list):
        self.logger.info(f'width : {self.__fmt.fmt.pix.width}')
        self.logger.info(f'height : {self.__fmt.fmt.pix.height}')
        self.logger.info(f'pixel format : {self.__fmt.fmt.pix.pixelformat}')
        self.logger.info(f'bytesperline : {self.__fmt.fmt.pix.bytesperline}')
        self.logger.info(f'sizeimage : {self.__fmt.fmt.pix.sizeimage}')
        self.logger.info(f'buffer type : {self.__param.type}')
        self.logger.info(f'frame rate : {self.__param.parm.capture.timeperframe.denominator}')

        for iter_req in range(self.__req.count) :
            self.__buf.index = iter_req
            fcntl.ioctl(self.__vd, VIDIOC_QUERYBUF, self.__buf)

            _p_frame_string = mmap.mmap(self.__vd.fileno(), self.__buf.length, mmap.MAP_SHARED, mmap.PROT_READ | mmap.PROT_WRITE, offset=self.__buf.m.offset)
            _frame_buffer.append(_p_frame_string)

            ret_qbuf = self.try_ioctl_buf_CU135(VIDIOC_QBUF, self.__buf)
            if ret_qbuf == 0 :
                pass
            else :
                self.logger.info(f'[core - do_mmap] Return value of VIDIOC_QBUF : {ret_qbuf}, ioctl error occured!')
            return ret_qbuf

    def set_stream_on_CU135(self) :
        fcntl.ioctl(self.__vd, VIDIOC_STREAMON, self.__buf_type)

    def set_stream_off_CU135(self) :
        fcntl.ioctl(self.__vd, VIDIOC_STREAMOFF, self.__buf_type)

    def request_dqueue_CU135(self) :
        fcntl.ioctl(self.__vd, VIDIOC_DQBUF, self.__buf)

    def convert_UYVY_to_BGR_CU135(self, _p_frame_string) :
        np_frame_data = np.frombuffer(_p_frame_string, dtype=np.uint8).reshape(self.__height, self.__width, 2)
        mat_img = cv2.cvtColor(np_frame_data, cv2.COLOR_YUV2BGR_UYVY)
        return mat_img

    def requeue_buffer_CU135(self, _p_frame_string) :
        _p_frame_string.seek(0)

        ret_qbuf = self.try_ioctl_buf_CU135(VIDIOC_QBUF, self.__buf)
        if ret_qbuf == 0 :
            pass
        else :
            self.logger.info(f'[core - requeue_buffer] Return value of VIDIOC_QBUF : {ret_qbuf}, ioctl error occured!')
        return ret_qbuf

    def terminate_stream_CU135(self) :
        self.__vd.close()

    def set_current_device_default_stream_param(self) :
        fcntl.ioctl(self.__vd, VIDIOC_G_PARM, self.__param)
        fcntl.ioctl(self.__vd, VIDIOC_S_PARM, self.__param)

    def get_buffer_index_CU135(self) :
        return self.__buf.index

    def terminate_stream(self, _file_descriptor) :
        _file_descriptor.close()
