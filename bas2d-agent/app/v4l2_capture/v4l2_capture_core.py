import fcntl
import mmap
import select
import time
import os
import logging
import cv2
import numpy as np
from v4l2 import *

class V4l2Capture :
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
        self.set_logger(logging.DEBUG)

    def set_logger(self, level_param = logging.DEBUG) :
        self.logger.setLevel(level_param)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        self.log_handler.setFormatter(formatter)
        self.logger.addHandler(self.log_handler)

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
        fcntl.ioctl(self.__vd, VIDIOC_S_FMT, self.__fmt)

    def convert_current_colorspace_to_BGR(self, _p_frame_string, _cv_color_convert_param, _cur_channels) :
        np_frame_data = np.frombuffer(_p_frame_string, dtype=np.uint8).reshape(self.__height, self.__width, _cur_channels)
        mat_img = cv2.cvtColor(np_frame_data, _cv_color_convert_param)
        return mat_img

    def query_video_capability(self, _file_descriptor, _cp : v4l2_capability) :
        fcntl.ioctl(_file_descriptor, VIDIOC_QUERYCAP, _cp)

    def init_stream_param(self, _stream_param : v4l2_streamparm) :
        _stream_param.type = V4L2_BUF_TYPE_VIDEO_CAPTURE
        _stream_param.pram.capture.capability = V4L2_CAP_TIMEPERFRAME
        return _stream

    def init_mmap(self, _requestbuffers : v4l2_requestbuffers, _buffer_size = 1) :
        _requestbuffers.type = V4L2_BUF_TYPE_VIDEO_CAPTURE
        _requestbuffers.memory = V4L2_MEMORY_MMAP
        _requestbuffers.count = _buffer_size
        return _requestbuffers

    def get_buffer_size(self, _requestbuffers : v4l2_requestbuffers):
        if _requestbuffers.count != None :
            pass
        else :
            _requestbuffers.count = 1

        return _requestbuffers.count

    def init_buf(self, _buf : v4l2_buffer) :
        _buf.type = V4L2_BUF_TYPE_VIDEO_CAPTURE
        _buf.memory = V4L2_MEMORY_MMAP
        return _buf

    def try_ioctl_buf(self, _file_descriptor, _ioctl_request, _buffer) :
        trial_count = self.__max_trial_count
        res = 0
        while (trial_count > 0) :
            ret = fcntl.ioctl(_file_descriptor, _ioctl_request, _buffer)
            if ret is 0 :
                res = ret
            else :
                self.logger.debug(f'[core - try_ioctl_buf] {_ioctl_request} is failed. try again.')
                trial_count = trial_count - 1
                res = ret

        self.logger.debug(f'[core - try_ioctl_buf] {_ioctl_request} [full trial] Failed. ')
        return res

    def do_mmap(self, _file_descriptor,  _buf : v4l2_buffer, _frame_buffer : list, _buffer_size):
        self.logger.debug(f'width : {self.__fmt.fmt.pix.width}')
        self.logger.debug(f'height : {self.__fmt.fmt.pix.height}')
        self.logger.debug(f'pixel format : {self.__fmt.fmt.pix.pixelformat}')
        self.logger.debug(f'bytesperline : {self.__fmt.fmt.pix.bytesperline}')
        self.logger.debug(f'sizeimage : {self.__fmt.fmt.pix.sizeimage}')
        self.logger.debug(f'buffer type : {self.__param.type}')
        self.logger.debug(f'frame rate : {self.__param.parm.capture.timeperframe.denominator}')

        for iter_req in range(_buffer_size) :
            _buf.index = iter_req
            fcntl.ioctl(_file_descriptor, VIDIOC_QUERYBUF, _buf)

            _p_frame_string = mmap.mmap(_file_descriptor.fileno(), _buf.length, mmap.MAP_SHARED, mmap.PROT_READ | mmap.PROT_WRITE, offset=_buf.m.offset)
            _frame_buffer.append(_p_frame_string)

            ret_qbuf = self.try_ioctl_buf(_file_descriptor, VIDIOC_QBUF, _buf)
            if ret_qbuf == 0 :
                pass
            else :
                self.logger.debug(f'[core - do_mmap] Return value of VIDIOC_QBUF : {ret_qbuf}, ioctl error occured!')

            return ret_qbuf

    def set_stream_on(self, _file_descriptor ,_buf_type : v4l2_buf_type) :
        fcntl.ioctl(_file_descriptor, VIDIOC_STREAMON, _buf_type)

    def set_stream_off(self, _file_descriptor ,_buf_type : v4l2_buf_type) :
        fcntl.ioctl(_file_descriptor, VIDIOC_STREAMOFF, _buf_type)

    def request_dqueue(self, _file_descriptor, _buf : v4l2_buffer) :
        fcntl.ioctl(_file_descriptor, VIDIOC_DQBUF, _buf)
        return

    def convert_UYVY_to_BGR(self, _p_frame_string, _width, _height) :
        np_frame_data = np.frombuffer(_p_frame_string, dtype=np.uint8).reshape(_height, _width, 2)
        mat_img = cv2.cvtColor(np_frame_data, cv2.COLOR_YUV2BGR_UYVY)
        return mat_img

    def processing_frame(self, _mat_img) :
        pass

    def test_resize_frame(self, _mat_img, _width, _height) :
        return cv2.resize(_mat_img, dsize(_width, _height), interpolation=cv2.INTER_AREA)

    def requeue_buffer(self, _p_frame_string, _file_descriptor, _buf : v4l2_buffer) :
        _p_frame_string.seek(0)
        ret_qbuf = self.try_ioctl_buf(_file_descriptor, VIDIOC_QBUF, _buf)

        if ret_qbuf == 0 :
            pass
        else :
            self.logger.debug(f'[core - requeue_buffer] Return value of VIDIOC_QBUF : {ret_qbuf}, ioctl error occured!')

        return ret_qbuf

    def processing_frame(self, _mat_img) :
        pass

    def test_resize_frame(self, _mat_img, _width, _height) :
        return cv2.resize(_mat_img, dsize = (_width, _height), interpolation=cv2.INTER_AREA)

    def terminate_stream(self, _file_descriptor) :
        _file_descriptor.close()
