from livenodes_core_nodes.ports import Port_TS_Int, Port_Matrix_Int
from typing import NamedTuple


class Ports_image_rgb(NamedTuple):
    # (Width, Height, RGB), is somewhat similar to (batch, time, channel)
    image_color: Port_TS_Int = Port_TS_Int("Image")

class Ports_image_depth(NamedTuple):
    # (Widht, Height)
    image_depth: Port_Matrix_Int = Port_Matrix_Int("Depth Image")
