import pyrealsense2.pyrealsense2 as rs
import bbot.box as Box
import numpy as np
import math

class Camera:
    def __init__(self):
        self.color_frame = False
        self.aligned_depth_frame = False

    def setup(self) -> None:
        # Create a pipeline
        self.pipeline = rs.pipeline()

        # Create a config and configure the pipeline to stream
        config = rs.config()

        # Get device product line for setting a supporting resolution
        pipeline_wrapper = rs.pipeline_wrapper(self.pipeline)
        config.enable_stream(rs.stream.depth, 1280, 720, rs.format.z16, 30)
        config.enable_stream(rs.stream.color, 1920, 1080, rs.format.bgr8, 30)

        # Start streaming
        profile = self.pipeline.start(config)

	    # Allow some frames for the auto-exposure controller to stablise
        for i in range(30):
            self.pipeline.wait_for_frames()

        # Create an align object
        # rs.align allows us to perform alignment of depth frames to others frames
        # The "align_to" is the stream type to which we plan to align depth frames.
        align_to = rs.stream.color
        self.align = rs.align(align_to)

    def take_photo(self) -> None:
        # Get frameset of color and depth
        frames = self.pipeline.wait_for_frames()

        # Align the depth frame to color frame
        aligned_frames = self.align.process(frames)

        # Get aligned frames
        self.aligned_depth_frame = aligned_frames.get_depth_frame()
        color_frame = aligned_frames.get_color_frame()

        # Validate that both frames are valid
        if not self.aligned_depth_frame or not color_frame:
            return

        self.color_intrin = color_frame.profile.as_video_stream_profile().intrinsics
        self.color_image = np.asanyarray(color_frame.get_data())

    def get_color_frame(self) -> np.ndarray:
        return self.color_image

    def get_depth_in_mm(self, box: Box) -> int:
        # convert m to mm
        x, y = box.get_center()
        depth = int(self.aligned_depth_frame.get_distance(x,y) * 1000)

        return depth

    def get_diameter_in_mm(self, box: Box) -> int:
        left_x, left_y = box.get_left_center()
        right_x, right_y = box.get_right_center()

        x, y = box.get_center()
        dist = self.aligned_depth_frame.get_distance(x,y)

        left_point = rs.rs2_deproject_pixel_to_point(self.color_intrin, [left_x, left_y], dist)
        right_point = rs.rs2_deproject_pixel_to_point(self.color_intrin, [right_x, right_y], dist)

        diameter = math.sqrt(
            math.pow(left_point[0] - right_point[0], 2) + math.pow(left_point[1] - right_point[1],2) + math.pow(
                left_point[2] - right_point[2], 2))

        # convert m to mm
        return int(diameter * 1000)
