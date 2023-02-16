from glob import glob
import random
import imageio.v3 as iio
import time
import asyncio

from livenodes.producer_async import Producer_async

from .ports import Ports_image_rgb
from livenodes_core_nodes.ports import Ports_empty


class Playback_colorised(Producer_async):
    """Playback rgb images in normal/viewing time.

    Feeds rgb images one by one with the videos' fps rate into the subsequent nodes.
    """
    ports_in = Ports_empty()
    ports_out = Ports_image_rgb()

    category = "Data Source"
    description = ""

    example_init = {
        "files": "./data/realsense/**.avi",
        "files_exclude": '',
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

    async def _async_run(self):
        """
        Streams the data and calls frame callbacks for each frame.
        """
        fs = sorted(list(set(glob(self.files)) - set(glob(self.files_exclude))))

        if self.shuffle:
            random.shuffle(fs)

        self.info('Reading these files (in this order):', fs)
        last_time = time.time()

        for file_name in fs:
            sleep_time = 1.0/iio.immeta(file_name)["fps"]
            
            # iterate over large videos
            for frame in iio.imiter(file_name):
                while time.time() < last_time + sleep_time + 0.0001:
                    await asyncio.sleep(0.0001)

                last_time = time.time()
                yield self.ret(image_color=frame)
