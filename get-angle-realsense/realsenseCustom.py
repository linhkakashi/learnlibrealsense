import math
import pyrealsense2 as rs

class RealsenseCustom:
    def __init__(self, depth_intrin):
        self.depth_intrin = depth_intrin

    def getAngleFromPoint(self, depth_frame, x, y):
        angle = 0
        depth = depth_frame.get_distance(x, y)
        if(depth != 0):
            depth_point = rs.rs2_deproject_pixel_to_point(self.depth_intrin, [x, y], depth)
            angle = math.degrees(math.atan2(depth_point[0], depth_point[2]))
        return angle