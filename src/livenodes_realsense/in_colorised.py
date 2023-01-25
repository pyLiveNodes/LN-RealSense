from functools import reduce
import numpy as np
from glob import glob
import random
import imageio as iio

from livenodes.producer import Producer

from .ports import Ports_image_rgb
from livenodes_core_nodes.ports import Ports_empty


class In_colorised(Producer):
    """Reads rgb images from .avi video files.

    Emits single rgb images from compressed .avi files.
    """
    ports_in = Ports_empty()
    ports_out = Ports_image_rgb()

    category = "Data Source"
    description = ""

    example_init = {
        "files": "./files/**.h5",
        "files_exclude": './files/part0*.h5',
        "name": "Data input",
        "shuffle": True,
    }

    def __init__(self,
                 files,
                 files_exclude = '',
                 shuffle=True,
                 name="Data input",
                 **kwargs):
        super().__init__(name, **kwargs)

        self.files = files
        self.files_exclude = files_exclude
        self.shuffle = shuffle

    def _settings(self):
        return {\
            "files": self.files,
            "files_exclude": self.files_exclude,
            "shuffle": self.shuffle,
        }

    def _run(self):
        """
        Streams the data and calls frame callbacks for each frame.
        """
        fs = sorted(list(set(glob(self.files)) - set(glob(self.files_exclude))))

        if self.shuffle:
            random.shuffle(fs)

        self.info('Reading these files (in this order):', fs)

        # TODO: add loading in background
        # TODO: add chunking
        # TODO: add percentage read/sent and/or other meta information

        for file_name in fs:
            # iterate over large videos
            for frame in iio.imiter(file_name, plugin="ffmpeg"):
                yield self.ret(image_color=frame)
