import time
import datetime
import h5py
import json
import os
import numpy as np

from livenodes.node import Node
from livenodes_core_nodes.ports import Port_Dict, Port_Data, Ports_empty
from typing import NamedTuple

class Ports_in(NamedTuple):
    video: Port_Data = Port_Data("Video")
    meta: Port_Dict = Port_Dict("Meta")

class Out_data(Node):
    ports_in = Ports_in()
    ports_out = Ports_empty()

    category = "Save"
    description = ""

    example_init = {'name': 'Save', 'folder': './data/Debug/'}

    def __init__(self, folder, name="Save", compute_on="1:1", **kwargs):
        super().__init__(name, compute_on=compute_on, **kwargs)

        self.folder = folder

        if not os.path.exists(self.folder):
            os.makedirs(self.folder)

        # NOTE: we can create the filename here (although debatable)
        # but we cannot create the file here, as no processing is being done or even planned yet (this might just be create_pipline)
        self.outputFilename = f"{self.folder}{datetime.datetime.fromtimestamp(time.time())}"
        print("Saving to:", self.outputFilename)

        self.outputFile = None
        self.outputDataset = None

        self.recv_meta = False
        
        self.running = False

        self.buffer = []

    def _settings(self):
        return {\
            "folder": self.folder
        }

    def _onstart(self):
        if not self.running:
            self.running = True
            self.outputFile = h5py.File(self.outputFilename + '.h5', 'w')
            self.info('Created Files')

    def _onstop(self):
        if self.running:
            self.running = False

            self._append_buffer_to_file()
            self.outputFile.close()
            self.info('Stopped writing out and closed files')

    def _should_process(self,
                        video=None,
                        meta=None,):
        return video is not None \
            and (meta is not None or self.recv_meta)


    def process(self,
                video,
                meta=None,
                **kwargs):

        if meta is not None:
            self.recv_meta = True
            m_dict = {**self._read_meta(), **meta}
            self._write_meta(m_dict)
            self.width = m_dict.get('width', 1280)
            self.height = m_dict.get('height', 720)

            if self.outputDataset is None:
                self.outputDataset = self.outputFile.create_dataset(
                    "data", (0, self.height * self.width),
                    maxshape=(None, self.height * self.width),
                    dtype=np.array(video).dtype)

        for frame in video:
            self.buffer.append(np.hstack(frame))

        if len(self.buffer) > 100:
            self._append_buffer_to_file()

    def _append_buffer_to_file(self):
        buff_len = len(self.buffer)
        if buff_len >= 1:
            self.outputDataset.resize(self.outputDataset.shape[0] + buff_len, axis=0)
            self.outputDataset[-buff_len:] = self.buffer
            self.buffer = []

    def _read_meta(self):
        if not os.path.exists(f"{self.outputFilename}.json"):
            return {}
        with open(f"{self.outputFilename}.json", 'r') as f:
            return json.load(f)

    def _write_meta(self, setting):
        with open(f"{self.outputFilename}.json", 'w') as f:
            json.dump(setting, f, indent=2)
