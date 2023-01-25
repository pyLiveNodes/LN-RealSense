import cv2
from PyQt5.QtWidgets import QVBoxLayout, QLabel
from PyQt5 import QtGui
from PyQt5.QtGui import QPixmap
from PyQt5 import QtCore

from .ports import Ports_image_depth
from livenodes_core_nodes.ports import Ports_empty

from livenodes.viewer import View_QT

class Draw_image_depth(View_QT):
    """Draw raw depth images on qt canvas.

    Draws received single raw depth image frames on a qt canvas.
    """

    ports_in = Ports_image_depth()
    ports_out = Ports_empty()

    category = "Draw"
    description = ""

    example_init = {
        "name": "Image Render",
    }

    def _init_draw(self, parent):
        """
        Visualize video framewise.
        """
        self.frame_label = QLabel()

        layout = QVBoxLayout(parent)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.frame_label)
        self.frame_label.setAlignment(QtCore.Qt.AlignCenter)

        def update(data=[]):
            playback_colormap = self.convert_cv_to_qt(data)
            self.frame_label.setPixmap(playback_colormap)

        return update

    def process(self, depth_image,  **kwargs):  
        self._emit_draw(data=depth_image)

    def convert_cv_to_qt(self, cv_img):
        """
        Convert from an opencv image to QPixmap.
        Code source: https://github.com/docPhil99/opencvQtdemo/blob/master/staticLabel2.py
        """
        rgb_image = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
        height, width, channels = rgb_image.shape
        bytes_per_line = channels * width
        convert_to_Qt_format = QtGui.QImage(rgb_image.data, width, height, bytes_per_line, QtGui.QImage.Format_RGB888)

        return QPixmap.fromImage(convert_to_Qt_format)