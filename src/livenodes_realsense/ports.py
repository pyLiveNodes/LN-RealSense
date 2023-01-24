from livenodes_core_nodes.ports import Port_Data
from typing import NamedTuple

class Ports_video(NamedTuple):
    video: Port_Data = Port_Data("Video")

class Ports_depth_video(NamedTuple):
    # (Time, Widht, Height)
    depth: Port_Data = Port_Data("Depth")
