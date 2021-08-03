import pyrealsense2.pyrealsense2 as rs
import bbot.box as Box
import numpy as np

class Camera:
    def __init__(self):
        self.color_frame = False
        self.aligned_depth_frame = False

    def setup(self) -> None:
        # Create a pipeline
        self.pipeline = rs.pipeline()

        # Create a config and configure the pipeline to stream
        #  different resolutions of color and depth streams
        config = rs.config()

        # Get device product line for setting a supporting resolution
        pipeline_wrapper = rs.pipeline_wrapper(self.pipeline)
        pipeline_profile = config.resolve(pipeline_wrapper)

        # todo format 1920x1080
        config.enable_stream(rs.stream.depth, 1280, 720, rs.format.z16, 30)
        config.enable_stream(rs.stream.color, 1280, 720, rs.format.bgr8, 30)

        # Start streaming
        profile = self.pipeline.start(config)

        # Getting the depth sensor's depth scale (see rs-align example for explanation)
        depth_sensor = profile.get_device().first_depth_sensor()
        depth_scale = depth_sensor.get_depth_scale()
        print("Depth Scale is: " , depth_scale)

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
        self.aligned_depth_frame = aligned_frames.get_depth_frame() # aligned_depth_frame is a 640x480 depth image
        color_frame = aligned_frames.get_color_frame()

        # Validate that both frames are valid
        if not self.aligned_depth_frame or not color_frame:
            return

        # self.depth_image = np.asanyarray(aligned_depth_frame.get_data())
        self.color_image = np.asanyarray(color_frame.get_data())

    def get_color_frame(self) -> np.ndarray:
        return self.color_image

    def get_depth_in_mm(self, box: Box) -> int:
        # convert m to m
        x, y = box.get_center()
        depth = int(self.aligned_depth_frame.get_distance(x,y) * 1000)

        return depth

    def get_diameter_in_mm(self, box: Box) -> int:
        # todo get diameter at depth
        return box.get_max_size()
