"""
Code to record RGB and IR frame. This will be used for calibrating depth and RGB camera.
Author: Bharat
"""

import sys
sys.path.insert(1, '../pyKinectAzure/')

import numpy as np
from pyKinectAzure import pyKinectAzure, _k4a
import cv2

# Path to the module
# TODO: Modify with the path containing the k4a.dll from the Azure Kinect SDK
modulePath = 'C:\\Program Files\\Azure Kinect SDK v1.4.1\\sdk\\windows-desktop\\amd64\\release\\bin\\k4a.dll'
# under x86_64 linux please use r'/usr/lib/x86_64-linux-gnu/libk4a.so'
# In Jetson please use r'/usr/lib/aarch64-linux-gnu/libk4a.so'

if __name__ == "__main__":

    # Initialize the library with the path containing the module
    pyK4A = pyKinectAzure(modulePath)

    # Open device
    pyK4A.device_open()

    # Modify camera configuration
    device_config = pyK4A.config
    device_config.color_resolution = _k4a.K4A_COLOR_RESOLUTION_1080P
    device_config.depth_mode = _k4a.K4A_DEPTH_MODE_WFOV_2X2BINNED
    print(device_config)

    # Start cameras using modified configuration
    pyK4A.device_start_cameras(device_config)

    cv2.namedWindow('IR Image',cv2.WINDOW_NORMAL)
    cv2.namedWindow('RGB Image',cv2.WINDOW_NORMAL)

    k = 0
    while True:
        # Get capture
        pyK4A.device_get_capture()

        # Get the color image from the capture
        color_image_handle = pyK4A.capture_get_color_image()

        # Get the color image from the capture
        ir_image_handle = pyK4A.capture_get_ir_image()

        # Check if the images have been read correctly
        if ir_image_handle and color_image_handle:
            # Read and convert the IR image data to numpy array:
            ir_image = pyK4A.image_convert_to_numpy(ir_image_handle)

            # Convert to 0-255 range and saturate over 4000 pixel value
            image_to_show = ir_image
            image_to_show[image_to_show > 4000] = 4000
            image_to_show = cv2.convertScaleAbs(image_to_show,
                                                alpha=0.4)  # alpha is fitted by visual comparison with Azure k4aviewer results

            # Read and convert the image data to numpy array:
            color_image = pyK4A.image_convert_to_numpy(color_image_handle)

            # Show images
            cv2.imshow('IR Image', image_to_show)
            cv2.imshow('RGB Image', color_image)

            k = cv2.waitKey(1)

            # Release the images
            pyK4A.image_release(color_image_handle)
            pyK4A.image_release(ir_image_handle)

        pyK4A.capture_release()
        if k == 27:  # Esc key to stop
            break

    pyK4A.device_stop_cameras()
    pyK4A.device_close()

