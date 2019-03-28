import argparse
import logging
import time
import math
import cv2
import numpy as np

import pyrealsense2 as rs
from realsenseCustom import RealsenseCustom
import sys

pipeline = rs.pipeline()
config = rs.config()

if __name__ == '__main__':

    x = int(sys.argv[1])
    y = int(sys.argv[2])
    print("({}, {})".format(x, y))
    config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
    config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)
    pipeline.start(config)
    frames = pipeline.wait_for_frames()
    depth_frame = frames.get_depth_frame()
    depth_intrin = depth_frame.profile.as_video_stream_profile().intrinsics
    print(depth_intrin)
    rsCustom = RealsenseCustom(depth_intrin)

    try:
        while True:

            # Wait for a coherent pair of frames: depth and color
            frames = pipeline.wait_for_frames()
            depth_frame = frames.get_depth_frame()
            color_frame = frames.get_color_frame()

            depth_intrin = depth_frame.profile.as_video_stream_profile().intrinsics
            color_intrin = color_frame.profile.as_video_stream_profile().intrinsics
            
            angle = rsCustom.getAngleFromPoint(depth_frame, x, y)
            
            print(angle)

            if not depth_frame or not color_frame:
                continue

            # Convert images to numpy arrays
            depth_image = np.asanyarray(depth_frame.get_data())
            color_image = np.asanyarray(color_frame.get_data())
            cv2.circle(color_image, (x, y), 3, (0,255,0), thickness=3, lineType=8, shift=0)

 
            if cv2.waitKey(1) == 27:
                break
            # Apply colormap on depth image (image must be converted to 8-bit per pixel first)
            depth_colormap = cv2.applyColorMap(cv2.convertScaleAbs(depth_image, alpha=0.03), cv2.COLORMAP_JET)
            
            # Stack both images horizontally
            images = np.hstack((color_image, depth_colormap))

            # Show images
            cv2.namedWindow('Get Angle', cv2.WINDOW_AUTOSIZE)
            cv2.imshow('Get Angle', images)
            cv2.waitKey(1)
    finally:
        # Stop streaming
        pipeline.stop()
