import cv2
from PyQt5 import QtGui
from PyQt5.QtGui import QPixmap

from .draw_image_depth import Draw_image_depth
from .ports import Ports_image_rgb



class Draw_image_rgb(Draw_image_depth):
    """Draw rgb images on qt canvas.

    Draws received single rgb image frames on a qt canvas.
    """

    ports_in = Ports_image_rgb()

    def process(self, image,  **kwargs):  
        self._emit_draw(data=image)
    
    def convert_cv_to_qt(self, cv_img):
        """
        Convert from an opencv image to QPixmap.
        Code source: https://github.com/docPhil99/opencvQtdemo/blob/master/staticLabel2.py
        """
        rgb_image = cv2.cvtColor(cv_img) # i think we don't need any conversion, as this should already be rgb
        height, width, channels = rgb_image.shape
        bytes_per_line = channels * width
        convert_to_Qt_format = QtGui.QImage(rgb_image.data, width, height, bytes_per_line, QtGui.QImage.Format_RGB888)

        return QPixmap.fromImage(convert_to_Qt_format)