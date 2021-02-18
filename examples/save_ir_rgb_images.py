"""
Code to record RGB and IR frame. This will be used for calibrating depth and RGB camera.
Author: Bharat
"""

import sys
sys.path.insert(1, '../pyKinectAzure/')

import numpy as np
from pyKinectAzure import pyKinectAzure, _k4a
import cv2
import os
from os.path import join, split, exists
from example_rgb_ir import prepare_device, get_rgb_frame, get_ir_frame
import time

# Path to the module
# TODO: Modify with the path containing the k4a.dll from the Azure Kinect SDK
modulePath = 'C:\\Program Files\\Azure Kinect SDK v1.4.1\\sdk\\windows-desktop\\amd64\\release\\bin\\k4a.dll'
# under x86_64 linux please use r'/usr/lib/x86_64-linux-gnu/libk4a.so'
# In Jetson please use r'/usr/lib/aarch64-linux-gnu/libk4a.so'

if __name__ == "__main__":
    save_path = '../data'
    if not exists(save_path):
        os.makedirs(save_path)

    pyK4A = prepare_device()

    cv2.namedWindow('IR Image',cv2.WINDOW_NORMAL)
    cv2.namedWindow('RGB Image',cv2.WINDOW_NORMAL)

    k = 0
    while True:
        # Get capture
        pyK4A.device_get_capture()

        color_image, color_image_handle = get_rgb_frame(pyK4A)
        ir_image, ir_image_handle = get_ir_frame(pyK4A)

        # Check if the images have been read correctly
        if ir_image_handle and color_image_handle:
            # Show images
            cv2.imshow('IR Image', ir_image)
            cv2.imshow('RGB Image', color_image)
            k = 1
            # Save images
            name = str(round(time.time()))
            cv2.imwrite(join(save_path, name + '_ir.png'))
            cv2.imwrite(join(save_path, name + '_rgb.png'))

        pyK4A.capture_release()
        if k == 1:  # Esc key to stop
            break

    pyK4A.device_stop_cameras()
    pyK4A.device_close()