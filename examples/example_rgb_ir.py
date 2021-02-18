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

def prepare_device():
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

    return pyK4A

def get_rgb_frame(pyK4A):
    color_image_handle = pyK4A.capture_get_color_image()

    if not color_image_handle:
        return color_image_handle

    color_image = pyK4A.image_convert_to_numpy(color_image_handle)
    pyK4A.image_release(color_image_handle)

    return color_image

def get_ir_frame(pyK4A):
    ir_image_handle = pyK4A.capture_get_ir_image()

    if not ir_image_handle:
        return ir_image_handle

    ir_image = pyK4A.image_convert_to_numpy(ir_image_handle)

    # Convert to 0-255 range and saturate over 4000 pixel value
    image_to_show = ir_image
    image_to_show[image_to_show > 4000] = 4000
    image_to_show = cv2.convertScaleAbs(image_to_show,
                                        alpha=0.4)  # alpha is fitted by visual comparison with Azure k4aviewer results

    pyK4A.image_release(ir_image_handle)
    return image_to_show

if __name__ == "__main__":

    pyK4A = prepare_device()

    cv2.namedWindow('IR Image',cv2.WINDOW_NORMAL)
    cv2.namedWindow('RGB Image',cv2.WINDOW_NORMAL)

    k = 0
    while True:
        # Get capture
        pyK4A.device_get_capture()

        color_image = get_rgb_frame(pyK4A)
        ir_image = get_ir_frame(pyK4A)

        # Check if the images have been read correctly
        if ir_image and color_image:
            # Show images
            cv2.imshow('IR Image', ir_image)
            cv2.imshow('RGB Image', color_image)

            k = cv2.waitKey(1)

        pyK4A.capture_release()
        if k == 27:  # Esc key to stop
            break

    pyK4A.device_stop_cameras()
    pyK4A.device_close()

