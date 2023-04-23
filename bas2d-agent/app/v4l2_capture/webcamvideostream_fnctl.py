import cv2
import time
from threading import Thread
from v4l2_capture.v4l2_capture_manager import V4l2CaptureMng

class WebcamVideoStream :
    def __init__(self, src, src_width, src_height, fps, buff_size = 1, name="WebcamVideoStream") :
        # initialize the video camera stream and read the first frame
        # from the stream
        self.stream = V4l2CaptureMng(src)
        self.stream.setup_webcamvideostream(src_width, src_height, fps, buff_size)
        self.frame = self.stream.frame_read()
        self.prevframe = self.frame
        # initialize the thread name
        self.name = name
        # initialize the variable used to indicate if the thread should
        # be stopped
        self.stopped = False

    def start(self) :
    # start the thread to read frames from the video stream
        t = Thread(target=self.update, name=self.name, args=())
        t.daemon = True
        t.start()
        return self

    def update(self) :
    # keep looping infinitely until the thread is stopped
        while True :
        # if the thread indicator variable is set, stop the thread
            if self.stopped :
                return
            # otherwise, read the nex frame from the stream
            self.frame = self.stream.frame_read()

    def read(self) :
        # return the frame most recently read
        return self.frame

    def stop(self) :
    # indicate that the thread should be stopped
        self.stopped = True
        self.stream.release_v4l2()
