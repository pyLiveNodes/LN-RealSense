import cv2
import numpy as np
from PyQt5 import QtGui
from PyQt5.QtGui import QPixmap

from .draw_image_depth import Draw_image_depth
from .ports import Ports_image_rgb



class Draw_image_rgb(Draw_image_depth):
    """Draw rgb images on qt canvas.

    Draws received single rgb image frames on a qt canvas.
    """

    ports_in = Ports_image_rgb()

    def process(self, image_color,  **kwargs):  
        self._emit_draw(data=image_color)
    
    def convert_cv_to_qt(self, cv_img):
        rgb_image = np.array(cv_img)
        height, width, channels = rgb_image.shape
        bytes_per_line = channels * width
        convert_to_Qt_format = QtGui.QImage(rgb_image.data, width, height, bytes_per_line, QtGui.QImage.Format_RGB888)

        return QPixmap.fromImage(convert_to_Qt_format)