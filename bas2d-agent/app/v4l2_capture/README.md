# v4l2_capture
 This module performs the v4l2 driver control for camera I/O control at a lower level. For module development, videoio module of opencv was benchmarked and developed based on the ioctl method that can utilize the device driver as a medium to utilize the v4l2 driver. In particular, it was developed to deal with errors that occur when VIDIOC_QBUF and DQBUF requests fail. This module consists of 4 files, and the details of each are as follows.
 
 1. v4l2_capture_core.py
     - Basic ioctl-based class for requesting and acquiring camera frames
 
 2. v4l2_capture_core_cu135.py
     - A refactored core class optimized for the use of a specific camera model installed in a hanana(See3CAM CU135) (This module was written so that it can be applied directly to the HiBAS agent together with the "v4l2_capture_manager.py" module.)
     
 3. v4l2_capture_manager.py
     - A manager class to reduce interface dependency to core module. It has a form similar to opencv's videocapture.

 4. webcamvideostream_fnctl.py
     - Example module applying "v4l2_capture_core_cu135.py" and "v4l2_capture_manager.py" to the existing webcamvideostream module

# Example
python3 example.py

time.sleep(0.02) in the while loop is set to avoid overload of reading speed of frame.

If any function that occupies computational time in while loop is added, time.sleep can be terminated.

# Requirement
 NO REQUIREMENTS(v4l2 library was required, added file into the repository)
