from livenodes.producer_blocking import Producer_Blocking

from livenodes_core_nodes.ports import Ports_empty
from .ports import Ports_image_depth

import pyrealsense2 as rs
import numpy as np

class In_realsense(Producer_Blocking):
    """Realsense input, raw depth.

    Connects to a RealSense and feeds single depth images into subsequent nodes.

    Requires librealsense and pyrealsense2 libaries.
    """

    ports_in = Ports_empty()
    ports_out = Ports_image_depth()

    category = "Data Source"
    description = ""

    example_init = {
        "width": 1280,
        "height": 720,
        "fps": 30,
        "options": {},
        "name": "RealSense Input",
    }

    def __init__(self,
                 width=1280,
                 height=720,
                 fps=30,
                 options={},
                 name="RealSense Input",
                 **kwargs):
        super().__init__(name, **kwargs)

        self.width = width
        self.height = height
        self.fps = fps
        self.options = options

        self.run = True

    def _settings(self):
        return {\
            "width": self.width,
            "height": self.height,
            "fps": self.fps,
            "options": self.options
        }

    def _onstop(self):
        self.run = False
        self.pipeline.stop()

    def setup(self):
        ### --- Setup RealSense connection ----------------------------------------
        self.pipeline = rs.pipeline()
        self.config = rs.config()

        # Get device product line for setting a supporting resolution
        pipeline_wrapper = rs.pipeline_wrapper(self.pipeline)
        pipeline_profile = self.config.resolve(pipeline_wrapper)
        self.device = pipeline_profile.get_device()

        device_product_line = str(self.device.get_info(rs.camera_info.product_line))
        self.serial_number = str(self.device.get_info(rs.camera_info.serial_number))
        print(f"Found RealSense: {device_product_line} - {self.serial_number}")

        depth_sensor = self.device.first_depth_sensor()
        for key, val in self.options.items():
            if hasattr(rs.option, key):
                depth_sensor.set_option(getattr(rs.option, key), val)
                print(f"Set option: {key} to {str(val)}")
            else:
                print(f"Unknown option: {key}")

        self.config.enable_stream(rs.stream.depth, self.width, self.height, rs.format.z16, self.fps)


    def _blocking_onstart(self):
        """
        Streams the data and calls frame callbacks for each frame.
        """

        self.setup()

        self.pipeline.start(self.config)
        
        while self.run:
            # Wait for a coherent pair of frames: depth and color
            # yh: called "frames" as this might be multiple streams, but only retrives one time frame
            # streams = queue.wait_for_frame()
            streams = self.pipeline.wait_for_frames() # blocking, TODO: add timeout, such that the outer function can return even if this blocks forever (because no frame is received)
            depth_frame = streams.get_depth_frame()

            # Convert images to numpy arrays
            depth_image = np.asanyarray(depth_frame.get_data(), dtype=np.int16)
            self.msgs.put_nowait((depth_image, "depth_image", True))
