import time
import datetime
import os
import imageio as iio

from livenodes.node import Node

from .ports import Ports_image_rgb, Ports_empty

class Out_colorised(Node):
    """Saves rgb images to .avi video files.

    Expects single rgb images, which are saved lossless or lossy compressed into <folder><timestamp>.avi files.
    """
    
    ports_in = Ports_image_rgb()
    ports_out = Ports_empty()

    category = "Save"
    description = ""

    example_init = {'name': 'Save', 'folder': './data/Debug/', "lossless": True}

    def __init__(self, folder, lossless=True, name="Save", **kwargs):
        super().__init__(name, **kwargs)

        self.folder = folder
        self.lossless = lossless

        if not os.path.exists(self.folder):
            os.makedirs(self.folder)

        # NOTE: we can create the filename here (although debatable)
        # but we cannot create the file here, as no processing is being done or even planned yet (this might just be create_pipline)
        self.save_loc = f"{self.folder}{datetime.datetime.fromtimestamp(time.time())}.avi"

        self.writer = None

    def _settings(self):
        return {\
            "folder": self.folder,
            "lossless": self.lossless
        }

    def _onstart(self):
        if self.writer is None:
            if self.lossless:
                self.writer = iio.get_writer(self.save_loc, fps=self.fps, mode="I", format='FFMPEG', quality=None, codec="libx264rgb", pixelformat="rgb24", output_params=['-crf', '0', # Ensure setting crf to 0
                                '-preset', 'ultrafast']) # Maximum compression: veryslow, 
                                                        # maximum speed: ultrafast)
            else:
                self.writer = iio.get_writer(self.save_loc, fps=self.fps, mode="I", format='FFMPEG', quality=10, codec="libx264rgb", pixelformat="rgb24")

            self.info('Created writer')

    def _onstop(self):
        if self.writer is not None:
            self.writer.close()
            self.writer = None

    def process(self, image_color, **kwargs):
        self.writer.append_data(image_color)