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
        config.enable_stream(rs.stream.depth, 1280, 720, rs.format.z16, 30)
        config.enable_stream(rs.stream.color, 1920, 1080, rs.format.bgr8, 30)

        # Start streaming
        self.pipeline.start(config)

	    # Allow some frames for the auto-exposure controller to stablise
        for i in range(30):
            self.pipeline.wait_for_frames()

        # Create an align object
        # rs.align allows us to perform alignment of depth frames to others frames
        # The "align_to" is the stream type to which we plan to align depth frames.
        align_to = rs.stream.color
        self.align = rs.align(align_to)

    def take_photo(self) -> None:
        # Get frames of color and depth
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

        return int(self.aligned_depth_frame.get_distance(x,y) * 1000)

    def get_diameter_in_mm(self, box: Box) -> int:
        # Get xy for max size
        x_1, y_1, x_2, y_2 = box.get_max_size()

        # Calculate distance at center
        x_center, y_center = box.get_center()
        dist = self.aligned_depth_frame.get_distance(x_center, y_center)

        # Convert 2D to 3D point
        # Take into account: depth and intrinsics of the hardware
        point_1 = rs.rs2_deproject_pixel_to_point(self.color_intrin, [x_1, y_1], dist)
        point_2 = rs.rs2_deproject_pixel_to_point(self.color_intrin, [x_2, y_2], dist)

        # Calculate euclidean distance between the two points
        diameter = math.sqrt(math.pow(point_1[0] - point_2[0], 2) + math.pow(point_1[1] - point_2[1],2) + math.pow(point_1[2] - point_2[2], 2))

        # convert m to mm
        return int(diameter * 1000)
