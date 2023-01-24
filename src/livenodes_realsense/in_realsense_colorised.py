from .in_realsense import In_realsense

from .ports import Ports_image_rgb

import pyrealsense2 as rs
import numpy as np

class In_realsense_colorised(In_realsense):
    """Realsense input, colorized depth.

    Connects to a RealSense and feeds single depth images into subsequent nodes.

    Requires librealsense and pyrealsense2 libaries.
    """

    ports_out = Ports_image_rgb()

    def _blocking_onstart(self):
        """
        Streams the data and calls frame callbacks for each frame.
        """

        self.setup()
        colorizer = rs.colorizer()

        self.pipeline.start(self.config)
        
        while self.run:
            # Wait for a coherent pair of frames: depth and color
            # yh: called frames as this might be multiple streams, but only retrives one time frame
            # streams = queue.wait_for_frame()
            streams = self.pipeline.wait_for_frames() # blocking, TODO: add timeout, such that the outer function can return even if this blocks forever (because no frame is received)
            depth_frame = streams.get_depth_frame()

            depth_color_frame = colorizer.colorize(depth_frame)

            # Convert images to numpy arrays
            colorized_depth_image = np.asanyarray(depth_color_frame.get_data(), dtype=np.int8)
            self.msgs.put_nowait((colorized_depth_image, "image", True))
